# On importe les librairies a scraper 

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, datetime
import pandas as pd
from Job import Job

def format_jobs(jobs_array):
    jobs_data = []  # On crée un tableau pour stocker les informations sur les emplois
    for job in jobs_array:  # Puis on fait une boucle à travers tous les emplois dans le tableau
        if job:  # si l'emploi n'est pas nul (ou vide) on crée un dictionnaire avec des informations sur l'emploi en utilisant les méthodes de l'objet
            job_dict = {
                'Url': job.get_url(),
                'Title': job.get_title(),
                'Company Name': job.get_company_name(),
                'Type': job.get_type(),
                'Location' : job.get_location(),
                'Description': job.get_description()
            }
            jobs_data.append(job_dict)  # puis on ajoute le dictionnaire au tableau des données d'emplois

    return jobs_data  # et on renvoye le tableau des données d'emplois


# Cette ligne de code est utilisée pour ouvrir le pilote de chrome.
# Comme il s'agit de sites Web contenant des javascripts, nous allons créer un lecteur de chrome virtuel afin que la sécurité du site Web ne détecte pas que nous sommes un robot.

options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
list_of_jobs = []

# Dans cette section, nous allons coller le lien que nous allons scraper.  
# time.sleep est utilisé pour ajouter un délai dans le site Web. On peut donc l'augmenter ou le diminuer en fonction de nos besoins et de notre connexion Internet.
# time.sleep (5) signifie un délai de 5 secondes.

driver.get('https://www.jobteaser.com/fr/job-offers?location=India..India&locale=en,fr')
time.sleep(5)

# Cette ligne est utilisée pour créer la pagination, car nous avons remarqué que notre site Web a 50 pages, donc notre gamme est de 1 à 51. 
# Car dans python 1 à 51 signifie 1 à 50 car le dernier chiffre python n'est pas pris en compte.

for i in range(1,51):
    try:
        Results = driver.find_elements_by_xpath('//a[@data-track-marketing="click:open_single_offer"]')
        for data in Results:
            #Cette ligne de code est utilisée pour ouvrir chaque job un par un afin que nous puissions collecter les données.
            #Donc simplement, c'est l'ouverture de chaque job un par un.

            url = data.get_attribute('href')
            parent = driver.window_handles[0]
            driver.execute_script(f'''window.open("{url}","_blank");''')
            chld = driver.window_handles[1]
            driver.switch_to.window(chld)
            time.sleep(2)

            try:
                # On va trouver l'élément 'body' dans la page web chargée dans le navigateur.
                Item = driver.find_element_by_xpath('//body')

                # Puis, on va trouver l'élément 'h1' à l'intérieur de l'élément 'body' et récupérer son texte.
                title = Item.find_element_by_xpath('//h1').text

                # Ensuite, on va rouver l'élément 'a' qui a un attribut 'data-e2e' de valeur 'jobad-DetailView__CompanyLink'
                # à l'intérieur de l'élément 'body', et récupérer le texte du paragraphe 'p' qu'il contient (si présent).
                company_name = Item.find_element_by_xpath('//a[@data-e2e="jobad-DetailView__CompanyLink"]/p').text \
                    if Item.find_element_by_xpath('//a[@data-e2e="jobad-DetailView__CompanyLink"]/p') else None

                # Puis, on va trouver l'élément 'p' qui a les classes CSS suivantes : 'jds-Text__3KLTn', 'jds-Text--subhead-small__Up-Vq',
                # 'jds-Text--resetSpacing__15GE_', 'jds-Text--weight-normal__1XPqo' et 'jo-Heading--summary__22nW8' à l'intérieur de l'élément 'body'.
                # Ensuite, on va récupérer le texte de cet élément, puis le diviser en sous-chaînes en utilisant le caractère '- ' comme séparateur.
                more_details = Item.find_element_by_xpath('//p[@class="jds-Text__3KLTn jds-Text--subhead-small__Up-Vq jds-Text--resetSpacing__15GE_ jds-Text--weight-normal__1XPqo jo-Heading--summary__22nW8"]').text
                single_detail = more_details.split('- ')

                # Si la variable 'single_detail' n'est pas vide, on va affecter sa première sous-chaîne à la variable 'type', et sa deuxième sous-chaîne à la variable 'location'.
                type = single_detail[0] if single_detail else None
                location = single_detail[1] if single_detail else None

                # On va trouver l'élément 'div' qui a les classes CSS suivantes : 'jds-Text__3KLTn', 'jds-Text--normal__397yB', et 'jds-RichText__2o_RW'
                # à l'intérieur de l'élément 'body'.
                # Puis on va récupérer le texte de cet élément, puis remplacer tous les caractères de nouvelle ligne par des espaces dans cette chaîne
                description = Item.find_element_by_xpath('//div[@class="jds-Text__3KLTn jds-Text--normal__397yB jds-RichText__2o_RW"]')\
                                .text.replace("\n", " ") if Item.find_element_by_xpath('//div[@class="jds-Text__3KLTn jds-Text--normal__397yB jds-RichText__2o_RW"]') else None

                # Enfin on va créer un nouvel objet Job avec les valeurs des variables récupérées précédemment,
                # et ajouter cet objet à la liste 'list_of_jobs'.
                job = Job(url, title, company_name, type, location, description)
                list_of_jobs.append(job)
            except:
                pass

            driver.close()
            driver.switch_to.window(parent)   




        # Cette ligne de code est utilisée pour cliquer sur la page suivante après avoir récupéré tous les travaux de cette page.
        # Donc on passe à la page suivante pour le scraping de la page suivante.

        Next_Page = driver.find_element_by_xpath('//a[@data-icon="chevronRight|alone"]')
        Next_Page.click()
        time.sleep(5)
    
    except:
        break



# Cette ligne de code est utilisée pour créer un fichier csv.
# Enfin on ajoute l'option "datetime" pour éviter la saisie de données à chaque scraping.


print(len(list_of_jobs))
df = pd.DataFrame(format_jobs(list_of_jobs))
date = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
df.to_csv(f'csvs/JobSite_{date}.csv',index=False)
print('Les datas sont sauvegardé dans le CSV!')
driver.quit()