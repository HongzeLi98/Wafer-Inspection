import time
import sys
import serial
from PIL import ImageGrab
import CreateXMLbyOrder
import os


def shot_by_order(projectpath, sourcepath, wafername, direction, com, x1, y1, x2, y2, timeslot):
    # 参数说明：xml模板，wafer批次，截图区域坐标, 截图时间
    # 所有创建文件夹的操作都在UI界面进行
    # 注意在不同的电脑上端口号未必是com3，需要打开设备管理器确认，注意要大写
    Type = ['Back', 'Front']
    XmlPath = sourcepath + '/'
    ImgPath = projectpath + '/Input/' + Type[direction] + '/'
    XmlDir = os.listdir(XmlPath)
    com = serial.Serial(com, 9600)
    time.sleep(5)

    if len(XmlDir) == 1:
        for name in XmlDir:
            if name.endswith('.xml'):
                XmlPath = XmlPath + name
                ImgOrder = CreateXMLbyOrder.CreateXML_byOrder(XmlPath)
                ImgNumber = len(ImgOrder)
                for i in range(ImgNumber):
                    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                    # 列在前，行在后
                    img.save(ImgPath + wafername + '_' + str(ImgOrder[i][1]) + '_' + str(ImgOrder[i][0]) + '.jpg')
                    push_bytes = com.write(b'\x55\x01\x06\x01\x00\x5D')
                    time.sleep(timeslot)
                    pop_bytes = com.write(b'\x55\x01\x06\x02\x00\x5E')
            else:
                print('No XML File!')
    else:
        print('Need Only One XML File!')

#shot_by_order('D:\\ScreenShot_Qt_test', r'C:\Users\Hongze\Documents\WeChat Files\wxid_j3kngrdf4tgf22\FileStorage\File\2020-12\AI_before_package\Source', 'cell_9Y1925_23_B', 0, 0, 800, 800, 1)
