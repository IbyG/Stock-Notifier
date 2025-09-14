#!/usr/bin/env python3
"""
Vanguard Stock Price Scraper

This script scrapes the Vanguard website to extract historical price data
for the specified fund (portId=8134).
"""

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


def scrape_vanguard_page(url):
    """
    Scrape the Vanguard website using Selenium to handle JavaScript rendering.
    
    Args:
        url (str): The URL to scrape
        
    Returns:
        tuple: (page_source, soup_object) or (None, None) if error
    """
    driver = None
    try:
        print(f"Fetching data from: {url}")
        print("Starting browser... (this may take a moment)")
        
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Wait for the page to load
        print("Waiting for page to load...")
        wait = WebDriverWait(driver, 30)
        
        # Wait for content to load (not just the basic HTML shell)
        wait.until(lambda driver: len(driver.page_source) > 10000)
        
        # Wait for dynamic content to load
        time.sleep(3)
        
        # Wait for tab panel to be visible
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="tabpanel"]')))
            print("Tab panel found, waiting for content...")
            time.sleep(2)
        except TimeoutException:
            print("Warning: Tab panel not found, but continuing...")
        
        page_source = driver.page_source
        print(f"Content length: {len(page_source)} characters")
        
        # Parse the HTML
        soup = BeautifulSoup(page_source, 'html.parser')
        
        return soup
        
    except WebDriverException as e:
        print(f"Browser error: {e}")
        print("Note: You may need to install Chrome and ChromeDriver")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    finally:
        if driver:
            driver.quit()


def extract_historical_prices_table(soup):
    """
    Extract and display the historical prices table from the parsed HTML.
    
    Args:
        soup: BeautifulSoup object containing the parsed HTML
    """
    try:
        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables on the page")
        
        if not tables:
            print("No tables found on the page")
            return
        
        for i, table in enumerate(tables):
            print(f"\n--- Table {i+1} ---")
            
            # Get table headers
            headers = []
            header_row = table.find('thead')
            if header_row:
                header_cells = header_row.find_all(['th', 'td'])
                headers = [cell.get_text(strip=True) for cell in header_cells]
            else:
                # Try to find headers in the first row
                first_row = table.find('tr')
                if first_row:
                    header_cells = first_row.find_all(['th', 'td'])
                    headers = [cell.get_text(strip=True) for cell in header_cells]
            
            print(f"Headers: {headers}")
            
            # Check if this looks like a prices table
            is_prices_table = any(keyword in ' '.join(headers).lower() for keyword in 
                                ['date', 'price', 'nav', 'unit', 'value', 'distribution'])
            
            if is_prices_table:
                print("This appears to be a prices table!")
                
                # Extract all rows
                rows = table.find_all('tr')
                print(f"Found {len(rows)} rows in table")
                
                # Display the table data
                print("\nTable data:")
                for j, row in enumerate(rows[:10]):  # Show first 10 rows
                    cells = row.find_all(['td', 'th'])
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    print(f"Row {j+1}: {row_data}")
                
                # Find the latest row (usually the first data row after headers)
                data_rows = []
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:  # At least date and price columns
                        row_data = [cell.get_text(strip=True) for cell in cells]
                        # Check if it looks like a data row (has date and price)
                        if row_data and any('$' in str(cell) for cell in row_data):
                            data_rows.append(row_data)
                
                if data_rows:
                    # Display latest price data in table format
                    print("\n" + "="*60)
                    print("LATEST PRICE DATA")
                    print("="*60)
                    
                    # Create table header
                    header_row = rows[0]  # First row contains headers
                    header_cells = header_row.find_all(['th', 'td'])
                    headers = [cell.get_text(strip=True) for cell in header_cells]
                    
                    # Only use the first 4 columns to match the header structure
                    # (Date, Buy, Sell, NAV)
                    if len(headers) >= 4:
                        headers = headers[:4]
                    
                    # Create table separator
                    separator = "|" + "|".join(["-" * (max(len(h), 12) + 2) for h in headers]) + "|"
                    
                    # Print header row
                    header_str = "|" + "|".join([f" {h:<{max(len(h), 12)}} " for h in headers]) + "|"
                    print(header_str)
                    print(separator)
                    
                    # Print latest price data (first data row)
                    latest_row = data_rows[0]
                    # Only use first 4 columns to match headers
                    if len(latest_row) >= 4:
                        latest_row = latest_row[:4]
                    
                    row_str = "|" + "|".join([f" {cell:<{max(len(headers[i]), 12)}} " for i, cell in enumerate(latest_row)]) + "|"
                    print(row_str)
                    
                    if len(data_rows) > 1:
                        print("\n" + "="*60)
                        print("PREVIOUS PRICE DATA")
                        print("="*60)
                        print(header_str)
                        print(separator)
                        
                        # Print previous price data (second data row)
                        previous_row = data_rows[1]
                        # Only use first 4 columns to match headers
                        if len(previous_row) >= 4:
                            previous_row = previous_row[:4]
                        
                        row_str = "|" + "|".join([f" {cell:<{max(len(headers[i]), 12)}} " for i, cell in enumerate(previous_row)]) + "|"
                        print(row_str)
                
            else:
                print("This doesn't appear to be a prices table")
            
    except Exception as e:
        print(f"Error extracting table data: {e}")


def main():
    """Main function to run the scraper."""
    # Vanguard URL for the specific fund
    url = "https://www.vanguard.com.au/personal/invest-with-us/fund?portId=8134&tab=prices-and-distributions"
    
    print("Vanguard Stock Price Scraper")
    print("="*40)
    
    # Scrape the page
    soup = scrape_vanguard_page(url)
    
    if soup:
        print("\nSuccessfully scraped the page!")
        
        # Basic page analysis
        print(f"\nPage title: {soup.title.string if soup.title else 'No title found'}")
        
        # Extract and display the historical prices table
        print("\n" + "="*50)
        print("EXTRACTING HISTORICAL PRICES TABLE")
        print("="*50)
        
        extract_historical_prices_table(soup)
        
    else:
        print("Failed to scrape the page. Please check your internet connection and try again.")
        print("Note: You may need to install Chrome and ChromeDriver")


if __name__ == "__main__":
    main()