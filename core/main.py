# 此版本可以自定义OK,NG对应的数字
# 模型和模板的文件夹可以在项目里创建

# 12.14 更新，Recreate: 重新根据OK和NG图片建立文件夹
# 01.16 更新，back模型级联，新开辟文件夹存储模型，新模型推断程序
# 01.16 更新，新增一个吸取转化工人map图的按钮

import mrcnn
import ToXML_OKNG
import os
import numpy as np
import cv2


def start_wafer(ProjectPath, ResPath, NewName, OKNum, NGNum):
    ProjectPath = ProjectPath
    IoName = ["\\Input", "\\Output", "\\Source"]
    OriName = ["\\Front", "\\Back", "\\Back_Recheck"]
    ClassName = ["\\OK", "\\NG", "\\Xml"]

    AsmbPath = [
        ProjectPath+IoName[0]+OriName[0],
        ProjectPath+IoName[0]+OriName[1],
        ProjectPath+IoName[1]+OriName[0]+ClassName[0],
        ProjectPath+IoName[1]+OriName[0]+ClassName[1],
        ProjectPath+IoName[1]+OriName[0]+ClassName[2],
        ProjectPath+IoName[1]+OriName[1]+ClassName[0],
        ProjectPath+IoName[1]+OriName[1]+ClassName[1],
        ProjectPath+IoName[1]+OriName[1]+ClassName[2],
        ProjectPath+IoName[1]+ClassName[2],
        # 正面资源，反面资源
        ResPath+OriName[0]+"\\",
        ResPath+OriName[1]+"\\",
        # 新增一个判断浅色气泡的模型
        ResPath+OriName[2]+"\\"
        ]

    SocPath = [
        ResPath + "\\XmlTemplate",     #模板依然在原始资源文件夹里
        ResPath + "\\FinalXmlTemplate"
    ]

    # ----------创建文件夹----------- #
    for i in range(len(AsmbPath)):
        folder = os.path.exists(AsmbPath[i])

        if not folder:
            os.makedirs(AsmbPath[i])  # makedirs 创建文件时如果路径不存在会创建这个路径
            print("Create new folder")
            print("Create Successfully")
        else:
            print("Folder already exists")

    for i in range(len(SocPath)):
        folder = os.path.exists(SocPath[i])

        if not folder:
            os.makedirs(SocPath[i])  # makedirs 创建文件时如果路径不存在会创建这个路径
            print("Create new folder")
            print("Create Successfully")
        else:
            print("Folder already exists")
    # ----------创建文件夹----------- #

# ------------------------处理反面------------------------------#

    ImageList_back = os.listdir(AsmbPath[1])
    ai_model_back = mrcnn.load_V4(AsmbPath[10])

    for image in ImageList_back:
        object_class = image.split('.')[0]      #去掉文件扩展名
        if image.split('.')[-1] != 'jpg':
            src = cv2.imread(AsmbPath[1]+"\\"+image)
            cv2.imwrite(AsmbPath[1]+"\\"+object_class+'.jpg',src)
            os.remove(AsmbPath[1]+'\\'+image)
            img = cv2.imread(AsmbPath[1]+"\\"+object_class+'.jpg')

        else:
            img = cv2.imread(AsmbPath[1]+"\\"+image)

        # img_temp是扣图出来的照片，大小为299*299
        result, img_temp = mrcnn.run_mrcnn_back(ai_model_back, img, AsmbPath[10])

        if result[0][-1] == 1:
            cv2.imwrite(AsmbPath[6] + '\\' + object_class + '.jpg', img_temp[0])
        else:
            cv2.imwrite(AsmbPath[5] + '\\' + object_class + '.jpg', img_temp[0])

    print('反面图片处理完毕')


