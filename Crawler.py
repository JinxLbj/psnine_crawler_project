# import Producer

# Producer.KafkaFactory.init()
#
# Producer.KafkaFactory.send("hahaha")
#
# Producer.KafkaFactory.close()

from Producer import KafkaFactory

from urllib import request

import pymysql

import time

from bs4 import BeautifulSoup

db = pymysql.connect("123.206.41.36", "root", "123456", "psnine")

cursor = db.cursor()

mainpage = request.Request("http://psnine.com/psngame")

mainpage2 = request.urlopen(mainpage).read().decode('utf-8')

mainpagesoup = BeautifulSoup(mainpage2, 'html.parser')

totalpage = mainpagesoup.find_all('div',class_='page')[0].find('ul').find_all('li')[4].find('a')

print(totalpage.string)

# KafkaFactory.init()

for i in range(int(totalpage.string)):
    a = i + 1
    indexpage = request.Request("http://psnine.com/psngame?page=" + str(a))

    indexpage2 = request.urlopen(indexpage).read().decode('utf-8')

    indexsoup = BeautifulSoup(indexpage2, 'html.parser')

    nextpage = indexsoup.find_all('td', class_='pdd15')

    nextpage1 = indexsoup.find_all('td', class_='pd1015 title lh180')

    print("------------------------------第" + str(a) + "页------------------------------")

    print(nextpage.__len__())

    print(nextpage1.__len__())


    for i in range(len(nextpage)):

        print("------------------------------本页第" + str(i) + "个游戏------------------------------")

        gamepage = nextpage[i].find('a')['href']

        game_name = nextpage1[i].find('a').getText()

        print(gamepage)

        # if(gamepage == "http://psnine.com/psngame/17144"):
        #     continue

        page = request.Request(gamepage)

        page_info = request.urlopen(page).read().decode('utf-8')

        soup = BeautifulSoup(page_info, 'html.parser')

        # print(soup.prettify())

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
                    # 执行sql语句
                    cursor.execute(sql)
                    # 执行sql语句
                    db.commit()
                except:
                    # 发生错误时回滚
                    db.rollback()
                # KafkaFactory.send(namestring + "jinxLbj" + rarestring)
                print("send-over")

db.close()

# KafkaFactory.close()
exit()



# for tr in trs:
#     if a != 0:
#         print(tr.find('em'))
#         print(tr.find_all('td',class_='twoge t1 h-p'))
#     else


# with open(r"D:\devilmaycry5.txt", "w") as file:
#     for title in titles:
#         print(title.string)
#         file.write(title.string + "\n")
