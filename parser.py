import requests
import lxml.html
import re
import sqlite3

# base_url = 'https://www.work.ua'




# rez = requests.post('https://www.work.ua/jobs/2991081/ajax/get-jobs-data/',data={},headers={'User-Agent': user_agents[0]})
# print(rez.json())





class WorkUa:
    def __init__(self,base_url):
        self.base_url = base_url
        self.user_agents = ["Google Chrome 53 (Win 10 x64): Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36", 
                           "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"]
        self.conn = sqlite3.connect('info_work.db')
        self.cur =  self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF not EXISTS work
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    link text,
                    title text, 
                    sel text,
                    kompani text,
                    time text,
                    phone text
                    )"""


            )



    def get_info(self):

        page = 1
        flag = True
        cards = []
        while flag:
            url = '{0}/jobs-rivne-it/?advs=1&page={1}'.format(self.base_url,page)
            rez = requests.get(url,headers={'User-Agent': self.user_agents[0]})
            if rez.status_code==200:
                dom = lxml.html.fromstring(rez.text)
                divs = dom.xpath("//div[@class='card card-hover card-visited wordwrap job-link']")
                flag = len(divs)!=0

                for div in divs:

                    a_s = div.xpath('h2/a')
                    div_bs =div.xpath('div/b')
                    times = div.xpath('div[@class="pull-right"]/span[@class="text-muted small"]')
                    kompani_divs = div.xpath('div[@class="add-top-xs"]')
                    for a,div_b,time,kompani_div in zip(a_s,div_bs,times,kompani_divs):
                        kompani = kompani_div.xpath('span')
                        if kompani:
                            kompani = kompani[0]

                        cards.append(
                                {
                                    'link':self.base_url+a.attrib.get('href'),
                                    'title':a.text_content(),
                                    'sel':div_b.text_content(),
                                    'kompani':kompani.text_content(),
                                    'time':time.text_content()
                                }
                        )
            else:
                print('Error', rez.status_code)

            page = page + 1
        
# link text,
#                     title text, 
#                     sel text,
#                     kompani text,
#                     time text,
#                     phone text
        sql_insert = """
        INSERT INTO work (link,title,sel,kompani,time,phone) VALUES(?,?,?,?,?,?) 
        """
        for card in cards:
            rez = requests.get(card['link'],headers={'User-Agent': self.user_agents[0]})
            if rez.status_code==200:
                dom = lxml.html.fromstring(rez.text)
                tel = dom.xpath("//span[@id='contact-phone']")
                if tel:
                    tel_info = requests.post('{0}ajax/get-jobs-data/'.format(card['link']),data={},headers={'User-Agent': self.user_agents[0]})
                    if tel_info.status_code == 200:
                        contactPhone = tel_info.json().get('contactPhone')
                        contactPhone = re.sub(r'[-\(\)+]','',contactPhone)
                        contactPhone = re.findall(r'tel:(\d+)',contactPhone)
                        card['phone'] = contactPhone[0]

            
            self.cur.execute(sql_insert,(card['link'],card['title'],card['sel'],card['kompani'],card.get('time'),card.get('phone')))
        
        self.conn.commit()
        self.conn.close()




        return cards



work = WorkUa('https://www.work.ua')
for info in work.get_info():
    print(info)
    print()




