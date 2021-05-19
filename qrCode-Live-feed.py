import cv2
import numpy as np
import webbrowser
import pyzbar.pyzbar as pyzbar

cam = cv2.VideoCapture(0)
found = False
while cam.isOpened():
    _, frame = cam.read()
    
    decoded = pyzbar.decode(frame)
    
    for data in decoded:
        pts = np.array([data.polygon], np.int32).reshape(-1, 1, 2)
        cv2.polylines(frame, [pts], True, (0, 255, 0), 4)
        #print(pts)
        px1 = (pts[0][0][0])
        px3 = (pts[2][0][0])
        test_size = (100/(px3-px1))   #100 is a constant and (px3-px1) is width of the qr code
        #print(size)
        if test_size<0.7:
            test_size = 0.7
        if test_size>1.5:
            test_size = 1.5
        cv2.putText(frame, data.data.decode(), (data.rect[0], data.rect[1]), cv2.FONT_HERSHEY_SIMPLEX, test_size, (0, 255, 0), 2)
        
        # uncomment if any web link is encoded in the qr code
        '''try:
            webbrowser.open(str(data.data.decode()), new=1)     
            cv2.destroyAllWindows()
            cam.release()
            
        except:
            pass'''
        
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
        
cv2.destroyAllWindows()
cam.release()
