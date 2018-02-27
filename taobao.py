from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pyquery import PyQuery as pq


browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

def search():
    try:

        browser.get('http://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )

        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button '))
        )

        input.send_keys('美食')
        submit.click()

        total_page = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total'))
        )

        return total_page.text

    except TimeoutException:
        print('超时')



def next_page(page_number):
    try:
        page_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )

        page_submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )

        page_input.clear()
        page_input.send_keys(page_number)
        page_submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number))
        )

        get_products()


    except TimeoutError:
        print('翻页时间异常！')

def get_products():
    load_products_status = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .m-itemlist .items'))
    )
    if load_products_status:
        html = browser.page_source
        doc = pq(html)
        items = doc('#mainsrp-itemlist .items .item').items()
        #print(len(list(items)))
        for item in items:

            product = {
                'price' :item.find('.price').text(),
                '付款数量':item.find('.deal-cnt').text(),
                'title':item.find('.J_ClickStat').text(),
               # 'img':'https:'+item.find('J_ItemPic img').attr('src')
            }
            print(product)


    else:
        print('加载商品失败！')


def main():
    total = search()
    total_page = int(re.compile('(\d+)').search(total).group(1))
    for i in range(2,total_page+1):
        next_page(i)




    page_submit.click()
if __name__ == '__main__':
    main()