# LAB 2 - toddtian@bu.edu bbulut@bu.edu hhijazi@bu.edu

import socket
import os
import sys
import hashlib

# Set the IP address and port number
IP_ADDRESS = '127.0.0.1'
PORT = 9000

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send requests for files
if len(sys.argv) > 1:
    file_name = sys.argv[1]
    if len(sys.argv) > 2:
        IP_ADDRESS = sys.argv[2]
    file_name_get = "GET " + file_name # bandage method in order to filter get on server side
    sock.sendto(file_name_get.encode('utf-8'), (IP_ADDRESS, PORT)) # send the filename to the server
    data, addr = sock.recvfrom(65507) # receive the file info from the server
    if data == b'File not found': # conditions based on server response
        print(f'File not found: {file_name}')
    elif data == b'BAD REQUEST':
        print('BAD REQUEST')
    elif data == b'TOOLARGE':
        print(f'TOOLARGE {file_name}')
    else:
        with open(file_name, 'wb') as f:
            # get the expected length of the file from the file info received from the server
            file_info = data.decode('utf-8').split('\r\n')
            print('\n'.join(file_info))
            expected_file_size = int(file_info[2].split(' ')[1])
            total_data_received = 0
            # receive the file data in chunks of 1024 bytes
            while total_data_received < expected_file_size:
                data, addr = sock.recvfrom(1024)
                if not data:
                    break
                f.write(data)
                total_data_received += len(data)
            print(f'Successfully downloaded {file_name}')
            exit(0)
else:
    while True:
        request = input("Enter request in the format 'GET filename': ")
        file_name = request.split(' ')
        sock.sendto(request.encode('utf-8'), (IP_ADDRESS, PORT)) # send the filename to the server
        data, addr = sock.recvfrom(65507) # receive the file info from the server
        if data == b'File not found':
            print(f'NOTFOUND {file_name[1]}')
        elif data == b'BAD REQUEST':
            print('BADREQUEST')
        elif data == b'TOOLARGE':
            print(f'TOOLARGE {file_name[1]}')
        else:
            # remove the "GET_" prefix from the filename
            file_name = file_name[1]
            # save the file in the current directory
            with open(file_name, 'wb') as f:
                file_info = data.decode('utf-8').split('\r\n')
                print('\n'.join(file_info))
                expected_file_size = int(file_info[2].split(' ')[1])
                total_data_received = 0
                # receive the file data in chunks of 1024 bytes
                while total_data_received < expected_file_size:
                    data, addr = sock.recvfrom(1024)
                    if not data:
                        break
                    f.write(data)
                    total_data_received += len(data)
                file_len = os.path.getsize(file_name)
                print(file_len)
                print(f'Successfully downloaded {file_name}')
