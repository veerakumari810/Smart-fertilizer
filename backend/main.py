from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import os
from fastapi.middleware.cors import CORSMiddleware
import json

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
        
        # Question classification keywords
        self.soil_keywords = ['soil', 'dirt', 'earth', 'clay', 'loam', 'sand', 'fertility', 'nutrients', 'ph', 'acidity', 'alkaline', 'erosion', 'compaction', 'texture', 'structure', 'organic matter', 'humus', 'topsoil']
        self.irrigation_keywords = ['water', 'irrigation', 'watering', 'drip', 'sprinkler', 'flood', 'moisture', 'drought', 'rain', 'drainage', 'waterlogging', 'schedule', 'frequency']
        self.fertilizer_keywords = ['fertilizer', 'fertiliser', 'npk', 'urea', 'dap', 'compost', 'manure', 'nutrient', 'dosage', 'application', 'organic fertilizer', 'chemical fertilizer']
        self.greeting_keywords = ['hi', 'hello', 'hey', 'namaste', 'greetings', 'good morning', 'good evening']
        self.thanks_keywords = ['thank', 'thanks', 'appreciate', 'grateful']
        
        # Telugu keywords
        self.soil_keywords_te = ['నేల', 'మట్టి', 'భూమి', 'ఆమ్ల', 'క్షార']
        self.irrigation_keywords_te = ['నీరు', 'నీటిపారుదల', 'తేమ']
        self.fertilizer_keywords_te = ['ఎరువు', 'యూరియా', 'పోషకాలు']
    
    def classify_question(self, query, language='en'):
        """Classify the question into categories"""
        query_lower = query.lower()
        
        # Check for greetings
        if any(word in query_lower for word in self.greeting_keywords):
            return 'greeting'
        
        if any(word in query_lower for word in self.thanks_keywords):
            return 'thanks'
        
        # Check for specific topics
        is_soil = any(word in query_lower for word in self.soil_keywords)
        is_irrigation = any(word in query_lower for word in self.irrigation_keywords)
        is_fertilizer = any(word in query_lower for word in self.fertilizer_keywords)
        
        # Telugu keywords
        if language == 'te':
            is_soil = is_soil or any(word in query_lower for word in self.soil_keywords_te)
            is_irrigation = is_irrigation or any(word in query_lower for word in self.irrigation_keywords_te)
            is_fertilizer = is_fertilizer or any(word in query_lower for word in self.fertilizer_keywords_te)
        
        # Prioritize classification
        if is_fertilizer:
            return 'fertilizer'
        elif is_soil:
            return 'soil'
        elif is_irrigation:
            return 'irrigation'
        else:
            return 'general'
    
    def generate_soil_response(self, query, language='en'):
        """Generate intelligent soil-related responses"""
        query_lower = query.lower()
        
        # Specific soil questions
        if 'ph' in query_lower or 'acidity' in query_lower or 'acidic' in query_lower or 'ఆమ్ల' in query_lower:
            if language == 'te':
                return "ఆమ్ల నేల (తక్కువ pH) సమస్యను పరిష్కరించడానికి, వ్యవసాయ సున్నం (కాల్షియం కార్బోనేట్) లేదా డోలమైట్ వర్తింపజేయండి. ఇది pH స్థాయిలను 6.0-7.0 వరకు పెంచుతుంది. క్షార నేల (అధిక pH) కోసం, సల్ఫర్ లేదా జిప్సం ఉపయోగించండి."
            return "For acidic soil (low pH), apply agricultural lime (calcium carbonate) or dolomite to raise pH to 6.0-7.0. For alkaline soil (high pH), use sulfur or gypsum. Test your soil pH first before treatment."
        
        elif 'type' in query_lower or 'kind' in query_lower or 'రకం' in query_lower:
            if language == 'te':
                return "ప్రధాన నేల రకాలు: 1) నల్ల నేల - పత్తి, గోధుమకు మంచిది, 2) ఎరుపు నేల - వరి, చెరకుకు అనుకూలం, 3) ఒండ్రు నేల - చాలా సారవంతమైనది, అన్ని పంటలకు మంచిది, 4) ఇసుక నేల - మంచి డ్రైనేజీ, కానీ తక్కువ పోషకాలు. మీ నేల రకం ఏమిటి?"
            return "Main soil types: 1) Black soil - rich in clay, good for cotton and wheat, 2) Red soil - suitable for rice and sugarcane, 3) Alluvial soil - very fertile, good for all crops, 4) Sandy soil - good drainage but low nutrients. Which type do you have?"
        
        elif 'fertility' in query_lower or 'improve' in query_lower or 'better' in query_lower or 'సారవంతం' in query_lower:
            if language == 'te':
                return "నేల సారవంతాన్ని మెరుగుపరచడానికి: 1) సేంద్రీయ పదార్థాన్ని జోడించండి (కంపోస్ట్, పంట అవశేషాలు), 2) పంట మార్పిడి చేయండి, 3) చిక్కుడు కాయలు పండించండి (నత్రజని స్థిరీకరణ కోసం), 4) మల్చింగ్ చేయండి, 5) లోతైన దున్నడం నివారించండి. ఇవి నేల నిర్మాణం మరియు పోషకాలను మెరుగుపరుస్తాయి."
            return "To improve soil fertility: 1) Add organic matter (compost, crop residues), 2) Practice crop rotation, 3) Grow legumes (for nitrogen fixation), 4) Use mulching, 5) Avoid deep plowing. These improve soil structure and nutrient content naturally."
        
        elif 'nutrient' in query_lower or 'npk' in query_lower or 'nitrogen' in query_lower or 'పోషకాలు' in query_lower:
            if language == 'te':
                return "నేల పోషకాలు: నత్రజని (N) - ఆకుల పెరుగుదల, భాస్వరం (P) - వేర్ల అభివృద్ధి, పొటాషియం (K) - మొత్తం ఆరోగ్యం. లోపం సంకేతాలు: పసుపు ఆకులు (N లోపం), పేలవమైన వేర్లు (P లోపం), బలహీన కాండం (K లోపం). నేల పరీక్ష చేయించుకోండి."
            return "Soil nutrients: Nitrogen (N) - leaf growth, Phosphorus (P) - root development, Potassium (K) - overall health. Deficiency signs: yellowing leaves (N), poor roots (P), weak stems (K). Get a soil test for accurate assessment."
        
        elif 'moisture' in query_lower or 'dry' in query_lower or 'wet' in query_lower or 'తేమ' in query_lower:
            if language == 'te':
                return "నేల తేమ నిర్వహణ: 1) మల్చింగ్ తేమను నిలుపుకుంటుంది, 2) సేంద్రీయ పదార్థం నీటి నిలుపుదలని మెరుగుపరుస్తుంది, 3) సరైన డ్రైనేజీ నీటి చేరడం నివారిస్తుంది, 4) నేల తేమ 20-40% మధ్య ఉండాలి. చాలా పొడిగా ఉంటే నీరు పోయండి, చాలా తడిగా ఉంటే డ్రైనేజీ మెరుగుపరచండి."
            return "Soil moisture management: 1) Mulching retains moisture, 2) Organic matter improves water retention, 3) Proper drainage prevents waterlogging, 4) Ideal moisture is 20-40%. If too dry, irrigate; if too wet, improve drainage."
        
        else:
            if language == 'te':
                return "నేల ఆరోగ్యం విజయవంతమైన వ్యవసాయానికి కీలకం. మంచి నేలకు సరైన నిర్మాణం, తగినంత పోషకాలు, మంచి డ్రైనేజీ మరియు సేంద్రీయ పదార్థం అవసరం. మీకు నేల గురించి నిర్దిష్ట ప్రశ్న ఏమైనా ఉందా? (pH, రకం, సారవంతం, తేమ?)"
            return "Soil health is key to successful farming. Good soil needs proper structure, adequate nutrients, good drainage, and organic matter. Do you have a specific question about soil? (pH, type, fertility, moisture?)"
    
    def generate_irrigation_response(self, query, language='en'):
        """Generate intelligent irrigation-related responses"""
        query_lower = query.lower()
        
        if 'method' in query_lower or 'type' in query_lower or 'drip' in query_lower or 'sprinkler' in query_lower:
            if language == 'te':
                return "నీటిపారుదల పద్ధతులు: 1) డ్రిప్ - 90% నీటి సామర్థ్యం, కూరగాయలకు ఉత్తమం, 2) స్ప్రింక్లర్ - పెద్ద పొలాలకు మంచిది, 3) ఫ్లడ్ - సాంప్రదాయ, వరికి ఉపయోగించబడుతుంది, 4) ఫర్రో - వరుస పంటలకు. డ్రిప్ అత్యంత సమర్థవంతమైనది కానీ ప్రారంభ ఖర్చు ఎక్కువ."
            return "Irrigation methods: 1) Drip - 90% water efficiency, best for vegetables, 2) Sprinkler - good for large fields, 3) Flood - traditional, used for rice, 4) Furrow - for row crops. Drip is most efficient but has higher initial cost."
        
        elif 'frequency' in query_lower or 'how often' in query_lower or 'schedule' in query_lower or 'when' in query_lower:
            if language == 'te':
                return "నీటిపారుదల షెడ్యూల్: 1) వేసవి - ప్రతి 2-3 రోజులకు, 2) వర్షాకాలం - వర్షం ఆధారంగా, 3) చలికాలం - వారానికి ఒకసారి. నేల తేమను తనిఖీ చేయండి - 5 సెం.మీ లోతులో పొడిగా ఉంటే నీరు పోయండి. ఉదయం లేదా సాయంత్రం నీరు పోయడం ఉత్తమం."
            return "Irrigation schedule: 1) Summer - every 2-3 days, 2) Monsoon - based on rainfall, 3) Winter - once a week. Check soil moisture - water when dry at 5cm depth. Best time: early morning or evening to reduce evaporation."
        
        elif 'water' in query_lower and ('much' in query_lower or 'amount' in query_lower or 'quantity' in query_lower):
            if language == 'te':
                return "నీటి అవసరం పంట, నేల రకం మరియు వాతావరణంపై ఆధారపడి ఉంటుంది. సాధారణంగా: వరి - 1200-1500 మిమీ, గోధుమ - 450-650 మిమీ, కూరగాయలు - 300-500 మిమీ. అధిక నీరు వేర్ల కుళ్ళుకు దారితీస్తుంది, తక్కువ నీరు ఒత్తిడిని కలిగిస్తుంది. నేల తేమను పర్యవేక్షించండి."
            return "Water requirement depends on crop, soil type, and climate. Generally: Rice - 1200-1500mm, Wheat - 450-650mm, Vegetables - 300-500mm. Over-watering causes root rot, under-watering causes stress. Monitor soil moisture regularly."
        
        elif 'problem' in query_lower or 'issue' in query_lower or 'waterlog' in query_lower:
            if language == 'te':
                return "నీటిపారుదల సమస్యలు: 1) నీటి చేరడం - డ్రైనేజీ మెరుగుపరచండి, పెరిగిన పడకలు ఉపయోగించండి, 2) నీటి కొరత - డ్రిప్ వ్యవస్థ, మల్చింగ్, 3) లవణీకరణ - మంచి డ్రైనేజీ, నాణ్యమైన నీరు. మీకు ఏ సమస్య ఎదురవుతోంది?"
            return "Irrigation problems: 1) Waterlogging - improve drainage, use raised beds, 2) Water scarcity - drip system, mulching, 3) Salinity - good drainage, quality water. Which problem are you facing?"
        
        else:
            if language == 'te':
                return "సరైన నీటిపారుదల పంట ఆరోగ్యానికి కీలకం. అధిక నీరు మరియు తక్కువ నీరు రెండూ హానికరం. నేల తేమను తనిఖీ చేయండి, పంట దశను పరిగణించండి మరియు వాతావరణాన్ని పర్యవేక్షించండి. నీటిపారుదల గురించి మీకు నిర్దిష్ట ప్రశ్న ఏమైనా ఉందా?"
            return "Proper irrigation is crucial for crop health. Both over-watering and under-watering are harmful. Check soil moisture, consider crop stage, and monitor weather. Do you have a specific irrigation question?"
    
    def generate_fertilizer_response(self, query, language='en'):
        """Generate intelligent fertilizer-related responses"""
        query_lower = query.lower()
        
        # Check if asking about specific crop fertilizer
        if 'rice' in query_lower or 'వరి' in query_lower:
            if language == 'te':
                return "వరికి ఎరువు: 1) యూరియా (నత్రజని కోసం) - రోజుకు 2-3 విడతలుగా, 2) DAP/SSP (భాస్వరం) - విత్తనం సమయంలో, 3) MOP (పొటాషియం) - పాన్పు దశలో, 4) జింక్ సల్ఫేట్ - జింక్ లోపం ఉంటే. ఎకరానికి సుమారు 50-60 కిలోల యూరియా. మీ నేల పరీక్ష ఫలితాలు ఉన్నాయా?"
            return "For Rice: 1) Urea (nitrogen) - split into 2-3 doses, 2) DAP/SSP (phosphorus) - at sowing, 3) MOP (potassium) - at panicle stage, 4) Zinc sulfate if deficiency. Apply approx 50-60 kg urea per acre. Do you have soil test results?"
        
        elif 'wheat' in query_lower or 'గోధుమ' in query_lower:
            if language == 'te':
                return "గోధుమకు ఎరువు: 1) DAP - విత్తనం సమయంలో 50 కిలోలు/ఎకరం, 2) యూరియా - కిరీటం వేరు దశలో 40 కిలోలు/ఎకరం, 3) సమతుల్య NPK నిష్పత్తి 120:60:40. సేంద్రీయ ఎరువు (FYM) కూడా ఉపయోగించండి. మీ పొలం ఎంత విస్తీర్ణం?"
            return "For Wheat: 1) DAP - 50 kg/acre at sowing, 2) Urea - 40 kg/acre at crown root stage, 3) Balanced NPK ratio 120:60:40. Also use organic manure (FYM). What's your field size?"
        
        elif 'organic' in query_lower or 'natural' in query_lower or 'సేంద్రీయ' in query_lower:
            if language == 'te':
                return "సేంద్రీయ ఎరువులు: 1) కంపోస్ట్ - నేల నిర్మాణాన్ని మెరుగుపరుస్తుంది, 2) వర్మీకంపోస్ట్ - పోషకాలు సమృద్ధిగా, 3) పచ్చి ఎరువు - చిక్కుడు కాయలు, 4) FYM - 5-10 టన్నులు/ఎకరం, 5) నీమ్ కేక్ - తెగుళ్ళ నియంత్రణ + పోషకాలు. సేంద్రీయ ఎరువులు నెమ్మదిగా విడుదల అవుతాయి కానీ దీర్ఘకాలిక ప్రయోజనాలు ఉన్నాయి."
            return "Organic fertilizers: 1) Compost - improves soil structure, 2) Vermicompost - nutrient-rich, 3) Green manure - legumes, 4) FYM - 5-10 tons/acre, 5) Neem cake - pest control + nutrients. Organic fertilizers release slowly but have long-term benefits."
        
        elif 'dosage' in query_lower or 'amount' in query_lower or 'how much' in query_lower or 'quantity' in query_lower:
            if language == 'te':
                return "ఎరువు మొత్రం నేల పరీక్ష ఆధారంగా ఉండాలి. సాధారణ మార్గదర్శకాలు: యూరియా - 40-60 కిలోలు/ఎకరం, DAP - 40-50 కిలోలు/ఎకరం, MOP - 20-30 కిలోలు/ఎకరం. అధిక ఎరువు హానికరం - నీటి కాలుష్యం, పంట కాలిపోవడం. తక్కువ ఎరువు - పేలవమైన దిగుబడి. మీరు ఏ పంట పండిస్తున్నారు?"
            return "Fertilizer dosage should be based on soil test. General guidelines: Urea - 40-60 kg/acre, DAP - 40-50 kg/acre, MOP - 20-30 kg/acre. Over-fertilization is harmful - water pollution, crop burn. Under-fertilization - poor yield. Which crop are you growing?"
        
        elif 'timing' in query_lower or 'when' in query_lower or 'apply' in query_lower:
            if language == 'te':
                return "ఎరువు వేసే సమయం: 1) బేస్ డోస్ - విత్తనం/నాటడం సమయంలో (DAP, MOP), 2) టాప్ డ్రెస్సింగ్ - 20-30 రోజుల తర్వాత (యూరియా), 3) తెల్లవారుజామున లేదా సాయంత్రం వర్తింపజేయండి, 4) వర్షం తర్వాత లేదా నీటిపారుదల తర్వాత వర్తింపజేయండి. ఎండ సమయంలో ఎరువు వేయవద్దు - ఆవిరైపోతుంది."
            return "Fertilizer timing: 1) Basal dose - at sowing/planting (DAP, MOP), 2) Top dressing - after 20-30 days (Urea), 3) Apply in morning or evening, 4) Apply after rain or irrigation. Don't apply in hot sun - evaporates."
        
        else:
            if language == 'te':
                return "ఎరువులు పంట పెరుగుదలకు పోషకాలను అందిస్తాయి. రసాయన ఎరువులు త్వరగా పనిచేస్తాయి, సేంద్రీయ ఎరువులు నేలను మెరుగుపరుస్తాయి. సరైన మొత్రం మరియు సమయం కీలకం. మీకు ఎరువుల గురించి నిర్దిష్ట ప్రశ్న ఏమైనా ఉందా? (రకం, మొత్రం, సమయం?)"
            return "Fertilizers provide nutrients for crop growth. Chemical fertilizers work fast, organic fertilizers improve soil. Proper dosage and timing are key. Do you have a specific fertilizer question? (type, dosage, timing?)"
    
    def generate_general_response(self, query, language='en'):
        """Generate general agriculture responses"""
        query_lower = query.lower()
        
        if 'season' in query_lower or 'kharif' in query_lower or 'rabi' in query_lower or 'కాలం' in query_lower:
            if language == 'te':
                return "వ్యవసాయ కాలాలు: 1) ఖరీఫ్ (జూన్-అక్టోబర్) - వరి, మొక్కజొన్న, పత్తి, 2) రబీ (అక్టోబర్-మార్చి) - గోధుమ, శనగలు, ఆవాలు, 3) జైద్ (మార్చి-జూన్) - పుచ్చకాయ, కూరగాయలు. ప్రతి కాలానికి నిర్దిష్ట పంటలు మరియు వాతావరణ అవసరాలు ఉన్నాయి."
            return "Agricultural seasons: 1) Kharif (June-Oct) - rice, maize, cotton, 2) Rabi (Oct-March) - wheat, chickpea, mustard, 3) Zaid (March-June) - watermelon, vegetables. Each season has specific crops and weather requirements."
        
        elif 'crop rotation' in query_lower or 'rotation' in query_lower:
            if language == 'te':
                return "పంట మార్పిడి ప్రయోజనాలు: 1) నేల సారవంతాన్ని మెరుగుపరుస్తుంది, 2) తెగుళ్ళు మరియు వ్యాధులను తగ్గిస్తుంది, 3) నేల నిర్మాణాన్ని మెరుగుపరుస్తుంది. ఉదాహరణ: వరి → చిక్కుడు కాయలు → గోధుమ. చిక్కుడు కాయలు నత్రజనిని స్థిరీకరిస్తాయి."
            return "Crop rotation benefits: 1) Improves soil fertility, 2) Reduces pests and diseases, 3) Improves soil structure. Example: Rice → Legumes → Wheat. Legumes fix nitrogen naturally."
        
        elif 'pest' in query_lower or 'disease' in query_lower or 'insect' in query_lower:
            if language == 'te':
                return "తెగుళ్ళ నిర్వహణ: 1) నివారణ - పంట మార్పిడి, శుభ్రమైన విత్తనాలు, 2) జీవ నియంత్రణ - సహజ శత్రువులు, నీమ్ నూనె, 3) రసాయన నియంత్రణ - చివరి ఎంపిక. పంటను క్రమం తప్పకుండా పర్యవేక్షించండి. మీకు ఏ తెగులు సమస్య ఉంది?"
            return "Pest management: 1) Prevention - crop rotation, clean seeds, 2) Biological control - natural enemies, neem oil, 3) Chemical control - last option. Monitor crops regularly. Which pest problem do you have?"
        
        else:
            if language == 'te':
                return "నేను వ్యవసాయ నిపుణుడిని. నేల, నీటిపారుదల, ఎరువులు, పంటలు, కాలాలు మరియు వ్యవసాయ పద్ధతుల గురించి అడగండి. మీకు నిర్దిష్ట ప్రశ్న ఏమైనా ఉందా?"
            return "I'm an agriculture expert. Ask me about soil, irrigation, fertilizers, crops, seasons, and farming practices. Do you have a specific question?"
    
    def get_response(self, user_query, language='en'):
        """Main method to get intelligent response"""
        
        # Classify the question
        question_type = self.classify_question(user_query, language)
        
        # Handle greetings
        if question_type == 'greeting':
            if language == 'te':
                return "నమస్కారం! నేను మీ వ్యవసాయ సలహాదారుడిని. నేల, నీటిపారుదల, ఎరువులు లేదా పంటల గురించి అడగండి. నేను సహాయం చేయడానికి ఇక్కడ ఉన్నాను! 🌾"
            return "Hello! I'm your agriculture advisor. Ask me about soil, irrigation, fertilizers, or crops. I'm here to help! 🌾"
        
        if question_type == 'thanks':
            if language == 'te':
                return "స్వాగతం! విజయవంతమైన వ్యవసాయం కోసం శుభాకాంక్షలు! ఇంకా ప్రశ్నలు ఉంటే అడగండి. 🌱"
            return "You're welcome! Wishing you successful farming! Feel free to ask more questions. 🌱"
        
        # Generate contextual response based on question type
        if question_type == 'soil':
            return self.generate_soil_response(user_query, language)
        elif question_type == 'irrigation':
            return self.generate_irrigation_response(user_query, language)
        elif question_type == 'fertilizer':
            return self.generate_fertilizer_response(user_query, language)
        else:
            return self.generate_general_response(user_query, language)

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

