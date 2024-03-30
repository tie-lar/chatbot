import json
import time
import random
import requests
import spacy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load Spacy's English model
nlp = spacy.load("en_core_web_sm")

# Load intents JSON
with open('intents.json', 'r') as f:
    intents = json.load(f)["intents"]

def get_intent(message):
    doc = nlp(message)
    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern in message:
                return intent["tag"]
    return None

def find_tickets(origin, destination): #date):
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.nationalrail.co.uk/")
        # Add your Selenium code here to interact with the national rail website
        # and scrape the ticket information.
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler")))
        # Click the button
        button.click()

        start = driver.find_element(By.XPATH, '//*[@id="jp-form-preview"]/section/div/button')
        start.click()
        start = driver.find_element(By.XPATH, '//*[@id="jp-origin"]')
        start.send_keys(origin.capitalize())
        start.send_keys(Keys.DOWN)
        start.send_keys(Keys.ENTER)
        time.sleep(1)
        

        #Enter destination
        end = driver.find_element(By.XPATH, '//*[@id="jp-destination"]')
        end.send_keys(destination.capitalize())
        end.send_keys(Keys.DOWN)
        end.send_keys(Keys.ENTER)
        time.sleep(1)

        enter = driver.find_element(By.XPATH, '//*[@id="button-jp"]')
        enter.click()

        #if date == "today".capitalize() or "today".upper() or "today".lower():
            #enter = driver.find_element(By.XPATH, '//*[@id="button-jp"]')
            #enter.click()
        #elif "specific" in date:
            #enter = driver.find_element(By.XPATH, '//*[@id="leaving-date"]')
            #enter.click()
            #enter.clear()
            #time.sleep(5)


        # set maximum time to load the web page in seconds
        driver.implicitly_wait(10)
        time.sleep(5)
        current_url = driver.current_url
        
        driver.get(current_url)

        #train_elements = driver.find_elements(By.XPATH, )

        price_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '£')]")
        for element in price_elements:
            price = element.text
            if price:  # Ensure the text is not empty
                print(price)

        sections = driver.find_elements(By.XPATH, "//*[contains(text(), 'from')]")
        for section in sections:
            train_info = section.text
            if train_info:
                print(train_info)

        """
        sections = driver.find_elements(By.XPATH, "//section[contains(text(), 'from')]")
        for section in sections:
            train_info = section.text
            print(train_info)

            section, with id="outward-0", increment num by however many sections are in div
            id=$`outward-{num}`

         journeys = driver.find_elements(By.XPATH, "//div[contains(@class, 'journey-option')]")

        for journey in journeys:
            departure_time = journey.find_element(By.XPATH, ".//span[@class='departure-time']").text  # Pseudocode
            departure_station = journey.find_element(By.XPATH, ".//span[@class='departure-station']").text  # Pseudocode
            arrival_time = journey.find_element(By.XPATH, ".//span[@class='arrival-time']").text  # Pseudocode
            arrival_station = journey.find_element(By.XPATH, ".//span[@class='arrival-station']").text  # Pseudocode
            
            print(f"Departs, {departure_time} from {departure_station}")
            print(f"Arrives, {arrival_time} at {arrival_station}\n")
        """

    finally:
        driver.close()

def chat():
    print("Bot: Hey there! How can I assist you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Bot: Goodbye!")
            break
        
        intent = get_intent(user_input.lower())
        
        if intent == "greeting":
            print(f"Bot: {random.choice([response for intent in intents if intent['tag'] == 'greeting' for response in intent['responses']])}")
        elif intent == "goodbye":
            print(f"Bot: {random.choice([response for intent in intents if intent['tag'] == 'goodbye' for response in intent['responses']])}")
            break
        elif intent == "tickets":
            print("Bot: Sure thing! Where would you be beginning your journey from?")
            origin = input("You: ")
            destination = input("Bot: Where would you be travelling to?\nYou: ")
            #date = input("Bot: For today or a specific date?\nYou: ")
            print("Bot: Okay awesome, let me find that information for you.")
            find_tickets(origin, destination) 
            # For now, we'll skip the implementation details of this function.
        else:
            print("Bot: I'm not sure how to respond to that.")

if __name__ == "__main__":
    chat()
