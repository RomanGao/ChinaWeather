import requests
from bs4 import BeautifulSoup
from pyecharts import Bar

ALL_DATA = []
def spider(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    html  = response.content.decode('utf-8')
    # print(html)
    soup = BeautifulSoup(html, 'html5lib')
    conMidtab = soup.find('div',class_='conMidtab')
    tables = conMidtab.find_all('table')
    # print(tables[0])
    for table in tables:
        trs = table.find_all('tr')[2:]
        # print('#'*100)
        # print(trs[0])
        # trs = trs[-1]

        for index,tr in enumerate(trs):
            tds = tr.find_all('td')
            min_temp = tds[-2].string
            # print(min_temp)
            city_td = tds[0]
            if(index==0):
                # tr_tds = tr.find_all('td')[1]
                # city = list(tr_tds.stripped_strings)[0]
                # city = list(tds[1].stripped_strings)[0]
                city_td = tds[1]
                # print(city)
                # print(city)
            city = list(city_td.stripped_strings)[0]
            ALL_DATA.append({"city":city,"min_temp":int(min_temp)})
            # print({"city":city,"min_temp":min_temp})
            # print(city)
        # print('#'*100)
        # print(type(min_temp))

def analysis():
    # 分析
    # 根据最低气温进行排序
    ALL_DATA.sort(key=lambda data:data['min_temp'])
    # print(ALL_DATA)
    data = ALL_DATA[0:10]
    cities = list(map(lambda x:x['city'],data))
    temps = list(map(lambda x:x['min_temp'],data))

    chart = Bar("中国天气最低气温排行榜")
    chart.add("",cities,temps)
    chart.render('temperature.html')

if __name__ == '__main__':
    urls =[
        "http://www.weather.com.cn/textFC/hb.shtml",
        "http://www.weather.com.cn/textFC/db.shtml",
        "http://www.weather.com.cn/textFC/hd.shtml",
        "http://www.weather.com.cn/textFC/db.shtml",
        "http://www.weather.com.cn/textFC/hz.shtml",
        "http://www.weather.com.cn/textFC/hn.shtml",
        "http://www.weather.com.cn/textFC/xb.shtml",
        "http://www.weather.com.cn/textFC/xn.shtml",
        "http://www.weather.com.cn/textFC/gat.shtml"
    ]
    for url in urls:
        spider(url)
    analysis()