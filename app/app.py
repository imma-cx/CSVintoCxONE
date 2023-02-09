import os
import sys

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
from scan_management_2 import get_scan_management_number
from graphs.graphs_generator import process_json_data
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/report", methods=['GET'])
def report():
    # Access form data submitted from the frontend
    form_data = request.args

    # Access specific form fields by name
    scan_number = form_data.get('scan_number')

    # Iterate over the form data
    for key, value in form_data.items():
        print(f'{key}: {value}')

    scan_management_number = get_scan_management_number(scan_number)
    scan_data = process_json_data(scan_management_number)
    return render_template('report.html')


if __name__ == "__main__":
    app.run(debug=True)
