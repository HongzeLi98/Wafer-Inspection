# coding=utf-8
import cv2
import mrcnn_alg_interface
import xx_alg_interface
import os
import numpy as np

def is_ng142(img):
    is_ng142 = 0
    img_size = img.shape
    img_roi = img[int(img.shape[0]*0.05):int(img.shape[0]*0.95),int(img.shape[1]*0.05):int(img.shape[1]*0.95)]
    gray = cv2.cvtColor(img_roi, cv2.COLOR_RGB2GRAY)
    ret, binary = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    binary = cv2.bitwise_not(binary)  #对二值图像反色
    _, contours, hier = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area = cv2.contourArea(c)
        if(area > 2000):
            is_ng142 = 1
            break
    return is_ng142, contours

def load_mrcnn(model_path):
    file_list = os.listdir(model_path)
    for name in file_list:
        if (name.endswith('.pth') or name.endswith('.pb'))and name:
            model_name = model_path + name
    gpu_index_str = "0"
    os.environ['CUDA_DEVICE_ORDER'] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_index_str) # eg: "0,1"
    ai = mrcnn_alg_interface.MrcnnAlg(model_path=model_name)
    return ai

def load_V4(model_path):
    gpu_index_str = "0"
    os.environ['CUDA_DEVICE_ORDER'] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_index_str)
    file_list = os.listdir(model_path)
    for name in file_list:
        if (name.endswith('.pth') or name.endswith('.pb'))and name:
            model_name = model_path + name
    ai = xx_alg_interface.XXAlg(INIT_device_index_str=gpu_index_str, INIT_gpu_rate_tuple=(0.3,), INIT_model_path = model_name)
    return ai 
    
def run_mrcnn(ai, im_v, path):

    file_list = os.listdir(path)
    #ts = time.time()
    #print(file_list)
    #print(im_name)
    #print(path)
    op = []
    cont = tuple()
    number = 0
    result = 0
    pred = 0
    if len(file_list) == 2:
        for name in file_list:
            if name.endswith('.jpg') and name:
                #print(name)
                template = cv2.imread(path+name,0)
                name = name.lower()
                sty = name[0]
                ns = name.split('.')
                number = ns[0]
                number = int(number[1:])
                tmp_sp = template.shape
                #print(tmp_sp)
                coe_h = 299/tmp_sp[0]
                coe_w = 299/tmp_sp[1]
                template = cv2.resize(template,(299,299),interpolation=cv2.INTER_LINEAR)

                img_rgb_o = im_v
                img_rgb = img_rgb_o.copy()
                img_rgb = cv2.resize(img_rgb, None, fx = coe_w, fy = coe_h, interpolation=cv2.INTER_LINEAR)
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                h, w = np.shape(template)
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                p,q = np.shape(res)
                #p_1, q_1 = np.shape(img_gray)

                #image3 = np.ones((h,w,1))*0
                radius = int(min(h,w)/2)
                #for m in range(0,h):
                #    for n in range(0,w):
                #        if (((m-int(h/2))**2 + (n-int(w/2))**2)**0.5) <= radius:
                #            image3[m,n]=255
                #        else:
                #            continue

                stack = np.zeros((2,2))
                #aloo_last = np.zeros((1,1))
                #m_value = np.max(res)
                #print(m_value)
                for i in range(0,number):
                    loo = cv2.minMaxLoc(res)
                    nh_4 = loo[3][1]
                    nw_4 = loo[3][0]
                    #print(res[nh_4,nw_4])
                    res[max(int(nh_4)-int(int(h)*0.5),0):min(int(nh_4)+int(int(h)*0.5),p),max(int(nw_4)-int(int(w)*0.5),0):min(int(nw_4)+int(int(w)*0.5),q)] = -100
                    loo = np.array([[nh_4], [nw_4]])
                    stack = np.concatenate((stack, loo), axis=1)
                
                content = tuple()
                #img_rgb = cv2.resize(img_rgb, None, fx = 1/coe_w, fy = 1/coe_h, interpolation=cv2.INTER_LINEAR)
                for i in range(2,number+2):
                    image1 = img_rgb_o.copy()
                    image2 = image1[int(stack[0,i]/coe_h):(int(stack[0,i]/coe_h) + int(h/coe_w)), int(stack[1,i]/coe_w):(int(stack[1,i]/coe_w) + int(w/coe_w))]
                    #cv2.imwrite(str(i) +'.jpg',image2)
                    #cv2.rectangle(img_rgb,(int(int(stack[1,i])/coe_w),int(int(stack[0,i])/coe_h)),(int((int(stack[1,i])+299)/coe_w),int((int(stack[0,i])+299)/coe_h)),(255,255,0),5)
                    #print('(',int(int(stack[1,i])/coe_w),',',int(int(stack[0,i])/coe_h),')')
                    #print(np.shape(image2))
                    if sty == 'r':
                        for m in range(0,h):
                            for n in range(0,w):
                                if (((m-int(h/2/coe_h))**2 + (n-int(w/2/coe_w))**2)**0.5) >= radius:
                                    image2[m,n,:]=0
                                else:
                                    continue
                        #print(np.shape(image2))
                        #print(np.shape(image3))
                        #image2 = np.c_[image2,image3]
                    content += (image2,)
                cont = content

    ng_142,contours = is_ng142(content[0])
    #print("ng142",ng_142)
    if(ng_142 == 0):   ## 不是ng142
        result = ai.run(cont, batch_size=1)
    
        for i in range(2,number+2):
            pred = result[i-2]
            #print(pred)
            value = [int(stack[1,i]/coe_w),int(stack[0,i]/coe_h),int(w/coe_w),int(h/coe_h),pred]
            #value  = str(value)
            op += [value,]
    
    cont = tuple()
    number = 0
    result = 0
    pred = 0
    file_list = 0
    template = 0
    img_rgb = 0
    img_gray = 0
    res = 0
    stack = 0
    image1 = 0
    image2 = 0

    return op, content,ng_142,contours


