from xml.dom.minidom import parse
import xml.dom.minidom
import os
import re
import time
import shutil

def read_ok(num, row_mat, asebpath, OKNum):
    #type = re.findall(r'\d+', ClassName[Cindex])[0] # 提取数字
    MyList = os.listdir(asebpath)      # 获取文件夹内文件名
    for i in range(len(MyList)):
        MyList[i] = MyList[i].split("_")    # 以下划线为分隔符，分割一次
        #print(MyList)
    for i in range(len(MyList)):
        MyList[i][5] = MyList[i][5].split('.')[0]
        if int(MyList[i][5]) == num:
            row_mat[int(MyList[i][4])] = OKNum
    return row_mat

def read_ng(num, row_mat, asebpath, NGNum):
    #type = re.findall(r'\d+', ClassName[Cindex])[0] # 提取数字
    MyList = os.listdir(asebpath)      # 获取文件夹内文件名
    for i in range(len(MyList)):
        MyList[i] = MyList[i].split("_")    # 以下划线为分隔符，分割一次
        #print(MyList)
    for i in range(len(MyList)):
        MyList[i][5] = MyList[i][5].split('.')[0]
        if int(MyList[i][5]) == num:
            row_mat[int(MyList[i][4])] = NGNum
    return row_mat

def Recreate(InputPath, SourcePath, newname, OKNum, NGNum):

    IoName = ["\\Input", "\\Output", "\\Source"]
    OriName = ["\\Front", "\\Back"]
    ClassName = ["\\OK", "\\NG", "\\Xml"]

    AsebPath = [
        InputPath+IoName[0]+OriName[0],
        InputPath+IoName[0]+OriName[1],
        InputPath+IoName[1]+OriName[0]+ClassName[0],
        InputPath+IoName[1]+OriName[0]+ClassName[1],
        InputPath+IoName[1]+OriName[0]+ClassName[2],
        InputPath+IoName[1]+OriName[1]+ClassName[0],
        InputPath+IoName[1]+OriName[1]+ClassName[1],
        InputPath+IoName[1]+OriName[1]+ClassName[2],
        InputPath+IoName[1]+ClassName[2],
        # 正面资源，反面资源
        SourcePath+OriName[0]+"\\",
        SourcePath+OriName[1]+"\\"
        ]

    shutil.copy(SourcePath + '\\XmlTemplate\\' + 'WaferTemplate.xml', AsebPath[4]+ '\\' + newname + '_Front.xml')
    DOMTree = xml.dom.minidom.parse(AsebPath[4]+ '\\' + newname + '_Front.xml')
    patterns = DOMTree.documentElement
    rows = patterns.getElementsByTagName("ROW")       # 根据标签名获取

    NowTime = time.localtime(time.time())
    History = patterns.getElementsByTagName("INSPECTION")       # 根据标签名获取
    History[0].setAttribute("day", str(NowTime.tm_mday))
    History[0].setAttribute("month", str(NowTime.tm_mon))
    History[0].setAttribute("year", str(NowTime.tm_year))
    History[0].setAttribute("operator","")
    History[0].setAttribute("type","")

    # ------- 用来保存正面数组，用于合成 ------- #
    record_f = []

    for i in range(len(rows)):
        row_mat = rows[i].firstChild.data.split()
        row_mat = read_ok(i, row_mat, AsebPath[2], OKNum)
        row_mat = read_ng(i, row_mat, AsebPath[3], NGNum)
        row_mat_re = " ".join(row_mat)                 # 矩阵拼接成字符串
        rows[i].firstChild.data = row_mat_re

        record_f.append(row_mat)                      # 保存正面数据

    with open(AsebPath[4]+ '\\' + newname + '_Front.xml', 'w') as fp:
        DOMTree.writexml(fp)                          # 注意这里write的时候要用fp这种已处理形式
        print("正面xml生成成功")

    # 处理反面xml

    shutil.copy(SourcePath + '\\XmlTemplate\\' + 'WaferTemplate.xml', AsebPath[7]+ '\\' + newname + '_Back.xml')
    DOMTree_b = xml.dom.minidom.parse(AsebPath[7]+ '\\' + newname + '_Back.xml')
    patterns_b = DOMTree_b.documentElement
    rows_b = patterns_b.getElementsByTagName("ROW")       # 根据标签名获取

    History_b = patterns_b.getElementsByTagName("INSPECTION")       # 根据标签名获取
    History_b[0].setAttribute("day", str(NowTime.tm_mday))
    History_b[0].setAttribute("month", str(NowTime.tm_mon))
    History_b[0].setAttribute("year", str(NowTime.tm_year))
    History_b[0].setAttribute("operator","")
    History_b[0].setAttribute("type","")

    record_b = []

    for i in range(len(rows_b)):
        row_mat_b = rows_b[i].firstChild.data.split()
        row_mat_b = read_ok(i, row_mat_b, AsebPath[5], OKNum)
        row_mat_b = read_ng(i, row_mat_b, AsebPath[6], NGNum)
        row_mat_re_b = " ".join(row_mat_b)                 # 矩阵拼接成字符串
        rows_b[i].firstChild.data = row_mat_re_b

        record_b.append(row_mat_b)                      # 保存反面数据

    with open(AsebPath[7]+ '\\' + newname + '_Back.xml', 'w') as fp_b:
        DOMTree_b.writexml(fp_b)                          # 注意这里write的时候要用fp这种已处理形式
        print("反面xml生成成功")

