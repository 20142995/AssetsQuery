#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import sys
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import *
from tkinter.messagebox import *
from query import local_query,remote_query,update_data


class Application_ui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('溯源')
        self.master.geometry('603x418')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.output_textFont = Font(font=('宋体',9))
        self.output_text = Text(self.top, font=self.output_textFont)
        self.output_text.place(relx=0., rely=0.502, relwidth=0.997, relheight=0.481)

        self.style.configure('query_button.TButton',font=('宋体',16))
        self.query_button = Button(self.top, text='查询', command=self.query_button_Cmd, style='query_button.TButton')
        self.query_button.place(relx=0.415, rely=0.12, relwidth=0.167, relheight=0.17)

        self.style.configure('update_button.TButton',font=('宋体',9))
        self.update_button = Button(self.top, text='更新', command=self.update_button_Cmd, style='update_button.TButton')
        self.update_button.place(relx=0.879, rely=0.12, relwidth=0.085, relheight=0.074)

        self.input_textFont = Font(font=('宋体',9))
        self.input_text = Text(self.top, font=self.input_textFont)
        self.input_text.place(relx=0., rely=0.072, relwidth=0.35, relheight=0.337)

        self.style.configure('Label1.TLabel',anchor='w', font=('宋体',9))
        self.Label1 = Label(self.top, text='待查询的IP', style='Label1.TLabel')
        self.Label1.place(relx=0.066, rely=0.024, relwidth=0.234, relheight=0.05)

        self.style.configure('Label3.TLabel',anchor='w', font=('宋体',9))
        self.Label3 = Label(self.top, text='查询结果', style='Label3.TLabel')
        self.Label3.place(relx=0.066, rely=0.455, relwidth=0.134, relheight=0.05)


class Application(Application_ui):
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

    def query_button_Cmd(self, event=None):
        if self.input_text.get("0.0","end").strip():
            ip_str = ",".join([i for i in self.input_text.get("0.0","end").split("\n") if i.strip()])
            items = []
            items.append("\t".join(["来源", "IP", "IP/MASK", "IP属性","承载设备","负责部门","负责人"]))
            for item in local_query(ip_str).get("list",[]):
                items.append("\t".join(["本地",]+item))
            for item in remote_query(ip_str).get("list",[]):
                items.append("\t".join(item))
            self.output_text.delete('1.0','end')
            self.output_text.insert(INSERT,"\n".join(items))

    def update_button_Cmd(self, event=None):
        update_data()

if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()
    try: top.destroy()
    except: pass
