# Import required packages
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Define the chromedriver service
PATH = "C:\Program Files (x86)\chromedriver.exe"
s = Service(PATH)

# Instantiate the webdriver
driver = webdriver.Chrome(service=s)

# check heading_class is present or not first by document.querySelector("");, leetcode page's heading and body class changes day by day
heading_class = ".mr-2.text-label-1"
body_class = ".px-5.pt-4"
index = 1
QDATA_FOLDER = "Qdata"


def get_array_of_links():
    arr = []  # Array to store the lines of the file
# Open the file
    with open("lc_problem_links.txt", "r") as file:
        # Read each line one by one
        for line in file:
            # append each link into the array
            arr.append(line)
    return arr

# function to store all problems titles in a file named index.txt
def add_text_to_index_file(text):
    index_file_path = os.path.join(QDATA_FOLDER, "index.txt")
    with open(index_file_path, "a") as index_file:
        index_file.write(text + "\n")

# function to store all problems links in a file named Qindex.txt
def add_link_to_Qindex_file(text):
    index_file_path = os.path.join(QDATA_FOLDER, "Qindex.txt")
    with open(index_file_path, "a", encoding="utf-8", errors="ignore") as Qindex_file:
        Qindex_file.write(text)

# function to create new files corresponding to each problem, containing the problem description
def create_and_add_text_to_file(file_name, text):
    folder_path = os.path.join(QDATA_FOLDER, file_name)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name + ".txt")
    with open(file_path, "w", encoding="utf-8", errors="ignore") as new_file:
        new_file.write(text)

# function which calls the above functions to create new files
# if it is a premium problem, it returns false throwing some error, else it returns true
def getPagaData(url, index):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, body_class)))
        time.sleep(1)
        heading = driver.find_element(By.CSS_SELECTOR, heading_class)
        body = driver.find_element(By.CSS_SELECTOR, body_class)
        print(heading.text)
        if (heading.text):
            add_text_to_index_file(heading.text)
            add_link_to_Qindex_file(url)
            create_and_add_text_to_file(str(index), body.text)
        time.sleep(1)
        return True
    except Exception as e:
        print(e)
        return False

# function which gathers all the problem links into an array
arr = get_array_of_links()

# testing each link whether it is of a premium problem or not and incrementing the index based on it
for link in arr:
    success = getPagaData(link, index)
    if (success):
        index = index+1


driver.quit()