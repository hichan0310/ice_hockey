import socket

def main():
    listen_ip = '192.168.117.182'
    listen_port = 12345

    # UDP 소켓 생성 및 바인딩
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((listen_ip, listen_port))
    print("asdf")
    while True:
        # 데이터 수신
        data, addr = sock.recvfrom(1024)

        # 수신된 데이터를 문자열로 디코딩하여 출력
        print("수신된 메시지: ", data.decode())
        File = open("test.txt", "r")
        text = File.read().split(',')
        File.close()
        with open('test.txt', 'w') as File:
            newdata=data.decode().split(',')
            print(text)
            result=""
            for i in range(4):
                result+=(text[i] if newdata[i]=='N' else newdata[i])+','
            File.write(result)
        if data.decode() == "exit":
            break

    # 소켓 닫기
    sock.close()

if __name__ == '__main__':
    main()