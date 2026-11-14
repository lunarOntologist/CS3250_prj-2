### US1 --- US6 TESTED! ###
import os
import uuid
from datetime import datetime, timedelta

import pytest

selenium = pytest.importorskip("selenium")
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

BASE_URL = os.getenv("CAMPUS_EATS_URL", "http://localhost:5000")
WAIT_TIMEOUT = 15


def _driver():
    options = FirefoxOptions()
    options.add_argument("-headless")
    options.add_argument("--width=1400")
    options.add_argument("--height=1200")
    return webdriver.Firefox(options=options)


def _register(driver, name, email, password, role):
    driver.get(f"{BASE_URL}/register")
    WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.NAME, "name")))
    driver.find_element(By.NAME, "name").clear()
    driver.find_element(By.NAME, "name").send_keys(name)
    driver.find_element(By.NAME, "email").clear()
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "passwd").clear()
    driver.find_element(By.NAME, "passwd").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, f"input[name='role'][value='{role}']").click()
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Register']").click()


def _login(driver, email, password):
    driver.get(f"{BASE_URL}/login")
    WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.NAME, "email")))
    driver.find_element(By.NAME, "email").clear()
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "passwd").clear()
    driver.find_element(By.NAME, "passwd").send_keys(password)
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']").click()


def _future_listing_window(start_hours=3, end_hours=6):
    now = datetime.now()
    start = now + timedelta(hours=start_hours)
    end = now + timedelta(hours=end_hours)
    return start.strftime("%Y-%m-%dT%H:%M"), end.strftime("%Y-%m-%dT%H:%M")


def _unique_title(prefix):
    return f"{prefix} {uuid.uuid4().hex[:8]}"


def _create_listing(driver, title, description, portions, location, tags=None):
    driver.get(f"{BASE_URL}/listings/new")
    WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.NAME, "title")))
    driver.find_element(By.NAME, "title").clear()
    driver.find_element(By.NAME, "title").send_keys(title)
    driver.find_element(By.NAME, "description").clear()
    driver.find_element(By.NAME, "description").send_keys(description)
    driver.find_element(By.NAME, "portions_total").clear()
    driver.find_element(By.NAME, "portions_total").send_keys(str(portions))
    driver.find_element(By.NAME, "pickup_location").clear()
    driver.find_element(By.NAME, "pickup_location").send_keys(location)
    if tags:
        for tag in tags:
            driver.find_element(By.CSS_SELECTOR, f"input[name='dietary_tags'][value='{tag}']").click()
    start, end = _future_listing_window()
    driver.find_element(By.NAME, "pickup_start").clear()
    driver.find_element(By.NAME, "pickup_start").send_keys(start)
    driver.find_element(By.NAME, "pickup_end").clear()
    driver.find_element(By.NAME, "pickup_end").send_keys(end)
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Post']").click()


def _reserve_listing(driver, title, portions):
    row = driver.find_element(By.XPATH, f"//tr[td[normalize-space(.)='{title}']]")
    Select(row.find_element(By.NAME, "portions")).select_by_value(str(portions))
    row.find_element(By.XPATH, ".//button[normalize-space(.)='Reserve']").click()

### register login and duplicate email ###
def test_us1():
    driver = _driver()
    try:
        email = f"student-{uuid.uuid4().hex[:8]}@campuseats.test"
        _register(driver, "Student One", email, "SuperPass1", "student")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.url_contains("/login"))
        _login(driver, email, "SuperPass1")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.url_contains("/home"))
        assert "Student Home" in driver.page_source

        driver.get(f"{BASE_URL}/register")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.NAME, "name")))
        driver.find_element(By.NAME, "name").send_keys("Duplicate Student")
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "passwd").send_keys("AnotherPass1")
        driver.find_element(By.CSS_SELECTOR, "input[name='role'][value='student']").click()
        driver.find_element(By.XPATH, "//input[@type='submit' and @value='Register']").click()
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "error")))
        assert "That email is already registered" in driver.page_source

        driver.get(f"{BASE_URL}/logout")
        _login(driver, email, "WrongPass")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert "Wrong email or password" in driver.page_source
    finally:
        driver.quit()

