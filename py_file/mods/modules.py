
import numpy as np
import cv2

class preprocessing:
    def __init__(self,img):
        self.img= img
    def blur(self,kernel_size,iterasi):
        return cv2.GaussianBlur(self.img,(kernel_size,kernel_size),iterasi)
        # return cv2.GaussianBlur(self.img,(kernel,kernel),iterasi)
    def show(self):
        return cv2.imshow("original",self.img)
    def dilate(self,kernel_size,iterasi):
        return cv2.dilate(self.img, kernel_size, iterations=iterasi)
        

def calc_foreground_percentage(img):
    pixel_black = cv2.countNonZero(img)

    print("Number of dark pixels:")
    print(pixel_black)

    h, w = img.shape
    luas_total = h*w
    percentage = pixel_black / luas_total
    print(f"Percentage of foreground:{percentage*100},value : {percentage}")
    # print(pixel_black / luas_total * 100)    
    
    return percentage


def thresholding(images):
    kernel_th = np.ones((3,3),np.uint8)
    
    img = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # inv_img = (255-thresh1)
    thresh1 = cv2.erode(thresh1, kernel_th, iterations=1)
    
    size = np.size(img)
    # img_thresh = cv2.imshow('Binary Threshold', thresh1)
    # img_inv = cv2.imshow('Binary invers', inv_img)

    #  0 = hitam 
    background = cv2.countNonZero(thresh1)
    foreground = size - background
    # pixel_black = cv2.countNonZero(thresh1)
    

    print(f"Number of foreground pixels: {foreground}, background pixels: {background}")


    # h, w = images.shape()
    # luas_total = x*y
    luas = foreground+background
    percentage = round((foreground / luas)*100,2)
    # percentage = round(percentage*100,2)
    print(f"Percentage of foreground in pixel:{percentage}%")
    return thresh1,percentage
    # return img_thresh,percentage

def lidar():
    pass

def pixel_cm(jarak):
    # harus di update lagi
    # 123.02010343130996, coef : [-6.2577418   0.09104895]
    persamaan = ((0.09104895*(np.power(jarak,2))) + (-6.2577418*jarak) + 123.02010343130996)
    # 188.21307559706932, coef : [-1.41647011e+01  4.36014392e-01 -4.70028620e-03]
    persamaan = ((-0.00470028620*(np.power(jarak,3)))+(0.436014392*(np.power(jarak,2))) + (-14.1647011*jarak) + 188.21307559706932)
    
    # print(persamaan)
    return persamaan
    
def detect(frame):
    # global x,y,w,h
    # x,y,w,h = 0,0,0,0
    cx,cy =0 , 0
    luas=0
    edge = cv2.Canny(frame,30,100,3)
    contours, hierarchy = cv2.findContours(edge,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        # 23 agstus
        rect = cv2.minAreaRect(c)
        (a,b),(l,p),angle=rect
        # box =cv2.boxPoints(rect)
        # box = np.int0(box)
        # cv2.circle(frame,int(a),int(b),5,(0,0,255),-1)
        # end
        x,y,w,h = cv2.boundingRect(c)
        # luas = (y-(y+h))*(x-(x+w))
        luas= w*h
   
        # cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        # temp.append(luas)
        # print(temp)
        # cv2.imshow('roi',roi)
    # cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        if(luas > 180):
            # print(f'koordinat : {x,y}, luasan : {w,h}, luas : {luas}' )
            M = cv2.moments(c)
            if M['m00'] != 0:
                # cx1= int(M['m01'])
                # cx2= int(M['m00'])
                # cx3= int(M['m10'])
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
          
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) 
                return cx,cy,luas,edge,x,y,w,h
                
            else:
                cx,cy =0 , 0
        else:
            cx,cy=0,0
      
    # print(f'X:{cx},Y:{cy}')
    # print(f'X:{cx1},Y:{cx2},{cx3}')
    
    luas,edge,x,y,w,h=0,0,0,0,0,0 # fungsinya supaya ketika tidak ada kontuk nilainya dikembalikan 0 semua
    return cx,cy,luas,edge,x,y,w,h
def nothing(x):
    pass
kernel = np.ones((5, 5), np.uint8)
