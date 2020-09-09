#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import * 
import windnd
import hashlib
import time
from tkinter.messagebox import showinfo
import os
import chardet
import re
 

LOG_LINE_NUM = 0
image = None
image2 = None
labelInfo = None
btnStart = None
btnClear = None
icon = None
fileArr = []
msg = ''
class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    #设置窗口
    def set_init_window(self):
        screen_width = self.init_window_name.winfo_screenwidth()
        screen_height = self.init_window_name.winfo_screenheight()
        window_width = 1000
        window_height = 680
        posX = int((screen_width - window_width) * .5)
        posY = int((screen_height - window_height) * .5)

        self.init_window_name.title("ass->srt转换工具") 
        self.init_window_name.geometry(str(window_width) + 'x' +str(window_height) +'+'+str(posX)+'+'+str(posY))
        frame1 = Frame(width = 800,height=100, bd=1, relief="sunken")
        frame1.pack(fill=BOTH,padx=50, pady=40,expand=False)

        frame2 = Frame(width = 800,height=100, bd=0, relief="sunken")
        frame2.pack(fill=BOTH,padx=50, pady=0,expand=False)


        windnd.hook_dropfiles(frame1,func = dragged_files)
        global labelInfo
        labelInfo = Label(frame1, text="将文件或文件夹拖入此处",width = 50,height = 15)
        labelInfo.pack(expand=FALSE,fill=BOTH)
        curPath = os.path.dirname(__file__)
        finalPath = os.path.join(curPath,"img/btn_start.png")
        global image
        image = PhotoImage(file = finalPath)

        global icon
        iconPath = os.path.join(curPath,"img/icon.ico")
        icon = PhotoImage(iconPath)
        self.init_window_name.iconbitmap(icon)      #窗口名

        global btnStart
        btnStart = Button(frame2,text ="转换",image = image,bd = 0,relief = FLAT,command=btnConvertCBK)
        btnStart.pack(side = LEFT,pady=2 )
        btnStart["state"] = DISABLED

        
        finalPath = os.path.join(curPath,"img/btn_clear.png")
        global image2
        image2 = PhotoImage(file = finalPath)
        btnClear = Button(frame2,text ="清除",image = image2,bd = 0,relief = FLAT,command=btnClearCBK)
        btnClear.pack(side = LEFT,pady=2,padx = 10 )
        btnClear["state"] = NORMAL
        
    


    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

def clearAll():
        global msg
        msg = ''
        global fileArr
        fileArr = []
        global btnStart
        btnStart['state'] = DISABLED
        global labelInfo
        labelInfo['text'] = "将文件或文件夹拖入此处"
#转换单个文件
def convertFile(file):
    msg = ''
    index = 1
    if str(file).endswith('.ass'):
        _encoding = ''
        with open(file, 'rb') as f:
            data = f.read()
            _encoding = chardet.detect(data)['encoding']
            print('cur encoding ->' + _encoding)
        with open(file, "r",encoding=_encoding,errors='ignore') as f:
            for line in f.readlines():
                if 'Dialogue' in line:
                    msg = msg + str(index) + "\n"
                    #去除所有特效
                    result = re.sub('\{.*?\}', '', line)
                    #先把英文分离出来
                    strArr = result.split('\\N')
                    if len(strArr) > 0:
                        before = strArr[0]
                        beforeArr = before.split(',')
                        timeStart = beforeArr[1]
                        timeEnd = beforeArr[2]
                        beginTime = timeStart.split('.')[0]
                        beginTime2 = timeStart.split('.')[1]
                        endTime = timeEnd.split('.')[0]
                        endTime2 = timeEnd.split('.')[1]
                        msg = msg + beginTime + "," + str(int(beginTime2) * 10) + " --> " + endTime + ',' + str(int(endTime2) * 10) + '\n'
                        text = beforeArr[9]
                        msg = msg + text + "\n"
                    if len(strArr) > 1:
                        msg = msg + strArr[1] + "\n"
                    index = index + 1
        savePath = file.replace('.ass','.srt')
        with open(savePath,'w',encoding=_encoding,errors='ignore') as file_handle:   # .txt可以不自己新建,代码会自动新建
            file_handle.write(msg)     # 写入
                    
    else:
        showinfo("错误","不支持的格式")
    
#清除按钮
def btnClearCBK():
    clearAll()

def btnConvertCBK():
    global labelInfo
    labelInfo['text'] = "开始转换"
    global fileArr
    for file in fileArr:
        convertFile(file)
    clearAll()
    labelInfo['text'] = "转换完成"

def getAllFileInDir(dir):
    dirs = os.listdir(dir)
    for file in dirs:
        filePath = os.path.join(dir,file)
        if os.path.isdir(filePath):
            getAllFileInDir(filePath)
        elif os.path.isfile(filePath):
            if str(filePath).endswith('.ass'):
                global fileArr
                fileArr.append(filePath)
                global msg
                msg = msg + '\n' + filePath
    
def dragged_files(files):
    global msg
    msg = ''
    global fileArr
    fileArr = []
    for item in files:
        #先判断拖入的是文件还是文件夹
        filePath = item.decode('gbk')
        if os.path.isdir(filePath):
            getAllFileInDir(filePath)

        elif os.path.isfile(filePath):
            if str(filePath).endswith('.ass'):
                fileArr.append(filePath)
                msg = msg + '\n' + filePath
        else:
            print('i dont know what is this')
    global labelInfo
    if len(fileArr) == 0:
        labelInfo['text'] = '根本没有找到任何ass文件'
        btnStart['state'] = DISABLED
    else:
        labelInfo['text'] = msg
        btnStart['state'] = NORMAL
    

def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()