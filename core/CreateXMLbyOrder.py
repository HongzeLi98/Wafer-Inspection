# 根据当前拍到第几张图片，确定行列位置
# 默认扫描方式为从左下开始，S型扫描
# Date: 0701

from xml.dom.minidom import parse
import xml.dom.minidom
import time
import os
import shutil

def CreateXML_byOrder(PathXml):
    # ShotInfo为1*3098数组，代表拍照图像信息
    # PathXml为xml文件路径

    # 使用minidom解析器打开xml文档, 注意，文件别加扩展名
    DOMTree = xml.dom.minidom.parse(PathXml)
    patterns = DOMTree.documentElement

    # 在集合中获取所有行
    rows = patterns.getElementsByTagName("ROW")       # 根据标签名获取

    NowTime = time.localtime(time.time())
    History = patterns.getElementsByTagName("INSPECTION")       # 根据标签名获取
    History[0].setAttribute("day", str(NowTime.tm_mday))
    History[0].setAttribute("month", str(NowTime.tm_mon))
    History[0].setAttribute("year", str(NowTime.tm_year))
    History[0].setAttribute("operator","")
    History[0].setAttribute("type","")

    ImgOrder = []
    FirstLine = 0
    ProductInfo = []

    for i in range(len(rows)):
        row_mat = rows[i].firstChild.data.split()      # firstChild.data也可以用childnode[0]表示, split 以空格划分
        ProductInfo.append(row_mat)


    # 图片拍摄顺序是从左下角开始，先向上
    # 将ProductInfo转置,注意行列位置变化了
    ProductInfoT = list(map(list, zip(*ProductInfo)))


    for i in range(len(ProductInfoT)):
        if len(ImgOrder) > 0:
            FirstLine += 1
        row_mat = ProductInfoT[i]
        if FirstLine%2 == 0:
            for j in range(len(row_mat)):
                if row_mat[len(row_mat)-j-1][-2:] == '22' or row_mat[len(row_mat)-j-1][-2:] == '62':
                    ImgOrder.append([len(row_mat)-j-1,i])
        else:
            for j in range(len(row_mat)):
                if row_mat[j][-2:] == '22' or row_mat[j][-2:] == '62':
                    ImgOrder.append([j,i])

    return ImgOrder
