import cv2
import numpy as np
import pyautogui
import time


def deploy_airmouse():
    cap = cv2.VideoCapture(0)

    lower = np.array([22, 93, 0])
    upper = np.array([45, 255, 255])
    while True:
        t1 = time.time()
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        contours, hierarchy = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            area = cv2.contourArea(c)
            if area > 500:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                x_map = x*7.68
                y_map = y*2.16
                pyautogui.moveTo(x_map, y_map)
            if area > 10 and area < 500:
                pyautogui.click()
        frame = cv2.resize(frame, (500, 500))
        mask = cv2.resize(mask, (500, 500))
        t2 = time.time()
        fps = 1/(t2-t1)
        cv2.putText(frame, "FPS:{}".format(fps), (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=3)
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)
        print(fps)
        if cv2.waitKey(10) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    deploy_airmouse()