# --------------编辑xml文件中的row元素---------------- #

# --------------将之前两个xml文件合并----------------- #

    # ----------先将front和back内容合并--------------- #
    # 正反都为空，设为099，都ok，设为001，有ng，设为013
    #print(len(record_f))
    #print(len(record_f[0]))
    count_013 = 0
    count_001 = 0

    record_front_back = record_b.copy()

    for i in range(0, len(record_f)):
        for j in range(0,len(record_f[0])):
            if(record_f[i][j] != record_b[i][j]):
                record_f[i][j] = '013'
                record_front_back[i][j] = NGNum
                count_013 += 1
            else:
                if(record_f[i][j] == OKNum):
                    record_f[i][j]='001'
                    record_front_back[i][j] =OKNum
                    count_001 += 1
                elif(record_f[i][j] == NGNum):
                    record_f[i][j]='013'
                    record_front_back[i][j] = NGNum
                    count_013 += 1
                else:
                    record_f[i][j]='099'
                    record_front_back[i][j] = '00000000'

    #先生成一个前道工序图
    shutil.copy(SourcePath + '\\XmlTemplate\\' + 'WaferTemplate.xml', AsebPath[8]+ '\\' + newname + '_OIM328' + '.xml')
    DOMTree_front_back = xml.dom.minidom.parse(AsebPath[8]+ '\\' + newname + '_OIM328' + '.xml')
    patterns_front_back = DOMTree_front_back.documentElement
    rows_front_back = patterns_front_back.getElementsByTagName("ROW")

    History_front_back = patterns_front_back.getElementsByTagName("INSPECTION")       # 根据标签名获取
    History_front_back[0].setAttribute("day", str(NowTime.tm_mday))
    History_front_back[0].setAttribute("month", str(NowTime.tm_mon))
    History_front_back[0].setAttribute("year", str(NowTime.tm_year))
    History_front_back[0].setAttribute("operator","")
    History_front_back[0].setAttribute("type","")

    for i in range(0, len(record_front_back)):
        row_temp_fb = " ".join(record_front_back[i])
        rows_front_back[i].firstChild.data = row_temp_fb

    # 删除多余的row节点, 注意删除节点必须使用parentnode方式，这是目前唯一已知的方法
    for i in range(len(record_front_back),len(rows_front_back)):
        rows_front_back[i].parentNode.removeChild(rows_front_back[i])

    with open(AsebPath[8]+ '\\' + newname + '_OIM328' + '.xml', 'w') as fp_front_back:
        DOMTree_front_back.writexml(fp_front_back)                          # 注意这里write的时候要用fp这种已处理形式


    # 生成最终的map图
    shutil.copy(SourcePath + '\\FinalXmlTemplate\\' + 'FinalWaferTemplate.xml', AsebPath[8]+ '\\' + newname + '.xml')
    DOMTree_final = xml.dom.minidom.parse(AsebPath[8]+ '\\' + newname + '.xml')
    patterns_final = DOMTree_final.documentElement
    rows_final = patterns_final.getElementsByTagName("Row")

    # 更改各个代码的计数
    bin_final = patterns_final.getElementsByTagName("Bin")
    bin_final[0].setAttribute("BinCount", str(count_001))
    bin_final[2].setAttribute("BinCount", str(count_013))

    time_final = patterns_final.getElementsByTagName("Device")
    time_final[0].setAttribute("CreateDate", str(NowTime.tm_year)+str(NowTime.tm_mon)+str(NowTime.tm_mday)+str(NowTime.tm_hour)+str(NowTime.tm_min)+str(NowTime.tm_sec))

    for i in range(0, len(record_f)):
        row_temp = " ".join(record_f[i])
        rows_final[i].firstChild.data = row_temp

    # 删除多余的row节点, 注意删除节点必须使用parentnode方式，这是目前唯一已知的方法
    for i in range(len(record_f),len(rows_final)):
        rows_final[i].parentNode.removeChild(rows_final[i])

    with open(AsebPath[8]+ '\\' + newname + '.xml', 'w') as fp_final:
        DOMTree_final.writexml(fp_final)                          # 注意这里write的时候要用fp这种已处理形式
        print("最终xml生成成功")

#Recreate(r"C:\Users\Te390038\Desktop\test_wafer", r'C:\Users\Te390038\Documents\Source','aaa', '00000111', '00000222')
