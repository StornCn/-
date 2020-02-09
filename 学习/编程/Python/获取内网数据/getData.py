import requests
import re
import json
from lxml import etree

class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'http://222.134.147.86:8085/seeyon/main.do',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
            'Host': '222.134.147.86:8085',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            # 是否增加Content-Type
        }
        self.login_url = 'http://222.134.147.86:8085'
        self.post_url = 'http://222.134.147.86:8085/seeyon/main.do?method=login'
        self.logined_url = 'http://222.134.147.86:8085/seeyon/main.do?method=main'
        
        
        self.get_data_url = 'http://222.134.147.86:8085/seeyon/ajax.do?method=ajaxAction&managerName=colManager&rnd=29071'
        
        self.session = requests.Session()
        self.response = self.session.get(self.login_url, headers=self.headers)

    def login(self, name, password):
        post_data = {
            'power': 1,
            'login_username': name,
            'login_password': password,
            'fontSize': '12',
            'screenWidth': '1920',
            'screenHeight': '1080'
        }

        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            return 1
        else:
            return 0
            
       
        
    def getData(self):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'http://222.134.147.86:8085/seeyon/collaboration/collaboration.do?method=moreDone&fragmentId=5729755744506889160&ordinal=1&rowStr=subject,createDate,receiveTime,sendUser,deadline,category&columnsName=%E5%B7%B2%E5%8A%9E%E4%BA%8B%E9%A1%B9&isGroupBy=false',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
            'Host': '222.134.147.86:8085',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            # 是否增加Content-Type
        }
        payload = {'managerMethod': 'getMoreList4SectionContion', 'arguments': '[{"page":1,"size":"200"},{"isGroupBy":"false","fragmentId":"5729755744506889160","state":4,"ordinal":"1","isTrack":false,"section":"doneSection","isFromMore":true}]'}
        response = self.session.get(self.get_data_url, headers=headers, params=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            return 0
            
    def getData_id_travel(self, id, separator):
        headers_geturl = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
            'Host': '222.134.147.86:8085',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        get_idurl_url = 'http://222.134.147.86:8085/seeyon/collaboration/collaboration.do?method=summary&openFrom=listDone&affairId=' + id
        payload_geturl = {'method': 'summary', 'openFrom': 'listDone'}
        response_geturl = self.session.get(get_idurl_url, headers=headers_geturl, params=payload_geturl)
      

        try:
            if response_geturl.status_code == 200:
                response_geturl.encoding="utf-8"
                result_referer = re.search(r"src=\'(.+)\'></iframe>", response_geturl.text)
                result_referer_url = "http://222.134.147.86:8085" + result_referer.group(1)
                result_request = re.search(r"""id="moduleId" value="(-?\d+)">""", response_geturl.text)
                result_rightId = re.search(r"rightId=(-?\d+)&canFavorite", result_referer_url)
                result_request_url = "http://222.134.147.86:8085/seeyon/content/content.do?method=index&isFullPage=true&moduleId=" + result_request.group(1) + "&moduleType=1&rightId=" + result_rightId.group(1) + "&contentType=20&viewState=2&openFrom=listDone&canDeleteISigntureHtml=false&isShowMoveMenu=false&isShowDocLockMenu=false"
                
                headers_detail_data = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
                    'Host': '222.134.147.86:8085',
                    'Referer': result_referer_url,
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                }

                response_detail_data = self.session.get(result_request_url, headers=headers_detail_data)
                
                if response_detail_data.status_code == 200:
                    
                    response_detail_data.encoding = response_detail_data.apparent_encoding
                    
                    html = etree.HTML(response_detail_data.text)
                    
                    # 获取各项数据
                    self.department = html.xpath('//tbody[@valign="top"]/tr[4]/td[4]/div/font/span/span/text()') # 部门
                    self.big_category = html.xpath('//tbody[@valign="top"]/tr[6]/td[2]/div/font/span/span/text()') # 费用大类
                    self.category = html.xpath('//tbody[@valign="top"]/tr[7]/td[2]/div/font/span/span/text()') # 费用分类
                    self.name = html.xpath('//tbody[@valign="top"]/tr[7]/td[4]/div/font/span/span/text()') # 费用名称
                    self.person = html.xpath('//tbody[@valign="top"]/tr[9]/td[2]/div/span[1]/span/text()') # 出差人
                    # 分离出差人员
                    if len(self.person)>0:
                        for i in range(len(separator)):
                            string = self.person[0]
                            rr = string.split(separator[i])
                            if len(rr)>1:
                                self.person = rr
                                break
                    
                    self.transport = html.xpath('//tbody[@valign="top"]/descendant::tbody[@*="RepeatingTable"][1]/tr/td/div/span/span/text()') # 城市间交通
                    if len(self.transport)<8:
                        self.transport = []
                    self.airplane = html.xpath('//tbody[@valign="top"]/descendant::tbody[@*="RepeatingTable"][2]/tr/td/div/span/span') # 飞机
                    self.airplane_start = []
                    if len(self.airplane)==0:
                        self.airplane = []
                    else:
                        for i in self.airplane:                            
                            self.airplane_start.append(i.xpath('text()'))
                        self.airplane = self.airplane_start
                    self.Accommodation_day = html.xpath('//tbody[@valign="top"]/tr[17]/td[2]/font/span/span/text()') # 住宿天数
                    self.Accommodation_amount = html.xpath('//tbody[@valign="top"]/tr[18]/td[2]/div/font/span/span/text()') # 住宿金额
                    
                    self.taxi = html.xpath('//tbody[@valign="top"]/descendant::tbody[@*="RepeatingTable"][3]/tr/td/span/span/text()') # 出租车
                    if len(self.taxi)<6:
                        self.taxi = []
                    
                    self.Accommodation_subsidy = html.xpath('//tbody[@valign="top"]/tr[26]/td[2]/div/span/span/text()') # 住宿补助
                    self.meal_subsidy = html.xpath('//tbody[@valign="top"]/tr[27]/td[2]/div/span/span/text()') # 餐费补助
                    self.taxi_subsidy = html.xpath('//tbody[@valign="top"]/tr[28]/td[2]/div/span/span/text()') # 出租车补助
                    self.amount_total = html.xpath('//tbody[@valign="top"]/tr[29]/td[5]/font/div/span/span/text()') # 总金额
                    self.reason = html.xpath('//tbody[@valign="top"]/tr[32]/td[2]/font/div/span/span/text()') # 理由
                    self.tel = html.xpath('//tbody[@valign="top"]/tr[36]/td[2]/div/font/span/span/text()') # 联系电话
                    return 1
                else:
                    return 0
            else:
                return 0
        except:
            return 0
        
    def getData_id_other(self, id):
        headers_geturl = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
            'Host': '222.134.147.86:8085',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        get_idurl_url = 'http://222.134.147.86:8085/seeyon/collaboration/collaboration.do?method=summary&openFrom=listDone&affairId=' + id
        payload_geturl = {'method': 'summary', 'openFrom': 'listDone'}
        response_geturl = self.session.get(get_idurl_url, headers=headers_geturl, params=payload_geturl)
        try:
            if response_geturl.status_code == 200:
                response_geturl.encoding="utf-8"
                result_referer = re.search(r"src=\'(.+)\'></iframe>", response_geturl.text)
                result_referer_url = "http://222.134.147.86:8085" + result_referer.group(1)
                result_request = re.search(r"""id="moduleId" value="(-?\d+)">""", response_geturl.text)
                result_rightId = re.search(r"rightId=(-?\d+)&canFavorite", result_referer_url)
                result_request_url = "http://222.134.147.86:8085/seeyon/content/content.do?method=index&isFullPage=true&moduleId=" + result_request.group(1) + "&moduleType=1&rightId=" + result_rightId.group(1) + "&contentType=20&viewState=2&openFrom=listDone&canDeleteISigntureHtml=false&isShowMoveMenu=false&isShowDocLockMenu=false"
                headers_detail_data = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
                    'Host': '222.134.147.86:8085',
                    'Referer': result_referer_url,
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                }
                response_detail_data = self.session.get(result_request_url, headers=headers_detail_data)
                if response_detail_data.status_code == 200:
                    response_detail_data.encoding = response_detail_data.apparent_encoding

                    html = etree.HTML(response_detail_data.text)

                    # 获取各项数据
                    self.department = html.xpath('//tbody[@valign="top"]/tr[4]/td[4]/div/font/span/span/text()') # 部门
                    self.big_category = html.xpath('//tbody[@valign="top"]/tr[6]/td[2]/div/font/span/span/text()') # 费用大类
                    self.category = html.xpath('//tbody[@valign="top"]/tr[7]/td[2]/div/font/span/span/text()') # 费用分类
                    self.name = html.xpath('//tbody[@valign="top"]/tr[7]/td[4]/div/font/span/span/text()') # 费用名称
                    
                    self.expense_detail = html.xpath('//tbody[@valign="top"]/descendant::tbody[@*="RepeatingTable"][1]/tr/td/div/span/span') # 费用明细数据
                    self.expense_detail_start = []
                    if len(self.expense_detail)==0:
                        self.expense_detail = []
                    else:
                        for i in self.expense_detail:                            
                            self.expense_detail_start.append(i.xpath('text()'))
                        self.expense_detail = self.expense_detail_start

                    self.amount_total = html.xpath('//tbody[@valign="top"]/tr[10]/td[5]/font/div/span/span/text()') # 总金额
                    self.reason = html.xpath('//tbody[@valign="top"]/tr[13]/td[2]/font/div/span/span/text()') # 理由
                    self.tel = html.xpath('//tbody[@valign="top"]/tr[17]/td[2]/div/font/span/span/text()') # 联系电话
                    return 1
                else:
                    return 0
            else:
                return 0
        except:
            return 0
