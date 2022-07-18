import random

from selenium import webdriver
import os
import time
import csv

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("user-data-dir=%s" % os.path.join(os.path.dirname(os.path.realpath(__file__)), "selenium"))
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://github.com/pittcsc/Summer2022-Internships")
list = driver.find_elements_by_xpath("//tr/*[1]//a")
list.reverse()
f = open("companies_github.csv", "w+")
for elem in list:
    f.write(elem.text + "\n")