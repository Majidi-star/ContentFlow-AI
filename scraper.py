import os
import time
import uuid
import logging
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# --- تنظیمات لاگینگ (ثبت خطاها) ---
# این بخش باعث می‌شود تمام خطاها در فایل scraper_errors.log ذخیره شوند
logging.basicConfig(
    filename='scraper_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# --- تنظیمات اولیه ---
DATA_FOLDER = 'data'
SCRAPED_FILE = 'scraped.txt'

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

if not os.path.exists(SCRAPED_FILE):
    open(SCRAPED_FILE, 'w', encoding='utf-8').close()

# لیست وب‌سایت‌ها (با سلکتورهای جدید زومیت که پیدا کردیم)
TARGET_SITES = [
    {
        'url': 'https://www.zoomit.ir/',
        'selectors': [
            'a.block.w-full[href^="/"]',     # مقالات اصلی
            'div.lg\\:w-1\\/2 a[href^="/"]', # مقاله ویژه بزرگ
            '.border-borderPrimary a[href^="/"]', # لیست‌های کناری
            '.swiper-slide a[href^="/"]'     # اسلایدرها
        ]
    },
    # می‌توانید سایت‌های دیگر را اینجا اضافه کنید
]

def get_scraped_links():
    """خواندن لینک‌های قبلا اسکرپ شده"""
    try:
        with open(SCRAPED_FILE, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    except Exception as e:
        error_msg = f"Error reading history file: {str(e)}"
        print(error_msg)
        logging.error(error_msg, exc_info=True)
        return set()

def append_to_scraped(link):
    """اضافه کردن لینک موفق به لیست تاریخچه"""
    try:
        with open(SCRAPED_FILE, 'a', encoding='utf-8') as f:
            f.write(link + '\n')
    except Exception as e:
        error_msg = f"Error saving to history file: {str(e)}"
        print(error_msg)
        logging.error(error_msg, exc_info=True)

def clean_html_content(raw_html):
    """تمیز کردن HTML"""
    try:
        soup = BeautifulSoup(raw_html, 'html.parser')

        tags_to_remove = [
            'script', 'style', 'img', 'svg', 'video', 'iframe', 
            'nav', 'header', 'footer', 'aside', 'form', 'button', 
            'input', 'meta', 'link', 'noscript'
        ]

        for tag in tags_to_remove:
            for element in soup.find_all(tag):
                element.decompose()

        for element in soup.find_all():
            if len(element.get_text(strip=True)) == 0 and element.name not in ['br', 'hr']:
                element.extract()

        return str(soup)
    except Exception as e:
        error_msg = f"Error cleaning HTML content: {str(e)}"
        print(error_msg)
        logging.error(error_msg, exc_info=True)
        return raw_html

def init_driver():
    """تنظیمات درایور کروم"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # تنظیمات برای جلوگیری از تشخیص ربات
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    service = Service('/usr/bin/chromedriver') 

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        # لاگ کردن خطای درایور بسیار مهم است
        error_msg = f"Failed to initialize Chrome Driver: {str(e)}"
        print(error_msg)
        logging.critical(error_msg, exc_info=True)
        
        # تلاش دوم با مدیر درایور خودکار (اگر نصب باشد)
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
        except Exception as e2:
            logging.critical(f"Second attempt to init driver failed: {str(e2)}", exc_info=True)
            raise e

def main():
    driver = None
    try:
        driver = init_driver()
        scraped_history = get_scraped_links()

        print("Starting scraper cycle...")

        for site_info in TARGET_SITES:
            base_url = site_info['url']
            selectors_list = site_info['selectors']
            
            print(f"Processing Site: {base_url}")

            post_links = []
            
            try:
                driver.get(base_url)
                time.sleep(5)
                
                for sel in selectors_list:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, sel)
                        print(f"Selector '{sel}' found {len(elements)} elements.")
                        
                        for el in elements:
                            try:
                                link = el.get_attribute('href')
                                # فیلتر کردن لینک‌های شورت ویدیو و تکراری‌ها
                                if link and link not in scraped_history and '/shorts/' not in link:
                                    post_links.append(link)
                            except Exception as e:
                                # خطاهای جزئی در گرفتن لینک یک المنت خاص
                                logging.warning(f"Error getting href from element: {e}")
                                continue
                    except Exception as e:
                        error_msg = f"Error with selector '{sel}' on {base_url}: {str(e)}"
                        print(error_msg)
                        logging.error(error_msg, exc_info=True)
                        continue

            except Exception as e:
                error_msg = f"Fatal Error accessing site {base_url}: {str(e)}"
                print(error_msg)
                logging.error(error_msg, exc_info=True)
                continue 

            post_links = list(set(post_links))
            print(f"Total unique new links found: {len(post_links)}")

            for link in post_links:
                try:
                    print(f"Scraping: {link}")
                    driver.get(link)
                    time.sleep(3) 

                    full_html = driver.page_source
                    clean_html = clean_html_content(full_html)

                    filename = f"{uuid.uuid4()}.txt"
                    file_path = os.path.join(DATA_FOLDER, filename)

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(clean_html)
                    
                    append_to_scraped(link)
                    scraped_history.add(link)
                    
                    print(f"Saved: {filename}")

                except Exception as e:
                    error_msg = f"Error scraping specific link {link}: {str(e)}"
                    print(error_msg)
                    # exc_info=True باعث می‌شود کل متن خطا (Stack Trace) ذخیره شود
                    logging.error(error_msg, exc_info=True)
                    continue 

    except Exception as e:
        error_msg = f"CRITICAL ERROR IN MAIN LOOP: {str(e)}"
        print(error_msg)
        logging.critical(error_msg, exc_info=True)
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        print("Scraper cycle finished.")

if __name__ == "__main__":
    main()