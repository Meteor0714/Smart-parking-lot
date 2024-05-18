import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import sys, time

cred = credentials.Certificate('utils/firebase/serviceAccountKey.json') 
default_app = firebase_admin.initialize_app(cred)

# Use a service account.

db = firestore.client()

#location_ref = db.collection("parking").document("badeRd")

class Parking:
    def __init__(self, Location = "def"): #初始化設定
        self.Location = Location  
        self.Location_ref = 0
        self.occupied = 0
        self.data = ""

    def update(self, Location = "def", field = "occupied", occupied = 10):
        if(~(field in self.data)):  #若資料庫沒有就加上
            self.data.setdefault(field, occupied)
            self.Location_ref.update({
                field: occupied
            })
        self.occupied = self.data[field]
        big = self.data[field] if (self.data[field] > occupied) else occupied     
        small = self.data[field] if (self.data[field] < occupied) else occupied
        if big == 0: 
            big +=1 
            small +=1
        print(f"field:{field} big = {big}  small = {small}  誤差:{100 - (small / big) * 100}")
        if(self.data[field] != occupied and (100 - (small / big) * 100) > 10):   #誤差超過10%
            try:
                if (self.Location != Location):  #若突然變換停車地點改變資料庫文件(尚未建置)
                    self.Location_ref = db.collection("parking").document(Location)
                self.Location_ref.update({
                    field: occupied,
                    u'update_time' : firestore.SERVER_TIMESTAMP
                })
                print(f"firebase updated 10% difference And Time")
                self.data[field] = occupied  #改變從資料庫抓下來的資料
            except:
                print(f"firebase update wrong")  #更新錯誤
        else:
            print(f"not update within error")   #未超過10%不更新
    
P = Parking(str)  #宣告CLASS

def update(Location = "def", field = "occupied", occupied = 10):    #外部呼叫

    d = {"still vacancies":1, "mistake":2, "many parking spaces":3, "few vacancies":4} #Area set
    if(type(occupied) == str and (occupied in d)): 
        occupied = d[occupied]
        print(occupied)
        if(occupied == 2): field = "mistake"
    
    d2 = {"bicycle": "bicycle", "motorcycle": "occupied"}
    if field in d2:
        field = d2[field]

    

    P.update(Location, field , occupied)                #呼叫Class方法

def check_location(Location):                   #確認Location正確
    doc_ref = db.collection(u"parking").stream()
    file = open("Buffer.txt", "w")
    for doc in doc_ref:
        #print(f'{doc.id} => {doc.to_dict()}') #輸出抓取到到的資料
        if doc.id == Location:
            P.data = doc.to_dict()  #讀取資料庫上的數據
            P.Location_ref = db.collection("parking").document(Location)  #連線到目標文件
            P.Location = Location
            localtime = time.localtime()   #獲取系統時間
            result = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
            file.writelines( [f"{doc.to_dict()} \n {result}"] )
            file.close
            print(f"find document  {Location}")
            return 1
    print(f"don't find document  {Location}")
    sys.exit(0)     #查無正確地點退出程式
    return 0        #查無正確地點退出程式
