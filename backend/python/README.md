# Python Campsite Checker

Core Python logic for checking campsite availability on recreation.gov. This can be used standalone via the command line or integrated with the Node.js backend for the web interface.

## Prerequisites

- Python 3.9+

## Installation

```bash
# Create virtual environment (if not already created)
cd ../..  # Go to project root
python3 -m venv myvenv

# Activate virtual environment
source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate

# Install dependencies
cd backend/python
pip install -r requirements.txt
```

## Command Line Usage

### Basic Search

```bash
python camping.py \
  --start-date 2025-06-01 \
  --end-date 2025-06-05 \
  --parks 232448 232450 \
  --nights 2
```

### With Email Notifications

```bash
# Ensure email environment variables are set in backend/.env
python camping.py \
  --start-date 2025-06-01 \
  --end-date 2025-06-05 \
  --parks 232448 \
  --nights 2 \
  --email-notifications
```

### Weekends Only

```bash
python camping.py \
  --start-date 2025-06-01 \
  --end-date 2025-06-30 \
  --parks 232448 \
  --nights 2 \
  --weekends-only
```

### Specific Campsite IDs

```bash
python camping.py \
  --start-date 2025-06-01 \
  --end-date 2025-06-30 \
  --parks 232431 \
  --campsite-ids 18621 18622 \
  --nights 2
```

### With Detailed Info

```bash
python camping.py \
  --start-date 2025-06-01 \
  --end-date 2025-06-05 \
  --parks 232448 \
  --show-campsite-info \
  --nights 2
```

### JSON Output

```bash
python camping.py \
  --start-date 2025-06-01 \
  --end-date 2025-06-05 \
  --parks 232448 \
  --nights 2 \
  --json-output
```

## Command Line Options

```
usage: camping.py [-h] [--debug] --start-date START_DATE --end-date END_DATE
                  [--nights NIGHTS] [--campsite-ids CAMPSITE_IDS [CAMPSITE_IDS ...]]
                  [--show-campsite-info] [--campsite-type CAMPSITE_TYPE]
                  [--json-output] [--weekends-only] [--exclusion-file EXCLUSION_FILE]
                  [--excluded-dates EXCLUDED_DATES [EXCLUDED_DATES ...]]
                  [--email-notifications]
                  (--parks park [park ...] | --stdin)

Options:
  --debug, -d           Debug log level
  --start-date          Start date [YYYY-MM-DD]
  --end-date            End date [YYYY-MM-DD]
  --nights              Number of consecutive nights (default: 1)
  --parks               Park ID(s)
  --campsite-ids        Specific campsite ID(s) (optional)
  --show-campsite-info  Display campsite ID and availability dates
  --campsite-type       Filter by campsite type (e.g., "STANDARD NONELECTRIC")
  --json-output         Output results as JSON
  --weekends-only       Include only weekends (Friday/Saturday starts)
  --email-notifications Send email when sites are available
  --exclusion-file      File with campsite IDs to exclude
  --excluded-dates      Specific dates to exclude [YYYY-MM-DD]
```

## Project Structure

```
python/
├── camping.py              # Main command-line script
├── camping_runner.py       # Entry point for Node.js integration
├── clients/
│   ├── __init__.py
│   └── recreation_client.py  # Recreation.gov API client
├── enums/
│   ├── __init__.py
│   ├── date_format.py
│   └── emoji.py
├── utils/
│   ├── __init__.py
│   ├── camping_argparser.py  # Argument parser
│   └── formatter.py          # Output formatting
├── tests/                    # Unit tests
│   ├── __init__.py
│   ├── test_camping.py
│   ├── test_camping_arg_parser.py
│   └── test_notifier.py
├── notifier.py             # Notification logic
├── email_notifier.py       # Email notifications
├── setup_email.py          # Email setup helper
├── requirements.txt        # Python dependencies
└── excluded-campsites.txt  # List of campsites to exclude
```

## Node.js Integration

The `camping_runner.py` script is used by the Node.js backend:

```python
# camping_runner.py
# Runs camping.py in continuous monitoring mode
# Outputs JSON results that can be parsed by Node.js
```

The Node.js service spawns Python processes using:

```javascript
const pythonProcess = spawn('python', [
  'python/camping_runner.py',
  ...args
], {
  cwd: backendDir,
  env: process.env
});
```

## Email Setup

Create a `backend/.env` file:

```bash
CAMPSITE_FROM_EMAIL=your-email@gmail.com
CAMPSITE_EMAIL_PASSWORD=your-app-password
CAMPSITE_TO_EMAIL=recipient@gmail.com
CAMPSITE_SMTP_SERVER=smtp.gmail.com
CAMPSITE_SMTP_PORT=587
```

Test email setup:

```bash
python email_notifier.py
```

Or use the setup helper:

```bash
python setup_email.py
```

## Testing

Run the test suite:

```bash
python -m unittest discover tests
```

Run specific test:

```bash
python -m unittest tests.test_camping
```

## Development

### Code Formatting

Use `black` for formatting:

```bash
black -l 80 camping.py
```

Use `isort` for import sorting:

```bash
isort camping.py
```

### Adding New Features

1. Modify `camping.py` for core logic
2. Update `camping_argparser.py` for new arguments
3. Update `camping_runner.py` if needed for Node.js integration
4. Add tests in `tests/`
5. Update this README

## Troubleshooting

### Module Not Found

Ensure virtual environment is activated:

```bash
source ../../myvenv/bin/activate  # On Windows: ..\..\myvenv\Scripts\activate
pip install -r requirements.txt
```

### Import Errors

Run from the correct directory:

```bash
# Should be in backend/python/
pwd  # Should show: .../recreation-gov-campsite-checker/backend/python
```

### Email Not Sending

1. Check environment variables are set
2. For Gmail, use app password, not regular password
3. Ensure 2FA is enabled
4. Test with `python email_notifier.py`

### Recreation.gov API Errors

- Check internet connection
- Verify park IDs are valid
- Recreation.gov might be down (check website directly)
- Rate limiting might be in effect (wait a few minutes)

## Dependencies

Key Python packages (see `requirements.txt` for full list):

- `requests` - HTTP client for API calls
- `python-dateutil` - Date parsing and manipulation
- `fake-useragent` - User agent spoofing
- `python-twitter` - Twitter integration (optional)
- `black` - Code formatting
- `isort` - Import sorting

---

For more information, see the main [README.md](../../README.md)

