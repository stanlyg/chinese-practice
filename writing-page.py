#!/bin/python3

from fpdf import FPDF
import json

topmargin = .2
leftmargin = .5
maxwidth = 8
maxheight = 10.5

zh = .7  #zhong height
zw = .7  #zhong width
ph = .25  #pinyin height
pw = zw   #pinyin width

vs = 0.1 #vert space
hs = 0.15 #horiz space

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
  print (f'x: {x}, y: {y}, w: {w}, h: {h}, s: {s}')
  p.set_text_color(255,0,0)
  p.set_xy(x,y)
  p.set_font('pinyin','',64*h) # approx 90% height
  p.cell(w,h,s,align='C')

def zhongtext(p,x,y,w,h,s):
  print (f'x: {x}, y: {y}, w: {w}, h: {h}, s: {s}')
  p.set_text_color(0)
  p.set_xy(x,y+(0.1*h)) # offset y 10% for font rendering
  p.set_font('zhongwen','',64*h) # approx 90% height
  p.cell(w,h,s,align='C') 

def englishtext(p,x,y,w,h,s):
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

pdf = PDF('P','in','Letter')

#pdf.add_font('zhongwen','','fireflysung.ttf',uni=True)
pdf.add_font('zhongwen','','NotoSansSC-Regular.ttf',uni=True)
pdf.add_font('pinyin','','DejaVuSans.ttf', uni=True)
pdf.add_font('english','','DejaVuSans.ttf', uni=True)

pdf.add_page()

with open("wordlist.json","r") as f:
  wordlist = json.load(f)

  

pdf.set_auto_page_break(False)

x = leftmargin
row = 0
for w, d in wordlist.items():
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


pdf.output('writing-page.pdf', 'F')
