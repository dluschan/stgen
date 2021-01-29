from .tag import create_tag


def create_table(rows):
	table = create_tag('table', None, {'border': '1px', 'cellpadding': '4px'})
	tbody = create_tag('tbody')
	table.appendChild(tbody)

	for row in rows:
		tr = create_tag('tr')
		tbody.appendChild(tr)
		for cell in row:
			td = create_tag('td', str(cell) if cell else '')
			tr.appendChild(td)

	return table.toprettyxml()


def create_svg_table(rows, headers=None, width=None):
	indent = 50
	digit_width = 0
	cell_width = width
	cell_height = 100
	font_size = 50
	grid_width = len(rows[0]) * cell_width
	grid_height = len(rows) * cell_height
	svg = create_tag('svg', None, {'width': '50%', 'max-width': '400px', 'viewBox': f'0 0 {indent + digit_width + grid_width + indent} {indent + grid_height + indent}'})
	g = create_tag('g', None, {'stroke': 'black', 'stroke-width': 2})
	for i in range(len(rows) + 1):
		g.appendChild(create_tag('line', None, {'x1': indent + digit_width, 'y1': indent + i*cell_height, 'x2': indent + digit_width + grid_width, 'y2': indent + i*cell_height}))
	for i in range(len(rows[0]) + 1):
		g.appendChild(create_tag('line', None, {'x1': indent + digit_width + i*cell_width, 'y1': indent, 'x2': indent + digit_width + i*cell_width, 'y2': indent + grid_height}))
	svg.appendChild(g)
	for i, row in enumerate(rows):
		for j, cell in enumerate(row):
			if cell is None:
				svg.appendChild(create_tag('rect', None, {'x': indent + cell_width * j, 'y': indent + cell_height * i, 'width': cell_width, 'height': cell_height, 'fill': "silver", 'stroke': "black", 'stroke-width': 2}))
			else:
				svg.appendChild(create_tag('text', cell, {'text-anchor': "middle", 'x': indent + cell_width * (j + 0.5), 'y': indent + cell_height * (i + 0.75), 'font-size': "50px"}))
	if headers:
		svg.appendChild(create_tag('rect', None, {'x': indent, 'y': indent, 'width': grid_width, 'height': headers[0] * cell_height, 'fill': 'none', 'stroke': "black", 'stroke-width': 5}))
		svg.appendChild(create_tag('rect', None, {'x': indent, 'y': indent + headers[0] * cell_height, 'width': grid_width, 'height': grid_height - headers[0] * cell_height, 'fill': 'none', 'stroke': "black", 'stroke-width': 5}))
		svg.appendChild(create_tag('rect', None, {'x': indent, 'y': indent, 'width': headers[1] * cell_width, 'height': grid_height, 'fill': 'none', 'stroke': "black", 'stroke-width': 5}))
		svg.appendChild(create_tag('rect', None, {'x': indent + headers[1] * cell_width, 'y': indent, 'width': grid_width - headers[1] * cell_width, 'height': grid_height, 'fill': 'none', 'stroke': "black", 'stroke-width': 5}))
	return svg.toprettyxml()
