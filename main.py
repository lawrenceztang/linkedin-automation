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
    # options.add_argument("user-data-dir=C:/Users/larry/AppData/Local/Google/Chrome/User Data")
    options.add_argument("user-data-dir=%s" % os.path.join(os.path.dirname(os.path.realpath(__file__)), "selenium"))
    driver = webdriver.Chrome(executable_path=webdriver_path, chrome_options=options)
    # login(driver)
    driver.get("https://www.linkedin.com")
    time.sleep(1)

    day_count = 0

    for company in get_companies_list():
        print("\n" + company)
        driver.get(f"https://www.linkedin.com/search/results/all/?keywords={company}&origin=GLOBAL_SEARCH_HEADER&sid=.wg)")
        time.sleep(4)
        try:
            a = driver.find_element_by_xpath("//a[@class='app-aware-link  search-nec__hero-kcard-v2-link-wrapper link-without-hover-state link-without-visited-state t-normal t-black--light']").get_attribute("href")
            # a = "https://www.linkedin.com/company/rivian/"
            #company = "Rivian"
        except:
            continue
        driver.get(a + "/people/?keywords=recruiter")

        time.sleep(4)

        company_count = 0
        i = -1
        while company_count < limit_per_company and day_count < day_limit:
            i += 1

            while True:
                try:
                    driver.find_element_by_xpath("//button[@class='msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view']").click()
                    time.sleep(1)
                except:
                    break

            list = driver.find_elements_by_xpath("//div[@class='org-people-profile-card__profile-info']")
            if i >= len(list):
                try:
                    driver.find_element_by_xpath("//span[text()='Show more results']").click()
                except:
                    pass
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                list = driver.find_elements_by_xpath(
                "//div[@class='org-people-profile-card__profile-info']")

            try:
                elem = list[i]
            except:
                continue
            if company_count >= limit_per_company:
                break
            if day_count >= day_limit:
                time.sleep(86400)
            try:
                elem.click()
            except:
                pass
            time.sleep(3)

            try:
                name = driver.find_element_by_xpath("//h1[@class='text-heading-xlarge inline t-24 v-align-middle break-words']").text.split()[0]
            except:
                continue
            try:
                driver.find_elements_by_xpath("//li-icon[@type='send-privately']")[1].click()
                time.sleep(1)
            except:
                driver.get(a + "/people/?keywords=recruiter")
                time.sleep(5)
                continue
            try:
                driver.find_element_by_xpath("//input[@placeholder='Subject (optional)']").send_keys(note.format(company=company))
                driver.find_element_by_xpath("//div[@class='msg-inmail-compose-form-v2 relative flex-1 white display-flex flex-column']//div[@aria-label='Write a message…']").send_keys(message.format(company=company, name=name))
            except:
                driver.get(a + "/people/?keywords=recruiter")
                time.sleep(5)
                continue
            time.sleep(.1)
            driver.find_element_by_xpath("//button[@class='msg-form__send-button artdeco-button artdeco-button--1']").click()
            time.sleep(1)
            day_count += 1
            company_count += 1
            print(f" {company_count} ", end='')
            driver.get(a + "/people/?keywords=recruiter")
            time.sleep(random.random() + 5)



if __name__ == '__main__':
    main()