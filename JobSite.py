# On importe les librairies a scraper 

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, datetime
import pandas as pd




# Cette ligne de code est utilisée pour ouvrir le pilote de chrome.
# Comme il s'agit de sites Web contenant des javascripts, nous allons créer un lecteur de chrome virtuel afin que la sécurité du site Web ne détecte pas que vous êtes un robot.

options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
listofdict = list()


# Dans cette section, nous allons coller le lien que vous voulez effacer.  
# time.sleep est utilisé pour ajouter un délai dans le site Web. Vous pouvez donc l'augmenter ou le diminuer en fonction de vos besoins et de votre connexion Internet.
# time.sleep (10) signifie un délai de 10 secondes.

driver.get('https://www.jobteaser.com/fr/job-offers')
time.sleep(10)

# Cette ligne est utilisée pour créer la pagination, car vous avez remarqué que votre site Web a 50 pages, donc notre gamme est de 1 à 51. 
# Comme dans python 1 à 51 signifie 1 à 50 car le dernier chiffre pyhton n'est pas pris en compte.

for i in range(1,51):
    
# Cette ligne de code est utilisée pour trouver le nombre de jobs dans une page.
    try:
        Results = driver.find_elements_by_xpath('//a[@data-track-marketing="click:open_single_offer"]')
        for data in Results:

            #Cette ligne de code est utilisée pour ouvrir chaque job un par un afin que nous puissions collecter les parties "description" et "remmaining".
            #Donc simplement, c'est l'ouverture de chaque job un par un.

            datadict = dict()
            Url = data.get_attribute('href')
            datadict['URL'] = Url
            parent = driver.window_handles[0]
            driver.execute_script(f'''window.open("{Url}","_blank");''')
            chld = driver.window_handles[1]
            driver.switch_to.window(chld)
            time.sleep(5)




            #La ligne de code ci-dessous permet de trouver tous les détails du titre de l'emploi, du nom de la société, comme vous le voyez dans le nom datadict['Company name'].
            #signifie trouver le nom de la société et de la même manière pour tous.

            try:
                Item = driver.find_element_by_xpath('//body')
                datadict['Job Title'] = Item.find_element_by_xpath('//h1').text

                try:
                    datadict['Company name'] = Item.find_element_by_xpath('//a[@data-e2e="jobad-DetailView__CompanyLink"]/p').text
                except:
                    datadict['Company name'] =""

                More_Detail =Item.find_element_by_xpath('//p[@class="jds-Text__3KLTn jds-Text--subhead-small__Up-Vq jds-Text--resetSpacing__15GE_ jds-Text--weight-normal__1XPqo jo-Heading--summary__22nW8"]').text
                Single_Detail = More_Detail.split('- ')

                try:
                    datadict['Type']= Single_Detail[0]
                except:
                    datadict['Type']= ""

                try:
                    datadict['Location']= Single_Detail[1]
                except:
                    datadict['Location']= ""

                try:
                    datadict['Job Description'] = Item.find_element_by_xpath('//div[@class="jds-Text__3KLTn jds-Text--normal__397yB jds-RichText__2o_RW"]').text
                except:
                    datadict['Job Description'] =""
                    
                print(datadict)
                listofdict.append(datadict)

            except:
                pass

            driver.close()
            driver.switch_to.window(parent)   




        # Cette ligne de code est utilisée pour cliquer sur la page suivante après avoir récupéré tous les travaux de cette page...
        # Donc on passe à la page suivante pour le scraping de la page suivante.

        Next_Page = driver.find_element_by_xpath('//a[@data-icon="chevronRight|alone"]')
        Next_Page.click()
        time.sleep(5)
    
    except:
        break



# Cette ligne de code est utilisée pour créer un fichier csv.
# J'ai ajouté l'option date-heure pour éviter la saisie de données à chaque scraping.

df = pd.DataFrame.from_dict(listofdict)  
date = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
df.to_csv(f'JobSite_{date}.csv',index=False)
print('Les datas sont sauvegardé dans le CSV!')
driver.quit()