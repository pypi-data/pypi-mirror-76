# coding:utf-8

import sys
import time
import cv2
import serial
#import datetime
import numpy as np
from pyzbar import pyzbar


sys.path.append('./')
#from fhx711.voice import Voice



class ScannerImage:
    def __init__(self, barcode=False):
        #是否检测到二维码标示
        self.check = False
        #是否是条形码
        self.barcode = barcode

        #self.voiceTip = Voice()
        _cv = cv2.__version__
        _cv = _cv.split('.')
        if len(_cv)>0:
            self.cv = int(_cv[0])
        else:
            self.cv = 0


    def judge_pcscaling(self, contours,i,j):
        """
        comment:判断最外面的轮廓和子轮廓的比例

        args:
            contours:图片轮廓的坐标点集合
            i: 外层轮廓索引
            j: 字轮廓索引

        return：
            true：符合要求  false：不符合
        """
        ''''''
        area1 = cv2.contourArea(contours[i])
        area2 = cv2.contourArea(contours[j])
        if area2==0:
            return False
        ratio = area1 * 1.0 / area2
        if abs(ratio - 49.0 / 25):
            return True
        return False

    def judge_ccscaling(self, contours,i,j):
        '''判断子轮廓和子子轮廓的比例'''
        area1 = cv2.contourArea(contours[i])
        area2 = cv2.contourArea(contours[j])
        if area2==0:
            return False
        ratio = area1 * 1.0 / area2
        if abs(ratio - 25.0 / 9):
            return True
        return False

    def judge_contoursdistance(self, vec):
        '''判断这个轮廓和它的子轮廓以及子子轮廓的中心的间距是否足够小'''
        distance_1=np.sqrt((vec[0]-vec[2])**2+(vec[1]-vec[3])**2)
        distance_2=np.sqrt((vec[0]-vec[4])**2+(vec[1]-vec[5])**2)
        distance_3=np.sqrt((vec[2]-vec[4])**2+(vec[3]-vec[5])**2)
        if sum((distance_1,distance_2,distance_3))/3<3:
            return True
        return False

    def compute_center(self, contours,i):
        '''计算轮廓中心点'''
        M=cv2.moments(contours[i])
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        return cx,cy

    def juge_angle(self, rec):
        '''判断寻找是否有三个点可以围成等腰直角三角形'''
        if len(rec)<3:
            return -1,-1,-1
        
        for i in range(len(rec)):
            for j in range(i+1,len(rec)):
                for k in range(j+1,len(rec)):
                    distance_1 = np.sqrt((rec[i][0] - rec[j][0]) ** 2 + (rec[i][1] - rec[j][1]) ** 2)
                    distance_2 = np.sqrt((rec[i][0] - rec[k][0]) ** 2 + (rec[i][1] - rec[k][1]) ** 2)
                    distance_3 = np.sqrt((rec[j][0] - rec[k][0]) ** 2 + (rec[j][1] - rec[k][1]) ** 2)
                    if abs(distance_1-distance_2)<5:
                        if abs(np.sqrt(np.square(distance_1)+np.square(distance_2))-distance_3)<5:
                            return i,j,k
                    elif abs(distance_1-distance_3)<5:
                        if abs(np.sqrt(np.square(distance_1)+np.square(distance_3))-distance_2)<5:
                            return i,j,k
                    elif abs(distance_2-distance_3)<5:
                        if abs(np.sqrt(np.square(distance_2)+np.square(distance_3))-distance_1)<5:
                            return i,j,k
        return -1,-1,-1
    
    def juge_anglemore(self, rec):
        arr = []
        '''判断寻找是否有三个点可以围成等腰直角三角形'''
        if len(rec)<3:
            return arr
        
        for i in range(len(rec)):
            for j in range(i+1,len(rec)):
                for k in range(j+1,len(rec)):
                    distance_1 = np.sqrt((rec[i][0] - rec[j][0]) ** 2 + (rec[i][1] - rec[j][1]) ** 2)
                    distance_2 = np.sqrt((rec[i][0] - rec[k][0]) ** 2 + (rec[i][1] - rec[k][1]) ** 2)
                    distance_3 = np.sqrt((rec[j][0] - rec[k][0]) ** 2 + (rec[j][1] - rec[k][1]) ** 2)
                    #print('distance_1:', distance_1)
                    #print('distance_2:', distance_2)
                    #print('distance_3:', distance_3)
                    if abs(distance_1-distance_2)<15:
                        if abs(np.sqrt(np.square(distance_1)+np.square(distance_2))-distance_3)<25:
                            arr.append((i,j,k))
                    elif abs(distance_1-distance_3)<15:
                        if abs(np.sqrt(np.square(distance_1)+np.square(distance_3))-distance_2)<25:
                            arr.append((i,j,k))
                    elif abs(distance_2-distance_3)<15:
                        if abs(np.sqrt(np.square(distance_2)+np.square(distance_3))-distance_1)<25:
                            arr.append((i,j,k))
        return arr

    def find_boxs(self, image):
        '''找到符合要求的轮廓'''

        # 符合要求的所有二维码框
        boxs = []

        try:
            image = cv2.blur(image, (3, 3))  # 通过低通滤波平滑图像
                
            image = cv2.equalizeHist(image) # img.astype(np.uint8)
            _,gray=cv2.threshold(image,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)
                
            # opencv4以前的版本
            if self.cv<4:
                binary, contours, hierachy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            else:
                contours, hierachy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #print(hierachy.shape)

            if len(contours)==1:
                hierachy = hierachy[0]
            else:
                hierachy = np.squeeze(hierachy)
            
            rec=[]
            
            
            for i in range(len(hierachy)):
                child = hierachy[i][2]
                if child==-1:
                    continue
                
                child_child=hierachy[child][2]
                if child!=-1 and child_child!=-1:            
                    if self.judge_pcscaling(contours, i, child) and self.judge_ccscaling(contours,child,child_child):
                        cx1,cy1=self.compute_center(contours,i)
                        cx2,cy2=self.compute_center(contours,child)
                        cx3,cy3=self.compute_center(contours,child_child)
                        if self.judge_contoursdistance([cx1,cy1,cx2,cy2,cx3,cy3]):
                            rec.append([cx1,cy1,cx2,cy2,cx3,cy3,i,child,child_child])
                    
            #print('rec shape:', np.shape(rec))
            '''计算得到所有在比例上所有符合要求的轮廓中心点'''        
            indexArr=self.juge_anglemore(rec)
            
            for i,j,k in indexArr:
                if i==-1 or j== -1 or k==-1:
                    continue

                ts = np.concatenate((contours[rec[i][6]], contours[rec[j][6]], contours[rec[k][6]]))
                rect = cv2.minAreaRect(ts)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                
                boxs.append(box)
                """
                result=copy.deepcopy(image)
                cv2.drawContours(result, [box], 0, (0, 0, 255), 2)
                cv2.drawContours(image,contours,rec[i][6],(255,0,0),2)
                cv2.drawContours(image,contours,rec[j][6],(255,0,0),2)
                cv2.drawContours(image,contours,rec[k][6],(255,0,0),2)
                cv2.imshow('img',image)
                cv2.waitKey(0)
                

                height,width=image.shape[:2]
                min = np.min(box, axis=0)
                max = np.max(box, axis=0)

                min=min[:]-50
                max=max[:]+50
                                
                minArr=np.zeros(min.shape,dtype=np.int16)
                #maxArr=np.full(max.shape,width,dtype=np.int16)

                min=np.maximum(min[:],minArr[:])
                max[0]=np.minimum(max[0],width)
                max[1]=np.minimum(max[1],height)

                roi = result[min[1] :max[1], min[0] :max[0] ]
                cv2.imshow('img',roi)
                
                cv2.waitKey(0)
                """

            #print('boxs shape:', np.shape(boxs))

            # 如果有回子轮廓但没有box
            if len(boxs)<1 and len(rec)>0:
                for i in range(len(rec)):
                    _contour = contours[rec[i][6]]

                    # maxArr=np.full(_contour.shape,100,dtype=np.int16)
                    _contour1 = np.copy(_contour)
                    _contour2 = np.copy(_contour)
                    _contour3 = np.copy(_contour)

                    _contour1[:,:,0] = _contour[:,:,0] - 100
                    _contour1[:,:,1] = _contour[:,:,1] - 100

                    _contour2[:,:,0] = _contour[:,:,0] + 100
                    _contour2[:,:,1] = _contour[:,:,1] - 100

                    _contour3[:,:,0] = _contour[:,:,0] + 100
                    _contour3[:,:,1] = _contour[:,:,1] + 100

                    ts = np.concatenate((_contour1, _contour2, _contour3))
                    rect = cv2.minAreaRect(ts)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    
                    boxs.append(box)
                
            self.check = True
            
            return boxs
        except Exception as e:
            #print(e)
            self.check=False
            return boxs

    def find_closedboxs(self, frame, barcode=False):
        """
        if not frame:
            self.check = False            
            return None
        """
        # 符合要求的所有二维码框
        boxs = []

        try:
            #图像边缘细节处理
            #使用scharr操作(指定ksize=-1)构造灰度图在水平和竖直方向上的梯度幅值表示
            frameX = cv2.Sobel(frame, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)  # 对x方向求导
            frameY = cv2.Sobel(frame, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)   # 对y方向求导
    
            # Scharr操作后，从X梯度减去Y梯度得到轮廓图，此时噪点较多
            gradient = cv2.subtract(frameX, frameY)


            # 经过处理后，用convertScaleAbs()函数将其转回原来的uint8形式。否则将无法显示图像，而只是一副灰色的窗口
            gradient = cv2.convertScaleAbs(gradient)
   
            # 然后对梯度图采用用9x9的核进行平均模糊,进行于降噪
            blurred = cv2.blur(gradient, (9, 9))  # 通过低通滤波平滑图像

            # 然后进行二值化处理，要么是255(白)要么是0(黑)
            ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY)  # 进行图像固定阈值二值化

            #cv2.imshow('thresh',thresh)
            #cv2.waitKey(0)

            # 通过形态学操作，建立一个7*21的长方形内核，内核宽度大于长度，因此可以消除条形码中垂直条之间的缝隙
            # 将建立的内核应用到二值图中，以此来消除竖杠间的缝隙
            if barcode:
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))  # 条形码
            else:
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))   #二维码
      
            # 对图像进行闭运算
            closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            # 所得图像仍有许多白点，通过腐蚀和膨胀去除白点,最后一个参数是腐蚀的次数
            closed = cv2.erode(closed, None, iterations=4)          # 腐蚀操作            
            closed = cv2.dilate(closed, None, iterations=6)         # 膨胀操作
            
            #cv2.imshow('closed',closed)
            #cv2.waitKey(0)
            # 寻找轮廓
            # opencv4以前的版本
            if self.cv<4:
                binary, contours, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            else:
                contours, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # opencv4版本的方法
            #contours, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # print('contours len:',len(contours))
            # 如果没有找到，返回空9
            if len(contours) == 0:
                self.check = False
                return boxs
            
            c = sorted(contours, key=cv2.contourArea, reverse=True)[0]
            
            rect = cv2.minAreaRect(c)  # 生成最小外接矩形            
            # box为一个ndarry数组，返回4个顶点位置
            box = np.int0(cv2.boxPoints(rect))
            
            boxs.append(box)

            self.check = True
            return boxs
        except Exception as e:
            #print(e)
            self.check=False
            return boxs

    def find_closedandconboxs(self, frame,barcode=False):
        
        # 符合要求的所有二维码框
        boxs = []

        try:
            boxs= self.find_closedboxs(frame, barcode)
            
            if len(boxs)<1:
                return boxs

            
            cimage = self.image_interceptbox(frame, boxs[0])            

            bx = self.find_boxs(cimage)

            if bx and len(bx)>0:
                    
                #boxs = np.vstack((boxs, bx))
                for bb in bx:
                    boxs.append(bb)
            
            
            self.check = True
            return boxs
        except Exception as e:
            print(e)
            self.check=False
            return boxs

    def find_closedorconboxs(self, frame, barcode=False):
        
        box1 = self.find_closedboxs(frame)

        box2 = self.find_boxs(frame)

        if not box1 or len(box1)<1:
            return box2

        if not box2 or len(box2)<1:
            return box1

        for b in box1:
            box2.append(b)

        return box2

    def Rotate_Bound(self, image, angle):
        # grab the dimensions of the image and then determine the
        # center
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)

        # grab the rotation matrix (applying the negative of the    
        # angle to rotate clockwise), then grab the sine and cosine    
        # (i.e., the rotation components of the matrix)   
        M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)    
        cos = np.abs(M[0, 0])    
        sin = np.abs(M[0, 1])     

        # compute the new bounding dimensions of the image    
        nW = int((h * sin) + (w * cos))    
        nH = int((h * cos) + (w * sin))   

        # adjust the rotation matrix to take into account translation    
        M[0, 2] += (nW / 2) - cX    
        M[1, 2] += (nH / 2) - cY     

        # perform the actual rotation and return the image    
        shuchu=cv2.warpAffine(image, M, (nW, nH))    
        
        return shuchu

    def image_interceptbox(self, frame, box, padding=50):
        
        height,width=frame.shape[:2]
        
        padding = int(padding)
        min = np.min(box, axis=0)
        max = np.max(box, axis=0)
        
        print(np.shape(min))
        
        min=min[:] - padding
        max=max[:] + padding
                
        minArr=np.zeros(min.shape,dtype=np.int16)
            
        min=np.maximum(min[:],minArr[:])
        max[0]=np.minimum(max[0],width)
        max[1]=np.minimum(max[1],height)

        return frame[min[1] :max[1], min[0] :max[0] ]

    def image_scanner(self, frame, boxs):
        
        if not boxs or len(boxs)<1:
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                            
                barcodeData = barcode.data.decode("utf-8")
                            
                if len(barcodeData)>0:
                    #i=0
                    #print(barcodeData[0])
                    arr = barcodeData.split('/')
                    index = len(arr)-1
                    return arr[index]

            return None

        for box in boxs:    

            roi = self.image_interceptbox(frame, box)
            #cv2.imshow('img2',roi)
            """
            result = frame.copy()
            cv2.drawContours(result, [box], 0, (0, 0, 255), 2)

            cv2.imshow('img2',result)
            cv2.waitKey(0)
            """

            barcodes = pyzbar.decode(roi)

            """
            # 旋转
            if len(barcodes)<1:
                _arr = [5, -5, 10, -10, 15, -15, 20, -20, 25, -25]
                #_arr = [3, -3, 6, -6, 9, -9, 12, -12, 15, -15, 18, -18, 21, -21, 24, -24, 27, -27]
                for r in _arr:
                    _img = self.Rotate_Bound(roi, r)
                    barcodes = pyzbar.decode(_img)

                    if len(barcodes)>0:
                        break
            """
            #print('barcodes :', len(barcodes))
            for barcode in barcodes:
                            
                barcodeData = barcode.data.decode("utf-8")
                            
                if len(barcodeData)>0:
                    #i=0
                    #print(barcodeData[0])
                    arr = barcodeData.split('/')
                    index = len(arr)-1
                    return arr[index]
                    #return barcodeData

        return None

    def image_opencvscanner(self, frame, boxs):
        if not boxs or len(boxs)<1:
            return None

        qrDecoder = cv2.QRCodeDetector()

        for box in boxs:    

            roi = self.image_interceptbox(frame, box)

            """
            result = frame.copy()
            cv2.drawContours(result, [box], 0, (0, 0, 255), 2)

            cv2.imshow('img2',result)
            cv2.waitKey(0)
            """

            
            data,bbox,rectifiedImage = qrDecoder.detectAndDecode(roi)

            if len(data)>0:
                print("Decoded Data : {}".format(data))
                return data

            _arr = [5, -5, 10, -10, 15, -15, 20, -20, 25, -25]
            #_arr = [3, -3, 6, -6, 9, -9, 12, -12, 15, -15, 18, -18, 21, -21, 24, -24, 27, -27]
            for r in _arr:
                _img = self.Rotate_Bound(roi, r)
                
                data,bbox,rectifiedImage = qrDecoder.detectAndDecode(_img)

                if len(data)>0:
                    return data            

        return None
        
    def focusing_scale(self,cap):
        res = []

        if not cap:
            return res

        h3 = cap.get(3)
        h4 = cap.get(4)

        res.append([h3 + int(h3 * 0.1), h4 + int(h4 * 0.1)])
        res.append([h3 + int(h3 * 0.2), h4 + int(h4 * 0.2)])
        res.append([h3 + int(h3 * 0.3), h4 + int(h4 * 0.3)])
        res.append([h3 + int(h3 * 0.4), h4 + int(h4 * 0.4)])
        res.append([h3 + int(h3 * 0.5), h4 + int(h4 * 0.5)])
        res.append([h3 + int(h3 * 0.6), h4 + int(h4 * 0.6)])
        res.append([h3 + int(h3 * 0.7), h4 + int(h4 * 0.7)])
        res.append([h3 + int(h3 * 0.8), h4 + int(h4 * 0.8)])
        res.append([h3 + int(h3 * 0.9), h4 + int(h4 * 0.9)])
        res.append([h3 + int(h3 * 1), h4 + int(h4 * 1)])

        """
        res.append([h3, h4])

        # 扩大20%
        h3_1 = h3 + int(h3 * 0.2)
        h4_1 = h4 + int(h4 * 0.2)
        res.append([h3_1, h4_1])

        # 扩大40%
        h3_2 = h3 + int(h3 * 0.4)
        h4_2 = h4 + int(h4 * 0.4)
        res.append([h3_2, h4_2])
        """
        return res

    def VideoScannerQRCode(self, istest=False):
        
        text = None

        try:
            cap = cv2.VideoCapture(0)

            i = 0
            m = 0
            focusing = self.focusing_scale(cap)

            while True:
                i = i + 1

                cv2.waitKey(2)
                
                r = i % 100

                if r<10 and m==0:
                    m = 1
                    cap.set(3, focusing[2][0])
                    cap.set(4, focusing[2][1])
                elif r>9 and r<20 and m==1:
                    m = 2
                    #cap.set(3, focusing[1][0])
                    #cap.set(4, focusing[1][1])
                elif r>19 and r<30 and m==2:
                    m = 3
                    #cap.set(3, focusing[2][0])
                    #cap.set(4, focusing[2][1])
                elif r>29 and r<40 and m==3:
                    m = 4
                    cap.set(3, focusing[3][0])
                    cap.set(4, focusing[3][1])
                elif r>39 and r<50 and m==4:
                    m = 5
                    cap.set(3, focusing[4][0])
                    cap.set(4, focusing[4][1])
                elif r>49 and r<60 and m==5:
                    m = 6
                    cap.set(3, focusing[5][0])
                    cap.set(4, focusing[5][1])
                elif r>59 and r<70 and m==6:
                    m = 7
                    cap.set(3, focusing[6][0])
                    cap.set(4, focusing[6][1])
                elif r>69 and r<80 and m==7:
                    m = 8
                    #cap.set(3, focusing[7][0])
                    #cap.set(4, focusing[7][1])
                elif r>79 and r<90 and m==8:
                    m = 9
                    #cap.set(3, focusing[8][0])
                    #cap.set(4, focusing[8][1])
                elif r>89 and m==9:
                    m = 0
                    #cap.set(3, focusing[9][0])
                    #cap.set(4, focusing[9][1])
                    
                """
                if m==0 and r<33:
                    m = 1
                    cap.set(3, focusing[0][0])
                    cap.set(4, focusing[0][1])
                elif m==1 and r>32 and r<66:
                    m = 2
                    cap.set(3, focusing[1][0])
                    cap.set(4, focusing[1][1])
                elif m==2 and r>65 and r<99:
                    m = 0
                    cap.set(3, focusing[2][0])
                    cap.set(4, focusing[2][1])
                    
                """

                if i>10 and i % 100 == 0:
                    #语音提醒没有放好提示                    
                    cmd = "二维码扫描失败，请检查摄像头是否对准二维码或调整蛋箱位置重试"
                    #print(cmd)
                    #self.voiceTip.ILangReadText(cmd)
                    
                    continue

                ret, frame = cap.read()

                
                if not ret:
                    continue
                
                
                # 灰度处理
                image =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)   
                 
                
                # 先闭图在轮廓获取
                boxs = self.find_closedorconboxs(image)

                # 轮廓获取
                #boxs = self.find_boxs(image)

                # 闭图获取
                #boxs = self.find_closedboxs(image)
                #cv2.imshow('img2',image)
                if istest:
                    cv2.imshow('frame', frame)
                    cv2.waitKey(0)

                    for b in boxs:
                        simage = image.copy()
                        cv2.drawContours(simage, [b], 0, (0, 0, 255), 2)

                        cv2.imshow('img2',simage)
                        cv2.waitKey(0)


                if len(boxs)>0:
                    text = self.image_scanner(image, boxs)

                    if text:
                        break

                
                #time.sleep(0.5)

        finally:
            cap.release()
            cv2.destroyAllWindows()
        
        return text

    def display(self, im, bbox):
        n = len(bbox)
        for j in range(n):
            cv2.line(im, tuple(bbox[j][0]), tuple(bbox[ (j+1) % n][0]), (255,0,0), 3)
    
        # Display results
        cv2.imshow("Results", im)

    def VideoOpenCVScannerQRCode(self, istest=False):
        text = None

        try:
            cap = cv2.VideoCapture(0)

            i = 0
            while True:
                i = i + 1

                cv2.waitKey(2)
                
                
                if i>10 and i % 100 == 0:
                    #语音提醒没有放好提示                    
                    cmd = "二维码扫描失败，请检查摄像头是否对准二维码或调整蛋箱位置重试"
                    #self.voiceTip.ILangReadText(cmd)
                    
                    
                    continue

                ret, frame = cap.read()

                
                if not ret:
                    continue
                
                # 灰度处理
                image =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)                
                
                # 先闭图在轮廓获取
                boxs = self.find_closedandconboxs(image)

                # 轮廓获取
                #boxs = self.find_boxs(image)

                # 闭图获取
                #boxs = self.find_closedboxs(image)

                if istest:
                    cv2.imshow('frame', frame)
                    cv2.waitKey(0)

                    for b in boxs:
                        simage = frame.copy()
                        cv2.drawContours(simage, [b], 0, (0, 0, 255), 2)

                        cv2.imshow('img2',simage)
                        cv2.waitKey(0)

                
                if len(boxs)>0:
                    text = self.image_opencvscanner(frame, boxs)

                    if text:
                        break

                
                #time.sleep(0.5)

                

        finally:
            cap.release()
            cv2.destroyAllWindows()
        
        if not barcodeData:
            return None
        else:
            return barcodeData
 
    def testVideoBoxs(self, isloop=True):
        try:
            cap = cv2.VideoCapture(0)
            
            i = 1
            while True:               
                
                ret, frame = cap.read()
                if not ret:
                    continue    

                #image=cv2.imread('code.png')
               
                image = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)    
               
                boxs = self.find_closedandconboxs(image)

                # 轮廓获取
                #boxs = self.find_boxs(image)

                # 闭图获取
                #boxs = self.find_closedboxs(image)

                for b in boxs:
                    simage = frame.copy()
                    cv2.drawContours(simage, [b], 0, (0, 0, 255), 2)

                    cv2.imshow('img2',simage)
                    cv2.waitKey(0)


                
        finally:
            cap.release()
            cv2.destroyAllWindows()

    def testImgBoxs(self, path):
        try:
            if not path:
                return

            frame=cv2.imread(path)

            image = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            
            #boxs = self.find_boxs(image)
            boxs = self.find_closedandconboxs(image)

            # print(np.shape(boxs))
            cv2.imshow('img',frame)
            cv2.waitKey(0)

            for box in boxs:               
                simage = frame.copy()
                cv2.drawContours(simage, [box], 0, (0, 0, 255), 2)

                cv2.imshow('img2',simage)
                cv2.waitKey(0)
            
                
        finally:
            cv2.destroyAllWindows()

    def testVideoScanner(self, isloop=True):
        try:
            cap = cv2.VideoCapture(0)
            
            focusing = self.focusing_scale(cap)
            i = 0
            m=0
            while True:               
                
                ret, frame = cap.read()

                if not ret:
                    continue    

                r = i % 100

                if r<10 and m==0:
                    m = 1
                    cap.set(3, focusing[0][0])
                    cap.set(4, focusing[0][1])
                elif r>9 and r<20 and m==1:
                    m = 2
                    cap.set(3, focusing[1][0])
                    cap.set(4, focusing[1][1])
                elif r>19 and r<30 and m==2:
                    m = 3
                    cap.set(3, focusing[2][0])
                    cap.set(4, focusing[2][1])
                elif r>29 and r<40 and m==3:
                    m = 4
                    cap.set(3, focusing[3][0])
                    cap.set(4, focusing[3][1])
                elif r>39 and r<50 and m==4:
                    m = 5
                    cap.set(3, focusing[4][0])
                    cap.set(4, focusing[4][1])
                elif r>49 and r<60 and m==5:
                    m = 6
                    #cap.set(3, focusing[5][0])
                    #cap.set(4, focusing[5][1])
                elif r>59 and r<70 and m==6:
                    m = 7
                    #cap.set(3, focusing[6][0])
                    #cap.set(4, focusing[6][1])
                elif r>69 and r<80 and m==7:
                    m = 8
                    #cap.set(3, focusing[7][0])
                    #cap.set(4, focusing[7][1])
                elif r>79 and r<90 and m==8:
                    m = 9
                    #cap.set(3, focusing[8][0])
                    #cap.set(4, focusing[8][1])
                elif r>89 and m==9:
                    m = 0
                    #cap.set(3, focusing[9][0])
                    #cap.set(4, focusing[9][1])

                #image=cv2.imread('code.png')
               
                image = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)    
               
                boxs = self.find_closedorconboxs(image)

                i = i+1
                # 轮廓获取
                #boxs = self.find_boxs(image)

                # 闭图获取
                #boxs = self.find_closedboxs(image)

                cv2.imshow('img',image)
                """
                for b in boxs:
                    simage = frame.copy()
                    cv2.drawContours(simage, [b], 0, (0, 0, 255), 2)

                    cv2.imshow('img2',simage)
                    cv2.waitKey(1)
                """
                text = self.image_scanner(image, boxs)

                if text:
                    print(text)
                    return None

                
        finally:
            cap.release()
            cv2.destroyAllWindows()

    def testImgScanner(self, path):
        try:
            if not path:
                return

            frame=cv2.imread(path)

            image = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            
            #boxs = self.find_boxs(image)
            boxs = self.find_closedorconboxs(image)

            # print(np.shape(boxs))
            cv2.imshow('img',frame)
            cv2.waitKey(0)

            for box in boxs:               
                simage = frame.copy()
                cv2.drawContours(simage, [box], 0, (0, 0, 255), 2)

                cv2.imshow('img2',simage)
                cv2.waitKey(0)
            
            text = self.image_scanner(frame, boxs)

            if text:
                print(text)
                return None
                
        finally:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    
    obj = ScannerImage()
   
    # 获取视频中的二维码框
    obj.testVideoScanner()

    #obj.testImgScanner("test.png")

    """
    # 获取视频中的二维码并解析
    obj.testVideoScanner()


    # 获取图片中的二维码框
    path = ''
    obj.testImgBoxs(paht)

    # 获取图片中的二维码并解析
    path = ''
    obj.testImgScanner(path)
    """
    
