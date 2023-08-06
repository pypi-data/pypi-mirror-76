# -*- coding: utf-8 -*-
import re, os, locale
from os import path
from docutils import nodes
from docutils.parsers import rst
import shutil
from PIL import Image, ImageFont, ImageDraw
try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

OUTPUT_DEFAULT_FORMATS = dict(html='.html', latex='.png', text='.txt')
IMAGE_DEFAULT_FONT = 'NSimSun, simsun, monospace'
IMAGE_DEFAULT_FONT_SIZE = 14

#: the pattern to find ANSI color codes
#COLOR_PATTERN = re.compile('\x1b\\[([^m]+)m')
COLOR_PATTERN = re.compile('(\[([^m]*)m)')

#: map ANSI color codes to class names
CODE_NAME_MAP = {0: ("white", "bold-white"),
        30: ("black", "bold-black"),
        31: ("red", "bold-red"),
        32: ("green", "bold-green"),
        33: ("yellow", "bold-yellow"),
        34: ("blue", "bold-blue"),
        35: ("magenta", "bold-magenta"),
        36: ("cyan", "bold-cyan"),
        37: ("white", "bold-white"),
        40: ('bg_black', 'bg_black'),
        41: ('bg_red',   'bg_red'),
        42: ('bg_green', 'bg_green'),
        43: ('bg_yellow','bg_yellow'),
        44: ('bg_blue',  'bg_blue'),
        45: ('bg_magenta''bg_magenta'),
        46: ('bg_cyan',  'bg_cyan'),
        47: ('bg_white', 'bg_white') }

CODE_CLASS_MAP = {0: ("#b2b2b2", "#ffffff"), #white
        30: ("#111111", "#686868"),          #black
        31: ("#b21717", "#ff5454"),          #red
        32: ("#17b217", "#54ff54"),          #green
        33: ("#b26717", "#ffff54"),          #yellow
        34: ("#1717b2", "#5454ff"),          #blue
        35: ("#b217b2", "#ff54ff"),          #magenta
        36: ("#17b2b2", "#54ffff"),          #cyan
        37: ("#b2b2b2", "#ffffff"),          #white
        40: ('#111111', "#111111"),          #bg_black
        41: ('#b21717', "#b21717"),          #bg_red
        42: ('#17b217', "#17b217"),          #bg_green
        43: ('#b26717', "#b26717"),          #bg_yellow
        44: ('#1717b2', "#1717b2"),          #bg_blue
        45: ('#b217b2', "#b217b2"),          #bg_magenta
        46: ('#17b2b2', "#17b2b2"),          #bg_cyan
        47: ('#b2b2b2', "#b2b2b2"),          #bg_white
        }

