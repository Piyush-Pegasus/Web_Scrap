from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import pandas as pd
import requests

api_url = "https://openexchangerates.org/api/latest.json?app_id=69f515fc2fbe42698b4562d966152149&symbols=INR"
response = requests.get(api_url)
data = response.json()
conversion_rate = data['rates']['INR']

def get_day(date):
    words=date.split()
    day=int(words[1].split(',')[0])

    month=words[0]
    m=0
    if month=='Jan':
        m= 1
    elif month=='Feb':
        m= 2
    elif month=='Mar':
        m= 3
    elif month=='Apr':
        m= 4
    elif month=='May':
        m= 5
    elif month=='Jun':
        m= 6
    elif month=='Jul':
        m= 7
    elif month=='Aug':
        m= 8
    elif month=='Sep':
        m= 9
    elif month=='Oct':
        m= 10
    elif month=='Nov':
        m= 11
    elif month=='Dec':
        m= 12
    
    year=int(words[2])
    
    date_obj = datetime(year, m, day)
    day_of_week = date_obj.strftime('%A')
    formatted_date = date_obj.strftime('%d-%m-%Y')
    
    return day_of_week,formatted_date


def set_time_frame(url):
    try:
        
        
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        # # Wait until the close button is clickable and then click it
        # close_button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "use[href='/next_/icon.svg#close']"))
        # )
        # if close_button is not None:
        #     close_button.click()

        # Wait until the dropdown is visible and then interact with it
        dropdown = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span[class='flex-1']"))
        )
        dropdown.click()
        print(dropdown.text)

        #set timeframe to weekly
        select_weekly =  WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,"//span[normalize-space()='Weekly']")))
        print(select_weekly.text)
        select_weekly.click()
    except Exception as e:
        print(f"An error occurred: {e}")

try:    
    url="https://uk.investing.com/commodities/us-sugar-no11-historical-data"
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5) 

    Product=driver.find_element(By.XPATH,"//h2[@class='mb-6 text-xl/7 font-bold sm:text-3xl/8 md:whitespace-nowrap']")
    # Split the text by spaces and extract the second word
    words = Product.text.split()
    product=" "
    if len(words) >= 2:
        product = words[1]
    else:
        print("Product text does not contain enough words.")
    
    #Get all rows in table
    table=driver.find_element(By.CSS_SELECTOR,"table[class='freeze-column-w-1 w-full overflow-x-auto text-xs leading-4']")
    all_rows=table.find_elements(By.XPATH,".//tbody//tr")
    print(len(all_rows))

    product_names = []
    prices = []
    product_dates = []
    days=[]
    final_prices = []
    
    for row in all_rows:
        td_tags=row.find_elements(By.TAG_NAME,"td")
        print(len(td_tags))
        if(len(td_tags)==7):
            date_element=WebDriverWait(td_tags[0],10).until(EC.visibility_of_element_located((By.XPATH,".//time")))
            price_element=td_tags[1]

            # print(date_element.text)
            # print(price_element.text)
        # Extract the text content from date and price elements
            date = date_element.text
            price = price_element.text
            price = float(price.replace(",", ""))
            day=get_day(date)[0]
            date=get_day(date)[1]
            final_price = price * conversion_rate
            
            product_names.append(product)
            product_dates.append(date)
            days.append(day)
            prices.append(price)
            final_prices.append(final_price)    

    df = pd.DataFrame({
        'Product name': product_names,
        'Price': prices,
        'Product date': product_dates,
        'Day': days,
        'Final price(INR)': final_prices
    })

    print(df)
    df.to_excel("product_data.xlsx", index=False)
    print("DataFrame written to product_data.xlsx")
    time.sleep(5)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()

if __name__=='__main__':
    url="https://uk.investing.com/commodities/us-sugar-no11-historical-data"
    set_time_frame(url)