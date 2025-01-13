
import time
import json
import sqlite3
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from flask_bootstrap import Bootstrap
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.relative_locator import locate_with
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__, template_folder="C:/Users/atath/live_server/templates")

bootstrap = Bootstrap(app)


EMPLOYEE_DATA_PATH = "C:/Users/atath/live_server/employees.json" 
DATABASE_PATH = "C:/Users/atath/mydatabase.db"


def navigate_to_page(browser, url):
    browser.get(url)


def wait_for_element(browser, by, value, timeout=6):
    try:
        element = WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"Element not found: {value}")
        return None


def initialize_webdriver(driver_path):
    service = Service(driver_path)
    
    options = EdgeOptions()
    options.add_argument('--headless')
    
    browser = webdriver.Edge(service=service, options=options)
    return browser


def get_db_connection():
    connect = sqlite3.connect(DATABASE_PATH)
    connect.row_factory = sqlite3.Row
    return connect


date = datetime.datetime.now()  
local_time = date.strftime("%m/%d/%Y")
time = local_time.replace("/", "-")


def read_data():
    connect = get_db_connection()
    cur =  connect.cursor()
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    connect.close()
    return employees


def update_data(employee_name, employee_role, time_hired, employee_email):
    connect = get_db_connection()
    cur =  connect.cursor()
    cur.execute("""
        INSERT INTO employees (name, position, tenure, email)
        VALUES (?, ?, ?, ?)
    """, (employee_name, employee_role, time_hired, employee_email))
    connect.commit()
    connect.close()
    

@app.route('/', methods=['GET'])
def index():
    employees = read_data()
    employee_count = len(employees)
    
    return render_template("index.html", employees=employees, employee_count=employee_count)


@app.route('/', methods=['GET', 'POST'])
def add_employee():
    
    if request.method == 'POST':
        
        employee_name = request.form['employeeName']
        employee_role = request.form['employeeRole']
        employee_email = request.form['employeeEmail']
        time_hired = time
        
        update_data(employee_name, employee_role, time_hired, employee_email)

        return redirect(url_for('index'))
    return render_template("index.html")

@app.route('/delete', methods=['GET', 'POST'])
def remove_employee():
    
    employee_id = request.form.get('employee_id', None)
    
    if employee_id:
        connect = get_db_connection()
        cur = connect.cursor()
        cur.execute("DELETE FROM employees WHERE email = ?", (employee_id,))
        connect.commit()
        connect.close()
        
        return redirect(url_for('index'))
    return render_template("index.html")


@app.route('/search_employee', methods=['POST'])
def search_employee():
    query = request.form['search_query']
    
    connect = get_db_connection()
    cur = connect.cursor()
    
    cur.execute("""
        SELECT * FROM employees
        WHERE LOWER(name) LIKE ?
    """, (f"%{query.lower()}%",))
    search_results = cur.fetchall()
    connect.close()
    
    return render_template("index.html", employees=search_results, query=query, employee_count=len(search_results))


if __name__ == '__main__':
    app.run(debug=True, port=5050)

#navigate_to_page(browser, url)

#cons = wait_for_element(browser, By.CSS_SELECTOR, '*[data-test="review-text-CONS"]')
#pros = wait_for_element(browser, By.CSS_SELECTOR, '*[data-test="review-text-PROS"]')
