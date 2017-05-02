#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hershey Text - renders a line of text using "Hershey" fonts for plotters

Copyright 2011-2017, Windell H. Oskay, www.evilmadscientist.com

Additional contributions by Sheldon B. Michaels
and by the contributors of the Inkscape project, http://inkscape.org


This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
import hersheydata          #data file w/ Hershey font data
import inkex
import simplestyle
from simpletransform import computePointInNode

Debug = False
FONT_GROUP_V_SPACING = 45

spacing = 3  # spacing between letters

font_cyr = ""

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
    213 : ord("X"), # Х
    214 : ord("`"),
    215 : ord("J"),
    216 : ord("Q"),
    217 : ord("W"),
    218 : ord("]"), # Ь
    219 : ord("$"),
    220 : ord("_"),
    221 : ord("C"),
    222 : ord("U"),
    223 : ord("^"), # Я
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
    246 : ord("%"), # ц
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


def convert_cyrillic( c ):
    return dict.get( c, ord("*") );
    # inkex.debug(dict.get( c + 32, ord("*") ) - 32)

class Hershey( inkex.Effect ):
    def __init__( self ):
        inkex.Effect.__init__( self )
        self.OptionParser.add_option( "--tab",  #NOTE: value is not used.
            action="store", type="string",
            dest="tab", default="splash",
            help="The active tab when Apply was pressed" )
        self.OptionParser.add_option( "--text",
            action="store", type="string", 
            dest="text", default="Hershey Text for Inkscape",
            help="The input text to render")
        self.OptionParser.add_option( "--action",
            action="store", type="string",
            dest="action", default="render",
            help="The active option when Apply was pressed" )
        self.OptionParser.add_option( "--fontface",
            action="store", type="string",
            dest="fontface", default="rowmans",
            help="The selected font face when Apply was pressed" )
        self.OptionParser.add_option( "--fontface_cyr",
            action="store", type="string",
            dest="fontface_cyr", default="cyrillic",
            help="The selected font face when Apply was pressed" )
        self.OptionParser.add_option( "--boxwidth",
            action="store", type="string",
            dest="boxwidth", default="500",
            help="Prferrable max text width before line break" )

    def draw_svg_text(self, char, face, offset, vertoffset, parent):
        style = { 'stroke': '#000000', 'fill': 'none' }
        if char > 127: #  face == hersheydata.cyrillic:
            char = convert_cyrillic(char)
            if char > 127: #  face == hersheydata.cyrillic:
                return offset + 2 * spacing
            else:
                f = eval('hersheydata.' + str(self.options.fontface_cyr))
                pathString = f[char - 32]
        else:       
            pathString = face[char - 32]

        splitString = pathString.split()  
        midpoint = offset - float(splitString[0]) 
        splitpoint = pathString.find("M")
        # Space glyphs have just widths with no moves, so their splitpoint is 0
        # We only want to generate paths for visible glyphs where splitpoint > 0
        if splitpoint > 0:
            pathString = pathString[splitpoint:] #portion after first move
            trans = 'translate(' + str(midpoint) + ',' + str(vertoffset) + ')'
            text_attribs = {'style':simplestyle.formatStyle(style), 'd':pathString, 'transform':trans}
            inkex.etree.SubElement(parent, inkex.addNS('path','svg'), text_attribs) 

        return midpoint + float(splitString[1])   #new offset value

    def svg_char_width(self, char, face, offset):
        if char > 127: 
            char = convert_cyrillic(char)
            if char > 127: 
                return offset + 2 * spacing
            else:
                f = eval('hersheydata.' + str(self.options.fontface_cyr))
                pathString = f[char - 32]
        else:       
            pathString = face[char - 32]

        splitString = pathString.split()  
        midpoint = offset - float(splitString[0])
        return midpoint + float(splitString[1]) 

    def svg_text_width(char, face, offset):
        pathString = face[char - 32]
        splitString = pathString.split()  
        midpoint = offset - float(splitString[0])
        return midpoint + float(splitString[1]) #new offset value
        
    def effect( self ):

        OutputGenerated = False

        # Embed text in group to make manipulation easier:
        g_attribs = {inkex.addNS('label','inkscape'):'Hershey Text' }
        g = inkex.etree.SubElement(self.current_layer, 'g', g_attribs)

        scale = self.unittouu('1px')    # convert to document units
        font = eval('hersheydata.' + str(self.options.fontface))
        clearfont = hersheydata.futural  
        #Baseline: modernized roman simplex from JHF distribution.
        
        w = 0  #Initial spacing offset
        v = 0  #Initial vertical offset

        text = self.options.text

        if self.options.action == "render":
            #evaluate text string
            letterVals = [ord(q) for q in text] 
            i = 0
            for q in letterVals:
                if q == 10:
                    v += FONT_GROUP_V_SPACING
                    w = 0
                elif (q <= 32): 
                    w += 2 * spacing
                else:
                    w = self.draw_svg_text(q, font, w, v, g)
                    OutputGenerated = True

                if (q == 32 or q == 7) and (int(self.options.boxwidth) > 0):
                    tokenw = 0
                    for j in range(len(letterVals) - i - 1): 
                        ch = letterVals[j + i + 1]
                        if (ch == 32 or ch == 7):
                            break
                        tokenw = self.svg_char_width(ch, font, tokenw)
                        if (w > 0) and ((tokenw + w) > int(self.options.boxwidth)):
                            v += FONT_GROUP_V_SPACING
                            w = 0
                            break
                i += 1

        elif self.options.action == 'sample':
            w,v = self.render_table_of_all_fonts( 'group_allfonts', g, spacing, clearfont )
            OutputGenerated = True
            scale *= 0.4	#Typically scales to about A4/US Letter size
        else:
            #Generate glyph table
            wmax = 0;
            for p in range(0,10):
                w = 0
                v = spacing * (15*p - 67 )
                for q in range(0,10):
                    r = p*10 + q 
                    if (r <= 32) or (r > 127):
                        w += 5*spacing
                    else:
                        w = self.draw_svg_text(r, clearfont, w, v, g)
                        w = self.draw_svg_text(r, font, w, v, g)
                        w += 5 * spacing
                if w > wmax:
                    wmax = w
            w = wmax
            OutputGenerated = True            
        #  Translate group to center of view, approximately
        view_center = computePointInNode(list(self.view_center), self.current_layer)
        t = 'translate(' + str( view_center[0] - scale*w/2) + ',' + str( view_center[1] - scale*v/2 ) + ')'
        if scale != 1:
            t += ' scale(' + str(scale) + ')'
        g.set( 'transform',t)

