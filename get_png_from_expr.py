import requests as rq
import logging as log
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF


class EXPR:
	count = -1

	def __init__(self, expr, K=100):
		self.expr = expr
		self.K = K
		self.__class__.count += 1

	def _get_svg(self):
		self.filename = f'{self.__class__.count}'.zfill(6)
		with open(f'{self.filename}.svg', 'w') as file:
			res = rq.get(f'https://math.vercel.app/?from={self.expr}')
			if res.status_code != 200:
				raise Exception('Something went wrong...')
			svg = res.text
			file.write(svg)



	def _fix_svg(self):
		params = ['width=', 'height=']
		with open(f'{self.filename}.svg') as file:
			text = file.read()

		for param in params:

			start = text.find(param) + len(param)

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


				new_val = f'"{float(val[0])*self.K}{val[1]}"'

				text = text[:start] + new_val + text[end:]

			else:
				raise Exception('Something went wrong...')

		with open(f'{self.filename}.svg', 'w') as file:
			file.write(text)


	def _svg2png(self):
		#log.disable(level=log.DEBUG)
		dr = svg2rlg(f'{self.filename}.svg', resolve_entities=True)
		renderPDF.drawToFile(dr, f'{self.filename}.pdf')


	def file(self):
		self._get_svg()
		self._fix_svg()
		self._svg2png()
		return open(f'{self.filename}.pdf', 'rb')

# EXPR('\int%20x^{x}\,%20dx')
