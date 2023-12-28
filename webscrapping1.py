
from bs4 import BeautifulSoup

#BeautifulSoup =  permettre de faire le parsin et qui nous permettra de recuperer chaque element html

from selenium import webdriver

import pandas as pd

from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

import time

 

#initialiser Selenium with ChromeDriver

driver = webdriver.Chrome()

#Navigate to the provided

url = 'https://www.apec.fr/candidat/recherche-emploi.html/emploi?lieux=711&typesConvention=143684&typeConvention=143687&page=0'

driver.get(url)

#Wait for the page to load

wait = WebDriverWait(driver, 10)

page = 1

job_count = 1

job_posts = list()

#Compteur de  nombre de posts scraped

previous_num_posts = 0

 

while True:

    try:

        #Wait until button Suiv appears before clicking

        button = WebDriverWait(driver, 20).until(

            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Suiv.")]'))

        )

        button.click()

        #Give some time for new content to load

        time.sleep(10)

        print(f'Button clicked {page} times')

        page +=1

    except Exception as e:

        print(f'Error encountered:{e}')

    #parse the page content with BeautifulSoup

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    print('Scraping started ...')

    #Loop through html source based on specified div element

    for card in soup.find_all('div', class_='card-offer__text'):

        company = card.find('p', class_='card-offer__company').text.strip()

        titre = card.find('h2', class_='card-title').text.strip()

        description = card.find('p', class_='card-offer__description').text.strip()

        details = card.find_all('ul', class_='details-offer')

        salary = details[0].find('img', alt='Salaire texte').parent.text.strip() if len(details[0]) > 1 else 'N/A'

        contrat_type = details[1].find('img', alt='type de contrat').parent.text.strip() if len(details[1]) > 1 else 'N/A'

        location = details[1].find('img', alt='localisation').parent.text.strip() if len(details[1]) > 1 else 'N/A'

        Date =  details[1].find('img', alt='date de publication').parent.text.strip() if len(details[1]) > 1 else 'N/A'

        print(f'Page{page}')

        print(f'Company:{company}\nTitle: {titre}\nContrat type:{contrat_type}\nSalary: {salary}\nLocation:{location}\nDate:{Date}')

 

        job_posts.append({
            'Company': company,
            'Title': titre,
            'Salary': salary,
            'Contrat de type': contrat_type,
            'Location': location,
            'Publication Date':Date
        })
        job_count+=1
    #len retourne le nombre des elements    
    if len(job_posts)==previous_num_posts:
        print('No new posts found . Existing loop.')
        break
    previous_number=len(job_posts)
    page+=1
#Convert the job post list of dictionaries to a Dataframe
df=pd.DataFrame(job_posts)
print(f'Head rows\n{df.head()}')
print(f'Tail rows\n{df.tail()}')
print('Saving data ...')
df.to_csv('apec.csv', index= False)
#Close the browser
driver.quit()
print('Browser closed')