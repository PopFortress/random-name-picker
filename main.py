'''
随机点名 0.1.0
by Fortress
'''
import ctypes
import tkinter as tk
from tkinter.ttk import *
import tkinter.messagebox as msgbox
from random import choice
from tkinter import simpledialog
from tktooltip import ToolTip
from tkinter.filedialog import askopenfilename, asksaveasfilename
from time import sleep
import threading

# 创建高清窗口
root = tk.Tk()
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
root.tk.call('tk', 'scaling', ScaleFactor/75)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.title('随机点名 - Fortress Software')
root.geometry(f'{int(screen_width / 1.5)}x{int(screen_height / 1.5)}+500+200')

# 常量定义
REGULAR_COLOR = '#1d1d1f'
PRIMARY_COLOR = '#f3ab12'
PENDING_COLOR = '#acacac'
CONTENT_FONT = ('微软雅黑', 12)
TITLE_FONT = ('微软雅黑', 50)
ADD = '添加'
DEL = '删除'
CLR = '清空'
IMPORT_FROM_TXT_FILE = '从文本文档中导入...'
EXPORT_PROFILE = '导出为配置文件...'
PICK_RANDOM_NAME = '随机点名'
ERR = '错误'
READ_ERR = '无法读取文件内容为纯文本'
WRITE_ERR = '无法写入文件内容为纯文本'
ADD_NAME_WIN_TITLE = '添加...'
ADD_NAME_WIN_PROMPT = '请输入姓名'
FILE_CHOOSER_FILE_TYPES = [('名单文件','*.nl'),('文本文档', '*.txt'),('所有文件', '*.*')]
IMPORT_BTN_TOOLTIP = '从文本文档或配置文件中导入名单，一行一个姓名'
EXPORT_BTN_TOOLTIP = '将名单导出为配置文件，以便下次导入'
IMPORT_DLG_TITLE = '选择文件...'
EXPORT_DLG_TITLE = '另存为...'
WAITING = '等待...'

nameLstVar = tk.Variable()
nameLstVar.set(['',])


# 功能函数定义
def addName():
    name = simpledialog.askstring(ADD_NAME_WIN_TITLE, ADD_NAME_WIN_PROMPT, parent=root)
    if name:
        if nameLstVar.get() == ('',):
            nameLstVar.set([name,])
        else:
            nameLstVar.set(nameLstVar.get() + (name,))
def delName():
    nameLstbox.delete(tk.ANCHOR)
def clrName():
    nameLstVar.set(['',])
def importFromFile():
    file = askopenfilename(filetypes=FILE_CHOOSER_FILE_TYPES, parent=root, title=IMPORT_DLG_TITLE)
    if file:
        try:
            with open(file, 'r', encoding='utf-8') as file:
                nameLstVar.set(file.read().splitlines())
        except:
            msgbox.showerror(ERR, READ_ERR)
def exportToFile():
    file = asksaveasfilename(filetypes=FILE_CHOOSER_FILE_TYPES, parent=root, title=EXPORT_DLG_TITLE, initialfile='新建名单.nl')
    if file:
        try:
            with open(file, 'w', encoding='utf-8') as file:
                file.write('\n'.join(nameLstVar.get()))
        except:
            msgbox.showerror(ERR, WRITE_ERR)
def __random_name_thread():
    nameLstbox.selection_clear(0, tk.END)
    root.protocol('WM_DELETE_WINDOW', ...)  # 防止引发 RuntimeError
    randomNameBtn['state'] = 'disabled'

    randomNameLabel['foreground'] = REGULAR_COLOR
    randomNameLabel['text'] = WAITING
    sleep(1)
    
    randomNameLabel['foreground'] = PENDING_COLOR
    for i in range(1,20,1):
        name = choice(nameLstVar.get())
        randomNameLabel['text'] = name
        sleep(i/40)
    randomNameLabel['foreground'] = PRIMARY_COLOR

    root.protocol('WM_DELETE_WINDOW', root.destroy)
    randomNameBtn['state'] = 'normal'
def pickRandomName():
    if nameLstVar.get() != ('',) and nameLstVar.get():
        thread = threading.Thread(target=__random_name_thread)
        thread.start()


# 创建界面
# 基础框架
mainPanel = Frame(root)
operationPanel = Frame(mainPanel)
experiencePanel = Frame(mainPanel)

# 操作面板
nameLstbox = tk.Listbox(operationPanel, height=13, width=21, font=CONTENT_FONT, listvariable=nameLstVar)
lstOperationsFrame = Frame(operationPanel)
addBtn = Button(lstOperationsFrame, text=ADD, width=8, command=addName)
delBtn = Button(lstOperationsFrame, text=DEL, width=8, command=delName)
clrBtn = Button(lstOperationsFrame, text=CLR, width=8, command=clrName)
importBtn = Button(operationPanel, text=IMPORT_FROM_TXT_FILE, width=27, command=importFromFile)
exportBtn = Button(operationPanel, text=EXPORT_PROFILE, width=27, command=exportToFile)

# 功能面板
randomNameLabel = Label(experiencePanel, text='...', font=TITLE_FONT, foreground=REGULAR_COLOR)
randomNameBtn = Button(experiencePanel, text=PICK_RANDOM_NAME, command=pickRandomName)


# 放置组件
mainPanel.pack(pady=30)
operationPanel.pack(padx=40, side='left')
experiencePanel.pack(padx=100, side='right')
nameLstbox.pack(pady=10)
lstOperationsFrame.pack()
addBtn.grid(row=0, column=0)
delBtn.grid(row=0, column=1, padx=8)
clrBtn.grid(row=0, column=2)
importBtn.pack(pady=10)
exportBtn.pack()
randomNameLabel.pack(pady=30)
randomNameBtn.pack(ipadx=30, ipady=10)

# 给组件绑定 Tooltip
ToolTip(importBtn, IMPORT_BTN_TOOLTIP)
ToolTip(exportBtn, EXPORT_BTN_TOOLTIP)

# MAINLOOP
root.mainloop()