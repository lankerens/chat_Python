import tkinter
# 导入消息对话框子模块
import tkinter.simpledialog

from mapper.userMapper import createGroup, joinGroup, exitGroup


#  创建群组
def cgPanel(mid):
    # 创建主窗口
    root = tkinter.Tk()
    # 设置窗口大小
    # root.minsize(300, 300)

    # 窗口居中  =============  start  ====================
    # 窗口尺寸
    # window.geometry('1000x640')
    sw = root.winfo_screenwidth()
    # 得到屏幕宽度
    sh = root.winfo_screenheight()
    # 得到屏幕高度
    ww = 300
    wh = 300
    # 窗口宽高为100
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    root.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    # 窗口居中  =============  end  ====================

    cgname = ''

    # 创建函数
    def cg():
        cgname = (var_usr_cgname.get()).strip()
        if cgname == '' :
            tkinter.messagebox.showerror(message='Error, 群组名称不能为空, try again.')
            return

        #  数据库操作
        b = createGroup(mid, cgname)
        #  if effect 成功 >>  然后提示创建成功...
        if b :
            # 获取整型（标题，提示，初始值）
            result = tkinter.messagebox.showinfo(title = '信息提示！',message='内容：创建群组 [' + cgname + '] 成功 ! \n \n  重新启动软件生效 ! ')
            # 打印内容  ok
            # print(result)
            if result == 'ok' :
                #  销毁窗口
                root.destroy()
        else :
            tkinter.messagebox.showerror(message='Error, 出现了不可预料的错误，抱歉, try again.')
            return


    tkinter.Label(root, text='输入群组名称:  ', font=('Arial', 12)).place(x=10, y=80)
    var_usr_cgname = tkinter.StringVar()  # 定义变量
    tkinter.Entry(root, textvariable=var_usr_cgname).place(x = 130, y = 80)

    # 添加按钮
    btn = tkinter.Button(root, text='创建该群组', command=cg).place(x = 120, y = 150)
    # btn.pack()

    # 加入消息循环
    root.mainloop()




#  加入群组
def jgPanel(mid):
    # 创建主窗口
    root = tkinter.Tk()
    # 设置窗口大小
    # root.minsize(300, 300)

    # 窗口居中  =============  start  ====================
    # 窗口尺寸
    # window.geometry('1000x640')
    sw = root.winfo_screenwidth()
    # 得到屏幕宽度
    sh = root.winfo_screenheight()
    # 得到屏幕高度
    ww = 300
    wh = 300
    # 窗口宽高为100
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    root.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    # 窗口居中  =============  end  ====================

    gid = ''

    # 创建函数
    def jg():
        gid = (var_usr_gid.get()).strip()
        if gid == '':
            tkinter.messagebox.showerror(message='Error, 群组py号 不能为空, try again.')
            return

        #  数据库操作
        b = joinGroup(gid, mid)
        if b:
            # 获取整型（标题，提示，初始值）
            result = tkinter.messagebox.showinfo(title='信息提示！',
                                                 message='内容：加入群组py: [' + gid + '] 成功 ! \n \n  重新启动软件生效 ! ')
            # 打印内容  ok
            # print(result)
            if result == 'ok':
                #  销毁窗口
                root.destroy()
        else:
            tkinter.messagebox.showerror(message='你已经在该群组里面啦~~~')
            return

    tkinter.Label(root, text='输入群组号 py:  ', font=('Arial', 12)).place(x=10, y=80)
    var_usr_gid = tkinter.StringVar()  # 定义变量
    tkinter.Entry(root, textvariable=var_usr_gid).place(x=130, y=80)

    # 添加按钮
    btn = tkinter.Button(root, text='加入该群组', command=jg).place(x=120, y=150)
    # btn.pack()

    # 加入消息循环
    root.mainloop()


#  退出群组
def egPanel(mid):
    # 创建主窗口
    root = tkinter.Tk()
    # 设置窗口大小
    # root.minsize(300, 300)

    # 窗口居中  =============  start  ====================
    # 窗口尺寸
    # window.geometry('1000x640')
    sw = root.winfo_screenwidth()
    # 得到屏幕宽度
    sh = root.winfo_screenheight()
    # 得到屏幕高度
    ww = 300
    wh = 300
    # 窗口宽高为100
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    root.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    # 窗口居中  =============  end  ====================

    gid = ''

    # 创建函数
    def eg():
        gid = (var_usr_gid.get()).strip()
        if gid == '':
            tkinter.messagebox.showerror(message='Error, 群组py号 不能为空, try again.')
            return

        #  数据库操作
        b = exitGroup(gid, mid)
        if b:
            # 获取整型（标题，提示，初始值）
            result = tkinter.messagebox.showinfo(title='信息提示！',
                                                 message='内容：退出群组py: [' + gid + '] 成功 ! \n \n  重新启动软件生效 ! ')
            # 打印内容  ok
            # print(result)
            if result == 'ok':
                #  销毁窗口
                root.destroy()
        else:
            tkinter.messagebox.showerror(message='你本来就不在这个群组里面好吗。。。')
            return

    tkinter.Label(root, text='输入群组号 py:  ', font=('Arial', 12)).place(x=10, y=80)
    var_usr_gid = tkinter.StringVar()  # 定义变量
    tkinter.Entry(root, textvariable=var_usr_gid).place(x=130, y=80)

    # 添加按钮
    btn = tkinter.Button(root, text='退出该群组', command=eg).place(x=120, y=150)
    # btn.pack()

    # 加入消息循环
    root.mainloop()