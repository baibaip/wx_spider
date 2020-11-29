from selenium import webdriver
import time
from lxml import html
import re
import requests


wx_spider_nickname = None

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
}


def get_wx_spider_nickname():
    wx_post_url = input('请输入文章URL: ')
    wx_post = requests.get(wx_post_url, headers=headers)
    if wx_post.status_code == 200:
        h = html.etree.HTML(wx_post.text)
        global wx_spider_nickname
        wx_spider_nickname = h.xpath('//*[@id="js_profile_qrcode"]/div/strong/text()')[0]
        print('获取到wx_spider_nickname：%s' % (wx_spider_nickname))


def auto_spider():
    login_url = 'https://mp.weixin.qq.com'
    Browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    Browser.get(login_url)
    print('请扫描弹出页面二维码')
    time.sleep(20)
    h = html.etree.HTML(Browser.page_source)
    wx_token_url = h.xpath('//*[@id="menuBar"]/li[1]/a/@href')[0]
    wx_token = re.findall('\d+', wx_token_url)[0]
    print('获取到token：%s' % (wx_token))
    new_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token='+wx_token+'&lang=zh_CN'
    Browser.get(new_url)
    time.sleep(3)
    Browser.find_element_by_xpath('//*[@id="js_editor_insertlink"]').click()
    time.sleep(1)
    Browser.find_element_by_xpath('//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/p/button').click()
    time.sleep(1)
    input_box = Browser.find_element_by_xpath('//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div[1]/span/input')
    input_box.clear()
    input_box.send_keys(wx_spider_nickname)
    time.sleep(1)
    Browser.find_element_by_xpath('//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div/span/span/button[2]').click()
    time.sleep(5)
    Browser.find_element_by_xpath('//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div[2]/ul/li[1]').click()
    time.sleep(5)
    msg_list = Browser.find_elements_by_class_name('inner_link_article_item')
    print('获取到结果个数：%d' % (len(msg_list)))
    for index in range(len(msg_list)):
        title = Browser.find_element_by_xpath('//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[4]/div/div/div[2]/div/div/label['+str(index+1)+']/div/div[1]/span[2]').text
        print('获取到title：%s' % (title))
        url = Browser.find_element_by_xpath('//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[4]/div/div/div[2]/div/div/label['+str(index+1)+']/span[2]/a').get_attribute('href')
        print('获取到url：%s' % (url))
    time.sleep(30)


if __name__ == '__main__':
    get_wx_spider_nickname()
    auto_spider()
