import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "psnine")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 查询语句
sql = "SELECT * FROM trophy"
cursor.execute(sql)
# 获取所有记录列表
results = cursor.fetchall()
for row in results:
    fname = row[0]
    lname = row[1]
    print(fname)
    print(lname)

# 关闭数据库连接
db.close()
