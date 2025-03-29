from flask import Flask, render_template, request, jsonify
from sheet_calculator import select_best_sheet, calculate_costs
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of available sheet sizes
SHEETS = [
    (15, 20), (14, 22), (18, 23), (12, 23), (11.5, 18),
    (18, 25), (12.5, 18), (19, 26), (13, 19), (13.5, 15)
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            L_p = float(request.form['length'])
            B_p = float(request.form['breadth'])

            # Validate inputs
            if L_p <= 0 or B_p <= 0:
                return render_template('index.html', error='Dimensions must be positive numbers.')

            # Calculate best sheet
            best_sheet, max_pieces, min_waste, all_results = select_best_sheet(SHEETS, L_p, B_p)
            
            if best_sheet:
                return render_template('index.html', 
                                     result={
                                         'best_sheet': best_sheet,
                                         'max_pieces': max_pieces,
                                         'min_waste': round(min_waste, 2),
                                         'all_results': all_results
                                     },
                                     input_values={'length': L_p, 'breadth': B_p})
            else:
                return render_template('index.html', error='No suitable sheet size found.')
        except ValueError as e:
            logger.error(f"Invalid input: {str(e)}")
            return render_template('index.html', error='Please enter valid numbers.')
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return render_template('index.html', error='An unexpected error occurred')
    return render_template('index.html')

@app.route('/calculate_costs', methods=['POST'])
def calculate_costs_route():
    try:
        quantity = int(request.form['quantity'])
        product_name = request.form['product_name']
        product_type = request.form['product_type']
        length_product = float(request.form['length_product'])
        breadth_product = float(request.form['breadth_product'])
        length_sheet = float(request.form['length_sheet'])
        breadth_sheet = float(request.form['breadth_sheet'])
        pieces_in_one_sheet = int(request.form['pieces_in_one_sheet'])
        gsm = int(request.form['gsm'])
        paper_type = request.form['paper_type']
        paper_price = float(request.form['paper_price'])
        pasting_option = request.form['pasting_option']
        no_of_plates = int(request.form['no_of_plates'])
        cost_of_printing = float(request.form['cost_of_printing'])
        cost_of_lamination = float(request.form['cost_of_lamination'])
        cost_of_cutting = float(request.form['cost_of_cutting'])
        cost_of_uv = float(request.form['cost_of_uv'])
        cost_of_dye = float(request.form['cost_of_dye'])
        cost_of_leaf = float(request.form['cost_of_leaf'])

        # Calculate costs
        costs = calculate_costs(quantity, product_name, product_type, length_product, breadth_product,
                                length_sheet, breadth_sheet, pieces_in_one_sheet, gsm, paper_type,
                                paper_price, pasting_option, no_of_plates, cost_of_printing, cost_of_lamination,
                                cost_of_cutting, cost_of_uv, cost_of_dye, cost_of_leaf)

        return render_template('index.html', costs=costs)
    except Exception as e:
        logger.error(f"Error calculating costs: {str(e)}")
        return render_template('index.html', error='An error occurred while calculating costs.')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
