import socket
import os
import hashlib
import sys
from sys import getsizeof

# Default IP and Port
IP_ADDRESS = '127.0.0.1'
PORT = 9000

# If an IP was entered, IP equals input
if len(sys.argv) > 1:
    IP_ADDRESS = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the IP address and port number
sock.bind((IP_ADDRESS, PORT))

print("Server Started")
while True:
    data, addr = sock.recvfrom(65507)
    request = data.decode('utf-8')
    if request[:3] != "GET": # If no "GET" in the first 3 indices of string return bad request
        response = "BAD REQUEST".encode('utf-8')
        sock.sendto(response, addr)
        continue
    command, file_name = request.split(' ')
    try:
        file_size = os.path.getsize(file_name)
        if file_size > 65507:
            sock.sendto(b'TOOLARGE', addr)  # If the file size is too large, send back an error message
            continue
        with open(file_name, 'rb') as f:
            file_data = f.read()
            md5 = hashlib.md5(file_data).hexdigest() # calculate the MD5 sum of the file
            response_header = f"FOUND {file_name}\r\nMD5 {md5}\r\nLENGTH {file_size}\r\n".encode('utf-8') # build the response header
            sock.sendto(response_header, addr) # send the header to the client first
            # send the file data in chunks of 1024 bytes
            for i in range(0, len(file_data), 1024):
                chunk = file_data[i:i+1024]
                sock.sendto(chunk, addr)
    except:
        sock.sendto(b'File not found', addr) # If the file doesn't exist, send back an error message
