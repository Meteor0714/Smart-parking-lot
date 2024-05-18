import os,cv2,time
from threading import Thread
import logging
import utils.torch_utils
#from utils.datasets import LoadStreams, LoadImages

os.system(f"cd {os.getcwd()}")

count = 0  #計算有幾個停車場
failer = 0 #計算錯誤次數(如果三次檢查都有錯誤就會修復線程)
data = {}
f = open('IPCAM\capLoad.txt', 'r')

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename = "logfile.log",
                    filemode = "w",
                    format = Log_Format,
                    level = logging.INFO)
logger = logging.getLogger("autoRun")
logger.info(f"Program start")

while(True):
    line = f.readline().strip()
    if not line:
        break
    strings = line.split(' ')
    if strings[1] == '1':
        data.setdefault(count, strings[0])
        print(count, strings[0])
        count+=1

def Run(location, B):
    os.system(f'python detect.py --weights runs/train\yolov7_Max3/best.pt --source 0 --device cpu --view-img --save-txt --save-conf --conf 0.45  --location {location} --wait_time 10')
    #os.system(f'python detect.py --weights runs/train\yolov7_Max4/best.pt --source 0 --device cpu --view-img --save-txt --save-conf --conf 0.45  --location {location} --wait_time 10')

thread = [None] * count
for i in range(count):
    thread[i] = Thread(target=Run, args=([data[i], 0]), daemon=True)
    thread[i].start()
    logger.info(f"{data[i]} start in {thread[i]}")

while(True):
    fail = 0
    start_list = [None] *count
    for i in range(count):  #檢查子線程有沒有在工作
        if(thread[i].is_alive()):
            print(thread[i])
        else:
            fail+=1
            print(f"on {thread[i]}")
            logger.error(f"Thread is closed {data[i]} failer:{failer+1}")
            start_list[i] = thread[i]

    if fail!=0 and failer==2:  #子線程運作錯誤
        failer = 0
        if fail == count:  #攝影機全部錯誤
            logger.error("All cameras have failed, please check whether it is the local network or the camera is faulty.")
            for i in range(count):
                thread[i].join()
            os._exit()
        else:    #攝影機部份錯誤
            fail = 0
            for i in range(count):
                if start_list[i] != None:
                    thread[i] = Thread(target=Run, args=([data[i], 0]), daemon=True)
                    thread[i].start()
                    logger.info(f"Thread attempts to restart {data[i]}")
    else: fail == 0 #子執行緒沒有斷線就清空計數
    if fail !=0: #如果攝影機有錯誤將錯誤+1
        failer+=1
    time.sleep(10)
