from urllib import request

import pymysql

import time

from bs4 import BeautifulSoup

ttiem = time.strftime("%Y-%m-%d", time.localtime())

with open(r"psnineLog" + ttiem + ".txt", "w") as file:

    db = pymysql.connect("123.206.41.36", "root", "123456", "psnine")

    cursor = db.cursor()

    mainpage = request.Request("http://psnine.com/psngame")

    mainpage2 = request.urlopen(mainpage).read().decode('utf-8')

    mainpagesoup = BeautifulSoup(mainpage2, 'html.parser')

    totalpage = mainpagesoup.find_all('div',class_='page')[0].find('ul').find_all('li')[4].find('a')

    for i in range(int(totalpage.string)):
        a = i + 1
        indexpage = request.Request("http://psnine.com/psngame?page=" + str(a))

        indexpage2 = request.urlopen(indexpage).read().decode('utf-8')

        indexsoup = BeautifulSoup(indexpage2, 'html.parser')

        nextpage = indexsoup.find_all('td', class_='pdd15')

        nextpage1 = indexsoup.find_all('td', class_='pd1015 title lh180')

        print("------------------------------The " + str(a) + " Page------------------------------")

        file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ": The " + str(a) + " Page" + "\n")

        for i in range(len(nextpage)):

            print("------------------------------The " + str(i + 1) + " Game------------------------------")

            file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ": The " + str(i + 1) + " Game" + "\n")

            gamepage = nextpage[i].find('a')['href']

            game_name = nextpage1[i].find('a').getText()

            print(gamepage)

            page = request.Request(gamepage)

            page_info = request.urlopen(page).read().decode('utf-8')

            soup = BeautifulSoup(page_info, 'html.parser')

            box = soup.find_all('div', class_='box')[1]

            child = box.find('table')

            trs = child.find_all('tr')

            a = 0

            for i in range(len(trs) - 1):
                if (i != 0):
                    real_name = trs[i].find_all('td')[1].find('a').getText()
                    print(real_name)
                    trophy_type = trs[i].find_all('td')[1].find('a')['class'][0].split('-')[1]
                    print(trophy_type)
                    name = trs[i].find_all('em')
                    name = name[len(name) - 2]
                    trophy_namestring = name.string
                    rare = trs[i].find_all('td', class_='twoge')[0]
                    trophy_rarestring = "0"
                    if(rare.getText != ""):
                        try:
                            trophy_rarestring = str(float(rare.getText().split('%')[0]) / 100)
                        except:
                            trophy_rarestring = "0"
                    print(trophy_namestring)
                    print(trophy_rarestring)
                    sql = "insert into trophy(game_name,trophy_name,trophy_desc,rare,get_date,trophy_type) values('%s','%s','%s','%s','%s','%s')" % (game_name,real_name,trophy_namestring,trophy_rarestring,time.strftime("%Y-%m-%d", time.localtime()) ,trophy_type)
                    try:
                        cursor.execute(sql)
                        db.commit()
                    except:
                        db.rollback()
                    print("send-over")

    db.close()

    exit()
