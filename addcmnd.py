import tkinter as tk
import os
import time

line_index = 78
lines = None

pypath = os.getcwd() + '\pyvoice.py'

newline = '\n        '

def add(program, path):
    global win
    para = "\n    elif command == 'open " + program + "' or command == '" + program + ":" + newline + "mssge = tk.Text(win, height = 1, width = 50)" + newline + "mssge.insert(tk.INSERT, 'Opening " + program + "...')" + newline + "mssge.pack()" + newline + "win.update()" + newline + "sen = 'Opening " + program + "'" + newline + "ttseng.say(sen)" + newline + "ttseng.runAndWait()" + newline + "os.startfile('" + path + "')" + newline + "time.sleep(1)" + newline + "mssge.pack_forget()\n"

    with open(pypath, 'r') as file_handler:
        lines = file_handler.readlines()

    lines.insert(line_index, para)

    with open(pypath, 'w') as file_handler:
       file_handler.writelines(lines)

    succ = tk.StringVar()
    succ.set("Success!!")
    out = tk.Label(win, textvariable = succ)
    out.grid(row=2, column=1)
    win.update()
    time.sleep(2)
    exit()

win = tk.Tk()
win.geometry("235x75")
win.title("Add Program Path")
dis1 = tk.StringVar()
dis1.set("Program name: ")
pr = tk.Label(win, textvariable = dis1)
dis2 = tk.StringVar()
dis2.set("Program path: ")
pa = tk.Label(win, textvariable = dis2)
pre = tk.Entry(win)
pae = tk.Entry(win)
btn = tk.Button(win, text='Add', height=1, width=7, command = lambda: add(pre.get(),pae.get()))
pr.grid(row = 0, column = 0)
pa.grid(row = 1, column = 0)
pre.grid(row = 0, column = 1)
pae.grid(row = 1, column = 1)
btn.grid(row = 2, column = 0)

win.mainloop()
