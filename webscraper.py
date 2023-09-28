from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def getData(moviename = "bahubali",save = True):

    driver = webdriver.Chrome()

    url = "https://www.rottentomatoes.com/"
    driver.get(url)

    search = driver.find_element(By.CLASS_NAME,"search-text")
    search.send_keys(moviename)
    search.send_keys(Keys.RETURN)

    results = driver.find_elements(By.XPATH, '//search-page-media-row')
    reviewlinks = []

    for result in results:
        score = result.get_attribute('tomatometerscore')
        if len(score) > 0:
            link = result.find_element(By.XPATH,'.//a[@slot ="thumbnail"]')
            reviewlinks.append(link.get_attribute('href') + "/reviews")

    print(len(reviewlinks))



    def getReviews(result,nameslist,publicationlist,reviewtextlist):
        doc = BeautifulSoup(result,"lxml")
        reviewtable = doc.find_all("div",class_ = "review-row")

        #the table element
        for reviewrow in reviewtable:
            reviewdata = reviewrow.find("div",class_ = "review-data")
            nameNpublication = reviewdata.find("div",class_= "reviewer-name-and-publication")
            reviewelement = reviewrow.find("div",class_ = "review-text-container")

            # the name of reviewer and publication
            name = nameNpublication.find("a",class_= "display-name")
            publication = nameNpublication.find("a",class_= "publication")

            # the reviews
            review = reviewelement.find("p",class_ = "review-text")

            nametext = name.string.strip()
            nameslist.append(nametext)

            publicationname = publication.string.strip()
            publicationlist.append(publicationname)

            #reviewtext = review.string.strip()
            reviewtextlist.append(review.string)


    names = []
    publications = []
    reviews = []

    for link in reviewlinks:

        driver.get(link)
        result = driver.page_source
        getReviews(result,names,publications,reviews)
        # beautiful soup part collecting the reviews
        try:
            next = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "next"))
            )
            while next != None:
                next = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "next"))
                )
                next.click()
                time.sleep(3)
                result = driver.page_source
                getReviews(result,names,publications,reviews)    

        except:
            print("done")

    print("the number of names are: " + str(len(names)))
    print("the number of publications are: " + str(len(publications)))
    print("the number of reviews are: " + str(len(reviews)))

    #print(names[0:100])

    driver.quit()

    df = pd.DataFrame(list(zip(names,publications,reviews)),columns=['name','publishers','review'])

    if save:
        df.to_csv(moviename + '.csv')

    #print(df.head())

    return df

    

