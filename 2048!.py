import random
import math


_map_data = [
[0,0,0,0],
[0,0,0,0],
[0,0,0,0],
[0,0,0,0]]

def _left_move_number(line):
	moveflag = False
	for _ in range(3):
		for i in range(3):
			if line[i] == 0:
				line[i] = line[i + 1]
				line[i + 1] = 0
				moveflag = True
	return moveflag

def _left_plus_number(line):
	for i in range(3):
		if line[i] == line[i + 1]:
			moveflag = True
			line[i] *= 2
			line[i + 1] = 0

def _left_do_number(line):
	moveflag = False
	if _left_move_number(line):
		moveflag = True
	if _left_plus_number(line):
		moveflag = True
	if _left_move_number(line):
		moveflag = True
	return moveflag

def left():
	moveflag = False
	for line in _map_data:
		if _left_do_number(line):
			moveflag = True
	return moveflag

def right():
	for line in _map_data:
		line.reverse()
	moveflag = left()
	for line in _map_data:
		line.reverse()
	return moveflag

def up():
	moveflag = False
	line = [0, 0, 0, 0]
	for r in range(4):
		for c in range(4):
			line[c] = _map_data[c][r]
		if _left_do_number(line):
			moveflag = True
		for c in range(4):
			_map_data[c][r] = line[c]
	return _map_data

def down():
	_map_data.reverse()
	moveflag = up()
	_map_data.reverse()
	return moveflag

def reset():
	_map_data[:] = []
	_map_data.append([0, 0, 0, 0])
	_map_data.append([0, 0, 0, 0])
	_map_data.append([0, 0, 0, 0])
	_map_data.append([0, 0, 0, 0])
	fill2()
	fill2()

def get_space_count():
	count = 0
	for i in _map_data:
		count += i.count(0)
	return count

def get_score():
	score = 0
	for r in _map_data:
		for c in r:
			score += 0 if c < 4 else c * int((math.log(c, 2) - 1.0))
	return score

def fill2():
	back_count = get_space_count()
	if back_count == 0:
		return False
	n = random.randrange(back_count)
	offset = 0
	for row in _map_data:
		for col in range(4):
			if row[col] == 0:
				if offset == n:
					row[col] = 2
					return True
				offset += 1

def is_game_over():
	for r in _map_data:
		if r.count(0) != 0:
			return False
		for i in range(3):
			if r[i] == r[i + 1]:
				return False
	for r in range(4):
		for c in range(3):
			if _map_data[c][r] == _map_data[c + 1][r]:
				return False
	return True




from tkinter import *
from tkinter import messagebox

def main():

	reset()

	root = Tk()
	root.title('2048')
	root.resizable(width=False, height=False)

	keymap={
	'w':up,
	's':down,
	'a':left,
	'd':right,
	'Up':up,
	'Down':down,
	'Left':left,
	'Right':right,
	'q':root.quit
	}

	game_bg_color = "#bbbbbb"  

	mapcolor = {
		0: ("#cdc1b4", "#776e65"),
		2: ("#eee4da", "#776e65"),
		4: ("#ede0c8", "#f9f6f2"),
		8: ("#f2b179", "#f9f6f2"),
		16: ("#f59563", "#f9f6f2"),
		32: ("#f67c5f", "#f9f6f2"),
		64: ("#f65e3b", "#f9f6f2"),
		128: ("#edcf72", "#f9f6f2"),
		256: ("#edcc61", "#f9f6f2"),
		512: ("#e4c02a", "#f9f6f2"),
		1024: ("#e2ba13", "#f9f6f2"),
		2048: ("#ecc400", "#f9f6f2"),
		4096: ("#ae84a8", "#f9f6f2"),
		8192: ("#b06ca8", "#f9f6f2"),
		2**14: ("#b06ca8", "#f9f6f2"),
		2**15: ("#b06ca8", "#f9f6f2"),
		2**16: ("#b06ca8", "#f9f6f2"),
		2**17: ("#b06ca8", "#f9f6f2"),
		2**18: ("#b06ca8", "#f9f6f2"),
		2**19: ("#b06ca8", "#f9f6f2"),
		2**20: ("#b06ca8", "#f9f6f2"),
	}

	def on_key(event):
		keysym = event.keysym
		if keysym in keymap:
			if keymap[keysym]():
				fill2()
				update_ui()
		if is_game_over():
			mb = messagebox.askyesno(title='gameover', message='game over,\n retry?')
			if mb:
				root.quit()
			else:
				reset()
				update_ui()


	def update_ui():
		for r in range(4):
			for c in range(4):
				number = _map_data[r][c]
				label = map_label[r][c]
				label['text'] = str(number) if number else ''
				label['bg'] = mapcolor[number][0]
				label['foreground'] = mapcolor[number][1]
		label_score['text'] = str(get_score())

	frame = Frame(root, width=200, height=200, background='gray')
	frame.grid(sticky=N+S+E+W)
	frame.focus_set()
	frame.bind('<Key>',on_key)

	map_label = []
	for r in range(4):
		row = []
		for c in range(4):
			value = _map_data[r][c]
			text = str(value) if value else ''
			label = Label(frame, text=text, width=4, height=2, font=("黑体", 30, "bold"))
			label.grid(row=r, column=c, padx=5, pady=5, sticky=N+S+E+W)
			row.append(label)
		map_label.append(row)		
	
	label = Label(frame, text='分數', font=("黑体", 30, "bold"), bg="#bbada0", fg="#eee4da")
	label.grid(row=4, column=0, padx=5, pady=5)
	label_score = Label(frame, text='0', font=("黑体", 30, "bold"), bg="#bbada0", fg="#eee4da")
	label_score.grid(row=4, columnspan=2, column=1, padx=5, pady=5)

	def restart_button():
		reset()
		update_ui()

	button = Button(frame, text='restart', font=("黑体", 16, "bold"),
	 bg="#8f7a66", fg="#f9f6f2", command=restart_button)
	button.grid(row=4, column=3, padx=5, pady=5)


	frame.pack()
	update_ui()
	mainloop()

main()