class Text2Image(object):
    '''
    PILLOW Image file formats, https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html

    '''
    def __init__(self, text, **kwargs):
        '''
        '''
        #解析选项: font, fontsize, 注意处理一些非法的字符
        self.font = self._get_image_font(kwargs.get("font",
                                    'NSimSun, simsun, monospace'),
                                    kwargs.get("fontsize", 14))
        if not self.font:
            print("No readable font, return")
            return

        # 解析选项: line-height, spacing, 注意处理一些非法的字符
        self.line_height = self._get_image_line_height(self.font,
                kwargs.get("line-height", "1.0em"))
        self.line_height += kwargs.get("spacing", -1)

        # 初始化
        self.fg_color_index = 0  # 前景色index
        self.bg_color_index = 40  # 背景色index
        self.is_bold = 0          # 前景色是否加粗
        self.cursor = [0, 0]     # 当前的光标位置, for PIL image.

        width = max(self.font.getsize(COLOR_PATTERN.sub('', line))[0] for line in text)
        height = (len(text))*(self.line_height)

        try:
            # call PILLOW to write the text into a image file;
            self.pil_image = Image.new(mode = "RGB", size = (width, height),
                    color = (0x11, 0x11, 0x11))
            self.pil_draw = ImageDraw.Draw(self.pil_image)
        except Exception:
            return

    def _get_image_font (self, fontname = 'simsun, monospace', fontsize = 14):
        '''
        解析选项: font, fontsize, 注意处理一些非法的字符
        '''
        directory_list = ["./",
                "/usr/local/share/fonts/",
                "/usr/share/fonts/",
                "C:\\WINDOWS\\Fonts\\"]
        suffix_list = ["", ".ttf", ".ttc"]
        for f in fontname.split(','):
            for suffix in suffix_list:
                for directory in directory_list:
                    name = path.join(directory, f.strip()) + suffix
                    try:
                        font = ImageFont.truetype(name, fontsize, encoding="unic")
                        return font
                    except Exception:
                        continue
                    if f.endswith('.ttf') or f.endswith('.ttc'):
                        break
        return None

    def _get_image_line_height (self, font, high = '1.0em'):
        '''
        解析选项: font, fontsize, 注意处理一些非法的字符
        '''
        # 解析选项: letter-spacing, 注意处理一些非法的字符

        try:
            basic_high = font.getsize("_")[1]
        except Exception:
            basic_high = font.getsize("A")[1]+2
        if "px" in high:
            basic_high = high.split('px')[0]
        elif "em" in high:
            basic_high = basic_high*(float(high.split('em')[0]))
        else:
            try:
                basic_high = basic_high + int(high)
            except Exception:
                return int(basic_high)
        return int(basic_high)

    def parse_a_node (self, control_block, color_name = True):
        '''
        Draw a line on the canvas and move the cursor to the start of the next
        line.
        '''
        # 非贪婪模式
        match = re.match(r'[\d;]*?m', control_block, re.M|re.I)
        if match:
            m_index = len(match.group())
            codes = control_block[0:m_index-1].split(";")
            for code in codes:
                try:
                    n = int(code)
                except Exception:
                    n = 0

                if n >= 30 and n <= 37:
                    self.fg_color_index = n
                elif n >= 40 and n <= 47:
                    self.bg_color_index = n
                elif n == 1:
                    self.is_bold = 1
                elif n == 0:
                    self.is_bold = 0
                    self.fg_color_index = 0
                    self.bg_color_index = 40
        else:
            m_index = 0

        if color_name:
            return (CODE_NAME_MAP[self.fg_color_index][self.is_bold],
                    CODE_NAME_MAP[self.bg_color_index][0],
                    control_block[m_index:])
        else:
            return (CODE_CLASS_MAP[self.fg_color_index][self.is_bold],
                    CODE_CLASS_MAP[self.bg_color_index][0],
                    control_block[m_index:])

    def draw_string(self, fg_color, bg_color, string):
        '''
        Draw a string on the canvas and move the cursor to the end.
        '''
        text_size = self.pil_draw.textsize(string, font = self.font)
        self.pil_draw.rectangle([self.cursor[0],
            self.cursor[1],
            self.cursor[0] + text_size[0],
            self.cursor[1] + self.line_height],
            fill=bg_color)
        # 当行距不足时，会覆盖上一行几个像素的数据。将文本往上画一行，这样当
        # spacing=-2 时上下各覆盖一个像素而不是覆盖下面的两个像素
        self.pil_draw.text((self.cursor[0], self.cursor[1]-1),
                string, font = self.font, fill = fg_color)
        self.cursor[0] += text_size[0]

    def parse_asciiart_literal_to_html (self, app, block):
        # html mode is only supported by html output
        if app.builder.name == 'text':
            return pil.asciiart_litedral_block_to_text(app, block)
        elif app.builder.name != 'html':
            return pil.asciiart_litedral_block_to_image(app, img, "png")

        # create the "super" node, which contains to while block and all it
        # sub nodes, and replace the old block with it
        literal_node = nodes.literal_block()
        literal_node['classes'].append('ansi-block')
        block.replace_self(literal_node)

        # devide the txt to nodes by '\x1B['. txt[i] is color + text;
        txt = '\n'.join(block.asciiart["text"]).split('\x1B[')
        for i in range(0, len(txt)):
            (fg_color, bg_color, text) = self.parse_a_node(txt[i], True)
            # Add the color/text into the list;
            code_node = nodes.inline()
            code_node['classes'].append('ansi-%s' % fg_color)
            code_node['classes'].append('ansi-%s' % bg_color)
            code_node.append(nodes.Text(text))
            literal_node.append(code_node) # and add the nodes to the block
        print("rending asciiart literal block in html format")

    def asciiart_litedral_block_to_text (self, app, block):
        # strip all color codes in non-html output
        content = COLOR_PATTERN.sub('', block.rawsource)
        literal_node = nodes.literal_block(content, content)
        block.replace_self(literal_node)
        print("rending asciiart literal block in plain text format")

    def asciiart_litedral_block_to_image (self, app, img, suffix):
        #hashkey = sha('\n'.join(img.asciiart['text']).encode('utf-8')).hexdigest()
        hashkey = str(img.asciiart['text']) + str(img.asciiart['options']) +\
                str(app.builder.config.ascii_art_image_fontsize) +\
                str(app.builder.config.ascii_art_image_font)
        hashkey = sha(hashkey.encode('utf-8')).hexdigest()

        outfname = 'asciiart-%s.%s' %(hashkey, suffix.strip("."))
        out = dict(outrelfn=None,outfullfn=None,outreference=None)
        out["outrelfn"] = path.join(app.builder.imagedir, outfname)
        out["outfullfn"] = path.join(app.builder.outdir, app.builder.imagedir, outfname)

        if ((not img.get('height', None))
                and (not img.get('width', None))
                and (not img.get('scale', None))):
            # Keep the original height x width to avoid to magnify in pdf
            img['height'] = "%d" %(self.pil_image.height)
        if path.isfile(out["outfullfn"]):
            # 如果图片已经存在就不用再生成一次.
            img['uri'] = out["outrelfn"]
            return
        #out["outreference"] = posixpath.join(rel_imgpath, infname)

        for line in img.asciiart['text']:
            #print(font.getsize(COLOR_PATTERN.sub('', line)))
            txt = line.split('\x1B[')
            for i in range(0, len(txt)):
                (fg_color, bg_color, t) = self.parse_a_node(txt[i], False)
                self.draw_string(fg_color, bg_color, t)
            self.cursor[0] = 0
            self.cursor[1] += self.line_height
        imagedir = path.join(app.builder.outdir, app.builder.imagedir)

        if not os.path.exists(imagedir):
            os.mkdir(imagedir)
        self.pil_image.save(out["outfullfn"])
        print("asciiart literal block --> %s" %(outfname))
        img['uri'] = out["outrelfn"]
        if out["outreference"]:
            reference_node = nodes.reference(refuri=out["outreference"])
            img.replace_self(reference_node)
            reference_node.append(img) 

