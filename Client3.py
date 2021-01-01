import sys

import wx
import json
import _thread
import time
import socket

import tkinter as tk
from tkinter import messagebox

from mapper.userMapper import register


class ContentPanel(wx.SplitterWindow):

    # parent为父类实例
    def __init__(self, parent, logic, contact={"type": 11, "id": 0, "name": "未知"}):
        super(ContentPanel, self).__init__(parent, id=-1, style=wx.SP_LIVE_UPDATE | wx.SP_BORDER | wx.SP_3DSASH)
        self.logicClient = logic
        self.contact = contact

        upper = wx.Panel(self)
        lower = wx.Panel(self)

        self.SplitHorizontally(upper, lower, -200)
        self.SetMinimumPaneSize(120)

        self.contact_name = wx.StaticText(upper, -1, label=self.contact["name"])
        font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.contact_name.SetFont(font)

        self.content_text = wx.TextCtrl(upper, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.BORDER_NONE)
        self.input_text = wx.TextCtrl(lower, style=wx.TE_MULTILINE | wx.BORDER_NONE)
        self.input_text.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        ctrl_panel = wx.Panel(lower)
        send_button = wx.Button(ctrl_panel, label='发送')
        send_button.Bind(wx.EVT_BUTTON, self.OnClick_sendButton)

        # boxSizer
        upperbox = wx.BoxSizer(wx.VERTICAL)
        upper.SetSizer(upperbox)
        upperbox.Add(self.contact_name, proportion=0, flag=wx.EXPAND | wx.RIGHT | wx.TOP, border=15)
        upperbox.Add(self.content_text, proportion=1, flag=wx.EXPAND | wx.RIGHT | wx.TOP, border=15)

        lowerbox = wx.BoxSizer(wx.VERTICAL)
        lower.SetSizer(lowerbox)
        lowerbox.Add(self.input_text, proportion=1, flag=wx.EXPAND | wx.RIGHT | wx.BOTTOM, border=15)
        lowerbox.Add(ctrl_panel, proportion=0, flag=wx.EXPAND | wx.RIGHT, border=20)

    # 设置联系人，相当于重新布置面板    
    def setContact(self, contact={"type": 11, "id": 0, "name": "未知"}):
        self.contact = contact
        self.contact_name.SetLabel(contact["name"] + "（" + str(contact['id']) + "）")

    # 显示消息
    def showMessage(self, title, text, type=0):
        if type == 1:
            titleColor = wx.Colour(0, 0, 255)
        elif type == 2:
            titleColor = wx.Colour(0, 0, 255)
        else:
            titleColor = wx.Colour(0, 128, 64)

        titleFont = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)
        textFont = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)

        self.content_text.SetDefaultStyle(wx.TextAttr(titleColor, wx.NullColour, titleFont))
        self.content_text.AppendText(title + '\n')

        self.content_text.SetDefaultStyle(wx.TextAttr(wx.BLACK, wx.NullColour, textFont))
        self.content_text.AppendText(text + '\n')

        self.content_text.SetDefaultStyle(
            wx.TextAttr(wx.BLACK, wx.NullColour, wx.Font(3, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)))
        self.content_text.AppendText('\n')

    # 发送按钮
    def OnClick_sendButton(self, event):
        text = self.input_text.GetValue()
        text = text.strip('\n')
        if text and self.contact['id'] > 0:  # 0为系统，控制能不能给系统发送消息
            theTime = time.strftime("%H:%M:%S", time.localtime())  # 时间 %Y-%m-%d %H:%M:%S
            if self.logicClient.sendMsg(self.contact['type'], text, self.contact['id'], {"time": theTime}):
                # 将消息显示到窗口
                title = "我 " + theTime
                message = " " + text
                self.showMessage(title, message)
                self.input_text.Clear()
            else:
                self.showMessage("系统消息：发送数据失败！", "")


## -------------- sp --------------------- ##


