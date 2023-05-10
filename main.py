
import requests,createTables
import databaseManager as dM

class Scraper:

    def __init__(self) -> None:
        self.headers =  {
            'authority': 'v2api.novaindex.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,pl-PL;q=0.8,pl;q=0.7,de;q=0.6',
            'origin': 'https://novaindex.com',
            'referer': 'https://novaindex.com/',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        }

    def checkExist(self,response):
        keys = ['name', 'phone', 'address', 'zipcode', 'city','website','email']

        data = []
        for key in keys:
            value = response[key]
            if value == None:data.append('None')
            else:data.append(value)

        return data



    def getUser(self,path):

        params = {
        'path': f'{path}',
        }

        response = requests.get('https://v2api.novaindex.com/route/lookup', params=params, headers=self.headers)
        try:
            data = self.checkExist(response.json()['data'])
        except:return False
        return data



    def getCompanies(self,page):
        params = {
            'page': str(page),
            'query': 'indretningsarkitekter',
        }
        status_code = 500
        retry = 0
        while status_code != 200:
            if retry == 6:
                print('page',page,'skipped')
                return False
            response = requests.get('https://v2api.novaindex.com/search', params=params, headers=self.headers)

            status_code = response.status_code
            retry+=1

        try:return response.json()['companies']
        except: return None

page = 1

scraper = Scraper()



while page < 268:
    print('page',page)
    current_comapanies = []
    
    companies = scraper.getCompanies(page)

    if companies in [None,False]:
        page+=1
        continue

    for c in companies:
        data = scraper.getUser(c['path'])
        if data == False:continue
        data.append(c['path'].replace('/',''))
        current_comapanies.append(tuple(data))
    
    dM.addUsers(current_comapanies)


    
    page+=1

dM.exportDB()