### vendor post listing and student access blocked ###
def test_us2():
    driver = _driver()
    try:
        vendor_email = f"vendor-{uuid.uuid4().hex[:8]}@campuseats.test"
        _register(driver, "Vendor One", vendor_email, "VendorPass1", "vendor")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.url_contains("/login"))
        _login(driver, vendor_email, "VendorPass1")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.url_contains("/home"))

        title = _unique_title("Free Pasta Bowl")
        _create_listing(
            driver,
            title=title,
            description="Fresh pasta from the dining hall.",
            portions=5,
            location="Student Center",
            tags=["vegetarian"],
        )
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.url_contains("/home"))
        driver.get(f"{BASE_URL}/vendor/listings")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"), title
        ))
        assert "Student Center" in driver.page_source
        assert "vegetarian" in driver.page_source

        driver.get(f"{BASE_URL}/listings/new")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.NAME, "title")))
        driver.find_element(By.NAME, "title").send_keys("Broken Listing")
        driver.find_element(By.NAME, "description").send_keys("Bad end date")
        driver.find_element(By.NAME, "portions_total").clear()
        driver.find_element(By.NAME, "portions_total").send_keys("2")
        driver.find_element(By.NAME, "pickup_location").send_keys("North Hall")
        start, end = _future_listing_window(start_hours=6, end_hours=7)
        driver.find_element(By.NAME, "pickup_start").clear()
        driver.find_element(By.NAME, "pickup_start").send_keys(end)
        driver.find_element(By.NAME, "pickup_end").clear()
        driver.find_element(By.NAME, "pickup_end").send_keys(start)
        driver.find_element(By.XPATH, "//input[@type='submit' and @value='Post']").click()
        assert "Pickup window end must be after its start" in driver.page_source

        student_email = f"student-{uuid.uuid4().hex[:8]}@campuseats.test"
        _register(driver, "Student Viewer", student_email, "StudentPass1", "student")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.url_contains("/login"))
        _login(driver, student_email, "StudentPass1")
        driver.get(f"{BASE_URL}/listings/new")
        assert "Forbidden" in driver.page_source or "403" in driver.page_source
    finally:
        driver.quit()

### student can browse valid active listings ###
def test_us3():
    driver = _driver()
    try:
        vendor_email = f"vendor-{uuid.uuid4().hex[:8]}@campuseats.test"
        _register(driver, "Vendor Browse", vendor_email, "VendorPass2", "vendor")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.url_contains("/login"))
        _login(driver, vendor_email, "VendorPass2")
        title = _unique_title("Lunch Box")
        _create_listing(driver, title, "A lunch listing", 4, "Library", ["vegan"])

        student_email = f"student-{uuid.uuid4().hex[:8]}@campuseats.test"
        _register(driver, "Student Browse", student_email, "StudentPass2", "student")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.url_contains("/login"))
        _login(driver, student_email, "StudentPass2")
        driver.get(f"{BASE_URL}/listings")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        assert title in driver.page_source
        assert "Available Food" in driver.page_source
        assert "No food listings are currently available." not in driver.page_source
    finally:
        driver.quit()

### student can reserve and reject over booking ###
def test_us4():
    driver = _driver()
    try:
        vendor_email = f"vendor-{uuid.uuid4().hex[:8]}@campuseats.test"
        _register(driver, "Vendor Reserve", vendor_email, "VendorPass3", "vendor")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.url_contains("/login"))
        _login(driver, vendor_email, "VendorPass3")
        title = _unique_title("Single Portion Meal")
        _create_listing(driver, title, "Only two portions available.", 2, "Cafeteria")

        student_email = f"student-{uuid.uuid4().hex[:8]}@campuseats.test"
        _register(driver, "Student Reserve", student_email, "StudentPass3", "student")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.url_contains("/login"))
        _login(driver, student_email, "StudentPass3")
        driver.get(f"{BASE_URL}/listings")
        _reserve_listing(driver, title, 1)
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Reservation successful"))
        assert "pickup code" in driver.page_source.lower()

        driver.get(f"{BASE_URL}/listings")
        _reserve_listing(driver, title, 1)
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "already have an active reservation"))

        driver.get(f"{BASE_URL}/logout")
        other_student_email = f"student-{uuid.uuid4().hex[:8]}@campuseats.test"
        _register(driver, "Other Student", other_student_email, "OtherPass1", "student")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.url_contains("/login"))
        _login(driver, other_student_email, "OtherPass1")
        driver.get(f"{BASE_URL}/listings")
        _reserve_listing(driver, title, 2)
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"), "Not enough portions remaining"
        ))
        assert "Not enough portions remaining" in driver.page_source
    finally:
        driver.quit()

