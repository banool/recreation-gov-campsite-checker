#!/usr/bin/env python3
"""
Setup script to help configure email notifications for the campsite checker.
"""

import os
import sys
from email_notifier import send_email_notification, load_email_config

def setup_email_config():
    """Interactive setup for email configuration."""
    
    print("🏕️ Campsite Email Notification Setup")
    print("=" * 40)
    print()
    
    print("This will help you set up email notifications for when campsites become available.")
    print("You'll need a Gmail account (or other SMTP provider) to send notifications.")
    print()
    
    # Get email configuration
    from_email = input("📧 Enter your Gmail address (sender): ").strip()
    to_email = input("📧 Enter recipient email address: ").strip()
    
    print()
    print("🔐 For Gmail, you'll need an 'App Password' (not your regular password):")
    print("   1. Go to https://myaccount.google.com/security")
    print("   2. Enable 2-Factor Authentication if not already enabled")
    print("   3. Go to 'App passwords' and generate a new password")
    print("   4. Use that 16-character password below")
    print()
    
    password = input("🔑 Enter your Gmail app password: ").strip()
    
    # Optional SMTP settings
    print()
    use_custom_smtp = input("🔧 Use custom SMTP settings? (y/N): ").strip().lower()
    
    if use_custom_smtp == 'y':
        smtp_server = input("📡 SMTP server (default: smtp.gmail.com): ").strip() or "smtp.gmail.com"
        smtp_port = input("🔌 SMTP port (default: 587): ").strip() or "587"
    else:
        smtp_server = "smtp.gmail.com"
        smtp_port = "587"
    
    # Generate environment variable commands
    print()
    print("✅ Configuration complete! Add these to your environment:")
    print("=" * 50)
    print(f"export CAMPSITE_FROM_EMAIL='{from_email}'")
    print(f"export CAMPSITE_TO_EMAIL='{to_email}'")
    print(f"export CAMPSITE_EMAIL_PASSWORD='{password}'")
    if smtp_server != "smtp.gmail.com":
        print(f"export CAMPSITE_SMTP_SERVER='{smtp_server}'")
    if smtp_port != "587":
        print(f"export CAMPSITE_SMTP_PORT='{smtp_port}'")
    print()
    
    # Option to add to shell profile
    shell_profile = os.path.expanduser("~/.bashrc")
    if os.path.exists(os.path.expanduser("~/.zshrc")):
        shell_profile = os.path.expanduser("~/.zshrc")
    
    add_to_profile = input(f"📝 Add these to {shell_profile}? (y/N): ").strip().lower()
    
    if add_to_profile == 'y':
        with open(shell_profile, 'a') as f:
            f.write("\n# Campsite email notification settings\n")
            f.write(f"export CAMPSITE_FROM_EMAIL='{from_email}'\n")
            f.write(f"export CAMPSITE_TO_EMAIL='{to_email}'\n")
            f.write(f"export CAMPSITE_EMAIL_PASSWORD='{password}'\n")
            if smtp_server != "smtp.gmail.com":
                f.write(f"export CAMPSITE_SMTP_SERVER='{smtp_server}'\n")
            if smtp_port != "587":
                f.write(f"export CAMPSITE_SMTP_PORT='{smtp_port}'\n")
        
        print(f"✅ Added to {shell_profile}")
        print("🔄 Run 'source ~/.bashrc' (or restart terminal) to load the settings")
    
    # Test email
    print()
    test_email = input("📧 Send a test email now? (y/N): ").strip().lower()
    
    if test_email == 'y':
        # Set environment variables temporarily for testing
        os.environ["CAMPSITE_FROM_EMAIL"] = from_email
        os.environ["CAMPSITE_TO_EMAIL"] = to_email
        os.environ["CAMPSITE_EMAIL_PASSWORD"] = password
        os.environ["CAMPSITE_SMTP_SERVER"] = smtp_server
        os.environ["CAMPSITE_SMTP_PORT"] = smtp_port
        
        print("📤 Sending test email...")
        
        # Test data
        test_availabilities = {
            "12345": (2, 50, {
                "67890": [{"start": "2024-07-15", "end": "2024-07-17"}],
                "67891": [{"start": "2024-07-20", "end": "2024-07-22"}]
            }, "Test Campground - Setup")
        }
        
        config = load_email_config()
        if config:
            success = send_email_notification(test_availabilities, config)
            if success:
                print("✅ Test email sent successfully!")
                print("🎉 Email notifications are now configured!")
            else:
                print("❌ Test email failed. Please check your settings.")
        else:
            print("❌ Configuration error. Please try again.")
    
    print()
    print("🏕️ Usage:")
    print("   python camping.py --email-notifications --parks 12345 --start-date 2024-07-01 --end-date 2024-07-07")
    print()

if __name__ == "__main__":
    setup_email_config()
