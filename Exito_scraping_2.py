from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests


driver= webdriver.Chrome()
url="https://www.exito.com/tecnologia/celulares/smartphones?category-1=tecnologia&category-2=celulares&category-3=smartphones&facets=category-1%2Ccategory-2%2Ccategory-3&sort=score_desc&page=0"

final_data=[]

response=requests.get(url)

if response.status_code == 200:
    
    print("Sucessful conecction")

    #extract all data products by simulating clicks
    def extract_data(page_number):
        
        dinamic_url = url + str(page_number)

        driver.get(dinamic_url)

        html = driver.page_source

        soup=BeautifulSoup(html,'html.parser')

        #general revelant info container (it might change)
        products=soup.find_all('article',class_="productCard_productCard__M0677 productCard_column__Lp3OF")
        
        print(len(products))

        for product in products:
            
            brand=product.find('span', class_="styles_brand__IdJcB")   
            name=product.find('p',class_="styles_name__qQJiK")
            normal_price=product.find('p',class_="priceSection_container-promotion_price-dashed__FJ7nI")
            discount=product.find('div', class_="priceSection_container-promotion_discount__iY3EO")
            discount_price=product.find('p',class_="ProductPrice_container__price__XmMWA")
            seller = product.find('div', attrs={"data-fs-product-name-container":"true"})
            
            final_brand = brand.text.strip() if brand else 'NA'
            final_name = name.text.strip() if name else 'NA'
            final_normal_price = normal_price.text.strip() if normal_price else 'NA'
            final_discount=discount.text.strip() if discount else 'NA'
            final_discount_price=discount_price.text.strip() if discount_price else 'NA'
            final_seller=seller.text.strip() if seller else 'NA'
            
            print(final_brand)
            print(final_name)
            print(final_normal_price )
            print(final_discount )
            print(final_discount_price)
            print(final_seller)
            
            final_data.append({
                
                'Brand': final_brand,
                'Product Name':final_name,
                'Normal Price':final_normal_price,
                'Discount':final_discount,
                'Discount Price':final_discount_price,
                'Seller':final_seller
                
            })
    n_pages = 34  # change by the amount of pages to extract (Total 34 pgs)
    for page in range(n_pages):
        extract_data(page)
    
    #Format convertion
    df = pd.DataFrame(final_data)
    df.to_csv('Exito_smatrphones.csv', index=False)
        
else:
    print("Failed conection")        
      




   
