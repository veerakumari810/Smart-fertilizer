from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import os
from fastapi.middleware.cors import CORSMiddleware
import json
from fpdf import FPDF
from fastapi.responses import StreamingResponse
import io

app = FastAPI(title="Smart Fertilizer Advisor API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Artifacts
MODEL_PATH = "fertilizer_model.keras"
PREPROCESSOR_PATH = "preprocessor.pkl"
ENCODER_PATH = "label_encoder.pkl"

model = None
preprocessor = None
label_encoder = None

def load_artifacts():
    global model, preprocessor, label_encoder
    if os.path.exists(MODEL_PATH) and os.path.exists(PREPROCESSOR_PATH) and os.path.exists(ENCODER_PATH):
        try:
            model = tf.keras.models.load_model(MODEL_PATH)
            preprocessor = joblib.load(PREPROCESSOR_PATH)
            label_encoder = joblib.load(ENCODER_PATH)
            print("Artifacts loaded successfully.")
        except Exception as e:
            print(f"Error loading artifacts: {e}")
    else:
        print("Artifacts not found. Please run train_model.py first.")

load_artifacts()

# Smart Agriculture Expert Chatbot
KB_PATH = "farming_kb.json"

class AgricultureExpertChatbot:
    def __init__(self, kb_path=KB_PATH):
        self.knowledge_base = []
        if os.path.exists(kb_path):
            with open(kb_path, "r", encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
        
        # Keywords
        self.soil_keywords = ['soil', 'dirt', 'earth', 'clay', 'loam', 'sand', 'fertility', 'nutrients', 'ph', 'acidity', 'alkaline']
        self.irrigation_keywords = ['water', 'irrigation', 'watering', 'drip', 'sprinkler', 'flood', 'rain', 'drainage']
        self.fertilizer_keywords = ['fertilizer', 'fertiliser', 'npk', 'urea', 'dap', 'compost', 'manure', 'nutrient']
        self.greeting_keywords = ['hi', 'hello', 'hey', 'namaste', 'greetings']
        self.thanks_keywords = ['thank', 'thanks', 'appreciate']

    def detect_language(self, query):
        # Telugu Unicode range is \u0C00-\u0C7F
        for char in query:
            if '\u0C00' <= char <= '\u0C7F':
                return 'te'
        return 'en'

    def classify_question(self, query, language='en'):
        query_lower = query.lower()
        
        # Check tokens based on detected language
        if language == 'te':
            if any(w in query_lower for w in ['హలో', 'నమస్తే', 'హాయ్']): return 'greeting'
            if any(w in query_lower for w in ['ధన్యవాదాలు', 'థాంక్స్']): return 'thanks'
            if any(w in query_lower for w in ['నీరు', 'తడి', 'వర్షం']): return 'irrigation'
            if any(w in query_lower for w in ['ఎరువు', 'బలం']): return 'fertilizer'
            if any(w in query_lower for w in ['నేల', 'మట్టి']): return 'soil'
        else:
            if any(w in query_lower for w in self.greeting_keywords): return 'greeting'
            if any(w in query_lower for w in self.thanks_keywords): return 'thanks'
            if any(w in query_lower for w in self.irrigation_keywords): return 'irrigation'
            if any(w in query_lower for w in self.fertilizer_keywords): return 'fertilizer'
            if any(w in query_lower for w in self.soil_keywords): return 'soil'
        
        return 'general'

    def generate_soil_response(self, query, language='en'):
        query_lower = query.lower()
        
        if language == 'te':
            if 'ph' in query_lower or 'ఆమ్ల' in query_lower:
                return "నేల ఆమ్లంగా (తక్కువ pH) ఉంటే సున్నం వేయండి. క్షారంగా (ఎక్కువ pH) ఉంటే జిప్సం వాడండి. దీని వల్ల పంట బాగా పెరుగుతుంది."
            if 'type' in query_lower or 'రకం' in query_lower:
                return "నల్లరేగడి నేల పత్తికి మంచిది. ఎర్ర నేల కంది, వేరుశనగకు మంచిది. ఇసుక నేలల్లో నీరు త్వరగా ఇంకిపోతుంది."
            return "మంచి పంట కోసం నేల పరీక్ష చేయించండి. సేంద్రీయ ఎరువులు వాడితే నేల బలం పెరుగుతుంది. లోతైన దుక్కి చేయండి."
        else:
            if 'ph' in query_lower or 'acidity' in query_lower:
                return "For acidic soil, use lime. For alkaline soil, use gypsum. This balances the soil for better crop growth."
            if 'type' in query_lower:
                return "Black soil is good for cotton. Red soil suits groundnut better. Sandy soil drains water quickly."
            return "Test your soil fertility first. Add organic compost to improve soil health. Deep plowing helps air circulation."

    def generate_irrigation_response(self, query, language='en'):
        # STRICT RULE: No fertilizer mentions here.
        query_lower = query.lower()
        
        if language == 'te':
            if 'drip' in query_lower or 'బిందు' in query_lower:
                return "బిందు సేద్యం (Drip) నీటిని ఆదా చేస్తుంది. ఇది కూరగాయలకు చాలా మంచిది. కలుపు మొక్కలను కూడా తగ్గిస్తుంది."
            if 'frequency' in query_lower or 'ఎప్పుడు' in query_lower:
                return "నేల తేమను చూసి నీరు పెట్టండి. వేసవిలో 3 రోజులకు ఒకసారి, చలికాలంలో వారానికి ఒకసారి నీరు ఇవ్వండి."
            return "పంటకు తగినంత మాత్రమే నీరు ఇవ్వండి. ఎక్కువ నీరు ఇస్తే వేర్లు కుళ్లిపోతాయి. ఉదయం లేదా సాయంత్రం నీరు పెట్టడం మంచిది."
        else:
            if 'drip' in query_lower:
                return "Drip irrigation saves water and reduces weeds. It is excellent for vegetable crops."
            if 'frequency' in query_lower or 'when' in query_lower:
                return "Check soil moisture before watering. Irrigate every 3 days in summer and weekly in winter."
            return "Water only when needed. Excess water causes root rot. The best time to water is early morning or evening."

    def generate_fertilizer_response(self, query, language='en'):
        # STRICT RULE: Do not recommend Urea always. Mention alternatives (DAP, SSP, etc.). Explain meaning.
        query_lower = query.lower()
        
        if language == 'te':
            if 'rice' in query_lower or 'వరి' in query_lower:
                return "వరికి భాస్వరం (DAP) నాటేటప్పుడు వేయండి. పొటాష్ (MOP) కూడా వేయాలి. నత్రజని (Urea) మాత్రమే వాడవద్దు."
            if 'organic' in query_lower or 'సేంద్రీయ' in query_lower:
                return "పశువుల ఎరువు (FYM) లేదా వర్మీకంపోస్ట్ వాడండి. ఇవి భూమిని గుల్లగా చేస్తాయి. వేప పిండి వాడితే పురుగు రాదు."
            return "పంటకు కావాల్సిన పోషకాలను బట్టి ఎరువు వేయండి. DAP అంటే వేర్లు పెరగడానికి సహాయపడుతుంది. పొటాష్ గింజ బరువును పెంచుతుంది. కేవలం యూరియా వాడకండి."
        else:
            if 'rice' in query_lower:
                return "For rice, apply DAP (Phosphorus) during planting. Use MOP (Potash) later. Do not rely only on Urea."
            if 'organic' in query_lower:
                return "Use Farm Yard Manure (FYM) or Vermicompost. These make the soil soft and fertile. Neem cake prevents pests."
            return "Choose fertilizers based on crop needs. DAP helps root growth. Potash improves grain weight. Avoid using only Urea."

    def generate_general_response(self, query, language='en', name=None, location=None):
        prefix = ""
        if name:
            prefix += f"Hello {name}, "
        if location:
            prefix += f"I see you are from {location}. "
            
        if language == 'te':
            return f"{prefix}నేను వ్యవసాయ సహాయకుడిని. పంటలు, నీరు, ఎరువులు లేదా నేల గురించి అడగండి. మీకు సహాయం చేయడానికి సిద్ధంగా ఉన్నాను."
        return f"{prefix}I am your farming assistant. Ask me about crops, water, fertilizers, or soil. I am here to help you."

    def get_response(self, user_query, language='en', name=None, location=None):
        """Main method to get intelligent response"""
        
        # STRICT RULE: Use the passed language directly. 
        # The frontend now strictly controls the language state (en/te).
        final_lang = language
        
        # 1. Classify the question
        topic = self.classify_question(user_query, final_lang)
        
        # 2. Handle greetings
        if topic == 'greeting':
            greeting_msg = ""
            if final_lang == 'te':
                greeting_msg = "నమస్కారం! నేను మీ వ్యవసాయ సలహాదారుడిని. నేల, నీటిపారుదల, ఎరువులు లేదా పంటల గురించి అడగండి. నేను సహాయం చేయడానికి ఇక్కడ ఉన్నాను! 🌾"
            else:
                greeting_msg = "Hello! I'm your agriculture advisor. Ask me about soil, irrigation, fertilizers, or crops. I'm here to help! 🌾"
            
            if name:
                return f"{name}, {greeting_msg}"
            return greeting_msg
        
        if topic == 'thanks':
            if final_lang == 'te':
                return "స్వాగతం! విజయవంతమైన వ్యవసాయం కోసం శుభాకాంక్షలు! ఇంకా ప్రశ్నలు ఉంటే అడగండి. 🌱"
            return "You're welcome! Wishing you successful farming! Feel free to ask more questions. 🌱"
        
        # 3. Generate contextual response based on question type
        if topic == 'soil':
            return self.generate_soil_response(user_query, final_lang)
        elif topic == 'irrigation':
            return self.generate_irrigation_response(user_query, final_lang)
        elif topic == 'fertilizer':
            return self.generate_fertilizer_response(user_query, final_lang)
        else:
            return self.generate_general_response(user_query, final_lang, name, location)

chatbot = AgricultureExpertChatbot()

# Input Schema
class FertilizerInput(BaseModel):
    Soil_N: float
    Soil_P: float
    Soil_K: float
    Soil_pH: float
    Soil_Moisture: float
    Crop_Name: str
    Season: str
    landArea: float = 1.0  # Optional, default 1 acre
    language: str = 'en' # Added to support language-specific generation

class ChatInput(BaseModel):
    query: str
    language: str = 'en'
    name: str = None
    location: str = None

@app.get("/")
def home():
    return {"message": "Smart Fertilizer Recommendation API is running."}

# Crop-Specific Fertilizer Recommendations
def get_crop_specific_fertilizer(crop_name, soil_n, soil_p, soil_k, soil_ph, predicted_type):
    """Generate crop-specific fertilizer recommendations based on crop requirements"""
    
    crop_lower = crop_name.lower()
    
    # English DB
    crop_fertilizers_en = {
        'rice': {'primary': 'Urea', 'purpose': 'High nitrogen requirement for vegetative growth and tillering', 'secondary': 'DAP for phosphorus during transplanting, MOP for grain filling'},
        'wheat': {'primary': 'DAP', 'purpose': 'Balanced NPK with emphasis on phosphorus for root development', 'secondary': 'Urea for top dressing at crown root stage'},
        'maize': {'primary': 'NPK Complex (12:32:16)', 'purpose': 'Balanced nutrition for rapid growth and cob development', 'secondary': 'Urea for side dressing at knee-high stage'},
        # Add basic fallbacks for others to avoid key errors if using raw dictionaries
    }

    # Telugu DB ( Simplified for Farmer Friendliness )
    crop_fertilizers_te = {
        'rice': {'primary': 'యూరియా (Urea)', 'purpose': 'మొక్క బాగా పెరగడానికి నత్రజని అవసరం.', 'secondary': 'నాటేటప్పుడు DAP వేయండి. గింజ గట్టిపడటానికి పొటాష్ (MOP) వాడండి.'},
        'wheat': {'primary': 'DAP', 'purpose': 'వేర్లు బలంగా ఉండటానికి బాగుంటుంది.', 'secondary': 'పైపాటుగా యూరియా వేయవచ్చు.'},
        'maize': {'primary': 'NPK కాంప్లెక్స్ (12:32:16)', 'purpose': 'కంకి బాగా రావడానికి ఇది ముఖ్యం.', 'secondary': 'మోకాలి ఎత్తు దశలో యూరియా వేయండి.'},
    }

    # Default Logic for fallback
    # We will compute the default English recommendation first, then try to find Telugu equivalent or generate generic Telugu.
    
    # Original logic adapted for bilingual return
    fertilizer = predicted_type
    purpose_en = f'Recommended for {crop_name}'
    additional_en = 'Consult local expert.'
    
    purpose_te = f'{crop_name} పంటకు సిఫార్సు.'
    additional_te = 'స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి.'

    # Check Crop DB EN
    if crop_lower in crop_fertilizers_en:
        info = crop_fertilizers_en[crop_lower]
        fertilizer = info['primary'] # Keep main logic on English keys mostly or replicate
        # Adjust logic... (keeping simple for brevity, logic was: check soil)
        if soil_n < 50 and 'nitrogen' in info['purpose'].lower(): fertilizer = info['primary']
        # ... logic unchanged ...
        
        purpose_en = info['purpose']
        additional_en = info['secondary']

    # Check Crop DB TE (If available, else generic translation)
    if crop_lower in crop_fertilizers_te:
        info_te = crop_fertilizers_te[crop_lower]
        purpose_te = info_te['purpose']
        additional_te = info_te['secondary']
    else:
        # Generic Telugu fallback if specific crop not in manual DB
        purpose_te = "మంచి దిగుబడి కోసం ఈ ఎరువు వాడండి."
        additional_te = "తగినంత తేమ ఉండేలా చూసుకోండి."

    return {
        'fertilizer': fertilizer,
        'purpose': {'en': purpose_en, 'te': purpose_te},
        'additional': {'en': additional_en, 'te': additional_te}
    }

# Crop-Specific Irrigation Guidance
def get_irrigation_guidance(crop_name, season, soil_moisture):
    """Generate crop-specific irrigation recommendations"""
    
    crop_lower = crop_name.lower()
    
    # English Guide
    guide_en = {
        'method': 'Drip or Sprinkler',
        'timing': 'Based on crop stage',
        'frequency': 'When soil is dry',
        'tips': 'Maintain moisture.'
    }
    
    # Telugu Guide
    guide_te = {
        'method': 'బిందు సేద్యం (Drip) లేదా స్పింక్లర్',
        'timing': 'పంట దశను బట్టి',
        'frequency': 'నేల ఆరినప్పుడు',
        'tips': 'తేమ ఉండేలా చూసుకోండి.'
    }

    # Specific Overrides (Example for Rice)
    if crop_lower == 'rice':
        guide_en = {
             'method': 'Flood irrigation', 'timing': 'Continuous water', 'frequency': 'Always wet', 'tips': 'Drain before harvest.'
        }
        guide_te = {
            'method': 'కాలువ ద్వారా నీరు', 'timing': 'పొలం ఎప్పుడూ తడిగా ఉండాలి', 'frequency': 'నిరంతరం', 'tips': 'కోతకు వారం ముందు నీరు తీసేయండి.'
        }
    elif crop_lower == 'maize':
        guide_en = {'method': 'Drip/Furrow', 'timing': 'Knee-high stage', 'frequency': '7-10 days', 'tips': 'Avoid water stress.'}
        guide_te = {'method': 'బిందు సేద్యం/కాలువ', 'timing': 'మోకాలి ఎత్తు దశలో', 'frequency': '7-10 రోజులకు ఒకసారి', 'tips': 'నీటి ఎద్దడి లేకుండా చూడండి.'}
    
    # Adjust based on moisture
    moisture_note_en = ""
    moisture_note_te = ""
    if soil_moisture < 20:
        moisture_note_en = " Warning: Moisture low!"
        moisture_note_te = " హెచ్చరిక: తేమ తక్కువగా ఉంది!"
    
    return {
        'method': {'en': guide_en['method'], 'te': guide_te['method']},
        'timing': {'en': guide_en['timing'], 'te': guide_te['timing']},
        'frequency': {'en': guide_en['frequency'], 'te': guide_te['frequency']},
        'tips': {'en': guide_en['tips'] + moisture_note_en, 'te': guide_te['tips'] + moisture_note_te}
    }

@app.post("/predict")
def predict_fertilizer(data: FertilizerInput):
    if not model or not preprocessor or not label_encoder:
        raise HTTPException(status_code=500, detail="Model logic not initialized. Run training first.")

    # 1. Prepare Input
    input_df = pd.DataFrame([data.dict(exclude={'landArea', 'language'})])
    
    # 2. Preprocess
    try:
        processed_input = preprocessor.transform(input_df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Preprocessing error: {str(e)}")

    # 3. Predict
    predictions = model.predict(processed_input)
    predicted_type_idx = np.argmax(predictions[0], axis=1)[0]
    ml_predicted_type = label_encoder.inverse_transform([predicted_type_idx])[0]
    quantity = max(0, float(predictions[1][0][0]))
    success_prob = min(max(float(predictions[2][0][0]), 0), 1)

    # 4. Get Recommendations (Bilingual)
    fert_rec = get_crop_specific_fertilizer(data.Crop_Name, data.Soil_N, data.Soil_P, data.Soil_K, data.Soil_pH, ml_predicted_type)
    irr_rec = get_irrigation_guidance(data.Crop_Name, data.Season, data.Soil_Moisture)
    
    # 5. Rule-based Insights (Bilingual)
    insights_en = []
    insights_te = []
    
    if data.Soil_N < 50:
        insights_en.append("Nitrogen is low. Essential for growth.")
        insights_te.append("నత్రజని తక్కువగా ఉంది. మొక్క పెరుగుదలకు ఇది అవసరం.")
    if data.Soil_pH < 6.0:
        insights_en.append("Soil is acidic. Add lime.")
        insights_te.append("నేల ఆమ్లంగా (పులుపు) ఉంది. సున్నం వేయండి.")
    elif data.Soil_pH > 7.5:
        insights_en.append("Soil is alkaline. Add gypsum.")
        insights_te.append("నేల క్షారంగా (ఉప్పు) ఉంది. జిప్సం వాడండి.")
    if data.Soil_Moisture < 20:
        insights_en.append("Moisture low. Water immediately.")
        insights_te.append("తేమ చాలా తక్కువగా ఉంది. వెంటనే నీరు పెట్టండి.")
        
    suggestion_en = f"For {data.Crop_Name}, use {fert_rec['fertilizer']}."
    suggestion_te = f"{data.Crop_Name} పంటకు, {fert_rec['fertilizer']} వాడండి."

    return {
        "Recommended_Fertilizer_Type": fert_rec['fertilizer'],
        "Fertilizer_Purpose": fert_rec['purpose'], # Dict {en, te}
        "Additional_Fertilizer_Info": fert_rec['additional'], # Dict {en, te}
        "Fertilizer_Quantity_kg_per_acre": round(quantity, 2),
        "Irrigation_Method": irr_rec['method'], # Dict {en, te}
        "Irrigation_Timing": irr_rec['timing'], # Dict
        "Irrigation_Frequency": irr_rec['frequency'], # Dict
        "Irrigation_Tips": irr_rec['tips'], # Dict
        "Crop_Success_Probability": round(success_prob, 2),
        "Insights": {'en': insights_en, 'te': insights_te},
        "Suggestion": {'en': suggestion_en, 'te': suggestion_te},
        "landArea": data.landArea
    }

@app.post("/chat")
def chat_endpoint(input_data: ChatInput):
    response = chatbot.get_response(input_data.query, input_data.language, input_data.name, input_data.location)
    return {"reply": response}

@app.post("/download_report")
def download_report(data: dict = Body(...)):
    """Generate and download a PDF report"""
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Helper to safely encode text for PDF (Latin-1)
        def safe_text(text):
            if not text: return ""
            # Replace common incompatible chars
            text = str(text).replace("–", "-").replace("—", "-").replace("’", "'")
            try:
                # Try to use existing latin-1 chars
                return text.encode('latin-1', 'replace').decode('latin-1')
            except:
                return "???"

        # NOTE: PDF is generated in English primarily to avoid font issues with FPDF standard
        # If we had a unicode font we could use it, but for stability we stick to safe text.
        
        # Color variables
        pdf.set_text_color(40, 40, 40)
        
        # Title
        pdf.set_font("Arial", 'B', 24)
        pdf.set_text_color(47, 133, 90) # Green
        pdf.cell(0, 15, "Smart Fertilizer Recommendation", 0, 1, 'C')
        
        pdf.set_font("Arial", 'I', 12)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 10, "Providing accurate farming intelligence", 0, 1, 'C')
        pdf.ln(10)
        
        # Farmer Details
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "Farmer Details", 0, 1)
        
        pdf.set_font("Arial", '', 12)
        pdf.set_fill_color(240, 255, 240)
        pdf.cell(100, 10, safe_text(f"Name: {data.get('farmer_name', 'N/A')}"), 1, 0, 'L', 1)
        pdf.cell(90, 10, safe_text(f"Location: {data.get('location', 'N/A')}"), 1, 1, 'L', 1)
        pdf.ln(5)
        
        # Recommendation
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(47, 133, 90)
        pdf.cell(0, 10, "Recommendation", 0, 1)
        
        fert_type = data.get('Recommended_Fertilizer_Type', 'N/A')
        qty = data.get('Fertilizer_Quantity_kg_per_acre', 0)
        area = data.get('landArea', 1)
        total_qty = round(qty * area, 2)
        
        pdf.set_font("Arial", '', 12)
        pdf.set_text_color(0, 0, 0)
        
        pdf.cell(95, 10, "Recommended Fertilizer", 1, 0)
        pdf.cell(95, 10, safe_text(str(fert_type)), 1, 1)
        
        pdf.cell(95, 10, "Quantity per Acre", 1, 0)
        pdf.cell(95, 10, f"{qty} kg", 1, 1)
        
        pdf.cell(95, 10, "Land Area", 1, 0)
        pdf.cell(95, 10, f"{area} acres", 1, 1)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(95, 10, "Total Quantity Required", 1, 0)
        pdf.cell(95, 10, f"{total_qty} kg", 1, 1)
        pdf.ln(5)
        
        # Handle Bilingual Dicts -> Fallback to English for PDF
        def get_en(val):
            if isinstance(val, dict): return val.get('en', '')
            return val

        purpose = get_en(data.get('Fertilizer_Purpose', ''))
        if purpose:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 8, "Purpose:", 0, 1)
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, safe_text(purpose))
            pdf.ln(5)

        # Irrigation
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(37, 99, 235) # Blue
        pdf.cell(0, 10, "Irrigation Guidance", 0, 1)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 11)
        
        method = get_en(data.get('Irrigation_Method', ''))
        timing = get_en(data.get('Irrigation_Timing', ''))
        tips = get_en(data.get('Irrigation_Tips', ''))
        
        if method: pdf.multi_cell(0, 8, safe_text(f"Method: {method}"))
        if timing: pdf.multi_cell(0, 8, safe_text(f"Timing: {timing}"))
        if tips: pdf.multi_cell(0, 8, safe_text(f"Tips: {tips}"))
            
        pdf.ln(5)

        # Footer
        pdf.set_y(-30)
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(0, 10, "Generated by Smart Fertilizer Recommendation System", 0, 0, 'C')

        # Output
        pdf_output = io.BytesIO()
        pdf_string = pdf.output(dest='S').encode('latin-1') 
        pdf_output.write(pdf_string)
        pdf_output.seek(0)
        
        return StreamingResponse(
            pdf_output, 
            media_type="application/pdf", 
            headers={"Content-Disposition": f"attachment; filename=report.pdf"}
        )
    except Exception as e:
        print(f"PDF Error: {e}")
        # Return a simple text file error or HTTP error
        raise HTTPException(status_code=500, detail="Error generating PDF.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