def run_mrcnn_back(ai, im_v, path):

    file_list = os.listdir(path)
    #ts = time.time()
    #print(file_list)
    #print(im_name)
    #print(path)
    op = []
    cont = tuple()
    number = 0
    result = 0
    pred = 0
    if len(file_list) == 2:
        for name in file_list:
            if name.endswith('.jpg') and name:
                #print(name)
                template = cv2.imread(path+name,0)
                name = name.lower()
                sty = name[0]
                ns = name.split('.')
                number = ns[0]
                number = int(number[1:])
                tmp_sp = template.shape
                #print(tmp_sp)
                coe_h = 299/tmp_sp[0]
                coe_w = 299/tmp_sp[1]
                template = cv2.resize(template,(299,299),interpolation=cv2.INTER_LINEAR)

                img_rgb = im_v.copy()

                #1125 保存扣出的照片
                #res_temp = cv2.matchTemplate(im_v, template, cv2.TM_CCOEFF_NORMED)

                img_rgb = cv2.resize(img_rgb, None, fx = coe_w, fy = coe_h, interpolation=cv2.INTER_LINEAR)
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                h, w = np.shape(template)
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

                p,q = np.shape(res)
                #p_1, q_1 = np.shape(img_gray)

                #image3 = np.ones((h,w,1))*0
                radius = int(min(h,w)/2)
                #for m in range(0,h):
                #    for n in range(0,w):
                #        if (((m-int(h/2))**2 + (n-int(w/2))**2)**0.5) <= radius:
                #            image3[m,n]=255
                #        else:
                #            continue

                stack = np.zeros((2,2))
                #aloo_last = np.zeros((1,1))
                m_value = np.max(res)
                #print(m_value)
                for i in range(0,number):
                    #print(np.max(res))
                    if np.max(res) <= (m_value/5):
                        number = i
                        #print(number)
                        break
                    loo = np.where(res >= np.max(res))
                    #print(i)
                    aloo = np.array(loo,dtype=int)
                    n,m = np.shape(aloo)
                    #print(aloo[0,0],aloo[1,0])
                    #print((aloo[0,0]+int(h)),(aloo[1,0]+int(w)))
                    res[max(int(aloo[0,0])-int(int(h)*0.5),0):min(int(aloo[0,0])+int(int(h)*0.5),p+int(h)),max(int(aloo[1,0])-int(int(w)*0.5),0):min(int(aloo[1,0])+int(int(w)*0.5),q+int(w))] = 0
                    #stack = np.concatenate((stack,aloo),axis=1)
                    stack = np.c_[stack,aloo[:,0]]
                
                content = tuple()
                #img_rgb = cv2.resize(img_rgb, None, fx = 1/coe_w, fy = 1/coe_h, interpolation=cv2.INTER_LINEAR)
                for i in range(2,number+2):
                    image1 = img_rgb.copy()
                    image2 = image1[int(stack[0,i]):(int(stack[0,i]) + h), int(stack[1,i]):(int(stack[1,i]) + w)]
                    #cv2.imwrite(str(i) +'.jpg',image2)
                    #cv2.rectangle(img_rgb,(int(int(stack[1,i])/coe_w),int(int(stack[0,i])/coe_h)),(int((int(stack[1,i])+299)/coe_w),int((int(stack[0,i])+299)/coe_h)),(255,255,0),5)
                    #print('(',int(int(stack[1,i])/coe_w),',',int(int(stack[0,i])/coe_h),')')
                    #print(np.shape(image2))
                    if sty == 'r':
                        for m in range(0,h):
                            for n in range(0,w):
                                if (((m-int(h/2))**2 + (n-int(w/2))**2)**0.5) >= radius:
                                    image2[m,n,:]=0
                                else:
                                    continue
                        #print(np.shape(image2))
                        #print(np.shape(image3))           
                        #image2 = np.c_[image2,image3]
                    content += (image2,)
                cont = content


    result = ai.run(cont, RUN_device_index=0)
    
    #cv2.imwrite('55.jpg',img_rgb)
    
    for i in range(2,number+2):
        pred = result[i-2]
        #print(pred)
        value = [int(int(stack[1,i])/coe_w),int(int(stack[0,i])/coe_h),int(w/coe_w),int(h/coe_h),pred.index(max(pred))]
        #value  = str(value)
        op += [value,]



    cont = tuple()
    number = 0
    result = 0
    pred = 0
    file_list = 0
    template = 0
    img_rgb = 0
    img_gray = 0
    res = 0
    stack = 0
    image1 = 0
    image2 = 0
 
    return op,content


