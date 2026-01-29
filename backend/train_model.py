import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib
import os
import matplotlib.pyplot as plt

# 1. Load Data
# Assuming dataset is in the parent directory as per user structure
DATA_PATH = r"..\smart_fertilizer_dataset.xlsx"
if not os.path.exists(DATA_PATH):
    print(f"Error: Dataset not found at {DATA_PATH}")
    exit(1)

print("Loading dataset...")
df = pd.read_excel(DATA_PATH)

# Standardize column names
df = df.rename(columns={
    'Soil_N (ppm)': 'Soil_N',
    'Soil_P (ppm)': 'Soil_P',
    'Soil_K (ppm)': 'Soil_K',
    'Soil_Moisture (%)': 'Soil_Moisture'
})

# Features and Targets
X = df[['Soil_N', 'Soil_P', 'Soil_K', 'Soil_pH', 'Soil_Moisture', 'Crop_Name', 'Season']]

y_type = df['Recommended_Fertilizer_Type']
y_quant = df['Fertilizer_Quantity_kg_per_acre']
y_prob = df['Crop_Success_Probability']

# 2. Preprocessing
print("Preprocessing data...")

# Target Encoders
le_type = LabelEncoder()
y_type_enc = le_type.fit_transform(y_type)
num_classes = len(le_type.classes_)

# Feature Preprocessing
# Numerical: N, P, K, pH, Moisture
# Categorical: Crop_Name, Season
numeric_features = ['Soil_N', 'Soil_P', 'Soil_K', 'Soil_pH', 'Soil_Moisture']
categorical_features = ['Crop_Name', 'Season']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ])

X_processed = preprocessor.fit_transform(X)

# Split Data
X_train, X_test, y_type_train, y_type_test, y_quant_train, y_quant_test, y_prob_train, y_prob_test = train_test_split(
    X_processed, y_type_enc, y_quant, y_prob, test_size=0.2, random_state=42
)

# 3. Model Architecture
print("Building model...")
input_layer = Input(shape=(X_train.shape[1],))

x = Dense(128, activation='relu')(input_layer)
x = Dropout(0.2)(x)
x = Dense(64, activation='relu')(x)
x = Dense(32, activation='relu')(x)

# Outputs
out_type = Dense(num_classes, activation='softmax', name='fertilizer_type')(x)
out_quant = Dense(1, activation='linear', name='quantity')(x)
out_prob = Dense(1, activation='sigmoid', name='probability')(x)

model = Model(inputs=input_layer, outputs=[out_type, out_quant, out_prob])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss={
        'fertilizer_type': 'sparse_categorical_crossentropy',
        'quantity': 'mse',
        'probability': 'mse' 
    },
    metrics={
        'fertilizer_type': 'accuracy',
        'quantity': 'mae',
        'probability': 'mae'
    }
)

# 4. Training
print("Starting training...")
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

history = model.fit(
    X_train,
    {'fertilizer_type': y_type_train, 'quantity': y_quant_train, 'probability': y_prob_train},
    validation_data=(X_test, {'fertilizer_type': y_type_test, 'quantity': y_quant_test, 'probability': y_prob_test}),
    epochs=40,
    batch_size=64,
    callbacks=[early_stopping],
    verbose=1
)

# 5. Evaluation
print("\n--- Evaluation ---")
results = model.evaluate(X_test, {'fertilizer_type': y_type_test, 'quantity': y_quant_test, 'probability': y_prob_test})
print(f"Loss: {results[0]}")
print(f"Type Accuracy: {results[4]}") # Index depends on metrics return order
print(f"Quantity MAE: {results[5]}")
print(f"Probability MAE: {results[6]}")

# 6. Save Artifacts
print("Saving artifacts...")
model.save('fertilizer_model.keras')
joblib.dump(preprocessor, 'preprocessor.pkl')
joblib.dump(le_type, 'label_encoder.pkl')


# Plot Loss
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.savefig('training_loss.png')

print("Done! Model and artifacts saved in backend/")
