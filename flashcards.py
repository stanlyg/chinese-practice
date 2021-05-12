#!/bin/python3

from fpdf import FPDF
import json
import configargparse

default_config_file = './flashcards.ini'

parser = configargparse.ArgParser(default_config_files=[default_config_file], 
  ignore_unknown_config_file_keys=True)
parser.add_argument("wordlist",help="List of words to use for the page, in JSON format")
parser.add_argument("output",help="Name of PDF file to output")
parser.add_argument("-c","--config",help="""
    Specify configration file to use. Command line options override 
    the config file. Defaults to writing-page.ini in the current
    directory.""",is_config_file=True)
parser.add_argument("-s","--save",action='store',help="""
    Save configuration file to specified name. Use it later with 
    the --config option.""",is_write_out_config_file_arg=True)
parser.add_argument("--page-size",nargs=2,default=[5,3],metavar=('WIDTH','HEIGHT'),type=float,help="""
    Specify page width and height. All size units are in inches.""")
parser.add_argument("--margins",nargs=2,default=[0.25,0.5],metavar=('VERTICALMARGIN','HORIZONTALMARGIN'),type=float,help="""
    Page Vertical (top/bottom) and Horizional (left/right) margins. 
    Text will be horizontally centered between the margins.""")
parser.add_argument("--square-size",default=2,type=float, help="""
    Size of squares for Chinese characters. Font is autoscaled to 8/9 of the box size.""")
parser.add_argument("--pinyin-height",default=0.5,type=float, help="Height of pinyin text.")
parser.add_argument("--english-height",default=0,type=float, help="Height of english text, uses pinyin-height if unspecified")
parser.add_argument("--font",default='fireflysung.ttf',help="""
    Font to use for Chinese characters. The file fireflysung.ttf should
    have been included with this script. This font must include the 
    Chinese characters to work.""")
parser.add_argument("--pinyinfont",default="",help="""
    Font to use for pinyin characters. This font must include accented 
    latin characters (macron, grave, caron, and acute) to work properly. 
    Uses Chinese font if not specified. The fireflysung.ttf file includes
    the required characters.""")
parser.add_argument("--englishfont",default="",help="""
    Font to use for English definitions. Uses Pinyin font if not specified.""")
parser.add_argument("-v","--verbose",default=0,action='count',help="Verbose output, increasing the number of v's increases verbosity.")
options = parser.parse_args()

if len(options.pinyinfont) == 0:
    options.pinyinfont = options.font
if len(options.englishfont) == 0:
    options.englishfont = options.pinyinfont

# Rename some options with more useful names
options.page_width = options.page_size[0]
options.page_height = options.page_size[1]
options.vmargin = options.margins[0]
options.hmargin = options.margins[1]

# horizontal center, less width
zhongleft = ( options.page_width - options.square_size ) / 2

# full width, less horizontal margins
options.pinyin_width = options.page_width - 2 * options.hmargin

if options.english_height == 0:
  options.english_height = options.pinyin_height
options.english_width = options.pinyin_width

class PDF(FPDF):
  def header(self):
    pass

def pinyintext(p,x,y,w,h,s):
  if options.verbose >= 2:
    print (f'x: {x}, y: {y}, w: {w}, h: {h}, s: {s}')
  p.set_text_color(255,0,0)
  p.set_xy(x,y)
  p.set_font('pinyin','',64*h) # approx 90% height
  p.cell(w,h,s,align='C')

def zhongtext(p,x,y,w,h,s):
  if options.verbose >= 2:
    print (f'x: {x}, y: {y}, w: {w}, h: {h}, s: {s}')
  p.set_text_color(0)
  p.set_xy(x,y+(0.1*h)) # offset y 10% for font rendering
  p.set_font('zhongwen','',64*h) # approx 90% height
  p.cell(w,h,s,align='C') 

def englishtext(p,w,h,s):
  p.set_text_color(0,0,255)
  p.set_font('english','',64*h) # approx 90% height
  lines = p.multi_cell(w,h,s,align='C',split_only=True)
  x = options.hmargin
  y = options.page_height / 2 - len(lines) * h / 2
  if options.verbose >= 2:
    print (f'x: {x}, y: {y}, w: {w}, h: {h}, s: {s}')
  p.set_xy(x, y)
  p.multi_cell(w,h,s,align='C')

pdf = PDF('L','in',(options.page_size[1],options.page_size[0]))

pdf.set_margin(0)
pdf.add_font('zhongwen','',options.font,uni=True)
pdf.add_font('pinyin','',options.pinyinfont,uni=True)
pdf.add_font('english','',options.englishfont,uni=True)

with open(options.wordlist,"r") as f:
  wordlist = json.load(f)

pdf.set_auto_page_break(False)

#x = leftmargin
for w, d in wordlist.items():
  pdf.add_page()
  if options.verbose:
    print (f'Word: {w}, pinyin: {d["pinyin"]}, english: {d["english"]}')
  y = options.vmargin
  pinyintext (pdf, options.hmargin, y, options.pinyin_width, options.pinyin_height, d["pinyin"]) 

  y = y + options.pinyin_height
  zhongtext (pdf, zhongleft, y, options.square_size, options.square_size, w)

  pdf.add_page()
    
  englishtext(pdf, options.english_width, options.english_height, d["english"])

pdf.output(options.output, 'F')