class ChatInput(BaseModel):
    query: str
    language: str = 'en'  # Default to English

@app.get("/")
def home():
    return {"message": "Smart Fertilizer Recommendation API is running."}
# Crop-Specific Fertilizer Recommendations
def get_crop_specific_fertilizer(crop_name, soil_n, soil_p, soil_k, soil_ph, predicted_type):
    """Generate crop-specific fertilizer recommendations based on crop requirements"""
    
    crop_lower = crop_name.lower()
    
    # Crop-specific fertilizer knowledge base
    crop_fertilizers = {
        'rice': {
            'primary': 'Urea',
            'purpose': 'High nitrogen requirement for vegetative growth and tillering',
            'secondary': 'DAP for phosphorus during transplanting, MOP for grain filling'
        },
        'wheat': {
            'primary': 'DAP',
            'purpose': 'Balanced NPK with emphasis on phosphorus for root development',
            'secondary': 'Urea for top dressing at crown root stage'
        },
        'maize': {
            'primary': 'NPK Complex (12:32:16)',
            'purpose': 'Balanced nutrition for rapid growth and cob development',
            'secondary': 'Urea for side dressing at knee-high stage'
        },
        'cotton': {
            'primary': 'SSP',
            'purpose': 'Phosphorus and sulfur for fiber quality and boll formation',
            'secondary': 'MOP for potassium during flowering'
        },
        'sugarcane': {
            'primary': 'NPK Complex (20:20:0)',
            'purpose': 'High nitrogen and phosphorus for tillering and sugar accumulation',
            'secondary': 'MOP for potassium during grand growth phase'
        },
        'groundnut': {
            'primary': 'SSP',
            'purpose': 'Phosphorus and calcium for pod development, sulfur for oil content',
            'secondary': 'Gypsum for calcium during pegging stage'
        },
        'soybean': {
            'primary': 'DAP',
            'purpose': 'Phosphorus for root nodulation and nitrogen fixation',
            'secondary': 'Minimal nitrogen as legume fixes its own'
        },
        'chickpea': {
            'primary': 'SSP',
            'purpose': 'Phosphorus for nodule formation, sulfur for protein synthesis',
            'secondary': 'Rhizobium culture for nitrogen fixation'
        },
        'tomato': {
            'primary': 'NPK Complex (19:19:19)',
            'purpose': 'Balanced nutrition for fruit development and disease resistance',
            'secondary': 'Calcium nitrate to prevent blossom end rot'
        },
        'potato': {
            'primary': 'MOP',
            'purpose': 'High potassium for tuber quality and starch content',
            'secondary': 'DAP for early root development'
        },
        'onion': {
            'primary': 'NPK Complex (12:32:16)',
            'purpose': 'Phosphorus for bulb initiation, balanced NPK for bulb development',
            'secondary': 'Avoid excess nitrogen which delays maturity'
        },
        'cabbage': {
            'primary': 'Urea',
            'purpose': 'High nitrogen for leafy growth and head formation',
            'secondary': 'Organic compost for soil structure'
        },
        'cauliflower': {
            'primary': 'NPK Complex (20:20:0)',
            'purpose': 'Balanced nitrogen and phosphorus for curd development',
            'secondary': 'Boron for preventing hollow stem'
        },
        'chilli': {
            'primary': 'NPK Complex (19:19:19)',
            'purpose': 'Balanced nutrition for flowering and fruit setting',
            'secondary': 'Calcium for cell wall strength'
        },
        'brinjal': {
            'primary': 'DAP',
            'purpose': 'Phosphorus for root and fruit development',
            'secondary': 'MOP during fruiting stage'
        },
        'banana': {
            'primary': 'MOP',
            'purpose': 'Very high potassium requirement for fruit quality and bunch weight',
            'secondary': 'Organic manure for continuous nutrient supply'
        },
        'mango': {
            'primary': 'NPK Complex (10:26:26)',
            'purpose': 'Low nitrogen, high P and K for flowering and fruit development',
            'secondary': 'Avoid excess nitrogen which promotes vegetative growth'
        },
        'grapes': {
            'primary': 'MOP',
            'purpose': 'High potassium for sugar content and berry quality',
            'secondary': 'Calcium for firmness, avoid excess nitrogen'
        },
        'apple': {
            'primary': 'NPK Complex (12:12:36)',
            'purpose': 'High potassium for fruit color and quality',
            'secondary': 'Calcium for fruit firmness and storage quality'
        },
        'orange': {
            'primary': 'NPK Complex (8:24:24)',
            'purpose': 'Balanced P and K for fruit quality and juice content',
            'secondary': 'Micronutrients like zinc and iron'
        },
        'papaya': {
            'primary': 'NPK Complex (14:14:14)',
            'purpose': 'Balanced nutrition for continuous fruiting',
            'secondary': 'Organic manure for soil health'
        },
        'watermelon': {
            'primary': 'MOP',
            'purpose': 'High potassium for sweetness and fruit size',
            'secondary': 'DAP during vine growth'
        },
        'muskmelon': {
            'primary': 'NPK Complex (19:19:19)',
            'purpose': 'Balanced nutrition for vine growth and fruit sweetness',
            'secondary': 'Avoid excess nitrogen near harvest'
        },
        'pomegranate': {
            'primary': 'NPK Complex (10:26:26)',
            'purpose': 'High P and K for flowering and fruit quality',
            'secondary': 'Micronutrients for aril color'
        }
    }
    
    # Get crop-specific recommendation or use ML prediction as fallback
    if crop_lower in crop_fertilizers:
        crop_info = crop_fertilizers[crop_lower]
        
        # Adjust based on soil nutrient levels
        if soil_n < 50 and 'nitrogen' in crop_info['purpose'].lower():
            fertilizer = crop_info['primary']
        elif soil_p < 30 and 'phosphorus' in crop_info['purpose'].lower():
            fertilizer = crop_info['primary']
        elif soil_k < 40 and 'potassium' in crop_info['purpose'].lower():
            fertilizer = crop_info['primary']
        else:
            fertilizer = crop_info['primary']
        
        return {
            'fertilizer': fertilizer,
            'purpose': crop_info['purpose'],
            'additional': crop_info['secondary']
        }
    else:
        # Fallback to ML prediction
        return {
            'fertilizer': predicted_type,
            'purpose': f'ML-recommended fertilizer for {crop_name}',
            'additional': 'Consult local agriculture expert for specific guidance'
        }

