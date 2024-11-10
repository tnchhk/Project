import requests
from bs4 import BeautifulSoup
import datetime
import time
import csv
import schedule

def scrape_michael_kors():

    #since the request could not be executed without headers, I added the headers to the request
    #The headers were copied from the network console when the inspect panel was opened 
    headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }
    url = 'https://www.michaelkors.com/on/demandware.store/Sites-mk_us-Site/en_US/Search-UpdateGrid?cgid=womens-handbags&start=0&sz=500'
    response = requests.get(url,headers=headers)


    #send a request to the URL
    soup = BeautifulSoup(response.content, 'html.parser')

    #see markdown after this section for screenshots and description of how the relevant sections were identified in the html content

    #parse the HTML content
    products = soup.find_all('div', {'class': 'product-tile-wrapper'})

    #Extract product name, price, discounted price ratings, timestamp
    data = []
    for product in products:
        name = product.find('a', class_='link back-to-product-anchor-js').text.strip()

    #For some products, there are original prices (if there is a separate discount). These may not appear in all products

        price = ""  # Default value in case price is not found
        list_span = product.find('span', {'class': 'list'})
        if list_span:
            value_span = list_span.find('span', {'class': 'value'})
            if value_span:
                price = value_span.text.strip()

    #For most products, there is a sales price
        sales_price = "No sales price"  # Default value in case price is not found

        sales_span = product.find('span', {'class': 'sales'})
        if sales_span:
            value_span_1 = sales_span.find('span', {'class': 'value'})
            if value_span_1:
                sales_price = value_span_1.text.strip()    

    #Not all products have ratings

        ratings = "" 

        ratings_span = product.find('div', {'class': 'ratings'})
        if ratings_span:
            value_span_2 = ratings_span.find('span', {'class': 'sr-only'})
            if value_span_2:
                ratings = value_span_2.text.strip()


        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data.append([name, price, sales_price, ratings, timestamp])

    #remove 'out of 5 Customer Rating' text from the ratings column
    for row in data:
        row[3] = row[3].replace(' out of 5 Customer Rating', '')

    #add column headers
    data.insert(0, ['Product Name', 'Original Price', 'Sales Price', 'Ratings', 'Timestamp'])

    #Generate current date
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    file_name = f'michael_kors_data_{current_date}.csv'

    #write data to a CSV file
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

#schedule the scraper to run at 9 am every day
schedule.every().day.at("09:00").do(scrape_michael_kors)

while True:
    schedule.run_pending()
    time.sleep(1)

