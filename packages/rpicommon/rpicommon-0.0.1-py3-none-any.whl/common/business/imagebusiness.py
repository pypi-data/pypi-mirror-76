# coding:utf-8

import sys
import time
import cv2
#import datetime
import numpy as np
from pyzbar import pyzbar

sys.path.append('./')

class ImageBusiness:
    def __init__(self, check=False, barcode=False):
        #是否检测到二维码标示
        self.check = check
        #是否是条形码
        self.barcode = barcode

    def DetectQRCodeLocation(self,frame, barcode=False):
        if not frame:
            self.check = False            
            return None

        try:
            #图像边缘细节处理
            #使用scharr操作(指定ksize=-1)构造灰度图在水平和竖直方向上的梯度幅值表示
            frameX = cv2.Sobel(frame, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)  # 对x方向求导
            frameY = cv2.Sobel(frame, ddepth=cv2.CV_32F, dx=0, dy=0, ksize=-1)   # 对y方向求导

            # Scharr操作后，从X梯度减去Y梯度得到轮廓图，此时噪点较多
            gradient = cv2.subtract(frameX, frameY)

            # 经过处理后，用convertScaleAbs()函数将其转回原来的uint8形式。否则将无法显示图像，而只是一副灰色的窗口
            gradient = cv2.convertScaleAbs(gradient)

            # 然后对梯度图采用用9x9的核进行平均模糊,进行于降噪
            blurred = cv2.blur(gradient, (9, 9))  # 通过低通滤波平滑图像

            # 然后进行二值化处理，要么是255(白)要么是0(黑)
            ret, thresh = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)  # 进行图像固定阈值二值化

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

            # 寻找轮廓
            binary, contours, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 如果没有找到，返回空9
            if len(contours) == 0:
                self.check = False
                return None

            c = sorted(contours, key=cv2.contourArea, reverse=True)[0]
            rect = cv2.minAreaRect(c)  # 生成最小外接矩形
            # box为一个ndarry数组，返回4个顶点位置
            box = np.int0(cv2.boxPoints(rect))
            #cv2.drawContours(frame, [box], 0, (255, 0, 0), 2)      #给轮廓填充颜色
        
            self.check = True
            return box
        except:
            self.check=False
            return None
        
    def VideoScannerQRCode(self):
        try:
            cap = cv2.VideoCapture(0)

            i = 0
            while True:
                i = i + 1

                if i % 10 == 0:
                    #语音提醒没有放好提示
                    # :todo
                    pass

                ret, frame = cap.read()

                cv2.waitKey(3)

                if not ret:
                    continue

                # 灰度处理
                frame =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

                box = self.DetectQRCodeLocation(frame)

                if self.check:
                    self.check = False

                    height,width=frame.shape[:2]

                    min = np.min(box, axis=0)
                    max = np.max(box, axis=0)

                    min=min[:]-80
                    max=max[:]+80
                    
                    minArr=np.zeros(min.shape,dtype=np.int16)
                    #maxArr=np.full(max.shape,width,dtype=np.int16)

                    min=np.maximum(min[:],minArr[:])
                    max[0]=np.minimum(max[0],width)
                    max[1]=np.minimum(max[1],height)

                    roi = frame[min[1] :max[1], min[0] :max[0] ]
            

                    barcodes = pyzbar.decode(roi)

                    for barcode in barcodes:
                    
                        barcodeData = barcode.data.decode("utf-8")
                        
                        if len(barcodeData)>0:
                            i=0
                            break
                    
                    if i==0:
                        break

                time.sleep(0.5)


        finally:
            cap.release()
            cv2.destroyAllWindows()
        
        if not barcodeData:
            return None
        else:
            return barcodeData


        
    
        
    