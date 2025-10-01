# Stock Notifier

A Python application to scrape and monitor multiple Vanguard fund prices with automatic ntfy notifications for each fund.

**📚 Educational Purpose**: This repository is intended for educational and learning purposes only.

**📖 [Why This Tool Was Created](UseCase.md)** - Learn about the problem this tool solves and how it can help you save time monitoring your investments.

## ⚠️ **IMPORTANT LEGAL NOTICE** ⚠️

> **🚨 WARNING: Before using this application, you MUST obtain formal written approval from Vanguard's legal and compliance team. This tool accesses Vanguard's website and data in ways that may violate their Terms of Service.**
> 
> **📋 User Responsibility**: By downloading, cloning, or using this code, you acknowledge that:
> - You are solely responsible for ensuring compliance with all applicable laws and Vanguard's Terms of Service
> - You must obtain proper authorization from Vanguard before using this tool
> - The author of this repository is not responsible for any legal consequences, account suspensions, or other issues that may arise from your use of this software
> - You use this software at your own risk and assume full responsibility for your actions

**🔒 Use this tool responsibly and in compliance with all applicable terms of service and laws.**

## Setup

### Option 1: Local Installation

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

### Option 2: Docker (Recommended)

1. Configure your environment and funds:
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your ntfy server details
nano .env

# Edit funds_config.yml to add/modify the Vanguard funds you want to monitor
nano funds_config.yml
```

2. Build the Docker image:
```bash
docker build -t stock-notifier .
```

3. Run the container:
```bash
docker run --rm stock-notifier
```

**Note**: The Docker container includes Chrome and ChromeDriver pre-installed, making it easier to run on any system without manual setup.

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

### Automated Scheduling with Cronjob

To run the scraper automatically every day at 6 AM, you can set up a cronjob that spins up the Docker container, executes the scraper, and then cleans up.

#### Step 1: Create a wrapper script

Create a script called `run-stock-notifier.sh` in your project directory:

```bash
#!/bin/bash
# Script to run Stock Notifier in Docker

# Change to the script's directory
cd "$(dirname "$0")"

# Check if the Docker image exists, build if it doesn't
if ! docker image inspect stock-notifier >/dev/null 2>&1; then
    echo "Docker image 'stock-notifier' not found. Building..."
    docker build -t stock-notifier .
    if [ $? -ne 0 ]; then
        echo "Failed to build Docker image"
        exit 1
    fi
else
    echo "Docker image 'stock-notifier' found"
fi

# Run the container
docker run --rm stock-notifier

# Exit with the same status as the docker command
exit $?
```

Make the script executable:
```bash
chmod +x run-stock-notifier.sh
```

**Note**: This script automatically checks if the Docker image exists and builds it if needed, so you don't have to manually build the image before setting up the cronjob.

#### Step 2: Set up the cronjob

Open your crontab for editing:
```bash
crontab -e
```

Add the following line to run the scraper at 6 AM every day:
```bash
# Run Stock Notifier every day at 6:00 AM
0 6 * * * /Absolute/Path/To/Stock-Notifier/run-stock-notifier.sh >> /Absolute/Path/To/Stock-Notifier/cron.log 2>&1
```

**Important Notes:**
- Replace `/Absolute/Path/To/Stock-Notifier/` with the actual absolute path to your project directory
- The output will be logged to `cron.log` in your project directory
- The Docker container automatically spins down after execution due to the `--rm` flag
- The wrapper script automatically builds the image if it doesn't exist, so no manual build is required
- Ensure Docker daemon is running on your system
- To view cronjob logs: `tail -f /Absolute/Path/To/Stock-Notifier/cron.log`

#### Step 3: Verify the cronjob

To verify your cronjob is set up correctly:
```bash
# List all cronjobs
crontab -l

# Check if Docker image exists
docker images stock-notifier

# Test the wrapper script manually
/Absolute/Path/To/Stock-Notifier/run-stock-notifier.sh
```

**Useful Docker commands:**
```bash
# Check if the Docker image exists
docker images stock-notifier

# View all Docker images
docker images

# Manually build the image (if needed)
docker build -t stock-notifier .

# Remove the image to force a rebuild
docker rmi stock-notifier
```

#### Alternative: Using systemd timer (for more control)

If you prefer systemd timers over cron, create two files:

**stock-notifier.service**:
```ini
[Unit]
Description=Stock Notifier Service
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
WorkingDirectory=/Absolute/Path/To/Stock-Notifier
ExecStart=/usr/bin/docker run --rm stock-notifier
StandardOutput=append:/Absolute/Path/To/Stock-Notifier/cron.log
StandardError=append:/Absolute/Path/To/Stock-Notifier/cron.log

[Install]
WantedBy=multi-user.target
```

**Note**: Replace `/Absolute/Path/To/Stock-Notifier` with your actual project directory path.

**stock-notifier.timer**:
```ini
[Unit]
Description=Run Stock Notifier daily at 6 AM

[Timer]
OnCalendar=*-*-* 06:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start the timer:
```bash
sudo cp stock-notifier.service stock-notifier.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable stock-notifier.timer
sudo systemctl start stock-notifier.timer

# Check timer status
sudo systemctl status stock-notifier.timer
sudo systemctl list-timers --all | grep stock-notifier
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
- `Dockerfile` - Docker configuration for containerized deployment
- `.dockerignore` - Files to exclude from Docker build
- `run-stock-notifier.sh` - Wrapper script for cronjob execution (optional)

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
