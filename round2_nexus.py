import cv2 
import numpy as np

#colourToBeFollowed =  input('colorToBeFollowed')
colourToBeFollowed = 'green'

#read video
vid = cv2.VideoCapture(0)
width  = int(vid.get(3))  # float width
height = int(vid.get(4))  # float height
#print(width,height)


def barcodeDetector(f,c,x,y,w,h):
    global colourToBeFollowed
    code=[0,0,0,0]
    l=[]
    for i in range(5,95):
        #print(x,w,i,x+int(w*0.01*i))
        c = f[y+int((h/2)),x+int(w*0.01*i)]
        if c[0]>120 and c[1]>120 and c[2]>120:
            #print('black')
            l.append('w')
        elif c[0]<120 and c[1]<120 and c[2]<120:
            #print('white')
            l.append('b')
    w=[]
    c=0
    for i in l:
        
        if i=='b':
            if c==0:
                pass
            else:
                if len(w)<4:
                    w.append(c)
                else:
                    pass
            c=0
        elif i == 'w':
            c+=1
    c=0  
    print(w,l.count('w'))
    if len(w)==3:
        print('added')
        w.append(l.count('w')-w[0]-w[1]-w[2])
    
    for i in range(len(w)):
        if int(w[i])<12:
            code[i] = '0'
        elif int(w[i])>12:
            code[i] = '1'
        else:
            break
    print(code)
    w=[]
    listToStr = ''.join([str(elem) for elem in code])
    print(int(listToStr,2))
    if int(listToStr,2)%3 == 0:
        colorToBeFollowed = 'green'
    elif (int(listToStr,2)%3)-1 == 0:
        print('hello')
        colorToBeFollowed = 'red'
    elif (int(listToStr,2)%3)-2 == 0:
        colorToBeFollowed = 'blue'
    print(colorToBeFollowed)
    cv2.putText(f, listToStr+'-'+str(int(listToStr,2)), (x+h+5, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    #print(l.count('w')-int(w[0])-int(w[1])-int(w[2]))
    #print(l)
    return colourToBeFollowed


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
        ctf = 'green'

        if color[1]>=color[2] and color[1]>=color[0]:
            colour = 'green'
        elif color[2]>=color[1] and color[2]>=color[0]:
            colour = 'red'
        elif color[0]>=color[1]  and color[0]>=color[2]:
            colour = 'blue'

        if len(approx) == 4:
            global colourToBeFollowed
            shape = 'quadilateral'
            ctf = barcodeDetector(f,approx,x,y,w,h)
            colourToBeFollowed = ctf
            print('move forward and turn right',ctf)
        else:
            shape = 'circle'
            if colour == ctf:
                if cx<300:
                    print('right')
                elif cx>340:
                    print('left')
                else:
                    print('forward')
            else:
                print('turn right for two seconds')
            #print('both wheels turn')
            
            
        #cv2.putText(f, colour, (x+h+5, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)  
        cv2.putText(f, shape, (x+h+5, y+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)  
        

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

    c,s = DrawShapesAndColours(contours,frame)
    #cv2.drawContours(frame,contours,-1, (213, 210, 75), 7)


    #Display the current frame 
    cv2.imshow('frame', frame)  
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
 
# Destroy all the windows 
cv2.destroyAllWindows()