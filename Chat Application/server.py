#for port and ipAddress
import socket

#for command line argument
import argparse

#threading for new client
import threading 

from socket import *
from threading import *

#for database
import sqlite3
import mysql.connector

#function for database
def Client_Database(client_socket, ipAddress):
    name_client=["client1", "client2", "client3", "client4", "client5"]
    
    #treated as string
    sql = "INSERT INTO clients(ClientName,IpAddress) VALUES (%s, %s)"
    
    val = (name_client[i],ipAddress[0])
    
    #To execute the query in database
    db_cursor.execute(sql, val)
    
    #to display the client records on database    
    data_Base.commit()
    

#Function for New clients
def NewClient(client_socket,conn):
    #IpAdress of client
    ip = conn[0]
    
    #client port Number
    port = conn[1]
    
    print(f"New connection successfully made on IpAddress:" )
    print(ip)  
    print(port)
    
    while True:
        #message recieve port of both client and server
        message = client_socket.recv(6013).decode()
        portNo = client_socket.recv(6013).decode()
        
        print("Message from client:",message)
        
        for Client in clients:
            if (Client is not client_socket):
                if Client == portNo:
                    Client.send((conn[0]+" and "+ str(conn[1])+" send: "+message).encode())
                else:
                    Client.send((conn[0]+" and "+ str(conn[1])+" send: "+message).encode())
        
        print(Client)
        print(client_socket)
        if message=="x":
            print(conn[0]+" and "+ str(conn[1])+" disconnect.....")
            break
        
    client_socket.close()


#main function code starts here
clients  = set()

parser = argparse.ArgumentParser()

#taking arguments from user
parser.add_argument("--hosting", metavar="hosting",type =str,nargs="?", default=gethostname())
parser.add_argument("--port",metavar="port", type=int, nargs="?", default=8080)
arguments = parser.parse_args()

print("Running the server on IPAddress:\nHost:")
print({arguments.hosting})
print({arguments.port})    

#connecting database
data_Base = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password= "abcd1234",
    database = "ServerClientDatabase",
    port = 3306
    )
print("Database has been connected!")

#create database
#cursor() instantly update the database
db_cursor = data_Base.cursor()

#create table and execute command in MySQL database
db_cursor.execute("CREATE TABLE clients(cid INT AUTO_INCREMENT PRIMARY KEY, ClientName VARCHAR(100),IpAddress VARCHAR(100))")

i=0

sock = socket(AF_INET,SOCK_STREAM)


#SOL_SOCKET - (for send and recieve message by some protocols)
#SO_REUSEADDR - Make sure that client IPAddress and port not changed by system
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
try:
    #bind the server on port so it can listen client
    #bind raise the exception
    sock.bind((arguments.hosting, arguments.port))
    sock.listen(5)
    
#handling binding exception    
except Exception as ex:
    print(f"Cannot bind host:{arguments.hosting} and port:{arguments.port} because of {ex}")
    raise SystemExit()
        
      
while True:
    try:
        print("Waiting for client.....")
        client_socket, ipAddress = sock.accept()
         
        clients.add(client_socket)
        
        #create client Database
        print("Adding client in Database.....")
        Client_Database(client_socket,ipAddress)
        i+=1
        
        #thread is created for every new client 
        #giving additional arguments
        thd = Thread(target=NewClient,args=(client_socket,ipAddress))
        thd.start()
        
            
    except KeyboardInterrupt:
        print("Keyboard Interrupt!")
    
    except Exception as ex:
        print("Exception error in thread ",ex)

  
#closing the socket
sock.close()