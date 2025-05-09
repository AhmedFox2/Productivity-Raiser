from customtkinter import *
from ttkbootstrap import Meter , Style
from ttkbootstrap .constants import *

#style = Style("cosmo")
root =CTk()

meter = Meter(root,bootstyle="primary",amounttotal=100,metersize=200,meterthickness=10,amountused=30,)
meter.pack()

root.mainloop()