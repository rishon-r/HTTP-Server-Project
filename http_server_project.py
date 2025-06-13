# WRITING A WEB SERVER
# WHAT IS A WEB SERVER
# A web server is a computer system that stores, processes and delivers web pages to users (also known as web clients)
# This communication usually happens via HTTP
# When you type a URL in the browser, a request goes out to the web server which then delivers the requested web pages

import socket
import threading

SERVER_PORT= 8080 # Port Numbers from 0 to 1023 are used by OS
SERVER_HOST = '127.0.0.1' # We are setting this to localhost


def start_http_server():
    # STEP 1: Create and initialize your socket
    # A socket is an endpoint in a network communication system
    # They allow data to be sent and received over the network and are one of the most important parts of a network
    # Here, they facilitate the connection between the client and server and allow the server to manage multiple clients at the same time
    # Without sockets, the communication needed for a web server to be implemented would not take place
    # Here, HTTP is the protocol used when data is sent or received over the sockets

    # Now, we initialize a socket of IPv4 family and TCP type
    # Note that HTTP is an application layer protocol built on top of TCP which is a transport layer protocol

    # TCP is the Transmission Control Protocol
    # TCP establishes a connection between the sender and receiver and ensures that the data, on arrival, is complete, in order and error free
    # This connection is established in a handshake process that takes place over 3 steps
    # First Step: SYN or synchronise- When the client wants to establish a connection with the server so it sends a single packet with the SYN (synchronize flag) set to the server
    # This packet consists of a sequence number (random number) initiates the sequence numbers for the packets that the client will send
    # Second Step: SYN-ACK or Synchronize Acknowledgement- Upon receiving the SYN packet, the server returns an SYN-ACK packet
    # This packet acknowledges the client's SYN packet and provides the server's sequence number for the data packets it will send to the client
    # Third Step: ACK or Acknowledgement - The client receives the server's SYN-ACK Packet and responds with the ACK packet.
    # This packet acknowledges the server's SYN-ACK packet
    # At this point, the handshake is complete and both the client and server have established a reliable communication
    # Data can now be sent between the client and server via the TCP protocol

    # IP stands for internet protocol. It is a set of rules that neeed to be followed when sending or receiving data over the internet
    # IPv4 is a type of IP address (IPv6 is the other newer type) and is used to identify a computer system in a network so that data is routed to the correct place
    # IPv4 is the most stable version of IP and also the most commonly used type

    # socket object initialized below
    server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.socket(family, type)
    # Here we have initialized a socket of IPv4 famly and TCP type

    # If we mentioned socket.SOCK_DGRAM as type instead of socket.SOCK_STREAM it would mean we want a socket of UDP type
    # UDP stands for User Datagram Protocol
    # TCP and UDP are both protocols used for transfer of data over a network
    # UDP is faster (fire and forget protocol) but does not send packets in order like TCP (TCP IS LINEAR)
    # TCP also provides error checking, retransmission of packets when they are corrupted and congestion control to reduce traffic load 
    # Hence, TCP is used more when data integrity matters and we can afford no loss of data. E.g Email and communcation over the internet
    # UDP does not initialize a connection with the handshake process, it sends packets without ensuring if the recipient is ready to receive packets
    # Key benefit is UDP is faster as it does not have to do checking, However, the tradeoff is that there is no guarantee of packets being received. 
    # This is used in Voice chat, Video chat, etc.

    # Now, we will configure some optional socket settings
    # setsockopt() is an optional method on the socket object
    # socket_object.setsockopt() allows you to configure socket options
    # socket options are configurations that control how the socket behaves at a system level
    # These options modify how a socket sends, receives or handles data
    # First argument it takes is level which is an integer. 
    # This means the protocol level for which configuration is happening.
    # For socket level options we provide socket.SOL_SOCKET
    # You can set options at multiple levels by simply using the setsockopt() function again but with a different level
    # Different options apply at different levels
    # Second argument it takes is the option name. This is the feature we wish to enable
    # Here, we use the socket.SO_REUSEADDR option which enables a socket to reuse a local IP Address + Port immediately after a connection is closed
    # Normally there is a delay before an endpoint can be reused so that any delayed packets are not mistakenly delivered to the wrong application
    # Third argument is the value. It is usually 1 or 0. 1 means on, 0 means off.
    # NOTE: All 3 arguments must be passed
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # The options currently configured with the socket object can be seen by using the socket.getsockopt()

    # NOTE: Sockets can be either in blocking mode or non blocking mode
    # When a socket is in blocking mode, the operation waits until it can proceed
    # If there's no data available, the program will wait until data arrives
    # E.g When there is no client connecting to the server socket, the socket waits until someone connects
    # When a socket is in non blocking mode, the operation does not wait
    # In non blocking mode, if an operation cannot proceed immediately, it raises an error (like BlockingIOError)
    # You can use the socket_obj.setblocking() method. It takes one argument called flag which is a boolean.
    # If flag is False, it is non blocking and vice versa
    server_socket.setblocking(True)
    # When blocking is set to False, it makes sense to use try and except blocks when accepting connections or receiving any kind of data
    # By default it is set to be in blocking mode

    # Now, we will bind our socket to our local machine so that the server knows where to listen for incoming requests from
    # Done using our IP Address and port
    # An IP address is used to identify a device in a network
    # A Port helps distinguish between multiple services running on the same device
    # It allows computers and servers to route incoming traffic to correct service or application
    # Web servers usually listen on port 80 for HTTP traffic and port 443 for HTTPS traffic
    # Ports allow computers to easiy distinguish between different kinds of traffic
    # E.g webpages go to a different port than emails



    # Binding the socket to this port and ip address
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    # Now, we want the socket to be able to listen to incoming connection requests. 
    # This is done using the listen() method of socket object
    # When this method is run, internally, the Operating System makes note that this particular socket is now ready to listen to incoming connections
    # It creates a queue for these conections, handling the initial three step handshake process
    # The maximum size of the queue for connections can be passed as an integer argument to the listen() method
    # If the maximum queue size is reached, new connection requests will either be refused or ignored based on the operating system
    server_socket.listen(5)

    print(f"Server listening on PORT: {SERVER_PORT} ...")

    # To get the front element of the queue (i.e the first client trying to make a connection), we use the socket_obj.accept() method
    # Returns a tuple consisting of the client's socket object as first element and address as second element
    # The client socket object serves only for communication with the new client object
    # This is not to be confused with the server socket object created above
    # The server_socket object will continue to listen for incoming connection requests
    # Since our socket has been set to blocking, we don't need to use try and except blocks here
    while True: # We use a while loop here so that the server is constantly trying to accept connections
        # Without the while loop the server only listens for one request 
        client_socket, client_address= server_socket.accept() # We have directly unpacked the tuple here
        # Once we receive the first client tuple from the queue, we start a thread for that particular client
        # The target for this thread is set to be the cliet_handler function which handles clients and parses requests
        thread = threading.Thread(target=client_handler, args=(client_socket, client_address)) 
        # The thread is set to be a daemon thread as it runs in the background and terminates whenever all the threads in the program terminate
        thread.daemon = True
        thread.start()

