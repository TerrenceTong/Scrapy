import pymysql
import traceback

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='mysql', db='spider')

cursor=conn.cursor()
'''
sql = "select * from all_info"
ret = cursor.execute(sql)

row1 = cursor.fetchall()

cursor.close()
conn.close()

print(row1[1][0])
print("%s row in set (0.00 sec)" % ret)'''

# 写sql语句
sql="insert into movies_moviecategory(category,movienum) values(%s,%s);"
# 把所有要插入的信息保存在元祖或列表中
data = [('喜剧',0),('动画',0),('剧情',0),('恐怖',0),('惊悚',0),('科幻',0),('动作',0),('悬疑',0),('犯罪',0),('冒险',0),('战争',0),('奇幻',0),('运动',0),('家庭',0),('古装',0),('武侠',0),('西部',0),('历史',0),('传记',0),('歌舞',0),('黑色电影',0),('短片',0),('纪录片',0),('其他',0)]
#data=((user1,pwd1),(user2,pwd2))
mv_types = ['喜剧','动画','剧情','恐怖','惊悚','科幻','动作','悬疑','犯罪','冒险','战争','奇幻','运动','家庭','古装','武侠','西部','历史','传记','歌舞','黑色电影','短片','纪录片','其他']
print(sql)
for mv_type in mv_types:
    try:
        # 执行sql语句
        cursor.execute(sql,(mv_type,0))    #使用executemany做批量处理
        conn.commit()   #把修改提交到数据库   
    except Exception as e :
        traceback.print_exc()
        conn.rollback()
cursor.close()
conn.close()