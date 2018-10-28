import csv
import requests
from bs4 import BeautifulSoup

def WriteJobsListInCSVFile(job):

    try:
        csv_writer.writerow(
            {
                'Job Title': job['job_title_text'],
                 'Company Name': job['company_name'],
                 'Education': job['education'],
                 'Experience': job['experience'],
                 'Deadline': job['deadline'],
                 'Job Link': job['job_link'],
             }
        )
    except:
        print('Exception Occurred!!! Skip for now and Keep going.')



main_site = 'http://jobs.bdjobs.com/'
print('BDJobs Job Category ID List:\n')

print('\n----------------------------------------------\n')
print('Accounting/Finance ID: 1')
print('Agro (Plant/Animal/Fisheries) ID: 26')
print('Bank/ Non-Bank Fin. Institution ID: 2')
print('Beauty Care/ Health & Fitness ID: 21')
print('Commercial/Supply Chain ID: 3')
print('Customer Support/Call Centre ID: 16')
print('Data Entry/Operator/BPO ID: 15')
print('Design/Creative ID: 18')
print('Driving/Motor Technician ID: 25')
print('Education/Training ID: 4')
print('Engineer/Architects ID: 5')
print('Electrician/ Construction/ Repair ID: 23')
print('Garments/Textile ID: 6')
print('Gen Mgt/Admin ID: 7')
print('Hospitality/ Travel/ Tourism ID: 20')
print('HR/Org. Development ID: 17')
print('IT & Telecommunication ID: 8')
print('Law/Legal ID: 22')
print('Marketing/Sales ID: 9')
print('Media/Ad./Event Mgt. ID: 10')
print('Medical/Pharma ID: 11')
print('NGO/Development ID: 12')
print('Others ID: 10')
print('Production/Operation ID: 19')
print('Research/Consultancy ID: 13')
print('Secretary/Receptionist ID: 14')
print('Security/Support Service ID: 24')
print('\n----------------------------------------------\n')

print('[-1 For All Category]')
category_id = int(input('~$ '))

print('Input Search Keyword: [You Can Leave It Blank To Get All Jobs For This Category]')
search_keyword = input('~$ ')

print('Input The CSV File Name : [Default: bdjobs-job-list.csv]')
csv_file_name = input('~$ ')

if not csv_file_name:
    csv_file_name = 'bdjobs-job-list.csv'

if csv_file_name.find(".csv") == -1:
    csv_file_name = csv_file_name + '.csv'

# Job search url
url = 'http://jobs.bdjobs.com/jobsearch.asp?fcatId={}'.format(category_id)

# Post data 'dictionary' for different crieteria.
# 'fcat' for 'Job Category'
# 'pg' for 'Pagination'. Value is 1 by default.
# 'txtsearch' for 'Specific Jobs Search for This Category'

post_data = {
             'fcat': category_id,
             'fcatId':category_id,
             'hidJobSearch': 'JobSearch',
             'pg': '1',
             'txtsearch': search_keyword,
             }

# Open a CSV File With 'Write' Mode
jobs_list_csv_file = open(csv_file_name, 'w', newline='')

csv_column_names = ['Job Title', 'Company Name', 'Education', 'Experience', 'Deadline', 'Job Link']

# Creating CSV Writer
csv_writer = csv.DictWriter(jobs_list_csv_file, fieldnames=csv_column_names)

# Write Column Name
csv_writer.writeheader()

csv_writer.writerow(
    {'Job Title': '', 'Company Name': '', 'Education': '', 'Experience': '', 'Deadline': '', 'Job Link': ''})

# At Least 1 Page Should Be Available
page_no = 1
max_page_no = 1

# Total Jobs Count
total_jobs = 0

while page_no <= max_page_no:
    print('Collecting Jobs Data From Page {0} Where Page Size Is 20.'.format(page_no))

    # Assign new page no.
    post_data['pg'] = page_no

    response_data = requests.post(url, data=post_data)

    html = BeautifulSoup(response_data.content, 'html.parser')

    contents = html.find_all('div', {'class': ['norm-jobs-wrapper', 'sout-jobs-wrapper']})

    if page_no == 1:
        max_page_no = html.find('div', {'id': 'topPagging'}).find_all('li')[-1].text.strip().replace('.', '')
        max_page_no = int(max_page_no)

    for content in contents:
        # A dictionary For Passing Data To WriteJobsListInCSVFile Function
        jobs_dict = {};

        # Find Education
        education_div = content.find('div', {'class': 'edu-text-d'})
        # As Sometimes Education Info Doesn't Exist
        if education_div:
            # As Some Are Given As Plain Text And Some Are Given As List (<ul>)
            education_div_li = education_div.find_all('li')
            if education_div_li:
                for count, li in enumerate(education_div_li):
                    # No Line Break Required Before First Line
                    if not count:
                        education = li.text.strip()
                    else:
                        education += '\n' + li.text.strip()
            else:
                education = education_div.text.strip()
        else:
            education = ''

        # Fetching desired content using its tag and class
        job_title = content.find('div', {'class': 'job-title-text'})
        jobs_dict['job_link'] = main_site + job_title.find('a', {'href': True})['href']
        jobs_dict['job_title_text'] = job_title.text.strip()
        jobs_dict['company_name'] = content.find('div', {'class': 'comp-name-text'}).text.strip()
        jobs_dict['education'] = education
        jobs_dict['experience'] = content.find('div', {'class': 'exp-text-d'}).text.strip()
        jobs_dict['deadline'] = content.find('div', {'class': 'dead-text-d'}).text.strip()

        # Call WriteJobsListInCSVFile Function
        WriteJobsListInCSVFile(jobs_dict)

        # Increment total_jobs
        total_jobs += 1

    # Increment page_no.
    page_no += 1

jobs_list_csv_file.close()

print('\nBDJobs Data Scraping Completed Successfully\n')

# Total Jobs
print('Total Jobs Found For Desired Category: {}\n'.format(total_jobs))

print('All Jobs Saved In {} file.'.format(csv_file_name))


def SearchBefore(value, a):
    pos_a = value.find(a)
    if pos_a == -1:
        return ""
    return value[0:pos_a]

def SearchAfter(value, a):
    pos_a = value.rfind(a)
    if pos_a == -1:
        return ""
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= len(value):
        return ""
    return value[adjusted_pos_a:]