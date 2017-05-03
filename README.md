Single stroke font converter for Inkscape/Hershey Text
======================================================

**hershey.py,
hersheydata.py,
hershey.inx** - updated Inkscape/Hershey Text plugin. Adds to the original plugin some new features: text block formatting, input of cyrillic text in cp1251 encoding instead of koi7, combining of latin and cyrillic in text.

**font_converter/converter.py** - converts **SFEdit2.exe** output to single stroke font in Inkscape/Hershey Text plugin font format

**font_converter/prepare_font.py** - prepares OTF/TTF font for **SFEdit2.exe**: converts OTF to TTF, optionally moves cyrillic cp1251 glyphs to positions, editable with **SFEdit2.exe**

[Roland Single Line Font Editor 2 (**SFEdit2**) Software v1.02](http://support.rolanddga.com/_layouts/rolanddga/productdetail.aspx?pm=egx-30a)

How to use
----------

1. Find a TTF or OTF font you'd like to convert to single stroke. Try to find the lightest (single stroke looking like) version of the desired font.

2. If the font is OTF or if you need to convert cyrillic glyphs, run
```
python prepare_font.py your_font.otf
or 
python prepare_font.py -c your_font.otf
```
> Flag **-c** forces cyrillic glyphs to be copied to editable positions.

> The script should output a TTF font, with name derived from the original font name.

3. Open the font with the default font viewer application and install it to the system.

4. Run ***SFEdit2.exe*** and start a new font, selecting the just installed TTF as an input

5. Review and adjust generated glyphs. Glyph edit tools of ***SFEdit2.exe*** are intuitive enough. 

6. Save the font. It should appear in **C:\ProgramData\Roland DG Corporation\SFEdit2\Rsf2** with **.sf2** extension

7. Copy the font to your working dir and run
```
python converter.py your_font.sf2 your_font.ttf
or 
python converter.py -c your_font.sf2 your_font.ttf
```
> Flag **-c** forces to additionally output cyrillic version of a font

> The script generates preview image **your_font.svg** and **your_font.py** Python code to be copy pasted to **hersheydata.py** and **hershey.inx** files of Inkscape/Hershey Text plugin (as a rule in **C:\Program Files\Inkscape\share\extensions**)




