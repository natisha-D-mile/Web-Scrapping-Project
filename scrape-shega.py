# A Project where I scrapped "shega.com" website and sent the data to my telegram channel using a bot
# Importing necessary libraries
import requests
from bs4 import BeautifulSoup
import time

# My Telegram bot token & channel ID
bot_token = '6180127208:AAFbR1fLEur7dVqpUClJ8K4Yov4loZjZmrc'
chat_id = '-1001807421456'
message_count = 0


# Function to find & scrape data from mega-menu links on the website
def find_megamenu_links(url):
    response = requests.get(url)
    # BeautifulSoup then parses this content, making it accessible for data extraction
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all anchor tags with id='sm_megamenu_97'
    links = soup.find_all('a', id='sm_megamenu_98')
    '''
    links = soup.find_all('a', class_='sm_megamenu_head sm_megamenu_drop')    sm_megamenu_haschild
                 #better not to use _ while using id
    '''
    # def contains_both_classes(class_list):
    #     return class_list is not None and'sm_megamenu_head' in class_list and 'sm_megamenu_drop' in class_list
    # links = soup.find_all('a', class_=contains_both_classes)

    if links:
        for link in links:
            href = link.get('href')
            # Exclude JavaScript void URLs
            if href and not href.startswith('javascript:void(0)'):
                print(f"Scraping data from: {href}")  # for string literal
            # Call the web_scrape_product_info function For each valid link found to scrape product information from the link
                web_scrape_product_info(href)
    else:
        print("No links found with the specified class or id!")


# Function to send data to the Telegram channel
def send_to_telegram(bot_token, chat_id, message, img_url=None):
    # Define the API URL based on whether there is an image or not
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    if img_url:
        api_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

    # Prepare the data to be sent in the message
    data = {
        "chat_id": chat_id,
        "caption": message
    }

    # If an image URL is provided, add it to the data dictionary
    if img_url:
        data["photo"] = img_url

    try:
        # Send the data using the Telegram API
        response = requests.post(api_url, data=data)
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(
                f"Failed to send message. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to scrape product information from a given URL


def web_scrape_product_info(url):
    global message_count
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', class_='product-item-info')

    if products:
        for product in products:
            image_tag = product.find('img', class_='product-image-photo')
            title_tag = product.find('a', class_='product-item-link')
            price_tag = product.find('span', class_='price')
            '''    
            description_link = title_tag.get('href')
            resp = requests.get(description_link)
            sou = BeautifulSoup(resp.text, 'html.parser')
            product_description = soup.find_all(class_='value')
            img_tag = soup.find_all(class_='fotorama__img magnify-opaque magnify-opaque')
            print(product_description.text)
            '''
            if image_tag and title_tag and price_tag:
                image_url = image_tag.get('src')
                title = title_tag.text.strip()
                price = price_tag.text.strip()

                # Prepare the message to be sent to the Telegram channel
                message = f"{title}\nPrice: {price}"
                # Call the send_to_telegram function to send the message to the channel
                send_to_telegram(bot_token, chat_id, message, image_url)
                message_count += 1

                # Make a 30-second delay every 15 messages
                if message_count % 15 == 0:
                    print("Waiting for 30 seconds...")
                    time.sleep(30)
    else:
        print("No Product Information Found!")


# Main script execution
if __name__ == '__main__':
    website_url = 'https://shega.com/'
    # calling our function
    find_megamenu_links(website_url)
