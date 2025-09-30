#!/usr/bin/env python3
"""
Vanguard Multi-Fund Stock Price Scraper

This script scrapes the Vanguard website to extract historical price data
for multiple funds configured in funds_config.yml.
Each fund gets its own separate NTFY notification.
"""

import time
import yaml
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from notifier import NtfyNotifier


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


def format_for_ntfy(headers, latest_row, previous_row=None):
    """
    Format price data for ntfy notifications (single line, text message style).
    
    Args:
        headers: List of column headers
        latest_row: Latest price data row
        previous_row: Previous price data row (optional)
        
    Returns:
        str: Formatted message for ntfy
    """
    # Extract key data
    date = latest_row[0] if len(latest_row) > 0 else "N/A"
    
    # Determine table type and format accordingly
    if 'Date' in headers and 'Buy' in headers and 'Sell' in headers:
        # Daily prices table - shortened format to avoid truncation
        buy_price = latest_row[1] if len(latest_row) > 1 else "N/A"
        sell_price = latest_row[2] if len(latest_row) > 2 else "N/A"
        
        # Add price change if previous data available
        if previous_row and len(latest_row) >= 2 and len(previous_row) >= 2:
            try:
                latest_price = float(latest_row[1].replace('$', '').replace(',', ''))
                previous_price = float(previous_row[1].replace('$', '').replace(',', ''))
                change = latest_price - previous_price
                change_percent = (change / previous_price) * 100
                
                direction = "UP" if change > 0 else "DOWN" if change < 0 else "SAME"
                # Shortened message to avoid truncation and emoji issues
                message = f"VG Fund {date}: {buy_price}/{sell_price} {direction} {change_percent:+.1f}%"
            except (ValueError, IndexError):
                # Fallback to basic format if calculation fails
                message = f"VG Fund {date}: Buy {buy_price}, Sell {sell_price}"
        else:
            # No previous data available
            message = f"VG Fund {date}: Buy {buy_price}, Sell {sell_price}"
    
    elif 'Distribution date' in headers:
        # Distribution table - shortened format
        cpu = latest_row[1] if len(latest_row) > 1 else "N/A"
        reinvest_price = latest_row[3] if len(latest_row) > 3 else "N/A"
        
        # Add price change if previous data available
        if previous_row and len(latest_row) >= 4 and len(previous_row) >= 4:
            try:
                latest_price = float(latest_row[3].replace('$', '').replace(',', ''))
                previous_price = float(previous_row[3].replace('$', '').replace(',', ''))
                change = latest_price - previous_price
                change_percent = (change / previous_price) * 100
                
                direction = "UP" if change > 0 else "DOWN" if change < 0 else "SAME"
                # Shortened message to avoid truncation and emoji issues
                message = f"VG Dist {date}: {reinvest_price} {direction} {change_percent:+.1f}%"
            except (ValueError, IndexError):
                # Fallback to basic format if calculation fails
                message = f"VG Dist {date}: CPU {cpu}, Price {reinvest_price}"
        else:
            # No previous data available
            message = f"VG Dist {date}: CPU {cpu}, Price {reinvest_price}"
    
    else:
        # Generic format for other table types
        message = f"VG Fund {date}"
        for i, header in enumerate(headers[:3]):  # Show first 3 columns
            if i < len(latest_row) and i > 0:  # Skip date (already shown)
                value = latest_row[i]
                message += f", {header}: {value}"
    
    return message


def format_for_slack(headers, latest_row, previous_row=None):
    """
    Format price data for Slack messages.
    
    Args:
        headers: List of column headers
        latest_row: Latest price data row
        previous_row: Previous price data row (optional)
        
    Returns:
        str: Formatted message for Slack
    """
    message = "*📊 Vanguard Fund Price Update*\n\n"
    message += "*Latest Price Data:*\n"
    
    # Format latest data
    for i, header in enumerate(headers[:4]):
        if i < len(latest_row):
            value = latest_row[i]
            message += f"• *{header}:* {value}\n"
    
    # Add previous data if available
    if previous_row:
        message += "\n*Previous Price Data:*\n"
        for i, header in enumerate(headers[:4]):
            if i < len(previous_row):
                value = previous_row[i]
                message += f"• *{header}:* {value}\n"
        
        # Calculate and add price change
        if len(latest_row) >= 2 and len(previous_row) >= 2:
            try:
                latest_price = float(latest_row[1].replace('$', '').replace(',', ''))
                previous_price = float(previous_row[1].replace('$', '').replace(',', ''))
                change = latest_price - previous_price
                change_percent = (change / previous_price) * 100
                
                direction = "📈 UP" if change > 0 else "📉 DOWN" if change < 0 else "➡️ UNCHANGED"
                message += f"\n*Price Change:* ${change:+.4f} ({change_percent:+.2f}%) {direction}"
            except (ValueError, IndexError):
                message += "\n*Price change calculation not available*"
    
    return message


