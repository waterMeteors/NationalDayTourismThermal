import csv

#定义加载文件的类型，用来读取csv并把器转换曾echart能够识别的数据类型
from pyecharts.charts import Geo
from pyecharts.globals import ChartType
from pyecharts import options as opts


class City(object):
    pass


def load_file():
    with open("去哪儿景点.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        cityList = []
        #根据规则读取文件中的每一行文字
        for line in reader:
            if len(line[0].split('·'))>1:
                city = City()
                city.cityName = line[0].split('·')[1]
                city.hotValue = float(line[5].split(' ')[1])
                foundRepeatCity = 0
                #获取城市名字cityName和热度信息hotValue
                #针对城市名字cityName做组合操作，也就是针对其做热点求和
                for originCity in cityList:
                    if originCity.cityName == city.cityName:
                        originCity.hotValue = originCity.hotValue + city.hotValue
                        foundRepeatCity = 1
                        break
                #过滤掉城市中没有在echart 备案信息
                if foundRepeatCity == 0 and Geo().get_coordinate(name = city.cityName) !=None and int(city.hotValue) !=0:
                    cityList.append(city)
        # 生成输出信息，用来传入到echart中
        outputGeoData = []
        for city in cityList:
            if Geo().get_coordinate(name = city.cityName) != None and int(city.hotValue) !=0:
                outputGeoDataRecord = (city.cityName, int(city.hotValue)*5)
                outputGeoData.append(outputGeoDataRecord)
        print(outputGeoData)
    return outputGeoData


def geo_base(data) ->Geo:
    c = (
        # 初始化地理热点图
        Geo()
        .add_schema(maptype="china")
        # 此处的 ChartType不同，形成的图形也不同
        .add("2019国庆旅游热力图", data, ChartType.EFFECT_SCATTER)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(title="2019国庆旅游热力图"),
        )
    )
    return c


if __name__ == '__main__':
    data = load_file()
    base = geo_base(data)
    base.render()
