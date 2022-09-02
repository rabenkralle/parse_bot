import mechanize
from lxml import html
import http.cookiejar as cookielib
import config

cj = cookielib.CookieJar()
br = mechanize.Browser()

addr_ds = config.addr_ds # адрес страницы конкретного товара
addr_search = config.addr_search # адрес страницы с поисковым запросом

# список того, что будем парсить на странице
in_stock_text = "//p[contains(@class,'stock')]/text()"
button_text = "//button[contains(text(),'Add to basket')]"
name_text = "//h1[contains(@class, 'product_title')]/text()"
price_text = "//span[contains(@class, 'woocommerce-Price-amount')]/bdi/text()"
addr_link = "//a[contains(@class,'woocommerce-LoopProduct-link')]/@href"

# Вход на сайт с использованием 'username' и 'password'
def logging_site():
    br.set_cookiejar(cj)
    br.open(config.login_addr)
    br.select_form(nr=0)
    br.form['username-5051'] = config.user_name
    br.form['user_password-5051'] = config.user_password
    br.submit()
    return br

# Функция для получения dom
def get_dom(parse_addr, br):
    br.open(parse_addr)
    page = br.response().read()
    return html.fromstring(page)

# Функция создания словаря с адресами
def make_addr_dict(parse_addr, br):
    dom = get_dom(parse_addr, br)
    addr_check = dom.xpath(addr_link)
    addr_dict = {1: addr_ds}
    for i in range(2, len(addr_check)+2):
        addr_dict[i] = addr_check[i - 2]
    return addr_dict

# Функция парсинга страниц для получения нужных данных
def parse_site(parse_addr, br):
    dom = get_dom(parse_addr, br)
    in_stock_check = dom.xpath(in_stock_text)[0]
    button_check = dom.xpath(button_text)
    name_check = dom.xpath(name_text)[0]
    price_check = dom.xpath(price_text)[0]
    return name_check, in_stock_check, price_check, button_check


if __name__ == '__main__':
    
    print('Это программа парсинг. Чтобы запустить бота, надо запустить программу atbot.py')
    