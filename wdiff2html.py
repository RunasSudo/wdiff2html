#!/usr/bin/env python3
#   wdiff2html - Convert wdiff output to side-by-side HTML
#   Copyright © 2017  RunasSudo (Yingtong Li)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re
import sys

RE_INS = re.compile(r'\{\+(.*?)\+\}')
RE_DEL = re.compile(r'\[\-(.*?)\-\]')

current = [None, None]

def write_line():
	print('<tr><td>{}</td><td>{}</td></tr>'.format(current[0] or '', current[1] or ''))

print('''<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>wdiff2html result</title>
		<style type="text/css">
			table { border: 0; width: 100%; }
			td { width: 50%; font-family: 'Liberation Sans', Helvetica, Arial, sans-serif; font-size: 1.2em; }
			b { color: #3b7405; }
		</style>
	</head>
	<body>
		<table>''')

with open(sys.argv[1], 'r') as f:
	for line in f:
		line = line.rstrip('\n')
		
		line_l, line_r = line, line
		
		line_l = RE_INS.sub(r'', line_l)
		line_l = RE_DEL.sub(r'<b>\1</b>', line_l)
		
		line_r = RE_DEL.sub(r'', line_r)
		line_r = RE_INS.sub(r'<b>\1</b>', line_r)
		
		if current[1] is None and len(line_l) == 0:
			# We are processing an addition, and the previous line was only a deletion, and this line is only an addition
			# Reuse the previous line
			pass
		else:
			# New line
			write_line()
			current = [None, None]
		
		if len(line_l) > 0:
			current[0] = line_l
		if len(line_r) > 0:
			current[1] = line_r

write_line()

print('''		</table>
	</body>
</html>''')
