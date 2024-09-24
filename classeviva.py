import requests
import json
import re
import locale
from datetime import datetime

class CT:
    DEFAULT = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    CYAN = '\033[36m'

    BALD = '\033[1m'
    REVERSED = '\033[7m'


class User:
    def __init__(self, uid:str, pwd: str):
        self.uid = uid      # Username / Email
        self.pwd = pwd      # Password
        self.ident = ''     # Identification String
        self.token = ''     # Access Token

        locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8') # Sets the default time language to Italian

    def to_json(self):
        return {"uid": self.uid, "pwd": self.pwd, "ident": self.ident, "token": self.token}
        
    # logs in the current user to allow for requests
    def login(self):
        if self.token != '':     # If the user is already logged in -> return
            return
        
        headers = self.get_headers()    # Gets default headers (without token)
        
        payload = json.dumps({"ident": None, "pass": self.pwd, "uid": self.uid})    # Login data
        response = requests.post(RequestURLs.LOGIN_URL, headers=headers, data=payload)     # Requests the login with default headers and login data

        if response.status_code == 200:     # If the request is successful
            data = response.json()

            self.ident = re.search(r'\d+', data['ident']).group()
            self.token = data['token']
        
            print(f"{CT.GREEN}Logged successfully{CT.DEFAULT}")
            return response.json()
        else:
            error = response.json()

            print(f"{CT.RED}Error while logging in ({error['statusCode']}): {CT.DEFAULT}{error['error']} - {error['info']}{CT.DEFAULT}")
            return response.json()
        
    # request data from a specific endpoint, given specific parameters such as ident(mandatory), and others
    def request(self, request_url: dict, params: tuple = ()):
        if not self.token:      # If the user does NOT have a token, so it is NOT logged in -> return
            print(f"{CT.RED}User is not logged in!{CT.DEFAULT}")
            return False
        
        args = (self.ident, )   # Initializes the request arguments as a tuple with user ident
        if len(params) > 0:    # If parameters are given -> add them to the request arguments
            args += params

        headers = self.get_headers()  # Gets default headers
        request_url["url"] = request_url["url"].format(*args)
        response = requests.request(url=request_url["url"], method=request_url["method"], headers=headers)

        if response.status_code == 200:
            return {"request": request_url, "data": response.json()}
        else:
            error = response.json()

            print(f"{CT.RED}Error while requesting data ({error['statusCode']}): {CT.DEFAULT}{error['error']} - {error['message']}{CT.DEFAULT}")
            return response.json()


    def get_headers(self):
        if not self.token:
            return {
                "User-Agent": "CVVS/std/4.1.7 Andorid/12",
                "Content-Type": "application/json",
                "Z-Dev-ApiKey": "Tg1NWEwNGIgIC0K"
            }
        else:
            return {
                "User-Agent": "CVVS/std/4.1.7 Andorid/12",
                "Content-Type": "application/json",
                "Z-Dev-ApiKey": "Tg1NWEwNGIgIC0K",
                "Z-Auth-Token": self.token
            }
        
    def print_prettify_output(self, data: json):
        if data["request"] == RequestURLs.NOTICEBOARD_URL:
            print(f"\n\n{CT.CYAN}{CT.BALD}{CT.REVERSED}===== Notice Board ====={CT.DEFAULT}")

            valid_items = []
            invalid_items = []
            for item in data["data"]["items"]:
                if item["cntValidInRange"] == True:
                    valid_items.append(item)
                else:
                    invalid_items.append(item)  


            print(f"{CT.CYAN}{CT.BALD}-> Valid Notices{CT.DEFAULT}")
            for item in valid_items:
                date = datetime.fromisoformat(item['pubDT']).strftime("%d %B %Y").upper()
                    
                if item["readStatus"] == False:
                    print(f"{CT.BALD}", end='')

                if item["cntCategory"] != "":
                    print(f"\t{CT.CYAN}[{item['cntCategory']}] {CT.GREEN}{item['cntTitle']} {CT.DEFAULT}- {date}{CT.DEFAULT}")
                else:
                    print(f"\t{CT.CYAN}[Comunicazione] {CT.GREEN}{item['cntTitle']} {CT.DEFAULT}- {date}{CT.DEFAULT}")

            print(f"\n{CT.RED}{CT.BALD}-> Expired Notices{CT.DEFAULT}")
            for item in invalid_items:
                date = datetime.fromisoformat(item['pubDT']).strftime("%d %B %Y").upper()
                    
                if item["readStatus"] == False:
                    print(f"{CT.BALD}", end='')

                if item["cntCategory"] != "":
                    print(f"\t{CT.CYAN}[{item['cntCategory']}] {CT.RED}{item['cntTitle']} {CT.DEFAULT}- {date}{CT.DEFAULT}")
                else:
                    print(f"\t{CT.CYAN}[Comunicazione] {CT.RED}{item['cntTitle']} {CT.DEFAULT}- {date}{CT.DEFAULT}")
        
        elif data["request"] == RequestURLs.SUBJECTS_URL:
            print(f"\n\n{CT.CYAN}{CT.BALD}{CT.REVERSED}===== Subjects ====={CT.DEFAULT}")
            for subject in data["data"]["subjects"]:
                print(f"{CT.CYAN}{CT.BALD}{subject['description']}: {CT.DEFAULT}", end="")
                for idx, teacher in enumerate(subject["teachers"]):
                    if idx < len(subject["teachers"]) - 1:
                        print(f"{teacher['teacherName']}", end=", ")
                    else:
                        print(f"{teacher['teacherName']}")
        
        elif data["request"] == RequestURLs.CARD_URL:
            card = data["data"]["card"]

            print(f"\n\n{CT.CYAN}{CT.BALD}{CT.REVERSED}===== Card ====={CT.DEFAULT}")
            print(f"{CT.CYAN}{CT.BALD}First Name: {CT.DEFAULT}{card['firstName']}")
            print(f"{CT.CYAN}{CT.BALD}Last Name: {CT.DEFAULT}{card['lastName']}")
            print(f"{CT.CYAN}{CT.BALD}Birth Date: {CT.DEFAULT}{datetime.fromisoformat(card['birthDate']).strftime('%d %B %Y').upper()}")
            print(f"{CT.CYAN}{CT.BALD}Ident: {CT.DEFAULT}{card['ident']}")
            print(f"{CT.CYAN}{CT.BALD}School Name: {CT.DEFAULT}{card['schName']}{card['schDedication']}")
            print(f"{CT.CYAN}{CT.BALD}School City: {CT.DEFAULT}{card['schCity']} ({card['schProv']})")
        
        elif data["request"] == RequestURLs.PERIODS_URL:
            print(f"\n\n{CT.CYAN}{CT.BALD}{CT.REVERSED}===== Periods ====={CT.DEFAULT}")
            for period in data["data"]["periods"]:
                print(f"{CT.CYAN}{CT.BALD}-> {period['periodDesc']}{CT.DEFAULT}")
                print(f"\t{CT.CYAN}Start: {CT.DEFAULT}{datetime.fromisoformat(period['dateStart']).strftime('%d %B %Y').upper()}{CT.DEFAULT}")
                print(f"\t{CT.CYAN}End: {CT.DEFAULT}{datetime.fromisoformat(period['dateEnd']).strftime('%d %B %Y').upper()}{CT.DEFAULT}")
        
        elif data["request"] == RequestURLs.SCHOOLBOOKS_URL:
            print(f"\n\n{CT.CYAN}{CT.BALD}{CT.REVERSED}===== School Books ====={CT.DEFAULT}")
            total = 0
            for book in data["data"]["schoolbooks"][0]["books"]:
                total += book['price']
                print(f"{CT.CYAN}{CT.BALD}{book['title']} {CT.DEFAULT}{CT.CYAN}(€{book['price']}0){CT.DEFAULT} - {book['subjectDesc']} ({book['isbnCode']})")

            total = round(total, 2)
            print(f"{CT.CYAN}{CT.BALD}Total Cost: {CT.DEFAULT}€{total}0")
        elif data["request"] == RequestURLs.AGENDA_URL:
            print(f"\n\n{CT.CYAN}{CT.BALD}{CT.REVERSED}===== Agenda ====={CT.DEFAULT}")
            for event in data["data"]["agenda"]:
                if event['notes'] != "":
                    print(f"{CT.CYAN}{CT.BALD}{datetime.fromisoformat(event['evtDatetimeBegin']).strftime('%d %B %Y, %H:%M').upper()}-{datetime.fromisoformat(event['evtDatetimeEnd']).strftime('%H:%M').upper()} {CT.DEFAULT}{CT.CYAN}({event['authorName']}) - {CT.DEFAULT}{event['notes']}{CT.DEFAULT}")
        elif data["request"] == RequestURLs.TODAY_LESSONS_URL:
            print(f"\n\n{CT.CYAN}{CT.BALD}{CT.REVERSED}===== Today's Lessons ====={CT.DEFAULT}")
            for lesson in data["data"]["lessons"]:
                if lesson['lessonArg'] != "":
                    print(f"{CT.CYAN}{CT.BALD}{lesson['subjectDesc']} {CT.DEFAULT}{CT.CYAN}({lesson['lessonType']}) - {CT.DEFAULT}{lesson['lessonArg']}{CT.DEFAULT}")
        elif data["request"] == RequestURLs.LESSONS_URL:
            print(f"\n\n{CT.CYAN}{CT.BALD}{CT.REVERSED}===== Lessons ====={CT.DEFAULT}")
            for lesson in data["data"]["lessons"]:
                if lesson['lessonArg'] != "":
                    print(f"{CT.CYAN}{CT.BALD}{lesson['subjectDesc']} {CT.DEFAULT}{CT.CYAN}({lesson['lessonType']}) - {CT.DEFAULT}{lesson['lessonArg']}{CT.DEFAULT}")

        else:
            print(data["data"])

