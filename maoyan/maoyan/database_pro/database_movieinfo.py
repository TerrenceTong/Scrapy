import re
import pymysql
import traceback
import datetime

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='mysql', db='spider')
cursor=conn.cursor()

sql_get = "select * from all_info"
sql_input = "insert into movies_movieinfo(id,moviename,releasedate,nation,directors,leadactors,editors,picture,averating,numrating,description,backpost) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
ret = cursor.execute(sql_get)

all_info = cursor.fetchall()
for each_info in all_info:
    mv_id = each_info[0]
    moviename = each_info[1]
    
    time_str_list = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}|\d{4}-\d{1,2}|\d{4})",each_info[2])
    time_str = time_str_list[0]
    if len(time_str)<5:
        releasedate = datetime.datetime.strptime(time_str,'%Y').date()
    elif len(time_str)<8:
        releasedate = datetime.datetime.strptime(time_str,'%Y-%m').date()
    else:
        releasedate = datetime.datetime.strptime(time_str,'%Y-%m-%d').date()
    
    nation = each_info[3]
    directors = each_info[4]
    leadactors = each_info[5]
    editors = each_info[6]

    picture_str_lst = each_info[7].split('@')
    picture = picture_str_lst[0]

    averating_pre = float(each_info[8])/2
    averating = round(averating_pre,1)

    numrating_str = each_info[9]
    num_str_lst = re.findall(r"[\d+\.\d]*",numrating_str)
    num_str_zn_lst = re.findall(r"万",numrating_str)
    if num_str_zn_lst:
        numrating = int(float(num_str_lst[0])*10000)
    else:
        numrating = int(num_str_lst[0])

    description = each_info[10]
    backpos = picture
    try:
        # 执行sql语句
        cursor.execute(sql_input,(mv_id,moviename,releasedate,nation,directors,leadactors,editors,
            picture,averating,numrating,description,backpos))    #使用executemany做批量处理
        conn.commit()   #把修改提交到数据库
        print(moviename+"  is done!")
    except Exception as e :
        traceback.print_exc()
        conn.rollback()


cursor.close()
conn.close()
