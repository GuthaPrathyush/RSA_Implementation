import socket
import RSA



def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 5000))
    print("Server started")
    e, d, n = RSA.get_private_and_public_key()
    client_e, client_n = None, None
    while True:
        if client_e is None:
            key, addr = server_socket.recvfrom(1024)
            client_e, client_n = map(int, key.decode().split(' '))
            server_socket.sendto(f'{e} {n}'.encode(), addr)
            continue
        message, addr = server_socket.recvfrom(1024)
        message = message.decode()
        flag = message[-1]
        message = int(message[:-1])
        decrypted = RSA.decrypt(d, n, message)
        if flag == 'T':
            decrypted = chr(decrypted)
        print(f'Encrypted text: {message}')
        print(f'Client: {decrypted}')

        reply = input('Server: ')
        if reply.isdigit():
            reply = int(reply)
            flag = False
        else:
            reply = ord(reply[0]) if len(reply) > 0 else 0
            flag = True
        reply = RSA.encrypt(client_e, client_n, reply)
        server_socket.sendto((str(reply)+("T" if flag else "F")).encode(), addr)


start_server()
