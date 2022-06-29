import os
import threading
import requests
from tkinter import Tk, ttk
from bs4 import BeautifulSoup

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

def get_data_display():
    response = requests.get('https://weathernews.jp/onebox/%s/%s/temp=c' % (latitude, longitude))
    soup = BeautifulSoup(response.text, 'html.parser')
    i, time, rain, temp = 0, [], [], []
    for row in soup.find_all(class_='wTable__row')[1:13]:
        time.append(row.find(class_='wTable__item time').text)
        rain.append(row.find(class_='wTable__item r').text)
        temp.append(row.find(class_='wTable__item t').text)
        i += 1
    
    for n in range(i):
    	ttk.Label(frm, text='{:>2}時:{:>2}%:{:>2}'.format(time[n],rain[n],temp[n])).grid(column=0, row=n)

get_data_display()

def scheduler():
	t = threading.Timer(10*60, scheduler)
	t.start()
	get_data_display()


thread = threading.Thread(target = scheduler)
thread.start()

root.mainloop()
