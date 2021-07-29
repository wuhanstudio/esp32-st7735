import socket

# Image Processing
from PIL import Image
import argparse
import numpy as np

def send_img(ip, port, img):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (ip, port)
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)

    try:
        # Send data
        print('sending img', img.shape)

        # Magic number
        head = [0xAA, 0x55]
        sock.sendall(bytearray(head))

        # Height Width
        size = [img.shape[1], img.shape[0]]
        sock.sendall(bytearray(size))

        sock.sendall(img.tobytes())
    finally:
        print('closing socket')
        sock.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='ESP32 ST7735 Client')
    parser.add_argument('--ip', help='ESP32 IP Address', type=str, required=True)
    parser.add_argument('--port', help='ESP32 Port', type=str, required=True)
    args = parser.parse_args()

    image = Image.open('minions.jpg')
    send_img(args.ip, int(args.port), np.array(image).astype(np.uint8))
