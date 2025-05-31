import streamlit as st
import urllib.parse
from scraper import get_linkedin_jobs
from h1b import load_h1b_employers, filter_h1b_jobs, filter_by_applicant_count

st.set_page_config(layout="wide")
st.title("LinkedIn H1B Job Scraper")

job_title = st.text_input("Enter job title", placeholder="e.g. Data Scientist")
location = st.text_input("Enter U.S. state (e.g. California, New York)", placeholder="e.g. California")

experience_options = {
    "Internship": "1",
    "Entry Level": "2",
    "Associate": "3",
    "Mid-Senior": "4",
    "Director": "5",
    "Executive": "6"
}
selected_experience = st.selectbox("Select experience levels", options=list(experience_options.keys()), index=1)
experience_codes = experience_options[selected_experience]

if st.button("Scrape LinkedIn Jobs"):
    if not job_title.strip() or not location.strip():
        st.warning("Please enter both a job title and a state")
    else:
        with st.spinner("Scraping jobs from LinkedIn..."):
            query_title = urllib.parse.quote(job_title.strip())
            query_location = urllib.parse.quote(location.strip())

            jobs_df = get_linkedin_jobs(query_title, query_location, experience_codes)
            h1b_employers = load_h1b_employers("employer2024.csv")
            filtered_df = filter_h1b_jobs(jobs_df, h1b_employers)
            filtered_df = filter_by_applicant_count(filtered_df, max_applicants=80)

        if not filtered_df.empty:
            st.success(f"Found {len(filtered_df)} jobs from H1B-sponsoring companies in {location}.")
            st.dataframe(filtered_df)
            st.download_button("Download CSV", filtered_df.to_csv(index=False), "h1b_jobs.csv")
        else:
            st.warning(f"No H1B jobs found for '{job_title}' in '{location}'.")