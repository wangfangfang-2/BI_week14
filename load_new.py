#获得指定城市的地铁路线
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import re
"""
def get_page_content(request_url):
    header={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(request_url,headers=header,timeout=10)
    content=html.text
    #print(content)
#通过content创建BS对象,html.parser是BS自带的HTML解析器
    soup=BeautifulSoup(content,'html.parser',from_encoding='utf-8')
    return soup
requests_url = 'https://ditie.mapbar.com/beijing_line/'
soup = get_page_content(requests_url)
subways = soup.find_all('div',class_='station')
df = pd.DataFrame(columns=['name','site'])
for subway in subways:
    #得到线路名称
    route_name=subway.find('strong',class_='bolder').text
    #print('route_name=',route_name)
    #找到该线路中 每一站的名称
    routes = subway.find('ul')
    routes = routes.find_all('a')
    for route in routes:
        temp = {'name':route.text,'site':route_name}
        df=df.append(temp,ignore_index = True)
#print(df)

        #print(route.text)
df['city']='北京'
df.to_excel('./subway.xlsx',index=False)

#添加经度longitude,维度latitude
def get_location(keyword,city):
    header={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    #requests_url='http://restapi.amap.com/v3/place/text?key=35fc3e2f362fa1eeec425f4468f2452b&keywords='+\keywords+'&types=&city'+city+'&children=1&offset=1&page=1&extensions=all'
    #requests_url='http://restapi.amap.com/v3/distance?key=35fc3e2f362fa1eeec425f4468f2452b&origins=116.337581,39.993138&destination=116.339941,39.976228&type=1'
    #requests_url='http://restapi.amap.com/v3/place/text?key=cb6271e8a1f293ded5422d57fbd0fcdc&keywords=五道口&types=&city=北京&children=1&offset=1&page=1&extensions=all'
    requests_url='http://restapi.amap.com/v3/place/text?key=cb6271e8a1f293ded5422d57fbd0fcdc&keywords='+keyword+'&types=&city='+city+'&children=1&offset=1&page=1&extensions=all'
    data=requests.get(requests_url,headers=header)
    data.encoding='utf-8'
    data=data.text
   # print(data)
   #.*具有贪婪的性质，首先匹配到不能匹配为止；。*？则相反，一个匹配以后，就可以继续后面到
    pattern='location":"(.*?),(.*?)"'
   
   #获取经纬度
    result=re.findall(pattern,data)
    
    return result




df=pd.read_csv('./subway.csv')
df['longitude'],df['latitude']=None,None
for index,row in df.iterrows():
    result = get_location(row['name'],row['city'])
    if len(result) < 2:
        continue
    longitude,latitude=result[0][0], result[0][1]
    df.iloc[index]['longitude']=longitude
    df.iloc[index]['latitude']=latitude
    #print(longitude,latitude)
get_location('五道口站','北京')
df.to_csv('./subway.csv',index=False)
"""

import pandas as pd 
import requests
import re
"""
#计算两点之间的距离
def compute_distance(longitude1,latitude1,longitude2,latitude2):
    header={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    requests_url='http://restapi.amap.com/v3/distance?key=cb6271e8a1f293ded5422d57fbd0fcdc&origins='+str(longitude1)+','+str(latitude1)+'&destination='+str(longitude2)+','+str(latitude2)+'&type=1'
    data=requests.get(requests_url,headers=header)
    data.encoding='utf-8'
    data=data.text
    #print(data)
    
   #.*具有贪婪的性质，首先匹配到不能匹配为止；。*？则相反，一个匹配以后，就可以继续后面到
    pattern='distance":"(.*?)","duration":"(.*?)"'
   
   #获取经纬度
    result=re.findall(pattern,data)
    #result= pd.DataFrame.dropna(result,axis=0,how='any',inplace=True)
    return result[0][0]
    #print(len(result))
    #print(result[0][0],result[0][1])
#compute_distance(116.337742,39.992894,116.365023,39.812904)
#compute_distance(116.337581,39.993138,116.339941,39.976228)
#数据加载

data=pd.read_csv('./subway1.csv')
#print(data)
from collections import defaultdict
#保存图中两点之间的距离，graph为邻接矩阵表
graph= defaultdict(dict)
for i in range(data.shape[0]):
    site1=data.iloc[i]['site']
    if i < data.shape[0]-1:
        site2= data.iloc[i+1]['site']
        #如果是同一条线路
        if site1==site2:
            longitude1,latitude1=data.iloc[i]['longitude'],data.iloc[i]['latitude']
            longitude2,latitude2=data.iloc[i+1]['longitude'],data.iloc[i+1]['latitude']
            name1=data.iloc[i]['name']
            name2=data.iloc[i+1]['name']
            #按照距离，计算两点之间的距离 
            distance = compute_distance(longitude1,latitude1,longitude2,latitude2)
            graph[name1][name2]=distance
            graph[name2][name1]=distance
            #print(name1,name2,distance)
import pickle
output=open('graph1.pkl','wb')
pickle.dump(graph,output)
#获得指定城市的地铁路线

import requests
def get_page_content(request_url):
    header={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(request_url,headers=header,timeout=10)
requests_url = 'https://ditie.mapbar.com/beijing_line/'
soup = get_page_content(requests_url)
"""

