import socket
import RSA




def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    e, d, n = RSA.get_private_and_public_key()
    server_e, server_n = None, None

    while True:
        if server_e is None:
            client_socket.sendto(f'{e} {n}'.encode(), ('localhost', 5000))
            key, addr = client_socket.recvfrom(1024)
            server_e, server_n = map(int, key.decode().split(' '))
            continue
        message = input('Client: ')
        if message.isdigit():
            message = int(message)
            flag = False
        else:
            message = ord(message[0]) if len(message) > 0 else 0
            flag = True

        message = RSA.encrypt(server_e, server_n, message)

        client_socket.sendto((str(message)+("T" if flag else "F")).encode(), ('localhost', 5000))

        reply, _ = client_socket.recvfrom(1024)
        reply = reply.decode()
        flag = reply[-1]
        reply = int(reply[:-1])
        decrypted = RSA.decrypt(d, n, reply)
        if flag == 'T':
            decrypted = chr(decrypted)
        print(f'Encrypted text: {reply}')
        print(f'Server: {decrypted}')


start_client()
