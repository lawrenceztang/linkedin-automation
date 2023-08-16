import random

from selenium import webdriver
import os
import time
import csv

message = "I'd like to connect!"
companies_file = "companies_short.csv"
day_limit = 50
limit_per_company = 50
password = "MY_PASSWORD"
username = "MY_USERNAME"
people_query = "?facetSchool=18314"
webdriver_path = "C:/Users/larry/Downloads/chromedriver_win32/chromedriver.exe"


def get_companies_list():
    out = []
    with open(companies_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for i, row in enumerate(reader):
            out.append(row[0])
    return out

def scroll_down(driver):
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def replace_message(company, driver, name):
    new_message = message
    new_message = new_message.replace("[company]", company)
    new_message = new_message.replace("there", name)
    return new_message

def login(driver):
    driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    input = driver.find_element_by_xpath("//input[@id='username']")
    input.send_keys(username)
    input = driver.find_element_by_xpath("//input[@id='password']")
    input.send_keys(password)
    driver.find_element_by_xpath("//button[@class='btn__primary--large from__button--floating']").click()

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("user-data-dir=%s" % os.path.join(os.path.dirname(os.path.realpath(__file__)), "selenium"))
    driver = webdriver.Chrome(executable_path=webdriver_path, chrome_options=options)
    driver.get("https://www.linkedin.com")

    time.sleep(1)

    day_count = 0

    for company in get_companies_list():
        count_bad = 0
        print("\n" + company)
        driver.get(f"https://www.linkedin.com/search/results/all/?keywords={company}&origin=GLOBAL_SEARCH_HEADER&sid=.wg)")
        time.sleep(4)
        try:
            a = driver.find_element_by_xpath(
                "//a[@class='app-aware-link  search-nec__hero-kcard-v2-link-wrapper link-without-hover-state link-without-visited-state t-normal t-black--light']").get_attribute(
                "href")
            # a = "https://www.linkedin.com/company/d.-e.-shaw-&-co./"
        except:
            continue

        driver.get(a + "/people/")


        time.sleep(4)

        company_count = 0
        while company_count < limit_per_company and day_count < day_limit:
            list = driver.find_elements_by_xpath("//span[text()='Connect']/..")
            if len(list) == 0:
                try:
                    driver.find_element_by_xpath("//span[text()='Show more results']").click()
                except:
                    pass
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(.5)
            else:
                for elem in list:
                    if company_count >= limit_per_company:
                        break
                    if day_count >= day_limit:
                        time.sleep(86400)
                    try:
                        elem.click()
                    except:
                        
                        continue
                    time.sleep(1)
                    name = driver.find_element_by_xpath("//strong").text.split(" ")[0]
                    try:
                        driver.find_element_by_xpath("//button[@aria-label='Add a note']").click()
                    except:
                        driver.refresh()
                        continue
                    try:
                        driver.find_element_by_xpath("//textarea").send_keys(replace_message(company, driver, name))
                    except:
                        driver.find_element_by_xpath("//textarea").send_keys(replace_message(company, driver, "there"))
                    time.sleep(.1)
                    try:
                        driver.find_element_by_xpath("//input[@type='email']").click()
                        driver.refresh()
                        count_bad += 1
                        continue
                    except:
                        driver.find_element_by_xpath("//button[@aria-label='Send now']").click()
                    try:
                        driver.find_element_by_xpath("//svg[@xmlns='http://www.w3.org/2000/svg']").click()
                    except:
                        pass
                    time.sleep(random.random() + 1)
                    day_count += 1
                    company_count += 1

                    print(f" {company_count} ", end='')



if __name__ == '__main__':
    main()



if __name__ == '__main__':
    main()