class ClientUI(wx.Frame):
    contacts = []  # 联系人
    contentPanels = []  # 所有面板
    last_selection = 0
    usr_name = 0

    def __init__(self, logic):
        super().__init__(parent=None, title="py聊天", size=(1000, 640))

        self.Center()
        self.logicClient = logic

        swindow = wx.SplitterWindow(parent=self, id=-1, style=wx.SP_LIVE_UPDATE)

        left = wx.Panel(parent=swindow)
        self.right = wx.Panel(parent=swindow)
        # 设置左右布局的分割窗口left和right
        swindow.SplitVertically(left, self.right, 100)
        swindow.SetMinimumPaneSize(260)

        # 创建布局管理器
        leftbox = wx.BoxSizer(wx.VERTICAL)
        left.SetSizer(leftbox)

        # 为right面板设置一个布局管理器
        self.rightbox = wx.BoxSizer(wx.VERTICAL)
        self.right.SetSizer((self.rightbox))

        # left 联系人面板
        contact_tab = wx.StaticText(left, -1, label=" 联系人列表:", style=wx.ST_ELLIPSIZE_END)
        contact_tab.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        leftbox.Add(contact_tab, 0, flag=wx.TOP | wx.LEFT, border=15)
        self.contact_list = wx.ListBox(left, style=wx.LB_SINGLE | wx.LB_OWNERDRAW | wx.BORDER_NONE)
        self.contact_list.SetFont(
            wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, faceName="微软雅黑"))
        self.contact_list.SetBackgroundColour("#FAFAFA")
        leftbox.Add(self.contact_list, 1, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.BOTTOM, border=15)

        self.init()


    def loginpanel(self):
        window = tk.Tk()
        window.title('lankerens多人聊天室')
        # 窗口尺寸
        window.geometry('1090x400')

        # 创建登录框架
        frame1 = tk.Frame(window, width=1024, height=800)

        #  ---------------------------exam-start--------------------
        #  ---------------------------------------------------------
        frame2 = tk.Frame(window, width=1024, height=700)
        frame_top = tk.Frame(frame2, width=1024, height=500)
        frame_top.propagate(0)
        frame_bottom = tk.Frame(frame2, width=1024, height=200)
        frame_bottom.propagate(0)

        # welcome image  >> frame1
        canvas = tk.Canvas(frame1, width=500, height=400)  # 创建画布
        image_file = tk.PhotoImage(file='static/welcome.png')  # 加载图片文件
        canvas.create_image(0, 0, anchor='nw', image=image_file)  # 将图片置于画布上
        canvas.pack(side='top')  # 放置画布（为上端）

        # user information
        tk.Label(frame1, text='py号: ', font=('Arial', 12)).place(x=100, y=150)  # 创建一个`label`名为`User name: `置于坐标（50,150）

        var_usr_name = tk.StringVar()  # 定义变量
        entry_usr_name = tk.Entry(frame1,
                                  textvariable=var_usr_name)  # 创建一个`entry`，显示为变量`var_usr_name`即图中的`example@python.com`
        entry_usr_name.place(x=160, y=150)

        is_login = False


        # frame2
        canvas2 = tk.Canvas(frame2, width=500, height=400)  # 创建画布
        canvas2.create_image(0, 0, anchor='nw', image=image_file)  # 将图片置于画布上
        canvas2.pack(side='top')  # 放置画布（为上端）
        tk.Label(frame2, text='输入py号: ', font=('Arial', 12)).place(x=50, y=150)
        tk.Label(frame2, text='输入昵称: ', font=('Arial', 12)).place(x=50, y=150 + 50)
        var_usr_pynum = tk.StringVar()  # 定义变量
        entry_usr_pynum = tk.Entry(frame2,
                                  textvariable=var_usr_pynum)
        entry_usr_pynum.place(x=160, y=150)
        var_usr_pynickname = tk.StringVar()  # 定义变量
        entry_usr_pynickname = tk.Entry(frame2,
                                  textvariable=var_usr_pynickname)
        entry_usr_pynickname.place(x=160, y=150 + 50)


        def usr_login():
            # global is_login
            global usr_name
            usr_name = (var_usr_name.get()).strip()

            if usr_name == '':
                tk.messagebox.showerror(message='Error, py号不能为空, try again.')
                return

            window.destroy()

            # for item in users:
            #     if item['num'] == usr_name and item['name'] == usr_pwd:
            #         # print('登录成功')
            #         is_login = True
            #
            #         ok = tk.messagebox.showinfo(title='Welcome', message='欢迎你:   ' + item['num'] + item['name'])
            #         if ok == 'ok':
            #             frame1.pack_forget()  # 用于pack布局
            #             frame2.pack()
            #
            # if (not is_login):
            #     tk.messagebox.showinfo(title='sorry', message='py错误? ')
            #     var_usr_name.set('')

        # 注册
        def usr_register():
            frame1.pack_forget()  # 用于pack布局
            frame2.pack()

        # 注册成功与否
        def usr_register_sql():
            pynum = (entry_usr_pynum.get()).strip()
            pynickename = (entry_usr_pynickname.get()).strip()
            if pynum == '' or pynickename == '':
                tk.messagebox.showerror(message='Error, py号 | 昵称 不能为空, try again.')
                return

            b = register(pynum, pynickename)
            if b:
                tk.messagebox.showinfo(title='Welcome', message='注册成功 ')
                frame2.pack_forget()  # 用于pack布局
                frame1.pack()

            else :
                tk.messagebox.showinfo(title='sorry', message='id或昵称已存在 ')

        def usr_register_return():
            frame2.pack_forget()  # 用于pack布局
            frame1.pack()


        # 登录按钮
        btn_login = tk.Button(frame1, text=' 登  录  ', font=('Arial', 12),
                              command=usr_login)  # 定义一个`button`按钮，名为`Login`,触发命令为`usr_login`

        btn_register = tk.Button(frame1, text=' 注  册  ', font=('Arial', 12),
                                 command=usr_register)  # 定义一个`button`按钮，名为`Login`,触发命令为`usr_login`

        usr_register_sql = tk.Button(frame2, text=' 注  册  ', font=('Arial', 12),
                                 command=usr_register_sql)

        usr_register_return = tk.Button(frame2, text=' 返  回  ', font=('Arial', 12),
                                     command=usr_register_return)


        btn_login.place(x=120, y=230)
        btn_register.place(x=170 + 100, y=230)
        usr_register_sql.place(x=120, y=150 + 100)
        usr_register_return.place(x=170 + 100, y=150 + 100)

        frame1.pack()

        # 显示出来
        window.mainloop()


    def init(self):
        self.contact_list.Bind(wx.EVT_LISTBOX, self.On_listSelect)

        for i in range(20):
            pp = ContentPanel(self.right, self.logicClient)
            self.contentPanels.append(pp)
            self.rightbox.Add(pp, proportion=1, flag=wx.EXPAND | wx.BOTTOM, border=15)
            pp.Hide()

        self.refreshUserList([{"type": 11, "id": 0, "name": "系统"}])
        self.contentPanels[0].Show()

        try:
            # 登录
            self.loginpanel()
            # dlg = wx.TextEntryDialog(self, "请输入您的PY号", "登录", style=wx.OK | wx.CANCEL)
            # if dlg.ShowModal() == wx.ID_OK:
            self.logicClient.setMe(int(usr_name))
        except:
           sys.exit()



    # 联系人切换监听
    def On_listSelect(self, event):
        selection = event.GetEventObject().GetSelection()
        if self.last_selection >= 0:
            self.contentPanels[self.last_selection].Hide()
        self.contact_list.SetItemBackgroundColour(selection, "#FAFAFA")
        self.contentPanels[selection].Show()
        self.contact_list.Refresh()
        self.right.Layout()

        self.last_selection = selection



    # 刷新联系人列表 datas:[{"id":3,"type":11or13,"name":"cyt"}]
    def refreshUserList(self, datas=[]):
        for i in range(len(self.contacts) - 1, -1, -1):
            if self.contacts[i]['id'] == 0:
                continue
            isfind = False
            for nu in datas:
                if self.contacts[i]['id'] == nu['id']:
                    isfind = True
                    # 名字不对改名字
                    if self.contacts[i]['name'] != nu['name']:
                        self.contacts[i]['name'] = nu['name']
                        self.contentPanels[i].setContact(nu)
                    datas.remove(nu)
                    break
            if not isfind:
                self.contacts.pop(i)
                # self.rightbox.Remove(i) #Detach移除不破坏，remove移除破坏
                # self.rightbox.Layout()
                po = self.contentPanels.pop(i)
                self.contentPanels.append(po)

        for su in datas:
            self.contacts.append(su)
            self.contentPanels[len(self.contacts) - 1].setContact(su)

        # 联系人列表显示    
        if self.contact_list.Items and len(self.contact_list.Items):
            self.contact_list.Clear()
        for i, sub in enumerate(self.contacts):
            if sub['type'] == 11:
                content = " " + sub['name'] + "（py：" + str(sub['id']) + "）"
            else:
                content = " 群：" + sub['name'] + "（PY：" + str(sub['id']) + "）"
            self.contact_list.Append(content)
            self.contact_list.SetItemBackgroundColour(i, "#FAFAFA")
        self.contact_list.Refresh()



    # 传递消息 type=0 新消息，type=1 同步的消息
    def addMessage(self, to, title, text, type=0):
        # 暂时添加到0中
        for index, us in enumerate(self.contacts):
            if us['id'] == to:
                if not self.last_selection == index and type != 0:
                    self.contact_list.SetItemBackgroundColour(index, "#F0A670")
                    self.contact_list.Refresh()
                self.contentPanels[index].showMessage(title, text, type)
                return True
        return False


