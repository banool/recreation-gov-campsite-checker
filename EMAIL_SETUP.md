# 📧 Email Notifications Setup

Get notified instantly when campsites become available! The email notifications include direct booking links for each available campsite.

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
python setup_email.py
```

### Option 2: Manual Setup

1. **Set up environment variables:**
```bash
export CAMPSITE_FROM_EMAIL="your-email@gmail.com"
export CAMPSITE_TO_EMAIL="recipient@gmail.com"  
export CAMPSITE_EMAIL_PASSWORD="your-app-password"
```

2. **For Gmail users:** You need an "App Password" (not your regular password):
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Enable 2-Factor Authentication
   - Generate an App Password for "Mail"
   - Use that 16-character password

**📱 Phone Notification Tip:** If using the same Gmail account for sender and receiver, use a Gmail alias for the sender to get phone notifications. For example:
- **From:** `youremail+campsites@gmail.com`
- **To:** `youremail@gmail.com`

This tricks your phone into treating it as a "new email" and you'll get notifications!

3. **Add to your shell profile** (optional, to persist across sessions):
```bash
echo 'export CAMPSITE_FROM_EMAIL="your-email@gmail.com"' >> ~/.bashrc
echo 'export CAMPSITE_TO_EMAIL="recipient@gmail.com"' >> ~/.bashrc  
echo 'export CAMPSITE_EMAIL_PASSWORD="your-app-password"' >> ~/.bashrc
source ~/.bashrc
```

## 📧 Usage

Add the `--email-notifications` flag to your camping.py command:

```bash
python camping.py --email-notifications --parks 232447 --start-date 2024-07-01 --end-date 2024-07-07
```

## 🎯 What You'll Get

When campsites become available, you'll receive an email with:
- **Park name and availability count**
- **Specific campsite numbers**  
- **Available date ranges**
- **Direct booking links** for each campsite
- **Mobile-friendly HTML formatting**

## 🔧 Advanced Configuration

For non-Gmail providers, set additional variables:
```bash
export CAMPSITE_SMTP_SERVER="smtp.your-provider.com"
export CAMPSITE_SMTP_PORT="587"
```

## 🧪 Testing

Test your email setup:
```bash
python email_notifier.py
```

## 🔍 Troubleshooting

**"Authentication failed"**: Make sure you're using an App Password, not your regular Gmail password.

**"Connection refused"**: Check your SMTP server and port settings.

**"No email config"**: Ensure all environment variables are set correctly.

## 💡 Pro Tips

1. **Run continuously**: The script checks every 20 seconds, so leave it running in the background
2. **Multiple recipients**: Set `CAMPSITE_TO_EMAIL` to a comma-separated list
3. **Combine with sound**: Email notifications work alongside the existing sound alerts
4. **Mobile notifications**: Forward emails to your phone for instant alerts

## 🏕️ Example Email Content

```
🏕️ CAMPSITES AVAILABLE! 🏕️

🎯 Yosemite National Park (232447)
2 site(s) available out of 50

Available sites and dates:
• Site 067:
  📅 2024-07-15 → 2024-07-17
  🔗 BOOK NOW: https://www.recreation.gov/camping/campsites/67890

⚡ Act fast - campsites can book up quickly!
```
