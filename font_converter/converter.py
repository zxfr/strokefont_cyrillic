#!/usr/bin/env python

''' 
converter.py

.sf2 single stroke font converter for 
Inkscape's Hershey Text plugin


Version 1.0.0, dated May 02, 2017.

Originally written by Igor Repinetski, http://pixelmeister.org

'''

import struct
import argparse
import sys

# bigger 'scale' value results smaller font glyphs
scale = float(28)
charspacing = 3 

def getNumberOfGlyphs(fileContent):
    return struct.unpack_from("H", fileContent, 0x60)[0]

def getChar(fileContent, i):
    return chr(struct.unpack_from("H", fileContent, 0xAC + i * 2)[0])

def getDataOffsetTableStart(fileContent):
    n = getNumberOfGlyphs(fileContent)
    return 0xAC + n * 2 + (n % 4) * 2

def getDataStart(fileContent):
    n = getNumberOfGlyphs(fileContent)
    return getDataOffsetTableStart(fileContent) + n * 4

def getGlyphDefStart(fileContent, i):
    off = struct.unpack_from("<I", fileContent, getDataOffsetTableStart(fileContent) + i * 4)[0]
    ds = getDataStart(fileContent)
    return ds + off

def getFontName(fileContent):
    fontName = ""
    fontMeta = fileContent[0x6c:0x8b]
    for c in fontMeta:
        if ord(c) == 0:
            break
        if c == ' ' or c == '.':
            fontName += '_'
        else:
            fontName += c
    return fontName

def getFontLabel(fileContent):
    fontName = ""
    fontMeta = fileContent[0x6c:0x8b]
    for c in fontMeta:
        if ord(c) == 0:
            break
        fontName += c
    return fontName

def computeBaseline(fileContent):
    glyphNo = getNumberOfGlyphs(fileContent)
    maxh = 0
    for i in range(glyphNo): 
        offset = getGlyphDefStart(fileContent, i)
        offset += 4
        
        strokesNum = struct.unpack_from("<I", fileContent, offset)[0]
        offset += 4
        nodesNum = []
        for j in range(strokesNum):
            segments = struct.unpack_from("<I", fileContent, offset)[0]
            offset += 4
            nodesNum.append(segments)
    
        for j in range(strokesNum):
            for k in range(nodesNum[j]):
                offset += 2
                cy = struct.unpack_from("<h", fileContent, offset)[0]
                offset += 10
                maxh = max(maxh, cy/scale)
    
    return maxh + 2

def generateFont(fileContent, ttFont, cyr):
    previewCode = ""
    glyphs = {}   

    glyphNo = getNumberOfGlyphs(fileContent)
    baseline = computeBaseline(fileContent)
    
    xx = 0
    yy = 0
    for i in range(glyphNo): 
        xx = (i % 16) * 50 + 10
        yy = int(i / 16) * 40 + 40
        
        ch = getChar(fileContent, i)
        offset = getGlyphDefStart(fileContent, i)
        
        previewCode += "<g transform='translate({}, {})'>\n".format(xx, yy)
    
        sx = struct.unpack_from("<I", fileContent, offset)[0]
        offset += 4
        
        strokesNum = struct.unpack_from("<I", fileContent, offset)[0]
        offset += 4
    
        nodesNum = []
        for j in range(strokesNum):
            segments = struct.unpack_from("<I", fileContent, offset)[0]
            offset += 4
            nodesNum.append(segments)
            
        coords = []
        for j in range(strokesNum):
            for k in range(nodesNum[j]):
                cx = struct.unpack_from("<h", fileContent, offset)[0]
                offset += 2
                cy = struct.unpack_from("<h", fileContent, offset)[0]
                offset += 2
                xx = struct.unpack_from("<h", fileContent, offset)[0]
                offset += 2
                xy = struct.unpack_from("<h", fileContent, offset)[0]
                offset += 2
                yx = struct.unpack_from("<h", fileContent, offset)[0]
                offset += 2
                yy = struct.unpack_from("<h", fileContent, offset)[0]
                offset += 2
                
                crd = [cx, cy, xx, xy, yx, yy]
                coords.append(crd)
    
        count = 0 
        maxw = 4
        glyphCode = ""
        for j in range(strokesNum):
            previewCode += "\t<path d=\""
            pathCode = ""
            
            for k in range(nodesNum[j]):
                flag = ord(fileContent[offset])
                offset += 1
                
                crd = coords[count]
                suff = ""
                pref = " L"
                if flag == 7:
                    suff = "Z"
                if k == 0:
                    pref = "M"
                    
                if k == 0 or crd[2] == 0 and crd[3] == 0 and crd[4] == 0 and crd[5] == 0:
                    pathCode += "{}{:.2f},{:.2f} {}".format(pref, crd[0]/scale, crd[1]/scale + baseline, suff)
                else:
                    pathCode += " Q{:.2f},{:.2f} {:.2f},{:.2f} {}".format((crd[2]+crd[0])/scale, (crd[3]+crd[1])/scale + baseline, crd[0]/scale, crd[1]/scale + baseline, suff)
                    
                pathCode = pathCode.strip()
                        
                maxw = max(maxw, crd[0]/scale) 
                count += 1
            
            
            glyphCode += pathCode
            previewCode += pathCode
            previewCode += "\" fill=\"none\" stroke=\"red\" stroke-width=\"1\"  />\n"
            
        mtx = getMetric(ttFont, chr(ord(ch)), cyr)
        ww = maxw
        if mtx != None:
            ww = mtx[0]/scale/1.5
            
        previewCode += "</g> <!-- {:.2f} vs. {:.2f} -->\n".format(maxw, ww)
        glyphs[ord(ch)] = ("0 {:.2f} ".format(ww + charspacing) + glyphCode).strip()  
            
        maxw = 4
        
    return previewCode, glyphs

