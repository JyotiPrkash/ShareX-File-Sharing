from __future__ import with_statement
from Tkinter import *
import socket
import threading
import os


root = Tk()

topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

def exi():
	exit()

def startSending():
	print ("Server")
	def RetrFile(name, sock):
	    filename = sock.recv(1024)
	    if os.path.isfile(filename):
	        sock.send("EXISTS " + str(os.path.getsize(filename)))
	        userResponse = sock.recv(1024)
	        if userResponse[:2] == 'OK':
	            with open(filename, 'rb') as f:
	                bytesToSend = f.read(1024)
	                sock.send(bytesToSend)
	                while bytesToSend != "":
	                    bytesToSend = f.read(1024)
	                    sock.send(bytesToSend)
	    else:
	        sock.send("ERR ")
	
	    sock.close()
	
	def Main():
	    host = '127.0.0.1'
	    port = 5000
	
	
	    s = socket.socket()
	    s.bind((host,port))
	
	    s.listen(5)
	
	    print "Server Started."
	    while True:
	        c, addr = s.accept()
	        print "client connedted ip:<" + str(addr) + ">"
	        t = threading.Thread(target=RetrFile, args=("RetrThread", c))
	        t.start()
	         
	    s.close()
	
	if __name__ == '__main__':
	    Main()
	
		
###

def startReciving():
	print ("Client")
	import socket
	
	def Main():
	    host = '127.0.0.1'
	    port = 5000

	    s = socket.socket()
	    s.connect((host, port))
	
	    filename = raw_input("Filename? -> ")
	    if filename != 'q':
	        s.send(filename)
	        data = s.recv(1024)
	        if data[:6] == 'EXISTS':
	            filesize = long(data[6:])
	            message = raw_input("File exists, " + str(filesize) +"Bytes, download? (Y/N)? -> ")
	            if message == 'Y':
	                s.send("OK")
	                f = open('new_'+filename, 'wb')
	                data = s.recv(1024)
	                totalRecv = len(data)
	                f.write(data)
	                while totalRecv < filesize:
	                    data = s.recv(1024)
			    print "Downloading...`"
	                    totalRecv += len(data)
	                    f.write(data)
	                   # print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
	                print "Download Complete!"
	                f.close()
	        else:
	            print "File Does Not Exist!"
	
	    s.close()
	    
	
	if __name__ == '__main__':
	    Main()
###
root.title('File Sharing Application')
root.geometry('300x300')

l = Label(topFrame, text="File Sharing Application")
b1 = Button(topFrame, text="Send", command=startSending)
b2 = Button(topFrame, text="Recive", command=startReciving)
b3 = Button(bottomFrame, text="Exit", command=exi)

l.pack()
b1.pack(side=LEFT)
b2.pack(side=LEFT)
b3.pack(side=BOTTOM)

root.mainloop()
