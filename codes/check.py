import sys
from fontTools.ttLib import TTFont

outfile, infile, subft=sys.argv[1], sys.argv[2], sys.argv[3]

def prouv(font, ispr):
	cmap=font.getBestCmap()
	for table in font["cmap"].tables:
		if table.format==14:
			for vsl in table.uvsDict.keys():
				newl=list()
				for cg in table.uvsDict[vsl]:
					if cg[1]==None and ispr:
						newl.append((cg[0], cmap[cg[0]]))
					elif cg[0] in cmap and cg[1]==cmap[cg[0]] and not ispr:
						newl.append((cg[0], None))
					else:
						newl.append((cg[0], cg[1]))
				table.uvsDict[vsl]=newl

font=TTFont(infile)
font2=TTFont(subft)
prouv(font, True)
cmap=font.getBestCmap()
cmap2=font2.getBestCmap()
uvg=set()
for table in font['cmap'].tables:
	if table.format==14:
		for vsl in table.uvsDict.keys():
			for cg in table.uvsDict[vsl]:
				if cg[1]==None: raise
				else: uvg.add(cg[1])

for cd in cmap2.keys():
	if cmap2[cd] in ['.notdef', '.null', 'nonmarkingreturn', 'space']:
		continue
	for table in font['cmap'].tables:
		if table.format==14: continue
		if cd in table.cmap and table.cmap[cd] in uvg:
			del table.cmap[cd]
prouv(font, False)

outfont=TTFont(infile, recalcBBoxes=False)
outfont['cmap']=font['cmap']
outfont.save(outfile)

