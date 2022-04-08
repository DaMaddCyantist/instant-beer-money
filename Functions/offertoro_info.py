"""
This module will contain code necessary to connect to and
scrape data from freecash.com
"""
import os
import time
import pandas as pd
import utils
import sys

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Set options to run Chrome in 'Headless' mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920x1080")

#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline
#and/or server side as well.

def start_driver_and_open_offertoro(offerwall_version):
    """
    Downloads the latest version of Google chromedriver and
    Opens the OfferToro offerwall within a webdriver

    str: offerwall

    offerwall examples:
    - 'BASELINE_TORO'
    - 'USER_TORO'
    """
    #This installs the latest version of the official Google chromedriver
    #Accesses cached version if present.

    #Initialize variable
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),\
                options=chrome_options)
    except Exception as err:
        print(f"'Setting Driver Error: {err}'")
        sys.exit(0)

    #Set OfferToro URL
    offertoro = os.environ[offerwall_version]
    #Open webpage
    driver.get(offertoro)
    return driver

def parse_available_offer_information(driver):
    """
    This function parses through the OfferToro available offerwall text and extracts:
    1. Offer Titles
    2. Offer Description
    3. Offer Amount
    4. Device type

    Sets device type and
    determines if offer has multiple rewards (multi-tiered)
    """
    #Create dictionary to hold offer information
    available_offer_dict = {'total_coins_earnable':[],'offer_title':[],\
                  'offer_description':[],'offer_device':[]}

    try:
        #Wait for hamburger button to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fa fa-star")))
        #Explicit Wait
        time.sleep(1)
    except Exception as err:
        print(f"'Error: {err}'")

    #Focus on offerwall information
    #Wait for menu to be visible button to appear
    available_offer_info = driver.find_elements(By.TAG_NAME,"TR")
    ############# LOGIC BLOCK ##############
    for offers in available_offer_info:
        #Set variables equal to text values of the offers
        available_offer_payout = offers.get_attribute('data-offer_payout')
        offer_device_type = offers.get_attribute('data-offer_device')
        #Split the offer text to gain information about the offer itself
        split_available_offer_info = offers.get_attribute('innerText').split('\t')
        
        #Insert available offer text into dictionary based on size
        #Sizes were pre-determined from trial and error.

        if len(split_available_offer_info) == 3:
            offer_and_desc = split_available_offer_info[1].split('\n')
            available_offer_dict['total_coins_earnable'].append(available_offer_payout)
            available_offer_dict['offer_device'].append(offer_device_type)
            available_offer_dict['offer_title'].append(offer_and_desc[1])
            available_offer_dict['offer_description'].append(offer_and_desc[2])

        elif len(split_available_offer_info) == (1):
            continue
        else:
            raise Exception ('Unexpected offer split size')
    ############# LOGIC BLOCK ##############
    return available_offer_dict

def create_available_offer_dataframe(available_offer_dict):
    """
    This function returns the available offer dictionary as a pandas DataFrame.
    """
    available_offer_dataframe = pd.DataFrame.from_dict(available_offer_dict)
    return available_offer_dataframe

def parse_completed_offer_info(driver):
    """
    This function parses through the OfferToro offerwall text and extracts:
    1. Completed Offer Titles
    2. Completed Offer Date
    3. Completed Offer Amount
    ### Need Device ###
    """
    #Create dictionary to hold offer information
    completed_offer_dict = {'offer_title':[],'coins_earned':[],'date_completed':[]}

    #Navigate to reward status page
    try:
        #Wait for hamburger button to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "hamburger-button")))
        #Explicit Wait
        time.sleep(1)
        #Click button
        driver.find_element(by=By.ID,value='hamburger-button').click()

        #Wait for reward status button to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sidebar-status")))
        #Explicit wait
        time.sleep(1)
        #Click button
        driver.find_element(by=By.ID,value='sidebar-status').click()
    except Exception as err:
        print(f"'Error: {err}'")

    #Attempt to scrape - Fails if offers are not marked as 'Complete' yet
    try:
        #Wait for completed page to render
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-status")))
        #Explicit wait
        time.sleep(1)
        #Extract completed offer info
        completed_offer_info = driver.find_elements(By.XPATH, "//div[@id='user-status']")[0]

        ############# LOGIC BLOCK ##############
        #Get actual text from webpage
        completed_offer_text = completed_offer_info.text
        #Split the text
        split_completed_offer_info = completed_offer_text.split('\n')
        #Chunk the text for insert into dictionary
        chunked_completed_list = utils.chunked_iterable(split_completed_offer_info, 4)
        #Insert values to dictionary
        for chunks in chunked_completed_list:
            completed_offer_dict['offer_title'].append(chunks[1])
            completed_offer_dict['coins_earned'].append(chunks[2])
            completed_offer_dict['date_completed'].append(chunks[3])
        ############# LOGIC BLOCK ##############

        return completed_offer_dict
    except Exception as err:
        print(f"'Unhandled Error: %{err}'")

def create_completed_offer_dataframe(completed_offer_dict):
    """
    This function returns the completed offer dict as a pandas DataFrame.
    """
    completed_offer_dataframe = pd.DataFrame.from_dict(completed_offer_dict)
    return completed_offer_dataframe

def parse_pending_offer_info(driver):
    """
    This function parses through the OfferToro offerwall text and extracts:
    1. Pending Offer Titles
    2. Pending Offer Description
    3. Pending Start Date/Time
    """
    #Create dictionary to hold offer information
    pending_offer_dict = {'pending_offer_title':[],'offer_description':[],'date_completed':[]}

    #Navigate to pending status page
    try:
        #Wait for hamburger button to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "hamburger-button")))
        #Explicit Wait
        time.sleep(1)
        #Click button
        driver.find_element(by=By.ID,value='hamburger-button').click()

        #Wait for reward status button to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sidebar-status")))
        #Explicit wait
        time.sleep(1)
        #Click button
        driver.find_element(by=By.ID,value='sidebar-status').click()

        #Wait for Pending button to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tabs-menu")))
        #Explicit wait
        time.sleep(1)
        #Click button
        driver.find_elements(By.XPATH, "//li[@href='#pending']")[0].click()
    except Exception as err:
        print(f"'Error: {err}'")

    #Attempt to scrape pending offers
    try:
        #Wait for pending page to render
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-status")))
        #Explicit wait
        time.sleep(1)
        #Extract pending offer info
        pending_offer_info = driver.find_elements(By.XPATH, "//div[@id='user-status']")[0]

        ############# LOGIC BLOCK ##############
        #Get actual text from webpage
        pending_offer_text = pending_offer_info.text
        #Split the text
        split_pending_offer_info = pending_offer_text.split('\n')
        #Chunk the text for insert into dictionary
        chunked_pending_list = utils.chunked_iterable(split_pending_offer_info, 4)
        #Insert values to dictionary
        for chunks in chunked_pending_list:
            pending_offer_dict['pending_offer_title'].append(chunks[1])
            pending_offer_dict['offer_description'].append(chunks[2])
            pending_offer_dict['date_completed'].append(chunks[3])
        ############# LOGIC BLOCK ##############

        return pending_offer_dict
    except Exception as err:
        print(f"'Unhandled Error: %{err}'")

def create_pending_offer_dataframe(pending_offer_dict):
    """
    This function returns the pending offer dict as a pandas DataFrame.
    """
    pending_offer_dataframe = pd.DataFrame.from_dict(pending_offer_dict)
    return pending_offer_dataframe
