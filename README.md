# Stock Notifier

A Python application to scrape and monitor multiple Vanguard fund prices with automatic ntfy notifications for each fund.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure ntfy notifications:
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your ntfy server details
nano .env
```

3. Configure your funds:
```bash
# Edit funds_config.yml to add/modify the Vanguard funds you want to monitor
nano funds_config.yml
```

See [Multi-Fund Configuration Guide](MultiFundGuide.md) for detailed instructions on setting up multiple funds.

4. Run the scraper:
```bash
python vanguard_scraper.py
```

## Features

- **Multi-Fund Support**: Monitor multiple Vanguard funds simultaneously
- **Separate Notifications**: Each fund sends its own ntfy notification
- **YAML Configuration**: Easy fund management via `funds_config.yml`
- Scrapes Vanguard fund price data
- Displays page content in terminal
- Extracts historical prices table data
- Sends automatic ntfy notifications with price updates
- Supports multiple output formats (terminal, Slack, ntfy)
- Error handling with fund-specific notification alerts

## Configuration

### Fund Configuration (funds_config.yml)

Configure which Vanguard funds to monitor in `funds_config.yml`:

```yaml
funds:
  - name: "Vanguard Australian Shares Index Fund"
    url: "https://www.vanguard.com.au/personal/invest-with-us/fund?portId=8110&tab=prices-and-distributions"
    port_id: "8110"
    
  - name: "Vanguard Growth Index Fund"
    url: "https://www.vanguard.com.au/personal/invest-with-us/fund?portId=8133&tab=prices-and-distributions"
    port_id: "8133"
```

**📖 For detailed instructions on adding/configuring funds, see the [Multi-Fund Configuration Guide](MultiFundGuide.md)**

### Environment Variables (.env file)

```bash
# ntfy Configuration
NTFY_URL=http://192.168.0.2:6244/vanguard_not
NTFY_PRIORITY=default
NTFY_TAGS=chart_with_upwards_trend,heavy_dollar_sign
```

### Notification Options

- **NTFY_URL**: Your ntfy server URL and topic
- **NTFY_PRIORITY**: Notification priority (default, high, urgent)
- **NTFY_TAGS**: Comma-separated tags for the notification

## Usage

### Basic Usage
```bash
python vanguard_scraper.py
```

### Test Notifications
```bash
python notifier.py
```

## Output Formats

The script provides three output formats:

1. **Terminal Display**: Detailed breakdown with all data
2. **Slack Format**: Multi-line formatted message for Slack channels  
3. **ntfy Format**: Single-line, text message style for mobile notifications

## Files

- `vanguard_scraper.py` - Main scraper script with multi-fund support
- `notifier.py` - Notification module for ntfy integration
- `funds_config.yml` - YAML configuration for funds to monitor
- `MultiFundGuide.md` - Detailed guide for multi-fund configuration
- `.env` - Environment configuration (not tracked in git)
- `.env.example` - Example environment configuration
- `requirements.txt` - Python dependencies

## How It Works

1. The scraper reads all configured funds from `funds_config.yml`
2. Each fund is scraped sequentially with a 3-second delay between requests
3. Price data is extracted from each fund's page
4. A separate ntfy notification is sent for each fund with its specific name and price data
5. A summary of successful and failed scrapes is displayed at the end

## Adding New Funds

To monitor additional funds:

1. Find the Vanguard fund page you want to monitor
2. Note the `portId` from the URL (e.g., `portId=8110`)
3. Add a new entry to `funds_config.yml` following the existing format
4. Run the scraper - it will automatically process all configured funds

For more details, see the [Multi-Fund Configuration Guide](MultiFundGuide.md).