def render_asciiart_images(app, doctree):
    for img in doctree.traverse(nodes.image):
        if not hasattr(img, 'asciiart'):
            continue

        try:
            format_map = OUTPUT_DEFAULT_FORMATS.copy()
            format_map.update(app.builder.config.ascii_art_output_format)
            output_format = format_map.get(app.builder.name, "png")
        except:
            output_format = "png"

        global_option = {}
        if not img.asciiart['options'].get('font', None):
            global_option["font"] = app.builder.config.ascii_art_image_font \
                    and app.builder.config.ascii_art_image_font \
                    or IMAGE_DEFAULT_FONT
        if not img.asciiart['options'].get('fontsize', None):
            global_option["fontsize"] = app.builder.config.ascii_art_image_fontsize \
                    and app.builder.config.ascii_art_image_fontsize \
                    or IMAGE_DEFAULT_FONT_SIZE

        pil = Text2Image(img.asciiart['text'], **img.asciiart['options'], **global_option)
        if hasattr(img, 'asciiart'):
            if output_format.lower() in [".html", "html"]:
                pil.parse_asciiart_literal_to_html(app, img)
            elif output_format.lower() in [".txt", "txt"]:
                pil.asciiart_litedral_block_to_text(app, img)
            elif output_format.lower() in [ "bmp", ".bmp", "dib", ".dib",
                    "eps", ".eps", "gif", ".gif", "icns", ".icns", "ico",
                    ".ico", "im",  ".im", "jpg", ".jpg", "jpeg", ".jpeg",
                    "msp", ".msp", "pcx", ".pcx", "png", ".png", "ppm", ".ppm",
                    "sgi", ".sgi", "spider", ".spide", "tga", ".tga", "tiff",
                    ".tiff", "webp", ".webp", "xbm", ".xbm", "palm", ".palm",
                    "pdf", ".pdf", "xv",  ".xv", "bufr", ".bufr", "fits", ".fits",
                    "grib", ".grib", "hdf5", ".hdf5", "mpeg", ".mpeg"]:
                pil.asciiart_litedral_block_to_image(app, img, output_format)
            else:
                print("Not supported suffix: %s, convert it to plain text" %(output_format))
                pil.asciiart_litedral_block_to_text(app, img)