import pickle
file = open('graph1.pkl','rb')
graph = pickle.load(file)
#print(graph)

#找到开销最小的节点
def find_lowest_cost_node(costs):
    #查找最小节点，采用打擂法
    lowest_cost=float('inf')
    lowest_cost_node = None
    #做一个遍历
    for node in costs :
        #如果该节点没有被处理
        if not node in processed:
            #如果当前节点的开销比已经存在的开销小，那么更新该节点为开销最小的节点
            if costs[node]<lowest_cost:
                lowest_cost = costs[node]
                lowest_cost_node = node 
    return lowest_cost_node
    #找到最短路径
def find_shortest_path():
    node = end 
    shortest_path = [end]
    #最终的跟节点为start
    while parents[node]!=start:
        #往前移动一步
        node=parents[node]
        #添加到路径中
        shortest_path.append(node)
    shortest_path.append(start)
    return shortest_path
#计算图中从start到end的最短路径
def dijkstra():
    #查询到目前开销最小的节点
    node = find_lowest_cost_node(costs)
    print('当前cost最小节点',node)
   
    #print('当前cost最小节点：',node)
    #使用找到的开销最小节点，计算它的邻居，是否可以通过它进行更新
    #如果所有节点都在processed,就结束
    while node is not None:
        #获取节点的cost
        cost = costs[node]#cost是从node到start的距离
        #获取节点的邻居
        neighbors = graph[node]
        #遍历所有邻居，看是否可以通过它进行更新
        for neighbor in neighbors.keys():
            #计算邻居到当前节点+当前节点开销
            new_cost = cost + float(neighbors[neighbor])
            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                #经过node到达neighbor
                parents[neighbor]=node
            # if neighbor not in costs new_cost < costs[neighbor]:
            #     costs[neighbor] = new_cost
            #     #经过node到达neighbor节点，cost更少
            #     parents[neighbor]= node
            #将当前节点标记为已处理
        processed.append(node)
        #下一步，继续找U中最短距离的节点，cost=U,processed=5
        node=find_lowest_cost_node(costs)
#循环完说明所有节点已经处理完，找最短路径
    shortest_path = find_shortest_path()
    shortest_path.reverse()
    print('从{}到{}的最短路径:{}'.format(start,end,shortest_path))
    #print('最短路径',shortest_path)
start = '回龙观站'
end = '天坛东门站'  
""" 
start = '首经贸站'
end = '五道口站'

start = '雍和宫站'
end = '西二旗站'



#start = '首经贸站'
#end = '五道口站'


start = '回龙观站'
end = '天坛东门站'
"""
# 创建节点的开销表，cost是指从start到该节点的距离
costs = {}
# 存储父节点的Hash表，用于记录路径
parents = {} 
parents[end] = None
# 记录处理过的节点list
processed = []
#获取节点相邻的节点
for node in graph[start].keys():
    print(graph[start][node])
    costs[node]= float(graph[start][node])
    #costs[node]= list(map(float(graph[start][node])))
   #costs[node]= graph[start][node]
    parents[node] = start
#终点到起始点设置为无穷大
costs[end]= float('inf')
#print(graph[start].keys())
#
#记录处理过的节点list
"""

if __name__ == "__main__":
    site1 = '五道口站'
    site2 = '北京南站'
    #保存当前最小距离
    distance = float('inf')
    longitude1,latitude= location[0],location1[1]
    nearest = None
    for i in range(data.shape[0]):
        site1= data.iloc[i]['name']
        #iloc=index location,使用index来进行定位（行）
        longitude = float(data.iloc[i]['longitude'])
        latitude = float(data.iloc[i]['latitude'])
        temp=(longitude1-longitude)**2 + (latitude1 -latitude)**2
        if temp < distance:
            distance=temp
            nearest=site1
    return nearest
    city = '北京'
    site1='清华大学'
    site2='798'


    shortest_path = route_api.compute(site1,site2)
    print(shortest_path)"""