import os
import logging
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def web_driver():
    service = Service('chromedriver.exe')
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-webgl')
    options.add_argument('--use-gl=swiftshader')
    # options.add_argument(
        # 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

    driver = webdriver.Chrome(service=service, options=options)
    return driver

def process_url(url):
    driver = web_driver()
    place_info = {
        'url': url,
        'name': None,
        'address': None,
        'status': None,
        'rating': None,
        'phone': None,
        'latitude': None,
        'longitude': None
    }

    try:
        driver.get(url)
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located(
        #         (By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1'))
        # ) # Wait for the page to load
        time.sleep(10)

        try:
            name_element = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1')
            place_info['name'] = name_element.text.strip() if name_element else None
        except Exception as e:
            logger.warning(f"Unable to extract name from {url}. Error: {e}")

        try:
            address_element = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[3]/button/div/div[2]/div[1]')
            place_info['address'] = address_element.text.strip() if address_element else None
        except Exception as e:
            logger.warning(f"Unable to extract address from {url}. Error: {e}")

        try:
            status_element = driver.find_element(By.CLASS_NAME, 'ZDu9vd')
            place_info['status'] = status_element.text.strip() if status_element else None
        except Exception as e:
            logger.warning(f"Unable to extract status from {url}. Error: {e}")

        try:
            rating_element = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]')
            place_info['rating'] = rating_element.text.strip() if rating_element else None
        except Exception as e:
            logger.warning(f"Unable to extract rating from {url}. Error: {e}")

        try:
            phone_element = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[6]/button/div/div[2]/div[1]')
            place_info['phone'] = phone_element.text.strip() if phone_element else None
        except Exception as e:
            logger.warning(f"Unable to extract phone from {url}. Error: {e}")

        try:
            coordinates = driver.current_url.split('@')[1].split(',')[:2]
            place_info['latitude'], place_info['longitude'] = coordinates
        except Exception as e:
            logger.warning(f"Unable to extract coordinates from {url}. Error: {e}")

        logger.info(f"Extracted place information from {url}: {place_info}")

    except Exception as e:
        logger.error(f"Error processing URL {url}: {e}")
    finally:
        driver.quit()

    return place_info

def save_results_to_csv(file_path, results, mode='a'):
    df = pd.DataFrame(results)
    df.columns = ['url', 'name', 'address', 'status', 'rating', 'phone', 'latitude', 'longitude']
    if mode == 'w' or not os.path.exists(file_path):
        df.to_csv(file_path, index=False, mode=mode, header=True)
    else:
        df.to_csv(file_path, index=False, mode=mode, header=False)
def scrape_multiple_urls(urls):
    temp_success_file = 'temp_place_info.csv'
    final_success_file = 'place_info.csv'

    # Ensure the temp file is empty before starting
    if os.path.isfile(temp_success_file):
        os.remove(temp_success_file)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(process_url, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                place_info = future.result()
                save_results_to_csv(temp_success_file, [place_info], mode='a')

            except Exception as e:
                logger.error(f"Error occurred while processing {url}: {e}")

    # Move temp file to final location
    if os.path.isfile(temp_success_file):
        os.rename(temp_success_file, final_success_file)

if __name__ == "__main__":
    # Load the CSV containing URLs
    df = pd.read_csv('Me&Be.csv')
    urls = df['URL']  # Assuming the column with URLs is named 'link'

    try:
        scrape_multiple_urls(urls)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Scraping completed. Data saved to place_info.csv.")
