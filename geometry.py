import tkinter as tk
from tkinter import Tk, ttk
import requests
import muni

class Geometry(tk.Toplevel):
    # ありがとうにゃ！
    url_rev_geo = 'https://mreversegeocoder.gsi.go.jp/reverse-geocoder/LonLatToAddress'
    url_geo = 'https://msearch.gsi.go.jp/address-search/AddressSearch'

    def __init__(self, root, latlon_dict):
        super().__init__()
        self.root = root
        self.latlon_dict = latlon_dict
        self.latitude = latlon_dict['latitude']
        self.longitude = latlon_dict['longitude']
        # root の位置を調べるにゃ
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        self.geometry('+%s+%s' % (int(root_x) + 50, int(root_y + 50)))
        self.title('座標の設定')
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.g_frm = ttk.Frame(self, padding=10)
        self.g_frm.grid(column=0, row=0,
            sticky=tk.E+tk.W+tk.N+tk.S)

        # 地名
        self.address_entry = tk.StringVar()
        self.g_entry_address = ttk.Entry(
            self.g_frm,
            textvariable = self.address_entry,
            exportselection = 0,
        )
        self.g_entry_address.grid(column=0, row=0, columnspan=2,
            sticky=tk.E+tk.W)
        self.g_entry_address.bind('<KeyPress-Return>', self.select_address_handler)
        ttk.Button(
            self.g_frm,
            text='地名から選択',
            command=self.select_address,
        ).grid(column=2, row=0, sticky=tk.E+tk.W)

        self.g_select_address = tk.Listbox(
            self.g_frm, selectmode=tk.SINGLE)
        self.g_select_address.grid(column=0, row=1, columnspan=3,
                sticky=tk.E+tk.W+tk.N+tk.S)
        self.g_select_address.bind('<<ListboxSelect>>', self.select_list_handler)

        # 緯度
        self.latitude_entry = tk.StringVar()
        self.latitude_entry.set(self.latitude)
        self.g_entry_latitude = ttk.Entry(
            self.g_frm,
            textvariable = self.latitude_entry,
            exportselection = 0,
        )
        self.g_entry_latitude.grid(column=0, row=2, sticky=tk.E+tk.W)
        # 経度
        self.longitude_entry = tk.StringVar()
        self.longitude_entry.set(self.longitude)
        self.g_entry_longitude = ttk.Entry(
            self.g_frm,
            textvariable = self.longitude_entry,
            exportselection = 0,
        )
        self.g_entry_longitude.grid(column=1, row=2, sticky=tk.E+tk.W)
        # 決定
        ttk.Button(
            self.g_frm,
            text='決定',
            command=self.close,
        ).grid(column=2, row=2, sticky=tk.E+tk.W)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.g_frm.columnconfigure(0, weight=0)
        self.g_frm.columnconfigure(1, weight=1)
        self.g_frm.columnconfigure(2, weight=0)
        self.g_frm.rowconfigure(0, weight=0)
        self.g_frm.rowconfigure(1, weight=1)
        self.g_frm.rowconfigure(2, weight=0)

    def close(self):
        self.latitude = self.latitude_entry.get()
        self.longitude = self.longitude_entry.get()
        self.latlon_dict['latitude'] = self.latitude
        self.latlon_dict['longitude'] = self.longitude
        self.destroy()

    def select_address(self):
        self.address_list = self.get_geometry(self.address_entry.get())
        a = [x[0]+':'+x[1] for x in self.address_list]
        self.g_select_address.delete(0, tk.END)
        self.g_select_address.insert(tk.END, *a)

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

    # 座標から場所
    def get_address(self, lat, lon):
        response = requests.get(self.url_rev_geo, paramas={'lat':lat,'lon':lon})
        result = response.json()['results']
        muniCd = result['muniCd']
        #muniCd = muniCd[1:] if muniCd[0] == '0' else muniCd
        address = muni.MUNI_DICT[muniCd].split(',')
        return adress[1], address[3], result['lv01Nm']

    # 場所から座標
    def get_geometry(self, address):
        def pickup(s):
            if s == '':
                return ''
            x = s.split(',')
            return x[1]+x[3]

        response = requests.get(self.url_geo, params={'q':address})
        results = [(
                pickup(muni.MUNI_DICT.get(x['properties']['addressCode'],'')),
                x['properties']['title'],
                (x['geometry']['coordinates'][1],
                    x['geometry']['coordinates'][0]))
                for x in response.json()]
        return results

