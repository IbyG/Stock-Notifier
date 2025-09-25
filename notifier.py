#!/usr/bin/env python3
"""
Notification module for sending ntfy alerts.

This module handles sending notifications via ntfy for Vanguard fund price updates.
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class NtfyNotifier:
    """
    Handles sending notifications via ntfy.
    """
    
    def __init__(self):
        """Initialize the ntfy notifier with configuration from environment variables."""
        self.ntfy_url = os.getenv('NTFY_URL', 'http://192.168.0.2:6244/vanguard_not')
        self.default_priority = os.getenv('NTFY_PRIORITY', 'default')
        self.default_tags = os.getenv('NTFY_TAGS', 'chart_with_upwards_trend,heavy_dollar_sign')
        
    def send_price_update(self, message, title="Vanguard Fund Price Update"):
        """
        Send a price update notification via ntfy.
        
        Args:
            message (str): The message content to send
            title (str): The notification title (optional)
        """
        try:
            response = requests.post(
                self.ntfy_url,
                data=message,
                headers={
                    "Title": title,
                    "Priority": self.default_priority,
                    "Tags": self.default_tags
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Notification sent successfully via ntfy")
                return True
            else:
                print(f"❌ Failed to send notification. Status code: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error sending notification: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error sending notification: {e}")
            return False
    
    def send_error_notification(self, error_message):
        """
        Send an error notification via ntfy.
        
        Args:
            error_message (str): The error message to send
        """
        try:
            response = requests.post(
                self.ntfy_url,
                data=f"Error in Vanguard scraper: {error_message}",
                headers={
                    "Title": "Vanguard Scraper Error",
                    "Priority": "high",
                    "Tags": "rotating_light,exclamation"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Error notification sent successfully via ntfy")
                return True
            else:
                print(f"❌ Failed to send error notification. Status code: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error sending error notification: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error sending error notification: {e}")
            return False


def test_notification():
    """Test function to verify ntfy configuration."""
    notifier = NtfyNotifier()
    print(f"Testing ntfy notification...")
    print(f"URL: {notifier.ntfy_url}")
    print(f"Priority: {notifier.default_priority}")
    print(f"Tags: {notifier.default_tags}")
    
    test_message = "🧪 Test notification from Vanguard Stock Notifier"
    success = notifier.send_price_update(test_message, "Test Notification")
    
    if success:
        print("✅ Test notification sent successfully!")
    else:
        print("❌ Test notification failed!")
    
    return success


if __name__ == "__main__":
    test_notification()
