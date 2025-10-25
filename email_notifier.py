# -*- coding: utf-8 -*-
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import sys
import time
import json
from hashlib import md5

def send_email_notification(availabilities_info, email_config, min_interval_minutes=5):
    """
    Send email notification when campsites are available.
    Rate limited to prevent spam - only sends if enough time has passed since last email.
    
    Args:
        availabilities_info: Dict with park info and available sites
        email_config: Dict with email configuration
        min_interval_minutes: Minimum minutes between emails (default: 5)
    
    Returns:
        bool: True if email was sent, False if rate limited or failed
    """
    
    # Check rate limiting
    if not should_send_email(availabilities_info, min_interval_minutes):
        print(f"⏰ Email rate limited - waiting {min_interval_minutes} minutes between notifications")
        return False
    
    # Create message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🏕️ Campsites Available! - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    msg["From"] = email_config["from_email"]
    msg["To"] = email_config["to_email"]
    
    # Create email content
    text_content, html_content = generate_email_content(availabilities_info)
    
    # Create text and HTML parts
    text_part = MIMEText(text_content, "plain")
    html_part = MIMEText(html_content, "html")
    
    msg.attach(text_part)
    msg.attach(html_part)
    
    # Send email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"]) as server:
            server.starttls(context=context)
            server.login(email_config["from_email"], email_config["password"])
            server.sendmail(email_config["from_email"], email_config["to_email"], msg.as_string())
        print(f"✅ Email notification sent to {email_config['to_email']}")
        
        # Update the last sent time
        update_last_email_time(availabilities_info)
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def should_send_email(availabilities_info, min_interval_minutes):
    """
    Check if enough time has passed since the last email for this availability set.
    Uses a hash of the availability info to track different campsite combinations.
    
    Args:
        availabilities_info: Dict with park info and available sites
        min_interval_minutes: Minimum minutes between emails
    
    Returns:
        bool: True if email should be sent, False if rate limited
    """
    # Create a hash of the availability info to track different combinations
    availability_hash = create_availability_hash(availabilities_info)
    timestamp_file = f".email_timestamp_{availability_hash}.json"
    
    try:
        if os.path.exists(timestamp_file):
            with open(timestamp_file, 'r') as f:
                data = json.load(f)
                last_sent_time = data.get('last_sent', 0)
                
                # Check if enough time has passed
                current_time = time.time()
                time_since_last = (current_time - last_sent_time) / 60  # Convert to minutes
                
                if time_since_last < min_interval_minutes:
                    remaining_minutes = min_interval_minutes - time_since_last
                    print(f"⏰ Last email sent {time_since_last:.1f} minutes ago. Waiting {remaining_minutes:.1f} more minutes.")
                    return False
        
        return True
    except Exception as e:
        print(f"⚠️ Error checking email rate limit: {e}")
        return True  # Allow email if we can't check the rate limit

def update_last_email_time(availabilities_info):
    """Update the timestamp file with the current time."""
    availability_hash = create_availability_hash(availabilities_info)
    timestamp_file = f".email_timestamp_{availability_hash}.json"
    
    try:
        data = {
            'last_sent': time.time(),
            'sent_at': datetime.now().isoformat()
        }
        with open(timestamp_file, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"⚠️ Error updating email timestamp: {e}")

def create_availability_hash(availabilities_info):
    """
    Create a hash of the availability info to track different campsite combinations.
    This ensures we rate limit per unique set of available campsites.
    """
    # Create a simplified representation for hashing
    hash_data = {}
    for park_id, (current, maximum, available_dates_by_site_id, park_name) in availabilities_info.items():
        if current > 0:
            # Include park and available site IDs in hash
            site_ids = sorted(available_dates_by_site_id.keys()) if available_dates_by_site_id else []
            hash_data[park_id] = {
                'park_name': park_name,
                'site_ids': site_ids
            }
    
    # Create hash from the data
    hash_string = json.dumps(hash_data, sort_keys=True)
    return md5(hash_string.encode('utf-8')).hexdigest()[:8]

