import requests
from bs4 import BeautifulSoup
import time as t

class scraper:
  def __init__(self, url):
    self.url = url
    self.header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

  def get_response(self, url):
    try:
        web = requests.get(url, headers=self.header, timeout=5)
        web.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(web.content, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

  def scrape_content(self, url = None):
    if url is None:
      url = self.url
    soup = self.get_response(url)
    try:
        # Assuming you want to extract book titles and prices
        # Adjust the selectors to match the website's structure
        books = soup.find_all('article', class_='product_pod')
        for book in books:
            title = book.h3.a['title']
            rate = book.find('p', class_='star-rating')['class'][1]
            price = book.find('p', class_='price_color').text
            print(f"Title: {title}, Price: {price}, Rate: {rate}")
    except AttributeError as e:
        print(f"Error extracting content: {e}")
    finally:
      print("done")

  def scrape_multiple(self,pages = 5):

    soup = self.get_response(self.url)

    for halaman in range(1, pages + 1):
        url = f"{self.url}/catalogue/page-{halaman}.html"
        soup = self.get_response(url)
        print(f"scrape halaman ke {halaman}")

        self.scrape_content(url)

        t.sleep(2)




def main():
  target = "http://books.toscrape.com/"
  print("web to-scrape dump CLI based")
  print("select a feature : ")
  print("1. book-store \n 2. quotes finder \n choose between 1 or 2")
  choose = input(": ")
  if choose == "1":
    bookstore = input("1. single page \n 2. multiple page (custom)")
    match bookstore:
      case "1":
        scraping = scraper(target)
        return scraping.scrape_content()  # Call the scrape_content method
      case "2":
        totalpg = int(input("berapa?"))
        multiscrape = scraper(target)
        return multiscrape.scrape_multiple(totalpg)
      case _:
        print("invalid input")
  elif choose == "2":
    url1 = "https://quotes.toscrape.com"
    pg = 1
    print("welcome to quote scraper")
    i = input("which feature did u want? \n 1. scrape by author \n 2. scrape by tags \n 3. scrape all single page \n 4. scrape multiple page")

    match i:
      case "1":
       ator = input("siapa nama author atau penulis? : ")

       while True:
        url1 =  f"{url}/page/{pg}"
        resp = requests.get(url)

        if resp.status_code != 200:
          print("sorry website isnt responding")

        soup = BeautifulSoup(response.content, 'html.parser')

        coldiv = soup.find_all('div', class_="quote")
        for col in coldiv:
          author_links = soup.find('small', class_="author").text
        if author_links == ator:
          text = soup.find_all('span', class_="text")

          for q in text:
           print(f"author : {author_links}\n the quote is : {q.text}")
        pg += 1
      case "2":
        tag = input("masukkan tags yang ingin dicari")
        url2 = f"{url1}/tag/{tag}/page/{pg}"

        while True:
          response = requests.get(url2)

          if response.status_code == 200:
            soup1 = BeautifulSoup(response.content, 'html.parser')

            cont = soup1.find_all('div', class_="quote")
            for c in cont:
              tags = soup1.find_all('span', class_="text")
              athori = soup1.find_all('small', class_="author")

              for z,h in zip(tags,athori):
                 print(f"author : {z.text}\n the quote is : {h.text}")
                 t.sleep(3)
            pg += 1
          else:
            pass
      case "3":
        soup2 = requests.get(url1)
        soup = BeautifulSoup(soup2.content, 'html.parser')

        b = soup.find_all('div', class_="quote")

        for v in b:
          teks = soup.find_all('span', class_="text")
          athori = soup.find_all('small', class_="author")

          for nm,bv in zip(teks,athori):
            print(f"author : {nm.text}\n the quote is : {bv.text}")
            t.sleep(3)
       ###
       #author_links = soup.find_all('small', class_="author")

       #for author in author_links:
        #if author.text == ator:
         # print(author.text)
  else:
    print("wtf")

if __name__ == "__main__":
  main()
