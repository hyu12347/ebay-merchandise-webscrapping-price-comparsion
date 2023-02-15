from bs4 import BeautifulSoup
import requests
import time
import re
import os
import pandas as pd

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}


def htm_download01():
    try:
        filename = "amazon_gift_card_01.htm".format()
        response = requests.get("https://www.ebay.com/sch/i.html?&_nkw=amazon+gift+card&LH_Sold=1",timeout=5,headers=headers,stream=True)
        webContent = response.content
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(webContent.decode('utf-8'))

    except:
        print("Problem with the connection...")
        
if __name__ == '__main__':
    htm_download01()


def htm_download10():
    try:
        url_10_list = []
        for x in range(1,11):
            url_10_list.append("https://www.ebay.com/sch/i.html?_nkw=amazon+gift+card&LH_Sold=1&_pgn="+str(x))
        print(url_10_list)
        for i in range(0,10):    
            filename = "amazon_gift_card_{:02d}.htm".format(i+1)
            response = requests.get(url_10_list[i],timeout=10,headers=headers,stream=True)
            webContent = response.content
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(webContent.decode('utf-8'))
    except:
            print("Problem with the connection...")
        
if __name__ == '__main__':
    htm_download10()


def parse():
    try:
        #price_data = []
        path = 'C:/Users/Cici/MSBA 422'
        file_count = 0
        for file_name in os.listdir(path):
            if file_name.endswith('.htm'):
                if file_count < 11:
                    with open(path+"/"+file_name, 'r',encoding='utf-8') as f:
                        html_content = f.read()
                        soup = BeautifulSoup(html_content, 'html.parser')
                        list_of_titles =soup.select("#srp-river-results > ul > li > div > div.s-item__info.clearfix > a > div")
                        list_of_prices =soup.select("#srp-river-results > ul > li > div > div.s-item__info.clearfix > div.s-item__details.clearfix > div:nth-child(1) > span")
                        list_of_shipping = soup.find_all(class_="s-item__shipping s-item__logisticsCost")

                        combine = []
                        for i, title in enumerate(list_of_titles):
                            shipping = list_of_shipping[i].text if i < len(list_of_shipping) else "SHOW NA"
                            combine.append({"title": title.text, "price": list_of_prices[i].text, "shipping": shipping})
                        #print(combine)

                        price_data = []
                        price_pattern = re.compile(r"(\d+(?:\.\d+)?)")
                        for item in combine:
                            match_title = price_pattern.search(item["title"])
                            match_price = price_pattern.search(item["price"])
                            match_ship = price_pattern.search(item["shipping"])
                            if match_title:
                                title_price = float(match_title.group(1))
                            else:
                                title_price = 0
                            if match_price:
                                sold_price = float(match_price.group(1))
                            else:
                                sold_price = 0
                            if match_ship:
                                ship_price = float(match_ship.group(1))
                            else:
                                ship_price = 0
                            
                            actual = sold_price+ship_price
                            #print(actual)
                            price_data.append({"title_price": title_price, "sold_price": sold_price, "shipping_price": ship_price, "actual_price": actual})
                        df = pd.DataFrame(price_data)
                        #print(df)
                        sort = df.loc[df['title_price']<df['actual_price']]
                        print("In each htm file, the number of positive difference rows are:",len(sort))
        positive_diff = print(25+26+28+31+27+33+23+22+29+24)
        fraction = 268/600
        print("the fraction is:",fraction)

    except:
            print("Problem with the connection...")

if __name__ == '__main__':
    parse()