# -*- coding: utf-8 -*-

# Xlib documentation
# http://python-xlib.sourceforge.net/doc/html/python-xlib_16.html
# http://python-xlib.sourceforge.net/doc/html/python-xlib_21.html

import Xlib, threading
from Xlib.display import Display
from Xlib import X
from time import sleep
from Xlib.ext.xtest import fake_input


class EventObj:
	
	is_listen_mouse = False
	is_listen_keyboard = False
	
	KEY_CODE_LOCK = 106
	KEY_CODE_UNLOCK = 63



def get_active_window(display):
	root = display.screen().root
	NET_ACTIVE_WINDOW = display.intern_atom('_NET_ACTIVE_WINDOW')
	win_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
	try:
		return display.create_resource_object('window', win_id)
	except Xlib.error.XError:
		pass
	

def get_window_rect(win, root):
	g = win.get_geometry()
	x = g.x
	y = g.y
	while win.id != root.id:
		win = win.query_tree().parent
		r = win.get_geometry()
		x += r.x
		y += r.y
	
	return (x, y, g.width, g.height)
	
	
def set_mouse_pos(display, x, y):
	fake_input(display, X.MotionNotify, x=x, y=y)
	display.sync()
	

def listen_mouse(event_obj):
	
	display = Display(":0")
	root = display.screen().root
	active_window = get_active_window(display)
	active_window_rect = get_window_rect(active_window, root)

	while event_obj.is_listen_mouse:
		data = root.query_pointer()._data
		
		is_new = False
		x = data["root_x"]
		y = data["root_y"]
		new_x = x
		new_y = y
		
		if x < active_window_rect[0] + 3:
			is_new = True
			new_x = active_window_rect[0] + 3
		
		if y < active_window_rect[1] + 3:
			is_new = True
			new_y = active_window_rect[1] + 3
		
		if x > active_window_rect[0] + active_window_rect[2] - 3:
			is_new = True
			new_x = active_window_rect[0] + active_window_rect[2] - 3
		
		if y > active_window_rect[1] + active_window_rect[3] - 3:
			is_new = True
			new_y = active_window_rect[1] + active_window_rect[3] - 3
		
		if is_new:
			set_mouse_pos(display, new_x, new_y)
		
		sleep(0.05)

		
		
def start_listen_mouse(event_obj):
	t = threading.Thread(target=listen_mouse, args=(event_obj,))
	t.start()
	return t
	

def keyboard_event(event_obj, e):
	keycode = e.detail
	if e.type == X.KeyPress:
		if keycode == event_obj.KEY_CODE_LOCK:
			event_obj.onLock()
		if keycode == event_obj.KEY_CODE_UNLOCK:
			event_obj.onUnLock()
		
		
def listen_keyboard(event_obj):
	
	time = X.CurrentTime
	display = Display(":0")
	root = display.screen().root
	
	#root.grab_keyboard(True, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)
	#root.grab_key(X.AnyKey, X.AnyModifier, True, X.GrabModeAsync, X.GrabModeAsync)
	root.grab_key(event_obj.KEY_CODE_LOCK, X.AnyModifier, True, X.GrabModeAsync, X.GrabModeAsync)
	root.grab_key(event_obj.KEY_CODE_UNLOCK, X.AnyModifier, True, X.GrabModeAsync, X.GrabModeAsync)
	
	while (event_obj.is_listen_keyboard):
		
		if root.display.pending_events() > 0:		
			ev = root.display.next_event()
			try:
				keyboard_event(event_obj, ev)
			except Exception as e:
				print (e)
				pass
			
			#display.send_event(ev.child, ev)
			#display.allow_events(X.ReplayKeyboard, X.CurrentTime)
		
		sleep(0.05)
		
		
def start_listen_keyboard(event_obj):
	t = threading.Thread(target=listen_keyboard, args=(event_obj,))
	t.start()
	return t
	