def extract_historical_prices_table(soup):
    """
    Extract and display the historical prices table from the parsed HTML.
    
    Args:
        soup: BeautifulSoup object containing the parsed HTML
        
    Returns:
        str: ntfy-formatted message or None if no valid data found
    """
    try:
        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables on the page")
        
        if not tables:
            print("No tables found on the page")
            return None
        
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
                    # Get table headers
                    header_row = rows[0]  # First row contains headers
                    header_cells = header_row.find_all(['th', 'td'])
                    headers = [cell.get_text(strip=True) for cell in header_cells]
                    
                    latest_row = data_rows[0]
                    previous_row = data_rows[1] if len(data_rows) > 1 else None
                    
                    # Display latest price data in Slack-compatible format
                    print("\n" + "="*50)
                    print("📊 LATEST PRICE DATA")
                    print("="*50)
                    
                    # Display each field in Slack-compatible format
                    for i, header in enumerate(headers[:4]):  # Only first 4 columns
                        if i < len(latest_row):
                            value = latest_row[i]
                            print(f"*{header}:* {value}")
                    
                    if previous_row:
                        print("\n" + "="*50)
                        print("📈 PREVIOUS PRICE DATA")
                        print("="*50)
                        
                        # Display each field in Slack-compatible format
                        for i, header in enumerate(headers[:4]):  # Only first 4 columns
                            if i < len(previous_row):
                                value = previous_row[i]
                                print(f"*{header}:* {value}")
                        
                        # Show price change if possible
                        if len(latest_row) >= 2 and len(previous_row) >= 2:
                            try:
                                latest_price = float(latest_row[1].replace('$', '').replace(',', ''))
                                previous_price = float(previous_row[1].replace('$', '').replace(',', ''))
                                change = latest_price - previous_price
                                change_percent = (change / previous_price) * 100
                                
                                print("\n" + "="*50)
                                print("📊 PRICE CHANGE")
                                print("="*50)
                                print(f"*Price Change:* ${change:+.4f}")
                                print(f"*Change %:* {change_percent:+.2f}%")
                                print(f"*Direction:* {'📈 UP' if change > 0 else '📉 DOWN' if change < 0 else '➡️ UNCHANGED'}")
                            except (ValueError, IndexError):
                                pass  # Skip price change calculation if data is invalid
                    
                    # Display ntfy-formatted message (single line, text message style)
                    print("\n" + "="*60)
                    print("NTFY MESSAGE FORMAT")
                    print("="*60)
                    ntfy_message = format_for_ntfy(headers, latest_row, previous_row)
                    print(ntfy_message)
                    
                    # Display Slack-formatted message
                    print("\n" + "="*60)
                    print("SLACK MESSAGE FORMAT")
                    print("="*60)
                    slack_message = format_for_slack(headers, latest_row, previous_row)
                    print(slack_message)
                    
                    # Return the ntfy message for the first valid table found
                    return ntfy_message
                
            else:
                print("This doesn't appear to be a prices table")
            
    except Exception as e:
        print(f"Error extracting table data: {e}")
    
    return None


def load_funds_config(config_path="funds_config.yml"):
    """
    Load funds configuration from YAML file.
    
    Args:
        config_path (str): Path to the configuration file
        
    Returns:
        list: List of fund configurations
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            return config.get('funds', [])
    except FileNotFoundError:
        print(f"❌ Configuration file '{config_path}' not found!")
        return []
    except yaml.YAMLError as e:
        print(f"❌ Error parsing configuration file: {e}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error loading configuration: {e}")
        return []


def scrape_fund(fund_config, notifier):
    """
    Scrape a single fund and send notification.
    
    Args:
        fund_config (dict): Fund configuration containing name and url
        notifier (NtfyNotifier): The notification handler
    """
    fund_name = fund_config.get('name', 'Unknown Fund')
    url = fund_config.get('url', '')
    
    print(f"\n{'='*60}")
    print(f"SCRAPING: {fund_name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        # Scrape the page
        soup = scrape_vanguard_page(url)
        
        if soup:
            print(f"\n✅ Successfully scraped {fund_name}!")
            
            # Basic page analysis
            print(f"\nPage title: {soup.title.string if soup.title else 'No title found'}")
            
            # Extract and display the historical prices table
            print("\n" + "="*50)
            print("EXTRACTING HISTORICAL PRICES TABLE")
            print("="*50)
            
            # Extract data and get the ntfy message
            ntfy_message = extract_historical_prices_table(soup)
            
            # Send notification if we got a valid message
            if ntfy_message:
                print("\n" + "="*50)
                print("SENDING NOTIFICATION")
                print("="*50)
                notifier.send_price_update(ntfy_message, fund_name)
            else:
                print(f"\n❌ No valid price data found for {fund_name}")
                
        else:
            error_msg = f"Failed to scrape {fund_name}. Please check your internet connection and try again."
            print(f"❌ {error_msg}")
            print("Note: You may need to install Chrome and ChromeDriver")
            notifier.send_error_notification(error_msg, fund_name)
            
    except Exception as e:
        error_msg = f"Unexpected error occurred while scraping {fund_name}: {str(e)}"
        print(f"\n❌ {error_msg}")
        notifier.send_error_notification(error_msg, fund_name)


def main():
    """Main function to run the scraper for multiple funds."""
    # Initialize notifier
    notifier = NtfyNotifier()
    
    print("Vanguard Multi-Fund Stock Price Scraper")
    print("="*50)
    
    # Load funds configuration
    funds = load_funds_config()
    
    if not funds:
        print("❌ No funds configured. Please check your funds_config.yml file.")
        return
    
    print(f"📊 Found {len(funds)} fund(s) to scrape:")
    for i, fund in enumerate(funds, 1):
        print(f"  {i}. {fund.get('name', 'Unknown Fund')}")
    
    # Process each fund
    successful_scrapes = 0
    failed_scrapes = 0
    
    for fund in funds:
        try:
            scrape_fund(fund, notifier)
            successful_scrapes += 1
        except Exception as e:
            print(f"❌ Failed to process fund {fund.get('name', 'Unknown')}: {e}")
            failed_scrapes += 1
        
        # Add a small delay between funds to be respectful to the server
        if len(funds) > 1:
            print("\n⏳ Waiting 3 seconds before next fund...")
            time.sleep(3)
    
    # Summary
    print(f"\n{'='*60}")
    print("SCRAPING SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful scrapes: {successful_scrapes}")
    print(f"❌ Failed scrapes: {failed_scrapes}")
    print(f"📊 Total funds processed: {len(funds)}")


if __name__ == "__main__":
    main()