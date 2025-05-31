from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    return driver

def close_sign_in_modal(driver):
    try:
        close_btn = driver.find_element(By.XPATH, "//div[contains(@class, 'modal__overlay') and contains(@class, 'modal__overlay--visible')]//button[@aria-label='Dismiss']")
        driver.execute_script("arguments[0].click();", close_btn)
        time.sleep(1)
    except Exception:
        pass

def scroll_to_load_jobs(driver, pause_time=2, max_scrolls=60):
    for i in range(max_scrolls):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause_time)

            see_more = driver.find_element(By.CLASS_NAME, "infinite-scroller__show-more-button")
            if see_more.is_displayed():
                print(f"Clicking 'See more jobs' (scroll {i+1})")
                see_more.click()
                time.sleep(pause_time)
        except:
            break

def fetch_job_elements(driver):
    return driver.find_elements(By.XPATH, "//div[contains(@class, 'base-card')]")

def extract_job_info(job_card):
    try:
        title = job_card.find_element(By.XPATH, ".//h3[contains(@class, 'base-search-card__title')]").text
        company = job_card.find_element(By.XPATH, ".//h4[contains(@class, 'base-search-card__subtitle')]").text
        location = job_card.find_element(By.XPATH, ".//span[contains(@class, 'job-search-card__location')]").text
        posted_time = job_card.find_element(By.XPATH, ".//time").text
        return title, company, location, posted_time
    except:
        return "N/A", "N/A", "N/A", "N/A"


def extract_applicants_from_right_pane(driver):
    try:
        elements = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'applicant')]")
        for element in elements:
            text = element.text.strip()
            if text and "applicant" in text.lower():
                return text
        return "N/A"
    except:
        return "N/A"
    
def get_linkedin_jobs(job_title, location, experience_codes):
    url = (
        f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}&f_TPR=r43200&f_E={experience_codes}"
    )
    driver = setup_driver()
    driver.get(url)
    time.sleep(3)

    close_sign_in_modal(driver)
    scroll_to_load_jobs(driver, pause_time=2, max_scrolls=60)

    job_cards = fetch_job_elements(driver)
    print(f"Found {len(job_cards)} job cards")

    job_data = []

    for i in range(len(job_cards)):
        print(f"\n📄 Processing job {i+1}/{len(job_cards)}")

        try:
            # Re-fetch to avoid stale element references
            job_cards = fetch_job_elements(driver)
            card = job_cards[i]

            # Extract basic info from the card
            title, company, location, posted_time = extract_job_info(card)

            # Get job URL from the anchor tag
            job_link = card.find_element(By.XPATH, ".//a[contains(@class, 'base-card__full-link')]")
            job_url = job_link.get_attribute("href")

            # Open the job post in a new tab
            driver.execute_script("window.open(arguments[0]);", job_url)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(2)

            # Extract applicants from full job page
            applicants = extract_applicants_from_right_pane(driver)
            print(f"👤 Applicants: {applicants}")

            # Close job tab and switch back to main tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(f"❌ Failed to process job {i+1}: {e}")
            applicants = "N/A"
            job_url = "N/A"
            title = title if 'title' in locals() else "N/A"
            company = company if 'company' in locals() else "N/A"
            location = location if 'location' in locals() else "N/A"
            posted_time = posted_time if 'posted_time' in locals() else "N/A"

        job_data.append((title, company, location, posted_time, applicants, job_url))

    driver.quit()
    return pd.DataFrame(job_data, columns=["Position", "Company", "Location", "Posted Time", "Applicants", "Job URL"])