import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def get_amazon_price(product_name):
    search_query = product_name.replace(' ', '+')
    url = f"https://www.amazon.in/s?k={search_query}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'https://www.amazon.in/'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        product_container = soup.select_one('div[data-component-type="s-search-result"]')
        if not product_container:
            return None, None, None
        
        title_element = product_container.select_one('h2 a span')
        if not title_element:
            title_element = product_container.select_one('.a-text-normal')
        
        product_title = title_element.text.strip() if title_element else "Title not found"
        
        price_element = product_container.select_one('.a-price-whole')
        if price_element:
            price_text = price_element.text.strip()
            price = re.sub(r'[^\d.]', '', price_text)
            date = datetime.now().strftime('%Y-%m-%d')
            return product_title, f"Rs.{price}", date
        else:
            return product_title, "Price not found", datetime.now().strftime('%Y-%m-%d')
            
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None
