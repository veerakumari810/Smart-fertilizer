# Voice-Enabled Agriculture Chatbot Guide

The chatbot has been upgraded to support Multilingual Voice Interaction (English & Telugu).

## Features

### 1. Voice Interaction 🎤
- **Voice Input**: Click the **Microphone Icon 🎤** in the chat window to speak.
- **Voice Output**: The chatbot automatically reads out the response (Text-to-Speech).
- **Supported Browser**: Use Google Chrome or Microsoft Edge for best compatibility.

### 2. Smart Language Detection 🌐
- **Typing**: The bot detects if you type in Telugu script (e.g., "నమస్కారం") and responds in Telugu.
- **Speaking**:
    - If the chat language is set to **English**, speak in English.
    - If the chat language is set to **Telugu**, speak in Telugu.
- **Strict Mode**: The bot never mixes languages. It replies strictly in the language detected or selected.

### 3. Agricultural Expert Knowledge 🌾
- **Topics**: Soil, Irrigation, Fertilizers, Crops.
- **Fertilizer Rules**: Avoids generic "Urea" advice; suggests crop-specific nutrients (DAP, MOP, etc.) and explains them.
- **Irrigation Rules**: Focuses on water management without confusing with fertilizers.
- **Farmer-Friendly**: Uses short, clear sentences suitable for voice.

## How to Test

1. **Start the Backend**:
   ```bash
   cd backend
   python main.py
   ```

2. **Start the Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open App**: Go to `http://localhost:5173` (or the URL shown in terminal).

4. **Use Voice**:
   - Open the Chatbot (bottom right).
   - Click the **Mic 🎤**.
   - Say: *"Which fertilizer is best for Rice?"* (Ensure EN mode is on).
   - The bot should reply in English and speak the answer.
   - Switch to **Telugu** mode.
   - Click **Mic 🎤**.
   - Say: *"Vari ki ye eruvi veyali?"* (Speak in Telugu).
   - The bot should reply in Telugu and speak the answer.

## Troubleshooting
- **Microphone not working**: Allow browser permission for the microphone.
- **No Sound**: Check system volume. Note that Telugu Text-to-Speech voice depends on OS support (Windows usually supports it).
