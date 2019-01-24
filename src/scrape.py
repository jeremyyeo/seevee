import os
import sys
from bs4 import BeautifulSoup, NavigableString
import requests
import json
import re
import pprint

terminal_columns, terminal_rows = os.get_terminal_size(0)
pp = pprint.PrettyPrinter(indent=2)

job_url_template = "https://www.seek.co.nz/job/{}"
search_url_template = "https://www.seek.co.nz/administrator-jobs/in-All-Wellington?sortmode=ListedDate&page={}"

initial_search_page = "https://www.seek.co.nz/administrator-jobs/in-All-Wellington?page=1&sortmode=ListedDate"
job_page = "https://www.seek.co.nz/job/38034218"  # Also test 38162642

page = requests.get(initial_search_page)

soup = BeautifulSoup(page.content, "html.parser")
x = soup.find_all("script", {"data-automation": "server-state"})[0]
y = str(x.get_text())
data = re.findall("window.SEEK_REDUX_DATA =(.+?});", y)
ls = []
if data:
    ls = json.loads(data[0])
    number_of_pages = int(ls["results"]["pagination"]["lastPage"])

# if ls:
#     print(ls["results"].keys())
# if number_of_pages:
#     pp.pprint(number_of_pages)
#     for page_number in range(1, number_of_pages):
#         if page_number == 1:
#             print("yes")

number_of_jobs = len(ls["results"]["results"]["jobs"])
job_id_all = []
for i in range(0, number_of_jobs):
    job_id_all.append(ls["results"]["results"]["jobs"][i]["id"])

# for i in job_id_all:
#     print(i)

job = ls["results"]["results"]["jobs"][2]
pp.pprint(job)
job_id = job["id"]
# job_id = 38162642

# Job attributes from JSON.
job_title = job["title"]
job_work_type = job["workType"]
job_advertiser = job["advertiser"]["description"]
job_salary = job["salary"]
job_area = job["area"]
job_location = job["location"]
job_classification = job["classification"]
job_sub_classification = job["subClassification"]
job_custom_template = job["hasCustomTemplate"]
job_listing_date = job["listingDate"]

# Job description available from job page.
job_page = requests.get(job_url_template.format(job_id))
job_soup = BeautifulSoup(job_page.content, "html.parser")
job_description = job_soup.find_all("div", {"data-automation": "jobDescription"})[0]
job_description_text = job_description.get_text()
line_count = job_description_text.count("\n") + 1
line_string = (
    (str(line_count) + " LINES") if line_count > 1 else (str(line_count) + " LINE")
)
job_description_text = job_description_text.split("\n")


# print("{:^{width}}".format("", width=terminal_columns))
# print("{:^{width}}".format("JOB ID: " + str(job_id), width=terminal_columns))
# print("{:^{width}}".format("JOB DESCRIPTION", width=terminal_columns))
# print("{:^{width}}".format(line_string, width=terminal_columns))
# print("{:^{width}}".format("", width=terminal_columns))

# print(job_description_text[line_count - 1])
