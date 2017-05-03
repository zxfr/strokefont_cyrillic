Single stroke font converter for Inkscape/Hershey Text
======================================================

**hershey.py,
hersheydata.py,
hershey.inx** - updated Inkscape/Hershey Text plugin. Adds to the original plugin some new features: text block formatting, input of cyrillic text in cp1251 encoding instead of koi7, combining of latin and cyrillic in text.

**font_converter/converter.py** - converts **SFEdit2.exe** output to single stroke font in Inkscape/Hershey Text plugin font format

**font_converter/prepare_font.py** - prepares OTF/TTF font for **SFEdit2.exe**: converts OTF to TTF, optionally moves cyrillic cp1251 glyphs to positions, editable with **SFEdit2.exe**

Prerequisites
-------------

[Roland Single Line Font Editor 2 (**SFEdit2**) Software v1.02](http://support.rolanddga.com/_layouts/rolanddga/productdetail.aspx?pm=egx-30a)

[Inkscape](http://inkscape.org) - Recent versions include original **Hershey Text plugin** by default

The scripts depend on Python modules **cu2qu** and **fontTools**


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

4. Run **SFEdit2.exe** and start a new font, selecting the just installed TTF as an input

5. Review and adjust auto-generated glyphs. Glyph edit tools of ***SFEdit2.exe*** are intuitive enough. 
![SFEdit2.exe](/i/sfedit2.png)

6. Save the font. It should appear in **C:\ProgramData\Roland DG Corporation\SFEdit2\Rsf2** with **.sf2** extension

7. Copy the font to your working dir and run
```
python converter.py your_font.sf2 your_font.ttf
or 
python converter.py -c your_font.sf2 your_font.ttf
```
> Flag **-c** forces to additionally output cyrillic version of a font

> The script generates preview image **your_font.svg** and **your_font.py** Python code snippet.

8. For a better cyrillic text support and for some new features I would recommend to backup and to overwrite default Inkscape/Hershey Text plugin files with the supplied ones (**hershey.py, hersheydata.py, hershey.inx** as a rule in **C:\Program Files\Inkscape\share\extensions**)

9. Copy-paste font data from **your_font.py** to suitable positions in **hersheydata.py** and **hershey.inx**

10. Run **Inkscape** and open the plugin via **Extensions->Render->Hershey Text...** menu item.
![Updated hershey text plugin](/i/plugin.png)



