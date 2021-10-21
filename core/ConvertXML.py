from xml.dom.minidom import parse
import xml.dom.minidom
import os
import re
import time
import shutil

def Convert(InputPath, SourcePath):

    IoName = ["\\Input"]
    ClassName = ["\\Manual_Xml"]

    # 放输入和输出xml文件的位置
    AsebPath = [
        InputPath+IoName[0]+ClassName[0],
        ]

    # 放资源文件路径的位置
    SocPath = [
        SourcePath + '\\FinalXmlTemplate\\FinalWaferTemplate.xml'
    ]

    for i in range(len(AsebPath)):
       folder = os.path.exists(AsebPath[i])

       if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
          os.makedirs(AsebPath[i])  # makedirs 创建文件时如果路径不存在会创建这个路径
          print("Create new folder")
          print("Create Successfully")
       else:
          print("Folder already exists")

    XML_list = os.listdir(AsebPath[0])

    if len(XML_list)>=1:
        for XML in XML_list:
            res = []
            newname = XML.split('.')[0] + '_Converted'
            if XML.endswith('.xml') and XML:
                # 从输入的xml获取数据
                # 使用minidom解析器打开xml文档, 注意，文件别加扩展名
                DOMTree = xml.dom.minidom.parse(AsebPath[0] + '\\' + XML)
                patterns = DOMTree.documentElement
                # 在集合中获取所有行
                rows = patterns.getElementsByTagName("ROW")       # 根据标签名获取
                for i in range(0,len(rows)):
                    row_mat = rows[i].firstChild.data.split()      # firstChild.data也可以用childnode[0]表示, split 以空格划分
                    res.append(row_mat)

                # 将数据放入新的map图
                count_001 = 0
                count_013 = 0
                for i in range(0,len(res)):
                    for j in range(0,len(res[0])):
                        if(res[i][j]=='00000062'):
                            res[i][j]='001'
                            count_001+=1
                        elif(res[i][j]=='00000000' or res[i][j]=='00000001'):
                            res[i][j]='099'
                        else:
                            res[i][j]='013'
                            count_013+=1

                # 生成最终的map图
                shutil.copy(SocPath[0], AsebPath[0]+ '\\' + newname + '.xml')
                DOMTree_final = xml.dom.minidom.parse(AsebPath[0]+ '\\' + newname + '.xml')
                patterns_final = DOMTree_final.documentElement
                rows_final = patterns_final.getElementsByTagName("Row")

                # 更改各个代码的计数
                bin_final = patterns_final.getElementsByTagName("Bin")
                bin_final[0].setAttribute("BinCount", str(count_001))
                bin_final[2].setAttribute("BinCount", str(count_013))

                NowTime = time.localtime(time.time())
                time_final = patterns_final.getElementsByTagName("Device")
                time_final[0].setAttribute("CreateDate", str(NowTime.tm_year)+str(NowTime.tm_mon)+str(NowTime.tm_mday)+str(NowTime.tm_hour)+str(NowTime.tm_min)+str(NowTime.tm_sec))

                for i in range(0, len(res)):
                    row_temp = " ".join(res[i])
                    rows_final[i].firstChild.data = row_temp

                # 删除多余的row节点, 注意删除节点必须使用parentnode方式，这是目前唯一已知的方法
                for i in range(len(res),len(rows_final)):
                    rows_final[i].parentNode.removeChild(rows_final[i])

                with open(AsebPath[0]+ '\\' + newname + '.xml', 'w') as fp_final:
                    DOMTree_final.writexml(fp_final)                          # 注意这里write的时候要用fp这种已处理形式
            else:
                print('No XML File')
    else:
        print('Need One More Xml Files')


#Convert(r'C:\Users\Te390038\Desktop\test_wafer_12',r'C:\Users\Te390038\Documents\Source','dda')
