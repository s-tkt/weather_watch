import os
import threading
import requests
import tkinter
from tkinter import Tk, ttk
from bs4 import BeautifulSoup
import muni

# 情報ありがとうにゃん
url = 'https://weathernews.jp/onebox/%s/%s/temp=c' 
url_rev_geo = 'https://mreversegeocoder.gsi.go.jp/reverse-geocoder/LonLatToAddress'
url_geo = 'https://msearch.gsi.go.jp/address-search/AddressSearch'

# これを調整するにゃ
address = ''
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
# メニュー
menu_settings = tkinter.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='設定', menu=menu_settings)

# 座標から場所
def get_address(lat, lon):
    response = requests.get(url_rev_geo, paramas={'lat':lat,'lon':lon})
    result = response.json()['results']
    muniCd = result['muniCd']
    #muniCd = muniCd[1:] if muniCd[0] == '0' else muniCd
    address = muni.MUNI_DICT[muniCd].split(',')
    return adress[1], address[3], result['lv01Nm']

# 場所から座標
def get_geometry(address):
    def pickup(s):
        if s == '':
            return ''
        x = s.split(',')
        return x[1]+x[3]

    response = requests.get(url_geo, params={'q':address})
    results = [(
            pickup(muni.MUNI_DICT.get(x['properties']['addressCode'],'')),
            x['properties']['title'],
            x['geometry']['coordinates'])
            for x in response.json()]
    return results

class Geometry(tkinter.Toplevel):
    def __init__(self, root, latitude, longitude):
        super().__init__()
        self.root = root
        self.latitude = latitude
        self.longitude = longitude
        #self.transient(self.root)
        self.title('座標の設定')
        self.withdraw()
        self.g_frm = ttk.Frame(self, padding=10)
        self.g_frm.grid(column=0, row=0,
            sticky=tkinter.E+tkinter.W+tkinter.N+tkinter.S)

        # 地名
        self.address_entry = tkinter.StringVar()
        self.g_entry_address = ttk.Entry(
            self.g_frm,
            textvariable = self.address_entry,
            exportselection = 0,
        )
        self.g_entry_address.grid(column=0, row=0, columnspan=2,
            sticky=tkinter.E+tkinter.W)
        self.g_entry_address.bind('<KeyPress-Return>', self.select_address_handler)
        ttk.Button(
            self.g_frm,
            text='地名から選択',
            command=self.select_address,
        ).grid(column=2, row=0, sticky=tkinter.E+tkinter.W)

        self.g_select_address = tkinter.Listbox(
            self.g_frm, selectmode=tkinter.SINGLE)
        self.g_select_address.grid(column=0, row=1, columnspan=3,
                sticky=tkinter.E+tkinter.W+tkinter.N+tkinter.S)
        self.g_select_address.bind('<Button-1>', self.select_list_handler)

        # 緯度
        self.latitude_entry = tkinter.StringVar()
        self.latitude_entry.set(self.latitude)
        self.g_entry_latitude = ttk.Entry(
            self.g_frm,
            textvariable = self.latitude_entry,
            exportselection = 0,
        )
        self.g_entry_latitude.grid(column=0, row=2, sticky=tkinter.E+tkinter.W)
        # 経度
        self.longitude_entry = tkinter.StringVar()
        self.longitude_entry.set(self.longitude)
        self.g_entry_longitude = ttk.Entry(
            self.g_frm,
            textvariable = self.longitude_entry,
            exportselection = 0,
        )
        self.g_entry_longitude.grid(column=1, row=2, sticky=tkinter.E+tkinter.W)
        # 決定
        ttk.Button(
            self.g_frm,
            text='決定',
            command=self.decide,
        ).grid(column=2, row=2, sticky=tkinter.E+tkinter.W)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.g_frm.columnconfigure(0, weight=0)
        self.g_frm.columnconfigure(1, weight=1)
        self.g_frm.columnconfigure(2, weight=0)
        self.g_frm.rowconfigure(0, weight=0)
        self.g_frm.rowconfigure(1, weight=1)
        self.g_frm.rowconfigure(2, weight=0)

    def select_address(self):
        self.address_list = get_geometry(self.address_entry.get())
        a = [x[0]+':'+x[1] for x in self.address_list]
        self.g_select_address.delete(0, tkinter.END)
        self.g_select_address.insert(tkinter.END, *a)

    def select_address_handler(self, event):
        self.select_address()

    def select_list_handler(self, event):
        selected = self.g_select_address.curselection()
        if len(selected) == 0:
            return
        else:
            idx = selected[0]
        [self.latitude, self.longitude] = self.address_list[idx][2]
        self.latitude_entry.set(self.latitude)
        self.longitude_entry.set(self.longitude)

    def decide(self):
        self.latitude = self.latitude_entry.get()
        self.longitude = self.longitude_entry.get()

    def get():
        return self.latitude, self.longitude


# 座標設定窓の作成
tw_geometry = Geometry(root, latitude, longitude)

def show_geometry():
    tw_geometry.deiconify()
    tw_geometry.grab_set()
    tw_geometry.focus_set()
    tw_geometry.transient(root)


# メニューのエントリー
menu_settings.add_command(label='座標の設定', command=show_geometry)
menu_settings.add('command', label='表示')

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
