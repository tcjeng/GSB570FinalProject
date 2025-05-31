import pandas as pd
import re

def load_h1b_employers(filepath = "employer2024.csv"):
    df = pd.read_csv(filepath)
    return set(df["Employer"].str.lower().str.strip())

def is_rough_match(company_name, employers):
    return any(company_name in employer for employer in employers)

def filter_h1b_jobs(jobs_df, h1b_employers):
    jobs_df["company_clean"] = jobs_df["Company"].fillna('').str.lower().str.strip()
    jobs_df["h1b_match"] = jobs_df["company_clean"].apply(lambda x: is_rough_match(x, h1b_employers))
    filtered = jobs_df[jobs_df["h1b_match"]]
    return filtered.drop(columns=["company_clean", "h1b_match"]).reset_index(drop=True)

def extract_applicant_count(text):
    text = str(text).lower().strip()
    
    if "first" in text:
        match = re.search(r'first (\d+)', text)
        return int(match.group(1)) if match else None
    elif "over" in text:
        match = re.search(r'over (\d+)', text)
        return int(match.group(1))  # or return a high number like 999 if you want to always exclude
    else:
        match = re.search(r'(\d+)', text)
        return int(match.group(1)) if match else None

def filter_by_applicant_count(df, max_applicants=80):
    df["applicant_count"] = df["Applicants"].apply(extract_applicant_count)
    df = df[df["applicant_count"] < max_applicants]
    df = df.drop(columns=["applicant_count"]).reset_index(drop=True)
    return df