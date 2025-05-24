from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.headless = False

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://x.com/login")
print("Please log in manually. Once you see your Twitter home page or navigate to a profile, press Enter in the terminal to continue.")
input("Waiting for manual login...")

driver.get("https://x.com/FabrizioRomano")
time.sleep(5)

unique_tweets= set()
all_tweets = []

def extract_tweets():
    divs = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')
    new_tweets = 0

    for div in divs:
        try:
            article = div.find_element(By.TAG_NAME, 'article')
            elts = article.find_elements(By.CSS_SELECTOR, 'div[lang]')
            text = "\n".join([el.text for el in elts]).strip()

            if text and text not in ["Don’t miss what’s happening", "Sign up", "Log in"]:
                if text not in unique_tweets:
                    unique_tweets.add(text)
                    all_tweets.append(text)
                    new_tweets += 1
        except Exception:
            continue
    return new_tweets

new_found = extract_tweets()
print(f"Initially found {new_found} unique tweets.")

scroll_pause_time = 3
scroll_step = 500

for i in range(500):
    driver.execute_script(f"window.scrollBy(0, {scroll_step});")
    time.sleep(scroll_pause_time)

    new_found = extract_tweets()
    print(f"After scroll {i + 1}, found {new_found} new unique tweets.")

print(f"Total unique tweets collected: {len(all_tweets)}")
print("\nAll unique tweets collected:\n" + "-"*40)
for idx, tweet in enumerate(all_tweets, 1):
    print(f"Tweet {idx}:\n{tweet}\n{'-'*40}")

driver.quit()
