import requests as rq
import logging as log
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


class EXPR:
	count = 0
	
	def __init__(self, expr):
		self.expr = expr
	
	def _get_svg(self):
		self.filename = f'{self.__class__.count}'.zfill(6)
		with open(f'{self.filename}.svg', 'w') as file:
			res = rq.get(f'https://math.vercel.app/?from={self.expr}')
			if res.status_code != 200:
				raise Exception('Something went wrong...')
			svg = res.text
			file.write(svg)
	


	def _fix_svg(self, K=10):
		params = ['width=', 'height=']
		with open(f'{self.filename}.svg') as file:
			text = file.read()
	
		for param in params:
	
			start = text.find(param) + len(param)
			print(start)
	
			if text[start] == '"':
	
				val = ['', '']
	
				for i in range(start + 1, 1000):
					if text[i] == '"':
						end = i + 1
						break
	
					if text[i].isdigit() or text[i] == '.':
						val[0] += text[i]
						continue
	
					val[1] += text[i]
	
	
				new_val = f'"{float(val[0])*K}{val[1]}"'
	
				text = text[:start] + new_val + text[end:]
	
			else:
				raise Exception('Something went wrong...')
	
		with open(f'{self.filename}.svg', 'w') as file:
			file.write(text)


	def _svg2png(self):
		log.disable(level=log.WARN)
		dr = svg2rlg(f'{self.filename}.svg')
		renderPM.drawToFile(dr, f'{self.filename}.png')


	def get_png_from_expr(self):
                # next time
                pass

# EXPR('\int%20x^{x}\,%20dx')
