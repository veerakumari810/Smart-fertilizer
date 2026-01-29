# Smart Fertilizer Recommendation System

This project is a full-stack AI application that recommends fertilizer type and quantity based on soil parameters.

## Structure
- `backend/`: FastAPI server + Machine Learning Model + Chatbot Engine
- `frontend/`: React + Vite UI with multi-language support
- `smart_fertilizer_dataset.xlsx`: The dataset used for training

## Prerequisites
- Python 3.8+
- Node.js & npm

## Setup & Run

### 1. Backend
Navigate to the backend folder:
```bash
cd backend
```

Install dependencies:
```bash
pip install -r requirements.txt
```
*Note: If you encounter issues, ensure `tensorflow`, `fastapi`, `uvicorn`, `pandas`, `scikit-learn`, `joblib` are installed.*

Train the model (if needed):
```bash
python train_model.py
```
*This will generate `fertilizer_model.keras`, `preprocessor.pkl`, and `label_encoder.pkl`.*

Start the server:
```bash
python -m uvicorn main:app --reload
```
The API will run at `http://localhost:8000`.

### 2. Frontend
Navigate to the frontend folder:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Start the development server:
```bash
npm run dev
```
The UI will be available at `http://localhost:5173`.

## Usage
1. Open the frontend URL.
2. **Select Language**: Choose between English (EN) or Telugu (తెలుగు) using the language selector.
3. **Soil Type Auto-Fill** (Optional): Select a soil type (Black, Red, Alluvial, or Sandy) to auto-populate NPK, pH, and moisture values. You can still edit these values manually.
4. Enter or adjust soil parameters:
   - Nitrogen (N), Phosphorus (P), Potassium (K)
   - Soil pH
   - Soil Moisture (%)
5. Enter **Land Area** in acres.
6. Select **Crop Name** and **Season**.
7. Click "Get Fertilizer Plan".
8. View the AI-generated recommendations:
   - Recommended fertilizer type
   - Quantity per acre
   - **Total quantity** for your land area
   - Success probability
   - Detailed insights

## Features

### Core Features
- **Machine Learning**: Neural Network trained on 25,000 samples.
- **Backend**: Fast and efficient API using FastAPI.
- **Frontend**: Modern, responsive UI with glassmorphism design.
- **Smart Insights**: Rule-based logic for acidic/alkaline/low-moisture warnings.

### New Features ✨

#### 1. Soil Type Auto-Fill
- Select from 4 soil types: **Black**, **Red**, **Alluvial**, **Sandy**
- Automatically fills NPK, pH, and Moisture values based on typical soil characteristics
- All values remain **editable** after auto-fill
- Values are sent to the backend exactly as displayed

#### 2. Land Area Calculations
- Input your **land area in acres**
- Get fertilizer quantity **per acre**
- See **total fertilizer quantity** needed (per acre × acres)
- Helps farmers plan bulk purchases accurately

#### 3. Multi-Language Support (English + Telugu)
- **Language Selector** near "Soil & Crop Details" heading
- Switch between **EN** and **తెలుగు** anytime
- All UI elements translate instantly:
  - Labels, buttons, placeholders
  - Results and insights
  - Chatbot messages
- Crop and season names displayed in selected language
- Central i18n configuration for easy maintenance

#### 4. Enhanced Chatbot
- **Floating chatbot** on the right side of the screen
- **Independent language selector** in chatbot header (EN / తెలుగు)
- Responds in the selected language
- **Greeting Detection**: Recognizes and responds to:
  - Hi, Hello, Hey, Namaste → Friendly greeting
  - Thanks, Thank you, ధన్యవాదాలు → You're welcome message
- **Farmer-Friendly**: Simple, easy-to-understand responses
- **Knowledge Base**: Answers questions about:
  - Fertilizers for specific crops
  - Soil health (acidity, moisture, NPK)
  - Farming best practices
  - Organic fertilizers
  - Seasonal crops

## API Endpoints

### POST /predict
Predicts fertilizer recommendation based on soil and crop data.

**Request Body:**
```json
{
  "Soil_N": 45,
  "Soil_P": 55,
  "Soil_K": 60,
  "Soil_pH": 7.2,
  "Soil_Moisture": 35,
  "Crop_Name": "Rice",
  "Season": "Kharif",
  "landArea": 5
}
```

**Response:**
```json
{
  "Recommended_Fertilizer_Type": "Urea",
  "Fertilizer_Quantity_kg_per_acre": 45.2,
  "Crop_Success_Probability": 0.87,
  "Insights": [...],
  "Suggestion": "For Rice in Kharif, use Urea. Apply approx 45.2 kg/acre."
}
```

### POST /chat
Chatbot endpoint for farming queries.

**Request Body:**
```json
{
  "query": "What is the best fertilizer for rice?",
  "language": "en"
}
```

**Response:**
```json
{
  "reply": "For Rice, Urea is commonly used for Nitrogen..."
}
```

## Technology Stack
- **Frontend**: React, Vite, Framer Motion, Axios
- **Backend**: FastAPI, TensorFlow/Keras, scikit-learn
- **ML Model**: Multi-output Neural Network
- **Chatbot**: TF-IDF based similarity matching
- **Styling**: CSS with glassmorphism effects
- **i18n**: Custom translation configuration

## Project Highlights
✅ **No hardcoded text** - All UI text uses i18n configuration  
✅ **User-editable auto-fill** - Soil type suggestions don't lock values  
✅ **Accurate calculations** - Backend receives exactly what user sees  
✅ **Language-aware chatbot** - Responds in user's preferred language  
✅ **Farmer-centric design** - Simple, practical, and accessible

---

**Built with ❤️ for farmers using AI & React**