# Crop-Specific Irrigation Guidance
def get_irrigation_guidance(crop_name, season, soil_moisture):
    """Generate crop-specific irrigation recommendations"""
    
    crop_lower = crop_name.lower()
    
    # Crop-specific irrigation knowledge base
    irrigation_guide = {
        'rice': {
            'method': 'Flood irrigation or Alternate Wetting and Drying (AWD)',
            'timing': 'Continuous standing water during tillering and flowering, drain 1 week before harvest',
            'frequency': 'Maintain 2-5 cm water depth, drain and re-flood every 3-4 days for AWD',
            'tips': 'AWD saves 15-30% water without yield loss. Ensure proper leveling for uniform water distribution'
        },
        'wheat': {
            'method': 'Furrow irrigation or Sprinkler',
            'timing': 'Critical at crown root initiation (21 DAS), tillering, flowering, and grain filling',
            'frequency': '4-6 irrigations depending on soil type and rainfall',
            'tips': 'Avoid waterlogging. Last irrigation 10 days before harvest for better grain quality'
        },
        'maize': {
            'method': 'Drip or Furrow irrigation',
            'timing': 'Critical at knee-high stage, tasseling, and grain filling',
            'frequency': 'Every 7-10 days, more frequent during tasseling',
            'tips': 'Drip irrigation increases yield by 20-30%. Avoid water stress during flowering'
        },
        'cotton': {
            'method': 'Drip irrigation (most efficient)',
            'timing': 'Critical at square formation, flowering, and boll development',
            'frequency': 'Every 10-12 days, reduce after boll opening',
            'tips': 'Stop irrigation 3-4 weeks before harvest for better fiber quality and easier picking'
        },
        'sugarcane': {
            'method': 'Furrow or Drip irrigation',
            'timing': 'Critical at germination, tillering, and grand growth phase',
            'frequency': 'Every 7-10 days during summer, 12-15 days in winter',
            'tips': 'Requires 1500-2500mm water annually. Drip saves 40% water and increases yield'
        },
        'groundnut': {
            'method': 'Drip or Sprinkler irrigation',
            'timing': 'Critical at flowering, pegging, and pod development',
            'frequency': 'Light irrigation every 7-10 days',
            'tips': 'Avoid excess water which causes root rot. Maintain 60-70% field capacity'
        },
        'soybean': {
            'method': 'Sprinkler or Furrow irrigation',
            'timing': 'Critical at flowering and pod filling stages',
            'frequency': '2-3 irrigations if rainfall is inadequate',
            'tips': 'Sensitive to waterlogging. Ensure good drainage. Drought during flowering reduces yield significantly'
        },
        'chickpea': {
            'method': 'Furrow irrigation (light)',
            'timing': 'Pre-flowering and pod development',
            'frequency': '1-2 irrigations in entire season',
            'tips': 'Excess water promotes disease. Avoid irrigation during flowering. Drought-tolerant crop'
        },
        'tomato': {
            'method': 'Drip irrigation (highly recommended)',
            'timing': 'Regular throughout crop cycle, critical during flowering and fruiting',
            'frequency': 'Daily or alternate days with drip, every 5-7 days with furrow',
            'tips': 'Consistent moisture prevents blossom end rot and fruit cracking. Mulching helps retain moisture'
        },
        'potato': {
            'method': 'Drip or Sprinkler irrigation',
            'timing': 'Critical at tuber initiation and bulking stages',
            'frequency': 'Every 5-7 days, maintain consistent moisture',
            'tips': 'Fluctuating moisture causes hollow heart and knobs. Stop irrigation 10 days before harvest'
        },
        'onion': {
            'method': 'Drip or Furrow irrigation',
            'timing': 'Frequent light irrigation during bulb formation',
            'frequency': 'Every 5-7 days, stop 15 days before harvest',
            'tips': 'Shallow roots require frequent irrigation. Stopping early improves storage quality'
        },
        'cabbage': {
            'method': 'Drip or Sprinkler irrigation',
            'timing': 'Regular throughout growth, critical during head formation',
            'frequency': 'Every 4-5 days, maintain consistent moisture',
            'tips': 'Inconsistent watering causes head splitting. Mulching reduces water requirement'
        },
        'cauliflower': {
            'method': 'Drip or Sprinkler irrigation',
            'timing': 'Critical during curd initiation and development',
            'frequency': 'Every 5-7 days, more frequent during curd formation',
            'tips': 'Water stress during curd formation causes buttoning. Maintain 70-80% field capacity'
        },
        'chilli': {
            'method': 'Drip irrigation (best for disease management)',
            'timing': 'Critical at flowering and fruit development',
            'frequency': 'Every 5-7 days, avoid waterlogging',
            'tips': 'Drip reduces disease incidence. Avoid overhead irrigation which spreads diseases'
        },
        'brinjal': {
            'method': 'Drip or Furrow irrigation',
            'timing': 'Regular throughout crop cycle, critical during fruiting',
            'frequency': 'Every 5-7 days in summer, 10-12 days in winter',
            'tips': 'Consistent moisture ensures continuous fruiting. Mulching helps in moisture conservation'
        },
        'banana': {
            'method': 'Drip irrigation (highly efficient)',
            'timing': 'Year-round, critical during bunch development',
            'frequency': 'Every 2-3 days in summer, 5-7 days in winter',
            'tips': 'High water requirement (2000-2500mm/year). Drip saves 45% water and increases yield by 30%'
        },
        'mango': {
            'method': 'Basin or Drip irrigation',
            'timing': 'Stop irrigation 2-3 months before flowering to induce flowering',
            'frequency': 'Every 10-15 days during fruit development',
            'tips': 'Water stress before flowering is beneficial. Resume irrigation after fruit set'
        },
        'grapes': {
            'method': 'Drip irrigation (essential)',
            'timing': 'Critical at bud break, flowering, and berry development',
            'frequency': 'Daily or alternate days with drip',
            'tips': 'Precise water management improves quality. Reduce irrigation near harvest for better sugar content'
        },
        'apple': {
            'method': 'Drip or Sprinkler irrigation',
            'timing': 'Critical during fruit development and sizing',
            'frequency': 'Every 7-10 days, adjust based on rainfall',
            'tips': 'Consistent moisture prevents fruit drop and improves size. Reduce irrigation before harvest'
        },
        'orange': {
            'method': 'Drip or Basin irrigation',
            'timing': 'Critical during flowering and fruit development',
            'frequency': 'Every 7-10 days, more frequent in summer',
            'tips': 'Water stress during fruit development reduces juice content. Maintain consistent moisture'
        },
        'papaya': {
            'method': 'Drip irrigation',
            'timing': 'Regular throughout the year',
            'frequency': 'Every 2-3 days, daily in summer',
            'tips': 'Shallow roots require frequent irrigation. Waterlogging causes root rot and plant death'
        },
        'watermelon': {
            'method': 'Drip irrigation',
            'timing': 'Critical during vine growth and fruit development',
            'frequency': 'Every 5-7 days, reduce near harvest',
            'tips': 'Reduce irrigation 1 week before harvest to increase sugar content. Avoid wetting fruits'
        },
        'muskmelon': {
            'method': 'Drip irrigation',
            'timing': 'Critical during flowering and fruit development',
            'frequency': 'Every 5-7 days, stop 1 week before harvest',
            'tips': 'Stopping irrigation before harvest improves sweetness and shelf life'
        },
        'pomegranate': {
            'method': 'Drip irrigation',
            'timing': 'Critical during flowering and fruit development',
            'frequency': 'Every 7-10 days, adjust based on season',
            'tips': 'Irregular irrigation causes fruit cracking. Drip irrigation prevents this and saves 40% water'
        }
    }
    
    # Get crop-specific irrigation or provide general guidance
    if crop_lower in irrigation_guide:
        guide = irrigation_guide[crop_lower]
        
        # Adjust based on current soil moisture
        moisture_note = ""
        if soil_moisture < 20:
            moisture_note = " ⚠️ Current soil moisture is critically low - irrigate immediately."
        elif soil_moisture < 40:
            moisture_note = " Current soil moisture is moderate - plan next irrigation soon."
        
        return {
            'method': guide['method'],
            'timing': guide['timing'],
            'frequency': guide['frequency'],
            'tips': guide['tips'] + moisture_note
        }
    else:
        # General irrigation guidance
        return {
            'method': 'Drip or Sprinkler irrigation recommended',
            'timing': 'Based on crop growth stages',
            'frequency': 'Monitor soil moisture, irrigate when needed',
            'tips': f'Maintain adequate moisture for {crop_name}. Consult local agriculture expert for specific guidance.'
        }

