import csv
import requests
import json
import tweepy
from dotenv import load_dotenv
import os

# Load env variables 
load_dotenv()
ETHSCAN_KEY = os.environ.get("ETHSCAN_KEY")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
TG_API_KEY = os.environ.get("TG_API_KEY")
MAIN_GRP_ID = os.environ.get("MAIN_GRP_ID")
TEST_GRP_ID = os.environ.get("TEST_GRP_ID")

#Offical $HOGE ETH wallet address
HOGE_ETH_ADDR = '0xfad45e47083e4607302aa43c65fb3106f1cd7607'

#This function makes an API call to etherscan and parses the JSON response for the current amount of $HOGE in the dead address wallet.
def get_current_burn():
    url = "https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=" + HOGE_ETH_ADDR + "&address=0x000000000000000000000000000000000000dead&tag=latest&apikey=" + ETHSCAN_KEY
    res = requests.post(url, json={"key": "value"})
    current_burn = int(res.json()['result'])
    print("Current Burn: " + str(current_burn))
    return current_burn

#This function calls the raw value for the last time get_current_burn was called that's by default saved in a csv file in the current working directory.
def get_last_daily_burn():
    with open('./burnRecord.csv') as f:
        csv_f = csv.reader(f)
        for row in csv_f:
            last_burn = int(row[-1])
    print("Last Daily Burn: " + str(last_burn))
    return last_burn

#This function calculates the difference in the amount total amount of $HOGE in the burn wallet between today and yesterday.
def calculate_burn_difference():
    current_burn = get_current_burn()
    last_daily_burn = get_last_daily_burn()
    raw_daily_burn = current_burn - last_daily_burn
    print("Burn Difference: " + str(raw_daily_burn))
    return raw_daily_burn

#This formats the daily burn total in a format for posting on social media.
def format_burn(data):
    burn_difference_str = str(data)
    burn_difference_dec = burn_difference_str[:-9] + "." + burn_difference_str[-9:]
    clean_daily_burn = '{:,}'.format(float(burn_difference_dec))
    print("Formatted Daily Burn: " + str(clean_daily_burn))
    return clean_daily_burn

#This function authenticates and posts the daily burn to twitter.
def post_to_twitter(burn_difference_formatted):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create API object
    api = tweepy.API(auth)

    # Create a tweet
    api.update_status(burn_difference_formatted + " $HOGE burned from circulation in the past 24 hours" + " " + u"\U0001F525")

#This function posts the daily burn main to the main telegram group
def post_to_telegram(burn_difference_formatted):
    raw_total_burn = get_current_burn()
    total_burn = format_burn(raw_total_burn)
    #requests.post("https://api.telegram.org/bot" + TG_API_KEY + "/sendMessage?chat_id=" + str(MAIN_GRP_ID) + "&text=" +  burn_difference_formatted + " $HOGE burned from circulation in the past 24 hours" + " " + u"\U0001F525" + "\n\n" + total_burn + " $HOGE has been burned in total! " + u"\U0001F525")
    requests.post("https://api.telegram.org/bot" + TG_API_KEY + "/sendMessage?chat_id=" + str(MAIN_GRP_ID) + "&text=" + "Hello World!")
    
#This function posts the daily burn  to the test telegram group
def post_to_telegram_test(burn_difference_formatted):    
    raw_total_burn = get_current_burn()
    total_burn = format_burn(raw_total_burn)
    requests.post("https://api.telegram.org/bot" + TG_API_KEY + "/sendMessage?chat_id=" + str(TEST_GRP_ID) + "&text=" +  burn_difference_formatted + " $HOGE burned from circulation in the past 24 hours" + " " + u"\U0001F525" + "\n\n" + total_burn + " $HOGE has been burned in total! " + u"\U0001F525")
    
#This function updates the CSV file tracking the previous day's burn.
def update_burn_csv():
    current_burn = get_current_burn()
    with open('./burnRecord.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([current_burn])

def main():
    current_burn = get_current_burn()
    last_daily_burn = get_last_daily_burn()
    #Post to twitter
    burn_difference = calculate_burn_difference()
    burn_difference_formatted = format_burn(burn_difference)
    post_to_twitter(burn_difference_formatted)
    #Post to TG
    burn_difference = calculate_burn_difference()
    burn_difference_formatted = format_burn(burn_difference)
    post_to_telegram(burn_difference_formatted)
    #Post to TG test channel
    burn_difference = calculate_burn_difference()
    burn_difference_formatted = format_burn(burn_difference)
    post_to_telegram_test(burn_difference_formatted)
    #Update burnRecord.csv
    update_burn_csv()

if __name__ == "__main__":
    main()
