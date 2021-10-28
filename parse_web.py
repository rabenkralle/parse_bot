import mechanize
from lxml import html
import http.cookiejar as cookielib

cj = cookielib.CookieJar()
br = mechanize.Browser()

addr = {1: "___",
        2: "___",
        3: "___"}

in_stock_text = "//p[contains(@class,'stock')]/text()"
button_text = "//button[contains(text(),'Add to basket')]"
name_text = "//h1[contains(@class, 'product_title')]/text()"
price_text = "//span[contains(@class, 'woocommerce-Price-amount')]/bdi/text()"

def logging_site():
    br.set_cookiejar(cj)
    br.open("___")
    br.select_form(nr=0)
    br.form['username-5051'] = '___'
    br.form['user_password-5051'] = '___'
    br.submit()
    return br


def parse_site(parse_addr, br):
    br.open(parse_addr)
    page = br.response().read()
    dom = html.fromstring(page)
    in_stock_check = dom.xpath(in_stock_text)[0]
    button_check = dom.xpath(button_text)
    name_check = dom.xpath(name_text)[0]
    price_check = dom.xpath(price_text)[0]

    if in_stock_check == 'In stock' and button_check:
        return name_check, in_stock_check, parse_addr, price_check
    else:
        return name_check, in_stock_check


if __name__ == '__main__':
    br = logging_site()
    print(parse_site(addr[1], br))
    print(parse_site(addr[2], br))


