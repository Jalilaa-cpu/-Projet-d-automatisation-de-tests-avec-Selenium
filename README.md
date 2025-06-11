# Weather Shopper Automated Test Suite

This repository contains a robust, production-style automated end-to-end test suite for the [Weather Shopper](https://weathershopper.pythonanywhere.com) demo web application. The suite is built using **Selenium WebDriver** and **pytest** in Python, following the Page Object Model (POM) design pattern for maintainability and scalability.

---

## 🚀 Project Purpose

The goal of this project is to **automate the entire user journey** on the Weather Shopper site, including:
- Reading the current temperature
- Selecting the correct products (moisturizers or sunscreens) based on the weather
- Adding the cheapest relevant products to the cart
- Validating cart contents and totals
- Completing a payment using the Stripe Checkout popup
- Verifying payment success

This suite is designed for:
- **Regression testing**
- **Demoing automation best practices**
- **Learning and teaching Selenium with real-world flows**
- **CI/CD integration** (HTML reports and logs for easy review)

---

## 🏗️ Project Structure

```
weather_shopper_tests/
│
├── pages/                  # Page Object Model classes (e.g., payment_page.py)
├── tests/                  # Test scripts (e.g., test_happy_path.py)
├── venv/                   # (optional) Python virtual environment
├── report.html             # Generated HTML test report (after running tests)
├── weather_shopper_automation.log  # Generated log file (after running tests)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## ⚙️ Technologies Used

- **Python 3.8+**
- **Selenium WebDriver** (browser automation)
- **pytest** (test runner)
- **pytest-html** (HTML reporting)
- **ChromeDriver** (for Google Chrome browser automation)
- **Page Object Model** (for scalable, maintainable test code)

---

## 📝 Getting Started

### Prerequisites

- Python 3.8 or newer
- Google Chrome browser
- [ChromeDriver](https://chromedriver.chromium.org/) (matching your Chrome version)
- (Recommended) Create and activate a virtual environment:
  ```sh
  python -m venv venv
  venv\Scripts\activate
  ```

### Install dependencies

```sh
pip install -r requirements.txt
```

---

## 🧪 Running the Tests

To execute the main test and generate both an HTML report and a log file:

```sh
pytest --html=report.html --self-contained-html --log-file=weather_shopper_automation.log --log-level=INFO
```

- **report.html**: Open in your browser for a detailed test report.
- **weather_shopper_automation.log**: Contains all log output for debugging and audit.

---

## 🛠️ What the Test Does

1. **Opens the Weather Shopper homepage**
2. **Reads the current temperature**
3. **Selects the appropriate product category** (moisturizers if cold, sunscreens if hot)
4. **Finds and adds the cheapest Aloe/Almond or SPF-30/SPF-50 products to the cart**
5. **Validates the cart contents and total price**
6. **Proceeds to payment and fills out the Stripe popup**
7. **Submits payment and verifies success message**

---

## 🧩 Key Implementation Details

- **Page Object Model**: All page interactions are encapsulated in page classes for reusability and clarity.
- **Robust Stripe Handling**: The payment page logic handles Stripe's input masking, field focus, and iframe switching.
- **Dynamic waits**: Uses explicit waits for all asynchronous elements (popups, iframes, etc.).
- **Logging**: All major actions and errors are logged for easy troubleshooting.
- **Reporting**: Generates a self-contained HTML report and a detailed log file for every run.

---

## 📝 Example `.gitignore`

Before pushing to GitHub, you may want to add a `.gitignore` file:

```
venv/
__pycache__/
*.pyc
*.log
report.html
```

---

## 🧪 Test Data

- **Stripe test card**: `4242 4242 4242 4242`
- **Expiry**: Any future date in MMYY format (e.g., `1234`)
- **CVC**: Any 3 digits (e.g., `123`)
- **ZIP**: Any 5 digits (e.g., `12345`)

---

## 🤝 Contributors

This project was developed by:
- **BIZALINE Jalila**
- **ABOUTABIT Salma**
- **IRHAL Haitam**


---

## 📄 License

This project is for educational and demonstration purposes.

---

**Happy Testing!**
