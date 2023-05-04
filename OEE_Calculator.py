import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

def addTextandEntry(text, row, col):
    tk.Label(win, text=text, font=("Times", "10", "bold")).grid(row=row, column=col, pady=10)
    variable = tk.Entry(win, width=10, borderwidth=1)
    variable.grid(row=row, column=col+1)
    return variable

def separator(row, col, width):
    separate = tk.Frame(win, width=width)
    separate.grid(row=row, column=col)

def get_data():
    data = []
    Entries = [Tz, Tpp, Tpz, Taw, Tpn, Product, Shortages, TimeNProduct, N, Naw]
    for entry in Entries:
        data.append(entry.get())

    for element in range(0, len(data)):
        data[element] = int(data[element])

    tz, tpp, tpz, taw, tpn, product, shortages, timeNProduct, n, naw = [data[i] for i in range(0, len(data))]

    tz = 60*tz
    top = tz-tpp      #czas operacyjny Top
    rtop = tz-top     #rezerwa czasu operacyjnego
    per_top = round(top*100/tz, 2)    # procent top
    td = top-tpz-taw-tpn    #dostępność
    std = top-td          #strata dostępności
    per_td = round(td*100/top, 2)
    tw = (product*timeNProduct)/(60*n)    #wykorzystanie
    stw = td-tw
    per_tw = round(tw*100/td, 2)
    stj = tw*shortages/product
    tj = tw-stj
    per_tj = round(100*(1-(shortages/product)), 2)

    el = 5
    tmain = (tz, top, td, tw, tj)
    tadd = (0, rtop, std, stw, stj)
    ind = np.arange(el)
    width = 0.9

    fig = plt.Figure(figsize=(4, 4))
    ax = fig.add_subplot(111)
    ax.barh(ind, tmain, width, color='green', edgecolor='black', linewidth=1)
    ax.barh(ind, tadd, width, left=tmain, color='red', edgecolor='black', linewidth=1)
    ax.invert_yaxis()
    ax.axis("off")

    canvas = FigureCanvasTkAgg(fig, master=bottomFrame)
    canvas.draw()
    canvas.get_tk_widget().place(x=0, y=-10)

    time_zFrame = tk.Frame(master=bottomFrame, width=100, height=52, highlightbackground='black', highlightthickness=1)
    time_zFrame.place(x=400, y=52)
    time_zText = tk.Label(master=time_zFrame, text="Czas zamówiony", font=("Times", "8"))
    time_zText.place(x=0, y=0)
    time_zperText = tk.Label(master=time_zFrame, text="100%", font=("Times", "15", "bold"), fg="red")
    time_zperText.place(x=0, y=17)

    time_opFrame = tk.Frame(master=bottomFrame, width=100, height=52, highlightbackground='black', highlightthickness=1)
    time_opFrame.place(x=400, y=109)
    time_opText = tk.Label(master=time_opFrame, text="Czas operacyjny", font=("Times", "8"))
    time_opText.place(x=0, y=0)
    time_opperText = tk.Label(master=time_opFrame, text=f"{per_top}%", font=("Times", "15", "bold"), fg="red")
    time_opperText.place(x=0, y=17)

    DFrame = tk.Frame(master=bottomFrame, width=100, height=52, highlightbackground='black', highlightthickness=1)
    DFrame.place(x=400, y=166)
    DText = tk.Label(master=DFrame, text="Dostępność", font=("Times", "8"))
    DText.place(x=0, y=0)
    DperText = tk.Label(master=DFrame, text=f"{per_td}%", font=("Times", "15", "bold"), fg="red")
    DperText.place(x=0, y=17)

    WFrame = tk.Frame(master=bottomFrame, width=100, height=52, highlightbackground='black', highlightthickness=1)
    WFrame.place(x=400, y=223)
    WText = tk.Label(master=WFrame, text="Wykorzystanie", font=("Times", "8"))
    WText.place(x=0, y=0)
    WperText = tk.Label(master=WFrame, text=f"{per_tw}%", font=("Times", "15", "bold"), fg="red")
    WperText.place(x=0, y=17)

    JFrame = tk.Frame(master=bottomFrame, width=100, height=52, highlightbackground='black', highlightthickness=1)
    JFrame.place(x=400, y=280)
    JText = tk.Label(master=JFrame, text="Jakość", font=("Times", "8"))
    JText.place(x=0, y=0)
    JperText = tk.Label(master=JFrame, text=f"{per_tj}%", font=("Times", "15", "bold"), fg="red")
    JperText.place(x=0, y=17)

    factorFrame = tk.Frame(master=bottomFrame, width=270, height=280, highlightbackground='black', highlightthickness=1)
    factorFrame.place(x=520, y=52)

    OEE = tk.Label(master=factorFrame, text=f"OEE = {round(per_td*per_tw*per_tj/10000, 2)}%", font=("Times", "20", "bold"))
    OEE.place(x=0, y=0)

    td_teep = round(td*100/tz, 2)
    TEEP = tk.Label(master=factorFrame, text=f"TEEP = {round(td_teep * per_tw * per_tj / 10000, 2)}%",font=("Times", "20", "bold"))
    TEEP.place(x=0, y=35)

    timeInMinMTTR = datetime.timedelta(minutes=taw/naw)
    timeInFormatMTTR = (datetime.datetime.min + timeInMinMTTR).strftime('%H:%M:%S')
    MTTR = tk.Label(master=factorFrame, text=f"MTTR = {timeInFormatMTTR}", font=("Times", "20", "bold"))
    MTTR.place(x=0, y=70)

    days, remainder = divmod(int(tz*60/naw), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    timeToMTBF = '{:02d}:{:02d}:{:02d}:{:02d}'.format(days, hours, minutes, seconds)
    MTBF = tk.Label(master=factorFrame, text=f"MTBF = {timeToMTBF}", font=("Times", "20", "bold"))
    MTBF.place(x=0, y=105)

win = tk.Tk()
win.title("OEE Calculator")
win.geometry("850x600")

lineFrame = tk.Frame(master=win, width=1920, height=1, bg="#5f5f5f")
lineFrame.pack()
lineFrame.place(x=0, y=200)

bottomFrame = tk.Frame(master=win, width=1920, height=500, bg="white")
bottomFrame.place(x=0, y=201)

Tz = addTextandEntry("Czas zamówiony Tz[h]", 0, 0)
Tpp = addTextandEntry("Postoje planowane Tpp[min]", 1, 0)
Tpz = addTextandEntry("Czas przezbrajania Tpz[min]", 2, 0)
Taw = addTextandEntry("Awarie Taw[min]", 3, 0)
Naw = addTextandEntry("Ilość awarii", 3, 3)
Tpn = addTextandEntry("Postoje nieplanowane Tpn[min]", 4, 0)
separator(0, 2, 50)
Product = addTextandEntry("Ilość produktów [sztuki]", 0, 3)
separator(0, 5, 10)
Shortages = addTextandEntry("Braki [sztuki]", 0, 6)
TimeNProduct = addTextandEntry("Czas wykonania n przedmiotów [s]", 1, 3)
N = addTextandEntry("n [sztuki]", 1, 6)

calculate = tk.Button(win, text="Przelicz", padx=20, pady=10, bg="#48D1CC", command=get_data)
calculate.grid(row=3, column=8)

win.mainloop()
