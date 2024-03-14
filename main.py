# Required imports
import csv               # Import module for reading and writing CSV files
import numpy as np      # Import NumPy library for numerical computations
import matplotlib.pyplot as plt   # Import Matplotlib library for data visualization
from flask import Flask, render_template, request   # Import Flask framework for web application development

# Required imports
import csv
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)

# Function to create CSV file or append data to it
def save_to_csv(animals, food):
    with open("animal_food_data.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        for animal, food_item in zip(animals, food):
            writer.writerow([animal, food_item])

# Function to clear all data in the CSV file
def clear_csv():
    with open("animal_food_data.csv", mode='w', newline='') as file:
        file.truncate(0)  # Clear the file contents

# Function to read data from CSV file
def read_from_csv():
    animals = []
    food = []
    with open("animal_food_data.csv", mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            animals.append(row[0])
            food.append(float(row[1]))
    return animals, food
# Function to plot consumption graph
def plot_consumption():
    """
    Plot food consumption graph.
    """
    animals = []
    food = []
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    for day in days:
        day_animals, day_food = read_from_csv_day(day)
        animals.extend(day_animals)
        food.extend(day_food)

    plt.bar(animals, food)
    plt.xlabel('Animals')
    plt.ylabel('Food Consumption (oz)')
    plt.title('Daily Food Consumption by Animals')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/food_consumption.png')
    plt.close()

# Function to read data for a specific day from CSV file
def read_from_csv_day(day):
    """
    Read data for a specific day from CSV file.
    
    Args:
        day (str): Day of the week.
    
    Returns:
        tuple: Tuple containing lists of animals and food consumption values for the specified day.
    """
    animals = []
    food = []
    with open("animal_food_data.csv", mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0].lower().startswith(day):
                animals.append(row[0])
                food.append(float(row[1]))
    return animals, food

# Route to display form and process data
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Route to display form for data input and process the submitted data.
    """
    if request.method == 'POST':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        for day in days:
            animals = request.form.getlist(f'{day}_animals[]')
            food = request.form.getlist(f'{day}_food[]')
            animals = [animal.capitalize() for animal in animals]
            food = [float(f) for f in food]
            save_to_csv([f"{day}_{animal}" for animal in animals], food)

        plot_consumption()

        return render_template('result.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
