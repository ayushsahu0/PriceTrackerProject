import requests
from bs4 import BeautifulSoup as BS
#from smtplib import SMTP
from twilio.rest import Client
from datetime import datetime
import csv
import time


URL="https://www.amazon.in/Samsung-Galaxy-Ultra-Phantom-Storage/dp/B0BT9FDZ8N/ref=sr_1_3?crid=347NLDONB33SW&keywords=samsung+s23+ultra+5g&qid=1685869435&sprefix=s%2Caps%2C229&sr=8-3"
def extractPrice():
    page=requests.get(URL, headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"})
    soup = BS(page.content,"html.parser")
    price=soup.find(class_="a-price-whole").text.replace(",","").replace(".","")
    return price

'''SMTP_SERVER = "smtp.gamil.com"
PORT= 587
EMAIL_ID="sahayush2003ayu@gmail.com"
PASSWORD = "**********"

server=SMTP(SMTP_SERVER,PORT)
server.starttls()
server.login(EMAIL_ID,PASSWORD)

subject="BUY NOW!!"
body="Price has Fallen. Go Buy NOW"+URL
msg=f"Subject:{subject}\n\nBody:{body}"

server.sendmail(EMAIL_ID,EMAIL_ID,msg)
server.quit()'''

def sendwhatsapp_message(body):
    account_sid = 'ACda354b39cfcd7a2e5265193b01106aca'
    auth_token = '83b1826d9667ca1ca9ea0b7aa28d747a'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=body,
        to='whatsapp:+918209446854'
    )

def save_to_file():
    fields=[datetime.today().strftime("%B-%D %H:%M"),extractPrice()]
    with open('prices.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

def compare_prices():
    with open('prices.csv', 'r') as file:
        reader = csv.reader(file)
        prices = list(reader)

    # Extracting the last price
    last_price = float(prices[-1][1])
    last_price2 = float(prices[-2][1])
    # Comparing with the threshold
    threshold = last_price2  # Set your threshold here
    if last_price < threshold:
        sendwhatsapp_message("BUY NOW!!!! BEST PRICE")
        sendwhatsapp_message(f'The Current Price is ₹{extractPrice()}!!!!! The URL is -> {URL}')
        quit()
    else:
        print("Price is high. Rerunning the code after 6 hours...")
        time.sleep(6 * 60 * 60)  # Sleep for 6 hours (in seconds)
        compare_prices()

if __name__ == '__main__':
    extractPrice()
    save_to_file()
    compare_prices()


