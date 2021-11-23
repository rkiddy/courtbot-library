
import requests
import json

"""A package for retreiving court calendar data from Santa Clara County, California"""

courts = [ 'Alameda',
           'Alpine',
           'Amador',
           'Butte',
           'Calaveras',
           'Colusa',
           'Contra Costa',
           'Del Norte',
           'El Dorado',
           'Fresno',
           'Glenn',
           'Humboldt',
           'Imperial',
           'Inyo',
           'Kern',
           'Kings',
           'Lake',
           'Lassen',
           'Los Angeles',
           'Madera',
           'Marin',
           'Mariposa',
           'Mendocino',
           'Merced',
           'Modoc',
           'Mono',
           'Monterey',
           'Napa',
           'Nevada',
           'Orange',
           'Placer',
           'Plumas',
           'Riverside',
           'Sacramento',
           'San Benito',
           'San Bernardino',
           'San Diego',
           'San Francisco',
           'San Joaquin',
           'San Luis Obispo',
           'San Mateo',
           'Santa Barbara',
           'Santa Clara',
           'Santa Cruz',
           'Shasta',
           'Sierra',
           'Siskiyou',
           'Solano',
           'Sonoma',
           'Stanislaus',
           'Sutter',
           'Tehama',
           'Trinity',
           'Tulare',
           'Tuolumne',
           'Ventura',
           'Yolo',
           'Yuba' ]

court_names = ["Civil",
               "Probate",
               "Family",
               "Juvenile",
               "Criminalhoj",
               "CriminalPaloAlto",
               "CriminalSouthCounty"]

class Court:

    def __init__(self, name, department):
        self.__name = name
        self.__dept = department

    def setDepartment(self, dept_name):
        self.__dept = dept_name

    def getDepartment(self):
        return self.__dept

class CourtAppearance:

    def __init__(self):
        self.__when = ''

    def __call__(self, court, appear_date, case_num):

        cases = get_list( court, appear_date )

        for case in cases:
            if case['caseNbr'] == case_num:
                return case

        return {}

    def setCourtName(self, name):
        self.__court_name = name

    def getCourtName(self):
        return self.__court_name

    court_name = property(getCourtName, setCourtName)

    def setWhen(self, appear_datetime):
        self.__when = appear_datetime

    def getWhen(self):
        return self.__when

    when = property(getWhen, setWhen)

    def setCaseNumber(self, case_number):
        self.__case_number = case_number

    def getCaseNumber(self):
        return self.__case_number

    case_number = property(getCaseNumber, setCaseNumber)

    def setParties(self, parties):
        self.__parties = parties

    def getParties(self):
        return self.__psrties

    parties = property(getParties, setParties)

    def setCourt(self, court_name, department):
        self.__court = Court(name, department)

    def getCourt(self):
        return self.__court

    court = property(getCourt, setCourt)

get_case = CourtAppearance()

class CourtAppearanceList:

    def __call__(self, court, appear_date, fetch=0):

        calendar_infos = []

        if court == 'Santa Clara':

            case_urls = []

            file_name = 'data/CA/Santa Clara/' + appear_date + '.json'

            if fetch == 0:

                data_file = open(file_name, 'r')

                if data_file == None:
                    raise Exception('Cannot find file: ' + file_name)

                calendar_infos = json.loads(data_file.read())

            if fetch == 1:

                for court_name in court_names:

                    depts = requests.get("https://portal.scscourt.org/api/calendar/" +
                                         court_name + "/" +
                                         appear_date + "/" + appear_date)

                    data = depts.json()['data']

                    for dept_info in data:
                        case_urls.append('https://portal.scscourt.org/api/calendardepartment/' +
                                         dept_info['courtroom'] + '/' +
                                         court_name + '/' +
                                         appear_date + '/' + appear_date)

                for case_url in case_urls:

                    cal = requests.get(case_url).json()

                for cal_entry in cal['data']:
                    cal_entry['court'] = court_name
                    cal_entry['created'] = cal['created']

                    calendar_infos.append(cal_entry)

                f = open(file_name, "w")

                f.write(json.dumps(calendar_infos))

                f.close()

        return calendar_infos

get_list = CourtAppearanceList()
