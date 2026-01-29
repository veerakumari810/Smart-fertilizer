import requests
import json

def test_prediction(crop, n, p, k, ph, moisture, season, area):
    url = "http://localhost:8000/predict"
    payload = {
        "Soil_N": n,
        "Soil_P": p,
        "Soil_K": k,
        "Soil_pH": ph,
        "Soil_Moisture": moisture,
        "Crop_Name": crop,
        "Season": season,
        "landArea": area
    }
    
    print(f"\n--- Testing {crop} ---")
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            output = []
            output.append(f"✅ Success!")
            output.append(f"Recommended Fertilizer: {data['Recommended_Fertilizer_Type']}")
            output.append(f"Purpose: {data.get('Fertilizer_Purpose', 'N/A')}")
            output.append(f"Quantity per Acre: {data['Fertilizer_Quantity_kg_per_acre']} kg")
            output.append(f"Irrigation Method: {data.get('Irrigation_Method', 'N/A')}")
            
            # Verify specific logic
            fert_type = data.get('Recommended_Fertilizer_Type', '')
            if crop == 'Rice':
                if 'Urea' in fert_type: output.append("   -> Correctly recommended Urea for Rice")
                else: output.append(f"   -> ⚠️ Warning: Expected Urea for Rice, got {fert_type}")
                
            if crop == 'Wheat':
                if 'DAP' in fert_type: output.append("   -> Correctly recommended DAP for Wheat")
                else: output.append(f"   -> ⚠️ Warning: Expected DAP for Wheat, got {fert_type}")
            
            print("\n".join(output))
            with open("test_results.txt", "a", encoding='utf-8') as f:
                f.write(f"\n--- Testing {crop} ---\n")
                f.write("\n".join(output) + "\n")
                
        else:
            msg = f"❌ Failed: {response.status_code}\n{response.text}"
            print(msg)
            with open("test_results.txt", "a") as f: f.write(msg + "\n")

    except Exception as e:
        msg = f"❌ Error: {str(e)}"
        print(msg)
        with open("test_results.txt", "a") as f: f.write(msg + "\n")

# Clear file
with open("test_results.txt", "w") as f: f.write("API TEST RESULTS\n")

# Test Case 1: Rice (High N needs -> Urea)
test_prediction("Rice", 45, 55, 60, 7.2, 35, "Kharif", 5)

# Test Case 2: Wheat (P needs -> DAP)
test_prediction("Wheat", 45, 55, 60, 6.5, 30, "Rabi", 2)

# Test Case 3: Potato (K needs -> MOP)
test_prediction("Potato", 50, 40, 30, 6.0, 40, "Rabi", 1)
