# Stock Notifier

A Python application to scrape and monitor Vanguard fund prices with automatic ntfy notifications.

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

3. Run the scraper:
```bash
python vanguard_scraper.py
```

## Features

- Scrapes Vanguard fund price data
- Displays page content in terminal
- Extracts historical prices table data
- Sends automatic ntfy notifications with price updates
- Supports multiple output formats (terminal, Slack, ntfy)
- Error handling with notification alerts

## Configuration

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

- `vanguard_scraper.py` - Main scraper script
- `notifier.py` - Notification module for ntfy integration
- `.env` - Environment configuration (not tracked in git)
- `.env.example` - Example environment configuration
- `requirements.txt` - Python dependencies
