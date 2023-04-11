
# https://weather.com/swagger-docs/call-for-code

# https://github.com/qxhtju/-1/blob/master/GetWeather.py



class GetWeather(object):
    def __init__(self):
        self.baseUrl = r"http://www.weather.com.cn/weather/"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        self.htmlResult = []
        self.loadList=[]
        self.cityList = [] #格式为：列表里面的子列表都是一个省份的所有城市，子列表里所有元素都是字典，每个字典有两项
        self.cityDict={}
        self.result= xlwt.Workbook(encoding='utf-8', style_compression=0)
        self.sheet = self.result.add_sheet('result', cell_overwrite_ok=True)
        self.cityRow=0
        self.totalGet=0
        with open("./CITY.txt", 'r',encoding='UTF-8') as load_f:
            loadList = json.load(load_f) #34个省份
            for i in range(0,4):
                self.cityList.append(loadList[i]['cityList'])
            for i in range(4, 34):
                for j in loadList[i]['cityList']:
                    self.cityList.append(j['districtList'])
            for i in self.cityList:
                for j in i:
                    if 'cityName' in j.keys():
                        self.cityDict.setdefault(j['cityName'], j['cityId'])   #直辖市
                    else:
                        self.cityDict.setdefault(j['districtName'], j['districtId'])  #省
        print(len(self.cityDict))

    def __getWeatherInfo__(self):
        #print(self.cityList)
        #print(self.cityDict)
        for city, id in self.cityDict.items():
            self.totalGet=self.totalGet+1
            self.sheet.write(self.cityRow, 0, city)  #写当前城市名
            PageUrl = self.baseUrl + id + ".shtml"
            request = urllib.request.Request(url=PageUrl,headers=self.headers)
            response = urllib.request.urlopen(request)
            self.htmlResult = response.read().decode("utf-8")
            #soup = BeautifulSoup(self.htmlResult)
            #print(soup.span)
            #print(self.htmlResult)
            #temperature = re.findall(r'<span>(.*?)</span>/<i>(.*?)</i>', self.htmlResult)#取巧的方法
            highTemp = re.findall(r'<span>(.*?)</span>/<i>', self.htmlResult)
            print(highTemp)
            column = 1
            for i in highTemp:
                self.sheet.write(self.cityRow+1, column, i)  # 写最高温度
                column=column+1
            lowTemp= re.findall(r'</span>/<i>(.*?)</i>', self.htmlResult)
            column = 1
            for i in lowTemp:
                self.sheet.write(self.cityRow+2, column, i)  # 写最低温度
                column=column+1
            rain= re.findall(r'<p title="(.*?)" class="wea">', self.htmlResult)
            column = 1
            for weather in rain:
                self.sheet.write(self.cityRow, column, weather)  # 写当前天气状况
                column=column+1
            #CoverPicUrls = re.findall(r'<p class="tem">([\s\S]*?)</p>', self.htmlResult)#有换行，上面的方法失灵
            #print(temperature)
            #print(rain)
            self.result.save(r'.\result.xls')
            self.cityRow=self.cityRow+3
            print(self.totalGet)
            time.sleep(2)

    def __main__(self):
        print(datetime.datetime.now())
        self.__getWeatherInfo__()
        print(datetime.datetime.now())
