# -*- coding: utf-8 -*-
"""Milk Sales.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13D3JeImD8HMIRWqNmsVLv35b4U8jnn8-

Create an interactive python code, that essentially functions as an interactive chatbot, to use milks sales to determine ordering and stocking suggestions.
"""

import sqlite3

# Create or connect to the database
conn = sqlite3.connect('milk_stats.db')
cursor = conn.cursor()

# Create the milk_sales table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS milk_sales (
        ID INTEGER PRIMARY KEY,
        Type TEXT,
        Size TEXT,
        Sales INTEGER,
        Available INTEGER,
        Next_Delivery INTEGER
    )
''')
conn.commit()

def display_menu():
    print("Milk Orderbot Menu:")
    print("1. Enter Milk Sales")
    print("2. View Milk Sales Data")
    print("3. Exit")

def enter_milk_sales():
    milk_type = input("Select Milk Type (whole, 2%, 1%, Skim, Chocolate): ").strip()
    size = input("Select Size (gallon, half-gallon, quart, pint): ").strip()
    sales = int(input("Enter Weekly Sales Total: "))
    available = int(input("Enter Quantity Available: "))
    next_delivery = int(input("Enter Days Before Next Delivery: "))

    cursor.execute('''
        INSERT INTO milk_sales (Type, Size, Sales, Available, Next_Delivery)
        VALUES (?, ?, ?, ?, ?)
    ''', (milk_type, size, sales, available, next_delivery))
    conn.commit()

def view_milk_sales_data():
    cursor.execute('''
        SELECT Type, Size, Sales, Available, Next_Delivery,
               ROUND(Sales / Next_Delivery, 2) AS Avg_Daily
        FROM milk_sales
    ''')
    data = cursor.fetchall()

    print("\nMilk Sales Data:")
    print("{:<10} {:<10} {:<10} {:<15} {:<15} {:<10}".format(
        "Type", "Size", "Sales", "Available", "Next Delivery", "Avg Daily"))
    for row in data:
        print("{:<10} {:<10} {:<10} {:<15} {:<15} {:<10}".format(*row))
    print()

while True:
    display_menu()
    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == '1':
        enter_milk_sales()
        view_milk_sales_data()
    elif choice == '2':
        view_milk_sales_data()
    elif choice == '3':
        print("Goodbye!")
        conn.close()
        break
    else:
        print("Invalid choice. Please select a valid option.")

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_milk_order', methods=['POST'])
def process_milk_order():
    # Get data from the HTTP request
    data = request.get_json()

    # Retrieve user inputs
    milk_type = data['milkType']
    milk_size = data['milkSize']
    weekly_sales = int(data['weeklySales'])
    quantity_available = int(data['quantityAvailable'])
    days_to_delivery = int(data['daysToDelivery'])

    # Perform calculations and logic here
    # For simplicity, let's just echo back the input data
    result = {
        'milkType': milk_type,
        'milkSize': milk_size,
        'weeklySales': weekly_sales,
        'quantityAvailable': quantity_available,
        'daysToDelivery': days_to_delivery
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)