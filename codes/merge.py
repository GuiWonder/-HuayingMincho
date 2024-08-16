import os, sys
import fontforge

def getallcodesname(thfont):
	c_g = dict()
	g_c=dict()
	for gls in thfont.glyphs():
		if gls.glyphname in ('.notdef', '.null', 'nonmarkingreturn', 'space'):
			continue
		g_c[gls.glyphname]=list()
		if gls.unicode > -1:
			c_g[gls.unicode]=gls.glyphname
			g_c[gls.glyphname].append(gls.unicode)
		if gls.altuni != None:
			for uni in gls.altuni:
				if uni[1] <= 0:
					c_g[uni[0]] = gls.glyphname
					g_c[gls.glyphname].append(uni[0])
	return c_g, g_c

def mergeft(font, fin2, rplc=False):
	print(f'Loading {fin2}...')
	code_glyph, glyph_codes=getallcodesname(font)
	font2 = fontforge.open(fin2)
	font2.reencode("unicodefull")
	font2.em = font.em
	print('Getting glyph2 codes')
	code_glyph2, glyph_codes2=getallcodesname(font2)
	print('Adding glyphs...')
	code_codes2 = {}
	for n2 in glyph_codes2.keys():
		lc = [ac1 for ac1 in glyph_codes2[n2] if (rplc or ac1 not in code_glyph)]
		if len(lc) > 0:
			code_codes2[lc[0]] = lc[1:]
	font2.selection.select(*code_codes2.keys())
	font2.copy()
	font.selection.select(*code_codes2.keys())
	font.paste()
	print('Checking extra codings...')
	for cd1 in code_codes2.keys():
		if len(code_codes2[cd1]) > 0:
			font[cd1].altuni = code_codes2[cd1]
	del code_codes2
	del glyph_codes2
	del code_glyph2
	font2.close()

def build(outft, fonts):
	print('Target', outft)
	print('Processing...')
	font=fontforge.open(fonts[0])
	font.reencode("unicodefull")
	print('Merging glyphs...')
	mergeft(font, fonts[1], True)
	print('Saving...')
	gflags=('opentype', 'omit-instructions', 'short-post',)
	font.generate(outft, flags=gflags)
	print('Finished', outft)

if __name__ == "__main__":
	build(sys.argv[1], sys.argv[2:])
