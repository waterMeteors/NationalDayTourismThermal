import csv
import logging
from time import sleep

from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
# 定义日志级别
logging.basicConfig(level=logging.INFO)
# 新建写入景点的Csv文件，文件的编码格式和写方式
csvfile = open('去哪儿景点1.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csvfile)
# 写入第一行
writer.writerow(["区域", "名称", "景点id", "类型", "级别", "热度", "地址", "特色", "经纬度"])

# 定义请求头
HEADERS = {
    # 通过fake_useragent 组件随机生成浏览器请求头信息
    'User-Agent': UserAgent(use_cache_server=False).random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cookie': '',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'

}

# 下载页面 如果返回状态不为200,就等待2s以后重新下载
def download_soup_waitting(url):
    logging.info("请求的地址为："+url)
    try:
        response = requests.get(url, headers=HEADERS, allow_redirects=False, timeout=5)
        if response.status_code == 200:
            html = response.content
            html = html.decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            return soup
        else:
            # 没有返回200状态码，等待2秒，在次下载
            logging.warning("请求失败,休眠2s再次请求")
            sleep(2)
            print("等待下载中")
            return download_soup_waitting(url)
    except:
        return ""


def getType(type, url):
    # 下载热点旅游数据为soup对象
    soup = download_soup_waitting(url)
    # 旅游景点对应的列表元素
    search_list = soup.find('div', attrs={'id': 'search-list'})
    # 找到所有的旅游景点项目，并对器进行遍历
    sight_items = search_list.findAll('div', attrs={'class': 'sight_item'})
    logging.info("获取当前页的旅游景点列表，提取数据")
    for sight_item in sight_items:
        name = sight_item['data-sight-name']
        districts = sight_item['data-districts']
        point = sight_item['data-point']
        address = sight_item['data-address']
        data_id = sight_item['data-id']
        level = sight_item.find('span', attrs={'class': 'level'})
        if level:
            level = level.text
        else:
            level = ""
        product_star_level = sight_item.find('span', attrs={'class': 'product_star_level'})
        if product_star_level:
            product_star_level = product_star_level.text
        else:
            product_star_level = ""
        intro = sight_item.find('div', attrs={'class': 'intro'})
        if intro:
            intro = intro['title']
        else:
            intro = ""
        writer.writerow(
            [districts.replace("\n", ""), name.replace("\n", ""), data_id.replace("\n", ""), type.replace("\n", ""),
             level.replace("\n", ""), product_star_level.replace("\n", ""), address.replace("\n", ""),
             intro.replace("\n", ""), point.replace("\n", "")])
    next = soup.find('a', attrs={'class': 'next'})
    if next:
        next_url = "http://piao.qunar.com" + next['href']
        getType(type, next_url)



def getTypes():
    # 定义热门景点的类型
    types = ["文化古迹", "自然风光", "公园", "古建筑", "寺庙", "遗址", "古镇", "陵墓陵园", "故居", "宗教"]
    logging.info("遍历热门景点类型,构造请求路径地址... ...")
    # 根据类型循环构建请求地址
    for type in types:
        # 定义请求的url字符串 key="热门景点"被转译了，subject = "此处定义的就是我们的type",page ="当前页"
        url = "https://piao.qunar.com/ticket/list.htm?keyword=%E7%83%AD%E9%97%A8%E6%99%AF%E7%82%B9&region=&from=mpl_search_suggest&subject=" + type + "&page=1"
        getType(type, url)


if __name__ == '__main__':
    getTypes()
    csvfile.close()