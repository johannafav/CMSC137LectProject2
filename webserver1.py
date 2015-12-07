import socket

HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port %s ...' % PORT)
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    requestline = request.decode('utf-8')
    lines = requestline.split('\n')

    print(requestline)

    requestedFile = ''
    output = '<!DOCTYPE html><html><body><table border="1" style="width:100%">'

    for x in range(0, len(lines)):
        if len(lines[x]) > 0:
            output += '<tr>'
            temp = ''
            if x == 0:
                temp = lines[x].split(' ')
                if temp[0] == "GET":
                    requestedFile = temp[1].split('/')
                    requestedFile = requestedFile[1]
            else:
                temp = lines[x].split(': ')
            
            for y in range(0, len(temp)):
                output += '<td>' + temp[y] + '</td>'
            
            output += '</tr>'

    output += '</table></body></html>'
    
    #print(output)

    f = open('output.html', 'w')
    
    f.write(output)
    f.close()

    try:
        txt = open(requestedFile+'.html')
    except FileNotFoundError:
        requestedFile += '.html'
        f = open(requestedFile, 'w')
        f.write(output)
        f.close()
        txt = open(requestedFile)
        print(requestedFile)

    #http_response = """\
#HTTP/1.1 200 OK

#<h1><center>Hello, World!</center></h1>
#"""
    client_connection.sendall(bytes(txt.read(), 'utf-8'))
    client_connection.close()