import cv2, socket
import handdetector1 as hd1
import handdetector2 as hd2

cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # 640
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 480
# w = width/640*1920
# h = height/480*1060
# width = cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# height = cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1060)

detector1 = hd1.handDetector1()
detector2 = hd2.handDetector2()


def main():
    target_ip = '127.0.0.1'
    target_port = 12345

    # UDP 소켓 생성
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        # img1 = copy.copy(img)
        # img2 = copy.copy(img)

        if not ret:
            continue
        lmLst1 = detector1.drawHands(img)
        # img1 = cv2.rectangle(img1, (int(width/2), 0), (int(width), int(height)),(0,255,0), -1)

        lmLst2 = detector2.drawHands(img)
        # img2 = cv2.rectangle(img2, (0, 0), (int(width/2), int(height)), (255, 255, 255), -1)

        # detector1.circle(img, lmLst1, draw=True)
        # detector2.circle(img, lmLst2, draw=True)
        cv2.imshow("img", img)

        if lmLst1 == None and lmLst2 == None:
            m = 'N,N,N,N'
        elif lmLst1 == None:
            m = 'N,' + 'N,' + str(lmLst2[0]) + ',' + str(lmLst2[1])
        elif lmLst2 == None:
            m = str(lmLst1[0]) + ',' + str(lmLst1[1]) + ',N' + ',N'
        else:
            m = str(lmLst1[0]) + ',' + str(lmLst1[1]) + ',' + str(lmLst2[0]) + ',' + str(lmLst2[1])
        print(m)

        sock.sendto(m.encode(), (target_ip, target_port))
        if cv2.waitKey(1) == ord('q'):
            break
        # 소켓 닫기
    sock.close()


if __name__ == '__main__':
    main()
