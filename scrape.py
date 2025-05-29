from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import regex as re
from datetime import datetime

def scrape():
    options = webdriver.ChromeOptions()
    options.headless = False

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://x.com/login")
    print("Please log in manually. Once you see your Twitter home page or navigate to a profile, press Enter in the terminal to continue.")
    input("Waiting for manual login...")

    driver.get("https://x.com/FabrizioRomano")
    time.sleep(5)

    unique_tweets = set()
    all_tweets = []

    def extract_tweets():
        divs = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')
        new_tweets = 0

        for div in divs:
            try:
                article = div.find_element(By.TAG_NAME, 'article')
                elts = article.find_elements(By.CSS_SELECTOR, 'div[lang]')
                text = "\n".join([el.text for el in elts]).strip()
                time_element = article.find_element(By.TAG_NAME, 'time')
                tweet_date = time_element.get_attribute('datetime')
                dt = datetime.strptime(tweet_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                date = dt.strftime("%m/%d/%Y")

                if text and text not in ["Don’t miss what’s happening", "Sign up", "Log in"]:
                    if text not in unique_tweets:
                        unique_tweets.add(text)
                        all_tweets.append((text, date))
                        new_tweets += 1
            except Exception:
                continue
        return new_tweets

    extract_tweets()

    pause_time = 3
    step = 500

    for i in range(50):
        driver.execute_script(f"window.scrollBy(0, {step});")
        time.sleep(pause_time)
        extract_tweets()

    driver.quit()

    return all_tweets
