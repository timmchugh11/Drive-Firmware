from tkinter import *
from tkinter.ttk import *
from subprocess import *
import subprocess, os, tkinter, threading


root = tkinter.Tk()
root.title("HDD Firmware Flasher")

drives = subprocess.getoutput("ls /dev/ | grep sd | sed 's/.*[0-9].*//; /^$/d; s/^/\/dev\//'")


def clear():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def quit():
    root.destroy()

def flash():
    for line in drives.split():
        drive = line
        model = subprocess.getoutput("sudo smartctl -i " + drive + "| grep -E 'Vendor|Product' | sed 's/.*  //' | tr '\n' ' '")
        print(model)
        if model == "SEAGATE DKS5D-J900SS ":
            threading.Thread(target=lambda drive=drive: one(drive)).start()
        elif model == "SEAGATE DKS5E-J900SS ":
            threading.Thread(target=lambda drive=drive: two(drive)).start()
        elif model == "NETAPP X477_SMEGX04TA07 ":
            threading.Thread(target=lambda drive=drive: three(drive)).start()
        elif model == "SEAGATE DKS5E-J300SS ":
            threading.Thread(target=lambda drive=drive: four(drive)).start()
        else:
            globals()['status%s' % drive].set("No File")

def one(drive):
    os.system("sudo sg_write_buffer -v -m 7 -b 4k -I /home/bob/SAS\ Firmware/5SS.LOD " + drive)
    model = subprocess.getoutput("sudo smartctl -i " + drive + "| grep -E 'Vendor|Product' | sed 's/.*  //' | tr '\n' ' '")
    if model == "SEAGATE ST9900805SS ":
        globals()['model%s' % drive].set(model)
        globals()['status%s' % drive].set("Done")
    else:
        globals()['status%s' % drive].set("Error")


def two(drive):
    os.system("sudo sg_write_buffer -v -m 7 -b 4k -I /home/bob/SAS\ Firmware/006.LOD " + drive)
    model = subprocess.getoutput("sudo smartctl -i " + drive + "| grep -E 'Vendor|Product' | sed 's/.*  //' | tr '\n' ' '")
    if model == "SEAGATE ST900MM0006 ":
        globals()['model%s' % drive].set(model)
        globals()['status%s' % drive].set("Done")
    else:
        globals()['status%s' % drive].set("Error")

def three(drive):
    os.system("sudo sg_write_buffer -v -m 2 -b 4k -I /home/bob/SAS\ Firmware/4tb.LOD " + drive)
    model = subprocess.getoutput("sudo smartctl -i " + drive + "| grep -E 'Vendor|Product' | sed 's/.*  //' | tr '\n' ' '")
    if model == "SEAGATE ST900MM0006 ":
        globals()['model%s' % drive].set(model)
        globals()['status%s' % drive].set("Done")
    else:
        globals()['status%s' % drive].set("Error")

def four(drive):
    os.system("sudo sg_write_buffer -v -m 7 -b 4k -I /home/bob/SAS\ Firmware/st300.LOD " + drive)
    model = subprocess.getoutput("sudo smartctl -i " + drive + "| grep -E 'Vendor|Product' | sed 's/.*  //' | tr '\n' ' '")
    if model == "SEAGATE ST300MM0006 ":
        globals()['model%s' % drive].set(model)
        globals()['status%s' % drive].set("Done")
    else:
        globals()['status%s' % drive].set("Error")

Label(root, text = "Model").grid(row=0,column=0, sticky=W, padx=5, pady=15)
Label(root, text = "Serial").grid(row=0,column=1, sticky=W, padx=5)
Label(root, text = "Block Size").grid(row=0,column=2, sticky=W, padx=5)
Label(root, text = "Status").grid(row=0,column=3, sticky=W, padx=5)


i = 1
for line in drives.split():
    drive = line
    globals()['serial%s' % i] = subprocess.getoutput("sudo smartctl -i " + drive + "| grep Seri | sed 's/.* //g'")
    globals()['model%s' % drive] = StringVar()
    globals()['model%s' % drive].set(subprocess.getoutput("sudo smartctl -i " + drive + "| grep -E 'Vendor|Product' | sed 's/.*  //' | tr '\n' ' '"))
    globals()['bs%s' % i] = subprocess.getoutput("sudo smartctl -i " + drive + " | grep block | sed 's/.*  //;  s/ .*//'")
    globals()['status%s' % drive] = StringVar()
    globals()['status%s' % drive].set("Idle")
    if globals()['serial%s' % i] == "":
        print("Skipping" + drive)
    else:
        print("Not Skipping" + drive)
        Label(root, textvariable = globals()['model%s' % drive]).grid(row=i,column=0, sticky=W, padx=5)
        Label(root, text = globals()['serial%s' % i]).grid(row=i,column=1, sticky=W, padx=5)
        Label(root, text = globals()['bs%s' % i]).grid(row=i,column=2, sticky=E, padx=5)
        Label(root, textvariable = globals()['status%s' % drive]).grid(row=i,column=3, sticky=W, padx=5)
        i += 1


menubar = Menu(root)
menubar.add_command(label="Refresh", command=clear)
menubar.add_command(label="Flash Firmware", command=flash)
menubar.add_command(label="Quit", command=quit)
root.config(menu=menubar)

root.mainloop()
