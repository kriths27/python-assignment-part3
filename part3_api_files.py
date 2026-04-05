"""
Product Explorer & Error-Resilient Logger
-----------------------------------------
This script demonstrates:
1. File read/write basics
2. API integration with DummyJSON
3. Exception handling (calculator, file reader, API calls)
4. Logging errors to a file

Written in a human style with comments and clear structure.
"""

import requests
from datetime import datetime

# -------------------------------
# Task 1 — File Read & Write Basics
# -------------------------------

def write_notes():
    """Write and append notes to python_notes.txt"""
    notes = [
        "Topic 1: Variables store data. Python is dynamically typed.",
        "Topic 2: Lists are ordered and mutable.",
        "Topic 3: Dictionaries store key-value pairs.",
        "Topic 4: Loops automate repetitive tasks.",
        "Topic 5: Exception handling prevents crashes."
    ]
    try:
        with open("python_notes.txt", "w", encoding="utf-8") as f:
            for line in notes:
                f.write(line + "\n")
        print("File written successfully.")

        extra = [
            "Topic 6: Functions promote code reuse.",
            "Topic 7: Classes enable object-oriented programming."
        ]
        with open("python_notes.txt", "a", encoding="utf-8") as f:
            for line in extra:
                f.write(line + "\n")
        print("Lines appended.")
    except Exception as e:
        print("Error writing notes:", e)


def read_notes():
    """Read notes back, number them, count lines, and search by keyword"""
    try:
        with open("python_notes.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        for i, line in enumerate(lines, start=1):
            print(f"{i}. {line.strip()}")
        print(f"Total lines: {len(lines)}")

        keyword = input("Enter a keyword to search: ").strip().lower()
        matches = [line.strip() for line in lines if keyword in line.lower()]
        if matches:
            print("Matching lines:")
            for m in matches:
                print(m)
        else:
            print("No lines found with that keyword.")
    except FileNotFoundError:
        print("File not found.")


# -------------------------------
# Task 2 — API Integration
# -------------------------------

BASE_URL = "https://dummyjson.com/products"

def fetch_products():
    """Fetch 20 products and display them in a table"""
    try:
        resp = requests.get(f"{BASE_URL}?limit=20", timeout=5)
        resp.raise_for_status()
        data = resp.json()["products"]
        print("\n--- Product Table ---")
        print("ID  | Title                          | Category      | Price    | Rating")
        print("----|--------------------------------|---------------|----------|-------")
        for p in data:
            print(f"{p['id']:<4}| {p['title']:<30}| {p['category']:<13}| ${p['price']:<8}| {p['rating']}")
        return data
    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
    except Exception as e:
        print("Error:", e)


def filter_and_sort(products):
    """Filter products with rating ≥ 4.5 and sort by price descending"""
    filtered = [p for p in products if p["rating"] >= 4.5]
    sorted_list = sorted(filtered, key=lambda x: x["price"], reverse=True)
    print("\n--- Filtered & Sorted Products (rating ≥ 4.5) ---")
    for p in sorted_list:
        print(f"{p['title']} - ${p['price']} - Rating {p['rating']}")


def fetch_laptops():
    """Fetch laptops category"""
    try:
        resp = requests.get(f"{BASE_URL}/category/laptops", timeout=5)
        resp.raise_for_status()
        print("\n--- Laptops ---")
        for p in resp.json()["products"]:
            print(f"{p['title']} - ${p['price']}")
    except Exception as e:
        print("Error:", e)


def post_product():
    """Simulate adding a product via POST"""
    payload = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API"
    }
    try:
        resp = requests.post(f"{BASE_URL}/add", json=payload, timeout=5)
        print("\n--- POST Response ---")
        print(resp.json())
    except Exception as e:
        print("Error:", e)


# -------------------------------
# Task 3 — Exception Handling
# -------------------------------

def safe_divide(a, b):
    """Safe division with error handling"""
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"


def read_file_safe(filename):
    """Safe file reader with finally block"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        print("File operation attempt complete.")


def lookup_product_loop():
    """Interactive product lookup loop with validation"""
    while True:
        user_input = input("Enter a product ID to look up (1–100), or 'quit' to exit: ").strip()
        if user_input.lower() == "quit":
            break
        if not user_input.isdigit() or not (1 <= int(user_input) <= 100):
            print("Invalid input. Please enter a number between 1 and 100.")
            continue
        pid = int(user_input)
        try:
            resp = requests.get(f"{BASE_URL}/{pid}", timeout=5)
            if resp.status_code == 404:
                print("Product not found.")
            elif resp.status_code == 200:
                p = resp.json()
                print(f"{p['title']} - ${p['price']}")
            else:
                print("Unexpected response:", resp.status_code)
        except Exception as e:
            print("Error:", e)


# -------------------------------
# Task 4 — Logging to File
# -------------------------------

def log_error(context, error_type, message):
    """Log errors to error_log.txt with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("error_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] ERROR in {context}: {error_type} — {message}\n")


def trigger_logs():
    """Trigger sample logs for ConnectionError and HTTPError"""
    # ConnectionError
    try:
        requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
    except requests.exceptions.ConnectionError:
        log_error("fetch_products", "ConnectionError", "No connection could be made")

    # HTTP 404
    resp = requests.get(f"{BASE_URL}/999", timeout=5)
    if resp.status_code != 200:
        log_error("lookup_product", "HTTPError", f"{resp.status_code} Not Found for product ID 999")

    # Show log contents
    with open("error_log.txt", "r", encoding="utf-8") as f:
        print("\n--- Error Log Contents ---")
        print(f.read())


# -------------------------------
# Run All Tasks
# -------------------------------

if __name__ == "__main__":
    # Task 1
    write_notes()
    read_notes()

    # Task 2
    products = fetch_products()
    if products:
        filter_and_sort(products)
    fetch_laptops()
    post_product()

    # Task 3
    print("\n--- Safe Divide Tests ---")
    print(safe_divide(10, 2))
    print(safe_divide(10, 0))
    print(safe_divide("ten", 2))

    print("\n--- File Reader Tests ---")
    print(read_file_safe("python_notes.txt"))
    print(read_file_safe("ghost_file.txt"))

    # Uncomment to run interactive loop
    # lookup_product_loop()

    # Task 4
    trigger_logs()
