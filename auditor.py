import csv

def export_quantities_to_csv(elements_data, output_filename="quantity_report.csv"):
    """Exports parsed IFC spatial and quantity data to a clean CSV report."""
    fields = ["GlobalId", "Name", "ObjectType", "QuantityName", "Value"]
    
    with open(output_filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for item in elements_data:
            writer.writerow(item)
            
    print(f"[*] Quantity audit report successfully exported to '{output_filename}'")