#        inkex.debug(self.options.boxwidth)
#        inkex.debug(w)

        if not OutputGenerated:
            self.current_layer.remove(g)    #remove empty group, if no SVG was generated.

    def render_table_of_all_fonts( self, fontgroupname, parent, spacing, clearfont ):
        v = 0
        wmax = 0
        wmin = 0
        fontgroup = eval( 'hersheydata.' + fontgroupname )
        
        # Render list of font names in a vertical column:
        nFontIndex = 0
        for f in fontgroup:
            w = 0
            letterVals = [ord(q) for q in (f[1] + ' -> ')]
            # we want to right-justify the clear text, so need to know its width
            for q in letterVals:
                w = self.svg_text_width(q, clearfont, w)
                
            w = -w  # move the name text left by its width
            if w < wmin:
                wmin = w
            # print the font name
            for q in letterVals:
                w = self.draw_svg_text(q, clearfont, w, v, parent)
            v += FONT_GROUP_V_SPACING
            if w > wmax:
                wmax = w
            
        # Next, we render a second column. The user's text, in each of the different fonts:
        v = 0                   # back to top line
        wmaxname = wmax + 8     # single space width
        for f in fontgroup:
            w = wmaxname
            font = eval('hersheydata.' + f[0])
            #evaluate text string
            letterVals = [ord(q) - 32 for q in self.options.text] 
            for q in letterVals:
                if (q <= 32) or (q > 127):
                    w += 2*spacing
                else:
                    w = self.draw_svg_text(q, font, w, v, parent)
            v += FONT_GROUP_V_SPACING
            if w > wmax:
                wmax = w
        return wmax + wmin, v


if __name__ == '__main__':
    e = Hershey()
    e.affect()

# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
