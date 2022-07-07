import os
import re
import datetime
import threading
import requests
import tkinter
from tkinter import Tk, ttk, messagebox
# from bs4 import BeautifulSoup
from geometry import Geometry
from wmo import get_description

# 情報ありがとうにゃん
url = 'https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s&timezone=Asia/Tokyo&hourly=temperature_2m,dewpoint_2m,precipitation,relativehumidity_2m,weathercode'

# これを調整するにゃ
address = ''
latitude = '35.669'
longitude = '139.65'

maxrow = 24

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
root.geometry('+100+100')
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text='時刻').grid(column=0, row=0)
ttk.Label(frm, text='気温').grid(column=1, row=0)
ttk.Label(frm, text='湿度').grid(column=2, row=0)
ttk.Label(frm, text='降水量').grid(column=3, row=0)
ttk.Label(frm, text='天気').grid(column=4, row=0)

# メニューバー
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
# メニュー
menu_settings = tkinter.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='設定', menu=menu_settings)

label_list = []

def get_data_and_display():
    response = requests.get( url % (latitude, longitude))
    status_code = response.status_code
    if status_code != 200:
        messagebox.showerror('失敗しました', str(status_code))
        return
    result = response.json()['hourly']
    temperature = result['temperature_2m']
    precipitation = result['precipitation']
    humidity = result['relativehumidity_2m']
    weather = result['weathercode']
    #dewpoint = result['dewpoint_2m'][:6]
    time = result['time']
    hour = [re.search(r'^.+T(\d\d):\d\d$', t).group(1) for t in time]
    _now = ('0' + str(datetime.datetime.now().hour))[-2:]
    start = hour.index(_now)

    for lbl in label_list:
        lbl.destroy()

    label_list.clear()

    for n in range(maxrow):
        lbl = ttk.Label(frm, text='{:>2}時'.format(hour[start+n]))
        label_list.append(lbl)
        lbl.grid(column=0, row=n+1, sticky=tkinter.W)
        lbl = ttk.Label(frm, text='{:>2}℃'.format(temperature[start+n]))
        label_list.append(lbl)
        lbl.grid(column=1, row=n+1, sticky=tkinter.W)
        lbl = ttk.Label(frm, text='{:>3}%'.format(int(humidity[start+n])))
        label_list.append(lbl)
        lbl.grid(column=2, row=n+1, sticky=tkinter.W)
        lbl = ttk.Label(frm, text='{:>3}mm'.format(precipitation[start+n]))
        label_list.append(lbl)
        lbl.grid(column=3, row=n+1, sticky=tkinter.W)
        lbl = ttk.Label(frm, text='{}'.format(get_description(weather[start+n])))
        label_list.append(lbl)
        lbl.grid(column=4, row=n+1, sticky=tkinter.W)


# 座標決定窓の表示にゃ！
def show_geometry():
    global latitude, longitude
    latlon = {'latitude': latitude, 'longitude': longitude}
    tw_geometry = Geometry(root, latlon)
    #tw_geometry.deiconify()
    tw_geometry.grab_set()
    tw_geometry.focus_set()
    tw_geometry.transient(root)
    root.wait_window(tw_geometry)
    root.grab_set()
    root.focus_set()
    latitude = latlon['latitude']
    longitude = latlon['longitude']
    get_data_and_display()


# 設定メニューのエントリー
menu_settings.add_command(label='座標の設定',
        command=show_geometry)
menu_settings.add('command', label='表示')

def scheduler():
    t = threading.Timer(10*60, scheduler)
    t.start()
    get_data_and_display()


thread = threading.Thread(target=scheduler)
thread.start()

root.mainloop()