def run_mrcnn_back_recheck(ai, im_v, path):

    file_list = os.listdir(path)
    #ts = time.time()
    #print(file_list)
    #print(im_name)
    #print(path)
    op = []
    cont = tuple()
    number = 0
    result = 0
    pred = 0
    if len(file_list) == 2:
        for name in file_list:
            if name.endswith('.jpg') and name:
                #print(name)
                template = cv2.imread(path+name,0)
                name = name.lower()
                sty = name[0]
                ns = name.split('.')
                number = ns[0]
                number = int(number[1:])
                tmp_sp = template.shape
                #print(tmp_sp)
                coe_h = 299/tmp_sp[0]
                coe_w = 299/tmp_sp[1]
                template = cv2.resize(template,(299,299),interpolation=cv2.INTER_LINEAR)

                img_rgb = im_v.copy()

                #1125 保存扣出的照片
                #res_temp = cv2.matchTemplate(im_v, template, cv2.TM_CCOEFF_NORMED)

                img_rgb = cv2.resize(img_rgb, None, fx = coe_w, fy = coe_h, interpolation=cv2.INTER_LINEAR)
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                h, w = np.shape(template)
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

                p,q = np.shape(res)
                #p_1, q_1 = np.shape(img_gray)

                #image3 = np.ones((h,w,1))*0
                radius = int(min(h,w)/2)
                #for m in range(0,h):
                #    for n in range(0,w):
                #        if (((m-int(h/2))**2 + (n-int(w/2))**2)**0.5) <= radius:
                #            image3[m,n]=255
                #        else:
                #            continue

                stack = np.zeros((2,2))
                #aloo_last = np.zeros((1,1))
                m_value = np.max(res)
                #print(m_value)
                for i in range(0,number):
                    #print(np.max(res))
                    if np.max(res) <= (m_value/5):
                        number = i
                        #print(number)
                        break
                    loo = np.where(res >= np.max(res))
                    #print(i)
                    aloo = np.array(loo,dtype=int)
                    n,m = np.shape(aloo)
                    #print(aloo[0,0],aloo[1,0])
                    #print((aloo[0,0]+int(h)),(aloo[1,0]+int(w)))
                    res[max(int(aloo[0,0])-int(int(h)*0.5),0):min(int(aloo[0,0])+int(int(h)*0.5),p+int(h)),max(int(aloo[1,0])-int(int(w)*0.5),0):min(int(aloo[1,0])+int(int(w)*0.5),q+int(w))] = 0
                    #stack = np.concatenate((stack,aloo),axis=1)
                    stack = np.c_[stack,aloo[:,0]]

                content = tuple()
                #img_rgb = cv2.resize(img_rgb, None, fx = 1/coe_w, fy = 1/coe_h, interpolation=cv2.INTER_LINEAR)
                for i in range(2,number+2):
                    image1 = img_rgb.copy()
                    image2 = image1[int(stack[0,i]):(int(stack[0,i]) + h), int(stack[1,i]):(int(stack[1,i]) + w)]
                    #cv2.imwrite(str(i) +'.jpg',image2)
                    #cv2.rectangle(img_rgb,(int(int(stack[1,i])/coe_w),int(int(stack[0,i])/coe_h)),(int((int(stack[1,i])+299)/coe_w),int((int(stack[0,i])+299)/coe_h)),(255,255,0),5)
                    #print('(',int(int(stack[1,i])/coe_w),',',int(int(stack[0,i])/coe_h),')')
                    #print(np.shape(image2))
                    if sty == 'r':
                        for m in range(0,h):
                            for n in range(0,w):
                                if (((m-int(h/2))**2 + (n-int(w/2))**2)**0.5) >= radius:
                                    image2[m,n,:]=0
                                else:
                                    continue
                        #print(np.shape(image2))
                        #print(np.shape(image3))
                        #image2 = np.c_[image2,image3]
                    content += (image2,)
                cont = content


    result = ai.run(cont, RUN_device_index=0)

    #cv2.imwrite('55.jpg',img_rgb)

    for i in range(2,number+2):
        pred = result[i-2]
        #print(pred)
        value = [int(int(stack[1,i])/coe_w),int(int(stack[0,i])/coe_h),int(w/coe_w),int(h/coe_h),pred.index(max(pred))]
        #value  = str(value)
        op += [value,]



    cont = tuple()
    number = 0
    result = 0
    pred = 0
    file_list = 0
    template = 0
    img_rgb = 0
    img_gray = 0
    res = 0
    stack = 0
    image1 = 0
    image2 = 0

    return op,content
