# -*- coding: utf-8 -*-

import sys
from os.path import abspath, dirname, join
from .linux import EventObj, start_listen_keyboard, start_listen_mouse
from .MainWindow import Ui_MainWindow

from PyQt5.QtWidgets import \
	QApplication, QMainWindow, QSystemTrayIcon, QMenu, \
	QAction, QWidget, QStyle
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize


main_window = None


# Convert:
# pyuic5 MainWindow.ui -o MainWindow.py

class MainWindow(QMainWindow, Ui_MainWindow):
	
	event_obj = None
	app = None
	tray_icon = None
	tray_menu = None
	status_active = False
	thread_listen_mouse = None
	thread_listen_keyboard = None
	
	
	def __init__(self):
		QMainWindow.__init__(self)
		
		# Create event obj
		self.event_obj = EventObj()
		self.event_obj.onLock = self.onLock
		self.event_obj.onUnLock = self.onUnLock
		
		# Set a title
		self.setupUi(self)
		self.setWindowTitle("Mouse locker")
		
		# Tray icon
		self.tray_icon = QSystemTrayIcon(self)
		self.setTrayIcon(3);
		
		# Tray menu
		self.tray_menu = QMenu()
		
		action_enable = QAction("Enable", self)
		action_enable.triggered.connect(self.onEnableClick)
		self.tray_menu.addAction(action_enable)
		
		action_disable = QAction("Disable", self)
		action_disable.triggered.connect(self.onDisableClick)
		self.tray_menu.addAction(action_disable)
		
		action_exit = QAction("Exit", self)
		action_exit.triggered.connect(self.onExitClick)
		self.tray_menu.addAction(action_exit)
		self.closeButton.clicked.connect(self.onExitClick)
		
		self.tray_icon.setContextMenu(self.tray_menu)
		self.tray_icon.show()
	
		# Set Window Center
		desktop = QApplication.desktop()
		screen_width = desktop.width()
		screen_height = desktop.height()
		
		window_size = self.size()
		width = window_size.width(); 
		height = window_size.height();
		
		x = (screen_width - width) / 2;
		y = (screen_height - height) / 2;
		self.move ( x, y );
		
	def setTrayIcon(self, index):
		path = join(abspath(dirname(__file__)), "images/" + str(index) + ".ico")
		self.tray_icon.setIcon( QIcon( path ) )
	
	
	def onEnableClick(self):
		
		if self.status_active == False:
			self.status_active = True
			self.setTrayIcon(1);
			self.startListenKeyboard()
		
		
	def onDisableClick(self):
		
		if self.status_active == True:
			self.status_active = False
			self.setTrayIcon(3);
			self.stopListenKeyboard()
			self.stopListenMouse()
	
	
	def onLock(self):
		self.setTrayIcon(2);
		self.startListenMouse();
		pass
		
		
	def onUnLock(self):
		self.setTrayIcon(1);
		self.stopListenMouse();
		pass
	
	
	def startListenMouse(self):
		if self.thread_listen_mouse == None:
			self.event_obj.is_listen_mouse = True
			self.thread_listen_mouse = start_listen_mouse(self.event_obj)
			
	def stopListenMouse(self):
		if self.thread_listen_mouse != None:
			self.event_obj.is_listen_mouse = False
			self.thread_listen_mouse.join()
			self.thread_listen_mouse = None
			
	
	def startListenKeyboard(self):
		if self.thread_listen_keyboard == None:
			self.event_obj.is_listen_keyboard = True
			self.thread_listen_keyboard = start_listen_keyboard(self.event_obj)
			
	def stopListenKeyboard(self):
		if self.thread_listen_keyboard != None:
			self.event_obj.is_listen_keyboard = False
			self.thread_listen_keyboard.join()
			self.thread_listen_keyboard = None
	
	
	def onExitClick(self):
		self.app.quit()
		self.stopListenKeyboard()
		self.stopListenMouse()
		pass
	
	
	def closeEvent(self,event):
		self.stopListenKeyboard()
		self.stopListenMouse()
	
	
def run():
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.app = app;
	main_window.show()
	sys.exit(app.exec())
