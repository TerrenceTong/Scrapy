# -*- coding: utf-8 -*-
import os
import operator
import re
import xml.dom.minidom as xmldom
from bs4 import BeautifulSoup
import requests
from fontTools.ttLib import TTFont

# 请求头设置
header = {
    'Accept': '*/*;',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'maoyan.com',
    'Referer': 'http://maoyan.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}

# 下载请求电影页面的woff字体到本地
def downfont(url):
    r = requests.get('http://'+url)
    with open("temp.woff", "wb") as code:
        code.write(r.content)
    font = TTFont("temp.woff")
    font.saveXML('temp.xml')

def findstar(score_woff,score_num_woff):
    # 加载字体模板
    num = [0,4,5,7,6,1,8,2,3,9]
    #num = [8,6,2,1,4,3,0,9,5,7]
    #保存字体中的10个形状
    data = []
    #保存获取的当前字体的10个形状
    new_font = []
    #保存当前10个数字对应的编码标识
    font = TTFont("temp.woff")
    font_list = font.getGlyphNames()
    font_list.remove('glyph00000')
    font_list.remove('x')
    """ print("---------------------------")
    for i in range(10):
        print("font_list:"+font_list[i]) """

    xmlfilepath_temp = os.path.abspath("template.xml")
    domobj_temp = xmldom.parse(xmlfilepath_temp)
    elementobj_temp = domobj_temp.documentElement
    subElementObj = elementobj_temp.getElementsByTagName("TTGlyph")
    for i in range(len(subElementObj)):
        rereobj = re.compile(r"name=\"(.*)\"")
        find_list = rereobj.findall(str(subElementObj[i].toprettyxml()))
        data.append(str(subElementObj[i].toprettyxml()).replace(find_list[0],'').replace("\n",''))
    #获取模板字体中的十个形状
    data = data[1:-1]
    """ print(len(data))
    print("----------------------------------")
    for i in range(10):
        print(data[i])

    print("----------------------------------") """

    #根据字体模板解码本次请求下载的字体
    xmlfilepath_find = os.path.abspath("temp.xml")
    domobj_find = xmldom.parse(xmlfilepath_find)
    elementobj_find = domobj_find.documentElement
    #列表,保存当前字体所有形状
    tunicode = elementobj_find.getElementsByTagName("TTGlyph")
    for i in range(len(tunicode)):
        th = tunicode[i].toprettyxml()
        report = re.compile(r"name=\"(.*)\"")
        #获取当前字体的编码标识
        find_this = report.findall(th)
        get_code = th.replace(find_this[0], '').replace("\n", '')
        """ print("get_code:"+get_code)
        print("-----------------------------") """
        new_font.append(str(get_code))
        
        """ for j in range(len(data)):
            if not operator.eq(get_code,data[j]):
                new_font.append(num[j]) """
    #得到10个当前的字体形状
    new_font = new_font[1:-1]
    """ print("----------------------------------")
    print(len(new_font))
    for i in range(len(new_font)):
        print (new_font[i])
    print("----------------------------------") """


    # 匹配
    #对当前一串字体的每个编码循环
    for i in range(len(score_woff)):
        if(score_woff[i] == '.' ):
            continue
        #print("i:"+i)
        #当前单个字体编码
        getthis = score_woff[i].upper()
        #找到当前编码对应的字体形状
        for j in range(len(font_list)):
            #当前编码在font_list中的位置 即为 前编码的字体形状在new_font中的位置
            if operator.eq(getthis,font_list[j].replace("uni","")):
                """ print("j:"+str(j))
                print("getthis:"+getthis)
                print("font_list[j]:"+font_list[j].replace("uni","")) """
                for k in range(len(data)):
                    if operator.eq(data[k],new_font[j]):
                        """ print("k:"+str(k))
                        print(data[k])
                        print(new_font[j]) """
                        score_woff[i] = num[k]
                        #print(score_woff[i])
    
    # 匹配
    #对当前一串字体的每个编码循环
    for i in range(len(score_num_woff)):
        if(score_num_woff[i] == '.' or score_num_woff[i] == '万'):
            continue
        #print("i:"+i)
        #当前单个字体编码
        getthis = score_num_woff[i].upper()
        #找到当前编码对应的字体形状
        for j in range(len(font_list)):
            #当前编码在font_list中的位置 即为 前编码的字体形状在new_font中的位置
            if operator.eq(getthis,font_list[j].replace("uni","")):
                """ print("j:"+str(j))
                print("getthis:"+getthis)
                print("font_list[j]:"+font_list[j].replace("uni","")) """
                for k in range(len(data)):
                    if operator.eq(data[k],new_font[j]):
                        """ print("k:"+str(k))
                        print(data[k])
                        print(new_font[j]) """
                        score_num_woff[i] = num[k]


def web(url):
    db_data = requests.get(url, headers=header)
    soup = BeautifulSoup(db_data.text.replace("&#x",""), 'lxml')

    scores = soup.select(
        'body > div.banner > div > div.celeInfo-right.clearfix > div.movie-stats-container > div > div > span > span')
    numbers = soup.select(
        'body > div.banner > div > div.celeInfo-right.clearfix > div.movie-stats-container > div > div > div.index-right > span > span'
    )

    pt = r'(\.)'
    score_woff_ = re.findall(re.compile(r">(.*)<"), str(scores[0]))[0].replace(';','')
    #print(score_woff_)
    score_woff = re.split(pt, score_woff_)

    pt_num = '(\.)'
    score_num_woff_ = re.findall(re.compile(r">(.*)<"), str(numbers[0]))[0]
    #print(score_num_woff_)
    score_num_woff_temp = re.split(pt, score_num_woff_)
    score_num_woff = []
    for temp in score_num_woff_temp:
        for i in temp.split(';'):
            if(i != ''):
                score_num_woff.append(i)

    """ for i in score_num_woff:
        print(i) """
        

    #print(numbers)
    wotfs = soup.select('head > style')

    wotflist = str(wotfs[0]).split('\n')
    maoyanwotf = wotflist[5].replace(' ','').replace('url(\'//','').replace('format(\'woff\');','').replace('\')','')

    downfont(maoyanwotf)
    
    findstar(score_woff, score_num_woff)
    """ for i in score_woff:
        print(i) """
    result1 = [str(n) for n in score_woff]
    result2 = [str(n) for n in score_num_woff]
    """ print(result1)
    print(result2) """
    score = ''.join(result1)
    score_number = ''.join(result2)
    return [score,score_number]
    """ print(score)
    print(score_number) """




def setCsv():
    url = 'http://maoyan.com/films/42964'
    lst = web(url)
    for l in lst:
        print(l)


if __name__ == '__main__':
    setCsv()  # str为标签名