def calculate_costs(quantity, product_name, product_type, length_product, breadth_product,
                    length_sheet, breadth_sheet, pieces_in_one_sheet, gsm, paper_type,
                    paper_price, pasting_option, no_of_plates, cost_of_printing, cost_of_lamination,
                    cost_of_cutting, cost_of_uv, cost_of_dye, cost_of_leaf):
   
    # Calculating Sheets to be Used
    sheets_to_be_used = quantity / pieces_in_one_sheet
   
    # Calculating Gms.
    gms = (((length_sheet * breadth_sheet * gsm) / 3100) / 500) * 100
   
    # Calculating Amount per Sheet
    amount_per_sheet = (gms * paper_price) / 100
   
    # Calculating Cost of Paper before Pasting
    cost_of_paper_before_pasting = amount_per_sheet * sheets_to_be_used
   
    # Calculating Pasting Cost
    pasting = cost_of_paper_before_pasting if pasting_option.upper() == 'Y' else 0
   
    # Calculating Cost of Paper after Pasting
    cost_of_paper_after_pasting = cost_of_paper_before_pasting + pasting
   
    # Calculating Cost of Plates
    cost_of_plates = no_of_plates * 250
   
    # Fixed Cost of Designing
    cost_of_designing = 1000
   
    # Calculating Cost of Pasting
    cost_of_pasting = sheets_to_be_used if pasting_option.upper() == 'Y' else 0
   
    # Calculating Total Cost
    total_cost = (cost_of_paper_after_pasting + cost_of_plates + cost_of_printing + cost_of_lamination +
                  cost_of_cutting + cost_of_uv + cost_of_pasting + cost_of_designing + cost_of_dye + cost_of_leaf)
   
    # Calculating Cost per Piece
    cost_per_piece = total_cost / quantity
   
    # Return all calculated values
    return {
        'Sheets to be Used': round(sheets_to_be_used, 2),
        'Gms': round(gms, 2),
        'Amount per Sheet': round(amount_per_sheet, 2),
        'Cost of Paper before Pasting': round(cost_of_paper_before_pasting, 2),
        'Pasting Cost': round(pasting, 2),
        'Cost of Paper after Pasting': round(cost_of_paper_after_pasting, 2),
        'Cost of Plates': round(cost_of_plates, 2),
        'Cost of Designing': round(cost_of_designing, 2),
        'Cost of Printing': round(cost_of_printing, 2),
        'Cost of Lamination': round(cost_of_lamination, 2),
        'Cost of Cutting': round(cost_of_cutting, 2),
        'Cost of UV': round(cost_of_uv, 2),
        'Cost of Dye': round(cost_of_dye, 2),
        'Cost of Leaf': round(cost_of_leaf, 2),
        'Total Cost': round(total_cost, 2),
        'Cost per Piece': round(cost_per_piece, 2)
    }

def select_best_sheet(sheets, length_product, breadth_product):
    """
    Select the best sheet size that minimizes waste.
    Returns: (best_sheet, max_pieces, min_waste, all_results)
    """
    best_sheet = None
    max_pieces = 0
    min_waste = float('inf')
    all_results = []
    
    for sheet in sheets:
        length_sheet, breadth_sheet = sheet
        
        # Try normal orientation
        pieces_normal = (length_sheet // length_product) * (breadth_sheet // breadth_product)
        waste_normal = (length_sheet * breadth_sheet) - (pieces_normal * length_product * breadth_product)
        
        # Try rotated orientation
        pieces_rotated = (length_sheet // breadth_product) * (breadth_sheet // length_product)
        waste_rotated = (length_sheet * breadth_sheet) - (pieces_rotated * length_product * breadth_product)
        
        # Select better orientation
        if pieces_normal >= pieces_rotated:
            pieces = pieces_normal
            waste = waste_normal
        else:
            pieces = pieces_rotated
            waste = waste_rotated
            
        all_results.append({
            'sheet': sheet,
            'pieces': int(pieces),
            'waste': round(waste, 2)
        })
            
        # Update best if this sheet gives more pieces or same pieces with less waste
        if pieces > max_pieces or (pieces == max_pieces and waste < min_waste):
            best_sheet = sheet
            max_pieces = pieces
            min_waste = waste
            
    return best_sheet, int(max_pieces), min_waste, sorted(all_results, key=lambda x: (-x['pieces'], x['waste']))