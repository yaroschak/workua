import requests
import lxml.html

base_url = 'https://www.work.ua'


# with requests.session() as s:
#     rez = s.get('https://www.work.ua/jobs/2991081')
#     rez = s.post('https://www.work.ua/jobs/2991081/ajax/get-jobs-data/',data={},headers={'referer':'https://www.work.ua/jobs/2991081'})
#     print(rez.headers)
#     print(rez.json())

# link = 'https://www.work.ua/jobs/2991081/ajax/get-jobs-data/'
# link = 'https://www.work.ua/ajax/get-jobs-data/'
# ajax/get-jobs-data/
# rez = requests.post(link,data={})
# print(rez.status_code)



class WorkUa:
    def __init__(self,base_url):
        self.base_url = base_url


    def get_info(self):

        page = 1
        flag = True
        cards = []
        while flag:
            url = '{0}/jobs-rivne-it/?advs=1&page={1}'.format(self.base_url,page)
            rez = requests.get(url)
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
                                    'link':base_url+a.attrib.get('href'),
                                    'title':a.text_content(),
                                    'sel':div_b.text_content(),
                                    'kompani':kompani.text_content(),
                                    'time':time.text_content()
                                }
                        )
            else:
                print('Error', rez.status_code)

            page = page + 1

        return cards



work = WorkUa('https://www.work.ua')
print(work.get_info())
