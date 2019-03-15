import pandas
from PIL import Image, ImageDraw, ImageFont, ImageOps
import time
from shutil import copyfile

def normal_s(text):
    ans = ''
    i = 0
    while i < len(text):
        if( text[i] == '\\' and text[i+1] == 'n' ):
            ans += '\n'
            i += 2
        else:
            ans += text[i]
            i+=1
    return ans

def multiline_text_borders(d, x, y, text, fnt):
    d.multiline_text((x+2, y), normal_s(text), font=fnt, align="left", fill="black")
    d.multiline_text((x-2, y), normal_s(text), font=fnt, align="left", fill="black")
    d.multiline_text((x, y+2), normal_s(text), font=fnt, align="left", fill="black")
    d.multiline_text((x, y-2), normal_s(text), font=fnt, align="left", fill="black")
    d.multiline_text((x, y), normal_s(text), font=fnt, align="left", fill="white")

def make_dot(fnt, d ,x, y, r, text):
    d.ellipse((x-r, y-r, x+r, y+r), fill=(255,0,0,255))
    #d.multiline_text((x+5, y), normal_s(text), font=fnt, align="left", fill="white")
    multiline_text_borders(d, x+10, y-10, text, fnt)
    print(text)

def make_line(d, x1, y1, x2, y2, r, g, b, width):
    d.line((x1, y1) + (x2, y2), fill=(r, g, b), width = width)
    print('Tracing line from ({} ; {}) to ({} ; {})'.format(x1, y1, x2, y2))

def coord_t(x, y, w, h):
    x = w/2 + x
    y = h/2 - y
    return x, y

block_size = (128, 32)

def get_dominant_color_count(im):
    im = im.convert('RGB')
    im = ImageOps.posterize(im, 2)
    #im.show()
    #print(sorted(im.getcolors(maxcolors=32), reverse= True)[0][0])
    #print( (128*32)/sorted(im.getcolors(maxcolors=32), reverse= True)[0][0] )
    return sorted(im.getcolors(maxcolors=32), reverse= True)[0][0]

def copyright_on_good_block(im, fnt):
    if( ((block_size[0]*block_size[1])/get_dominant_color_count(im)) < 1.2 ):
        trans = 16
        txt = Image.new('RGBA', im.size, (255,255,255,0))
        d = ImageDraw.Draw(txt)
        d.text((0, 0), "Vgscq", font=fnt, fill=(255,255,255,trans))
        return Image.alpha_composite(im, txt)
    else:
        return im

def for_copyright(im, fnt):
    for i in range(0, im.size[0], block_size[0]):
        for j in range(0, im.size[1], block_size[1]):
            im_t = im.crop( (i, j, i+block_size[0], j+block_size[1]) )
            im_t = copyright_on_good_block(im_t, fnt)
            im.paste(im_t, (i, j, i+block_size[0], j+block_size[1]) )

def make_image(fnt, d, dots, lines, im, name):    
    start = time.time()
    for i in range(len(lines)):
        make_line(d, coord_t(lines['x1'][i], lines['y1'][i], im.size[0], im.size[1])[0], coord_t(lines['x1'][i], lines['y1'][i], im.size[0], im.size[1])[1],
        coord_t(lines['x2'][i], lines['y2'][i], im.size[0], im.size[1])[0], coord_t(lines['x2'][i], lines['y2'][i], im.size[0], im.size[1])[1], 
        lines['r'][i], lines['g'][i], lines['b'][i], 35 )#4

    for i in range(len(dots)):
        make_dot(fnt, d, coord_t(dots['x'][i], dots['y'][i], im.size[0], im.size[1])[0], coord_t(dots['x'][i], dots['y'][i], im.size[0], im.size[1])[1], 4, dots['name'][i] )


    for_copyright(im, fnt)

    im.save(name)

    im.thumbnail((250,250))
    im.save("thumb_"+name)
    print('\nImage {} processing time takes {}\n'.format(name, time.time()-start))

def main():
    start = time.time()

    dots = pandas.read_csv('dots.csv')
    lines = pandas.read_csv('lines.csv')
    fnt = ImageFont.truetype('FreeMonoBold.ttf', 30)

    im_hd = Image.open('Original_hd.png').convert('RGBA')
    d_hd = ImageDraw.Draw(im_hd)
    im_sd = Image.open('Original_sd.png').convert('RGBA')
    d_sd = ImageDraw.Draw(im_sd)

    make_image(fnt, d_hd, dots, lines, im_hd, 'Edited_hd.png')
    make_image(fnt, d_sd, dots, lines, im_sd, 'Edited_sd.png')
    
    print('Program work takes: {}'.format(time.time()-start))

if( __name__ == '__main__' ):
    main()
