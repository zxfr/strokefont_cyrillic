Single stroke font converter for Inkscape/Hershey Text
======================================================

hershey.py
hersheydata.py
hershey.inx - updated Inkscape/Hershey Text plugin. Adds to the original plugin some new features: text block formatting, input of cyrillic text in cp1251 encoding instead of koi7, combining of latin and cyrillic in text.

font_converter/converter.py - converts SFEdit2.exe output to single stroke font in Inkscape/Hershey Text plugin font format (to be copy-pasted to hersheydata.py and hershey.inx)

font_converter/prepare_font.py - prepares OTF/TTF font for SFEdit2.exe compatibility: converts OTF to TTF, optionally moves cyrillic cp1251 glyphs to positions, editable with SFEdit2.exe

[Roland Single Line Font Editor 2 (SFEdit2) Software v1.02](http://support.rolanddga.com/_layouts/rolanddga/productdetail.aspx?pm=egx-30a)


