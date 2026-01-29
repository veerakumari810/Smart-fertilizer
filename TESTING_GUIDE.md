# Quick Start & Testing Guide

## 🚀 Quick Start

### Step 1: Start Backend
```bash
cd backend
python -m uvicorn main:app --reload
```
✅ Backend should start at `http://localhost:8000`

### Step 2: Start Frontend
Open a new terminal:
```bash
cd frontend
npm run dev
```
✅ Frontend should start at `http://localhost:5173`

### Step 3: Open Browser
Navigate to `http://localhost:5173`

---

## 🧪 Feature Testing Checklist

### ✅ Test 1: Soil Type Auto-Fill

**Steps:**
1. Open the application
2. Look for "Soil Type" dropdown (first field)
3. Select **"Black Soil"** (or "నల్ల నేల" in Telugu)
4. **Expected Result:**
   - Nitrogen: 45
   - Phosphorus: 55
   - Potassium: 60
   - pH: 7.2
   - Moisture: 35

5. **Edit Test:** Change Nitrogen from 45 to 50
6. Click "Get Fertilizer Plan"
7. **Verify:** Backend should receive N=50 (your edited value)

**Other Soil Types to Test:**
- Red Soil: N=35, P=40, K=45, pH=6.0, M=25
- Alluvial Soil: N=50, P=60, K=55, pH=6.8, M=40
- Sandy Soil: N=25, P=30, K=35, pH=5.5, M=15

---

### ✅ Test 2: Land Area Calculation

**Steps:**
1. Fill the form with any values
2. Enter **Land Area: 5** acres
3. Click "Get Fertilizer Plan"
4. **Expected Result:**
   - You should see TWO cards:
     - **Application Quantity**: X kg/acre (from ML model)
     - **Total Quantity**: (X × 5) kg (calculated)
   - Example: If per acre = 45.2 kg, total = 226.0 kg

**Try Different Land Areas:**
- 1 acre → Total = 1 × per acre
- 10 acres → Total = 10 × per acre
- 2.5 acres → Total = 2.5 × per acre

---

### ✅ Test 3: Multi-Language Support

**Steps:**
1. **Default Language:** App should start in English
2. Click **"తెలుగు"** button (top right of form)
3. **Expected Changes:**
   - Form title: "🌱 నేల & పంట వివరాలు"
   - Nitrogen label: "నత్రజని (N) [ppm]"
   - Crop dropdown: "వరి" instead of "Rice"
   - Submit button: "ఎరువుల ప్రణాళిక పొందండి"

4. **Submit a form in Telugu**
5. **Results page should be in Telugu:**
   - Title: "📝 సిఫార్సు నివేదిక"
   - Labels: "సిఫార్సు చేయబడిన ఎరువు"
   - Insights in Telugu

6. Click **"EN"** button
7. **Verify:** Everything switches back to English

**Elements to Check:**
- [ ] Form labels
- [ ] Button text
- [ ] Placeholders
- [ ] Crop names in dropdown
- [ ] Season names in dropdown
- [ ] Results page title
- [ ] Results card labels
- [ ] Footer text

---

### ✅ Test 4: Chatbot Functionality

**Steps:**

#### A. Open Chatbot
1. Click the **💬** button (bottom right)
2. Chatbot window should open
3. Welcome message should appear in English

#### B. Test Greetings (English)
1. Type: **"hi"** → Press Enter
2. **Expected:** "Hello! How can I help you with farming today?"
3. Type: **"hello"** → Press Enter
4. **Expected:** "Hi there! Ask me about fertilizers, crops, or soil health."
5. Type: **"thanks"** → Press Enter
6. **Expected:** "You're welcome! Happy farming! 🌾"

#### C. Test Language Switch
1. Click **"తెలుగు"** button in chatbot header
2. Type: **"హలో"** → Press Enter
3. **Expected:** Response in Telugu
4. Type: **"ధన్యవాదాలు"** → Press Enter
5. **Expected:** "స్వాగతం! శుభ వ్యవసాయం! 🌾"

#### D. Test Farming Questions (English)
1. Click **"EN"** in chatbot header
2. Type: **"What is the best fertilizer for rice?"**
3. **Expected:** Detailed answer about Urea, DSP/SSP, MOP
4. Type: **"What is NPK?"**
5. **Expected:** Explanation of Nitrogen, Phosphorus, Potassium

