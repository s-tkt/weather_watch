import os
import threading
import requests
import tkinter
from tkinter import Tk, ttk
from bs4 import BeautifulSoup

# 情報ありがとうにゃん
url = 'https://weathernews.jp/onebox/%s/%s/temp=c' 

# これを調整するにゃ
latitude = 35.669
longitude = 139.65

root = Tk()

# 終了処理
# これをしないとプロセスが残ってしまうにゃぁぁぁ
def terminate():
    global root
    root.quit()
    root.destroy()
    # sys.exit() だとプロセスが残るにゃ？
    os._exit(0)


root.protocol("WM_DELETE_WINDOW", terminate)
root.title('天気予報')
frm = ttk.Frame(root, padding=10)
frm.grid()
# メニューバー
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
# 親メニュー
menu_settings = tkinter.Menu(root)
menu_bar.add_cascade(label='設定', menu=menu_settings)
# 子メニュー
menu_geometry = tkinter.Menu(root)
menu_settings.add_cascade(label='場所', menu=menu_geometry)
menu_display = tkinter.Menu(root)
menu_settings.add_cascade(label='表示', menu=menu_display)

def get_data_and_display():
    response = requests.get( url % (latitude, longitude))
    soup = BeautifulSoup(response.text, 'html.parser')
    size, time, rain, temp = 0, [], [], []
    for row in soup.find_all(class_='wTable__row')[1:13]:
        time.append(row.find(class_='wTable__item time').text)
        rain.append(row.find(class_='wTable__item r').text)
        temp.append(row.find(class_='wTable__item t').text)
        size += 1
    
    for n in range(size):
    	ttk.Label(frm, text='{:>2}時:{:>2}%:{:>2}'.format(time[n],rain[n],temp[n])).grid(column=0, row=n)

get_data_and_display()

def scheduler():
	t = threading.Timer(10*60, scheduler)
	t.start()
	get_data_and_display()


thread = threading.Thread(target=scheduler)
thread.start()

root.mainloop()
