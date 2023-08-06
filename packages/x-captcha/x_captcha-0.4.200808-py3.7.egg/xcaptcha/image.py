#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Captcha
"""
__author__ = 'Leo'


import random
import time
import os
from PIL import Image, ImageDraw, ImageFont

random.seed(time.time())

DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')

DEFAULT_SIZE = (100, 50)
DEFAULT_CHARACTERS = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
DEFAULT_NUMBER = 4
DEFAULT_FONT = os.path.join(DATA_DIR, 'msyhbd.ttf')


class Captcha(object):
	def __init__(self, size=DEFAULT_SIZE, characters=DEFAULT_CHARACTERS, number=DEFAULT_NUMBER, font=DEFAULT_FONT):
		self.config(size, characters, number, font)

	def config(self, size, characters, number, font):
		self.__size = size
		self.__characters = characters
		self.__number = number
		self.__font = font

	def generate(self):
		background = self._rand_color(128, 255)
		image = Image.new('RGB', self.__size, background)
		draw = ImageDraw.Draw(image)
		captcha = self._draw_text(draw)
		self._draw_line(draw)
		self._draw_point(draw)
		return (captcha, image)

	def save(self, filepath=None):
		captcha, image = self.generate()
		if filepath is None:
			timestamp = str(time.time()).replace(".", "")
			filepath = '%s/%s_%s.png' % ('captcha', captcha, timestamp)
		dirname = os.path.dirname(filepath)
		if not os.path.exists(dirname):
			os.mkdir(dirname)
		image.save(filepath)

	def _draw_text(self, draw):
		captcha = []
		for i in range(self.__number):
			font = self._rand_font()
			color = self._rand_color(0, 127)
			text = self._rand_text()
			position = self._rand_position(i, font, text)
			draw.text(position, text, fill=color, font=font)
			captcha.append(text)
		return ''.join(captcha)

	def _draw_line(self, draw):
		for i in range(2):
			line = self._rand_line()
			color = self._rand_color(0, 127)
			draw.line(line, color, width=2)

	def _draw_point(self, draw):
		pass

	def _rand_color(self, start, end, opacity=None):
			red = random.randint(start, end)
			green = random.randint(start, end)
			blue = random.randint(start, end)
			if opacity:
				return (red, green, blue, opacity)
			return (red, green, blue)

	def _rand_text(self):
		characters = self.__characters
		limit = len(characters) - 1
		index = random.randint(0, limit)
		return characters[index]

	def _rand_position(self, i, font, text):
		width, height = self.__size
		number = self.__number
		f_width, f_height = font.getsize(text)
		piece = width / number
		x_lower = piece * i
		x_upper = piece * (i + 1) - f_width
		if x_upper < x_lower:
			x_upper = x_lower
		x = random.uniform(x_lower, x_upper)
		y_lower = 0
		y_upper = height - f_height
		if y_upper < 0:
			y_upper = 0
		y = random.uniform(y_lower, y_upper)
		return (x, y)

	def _rand_font(self):
		piece = self.__size[0] // self.__number
		lower = int(piece * 2 / 3)
		upper = int(piece * 3 / 2)
		size = random.randint(lower, upper)
		font = ImageFont.truetype(self.__font, size)
		return font

	def _rand_line(self):
		width, height = self.__size
		line_x = random.uniform(0, width / 2)
		line_y = random.uniform(0, height)
		point_x = random.uniform(width / 2, width)
		point_y = random.uniform(0, height)
		line_width = point_x - line_x
		line_height = point_y - line_y
		return ((line_x, line_y), (line_width, line_height))


def main():
	size = (100, 50)
	characters = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	number = 4
	font = os.path.join(DATA_DIR, 'msyhbd.ttf')

	generator = Captcha(size, characters, number, font)
	captcha, image = generator.generate()
	print(captcha)
	image.show()
	generator.save()


if __name__ == '__main__':
	main()