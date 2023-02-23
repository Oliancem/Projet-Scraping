import requests
import pandas as pd
import sqlalchemy

def get_jobs():
    headers = {
        'authority': 'apigw.jobteaser.com',
        'accept': 'application/json',
        'accept-language': 'fr',
        'content-type': 'application/json',
        'origin': 'https://www.jobteaser.com',
        'referer': 'https://www.jobteaser.com/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',#Bypass le fait d'etre un bot 
    }

    json_data = {
        'query': '',
        'page_size': 1000,
        'page_token': '0',
        'sponsored_results_max': 2,
        'career_center_study_levels': [],
        'contract_types': [
            'alternating',
            'alternating',
            'berufsbegleitendes_studium',
            'job',
            'cdd',
            'cdi',
            'graduate_program',
            'vie',
            'part_time',
            'stage',
            'internship',
            'werkstudent',
            'thesis',
            'thesis',
        ],
        'school_ids': [
            '0',
        ],
        'curriculum_ids': None,
    }

    all_jobs = []
    while True:
        response = requests.post(
            'https://apigw.jobteaser.com/jobteaser.job_ad.v2alpha/JobAdService/SearchJobAds',
            headers=headers,
            json=json_data,
        )

        if response.status_code == 500:
            break

        response = response.json()
        json_data['page_token'] = response['next_page_token']
        for ad in response['job_ads']:
            title=company=type_=location=category=description=''
            try:
                title = ad['title']
                company = ad['company']['name']
                type_ =  ad['contract']['type']
                location =  ", ".join( ad['location'].values() )
                category = ad['remote_type']
                description = ad['description']
            except Exception as e:
                pass

            all_jobs.append(
                    {
                        'Job title': title,
                        'Company name': company,
                        'Type':type_,
                        'Location':location,
                        'Category': category,
                        'Job description': description
                    }                
                )

    return all_jobs

# On choppe la liste de jobs
print('Scraping jobs!')
jobs = get_jobs()

# Sauvegarder dans le fichier CSV
print('Data exporté dans le CSV.')
df = pd.DataFrame(jobs)
df.to_csv('jobs.csv', index=False)

# Sauvergarder dans la base de donées
print("Exporter dans la base de données.")
database_username = 'root'
database_password = 'r=6h6i.K;f9G6V'
database_ip       = '127.0.0.1'
database_name     = 'jobs_db'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))
df.to_sql(con=database_connection, name='jobs', if_exists='replace')

print("C'est tout bon!!")