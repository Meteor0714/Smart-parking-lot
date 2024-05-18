import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./utils/firebase/serviceAccountKey.json') 
default_app = firebase_admin.initialize_app(cred)

# Use a service account.

db = firestore.client()

badeRd_ref = db.collection("parking").document("badeRd")

class Parking:
    def __init__(self, Location = "def", occupied=20):
        self.Location = Location
        self.occupied = occupied
        try:
            badeRd_ref.update({
            "occupied": "null"
            })
        except:
            print(f"firebase initialzation wrong")
        pass

    def update(self, Location = "def", occupied = 20):
        big = self.occupied if (self.occupied > occupied) else occupied
        small = self.occupied if (self.occupied < occupied) else occupied
        print(f"big = {big}  small = {small}")
        if(self.occupied != occupied and (small / big) * 100 > 10 ):
            try:
                badeRd_ref = db.collection("parking").document(Location)
                badeRd_ref.update({
                    "occupied": occupied
                })
                print(f"firebase updated 10% difference")
                self.occupied = occupied
            except:
                print(f"firebase update wrong")
        else:
            print(f"not update within error")
    
P = Parking(str, 20)  #宣告CLASS

def update(Location = "def", occupied = 20):    #外部呼叫
    P.update(Location, occupied)                #呼叫Class方法



