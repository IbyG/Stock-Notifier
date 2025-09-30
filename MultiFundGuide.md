# Multi-Fund Configuration Guide

## Overview

The Vanguard Stock Notifier has been updated to support multiple funds with separate NTFY notifications for each fund.

## Configuration File

The scraper now reads fund configurations from `funds_config.yml`. This file contains:

- **Fund names**: Human-readable names for each fund
- **URLs**: Direct links to each fund's price page
- **Port IDs**: Vanguard's internal fund identifiers

## Adding New Funds

To add a new fund to monitor:

1. Open `funds_config.yml`
2. Add a new entry under the `funds:` section:

```yaml
funds:
  - name: "Your Fund Name"
    url: "https://www.vanguard.com.au/personal/invest-with-us/fund?portId=XXXX&tab=prices-and-distributions"
    port_id: "XXXX"
```

3. Replace `XXXX` with the actual port ID from Vanguard's website

## NTFY Notifications

Each fund now sends separate NTFY notifications with:

- **Fund-specific titles**: Each notification includes the fund name
- **Individual messages**: Price updates are sent per fund
- **Error handling**: Errors are also fund-specific

## Running the Scraper

The scraper will now:

1. Load all configured funds from `funds_config.yml`
2. Process each fund sequentially
3. Send separate NTFY notifications for each fund
4. Provide a summary of successful/failed scrapes

## Example Output

```
Vanguard Multi-Fund Stock Price Scraper
==================================================
📊 Found 3 fund(s) to scrape:
  1. Vanguard Australian Shares Index Fund
  2. Vanguard International Shares Index Fund
  3. Vanguard Balanced Index Fund

============================================================
SCRAPING: Vanguard Australian Shares Index Fund
URL: https://www.vanguard.com.au/personal/invest-with-us/fund?portId=8134&tab=prices-and-distributions
============================================================
```

## Dependencies

Make sure to install the updated requirements:

```bash
pip install -r requirements.txt
```

The new dependency `PyYAML>=6.0` has been added for configuration file parsing.
