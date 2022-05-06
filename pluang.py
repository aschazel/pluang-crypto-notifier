import time
import random
from discord import Webhook, RequestsWebhookAdapter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://pluang.com/produk/pluang-crypto/prices")

target = input("Currency to monitor: ")
targetprice = int(input("Price treshold: "))
modeHighPrice = input("Notify when high/low? [h/l]: ")

if modeHighPrice.lower() == 'h':
	modeHighPrice = True
elif modeHighPrice.lower() == 'l':
	modeHighPrice = False
else:
	print("Invalid argument")
	exit()

webhookUrl = input("Webhook url: ")

webhook = Webhook.from_url(webhookUrl, adapter=RequestsWebhookAdapter())

def messageHighPrice(currency, lastprice):
	lastpriceint = int(lastprice.replace("Rp", '').replace('.', ''))

	message = [
		f"Dojyaaan! **{currency}** is currently at **{lastprice}**, it's time to sell some napkins!",
		f"Dojyaaaaaaan! **{currency}** is currently at **{lastprice}**!",
		f"**{currency}** is currently at **{lastprice}**, it's time to sell some Jesus' corpses!"
		]

	if lastpriceint > targetprice:
		randomsg = random.randint(0, len(message)-1)
		message = message[randomsg]
		webhook.send(content=message)
		return True
	else:
		return False

def messageLowPrice(currency, lastprice):
	lastpriceint = int(lastprice.replace("Rp", '').replace('.', ''))

	message = [
		f"Dojyaaan! **{currency}** is currently dropping to **{lastprice}**, it's time buy some corpse parts!",
		f"Dojyaaaaaaan! **{currency}** is currently dropping to **{lastprice}**!",
		f"**{currency}** is currently dropping to **{lastprice}**, it's time to declare some horse racing event!"
		]

	if lastpriceint < targetprice:
		randomsg = random.randint(0, len(message)-1)
		message = message[randomsg]
		webhook.send(content=message)
		return True
	else:
		return False

while True:
	table = driver.find_elements(by=By.XPATH, value="/html/body/div[2]/div[4]/div[1]/div[2]/div/div/div/table/tbody/tr")

	for row in range(1, len(table)+1):
		currency = driver.find_elements(by=By.XPATH, value=f"/html/body/div[2]/div[4]/div[1]/div[2]/div/div/div/table/tbody/tr[{row}]/td[2]/div/p")[0].text
		if currency == target:
			lastprice = driver.find_elements(by=By.XPATH, value=f"/html/body/div[2]/div[4]/div[1]/div[2]/div/div/div/table/tbody/tr[{row}]/td[3]/p")[0].text
			break

	if modeHighPrice == True:
		result = messageHighPrice(currency, lastprice)
		if result:
			break
	elif modeHighPrice == False:
		result = messageLowPrice(currency, lastprice)
		if result:
			break

	print(currency, lastprice)
	driver.refresh()

driver.quit()
