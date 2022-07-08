import os
import re
import datetime
import threading
import requests
import tkinter
from tkinter import Tk, ttk, messagebox
from bs4 import BeautifulSoup
from geometry2 import Geometry
#from wmo import get_description

# 情報ありがとうにゃん
site = 'https://weathernews.jp'

# これを調整するにゃ
address = '皇居（東京都）'
latitude = '35.685316'
longitude = '139.747163'
uri = '/onebox/35.685316/139.747163/q=%E7%9A%87%E5%B1%85%EF%BC%88%E6%9D%B1%E4%BA%AC%E9%83%BD%EF%BC%89&v=33cf0c81d713854db71ea832bd6647dff38d61ce536ecedb323c6fb91c073de0'
fqdn = 'https://weathernews.jp'

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
label_address = ttk.Label(frm,text=address)
label_address.grid(column=0, row=0, columnspan=5)
ttk.Label(frm, text='時刻').grid(column=0, row=1)
ttk.Label(frm, text='天気').grid(column=1, row=1)
ttk.Label(frm, text='気温').grid(column=2, row=1)
ttk.Label(frm, text='降水').grid(column=3, row=1)
ttk.Label(frm, text='風速').grid(column=4, row=1)

# メニューバー
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
# メニュー
menu_settings = tkinter.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='設定', menu=menu_settings)

# 画面の初期作成
label_list = []
for i in range(maxrow):
    row = []
    for j in range(5):
        lbl = ttk.Label(frm, text='')
        lbl.grid(column=j, row=i+2, sticky=tkinter.W),
        row.append(lbl)
    label_list.append(row)

# 画像を探すにゃ
weather_icon = {}
def get_weather_icon(uri):
    name = re.search(r'^.+/(\d{3}.png)$', uri).group(1)
    if name in weather_icon:
        return weather_icon[name]
    try:
        icon = tkinter.PhotoImage(
            file='weather/'+name,
            #width=50,
            #height=37,
        ).subsample(5)
        weather_icon[name] = icon
    except:
        return name
    return icon

def get_data_and_display():
    response = requests.get(fqdn + uri)
    status_code = response.status_code
    if status_code != 200:
        messagebox.showerror('教えてくれなかったにゃ😥', str(status_code))
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    hour, rain, temp, wind, weather = [], [], [], [], []
    for row in soup.find_all(class_='wTable__row')[1:maxrow+1]:
        hour.append(row.find(class_='wTable__item time').text)
        rain.append(row.find(class_='wTable__item r').text)
        temp.append(row.find(class_='wTable__item t').text)
        wind.append(row.find(class_='wTable__item w').text)
        weather.append(row.find(class_='wTable__item weather')
            .find('img').attrs['src'])

    for n in range(maxrow):
        label_list[n][0].config(text='{:>2}時'.format(hour[n]))
        label_list[n][2].config(text='{:>2}'.format(temp[n]))
        label_list[n][3].config(text='{:>3}'.format(rain[n]))
        label_list[n][4].config(text='{:>3}'.format(wind[n]))
        icon = get_weather_icon(weather[n])
        if type(icon) == str:
            label_list[n][1].config(text=icon)
        else:
            label_list[n][1].config(image=icon)


# 座標決定窓の表示にゃ！
def show_geometry():
    global latitude, longitude, address, uri
    latlon = {'latitude': latitude, 'longitude': longitude, 'address': address, 'uri': uri}
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
    address = latlon['address']
    uri = latlon['uri']
    label_address.config(text=address)
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
