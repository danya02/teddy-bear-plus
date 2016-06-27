#!/usr/bin/python3
#    Teddy-bear Plus: a remote-presence parenting device
#    Copyright (C) 2016 Danya Generalov

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import time
class Button:
	def __init__(self,pin,notgnd):
		import RPi.GPIO
		self._gpio=RPi.GPIO
		self._pin_=pin
		self._gpio.setmode(self._gpio.BOARD)
		self._gpio.setwarnings(False)
		self._gpio.setup(self._pin_,self._gpio.IN,self._gpio.PUD_UP)
	def get_state(self):
		self._gpio.setmode(self._gpio.BOARD)
		self._gpio.setwarnings(False)
		self._gpio.setup(self._pin_,self._gpio.INPUT,self._gpio.PUD_UP)
		return self._gpio.input(self._pin_)
	def wait_for(self,which):
		self._gpio.wait_for_edge(self._pin_,which)	
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
b=Button(3,False)
while 1:
	l.color=[0,1,0]
	b.wait_for(b._gpio.FALLING)
	l.color=[0,0,0]
	b.wait_for(b._gpio.RISING)
