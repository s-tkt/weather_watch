import os
import sys
import re
import datetime
import threading
import json
import requests
import tkinter as tk
from tkinter import Tk, ttk, messagebox
from bs4 import BeautifulSoup
from geometry import Geometry
#from wmo import get_description

# 情報ありがとうにゃん
site = 'https://weathernews.jp'

conf_path = 'config.json'
settings = {
    'default' : {
        'address' : '皇居（東京都）',
        'latitude' : '35.685316',
        'longitude' : '139.747163',
        'uri' : '/onebox/35.685316/139.747163/q=%E7%9A%87%E5%B1%85%EF%BC%88%E6%9D%B1%E4%BA%AC%E9%83%BD%EF%BC%89&v=33cf0c81d713854db71ea832bd6647dff38d61ce536ecedb323c6fb91c073de0',
        'root_x': 50,
        'root_y': 50,
        'maxrow' : 12,
    },
    'bookmark' : []
}
default = settings['default']
bookmark = []
weather_icon = {}

# 設定値の読み込みにゃ
def load_config():
    global default, bookmark
    try:
        with open(conf_path, 'r', encoding='utf-8') as cnf:
            settings = json.load(cnf)
            default = settings['default']
            bookmark = settings['bookmark']
    except FileNotFoundError as e:
        pass
    except Exception as e:
        messagebox.showerror('エラー', '設定の読み込みに失敗したにゃぁぁぁ', detail=str(e))

# ついでに書き込み関数にゃ
def save_config():
    settings = { 'default' : default, 'bookmark' : bookmark }
    try:
        with open(conf_path, 'w', encoding='utf-8') as cnf:
            json.dump(settings, cnf, indent=4)
    except Exception as e:
        messagebox.showerror('エラー', '設定の保存に失敗したにゃぁぁぁ', detail=str(e))

# 終了処理
# これをしないとプロセスが残ってしまうにゃぁぁぁ
def terminate():
    global root, timer, thread
    timer.cancel()
    thread.join()
    root.quit()
    root.destroy()
    sys.exit(0)



# 画像を探すにゃ
def get_weather_icon(uri):
    global weather_icon
    name = re.search(r'^.+/(\d{3}.png)$', uri).group(1)
    if name in weather_icon:
        return weather_icon[name]
    try:
        icon = tk.PhotoImage(
            file='wicon/'+name,
            #width=50,
            #height=37,
        ).subsample(6)
        weather_icon[name] = icon
    except:
        return name
    return icon

def get_data_and_display():
    try:
        response = requests.get(site + uri)
        status_code = response.status_code
        if status_code != 200:
            messagebox.showerror('教えてくれなかったにゃ😥', str(status_code))
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        hour, rain, temp, wind, weather = [], [], [], [], []
        time_weather = soup.find(class_='wTable time').find(class_='wTable__body')
        for row in time_weather.find_all(class_='wTable__row'):
            hour.append(row.find(class_='wTable__item time').text)
            rain_mm = row.find(class_='wTable__item r').text
            rain.append(re.search(r'^(\d+)', rain_mm).group(1))
            temp.append(row.find(class_='wTable__item t').text)
            wind.append(row.find(class_='wTable__item w').text)
            weather.append(row.find(class_='wTable__item weather')
                .find('img').attrs['src'])

        n_row = maxrow if maxrow <= len(hour) else len(hour)
        for n in range(n_row):
            label_list[n][0].config(text='{:>2}時'.format(hour[n]))
            label_list[n][2].config(text='{:>2}'.format(temp[n]))
            label_list[n][3].config(text='{:>3}mm'.format(rain[n]))
            label_list[n][4].config(text='{:>3}'.format(wind[n]))
            icon = get_weather_icon(weather[n])
            if type(icon) == str:
                label_list[n][1].config(text=icon)
            else:
                label_list[n][1].config(image=icon)
    except Exception as e:
        messagebox.showerror('何かエラーが起きたにゃ', str(e))
        terminate()


# 座標決定窓の表示にゃ！
def show_geometry():
    global latitude, longitude, address, uri
    latlon = {'latitude': latitude, 'longitude': longitude, 'address': address, 'uri': uri, 'cancel': False}
    tw_geometry = Geometry(root, latlon)
    #tw_geometry.deiconify()
    tw_geometry.grab_set()
    tw_geometry.focus_set()
    tw_geometry.transient(root)
    root.wait_window(tw_geometry)
    root.grab_set()
    root.focus_set()
    if latlon['cancel'] is False:
        latitude = latlon['latitude']
        longitude = latlon['longitude']
        address = latlon['address']
        uri = latlon['uri']
        label_address.config(text=address)
        get_data_and_display()


def set_position_as_default():
    default['root_x'] = root.winfo_x()
    default['root_y'] = root.winfo_y()
    save_config()

def set_address_as_default():
    default['address'] = address
    default['latitude'] = latitude
    default['longitude'] = longitude
    default['uri'] = uri
    save_config()

def scheduler():
    global timer
    timer = threading.Timer(10*60, scheduler)
    timer.start()
    get_data_and_display()



if __name__ == '__main__':
    load_config()
    address = default['address']
    latitude = default['latitude']
    longitude = default['longitude']
    uri = default['uri']
    root_x = default['root_x']
    root_y = default['root_y']
    maxrow = default['maxrow']
    # root窓の設定にゃ
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", terminate)
    root.title('天気予報')
    root.iconbitmap(default='icon.ico')
    #root.iconphoto(False, tk.PhotoImage(file='icon.png'))
    root.geometry('+%s+%s' % (root_x, root_y))
    # 中身をごりごり作るにゃ
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    label_address = ttk.Label(frm,text=address)
    label_address.grid(column=0, row=0, columnspan=5)
    ttk.Label(frm, text='時刻').grid(column=0, row=1)
    ttk.Label(frm, text='天気').grid(column=1, row=1)
    ttk.Label(frm, text='気温').grid(column=2, row=1)
    ttk.Label(frm, text='降水').grid(column=3, row=1)
    ttk.Label(frm, text='風速').grid(column=4, row=1)

    # 画面の初期作成
    label_list = []
    for i in range(maxrow):
        row = []
        for j in range(5):
            lbl = ttk.Label(frm, text='')
            lbl.grid(column=j, row=i+2, sticky=tk.W),
            row.append(lbl)
        label_list.append(row)

    # トップのメニューバー
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    # メニュー
    menu_bar.add_command(label='場所設定', command=show_geometry)
    menu_settings = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label='設定', menu=menu_settings)
    # 設定メニューのエントリー
    menu_settings.add('command', label='場所を記憶', command=set_address_as_default)
    menu_settings.add('command', label='窓位置を記憶', command=set_position_as_default)

    get_data_and_display()
    thread = threading.Thread(target=scheduler)
    thread.start()

    root.mainloop()