def client_handler(client_socket, client_address):

    # Now, we will receive HTTP requests from the client_socket
    # This is done using the recv() method of the socket object
    # The first argument it takes is the buffer size, which is essentially the maximum size of message being received
    # It is usually set to 1024 or 1500
    # The output of recv() method is a byte stream and cannot be understood directly, so we have to decode it using the decode() method of strings

    try:
        request= client_socket.recv(1500).decode() # This is the entire HTTP request
        print(f"Request from {client_address}:\n{request}")
        headers= request.split('\r\n\r\n')[0] # We get the request line and headers in this string
        request_line= (headers.split('\n'))[0] # The request line is the first line of the headers paragraph, we split it and get the first index
        request_method= request_line.split()[0] # Request method from request line is obtained here
        request_path= request_line.split()[1] # Path requested from request line is obtained here
        request_version= request_line.split()[2] # HTTP version from request line is obtained here

        request_body= request.split('\r\n\r\n')[1] # We get the body of the request here 
        
    
        if request_path=="/" and request_method=="GET":
            fh= open('index.html')
            content= fh.read()
            fh.close()

            response= 'HTTP/1.1 200 OK\n\n' + content
            
        elif request_path=="/" and request_method=="POST":
            content_length=0 
            for line in headers.split('\n'):
                if line.lower().startswith('content-length'): 
                        # The Content-Length header in an HTTP POST request tells the exact size (in bytes) of the request body. 
                        # This lets the server know how much data to read from the client after the headers.
                        content_length = int(line.split(':')[1].strip()) # Getting the value at content-length header key:value pair

            while len(request_body) < content_length: # Reading additional body
                request_body += client_socket.recv(1024).decode()

            response= f'HTTP/1.1 200 OK\nContent-Type: text/plain; charset=utf-8\n\nPOST data received:\n{request_body}' 
           

        else:
            response= 'HTTP/1.1 405 Method Not Allowed OK\n\nAllow: GET' 

        client_socket.sendall(response.encode())
    except Exception:
        print(f"Error handling request from {client_address}: {Exception}")
    finally:
        client_socket.close()

if __name__=='__main__':
    start_http_server()