class AsciiArtDirective(rst.directives.images.Image):
    """

    https://learn-rst.readthedocs.io/zh_CN/latest/reST-%E6%89%A9%E5%B1%95/reST-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%89%A9%E5%B1%95.html
    The asciiart directive parse the color in the literal block and render
    them:

    .. asciiart:: 

        ascii art block.

    """
    # this enables content in the directive
    has_content = True
    required_arguments = 0
    own_option_spec = dict({
        'line-height': str,
        'spacing': int,
        'font': str,
        'fontsize': int,
        'suffix': str,
        })

    option_spec = rst.directives.images.Image.option_spec.copy()
    option_spec.update(own_option_spec)
    def run(self):
        '''
        This method must process the directive arguments, options and content,
        and return a list of Docutils/Sphinx nodes that will be inserted into
        the document tree at the point where the directive was encountered.
        '''
        self.arguments = ['']
        asciiart_options = dict([(k,v) for k,v in self.options.items() 
                                        if k in self.own_option_spec])

        # 因为在这里读不到app.builder.config.ascii_art_output_format 的值，
        # 所以我们把所有的节点初始化为image 节点，以后需要的时候再替换成
        # literal_block
        (img_node,) = rst.directives.images.Image.run(self)
        img_node.asciiart = dict(text=self.content, options=asciiart_options,
                suffix="asciiart", directive="asciiart")
        return [img_node]

def add_stylesheet(app):
    app.add_css_file('asciiart.css')

def copy_stylesheet(app, exception):
    # Copy the style sheet to the dest _static directory
    if app.builder.name != 'html' or exception:
        return
    dest = path.join(app.builder.outdir, '_static', 'asciiart.css')
    source = path.join(path.dirname(__file__), 'asciiart.css')
    try:
        shutil.copy(source, dest)
    except:
        print('Fail to copy %s to %s.' %(source, dest))


def setup(app):
    app.add_directive('asciiart', AsciiArtDirective)
    #app.connect('doctree-resolved', AsciiArtParser())
    app.connect('doctree-read', render_asciiart_images)
    app.connect('builder-inited', add_stylesheet)
    app.connect('build-finished', copy_stylesheet)
    app.add_config_value('ascii_art_output_format', OUTPUT_DEFAULT_FORMATS, 'html')
    app.add_config_value('ascii_art_image_font', IMAGE_DEFAULT_FONT, 'html')
    app.add_config_value('ascii_art_image_fontsize', IMAGE_DEFAULT_FONT_SIZE, 'html')
