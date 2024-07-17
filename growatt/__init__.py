import requests as re
import hashlib

class Growatt:
    
    def __init__(self):
        self.BASE_URL = "https://server.growatt.com"
        self.session = re.Session()

    def _hash_password(self, password: str) -> str:
        """
        Hashes the given password using MD5.

        Args:
            password (str): The plain text password to be hashed.

        Returns:
            str: The MD5 hash of the password.
        """
        return hashlib.md5(password.encode()).hexdigest()

    
    def login(self, username: str, password: str):
        """
        Logs in the user and saves the session.

        Args:
            username (str),
            password (str)

        Returns:
            Nothing, saves the session for later use.
        """
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

    def get_plants(self):
        """
        Retrieves the list of plants associated with the user.

        Returns:
            list: A list of dictionaries, each containing details about a plant.
            Example:
                [
                    {
                        'timezone': '1',
                        'id': '1234567',
                        'plantName': 'User Name'
                    },
                    ...
                ]
        """

        res = self.session.post(f"{self.BASE_URL}/index/getPlantListTitle")
        res.raise_for_status()

        try:
            json_res = res.json()

            if not json_res:
                raise ValueError("Empty response. Please ensure you are logged in.")
            return json_res
        except re.exceptions.JSONDecodeError:
            raise ValueError("Invalid response received. Please ensure you are logged in.")

    def get_plant(self, plantId: str):
        """
        Retrieves specific plant information by plantId.

        Args:
            plantId (str): The ID of the plant to retrieve.

        Returns:
            dict: A dictionary containing detailed plant information.
            Example:
                {
                    'country': 'Denmark',
                    'formulaCo2': '0.0',
                    'accountName': 'example@example.com',
                    'city': 'Sample City',
                    'timezone': '2',
                    'co2': '1234',
                    'creatDate': '2023-01-01',
                    'formulaCoal': '0.0',
                    'designCompany': '0',
                    'fixedPowerPrice': '1.2',
                    'id': '123456',
                    'lat': '55.000',
                    'valleyPeriodPrice': '1.0',
                    'tempType': '0',
                    'lng': '9.000',
                    'locationImg': 'null',
                    'tree': '100',
                    'peakPeriodPrice': '1.3',
                    'installMap': '',
                    'plantType': '0',
                    'nominalPower': '5000',
                    'formulaMoney': '0',
                    'formulaTree': '0.0',
                    'plantNmi': '',
                    'flatPeriodPrice': '1.1',
                    'eTotal': '5000.0',
                    'plantImg': '123456_image.jpg',
                    'isShare': 'false',
                    'coal': '1000.0',
                    'moneyUnit': 'usd',
                    'plantName': 'Sample Plant',
                    'moneyUnitText': 'USD'
                }
        """

        res = self.session.post(f"{self.BASE_URL}/panel/getPlantData?plantId={plantId}")
        res.raise_for_status()

        try:
            json_res = res.json()["obj"]

            if not json_res:
                raise ValueError("Empty response. Please ensure you are logged in.")
            return json_res
        except re.exceptions.JSONDecodeError:
            raise ValueError("Invalid response received. Please ensure you are logged in.")


    def get_mix_ids(self, plantId: str):
        """
        Retrieves the MIX id's by plantId.

        Args:
            plantId (str): The ID of the MIX id's to retrieve.

        Returns:
            list: A dictionary containing detailed plant information.
            Example:
                [['OICUJHP1PX', 'OICUJHP1PX', '0']]
        """
            

        res = self.session.post(f"{self.BASE_URL}/panel/getDevicesByPlant?plantId={plantId}")
        res.raise_for_status()

        try:
            json_res = res.json()['obj']["mix"]

            if not json_res:
                raise ValueError("Empty response. Please ensure you are logged in.")
            return json_res
        except re.exceptions.JSONDecodeError:
            raise ValueError("Invalid response received. Please ensure you are logged in.")

    def get_mix_total(self, plantId: str, mixSn: str):
        data = {
            'mixSn': str(mixSn),
        }
        res = self.session.post(f"{self.BASE_URL}/panel/mix/getMIXTotalData?plantId={plantId}", data=data)
        res.raise_for_status()

        try:
            json_res = res.json()["obj"]

            if not json_res:
                raise ValueError("Empty response. Please ensure you are logged in.")
            return json_res
        except re.exceptions.JSONDecodeError:
            raise ValueError("Invalid response received. Please ensure you are logged in.")
    
    def get_mix_status(self, plantId: str, mixSn: str):

        data = {
            'mixSn': mixSn
        }

        res = self.session.post(f"{self.BASE_URL}/panel/mix/getMIXStatusData?plantId={plantId}", data=data)
        res.raise_for_status()

        try:
            json_res = res.json()["obj"]

            if not json_res:
                raise ValueError("Empty response. Please ensure you are logged in.")
            return json_res
        except re.exceptions.JSONDecodeError:
            raise ValueError("Invalid response received. Please ensure you are logged in.")


