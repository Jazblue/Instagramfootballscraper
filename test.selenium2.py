import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_instagram_info(driver, handle):
    url = f"https://www.instagram.com/{handle}/"
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    try:
        followers_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(@href,'/followers')]/span"))
        )
        followers = followers_element.get_attribute('title') or followers_element.text

        posts_element = driver.find_element(By.XPATH, "//span[contains(text(),' posts')]//preceding-sibling::span")
        posts = posts_element.text

        following_element = driver.find_element(By.XPATH, "//a[contains(@href,'/following')]/span")
        following = following_element.text

        return followers, posts, following
    except Exception as e:
        print(f"Failed to scrape {handle}: {e}")
        return None, None, None

def main():
    # Load clubs data
    clubs_df = pd.read_csv("clubs.csv")

    # Setup driver using webdriver_manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    print("⚠️ Please log in to Instagram manually in the opened browser window, then press Enter here...")
    input()

    results = []

    for idx, row in clubs_df.iterrows():
        club = row['club_name']
        handle = row['instagram_handle']
        print(f"Scraping {club} (@{handle}) ...")

        followers, posts, following = scrape_instagram_info(driver, handle)
        if followers is None:
            followers = posts = following = "N/A"

        print(f"Followers: {followers}, Posts: {posts}, Following: {following}")
        results.append({
            "club_name": club,
            "instagram_handle": handle,
            "followers": followers,
            "posts": posts,
            "following": following
        })

        time.sleep(60)  # Pause 60 seconds between requests to avoid blocking

    # Save results to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv("instagram_clubs_data.csv", index=False)
    print("Done! Saved to instagram_clubs_data.csv")

    driver.quit()

if __name__ == "__main__":
    main()
