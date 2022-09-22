#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = "LOCALHOST"
PORT = 8001
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_s:
    
        #QUESTION 3
        proxy_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        proxy_s.bind((HOST, PORT))
        #set to listening mode
        proxy_s.listen(2)
        
        #continuously listen for connections from client
        while True:
            conn, addr = proxy_s.accept()
            print("Connected by", addr)
            
            #recieve data, wait a bit, then send it back
            full_data = conn.recv(BUFFER_SIZE)
            
            #This is the part where we send to google and get a response
                
            #This is where we send client stuff to google
            host = "www.google.com"
            port = 80
            payload = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'
            
            g_socket = create_tcp_socket()
            
            remote_ip = get_remote_ip(host)
        
            g_socket.connect((remote_ip , port))
            print (f'Socket Connected to {host} on ip {remote_ip}')
            
            #process stuff
            p = Process(target=handle_echo, args=(g_socket, payload, conn))
            p.daemon =  True
            p.start()
            print("Starting process ", p)


            conn.close()
            
            
def handle_echo(g_socket, payload, conn):
    new_full_data = b""
    buffer_size = 4096
    #send the data and shutdown
    send_data(g_socket, payload)
    g_socket.shutdown(socket.SHUT_WR)
    
    #continue accepting data until no more left
    
    while True:
        data = g_socket.recv(buffer_size)
        if not data:
            break
        new_full_data += data
    print(new_full_data)
    
    g_socket.close()
    
    #By this point we have all of the data back from google, and now need to send it back to the proxy client
    time.sleep(0.5)
    conn.sendall(new_full_data)
    
    
    
    
            
#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        # AF_INNET -> IPV4, SOCK_STREAM -> TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()
        
    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

if __name__ == "__main__":
    main()
    