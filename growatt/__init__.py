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
                        'plantName': 'name'
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
        """
        Retrieves the total measurements from specific MIX.

        Args:
            plantId (str): The ID of the plant.
            mixSn (str): The ID of the MIX.

        Returns:
            list: A dictionary containing total mix information.
            Example:
                {
                "eselfToday": "7.4",
                "gridPowerTotal": "2743",
                "eselfTotal": "3428",
                "elocalLoadToday": "12.6",
                "gridPowerToday": "5.2",
                "elocalLoadTotal": "6171",
                "eexTotal": "0",
                "photovoltaicRevenueToday": "37.3",
                "eexToday": "0",
                "etoGridToday": "18.2",
                "edischarge1Total": "1600.5",
                "photovoltaicRevenueTotal": "7338.4",
                "unit": "kr",
                "edischarge1Today": "0.4",
                "epvToday": "31.1",
                "epvTotal": "6115.3",
                "etogridTotal": "2568.6"
                }
        """
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
        """
        Retrieves the current status of measurements from specific MIX.

        Args:
            plantId (str): The ID of the plant.
            mixSn (str): The ID of the MIX.

        Returns:
            list: A dictionary containing the current status of mix information.
            Example:
                    {
                    "pdisCharge1": 0,
                    "uwSysWorkMode": "5",
                    "pactouser": 0,
                    "vBat": "53.1",
                    "vAc1": "236.7",
                    "priorityChoose": "0",
                    "lost": "mix.status.normal",
                    "pactogrid": 0.34,
                    "pLocalLoad": 0.84,
                    "vPv2": "252.9",
                    "deviceType": "2",
                    "pex": 0,
                    "chargePower": 0,
                    "vPv1": "256.7",
                    "upsVac1": "0",
                    "SOC": "95",
                    "wBatteryType": "1",
                    "pPv2": "615.6",
                    "fAc": "50.02",
                    "vac1": "236.7",
                    "pPv1": "568.4",
                    "storagePpv": "1.18",
                    "upsFac": "0",
                    "ppv": 1.18,
                    "status": "5"
                    }
        """

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
    
    def get_energy_stats_daily(self, date: str, plantId: str, mixSn: str):
        """
        Fetch daily energy statistics.

        Parameters:
        date (str): The date for the energy statistics in 'YYYY-MM-DD' format.
        plantId (str): The ID of the plant.
        mixSn (str): The serial number of the mix device.

        Example:
        api.get_energy_stats_daily(date="2024-07-28", plantId="1234567", mixSn="ODCUTJF8IFP")

        Returns:
            list: A JSON object that contains periodic data for the given day.
            Example:

        {
            "result": 1,
            "obj": {
            "etouser": "5.2",
            "charts": {
            "pex": [LIST],
            "pacToGrid": [LIST],
            "pcharge": [LIST],
            "ppv": [LIST],
            "sysOut": [LIST],
            "pself": [LIST],
            "elocalLoad": [LIST],
            "pdischarge": [LIST],
            "pacToUser": [LIST]
            },
            "eCharge": "25.7",
            "eAcCharge": "18.3",
            "eChargeToday2": "7.4",
            "elocalLoad": "12.6",
            "eChargeToday1": "7.4"
            }
        }
        """

        data = {
            "date": date,
            "plantId": str(plantId),	
            "mixSn": mixSn
        }

        res = self.session.post(f"{self.BASE_URL}/panel/mix/getMIXEnergyDayChart", data=data)
        res.raise_for_status()

        try:
            json_res = res.json()

            if not json_res:
                raise ValueError("Empty response. Please ensure you are logged in.")
            return json_res
        except re.exceptions.JSONDecodeError:
            raise ValueError("Invalid response received. Please ensure you are logged in.")
        
    def get_energy_stats_monthly(self, date: str, plantId: str, mixSn: str):
        """
        Fetch monthly energy statistics.

        Parameters:
        date (str): The date for the energy statistics in 'YYYY-MM' format.
        plantId (str): The ID of the plant.
        mixSn (str): The serial number of the mix device.

        Example:
        api.get_energy_stats_daily(date="2024-07", plantId="1234567", mixSn="ODCUTJF8IFP")

        Returns:        
            list: A JSON object that contains periodic data for the given month.
            Example:

        {
            "result": 1,
            "obj": {
            "etouser": "5.2",
            "charts": {
            "pex": [LIST],
            "pacToGrid": [LIST],
            "pcharge": [LIST],
            "ppv": [LIST],
            "sysOut": [LIST],
            "pself": [LIST],
            "elocalLoad": [LIST],
            "pdischarge": [LIST],
            "pacToUser": [LIST]
            },
            "eCharge": "25.7",
            "eAcCharge": "18.3",
            "eChargeToday2": "7.4",
            "elocalLoad": "12.6",
            "eChargeToday1": "7.4"
            }
        }
        """

        data = {
            "date": date,
            "plantId": str(plantId),	
            "mixSn": mixSn
        }

        res = self.session.post(f"{self.BASE_URL}/panel/mix/getMIXEnergyMonthChart", data=data)
        res.raise_for_status()

        try:
            json_res = res.json()

            if not json_res:
                raise ValueError("Empty response. Please ensure you are logged in.")
            return json_res
        except re.exceptions.JSONDecodeError:
            raise ValueError("Invalid response received. Please ensure you are logged in.")
        
    def get_energy_stats_yearly(self, year: str, plantId: str, mixSn: str):
        """
        Fetch yearly energy statistics.

        Parameters:
        year (str): The year for the energy statistics in 'YYYY' format.
        plantId (str): The ID of the plant.
        mixSn (str): The serial number of the mix device.

        Example:
        api.get_energy_stats_daily(year="2024", plantId="1234567", mixSn="ODCUTJF8IFP")


        Returns:        
            list: A JSON object that contains periodic data for the given year.
            Example:

        {
            "result": 1,
            "obj": {
            "etouser": "5.2",
            "charts": {
            "pex": [LIST],
            "pacToGrid": [LIST],
            "pcharge": [LIST],
            "ppv": [LIST],
            "sysOut": [LIST],
            "pself": [LIST],
            "elocalLoad": [LIST],
            "pdischarge": [LIST],
            "pacToUser": [LIST]
            },
            "eCharge": "25.7",
            "eAcCharge": "18.3",
            "eChargeToday2": "7.4",
            "elocalLoad": "12.6",
            "eChargeToday1": "7.4"
            }
        }
        """
        data = {
            "year": year,
            "plantId": str(plantId),	
            "mixSn": mixSn
        }

        res = self.session.post(f"{self.BASE_URL}/panel/mix/getMIXEnergyYearChart", data=data)
        res.raise_for_status()

        try:
            json_res = res.json()

            if not json_res:
                raise ValueError("Empty response. Please ensure you are logged in.")
            return json_res
        except re.exceptions.JSONDecodeError:
            raise ValueError("Invalid response received. Please ensure you are logged in.")


    def get_energy_stats_total(self, year: str, plantId: str, mixSn: str):
        """
        Fetch total energy statistics.

        Parameters:
        year (str): The year for the total energy statistics in 'YYYY' format.
        plantId (str): The ID of the plant.
        mixSn (str): The serial number of the mix device.

        Example:
        api.get_energy_stats_daily(year="2024", plantId="1234567", mixSn="ODCUTJF8IFP")

        Returns:        
            list: A JSON object that contains total periodic data.
            Example:

        {
            "result": 1,
            "obj": {
            "etouser": "5.2",
            "charts": {
            "pex": [LIST],
            "pacToGrid": [LIST],
            "pcharge": [LIST],
            "ppv": [LIST],
            "sysOut": [LIST],
            "pself": [LIST],
            "elocalLoad": [LIST],
            "pdischarge": [LIST],
            "pacToUser": [LIST]
            },
            "eCharge": "25.7",
            "eAcCharge": "18.3",
            "eChargeToday2": "7.4",
            "elocalLoad": "12.6",
            "eChargeToday1": "7.4"
            }
        }
        """

        data = {
            "year": year,
            "plantId": str(plantId),	
            "mixSn": mixSn
        }

        res = self.session.post(f"{self.BASE_URL}/panel/mix/getMIXEnergyTotalChart", data=data)
        res.raise_for_status()

        try:
            json_res = res.json()

            if not json_res:
                raise ValueError("Empty response. Please ensure you are logged in.")
            return json_res
        except re.exceptions.JSONDecodeError:
            raise ValueError("Invalid response received. Please ensure you are logged in.")
        
    def get_weekly_battery_stats(self, plantId: str, mixSn: str):
        '''
        Fetch the daily charge and discharge of your battery within the last 7 days.

        Parameters:
        plantId (str): The ID of the plant.
        mixSn (str): The serial number of the mix device.

        Returns:
            Example:
            {
                "result": 1,
                "obj": {
                    "date": "2024-08-06",
                    "cdsTitle": [
                    "2024-07-31",
                    "2024-08-01",
                    "2024-08-02",
                    "2024-08-03",
                    "2024-08-04",
                    "2024-08-05",
                    "2024-08-06"
                    ],
                    "batType": 1,
                    "socChart": {
                    "soc": [LIST]
                    },
                    "cdsData": {
                    "cd_charge": [LIST],
                    "cd_disCharge": [LIST]
                    }
                }
            }
        '''

        data = {
            "plantId": plantId,	
            "mixSn": mixSn
        }

        res = self.session.post(f"{self.BASE_URL}/panel/mix/getMIXBatChart", data=data)
        res.raise_for_status()

        try:
            json_res = res.json()

            if not json_res:
                raise ValueError("Empty response. Please ensure you are logged in.")
            return json_res
        except re.exceptions.JSONDecodeError:
            raise ValueError("Invalid response received. Please ensure you are logged in.")