def getMetric( ttFont, ch, cyr ):
    if ttFont == None or ord(ch) == 0x98:
        return None
    
    if cyr:
        ch = ch.decode('cp1251')
    hmtx = ttFont['hmtx']
    cmap = ttFont['cmap']
    for table in cmap.tables:
        if table.format in [4, 12, 13, 14]:
            for key in table.cmap:
                if key == ord(ch):
                    mmx  = hmtx.metrics[table.cmap[key]]
                    return mmx
                
    return None

dict = {
    192 : ord("A"),
    193 : ord("B"),
    194 : ord("V"),
    195 : ord("G"),
    196 : ord("D"),
    197 : ord("["),
    198 : ord("H"),
    199 : ord("Z"),
    200 : ord("I"),
    201 : ord("E"),
    202 : ord("K"),
    203 : ord("L"),
    204 : ord("M"),
    205 : ord("N"),
    206 : ord("O"),
    207 : ord("P"),
    208 : ord("R"),
    209 : ord("S"),
    210 : ord("T"),
    211 : ord("Y"),
    212 : ord("F"),
    213 : ord("X"), # Õ
    214 : ord("`"),
    215 : ord("J"),
    216 : ord("Q"),
    217 : ord("W"),
    218 : ord("]"), # Ü
    219 : ord("$"),
    220 : ord("_"),
    221 : ord("C"),
    222 : ord("U"),
    223 : ord("^"), # ß
    224 : ord("a"),
    225 : ord("b"),
    226 : ord("v"),
    227 : ord("g"),
    228 : ord("d"),
    229 : ord("{"),
    230 : ord("h"),
    231 : ord("z"),
    232 : ord("i"),
    233 : ord("e"),
    234 : ord("k"),
    235 : ord("l"),
    236 : ord("m"),
    237 : ord("n"),
    238 : ord("o"),
    239 : ord("p"),
    240 : ord("r"),
    241 : ord("s"),
    242 : ord("t"),
    243 : ord("y"),
    244 : ord("f"),
    245 : ord("x"),
    246 : ord("%"), # ö
    247 : ord("j"),
    248 : ord("q"),
    249 : ord("w"),
    250 : ord("|"),
    251 : ord("&"),
    252 : ord("~"),
    253 : ord("c"),
    254 : ord("u"),
    255 : ord("}"),
}

def getCyrillic( c ):
    for i in dict:
        if dict[i] == c:
            return i
    return c;

# for debug purposes only
def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines)


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("sf2", metavar="font.sf2")
    parser.add_argument("ttf", metavar="font.ttf")
    parser.add_argument("-c", "--cyrillic", dest="cyr", action="store_true", default=False)
    options = parser.parse_args(args)

    sfontFile = options.sf2
    ttFile = options.ttf

    with open(sfontFile, "rb") as file:
        fileContent = file.read()
    
    ttFont = None
    if ttFile != None:
        from fontTools.ttLib import TTFont
        ttFont = TTFont(ttFile)
    
    fontName = getFontName(fileContent)
    previewCode, glyphs = generateFont(fileContent, ttFont, options.cyr)
    
    result = '''<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="16cm" height="12cm" viewBox="0 0 820 620" xmlns="http://www.w3.org/2000/svg" version="1.1">
<g transform='translate(20, 20)'>
  <rect x="0" y="0" width="800" height="600" fill="none" stroke="blue" stroke-width="1" />
'''
    result += previewCode
    result += '''  
</g>
</svg>
    '''
    
    with open("{}.svg".format(fontName), "w") as file:
        file.write(result)
            
    result = "{} = [".format(fontName)
    count = 0
    for ch in glyphs:
        result += '"{}",'.format(glyphs[ch])
        count += 1
        if count > 97:
            break
    result += "]\n"
    
    if options.cyr:
        result += "{}_cyr = [".format(fontName)
        count = 0
        for ch in glyphs:
            ch = getCyrillic(ch)
            result += '"{}",'.format(glyphs[ch])
            count += 1
            if count > 97:
                break
        result += "]\n"

    label = getFontLabel(fileContent)    
    
    result += "\n# <_item value=\"{}\">{}</_item>\n".format(fontName, label)
    if options.cyr:
        result += "# <_item value=\"{}_cyr\">{} Cyrillic</_item>\n".format(fontName, label)
    result += "# ['{}','{}'],\n".format(fontName, label)
    if options.cyr:
        result += "# ['{}_cyr','{} Cyrillic'],\n".format(fontName, label)
    
    with open("{}.py".format(fontName), "w") as file:
        fileContent = file.write(result)
        
    print result
    print "generated font size: {}".format(len(result))

if __name__ == "__main__":
    sys.exit(main())


