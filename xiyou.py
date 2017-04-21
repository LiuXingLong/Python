import urllib.request
import http.cookiejar
import urllib.parse
from scrapy import Selector


def getcookie_str(cj):
    cookie = ''
    for item in cj:
        cookie += item.name
        cookie += '='
        cookie += item.value
        cookie += ';'
    return cookie

#参数默认值设置  data = None , headers = {} , cookie = None | 1, charset = None , yzm = None | 1
def get_http(url,data,headers,cookie,charset,yzm):
    # 代理
    proxy = "202.106.16.36:3128"
    proxy_support = urllib.request.ProxyHandler({'http': proxy})

    res = {}
    if charset is None:
        charset = 'utf-8'
    if data is None:
        req = urllib.request.Request(url)
    else:
        data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, data)
    for (k, v) in headers.items():
        req.add_header(k,v)
    if cookie is None:
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        response = urllib.request.urlopen(req) #response = opener.open(req)
        if yzm is None:
            html = response.read().decode(charset)
        else:
            html = response.read()
        res['html'] = html
    else:
        cj = http.cookiejar.CookieJar()
        cookie_support = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(proxy_support,cookie_support)
        urllib.request.install_opener(opener)
        response = urllib.request.urlopen(req) #response = opener.open(req)
        if yzm is None:
            html = response.read().decode(charset)
        else:
            html = response.read()
        res['html'] = html
        res['cookie'] = getcookie_str(cj)
    return res

#获取验证码
url = "http://222.24.62.120/CheckCode.aspx"
header  = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}
result = get_http(url,None,header,1,'gb2312',1)
cookie = result['cookie']

#下载验证码
fp = open('验证码.jpg','wb')
fp.write(result['html'])
fp.close()



name = input("请输入用户名 :")
passwd = input("请输入密码 :")
code = input("请输入验证码：")

url = 'http://222.24.62.120/default2.aspx'
data = {
'__VIEWSTATE' : 'dDwtNTE2MjI4MTQ7Oz5O9kSeYykjfN0r53Yqhqckbvd83A==',
'Textbox1': '',
'txtUserName' : name,
'TextBox2': passwd,
'txtSecretCode': code,
'RadioButtonList1':'(unable to decode value)',
'Button1':'',
'lbLanguage':'',
'hidPdrs':'',
'hidsc':''
}
header = {
'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
'Cookie' : cookie
}
result = get_http(url,data,header,None,'gb2312',None)




url = 'http://222.24.62.120/xscjcx.aspx?xh='+ name +'&xm=%D7%A3%CD%D8&gnmkdm=N121605'
header = {
'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
'Referer':'http://222.24.62.120/xs_main.aspx?xh='+ name,
'Cookie' : cookie
}
result = get_http(url,None,header,None,'gb2312',None)
rs = Selector(text=result['html']).xpath('//input[@name="__VIEWSTATE"]/@value').extract()
VIEWSTATE = rs[0]



while True:
    XN = input("请输入所查询的学年（比如 2013-2014） : ")
    XQ = input("请输入所查询的学期（比如 1） : ")

    url = 'http://222.24.62.120/xscjcx.aspx?xh=' + name + '&xm=%D7%A3%CD%D8&gnmkdm=N121605'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Referer': 'http://222.24.62.120/xscjcx.aspx?xh=' + name + '&xm=%D7%A3%CD%D8&gnmkdm=N121605',
        'Cookie': cookie
    }
    data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': VIEWSTATE,
        'hidLanguage': '',
        'ddlXN': XN,
        'ddlXQ': XQ,
        'ddl_kcxz': '',
        'btn_xq': '(unable to decode value)'
    }

    result = get_http(url, data, header, None, 'gb2312', None)

    rs = Selector(text=result['html']).xpath('//table[@class="datelist"]/tr/td').extract()

    res1 = []
    res2 = ['学年', '学期', '课程名称','课程性质','课程归属','学分','绩点','成绩','辅修标记','补考成绩','重修成绩','开课学院','备注','重修标记']
    i = 0
    j = -1
    for val in rs:
        if i > 14:
            flag = (i - 15) % 15
            if flag == 0:
                j += 1
                res1.append(res2)
                res2 = []
            if flag != 2:
                val = Selector(text=val).xpath('//td/text()').extract()
                if len(val) == 0:
                    res2.append('')
                else:
                    if val[0] == '\xa0':
                        val[0] = ''
                    res2.append(val[0])
        i += 1
    for val in res1:
        print(val)

    #代理测试代码
    '''
    response = get_http('http://icanhazip.com',data,{},None,None,None)
    print(response['html'])
    response = get_http('http://icanhazip.com', data, {}, 1, None, None)
    print(response['html'])
    '''