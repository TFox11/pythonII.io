# Required imports
import csv
from flask import Flask, render_template, request, send_from_directory

# Initialize Flask app
app = Flask(__name__, static_url_path='')

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

# Function to plot consumption graph (this function is incomplete and needs implementation)
def plot_consumption():
    # Your plotting code here...
    pass

# Route to serve index.html
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Process form data
        animals = request.form.getlist('animals')
        food = request.form.getlist('food')
        save_to_csv(animals, food)
        plot_consumption()  # Plot consumption graph
        return render_template('result.html')
    else:
        return render_template('index.html')

# Route to clear all data
@app.route('/clear', methods=['POST'])
def clear():
    clear_csv()
    return 'Data cleared successfully'

# Route to serve static files
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('', path)

if __name__ == '__main__':
    app.run(debug=True)