class RequestURLs:    
    BASE_URL: str = 'https://web.spaggiari.eu/rest/v1'
    STUDENTS_URL: str = f'{BASE_URL}/students/{{}}'
    LOGIN_URL: str = f'{BASE_URL}/auth/login'

    ABSENCES_URL: dict = {"url": f'{STUDENTS_URL}/absences/details', "method": 'GET'}
    AGENDA_URL: dict = {"url": f'{STUDENTS_URL}/agenda/all/{{}}/{{}}', "method": 'GET'} # Data Inizio (YYYYMMDD) / Data Fine (YYYYMMDD)
    SUBJECTS_URL: dict = {"url": f'{STUDENTS_URL}/subjects', "method": 'GET'}
    GRADES_URL: dict = {"url": f'{STUDENTS_URL}/grades', "method": 'GET'}
    TODAY_LESSONS_URL: dict = {"url": f'{STUDENTS_URL}/lessons/today', "method": 'GET'}
    LESSONS_URL: dict = {"url": f'{STUDENTS_URL}/lessons/{{}}', "method": 'GET'} # Data (YYYYMMDD)
    NOTES_URL: dict = {"url": f'{STUDENTS_URL}/notes/all', "method": 'GET'}
    PERIODS_URL: dict = {"url": f'{STUDENTS_URL}/periods', "method": 'GET'}
    DIDACTICS_URL: dict = {"url": f'{STUDENTS_URL}/didactics', "method": 'GET'}
    CARD_URL: dict = {"url": f'{STUDENTS_URL}/card', "method": 'GET'}
    CALENDAR_URL: dict = {"url": f'{STUDENTS_URL}/calendar/all', "method": 'GET'}
    SCHOOLBOOKS_URL: dict = {"url": f'{STUDENTS_URL}/schoolbooks', "method": 'GET'}
    NOTICEBOARD_URL: dict = {"url": f'{STUDENTS_URL}/noticeboard', "method": 'GET'}

    DOCUMENTS: dict = {"url": f'{STUDENTS_URL}/documents', "method": 'POST'}
