import sys
import ifcopenshell
import pandas as pd

def extract_ifc_data(ifc_file_path: str):
    print(f"[*] Loading OpenBIM IFC file: {ifc_file_path}...")
    try:
        model = ifcopenshell.open(ifc_file_path)
    except Exception as e:
        print(f"[!] Critical Error: Could not open IFC file. Details: {e}")
        sys.exit(1)

    # Extract all physical product elements from the BIM model
    elements = model.by_type("IfcProduct")
    print(f"[*] Total BIM elements detected in model: {len(elements)}")

    data = []
    for elem in elements:
        # Filter out spatial structures (like sites/buildings) to focus on physical assets
        if elem.is_a() in ["IfcSite", "IfcBuilding", "IfcBuildingStorey"]:
            continue
            
        global_id = getattr(elem, "GlobalId", "N/A")
        name = getattr(elem, "Name", "Unnamed")
        element_type = elem.is_a()
        
        data.append({
            "GlobalId": global_id,
            "ElementName": name,
            "ElementType": element_type
        })

    df = pd.DataFrame(data)
    print("\n[*] Sample Extracted BIM Elements DataFrame:")
    print(df.head(10))
    
    # Export to CSV for commercial/quantity surveying analysis
    output_csv = "ifc_extracted_quantities.csv"
    df.to_csv(output_csv, index=False)
    print(f"\n[SUCCESS] Extracted BIM data exported successfully to '{output_csv}'")

if __name__ == "__main__":
    # Fallback message if no IFC file is provided yet
    target_ifc = sys.argv[1] if len(sys.argv) > 1 else None
    if not target_ifc:
        print("[!] Please provide an IFC file path as an argument.")
        print("Example: python ifc_extractor.py sample_model.ifc")
        sys.exit(1)
    extract_ifc_data(target_ifc)
