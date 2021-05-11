#!/bin/python3

from fpdf import FPDF
import json
import configargparse

default_config_file = './writing-page.ini'
parser = configargparse.ArgParser(default_config_files=[default_config_file],
    ignore_unknown_config_file_keys=True)
parser.add_argument("wordlist",help="List of words to use for the page, in JSON format")
parser.add_argument("output",help="Name of PDF file to output")
parser.add_argument("-c","--config",help="""
    Specify configration file to use. Command line options override 
    the config file. Defaults to writing-page.ini in the current
    directory.""",is_config_file=True)
parser.add_argument("-s","--save",action='store',help="Save configuration file to specified name. Use it later with the --config option.",is_write_out_config_file_arg=True)
parser.add_argument("--page-size",nargs=2,default=(8.5,11),type=float,help="Specify page width and height. All size units are in inches.")
parser.add_argument("--top-margin",default=0.25,type=float,help="Page top margin.")
parser.add_argument("--left-margin",default=0.25,type=float, help="Page left margin.")
parser.add_argument("--square-size",default=.7,type=float, help="Size of squares for Chinese characters. Font is autoscaled to 8/9 of the box size.")
parser.add_argument("--pinyin-height",default=0.25,type=float, help="Height of pinyin text.")
parser.add_argument("--vspace",default=0.1,type=float, help="Vertical space between bottom of square and top of pinyin.")
parser.add_argument("--hspace",default=0.15,type=float, help="Horizontal space between columns.")
parser.add_argument("--font",default='fireflysung.ttf',help="Font to use for Chinese characters. This font must include the Chinese characters to work.")
parser.add_argument("--pinyinfont",default="",help="Font to use for pinyin characters. This font must include accented latin characters (macron, grave, caron, and acute) to work properly. Uses Chinese font if not specified.")
parser.add_argument("--englishfont",default="",help="Font to use for English definitions. Uses Pinyin font if not specified.")
parser.add_argument("-v","--verbose",action='store_true')
options = parser.parse_args()

if len(options.pinyinfont) == 0:
    options.pinyinfont = options.font
if len(options.englishfont) == 0:
    options.englishfont = options.pinyinfont

topmargin = options.top_margin
leftmargin = options.left_margin
maxwidth = options.page_size[0]
maxheight = options.page_size[1]

zh = options.square_size  #zhong height
zw = options.square_size #zhong width
ph = options.pinyin_height  #pinyin height
pw = options.square_size   #pinyin width

vs = options.vspace #vert space
hs = options.hspace #horiz space

class PDF(FPDF):
  def header(self):
    addgrid(leftmargin,topmargin,maxwidth,maxheight,zw,zh,ph+vs,hs)

def drawsplitbox(p,x,y,w,h):
  #print (f'rect x: {x}, y: {y}, w: {w}, h: {h}')
  p.set_draw_color(0)
  p.rect(x,y,w,h)
  p.set_draw_color(0,255,255)
  p.dashed_line(x+w/2, y,     x+w/2, y+h  ,0.05,0.05)
  p.dashed_line(x    , y+h/2, x+w  , y+h/2,0.05,0.05)

def pinyintext(p,x,y,w,h,s):
  if options.verbose:
    print (f'x: {x}, y: {y}, w: {w}, h: {h}, s: {s}')
  p.set_text_color(255,0,0)
  p.set_xy(x,y)
  p.set_font('pinyin','',64*h) # approx 90% height
  p.cell(w,h,s,align='C')

def zhongtext(p,x,y,w,h,s):
  if options.verbose:
    print (f'x: {x}, y: {y}, w: {w}, h: {h}, s: {s}')
  p.set_text_color(0)
  p.set_xy(x,y+(0.1*h)) # offset y 10% for font rendering
  p.set_font('zhongwen','',64*h) # approx 90% height
  p.cell(w,h,s,align='C') 

def englishtext(p,x,y,w,h,s):
  if options.verbose:
    print (f'x: {x}, y: {y}, w: {w}, h: {h}, s: {s}')
  p.set_text_color(0,0,255)
  p.set_xy(x,y)
  p.set_font('english','',64*h) # approx 90% height
  p.cell(w,h,s,align='L')


def addgrid(leftm,topm,pagew,pageh,boxw,boxh,vpad,hpad): 
  y = topm + vpad
  while y < pageh: 
    x = leftm
    while x < pagew: 
      drawsplitbox(pdf, x, y, boxw, boxh)
      x = x + boxw + hpad
    y = y + boxh + vpad

pdf = PDF('P','in',[options.page_size[0],options.page_size[1]])

#pdf.add_font('zhongwen','','fireflysung.ttf',uni=True)
pdf.add_font('zhongwen','',options.font,uni=True)
pdf.add_font('pinyin','',options.pinyinfont, uni=True)
pdf.add_font('english','',options.englishfont, uni=True)

pdf.add_page()

with open(options.wordlist,"r") as f:
  wordlist = json.load(f)

  

pdf.set_auto_page_break(False)

x = leftmargin
row = 0
for w, d in wordlist.items():
  if options.verbose:
    print (f'Word: {w}, pinyin: {d["pinyin"]}, english: {d["english"]}')
  y = topmargin + row * (vs + ph + zh) + vs
  pinyintext (pdf, x, y, pw, ph, d["pinyin"]) 

#  savex = x
  x = x + pw + hs
  ew = maxwidth - leftmargin - pw
  englishtext(pdf, x, y, ew, ph, d["english"])
  pdf.set_xy(x,y)
#  pdf.cell(4,ph,d["english"])

  x = leftmargin

  y = y + ph
  zhongtext (pdf, x, y, zw, zh, w)

  row = row + 1

  if pdf.get_y() + zh > maxheight:
    pdf.add_page()
    row = 0


pdf.output(options.output, 'F')