### vendor can manage listings and cancel them ###
def test_us5():
    driver = _driver()
    try:
        vendor_email = f"vendor-{uuid.uuid4().hex[:8]}@campuseats.test"
        _register(driver, "Vendor Manage", vendor_email, "VendorPass4", "vendor")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.url_contains("/login"))
        _login(driver, vendor_email, "VendorPass4")
        title = _unique_title("Manage This Listing")
        _create_listing(driver, title, "Fresh snacks after class.", 3, "Arts Building")

        student_email = f"student-{uuid.uuid4().hex[:8]}@campuseats.test"
        _register(driver, "Student Manage", student_email, "StudentPass4", "student")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.url_contains("/login"))
        _login(driver, student_email, "StudentPass4")
        driver.get(f"{BASE_URL}/listings")
        _reserve_listing(driver, title, 1)
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Reservation successful"))

        driver.get(f"{BASE_URL}/logout")
        _login(driver, vendor_email, "VendorPass4")
        driver.get(f"{BASE_URL}/vendor/listings")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        assert title in driver.page_source
        assert "Active" in driver.page_source
        row = driver.find_element(By.XPATH, f"//tr[td//strong[normalize-space(.)='{title}']]")
        row.find_element(By.LINK_TEXT, "Edit").click()
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.NAME, "title")))
        updated_title = f"{title} Updated"
        driver.find_element(By.NAME, "title").clear()
        driver.find_element(By.NAME, "title").send_keys(updated_title)
        driver.find_element(By.XPATH, "//input[@type='submit' and @value='Post']").click()
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"), updated_title
        ))

        row = driver.find_element(By.XPATH, f"//tr[td//strong[normalize-space(.)='{updated_title}']]")
        row.find_element(By.LINK_TEXT, "Cancel").click()
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Manage Your Listings"))
        row = driver.find_element(By.XPATH, f"//tr[td//strong[normalize-space(.)='{updated_title}']]")
        assert "Cancelled" in row.text
        driver.get(f"{BASE_URL}/listings")
        assert updated_title not in driver.page_source
    finally:
        driver.quit()

### student can cancel reservation and see status update ###
def test_us6():
    driver = _driver()
    try:
        vendor_email = f"vendor-{uuid.uuid4().hex[:8]}@campuseats.test"
        _register(driver, "Vendor Cancel", vendor_email, "VendorPass5", "vendor")
        _login(driver, vendor_email, "VendorPass5")
        title = _unique_title("Canceled Meal")
        _create_listing(driver, title, "Will be canceled soon.", 2, "Library Annex")

        student_email = f"student-{uuid.uuid4().hex[:8]}@campuseats.test"
        _register(driver, "Student Cancel", student_email, "StudentPass5", "student")
        _login(driver, student_email, "StudentPass5")
        driver.get(f"{BASE_URL}/listings")
        _reserve_listing(driver, title, 1)
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Reservation successful"))

        driver.get(f"{BASE_URL}/reservations")
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        assert "Canceled Meal" in driver.page_source
        assert "Active" in driver.page_source
        driver.find_element(By.XPATH, "//button[text()='Cancel']").click()
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "cancelled and the portions were returned"))
        assert "Cancelled" in driver.page_source
    finally:
        driver.quit()
