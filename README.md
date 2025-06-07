# GSB570 Final Project
# LinkedIn Job Scraper with H1B Sponsorship Filter

Youtube Demo: https://www.youtube.com/watch?v=uRhgmiH0-9s

This project is a Python-based prototype that automates the process of scraping LinkedIn job postings, checks whether the companies have historically sponsored H1B visas (using USCIS data), and filters jobs based on applicant count.

## Features
✅ Scrapes Data Scientist jobs in California from LinkedIn

✅ Extracts:
Job title
Company name
Location
Posted time
Number of applicants
Direct job posting URL

✅ Compares employers against USCIS H1B sponsorship records

✅ Filters jobs with fewer than 80 applicants

✅ Saves results to a clean .csv file for analysis or follow-up

## Technologies Used
Python
Selenium (for automated browser interaction)
pandas
ChromeDriver (via webdriver-manager)
Jupyter Notebook


## Step 1: Scrape LinkedIn Jobs
1. setup_driver()
   - Launches a Selenium-controlled Chrome browser
   - Uses your actual Chrome user profile (Default) to stay logged in to LinkedIn
   - Maximizes the window for consistent layout rendering
   - 
✅ Ensures LinkedIn sees you as a real user and loads the full job list (not limited to 7 postings)

2. close_sign_in_modal(driver)
   - Automatically closes the login popup LinkedIn sometimes shows to non-logged-in users
   - Skippable when using a logged-in profile, but included for robustness
     
3. scroll_to_load_jobs(driver)
   - Mimics user behavior by scrolling to the bottom of the LinkedIn job list
   - Clicks “See more jobs” until all postings are loaded (up to max_scrolls)
   - 
✅ Helps collect all listings into the visible DOM for scraping

4. fetch_job_elements(driver)
   - Base container for each job in the list

5. extract_job_info(job_card)
   - Extracts job details from the list view

6. extract_applicants_from_right_pane(driver)
   - Extract number of applicants from the right preview panel

7. get_linkedin_jobs()
   - Launches the driver
   - Loads the Linkedin search URL
   - Closes the modal if shown
   - Scrolls to load jobs
   - Loops through each job car and
     - Extracts title, company, location, posted time
     - Gets the job URL
     - Opens each job in a new tab to extracts applicant count
   - Store final data in a pandas data frame  

## Step 2: Download USCIS H1B Sponsorship Data
Source: USCIS H-1B Disclosure Dataset
Load it into your script as a CSV file
Normalize company names (strip punctuation, lowercase, etc.)

## Step 3: Filter Jobs
This keeps jobs:
From companies that have sponsored H1B visas in the past
With less than 80 applicants

## Notes on Authentication
To bypass LinkedIn’s login wall:
Use --user-data-dir and --profile-directory to open your real Chrome session
OR manually inject cookies (li_at, JSESSIONID) if you're experienced

## This project is for academic/demo purposes only. Automated scraping of LinkedIn violates their terms of service.

## Future Improvements
🌍 GUI with Streamlit to get user input and benefit more international students

📊 Publish on cloud service to save computation power and reduce run time

## Disclaimer
This prototype is built for a senior project course and is not intended for production use. Please respect website terms and only use for educational/research purposes.
