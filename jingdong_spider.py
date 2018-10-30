from scrapy import Spider, Request, FormRequest
from jingdong_scrapy.jingdong.items import JingdongItem
from jingdong_scrapy.jingdong.pipelines import JingdongPipeline

import json
import re
import scrapy
from lxml import etree
from scrapy import cmdline

flag = True

data_dict = {}
data_dict['q'] = '龙马'

class JingdongSpider(Spider):
    name = 'jingdong'
    allowed_domains = []
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep - alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    }

    start_urls = 'https://cidian.911cha.com'

    def start_requests(self):
        # regions = {'gulou':  '鼓楼','jianye': '建邺'}
        f = open("dict.txt", "r", encoding='utf-8')
        list = []
        lines = f.readlines()  # 读取全部内容
        for i in range(1000, 10000):  # (开始/左边界, 结束/右边界, 步长)
            # list = [] ## 空列表, 将第i行数据存入list中
            for word in lines[i].split():
                print(word)
                if (re.search(r'[\u4e00-\u9fa5]', str(word))):
                    list.append(word)



        for m in range(len(list)):
            data_dict['q'] =  list[m]

            yield scrapy.FormRequest(url=self.start_urls, headers=self.headers,
                                     formdata=data_dict, callback=self.parse,meta={'m': list[m]})

    def parse(self, response):
        meta = response.meta['m']
        print(meta)
        # print(1)#("//div[@class='pindaoTitle']/h3/a")
        # print(type(response))
        # bytes(response, encoding = "utf8")
        # response = response.replace(body=response.body.replace('<em>', ''))
        # selector = response.xpath('//ul[@class="l3 bt mt pt"]/li')
        # selector = etree.HTML(response.text)
        # response = re.sub('<em>', '', str(response))
        # selector = selector.replace(body=re.sub('<em>', '',str(response)))
        selector = etree.HTML(response.text)

        # sel = json.loads(body)  # 转化为字典
        # total_pages = sel.get("totalPage")
        # print(str(selector))
        k = re.findall(r'<a href=".+\.html" target="_blank">.+?</a>', response.text)
        # print(k[0])
        # print(type(k[0]))
        # for i in range(len(k)):

            # print(k[i])
        k = re.sub(r'<em>|</em>', '', str(k[0]))
        k = re.split(r'<a ',k )
        for i in range(len(k)):
            if (re.search(meta,k[i])):

                # print(k[i])
                href = re.findall(r'^href=".*\.html"',str(k[i]))
                # print(str(href))
                resultt2 = str(href)
                # print('%s70',href)
                resultt2 = (re.sub(r'^\[\'', '', resultt2))
                resultt2 = (re.sub(r'\'\]$', '', resultt2))
                # print(resultt2)

                resultt2 = (re.sub(r'href\=\"', '', resultt2))
                resultt2 = (re.sub(r'\"$', '', resultt2))
                # print(resultt2)
                url_page = "https://cidian.911cha.com/{}".format(resultt2)
                yield Request(url=url_page, headers=self.headers,
                              callback=self.parsebody, meta={'m1': meta})

                print('%s72',resultt2)

                break


        # print(len(k))
        # print(type(k))

        # print(k)
        # print(type(k))
        # sel = selector.xpath('//ul[@class="l3 bt mt pt"]/li/a/@href')
        # sel1 = selector.xpath('//ul[@class="l3 bt mt pt"]/li[1]/a[@href]/text()')
        # print(sel1)
        # sel1 = json.loads(sel1)
        # print(sel1)

        # for i in range(1, 7):
        #     url_page = "https://cidian.911cha.com/{}".format(str(sel[i]))
        #     yield Request(url=url_page, headers=self.headers, callback=self.parsebody,meta={'m1': meta})
            # if (flag == False):
                # break

            #     JingdongPipeline.close_spider()
            # break

            # return [scrapy.FormRequest(url=url_page,headers=self.headers,callback=self.parsebody)]

    def parsebody(self, response):
        meta = response.meta['m1']
        selector = etree.HTML(response.text)
        # print(str(selector))
        # data = response.read()
        # data = data.decode('utf-8')
        '''
        file = open('d:/Pythoncode/simplecodes/0.html','w',encoding='utf-8')
        file.write(data)
        file.close()
        '''
        # k = re.findall(r'<a href="\w+\.html" target="_blank">.+?</a>', response.text)
        # print(k)
        # print(type(k))

        # sel = selector.xpath('//ul[@class="l3 bt mt pt"]/li/a/@href')
        #
        resultnword = selector.xpath("//span[@class='green m']/text()")
        #
        #
        #
        resultprobe = selector.xpath("//div[@class='mcon bt noi f14'][1]/p[3]/a[1][@href]/text()")
        # if not (re.search(r'[\u4e00-\u9fa5]',str(resultprobe))):
        #     print(11)
        #     resultprobe = None
        #     resultcontent = selector.xpath("//div[@class='mcon bt noi f14'][1]/p[3]/text()")
        #     resultcontent = ''.join(resultcontent)
        # else:
        #     resultcontent = selector.xpath("//div[@class='mcon bt noi f14'][1]/p[4]/text()")
        #     resultcontent = ''.join(resultcontent)



        # resultt = selector.xpath("//div[@class='mcon noi f14']/p/atext()")
        # resultt2 = selector.xpath("//div[@class='mcon noi f14']/h2/text()")
        #
        #
        # print(resultn)
        # print(k)

        # resultt2 = str(resultt2)
        # resultt2 = (re.sub(r'^\[\'', '', resultt2))
        # resultt2 = (re.sub(r'\'\]$', '', resultt2))
        item = JingdongItem()

        # print(cmp(data_dict['q'], str(resultt2)))
        # if (meta== (str(resultt2))):
            # print(resultn)
        item['word'] = meta
        item['probe'] = resultprobe
        # item['content'] = resultcontent

        yield item
            # flag = False
        # print(data_dict['q'])
        # yield item



















