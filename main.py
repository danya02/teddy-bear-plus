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
global l
global s
s=6
l=RGBLED(7,12,11)
b=Button(3,False)
def status():
	from time import sleep
	global s
	global l
	while 1:
		if s==-1: # hidden
			l.color=[0,0,0]
		if s==0: # idle, not controlled
			l.color=[1,0,0]
			sleep(0.25)
			l.color=[0,0,0]
			sleep(3.75)
		if s==1: # idle, controlled
			l.color=[0,1,0]
			sleep(0.1)
		if s==2: # Xferring
			l.color=[0,0,1]
			sleep(0.5)
			l.color=[0,0,0]
			sleep(0.5)
		if s==3: # visualizing (e.g playing audio,..)
			l.color=[0,1,0]
			sleep(0.5)
			l.color=[0,0,0]
			sleep(0.5)
		if s==4: # recording audio
			l.color=[1,0,0]
			sleep(0.25)
			l.color=[0,0,0]
			sleep(0.25)
		if s==5: # preparing to take photo
			l.color=[0,1,0]
			sleep(0.25)
			l.color=[0,0,1]
			sleep(0.25)
		if s==6: # obfuscated
			import random
			l.color=random.choice([[1,0,0],[0,1,0],[0,0,1],[0,0,0]])
			sleep(random.random())
		if s==7: # encountering an error
			l.color=[1,0,0]
			sleep(0.5)
			l.color=[0,0,1]
			sleep(0.5)
import threading
blinkenlights=threading.Thread(name="Blinkenlights function",target=status)
blinkenlights.start()
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
	bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
	bot.sendMessage(update.message.chat_id, text='Help!')
global mode
mode=False

def echo(bot, update):
	global s
	global mode
	if not mode:
		bot.sendMessage(update.message.chat_id, text=update.message.text)
	else:
		try:
			s=int(update.message.text)
			bot.sendMessage(update.message.chat_id, text="Succesfully set mode to "+str(s))
		except:bot.sendMessage(update.message.chat_id, text="Failed to set mode to "+str(s))
	mode=False
		
def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))
def setmode(bot,update):
	bot.sendMessage(update.message.chat_id, text="Send, as number in -1~7, the displayed mode of operation.")
	global mode
	mode=True
def telegrammar():
    # Create the EventHandler and pass it your bot's token.
	updater = Updater("135232412:AAFfA6JImKl4sxv35IAw2f2Zjq7gb67Jk7Q")

    # Get the dispatcher to register handlers
	dp = updater.dispatcher

    # on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("mode",setmode))
    # on noncommand i.e message - echo the message on Telegram
	dp.add_handler(MessageHandler([Filters.text], echo))
	dp.add_error_handler(error)
	updater.start_polling()
	updater.idle()
telegrammar()
