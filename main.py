from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pprint
import keyboard
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox(executable_path=r"F:\Projects\ML\geckodriver.exe")


driver.get("https://www.incometaxindia.gov.in/pages/acts/income-tax-act.aspx")


radio = driver.find_element_by_class_name("noBold")

chapter = radio.find_elements_by_tag_name("td")
chapter[1].click()

chapterIndex = 0

sectionIndex = 0

pageCount = 0

data = dict()
sec = dict()
while True:
    driver.switch_to.default_content()
    radio = driver.find_element_by_class_name("noBold")
    chapter = radio.find_elements_by_tag_name("td")
    if len(chapter) == 0:
        keyboard.press_and_release("shift + alt + c")
        driver.switch_to.default_content()
    try:
        element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "search_result"))
        )
    except:
        keyboard.press_and_release("shift + alt + c")
        driver.switch_to.default_content()
        print("Waiting")
        time.sleep(2)
    title = driver.find_elements_by_class_name("search_result")
    if len(title) - 1 < chapterIndex:
        nextPage = driver.find_elements_by_class_name("ms-paging")
        nextPage[3].click()
        pageCount += 1
        if pageCount == 5:
            break
        chapterIndex = 0
        sectionIndex = 0
        continue

    print(title[chapterIndex].text.split("\n")[0], "chapter     \n")
    chapterTitle = title[chapterIndex].text.split("\n")[0]

    title[chapterIndex].click()
    try:
        element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "search-result-inner"))
        )
    except:
        keyboard.press_and_release("shift + alt + c")
        driver.switch_to.default_content()
        print("Waiting")
        time.sleep(2)
    results = driver.find_elements_by_class_name("search-result-inner")

    if len(results) - 1 != chapterIndex:
        time.sleep(2)
        results = driver.find_elements_by_class_name("search-result-inner")
    element = WebDriverWait(results[chapterIndex], 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "li"))
    )

    sections = results[chapterIndex].find_elements_by_tag_name("li")

    element = WebDriverWait(sections[sectionIndex], 10).until(
        EC.element_to_be_clickable((By.TAG_NAME, "a"))
    )
    section = sections[sectionIndex].find_element_by_tag_name("a")

    print(section.text, "section      \n")
    sectionTitle = section.text
    section.click()
    sectionIndex += 1

    frameList = driver.find_elements_by_tag_name("iframe")

    driver.switch_to.frame(frameList[1])

    element = WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, "overlaybx_page"))
    )

    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "viewerContent"))
    )

    content = driver.find_element_by_class_name("viewerContent")

    sec[sectionTitle] = {"description": content.text, "tags": []}

    if sectionIndex == len(sections):
        sectionIndex = 0
        chapterIndex += 1
        data[chapterTitle] = sec
        sec = dict()

    keyboard.press_and_release("shift + alt + c")


final = json.dumps(data)
file = open("new.json", "w")
file.write(final)
file.close()
