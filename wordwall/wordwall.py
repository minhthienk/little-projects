
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import time
import pandas as pd
import os
import pathlib
import pyautogui
import requests




from bing_image_downloader import downloader




# read data from a file
def read_data(path):
    with open(path, "r") as file_object:
        return file_object.read()
    return 


# write data to a file, overwrite mode
def write_data(path, data, mode='w'):
    with open(path, mode) as file_object:
        file_object.write(data)


def download(url, name):
    img_data = requests.get(url).content
    with open(name, 'wb') as handler:
        handler.write(img_data)


class Excel:
    # Contructor
    def __init__(self, path, sheet_names, header):
        self.sheets = self.load_dtb(path, sheet_names, header) # a dict to contain all sheets data frame
    # load dtb from excel or pickle files
    @staticmethod
    def load_dtb(path, sheet_names, header):
        # create data frames from pickle files if not create pickle files
        sheets = {}
        for sheet_name in sheet_names:
            print('read excel files: ', path, ' - ',sheet_name)
            sheets[sheet_name] = pd.read_excel(path, 
                                               sheet_name=sheet_name, 
                                               header=header, 
                                               na_values='#### not defined ###', 
                                               keep_default_na=False)
        return sheets


def input_excel_database(sheet, header):
    sheets = [sheet]
    
    df = Excel(EXCEL_PATH, sheets, header).sheets[sheet]
    # strip all strings from excel database
    df.replace(r'(^\s+|\s+$)', '', regex=True, inplace=True)
    df.replace(r'\s+', ' ', regex=True, inplace=True)
    return df



def log_in(driver, username, password):
    driver.get("https://wordwall.net/")
    driver.find_element_by_id("sign_in_btn").click()
    driver.find_element_by_name("Email").click()
    driver.find_element_by_name("Email").clear()
    driver.find_element_by_name("Email").send_keys(username)
    driver.find_element_by_name("Password").clear()
    driver.find_element_by_name("Password").send_keys(password)
    driver.find_element("class name", "account-submit-btn").click()



def attach_driver(session_path, username, password):
    try:
        driver_info = read_data(session_path)
        session_id = driver_info.split('\n')[0].replace('session_id: ', '')
        executor_url = driver_info.split('\n')[1].replace('executor_url: ', '')

        driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        driver.close()
        driver.session_id = session_id

        print('found a session and linked:',session_id)
        #print(session_id)
        #print(executor_url)
        #print(driver.current_url)

    except Exception as e:
        driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities={})
        #driver = webdriver.Chrome(desired_capabilities={})
        print('no session found, created new')
        executor_url = driver.command_executor._url
        session_id = driver.session_id
        print(session_id)
        print(executor_url)
        driver_info = 'session_id: ' + session_id + '\n' + 'executor_url: ' + executor_url
        write_data('session.txt', driver_info)

        log_in(driver, username, password)
    return driver


def get_paths(root_path):
    '''
    get all files from a folder, 
    also check subfolders 
    '''
    # create a list to contain file paths
    file_paths = [] 
    folder_paths = []

    root_path = pathlib.Path(root_path)

    for path in root_path.iterdir(): # iter all paths in each folder path
        if path.is_file(): # if path is file
            file_paths.append(str(path)) # collect
        else: # folder
            folder_paths.append(str(path)) # collect
    return file_paths






def wordwall_wordsearch(driver, data_title, data_words, data_images):
    # access wordwall template page 
    template = 'https://wordwall.net/create/entercontent?templateId=10'
    driver.get(template)

    # change title
    title = driver.find_element("class name", "js-activity-title")
    title.send_keys(Keys.CONTROL, 'a')
    title.send_keys(Keys.DELETE)
    title.send_keys(data_title)


    # select mode with clues
    mode = driver.find_element("id", "option_mode2")
    mode.click()


    # add rows
    for word_num in range(0, int(len(data_words)/2-1)):
        driver.find_element("class name", "editor-add-item").click()
        time.sleep(0.5)

    # enter words and definitions
    item_inputs = driver.find_elements("class name", "item-input")
    for item_input in item_inputs:
        item_input.click()
        item_input.clear()
        item_input.send_keys(data_words.pop(0))


    # upload images
    image_buttons = driver.find_elements(By.XPATH, '//*[contains(@title, "Add Image")]')
    for image_button in image_buttons:
        image_button.click()
        upload_button = driver.find_element("id", "upload_image_button").click()
        time.sleep(1)
        pyautogui.write(data_images.pop(0) + '\n', interval=0.05)
        time.sleep(1)

    # submit
    driver.find_element("class name", "js-done-button").click()

    print('>>> wordsearch: ')
    print(driver.current_url)
    return driver.current_url


query_string = 'window'
downloader.download(query_string, limit=3,  
    output_dir='images', 
    adult_filter_off=True, 
    force_replace=False, 
    timeout=60, 
    filter='photo', verbose=True)



# data
username = 'minhthien.k@gmail.com'
password = 'wordwall12333'


EXCEL_PATH = 'content_auto.xlsx'
df = input_excel_database('main', header=0)
df = df[df['allow']=='yes']


data_title = ''
data_words = []
data_images = []
for index, row in df.iterrows():
    data_title = row['title']
    data_words.append(row['word'])
    data_words.append(row['def'])
    image_url = row['image']
    image_name = '{}.png'.format(row['word'])
    if 'http' in image_url:
        download(image_url, 'images/' + image_name)
    else:
        data_images.append(image_name)

print(data_words)
print(data_images)


session_path = 'session.txt'
driver = attach_driver(session_path, username, password)
driver.maximize_window()
wordwall_wordsearch(driver,data_title, data_words, data_images)