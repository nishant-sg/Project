import cv2 
import numpy as np

#quadTurn = input('quadTurn:')
#triangleTurn = input('triangleTurn')
quadTurn = 'right'
triangleTurn = 'left'
#read video
vid = cv2.VideoCapture(0)
width  = int(vid.get(3))  # float width
height = int(vid.get(4))  # float height
#print(width,height)

def DrawShapesAndColours(countour,f):
    a=[]
    for cnt in countour:
        a.append(cv2.contourArea(cnt))
    
    i = a.index(max(a))
    colour = ''
    shape = ''
    area = cv2.contourArea(countour[i])
    cv2.drawContours(f,[countour[i]],-1,(213, 210, 75), 5)
    if area>2000:
        #cv2.drawContours(f,[countour[i]],-1, (213, 210, 75), 7)
        peri = cv2.arcLength(countour[i], True)
        approx = cv2.approxPolyDP(countour[i], 0.04 * peri, True)

        x,y,w,h = cv2.boundingRect(approx)
        cv2.rectangle(f,(x,y),(x+w,y+h),(0,0,0),2)
        #print(x+h/2,y+w/2)
        #print(len(approx))
        M = cv2.moments(countour[i])
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        color = f[cy,cx]

        if color[1]>=color[2] and color[1]>=color[0]:
            colour = 'green'
        elif color[2]>=color[1] and color[2]>=color[0]:
            colour = 'red'
        elif color[0]>=color[1]  and color[0]>=color[2]:
            colour = 'blue'

        if len(approx) == 3:
            shape = 'triangle'
            if triangleTurn == 'right':
                print('left wheel turns for 2 seconds')
            elif triangleTurn == 'left':
                print('right wheel turns for 2 seconds')
        elif len(approx) == 4:
            shape = 'quadilateral'
            if triangleTurn == 'right':
                print('left wheel turns for 2 seconds')
            elif triangleTurn == 'left':
                print('right wheel turns for 2 seconds')
        else:
            shape = 'circle'
            #print('both wheels turn')
  
        cv2.putText(f, colour, (x+h+5, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)  
        cv2.putText(f, shape, (x+h+5, y+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)  
        if cx<300:
            print('right')
        elif cx>340:
            print('left')
        else:
            print('forward')



    return colour,shape

while(True): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 

    imgc = frame
    imgc = cv2.GaussianBlur(imgc, (7, 7), 0)
    imgc = cv2.cvtColor(imgc , cv2.COLOR_BGR2GRAY)    
    imgc = cv2.Canny(imgc, 100, 40)

    kernel = np.ones((5,5))
    imgc = cv2.dilate(imgc,kernel,0)


    contours, hierarchy = cv2.findContours(imgc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    DrawShapesAndColours(contours,frame)
    #cv2.drawContours(frame,contours,-1, (213, 210, 75), 7)


    #Display the current frame 
    cv2.imshow('frame', frame)  

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
 
# Destroy all the windows 
cv2.destroyAllWindows()