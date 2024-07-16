import requests as re
import hashlib

class Growatt:
    
    def __init__(self):
        self.BASE_URL = "https://server.growatt.com"
        self.session = re.Session()

    def _hash_password(self, password: str) -> str:
        return hashlib.md5(password.encode()).hexdigest()

    def login(self, username: str, password: str):
        self.username = username
        self.password = password

        self.session.post(
            f"{self.BASE_URL}/login",
            data={
                "account": username,
                "password": "",
                "validateCode": "",
                "isReadPact": 0,
                "passwordCrc": self._hash_password(self.password)
            },
            headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        )

    def getPlantListTitle(self):
        res = self.session.post(f"{self.BASE_URL}/index/getPlantListTitle")
        return res.json()
    
    def getPlantTopic(self, plantId: str):
        data = {
            'plantId': plantId
        }
        res = self.session.post(f"{self.BASE_URL}/index/getPlantTopic", data=data)
        return res.json()
    
    def getDevicesByPlantList(self, page: str, plantId: str):
        data = {
            'currPage': str(page),
            'plantId': str(plantId)
        }
        res = self.session.post(f"{self.BASE_URL}/panel/getDevicesByPlantList", data=data)
        return res.json()
    
    def getMIXStatusData(self, plantId: str, mixSn: str):

        data = {
            'mixSn': mixSn
        }

        res = self.session.post(f"{self.BASE_URL}/panel/mix/getMIXStatusData?plantId={plantId}", data=data)
        return res.json()

