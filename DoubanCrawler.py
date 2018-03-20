"""
任务1:获取每个地区、每个类型页面的URL
return a string corresponding to the URL of douban movie lists given category and location.
"""
import csv
import io,sys
import expanddouban
from bs4 import BeautifulSoup

def getMovieUrl(category, location):
    url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,"+ category +","+ location 
    return url
"""
任务2: 获取电影页面 HTML
"""
def getMovieHtml(category, location):
    url = getMovieUrl(category,location)
    html = expanddouban.getHtml(url, True)
    return html

"""
任务3: 定义电影类
"""
class Movie():
    def __init__(self,name, rate, location, category, in_link, c_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.in_link = in_link
        self.c_link = c_link
"""
任务4: 获得豆瓣电影的信息
return a list of Movie objects with the given category and location.
"""


def getMovies(category, location):
    html = getMovieHtml(category, location)
    soup = BeautifulSoup(html, "html.parser")
    html_movie = soup.find_all('a',  class_='item')
    movie_list = []
    for e in html_movie:
        name = e.find('span', class_='title').string
        rate = e.find('span', class_='rate').string
        href = e.get('href') 
        src = e.find('img')['src']
        movie_list.append(Movie(name, rate, location, category, href, src))   
    return movie_list
"""
任务5: 构造电影信息数据表
任务6: 统计电影数据
"""           

sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
def count_movie():


    final_category=['暴力','恐怖','文艺']
    final_location=[]
    final_movie=[]
    url="https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影"
    html = expanddouban.getHtml(url,True)
    soup = BeautifulSoup(html, "html.parser")
    for child in soup.find(class_='tags').find(class_='category').next_sibling.next_sibling:
        location=child.find(class_='tag').get_text()
        if location!='全部地区':
            final_location.append(location)
    
    for e in final_category:
        for l in final_location:
            final_movie+=getMovies(e,l)#把所有类型和地区的组合的网页内的电影信息写入finalmovie的列表中
            
    with open('movies.csv', 'w', encoding='utf_8_sig') as f:#输出成文本
        writer = csv.writer(f)
        for e in final_movie:
            writer.writerow([e.name,e.rate,e.location,e.category,e.in_link,e.c_link])
    
    #统计数据
    with open('movie.txt','w',encoding='utf-8')as f:
        with open('movies.csv','r',encoding='utf-8')as g:
            file=list(csv.reader(g))
            for i in final_category:
                sametype_movie=[k for k in file if k[3]==i]#筛选出第一种类型，放入sametype列表中
                num_samearea=[]
                for j in final_location:
                    num_samearea.append((j,len( [k for k in sametype_movie if k[2]==j])))#利用元祖将地区和对应的数量固定
                sort=sorted(num_samearea,key=lambda x:x[1],reverse=True)
                fir_location,fri_number=sort[0]
                sec_location,sec_number=sort[1]
                third_location,third_number=sort[2]
                total_number=len(sametype_movie)
                f.write("[{}]类型电影数量排名前三的地区分别为{},{},{},它们分别占总量的{:.2%}，{:.2%}，{:.2%}。\n"
                    .format(i, fir_location, sec_location, third_location, fri_number/total_number, sec_number/total_number, third_number/total_number))

count_movie()



        

