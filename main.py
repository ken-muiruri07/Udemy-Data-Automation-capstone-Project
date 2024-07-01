import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

chrome_driver_path = r"C:\Development\chromedriver.exe"
ZILLOW_URL = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.85869079021397%2C%22south%22%3A37.691798932527874%2C%22east%22%3A-122.29977694873047%2C%22west%22%3A-122.56688205126953%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%7D"
GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSdGAZD87GuyASycFAwhVjXLGCUrcdTAbHrXoHNud1PeaoFxhg/viewform?usp=sf_link"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    "Accept-Language": "en-US,en;q=0.9"
}
response = requests.get(url=ZILLOW_URL, headers=headers)
content = response.text

soup = BeautifulSoup(content, "html.parser")

address_list = []
prices_list = []
address_links_list = []
addresses = soup.find_all("address")
for address in addresses:
    address_list.append(address.text)

prices = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine-srp-8-102-0__sc-16e8gqd-1 vjmXt")
for price in prices:
    stripped_price = (price.text.split()[0].replace("+", "").replace("/mo", ""))
    prices_list.append(stripped_price)

address_links = soup.find_all("a", class_="StyledPropertyCardDataArea-c11n-8-102-0__sc-10i1r6-0 klMkvj property-card-link")
for link in address_links:
    address_links_list.append(link['href'])

modified_link_list = ["https://www.zillow.com" + link if link.startswith("/") else link for link in address_links_list]

print("Step 1 done")

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

driver.get(GOOGLE_FORM_LINK)
time.sleep(5)

for n in range(len(addresses)):

    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address.send_keys(address_list[n])
    time.sleep(2)

    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price.send_keys(prices_list[n])
    time.sleep(2)

    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link.send_keys(modified_link_list[n])

    time.sleep(2)

    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit.click()
    print(f"Address {n} done.")
    next_response = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    next_response.click()
driver.quit()
