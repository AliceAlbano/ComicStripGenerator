#!/usr/bin/python

import argparse

FONTSIZE = 40
INTERLINE = FONTSIZE * 0.375
PADDING = FONTSIZE / 2

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-x', help = "top left absciss of the bubble", type = float, required = True)
	parser.add_argument('-y', help = "top left ordinate of the bubble", type = float, required = True)
	parser.add_argument('-w', help = "width of the bubble", type = float, required = True)
	parser.add_argument('-c', help = "Text for the bubble", type = str, required = True, nargs ="+")
	args = parser.parse_args()
	return args.x, args.y, args.w, args.c

#Return svg for the main rectangle bubble
def rect(x, y, w, h):
	return """	<rect
		style="fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#1a1a1a;stroke-width:5;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0"
		id="balloon"
		width=""" + "\"" + str(w) + "\"" + """
		height=""" + "\"" + str(h) + "\"" + """
		x=""" + "\"" + str(x) + "\"" + """
		y=""" + "\"" + str(y) + "\"" + """
		ry="17.857147"
	/>
"""

#Return svg for the small rectangle hiding the top of the path
def hide(x, y , w, h):
	return """	<rect
	style="fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#ffffff;stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0"
	id="hide"
	width="20.46574"
	height="30.052038"
	x=""" + "\"" + str(w/3 + x) + "\"" + """
	y=""" + "\"" + str(y + h - 28.052038) + "\"" + """
	/>
"""

#Return svg for the path (=peak of the bubble)
def path(x, y, w, h):
	return """	<path
	style="fill:#ffffff;fill-opacity:1;fill-rule:nonzero;stroke:#1a1a1a;stroke-width:5;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0"
	d="m """ + str(x + w/3 - 0.8) + "," + str(y + h - 2.45) + """ -0.1177,11.13567 -11.24652,17.65368 34.37565,-26.78428"
	id="peak"
	inkscape:connector-curvature="0"
	sodipodi:nodetypes="cccc" />
"""

#Return svg for the text
def text(x, y, w, h, c):
	t = """	<text
	style="font-size:""" + str(FONTSIZE) + """px;font-style:normal;font-variant:normal;font-weight:500;font-stretch:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:black;opacity:1;stroke:none;font-family:OpenComicFont;-inkscape-font-specification:OpenComicFont Medium"
	x=""" + "\"" + str(x) + "\"" + """
	y=""" + "\"" + str(y) + "\"" + """
	alignment-baseline="middle"
	text-anchor="middle"
	>"""
	t += c +"""</text>
"""
#	y=""" + "\"" + str(y + h/2 + 10) + "\"" + """
	return t

def multiline(x, y, w, h, c):
	result = ""
	i = 0
	while i < len(c) :
		result += text(x + w/2, y + (h / (len(c)+1)) + INTERLINE + i*FONTSIZE, w, h, c[i])
		i += 1
	return result

def height(c):
	h = len(c) * FONTSIZE + 2 * PADDING
	return h

#Print svg for a speech balloon
def output_balloon(x, y, w, h, c):
	f = open("header.svg", 'r')
	print f.read()
	f.close()

	print """ <g
     inkscape:label="Calque 1"
     inkscape:groupmode="layer"
     id="layer1">

	<!-- Balloon -->
	<!-- ry : define the corners round -->
	<g inkscape:label="Balloon"
	   inkscape:groupmode="layer"
	   id="layer2">
""" 
	print rect(x, y, w, h)
	print hide(x, y, w, h)
	print path(x, y, w, h)
	print """</g>
	<!-- Text -->
""" 
	print multiline(x, y, w, h, c)
	print """
</g>
</svg>
"""


x, y, w, c = get_args()

h = height(c)
output_balloon(x, y, w, h, c)
