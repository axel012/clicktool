import win32api,win32gui,win32con,win32ui
import time
import os

#realiza un click en una ventana
def click(hwnd,x,y):
    lParam = win32api.MAKELONG(x, y)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam);
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam);

#class name de la ventana de los clientes de dofus, se puede obtener con spy++, yo use una herramienta que viene con autoitscript
dofusWindowClassName = "ApolloRuntimeContentWindow"
#hwnds -> dictionary, key = hwnd , value = [windowName,enabled]
def enumHandler(hwnd, hwnds):
    if win32gui.IsWindowVisible(hwnd):
        if dofusWindowClassName in win32gui.GetClassName(hwnd):
            if(hwnd in hwnds):
                value = hwnds[hwnd]
                enabled = value[1]
                hwnds[hwnd] = [win32gui.GetWindowText(hwnd),enabled]
            else:
                hwnds[hwnd] = [win32gui.GetWindowText(hwnd),True]
hwnds = {}

prevclickstate = -1
#HOTKEYS
VK_F1 = 0x70
VK_F2 = 0x71
VK_F3 = 0x72


desktopWidth = win32api.GetSystemMetrics(0)
desktopHeight = win32api.GetSystemMetrics(1)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def updatewindow():
    win32gui.EnumWindows(enumHandler, hwnds)
    cls()
    print("[F1] TOGGLE ACTIVE WINDOW SCRIPT")
    print("[F2] TOGGLE ALL WINDOWS")
    print("[F3] DISABLE ALL WINDOWS")
    print("------------------------------------------")
    for key in hwnds:
        print("Window: {0} | Enabled: {1}".format(hwnds[key][0].split("|")[0],hwnds[key][1]))
#descomentar si queres que te aparezca en la ventana el estado del script
#        text = win32gui.GetWindowText(key)
#        text = text.split("|")
#        win32gui.SetWindowText(key,"{0}|{1}".format(text[0],"Activado" if hwnds[key][1] == True else "Desactivado"))

def togglewindow():
    currentwindow = win32gui.GetForegroundWindow()
    for key in hwnds:
        if(key == currentwindow):
            hwnds[key][1] = not hwnds[key][1]
            break
    updatewindow()

def toggleall():
    for key in hwnds:
        hwnds[key][1] = not hwnds[key][1]
    updatewindow()


def disableall():
    for key in hwnds:
        hwnds[key][1] = False
    updatewindow()

updatewindow()
#main loop
while True:
    if(win32api.GetAsyncKeyState(win32con.VK_F1) != 0):
        while(win32api.GetAsyncKeyState(win32con.VK_F1) != 0):
            time.sleep(0.05)
        togglewindow()
    if(win32api.GetAsyncKeyState(win32con.VK_F2) != 0):
        while(win32api.GetAsyncKeyState(win32con.VK_F2) != 0):
            time.sleep(0.05)
        toggleall()
    if(win32api.GetAsyncKeyState(win32con.VK_F3) != 0):
        while(win32api.GetAsyncKeyState(win32con.VK_F3) != 0):
            time.sleep(0.05)
        disableall()

    lastclickstate = win32api.GetKeyState(0x01)
#Al hacer click, comprobamos si la ventana activa es una de nuestra lista de hwnds
#si lo es obtenemos la posicion del mouse y obtenemos los x,y relativos del click
    if(lastclickstate >= 0 and lastclickstate != prevclickstate):
        prevclickstate = lastclickstate
        currentwindow = win32gui.GetForegroundWindow()
        clickedClient = False
        for key in hwnds:
            if(key == currentwindow and hwnds[key][1]):
                _sx,_sy = win32api.GetCursorPos()
                _rx,_ry = win32gui.ScreenToClient(currentwindow,(_sx,_sy))
                clickedClient = True
                break
        if(clickedClient):
            for key in hwnds:
                if(currentwindow == key): 
                    continue
                keyval = hwnds[key]
                if(keyval[1]):
                    click(key,_rx,_ry)
#previene cpu high ussage
    time.sleep(0.1)

