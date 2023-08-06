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
	
	mouse_lock_type = 1
	mouse_inc = 1
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
	
	if event_obj.mouse_lock_type == 1:
		
		while event_obj.is_listen_mouse:
			data = root.query_pointer()._data
			
			is_new = False
			x = data["root_x"]
			y = data["root_y"]
			new_x = x
			new_y = y
			
			if x <= active_window_rect[0] + event_obj.mouse_inc:
				is_new = True
				new_x = active_window_rect[0] + event_obj.mouse_inc
			
			if y <= active_window_rect[1] + event_obj.mouse_inc:
				is_new = True
				new_y = active_window_rect[1] + event_obj.mouse_inc
			
			if x >= active_window_rect[0] + active_window_rect[2] - event_obj.mouse_inc:
				is_new = True
				new_x = active_window_rect[0] + active_window_rect[2] - event_obj.mouse_inc
			
			if y >= active_window_rect[1] + active_window_rect[3] - event_obj.mouse_inc:
				is_new = True
				new_y = active_window_rect[1] + active_window_rect[3] - event_obj.mouse_inc
			
			if is_new:
				set_mouse_pos(display, new_x, new_y)
			
			sleep(0.005)

	
	else:
	
		# X.NoEventMask
		# X.ButtonPressMask | X.ButtonReleaseMask | X.KeyPressMask | X.KeyReleaseMask
		# X.EnterWindowMask | X.LeaveWindowMask | X.PointerMotionMask
		active_window.grab_pointer(True, X.ButtonPressMask | X.ButtonReleaseMask, \
			X.GrabModeAsync, X.GrabModeAsync, active_window, 0, X.CurrentTime)
		
		#print (1)
		#print (X.ButtonPressMask)
		#print (X.ButtonReleaseMask)
		print (active_window.get_wm_name())
		print (active_window.get_wm_class())
		prev_time = X.CurrentTime
		
		while event_obj.is_listen_mouse:
			
			#display.allow_events(X.ReplayPointer, X.CurrentTime)
			
			pos = root.display.pending_events()
			count = pos
			while pos > 0:
				e = root.display.next_event()
				active_window.send_event(e)
				#print (e.window.get_wm_class())
				#display.send_event(active_window, e, X.ButtonPressMask | X.ButtonReleaseMask)
				pos = pos - 1
			
			if count > 0:
				#display.flush()
				#display.allow_events(X.AllowReplayPointer, prev_time)
				prev_time = X.CurrentTime
			
			sleep(0.01)
		
		#print (2)
		
		#display.flush()
		display.ungrab_pointer(X.CurrentTime)
		display.sync()
	
	
	
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
	prev_time = X.CurrentTime
	
	while (event_obj.is_listen_keyboard):
		
		pos = root.display.pending_events()
		count = pos
		while pos > 0:
			e = root.display.next_event()
			pos = pos - 1
			
			try:
				keyboard_event(event_obj, e)
			except Exception as e:
				print (e)
				pass
			
			#active_window = get_active_window(display)
			#e.window = active_window
			#active_window.send_event(e)
			#print(e.window)
			#print(active_window)
			
			#display.send_event(ev.child, e)
			#display.allow_events(X.ReplayKeyboard, X.CurrentTime)
		
		#if count > 0:
		#	display.flush()
		#	display.allow_events(X.ReplayKeyboard, prev_time)
		#	prev_time = X.CurrentTime
		
		sleep(0.01)
	
	#display.flush()
	display.ungrab_keyboard(X.CurrentTime)
	display.sync()
	
def start_listen_keyboard(event_obj):
	t = threading.Thread(target=listen_keyboard, args=(event_obj,))
	t.start()
	return t
	