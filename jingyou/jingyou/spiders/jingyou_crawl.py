# -*- coding: utf-8 -*-
import scrapy

from scrapy import Request
import urllib
import urllib2
import re
import base64

from scrapy_splash import SplashRequest

from jingyou.items import JingyouItem


class QuotesSpider(scrapy.Spider):
    countingTimes = 1;
    name = "quotes"
    start_urls = "http://www.jyeoo.com/account/loginform"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Referer": "http://www.jyeoo.com"
    }

    # start_urls = ["http://www.jyeoo.com/math/ques/search/"]
    lua_scripts = """
            function main(splash, args)
                local cookies = splash:get_cookies()
                splash:init_cookies(cookies)  -- restore cookies
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(4))
                local el = splash:select('#divTree > ul > li:nth-child(2)')
                el:mouse_click()
                splash:wait(4)
                return splash:html()
            end"""

    lua_scripts_page1 = """
            function main(splash, args)
                local cookies = splash:get_cookies()
                splash:init_cookies(cookies)  -- restore cookies
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(2))
                --local el = splash:select('#divList > div.page > div > a.next')
                --el:mouse_click()
                splash:wait(4)
                return splash:html()
            end"""

    lua_scripts_page2 = """
                function main(splash, args)
                    local cookies = splash:get_cookies()
                    splash:init_cookies(cookies)  -- restore cookies
                    local url = splash.args.url
                    assert(splash:go(url))
                    assert(splash:wait(2))
                    local el = splash:select('#divList > div.page > div > a:nth-child(5)')
                    el:mouse_click()
                    splash:wait(4)
                    return splash:html()
                end"""

    # yield SplashRequest(url, self.parse,
    #                     endpoint='execute',
    #                     args={'lua_source': self.lua_scripts},
    #                     )


    # def parse(self, response):
    #     filename = 'page1.html'
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     for url in self.start_urls:
    #         yield SplashRequest(url, self.afterParse,
    #                             endpoint='execute',
    #                             args={'lua_source': self.lua_scripts},
    #                             )


    allowed_domains = ["jyeoo.com"]


    # def start_requests(self):
    #     yield scrapy.Request("http://www.jyeoo.com/account/loginform", meta={'cookiejar': 1},
    #                          callback=self.login)
    #
    # def login(self, response):
    #     captcha = response.xpath("//img[@id='capimg']/@src").extract_first()
    #     urllib.urlretrieve('http://www.jyeoo.com' + captcha, filename='validcode.jpg')
    #
    #     return scrapy.FormRequest("http://www.jyeoo.com/account/loginform", formdata={
    #         'Email': '13752129556',
    #         'Password': base64.b64encode('acrolyte1'),
    #         'Remember': 'true',
    #         'Ver': 'true',
    #         'AnonID': '9837d1b2-2170-4d21-b99e-ea6f4da58594',
    #         'Captcha': raw_input("输入验证码："),
    #     }, meta={'cookiejar': response.meta['cookiejar']},
    #                               headers=self.headers,
    #                               callback=self.after_login)

    def after_login(self, response):
        # 现在已经收到登录请求的响应了
        yield SplashRequest("http://www.jyeoo.com/math/ques/search/", self.afterParse,
                                    endpoint='execute',
                                    args={'lua_source': self.lua_scripts_page1},
                                    )

    def start_requests(self):
        # 现在已经收到登录请求的响应了
        yield SplashRequest("http://www.jyeoo.com/math/ques/search/", self.afterParse,
                                    endpoint='execute',
                                    args={'lua_source': self.lua_scripts},
                                    )

    def goto_next(self, response):
        filename = 'page3.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

    def afterParse(self, response):
        filename = 'page2.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

        # yield SplashRequest("http://www.jyeoo.com/math/ques/search/", self.goto_next,
        #                         endpoint='execute',
        #                         args={'lua_source': self.lua_scripts_page2},
        #                         )






        # filename = 'test'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)


            # def after_login(self, response):
            #     print ('after_login============', response)
            #
            #     for url in self.start_urls:
            #         print '======url:', url
            #         req = scrapy.Request(url, meta={'cookiejar': response.meta['cookiejar']})
            #
            #         yield req
            #
            #
            # def post_login(self, response):
            #     html = urllib2.urlopen(response.url).read()
            #     # # 验证码图片地址
            #     imgurl = re.search('<img id="captcha_image" src="(.+?)" alt="captcha" class="captcha_image"/>', html)
            #     print ('imgurl :' ,imgurl)
            #     if imgurl:
            #         url = imgurl.group(1)
            #     #     # 将图片保存至同目录下
            #         res = urllib.urlretrieve(url, 'v.jpg')
            #     #     # 获取captcha-id参数
            #         captcha = re.search('<input type="hidden" name="captcha-id" value="(.+?)"/>', html)
            #         if captcha:
            #             vcode = raw_input('请输入图片上的验证码：')
            #             return [scrapy.FormRequest.from_response(response,
            #                                               meta={'cookiejar': response.meta['cookiejar']},
            #                                               formdata={
            #                                                   'source': 'index_nav',
            #                                                   # 'source': s,
            #                                                   'form_email': 'humane002@163.com',
            #                                                   'form_password': 'Acrolyte1@!',
            #                                                   'captcha-solution': vcode,
            #                                                   'captcha-id': captcha.group(1),
            #                                                   'user_login': '登录'
            #                                               },
            #                                               callback=self.after_login,
            #                                               dont_filter=True)]
            #                 ]
            # return [FormRequest.from_response(response,
            #                                   meta={'cookiejar': response.meta['cookiejar']},
            #                                   formdata={
            #                                       'source': 'index_nav',
            #                                       # 'source': s,
            #                                       'form_email': 'your_email',
            #                                       'form_password': 'your_password'
            #                                   },
            #                                   callback=self.after_login,
            #                                   dont_filter=True)
            #         ]



            # def parse(self, response):









            # filename = 'test.html'
            # with open(filename, 'wb') as f:
            #     f.write(response.body)
            # self.log('Saved file %s' % filename)

            # item_list = response.css('body > div.main-wrapper > div.container > div.zx-table-container > table > tr.question_cnt_tr')




            # for item in item_list:
            #    JItem = JingyouItem()
            #    JItem['ques'] = item.css('div.question_cnt > div.question::text').extract_first()
            #    JItem['answer'] = item.css('div.question_cnt > div.question_a::text')[1].extract()

            #    yield JItem


            # li_list = response.css('div.zx-table-container div.pager-box ul.ch-page li.lip')
            # go2_next_page_lit_url = li_list[-2].css('a::attr(href)').extract_first()
            # if QuotesSpider.countingTimes > 5:
            #    pass
            # else:
            #    QuotesSpider.countingTimes += 1
            #    if go2_next_page_lit_url is not None:
            #        yield response.follow(go2_next_page_lit_url, callback=self.parse)
