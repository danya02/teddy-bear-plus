#!/usr/bin/python3
import time
class RGBLED:
	def __setattr__(self,prop,val):
		object.__setattr__(self,prop,val)
		if prop=="color":self.set_color(val[0],val[1],val[2])
		if prop=="red":self._red(val)
		if prop=="green":self._green(val)
		if prop=="blue":self._blue(val)
	def __init__(self,r,g,b):
		import RPi.GPIO
		self._gpio=RPi.GPIO
		self._r_=r
		self._g_=g
		self._b_=b
		self.color=[0,0,0]
		self._gpio.setmode(self._gpio.BOARD)
		self._gpio.setwarnings(False)
		for i in (self._r_,self._g_,self._b_):
			self._gpio.setup(i,self._gpio.OUT)
			self._gpio.output(i,0)
	def _red(self,m):
		self.set_color(m,self.color[1],self.color[2])
	def _green(self,m):
		self.set_color(self.color[0],m,self.color[2])
	def _blue(self,m):
		self.set_color(self.color[0],self.color[1],m)
	def set_color(self,r,g,b):
		self._gpio.setmode(self._gpio.BOARD)
		self._gpio.setwarnings(False)
		for i,j in zip((self._r_,self._g_,self._b_),(r,g,b)):
			self._gpio.setup(i,self._gpio.OUT)
			self._gpio.output(i,j)
	def invert(self):
		a=[0,0,0]
		for i,j in zip(self.color,[0,1,2]):
			a[j]=not i
		self.color=a
		a=None
	def on(self):self.color=[1,1,1]
	def off(self):self.color=[0,0,0]
l=RGBLED(7,12,11)
l.color=[0,1,0]
