import re
import datetime

""" date = '2017中国大陆'
time_str_list = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}|\d{4}-\d{1,2}|\d{4})",date)
time_str = time_str_list[0]
#date = datetime.datetime.strptime(date2,'%Y-%m-%d').date()

if len(time_str)==4:
    releasedate = datetime.datetime.strptime(time_str,'%Y').date()
elif len(time_str)==7:
    releasedate = datetime.datetime.strptime(time_str,'%Y-%m').date()
else:
    releasedate = datetime.datetime.strptime(time_str,'%Y-%m-%d').date()

print(releasedate) """

numrating_str = "280"
num_str_lst = re.findall(r"[\d+\.\d]*",numrating_str)
num_str_zn_lst = re.findall(r"万",numrating_str)
if num_str_zn_lst:
    numrating = int(float(num_str_lst[0])*10000)
else:
    numrating = int(num_str_lst[0])
print(numrating)

""" url_ = "https://p1.meituan.net/movie/83dfd2257f41df12b7b30ba3639d6244286474.jpg@464w_644h_1e_"
picture_str_lst = url_.split('@')
picture = picture_str_lst[0]

print(picture) """