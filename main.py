
import cv2
from cvzone.HandTrackingModule import HandDetector



class Button:
    def __init__(self,pos,width,hight,value):
        self.pos = pos
        self.width = width
        self.hight = hight
        self.value = value


    def draw(self,img):
        cv2.rectangle(img,self.pos,(self.pos[0]+self.width, self.pos[1]+self.hight),
                      (225,225,225),cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.hight),
                      (50, 50, 50),3)
        cv2.putText(img,self.value, (self.pos[0]+20,self.pos[1]+30),
                    cv2.FONT_HERSHEY_PLAIN,2,(50,50,50),2)


    def chickckik(self,x,y):
        if self.pos[0]<x<self.pos[0]+self.width and self.pos[1]<y<self.pos[1]+self.hight:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.hight),
                          (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.hight),
                          (50, 50, 50), 3)
            cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

            return True
        else:
            return False



cap = cv2.VideoCapture(0)



print(cap.get(3))
print(cap.isOpened())

#initilize the hand
detector = HandDetector(detectionCon=0.8,maxHands=1)

#creating Buttons
buttonsline = [['7','8','9','*'],
                ['4','5','6','-'],
                ['1','2','3','+'],
                ['0','/','.','=']]

myeq = '5+9'
delay = 0

buttonlist = []
for x in range(4):
    for y in range(4):
        xpos = x*50 + 400
        ypos = y*50 +100
        buttonlist.append(Button((xpos,ypos),50,50,buttonsline[y][x]))




while (cap.isOpened()):
    success, img = cap.read()
    img = cv2.flip(img, 1)
   # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # detection the hand and reteurn the points of hands
    hands, img = detector.findHands(img, flipType=False)

    #drawing buttons and result
    cv2.rectangle(img, (400,50), (400+200, 200),
                  (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (400,50), (400+200, 200),
                  (50, 50, 50), 3)
    for button in buttonlist:
        button.draw(img)



    #check for hand
    if hands:
        lmlist = hands[0]['lmList']
        print(lmlist[8])
        x1,y1,_ = lmlist[8]
        x2, y2, _ = lmlist[12]
        length, info , img = detector.findDistance( (x1,y1), (x2,y2), img)
        #x, y,_ = lmlist[8]
        if length<50:
            for i,butt in enumerate(buttonlist):
                if butt.chickckik(x1,y1) and delay == 0 :
                    myvalye = buttonsline[int(i%4)][int(i/4)]
                    if myvalye == "=":
                        myeq = str(eval(myeq))
                    elif myvalye == ".":
                        myeq = ''
                    else:
                        myeq += myvalye
                    delay = 1


    if delay !=0 :
        delay += 1
        if delay >10:
            delay = 0



    #display result
    cv2.putText(img, str(myeq), (410,80),
                cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)



    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()