#### E. Test Farming Questions (Telugu)
1. Click **"తెలుగు"** in chatbot header
2. Type: **"వరికి ఉత్తమ ఎరువు ఏమిటి?"**
3. **Expected:** Answer in Telugu about fertilizers
4. Type: **"NPK అంటే ఏమిటి?"**
5. **Expected:** Telugu explanation

**Questions to Test:**
- "How do I fix acidic soil?"
- "My soil moisture is very low, what should I do?"
- "When is the best time to apply fertilizer?"
- "What fertilizer for wheat?"
- "Why are my leaves turning yellow?"
- "tell me about organic fertilizers"

---

## 🎯 Complete User Flow Test

**Scenario:** A farmer wants fertilizer recommendation for 5 acres of rice field

1. **Open App** → Should see English interface
2. **Switch to Telugu** → Click "తెలుగు"
3. **Select Soil Type** → Choose "నల్ల నేల" (Black Soil)
   - Values auto-fill
4. **Adjust if needed** → Maybe change pH to 7.0
5. **Enter Land Area** → 5 acres
6. **Select Crop** → "వరి" (Rice)
7. **Select Season** → "ఖరీఫ్" (Kharif)
8. **Submit** → Click "ఎరువుల ప్రణాళిక పొందండి"
9. **View Results:**
   - Recommended fertilizer type
   - Per acre quantity
   - Total quantity for 5 acres
   - Success probability
   - Insights (if any)
10. **Ask Chatbot** → Click 💬
11. **Switch chatbot to Telugu** → Click "తెలుగు"
12. **Ask:** "వరికి ఉత్తమ ఎరువు ఏమిటి?"
13. **Get Answer** → In Telugu
14. **Say Thanks** → "ధన్యవాదాలు"
15. **Get Response** → "స్వాగతం! శుభ వ్యవసాయం! 🌾"

---

## 🐛 Common Issues & Solutions

### Issue 1: Backend not starting
**Error:** "Module not found: tensorflow"
**Solution:**
```bash
pip install tensorflow fastapi uvicorn pandas scikit-learn joblib
```

### Issue 2: Frontend not starting
**Error:** "Cannot find module 'axios'"
**Solution:**
```bash
cd frontend
npm install
```

### Issue 3: Chatbot not responding
**Check:**
1. Is backend running? (http://localhost:8000)
2. Check browser console for errors
3. Verify `farming_kb.json` exists in backend folder

### Issue 4: Telugu text showing as boxes
**Solution:**
- Install Telugu font support on your system
- Or use a browser that supports Unicode (Chrome, Firefox)

### Issue 5: Auto-fill not working
**Check:**
1. Did you select a soil type from dropdown?
2. Check browser console for JavaScript errors
3. Verify `i18n.js` file exists

---

## 📱 Browser Compatibility

**Tested & Recommended:**
- ✅ Google Chrome (Latest)
- ✅ Mozilla Firefox (Latest)
- ✅ Microsoft Edge (Latest)

**May have issues:**
- ⚠️ Internet Explorer (Not supported)
- ⚠️ Safari (Older versions)

---

## 🔍 API Testing (Optional)

### Test /predict endpoint
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Soil_N": 45,
    "Soil_P": 55,
    "Soil_K": 60,
    "Soil_pH": 7.2,
    "Soil_Moisture": 35,
    "Crop_Name": "Rice",
    "Season": "Kharif",
    "landArea": 5
  }'
```

### Test /chat endpoint (English)
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is NPK?",
    "language": "en"
  }'
```

### Test /chat endpoint (Telugu)
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "NPK అంటే ఏమిటి?",
    "language": "te"
  }'
```

---

## ✅ Final Checklist

Before considering testing complete, verify:

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Soil type auto-fill works for all 4 types
- [ ] Auto-filled values are editable
- [ ] Land area input accepts decimal values
- [ ] Total quantity calculation is correct
- [ ] Language switch works (EN ↔ తెలుగు)
- [ ] All form labels translate
- [ ] Crop names translate
- [ ] Season names translate
- [ ] Results page translates
- [ ] Chatbot opens and closes
- [ ] Chatbot language selector works
- [ ] Chatbot responds to greetings
- [ ] Chatbot answers farming questions
- [ ] Chatbot responds in correct language
- [ ] No console errors in browser
- [ ] No errors in backend terminal

---

## 📞 Support

If you encounter any issues:
1. Check browser console (F12)
2. Check backend terminal for errors
3. Verify all dependencies are installed
4. Ensure both frontend and backend are running
5. Try clearing browser cache and reloading

---

**Happy Testing! 🎉**
