import csv
import requests
from bs4 import BeautifulSoup

def SearchBetween(value, a, b):
    pos_a = value.find(a)
    if pos_a == -1:
        return ""
    pos_b = value.rfind(b)
    if pos_b == -1:
        return ""
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b:
        return ""
    return value[adjusted_pos_a:pos_b]

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

def ProcessRequestData():

    response_data = requests.post(url, data=post_data)
    html = BeautifulSoup(response_data.content, 'html.parser')
    return html

def WriteMoviesListInCSVFile(movie):

    try:
        csv_writer.writerow(
            {
                'Movie Title': movie['movie_name'],
                'Release Year': movie['release_year'],
                'Runtime': movie['runtime'],
                'Genre': movie['genre'],
                'Rating': movie['rating'],
                'Metascore': movie['metascore'],
                'Votes': movie['votes'],
                'Gross': movie['gross'],
                'IMDB Link': movie['imdb_url'],
             }
        )
    except:
        print('Exception Occurred!!! Skip for now and Keep going.')



main_site = 'https://www.imdb.com/'

soft_cat_dict =	{
    "1": "alpha,asc",
    "2": "user_rating,desc",
    "3": "num_votes,desc",
    "4": "boxoffice_gross_us,desc",
    "5": "runtime,desc",
    "6": "release_date,desc",
}

print('Scrap IMBD Movies Data For Given Year')
# print('\n----------------------------------------------\n')
print('\nSoft Movies By\n-------------------------------------\nAlphabetically(1)\nIMDb Rating(2)\nNumber of Votes (3)\nBox Office (4)\nRuntime (5)\nRelease Date (6)\n-------------------------------------\n')

print('[Provide Your Desire Year To Get All Movies Of That Year]')
release_year = int(input('~$ '))

print('Provide Sorting Category ID: [Default: Sort By Number of Votes]')
cat_id = input('~$ ')

if not cat_id:
    cat_id = "3"

# INDB Movie url
url = 'https://www.imdb.com/search/title?release_date={0}&sort={1}'.format(release_year, soft_cat_dict[cat_id])

# Post data 'dictionary' for different crieteria.
# 'release_date' for 'Movie Release Year'
# 'page' for 'Pagination'. Value is 1 by default.

post_data = {
             'release_date': release_year,
             'page': '1',
             }

html = ProcessRequestData()
temp_no_of_movies = html.find('div', {'class': 'desc'}).text.strip()

no_of_movies = ""

if temp_no_of_movies.find("of") == -1:
    no_of_movies = SearchBefore(temp_no_of_movies, ' titles')
else:
    no_of_movies = SearchBetween(temp_no_of_movies, 'of ', ' titles')

print('\n{0} Movies Found For {1}\n'.format(no_of_movies,release_year))

print('[Provide No Of Movies You Want To Scrap]')
movies_to_pick = int(input('~$ '))

print('Input The CSV File Name : [Default: imdb-movie-list.csv]')
csv_file_name = input('~$ ')

if not csv_file_name:
    csv_file_name = 'imdb-movie-list.csv'

if csv_file_name.find(".csv") == -1:
    csv_file_name = csv_file_name + '.csv'

# Open a CSV File With 'Write' Mode
movies_list_csv_file = open(csv_file_name, 'w', newline='')

csv_column_names = ['Movie Title', 'Release Year', 'Runtime', 'Genre', 'Rating', 'Metascore', 'Votes', 'Gross', 'IMDB Link']
# Creating CSV Writer
csv_writer = csv.DictWriter(movies_list_csv_file, fieldnames=csv_column_names)

# Write Column Name
csv_writer.writeheader()

csv_writer.writerow(
    {'Movie Title': '', 'Release Year': '', 'Runtime': '', 'Genre': '', 'Rating': '', 'Metascore': '', 'Votes': '', 'Gross': '','IMDB Link': ''})

# At Least 1 Page Should Be Available
page_no = 1
max_page_no = 1

# Total Jobs Count
total_movies = 0

while total_movies < movies_to_pick :

    if total_movies < movies_to_pick:
        print('Collecting Movies Data From Page {0} Where Page Size Is 50.'.format(page_no))

        # Assign new page no.
        post_data['page'] = page_no

        html = ProcessRequestData()

        contents = html.find_all('div', {'class': ['lister-item-content']})

        for content in contents:
            # A dictionary For Passing Data To WriteMoviesListInCSVFile Function
            movies_dict = {};

            # Fetching desired content using its tag and class
            imdb_url = content.find('a', {'href': True})['href']
            if not imdb_url.startswith(main_site):
                imdb_url = main_site + imdb_url
            movies_dict['imdb_url'] = imdb_url
            movies_dict['movie_name'] = content.find('a', {'href': True}).text.strip()
            movies_dict['release_year'] = content.find('span', {'class': 'lister-item-year'}).text.strip()
            try:
                movies_dict['runtime'] = content.find('span', {'class': 'runtime'}).text.strip()
            except:
                movies_dict['runtime'] = 'N/A'
            try:
                movies_dict['genre'] = content.find('span', {'class': 'genre'}).text.strip()
            except:
                movies_dict['genre'] = 'N/A'
            try:
                movies_dict['rating'] = content.find('div', {'class': 'ratings-imdb-rating'})['data-value']
            except:
                movies_dict['rating'] = 'N/A'
            try:
                movies_dict['metascore'] = content.find('span', {'class': 'metascore'}).text.strip()
            except:
                movies_dict['metascore'] = 'N/A'
            try:
                movies_dict['votes'] = content.find('span', {"name": 'nv'}).text.strip()
            except:
                movies_dict['votes'] = 'N/A'

            try:
                get_vote_span = content.find('span', {"name": 'nv'})
                movies_dict['gross'] = get_vote_span.find_next_sibling('span', {"name": 'nv'}).text.strip()
            except:
                movies_dict['gross'] = 'N/A'

            if total_movies <= movies_to_pick:
                # Call WriteMoviesListInCSVFile Function
                WriteMoviesListInCSVFile(movies_dict)
                # Increment total_jobs
                total_movies += 1

            else:
                break

        # Increment page_no.
        page_no += 1
    else:
        break

movies_list_csv_file.close()

print('\nIMDB Data Scraping Completed Successfully\n')

# Total Jobs
print('As You Desired {0} Movies Scraped Of {1}\n'.format((total_movies), release_year))

print('All Jobs Saved In {} file.'.format(csv_file_name))
