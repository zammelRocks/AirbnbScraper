import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
# Uncomment the line below to enable headless mode
# opts.add_argument("--headless")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)
driver.maximize_window()
driver.get('https://fr.airbnb.com/s/Jardins-De-Carthage--Tunisie/homes?checkin=2024-05-20&checkout=2024-05-27&tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&query=Jardins%20De%20Carthage%2C%20Tunisie&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-05-01&monthly_length=3&monthly_end_date=2024-08-01&price_filter_input_type=0&price_filter_num_nights=7&channel=EXPLORE&zoom_level=2&search_type=autocomplete_click&place_id=ChIJoccbBSy14hIRdxT0TcjVWU8&date_picker_type=calendar&source=structured_search_input_header')
sleep(15)  # Ensure the page loads completely

titulos_anuncios = driver.find_elements(By.XPATH, '//div[@data-testid="listing-card-title"]')
# Finding elements for prices
prices_elements = driver.find_elements(By.XPATH, '//span[contains(@class,"_14y1gc")]//div[contains(@class,"_1jo4hgw")]')
# Finding elements for names
Names_elements = driver.find_elements(By.XPATH, '//span[@data-testid="listing-card-name"]')
#Find beds
beds = driver.find_elements(By.XPATH, '//div[contains(@class,"fb4nyux")]//span[ contains(@class, "a8jt5op ") and contains(@class, "atm_3f_idpfg4")]')

ratings = driver.find_elements(By.XPATH, '//div//span[contains(@class, "ru0q88m ")and contains(@class, "atm_cp_1ts48j8 ") and contains(@class, "dir ") and contains(@class, " dir-ltr")]')

#finding comments
a_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "cy5jw6o ") and contains(@class," atm_5j_223wjw")]//a')

# Extract the href attributes and other details from each <a> element
links_data = [{'href': a.get_attribute('href'), 'text': a.text} for a in a_elements]
df = pd.DataFrame(links_data)
df = df.drop('text', axis=1)
df = df.drop_duplicates()
df.to_csv('airbnb_listings_links.csv', index=False)


with open('airbnb_listings_beds.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Check if the file is empty to write the header
    if file.tell() == 0:
        writer.writerow(['beds'])  # Writing the header of the CSV file

    # Iterate over each bed element found and write its text to the CSV file
    for bed in beds:
        bed_text = bed.text
        print(bed_text)  # Optional: prints the text to the console
        writer.writerow([bed_text])  # Write the text to the CSV file
#finding ratings

# Open the CSV file just once, before scraping the content
with open('airbnb_listings_ratings.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Check if the file is empty to write the header
    if file.tell() == 0:
        writer.writerow(['ratings'])  # Writing the header of the CSV file

    # Iterate over each bed element found and write its text to the CSV file
    for rate in ratings:
        rate_text = rate.text
        #print(rate_text)  # Optional: prints the text to the console
        writer.writerow([rate_text])  # Write the text to the CSV file

# Open a CSV file to write the prices of listings
with open('airbnb_prices.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Price'])  # Writing the header of the CSV file

    for price_element in prices_elements:
        price_text = price_element.text  # Access the text attribute of each element
        #print(price_text)  # Optional: prints the price to the console
        writer.writerow([price_text])  # Write the price to the CSV file

# Open a CSV file to write the titles of listings
with open('airbnb_listings.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Listing Title'])  # Writing the header of the CSV file

    for titulo in titulos_anuncios:
        #print(titulo.text)  # Optional: prints the title to the console
        writer.writerow([titulo.text])  # Write the title to the CSV file

with open('airbnb_listings_names.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Names_elements'])  # Writing the header of the CSV file

    for Names in Names_elements:
        #print(Names.text)  # Optional: prints the title to the console
        writer.writerow([Names.text])  # Write the title to the CSV file

driver.quit()  # Close the browser after scraping