def generate_email_content(availabilities_info):
    """Generate both text and HTML email content."""
    
    text_lines = ["🏕️ CAMPSITES AVAILABLE! 🏕️", ""]
    html_lines = [
        "<html><body>",
        "<h2>🏕️ CAMPSITES AVAILABLE! 🏕️</h2>",
        "<p>Great news! Campsites are now available for your dates:</p>"
    ]
    
    for park_id, (current, maximum, available_dates_by_site_id, park_name) in availabilities_info.items():
        if current > 0:
            text_lines.append(f"🎯 {park_name} ({park_id}): {current} site(s) available out of {maximum}")
            html_lines.append(f"<h3>🎯 {park_name} ({park_id})</h3>")
            html_lines.append(f"<p><strong>{current} site(s) available out of {maximum}</strong></p>")
            
            if available_dates_by_site_id:
                text_lines.append("Available sites and dates:")
                html_lines.append("<ul>")
                
                for site_id, dates in available_dates_by_site_id.items():
                    booking_url = f"https://www.recreation.gov/camping/campsites/{site_id}"
                    text_lines.append(f"  • Site {site_id}:")
                    html_lines.append(f"<li><strong>Site {site_id}</strong>:")
                    
                    for date_range in dates:
                        start_date = date_range["start"]
                        end_date = date_range["end"]
                        text_lines.append(f"    - {start_date} → {end_date}")
                        html_lines.append(f"<br>&nbsp;&nbsp;📅 {start_date} → {end_date}")
                    
                    text_lines.append(f"    🔗 Book now: {booking_url}")
                    html_lines.append(f'<br>&nbsp;&nbsp;<a href="{booking_url}" style="color: #0066cc; font-weight: bold;">🔗 BOOK NOW</a>')
                    html_lines.append("</li><br>")
                
                html_lines.append("</ul>")
            
            text_lines.append("")
    
    text_lines.extend([
        "⚡ Act fast - campsites can book up quickly!",
        "",
        "Happy camping! 🏕️"
    ])
    
    html_lines.extend([
        "<p style='color: #ff6600; font-weight: bold;'>⚡ Act fast - campsites can book up quickly!</p>",
        "<p>Happy camping! 🏕️</p>",
        "</body></html>"
    ])
    
    return "\n".join(text_lines), "\n".join(html_lines)

def load_email_config():
    """Load email configuration from environment variables or config file."""
    
    # Try environment variables first (most secure)
    config = {
        "smtp_server": os.getenv("CAMPSITE_SMTP_SERVER", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("CAMPSITE_SMTP_PORT", "587")),
        "from_email": os.getenv("CAMPSITE_FROM_EMAIL"),
        "password": os.getenv("CAMPSITE_EMAIL_PASSWORD"),
        "to_email": os.getenv("CAMPSITE_TO_EMAIL")
    }
    
    # Check if all required fields are present
    if not all([config["from_email"], config["password"], config["to_email"]]):
        print("❌ Email configuration missing. Please set environment variables:")
        print("   CAMPSITE_FROM_EMAIL=your-email@gmail.com")
        print("   CAMPSITE_EMAIL_PASSWORD=your-app-password")
        print("   CAMPSITE_TO_EMAIL=recipient@gmail.com")
        print("   Optional: CAMPSITE_SMTP_SERVER (default: smtp.gmail.com)")
        print("   Optional: CAMPSITE_SMTP_PORT (default: 587)")
        return None
    
    return config

if __name__ == "__main__":
    # Test the email functionality
    print("Testing email notification...")
    
    config = load_email_config()
    if not config:
        sys.exit(1)
    
    # Test data
    test_availabilities = {
        "12345": (2, 50, {
            "67890": [{"start": "2024-07-15", "end": "2024-07-17"}],
            "67891": [{"start": "2024-07-20", "end": "2024-07-22"}]
        }, "Test Campground")
    }
    
    success = send_email_notification(test_availabilities, config)
    if success:
        print("✅ Test email sent successfully!")
    else:
        print("❌ Test email failed!")
