#for command line arguments
import argparse

import socket
from socket import *
from threading import *

#gui
import tkinter as tk
from tkinter import *

#for image
from PIL import ImageTk,Image
from tkinter import PhotoImage

parser = argparse.ArgumentParser()
#getting hostname
hostName = gethostname()

#data type of ip address
parser.add_argument("--hosting", metavar="hosting",type =str,nargs="?", default=gethostname())
parser.add_argument("--port",metavar="port", type=int, nargs="?", default=8080)
parser.add_argument("--clientName",metavar="clientName",type=str, default="Client")

#arguments as a object containing all arguments
arguments = parser.parse_args()

print("Connecting to server.....")
      
print("Client Name:")
print(f"{arguments.clientName}")
print("host:",hostName)


sock = socket(AF_INET, SOCK_STREAM)

#SOL_SOCKET - (for send and recieve message by some protocols)
#SO_REUSEADDR - Make sure that client IPAddress and port not changed by system
sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

try:
    #connecting to server
    sock.connect((arguments.hosting, arguments.port))
    
    #creating Gui environment 
    app = Tk()
    app.geometry("350x420")
    
    #messageIcon is a object
    messageIcon = PhotoImage(file = "message.png")
    app.iconphoto(False, messageIcon)
    
    #for naming title bar
    app.title(arguments.clientName)
    
    #upper message box
    messageBox = Text(app,width=40)
    messageBox.grid(row=0)
    
    #input from user message box
    message = Entry(app,width=40)
    message.insert(0,"Enter Message:")
    message.grid(row=1)
    
    
#formating the literals
except Exception as ex:
        print(f"Failed to connect to host:{arguments.hosting} on port:{arguments.port} because of {ex}")
        raise SystemExit()

"""
functions
"""
#sending the message
def Send_Messages():
    #sending the message in text box with get() function
    #string variable clientmessage
    client_Messages = message.get()
    messageBox.insert(END,"\n"+"You: "+ client_Messages)
    
    #encoding message in binary form
    sock.send(client_Messages.encode())
    print("message send-all or one client: 0/1")
    
    #integer variable
    choice = int(input("Enter your choice:"))
    sock.send(client_Messages.encode())
    
    if(choice == 0):
        sock.send(client_Messages.encode())
    else:
        portNo = input("Enter client portNo:")
        sock.send(client_Messages.encode())
        sock.send(portNo.encode())
    

#displaying image on button
#image is object
image = tk.PhotoImage(file=r"send.png")
imageIcon = image.subsample(5,5)
sendBtn = Button(app,image=imageIcon,width=20,command=Send_Messages)
sendBtn.grid(row=1,column=1)

#recieve the message
def Recieve_Message():
    while True:
        servers_Message = sock.recv(8080).decode()
        print("Server Message:",servers_Message)
        messageBox.insert(END, "\n"+servers_Message)
           
            
#creating threads and call constructor for recieve message       
thd = Thread(target=Recieve_Message)
thd.daemon=True
thd.start()
          
#gui 
#Gui ready to Run Running Infinite loop   
app.mainloop()