# -----------------处理反面的浅色气泡，加载新的模型-----------------------#

    # 从output->back->NG文件夹里面读取图像列表
    ImageList_back_NG = os.listdir(AsmbPath[6])
    ai_model_back = mrcnn.load_V4(AsmbPath[11])

    for image in ImageList_back_NG:
        object_class = image.split('.')[0]      #去掉文件扩展名
        if image.split('.')[-1] != 'jpg':
            src = cv2.imread(AsmbPath[6]+"\\"+image)
            cv2.imwrite(AsmbPath[6]+"\\"+object_class+'.jpg',src)
            os.remove(AsmbPath[6]+'\\'+image)
            img = cv2.imread(AsmbPath[6]+"\\"+object_class+'.jpg')

        else:
            img = cv2.imread(AsmbPath[6]+"\\"+image)

        # 新增一个调用函数
        result, img_temp = mrcnn.run_mrcnn_back_recheck(ai_model_back, img, AsmbPath[11])

        if result[0][-1] == 0:
            cv2.imwrite(AsmbPath[5] + '\\' + object_class + '.jpg', img_temp[0])
            os.remove(AsmbPath[6]+"\\"+object_class+'.jpg')

    print('浅色气泡反面图片处理完毕')

# ------------------------处理正面，v4格式------------------------------#

    # ImageList_front = os.listdir(AsmbPath[0])
    # ai_model_front = mrcnn.load_V4(AsmbPath[9])
    #
    # for image in ImageList_front:
    #     object_class = image.split('.')[0]      #去掉文件扩展名
    #     if image.split('.')[-1] != 'jpg':
    #         src = cv2.imread(AsmbPath[0]+"\\"+image)
    #         cv2.imwrite(AsmbPath[0]+"\\"+object_class+'.jpg',src)
    #         os.remove(AsmbPath[0]+'\\'+image)
    #         img = cv2.imread(AsmbPath[0]+"\\"+object_class+'.jpg')
    #
    #     else:
    #         img = cv2.imread(AsmbPath[0]+"\\"+image)
    #
    #     # img_temp是扣图出来的照片，大小为299*299
    #     result, img_temp = mrcnn.run_mrcnn_back(ai_model_front, img, AsmbPath[9])
    #
    #     if result[0][-1] == 1:
    #         cv2.imwrite(AsmbPath[3] + '\\' + object_class + '.jpg', img_temp[0])
    #     else:
    #         cv2.imwrite(AsmbPath[2] + '\\' + object_class + '.jpg', img_temp[0])
    #
    # print('正面图片处理完毕')

#------------------------处理正面------------------------------#

    # 非jpg格式文件全部转码，生成img
    ImageList = os.listdir(AsmbPath[0])
    ai_model = mrcnn.load_mrcnn(AsmbPath[9])

    for image in ImageList:
        object_class = image.split('.')[0]      #去掉文件扩展名
        if image.split('.')[-1] != 'jpg':
            src = cv2.imread(AsmbPath[0]+"\\"+image)
            cv2.imwrite(AsmbPath[0]+"\\"+object_class+'.jpg',src)
            os.remove(AsmbPath[0]+'\\'+image)
            img = cv2.imread(AsmbPath[0]+"\\"+object_class+'.jpg')
        else:
            img = cv2.imread(AsmbPath[0]+"\\"+image)

        result, image_set, ng_142,contours = mrcnn.run_mrcnn(ai_model, img, AsmbPath[9])

        #这部分是用来话黑团的
        if(ng_142):
            cv2.drawContours(image_set[0][40:680,40:680],contours, -1,(0,0,255),3)
            cv2.imwrite(AsmbPath[3] + '\\' + object_class + '.jpg', image_set[0])
        else:
            #print(result[0][4])
            #print("Number of NG:", len(result[0][4]),"\n")
            #为什么是>1, 因为只有一个NG区域很多的是误判
            if len(result[0][4]) > 1:
                for ng in result[0][4]:
                    nodes = []
                    #print(ng)
                    #print("ng length",len(ng),",ng_type",type(ng),"\n")
                    for i in range(1,len(ng),2):
                        nodes.append(ng[i:i+2])         # 两两分组
                    nodes = np.array(nodes)                          # 必转换为numpy.array
                    cv2.polylines(image_set[0], [nodes], True, (0, 0, 255))       # 画折线
                cv2.imwrite(AsmbPath[3] + '\\' + object_class + '.jpg', image_set[0])
            else:
                cv2.imwrite(AsmbPath[2] + '\\' + object_class + '.jpg', image_set[0])

    print('正面图片处理完毕')

    ToXML_OKNG.toxml(AsmbPath, SocPath, NewName, OKNum, NGNum)

# start_wafer(r'D:\WAFER_LOT_TEST - Copy',r'D:\wafer\Wafer Inspection 0224\Wafer Inspection 0224\Source','dda', '00000111', '00000222')