## -------------- sp --------------------- ##


class Client():
    title = 'lankerens多人聊天室'
    serverIP = '127.0.0.1'
    serverPort = 1367
    hostIP = '127.0.0.1'
    hostPort = 3970
    status = 0  # 1为在线 # 0为离线

    me = -1  # 自己的id
    myName = ""
    contacts = []

    def setMe(self, id):
        self.me = id
        pass

    # sendMsg(self,type,data,to,extra = {})函数 成功返回True，失败返回False
    def sendMsg(self, type, data, to, extra={}):
        if not data:
            return False
        try:
            self.sendSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sendSock.connect((self.serverIP, self.serverPort))
            # 格式化数据并发送
            msg = {"type": type, "from": self.me, "to": to, "data": data}
            json_string = json.dumps(dict(msg, **extra))
            self.sendSock.send(bytes(json_string, encoding="utf8"))
            self.sendSock.close()
            return True
        except:
            self.sendSock.close()
            return False
        return False

    # 接收sock并处理
    def receive(self, sock, addr):
        while True:
            try:
                data = sock.recv(1024).decode(encoding="utf8")
                if not data:
                    break
                msg = json.loads(data)

                if msg['type'] == 2:  # 登录消息(返回)
                    break

                elif msg['type'] == 4:  # 请求信息(返回)
                    if msg['code'] == "contacts":
                        # 获取联系人列表并除去自己
                        self.contacts = msg['data']
                        for u in self.contacts:
                            if u['id'] == self.me:
                                self.myName = u['name']
                                self.contacts.remove(u)
                                break
                        clientUI.SetTitle(self.title + " - 已登录（" + self.myName + "）")
                        self.ui.refreshUserList(self.contacts)

                elif msg['type'] == 12 or msg['type'] == 14:  # 接收消息
                    data = msg['data']
                    for ms in data:
                        title = ms['fromName'] + " " + ms['time']
                        message = " " + ms['msg']
                        self.ui.addMessage(ms["from"], title, message, 1)  # 1代表同步的消息
            except:
                self.ui.addMessage(0, "系统消息：接受数据失败！", "")
        sock.close()

    # 接受消息线程
    def receiveThread(self):
        try:
            self.receiveSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.receiveSock.bind((self.hostIP, self.hostPort))
            self.receiveSock.listen(5)  # 允许最大连接数为5
            self.buffersize = 1024

            while True:
                sock, addr = self.receiveSock.accept()
                t = _thread.start_new_thread(self.receive, (sock, addr))

        except:
            self.ui.addMessage(0, "系统消息：", "接受线程错误，请重启程序！")
        finally:
            self.receiveSock.close()

    # 同步消息
    def syncServer(self):
        while True:
            if self.status == 0:
                if self.sendMsg(1, "login", 0, {"ip": self.hostIP, "port": self.hostPort}):
                    self.status = 1
                    clientUI.SetTitle(self.title + " - 连接成功")
                else:
                    clientUI.SetTitle(self.title + " - 连接失败")
            elif self.status > 0:
                if not self.sendMsg(1, "hello", 0, {"ip": self.hostIP, "port": self.hostPort}):
                    self.status = 0
                    clientUI.SetTitle(self.title + " - 已离线（" + self.myName + "）")
            time.sleep(5)
        self.ui.addMessage(0, "系统消息：同步线程（syncServer）异常退出！", "")

    def startRun(self, ui):
        self.ui = ui
        _thread.start_new_thread(self.syncServer, ())  # 同步状态线程
        _thread.start_new_thread(self.receiveThread, ())  # 接受消息线程


if __name__ == '__main__':
    app = wx.App(False)
    client = Client()
    clientUI = ClientUI(client)
    clientUI.Show(True)
    client.startRun(clientUI)
    app.MainLoop()

# code=1 客户端向服务端发送登录，问候信息
# code=2 
# code=3 客户端查询用户信息（例请求联系人列表code="contacts"）
# code=4 服务端返回结果(返回联系人列表code="contacts")
# code=5 客户端向服务端发送更改信息（ip，port等）
# code=11,13 客户端向服务端发送消息（单发，群发）
# code=12 服务端向客户端发送消息
