import csv
import requests
from bs4 import BeautifulSoup

# Prepare CSV file
csv_file = open("data1.csv", "w", newline="", encoding="utf-8")
fieldnames = ["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"]
csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
csv_writer.writeheader()

# Scrape 20 pages of product listings
for page in range(1, 21):
    url = f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all product listings on the page
    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    # Extract information from each product listing
    for product in products:
        product_url = "https://www.amazon.in" + product.find("a", class_="a-link-normal s-no-outline")["href"]
        product_name_element = product.find("span", class_="a-size-medium a-color-base a-text-normal")
        product_name = product_name_element.text.strip() if product_name_element else ""
        product_price_element = product.find("span", class_="a-price-whole")
        product_price = product_price_element.text.strip() if product_price_element else ""
        rating_element = product.find("span", class_="a-icon-alt")
        rating = rating_element.text.strip() if rating_element else ""
        #num_reviews_element = product.find("span", {"class": "a-size-base", "dir": "auto"})
        #num_reviews = num_reviews_element.text.strip() if num_reviews_element else ""
        num_reviews_element = product.find("span", class_="a-size-base")
        num_reviews = num_reviews_element.text.strip() if num_reviews_element else ""


        # Write data to the CSV file
        csv_writer.writerow({
            "Product URL": product_url,
            "Product Name": product_name,
            "Product Price": product_price,
            "Rating": rating,
            "Number of Reviews": num_reviews
        })

# Close the CSV file
csv_file.close()