@app.post("/predict")
def predict_fertilizer(data: FertilizerInput):
    if not model or not preprocessor or not label_encoder:
        raise HTTPException(status_code=500, detail="Model logic not initialized. Run training first.")

    # 1. Prepare Input
    input_df = pd.DataFrame([data.dict()])
    
    # 2. Preprocess
    try:
        processed_input = preprocessor.transform(input_df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Preprocessing error: {str(e)}")

    # 3. Predict
    predictions = model.predict(processed_input)
    
    # Parse predictions
    type_probs = predictions[0]
    predicted_type_idx = np.argmax(type_probs, axis=1)[0]
    ml_predicted_type = label_encoder.inverse_transform([predicted_type_idx])[0]
    
    # Quantity logic (ensure non-negative)
    quantity = float(predictions[1][0][0])
    if quantity < 0: quantity = 0
    
    success_prob = float(predictions[2][0][0])
    if success_prob < 0: success_prob = 0
    if success_prob > 1: success_prob = 1

    # 4. Get Crop-Specific Fertilizer Recommendation
    fertilizer_rec = get_crop_specific_fertilizer(
        data.Crop_Name, 
        data.Soil_N, 
        data.Soil_P, 
        data.Soil_K, 
        data.Soil_pH,
        ml_predicted_type
    )
    
    # 5. Get Crop-Specific Irrigation Guidance
    irrigation_rec = get_irrigation_guidance(
        data.Crop_Name,
        data.Season,
        data.Soil_Moisture
    )
    
    # 6. Rule-based Insights (Soil Health)
    insights = []
    if data.Soil_N < 50:
        insights.append("Nitrogen is low. Essential for leafy growth.")
    if data.Soil_pH < 6.0:
        insights.append("Soil is acidic. Consider adding lime to neutralize.")
    elif data.Soil_pH > 7.5:
        insights.append("Soil is alkaline. Considerations for pH reduction.")
    if data.Soil_Moisture < 20:
        insights.append("Moisture is critically low. Immediate irrigation recommended.")
    
    # 7. Smart suggestion
    suggestion = f"For {data.Crop_Name} in {data.Season}, use {fertilizer_rec['fertilizer']}. {fertilizer_rec['purpose']}"

    return {
        "Recommended_Fertilizer_Type": fertilizer_rec['fertilizer'],
        "Fertilizer_Purpose": fertilizer_rec['purpose'],
        "Additional_Fertilizer_Info": fertilizer_rec['additional'],
        "Fertilizer_Quantity_kg_per_acre": round(quantity, 2),
        "Irrigation_Method": irrigation_rec['method'],
        "Irrigation_Timing": irrigation_rec['timing'],
        "Irrigation_Frequency": irrigation_rec['frequency'],
        "Irrigation_Tips": irrigation_rec['tips'],
        "Crop_Success_Probability": round(success_prob, 2),
        "Insights": insights,
        "Suggestion": suggestion
    }

@app.post("/chat")
def chat_endpoint(input_data: ChatInput):
    response = chatbot.get_response(input_data.query, input_data.language)
    return {"reply": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
