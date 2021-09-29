from typing import Text
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

from sqlalchemy.sql.functions import coalesce

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("http://127.0.0.1:5000/")
print(driver.title)
#assert "Python" in driver.title

functions = ["x*x - 16", 
                "cos(x)- x**3", 
                "x + 20",
                "sin(x) \ 20",
                "1.0 \ x",
                "x - cos(x)",
                "0.3**x-x**2+4",
                "tan(x)",
                "x-cos(x)",
                "exp(0.3*x)-x**2+4",
                "x-(sqrt(x))",
                "3*(x)*(x)+4*(x)-10"]

for function in functions:
    time.sleep(3)
    formWrapper = driver.find_element_by_id("form-wrapper")
    theForm = formWrapper.find_element_by_class_name("theForm")
    eqHolder = theForm.find_element_by_id("eq-holder")
    x0Holder = theForm.find_element_by_id("x0-holder")
    time.sleep(3)
    f = eqHolder.find_element_by_id("eq")
    f.clear()
    time.sleep(3)
    print(function)
    f.send_keys(function)
    x = x0Holder.find_element_by_id("x0")
    x.clear()
    time.sleep(3)
    num = random.uniform(0.9, 10.0)
    num = round(num,3)
    x.send_keys(str(num))
    time.sleep(4)
    driver.find_element_by_name("subBotton").click()
    time.sleep(4)
    driver.back()
    time.sleep(3)

navBar = driver.find_element_by_id("navBar")
navBarList = navBar.find_element_by_id("navbarNav")
navItem = navBarList.find_element_by_id("navbar-nav")
stat = navBarList.find_element_by_id("stat")
stat.find_element_by_id("statLink").click()
time.sleep(3)
driver.quit()
