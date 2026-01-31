import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { translations, cropTranslations, seasonTranslations, soilTypeDefaults } from '../i18n';

const crops = ['Rice', 'Maize', 'Chickpea', 'Kidneybeans', 'Pigeonpeas', 'Mothbeans',
  'Mungbean', 'Blackgram', 'Lentil', 'Pomegranate', 'Banana', 'Mango', 'Grapes',
  'Watermelon', 'Muskmelon', 'Apple', 'Orange', 'Papaya', 'Coconut', 'Cotton', 'Jute',
  'Coffee', 'Wheat', 'Sugarcane'];

const seasons = ['Kharif', 'Rabi', 'Zaid', 'Summer', 'Winter', 'Whole Year'];

const InputForm = ({ onSubmit, isLoading, language, setLanguage }) => {
  const t = translations[language];

  const [formData, setFormData] = useState({
    soilType: '',
    Soil_N: '',
    Soil_P: '',
    Soil_K: '',
    Soil_pH: '',
    Soil_Moisture: '',
    Crop_Name: crops[0],
    Season: seasons[0],
    landArea: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSoilTypeChange = (e) => {
    const selectedSoilType = e.target.value;
    setFormData({ ...formData, soilType: selectedSoilType });

    // Auto-fill values if a soil type is selected
    if (selectedSoilType && soilTypeDefaults[selectedSoilType]) {
      const defaults = soilTypeDefaults[selectedSoilType];
      setFormData({
        ...formData,
        soilType: selectedSoilType,
        Soil_N: defaults.Soil_N,
        Soil_P: defaults.Soil_P,
        Soil_K: defaults.Soil_K,
        Soil_pH: defaults.Soil_pH,
        Soil_Moisture: defaults.Soil_Moisture
      });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <motion.div
      className="glass-panel"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2>{t.formTitle}</h2>

      </div>
      <p style={{ marginBottom: '1.5rem', color: '#718096' }}>{t.formSubtitle}</p>

      <form onSubmit={handleSubmit}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          {/* Soil Type Dropdown */}
          <div className="input-group" style={{ gridColumn: 'span 2' }}>
            <label>{t.soilTypeLabel}</label>
            <select name="soilType" value={formData.soilType} onChange={handleSoilTypeChange}>
              <option value="">{t.soilTypeSelect}</option>
              <option value="black">{t.soilTypes.black}</option>
              <option value="red">{t.soilTypes.red}</option>
              <option value="alluvial">{t.soilTypes.alluvial}</option>
              <option value="sandy">{t.soilTypes.sandy}</option>
            </select>
          </div>

          <div className="input-group">
            <label>{t.nitrogenLabel}</label>
            <input type="number" name="Soil_N" required value={formData.Soil_N} onChange={handleChange} placeholder={t.nitrogenPlaceholder} />
          </div>
          <div className="input-group">
            <label>{t.phosphorusLabel}</label>
            <input type="number" name="Soil_P" required value={formData.Soil_P} onChange={handleChange} placeholder={t.phosphorusPlaceholder} />
          </div>
          <div className="input-group">
            <label>{t.potassiumLabel}</label>
            <input type="number" name="Soil_K" required value={formData.Soil_K} onChange={handleChange} placeholder={t.potassiumPlaceholder} />
          </div>
          <div className="input-group">
            <label>{t.phLabel}</label>
            <input type="number" step="0.1" name="Soil_pH" required value={formData.Soil_pH} onChange={handleChange} placeholder={t.phPlaceholder} />
          </div>
          <div className="input-group">
            <label>{t.moistureLabel}</label>
            <input type="number" name="Soil_Moisture" required value={formData.Soil_Moisture} onChange={handleChange} placeholder={t.moisturePlaceholder} />
          </div>
          <div className="input-group">
            <label>{t.landAreaLabel}</label>
            <input type="number" step="0.1" name="landArea" required value={formData.landArea} onChange={handleChange} placeholder={t.landAreaPlaceholder} />
          </div>

          <div className="input-group">
            <label>{t.cropLabel}</label>
            <select name="Crop_Name" value={formData.Crop_Name} onChange={handleChange}>
              {crops.map(c => <option key={c} value={c}>{cropTranslations[language][c]}</option>)}
            </select>
          </div>
          <div className="input-group">
            <label>{t.seasonLabel}</label>
            <select name="Season" value={formData.Season} onChange={handleChange}>
              {seasons.map(s => <option key={s} value={s}>{seasonTranslations[language][s]}</option>)}
            </select>
          </div>
        </div>

        <button type="submit" className="btn-primary" disabled={isLoading} style={{ marginTop: '1rem' }}>
          {isLoading ? (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
              <div className="loader" style={{ width: '20px', height: '20px', border: '3px solid #f3f3f3', borderTop: '3px solid white' }}></div>
              {t.analyzing}
            </div>
          ) : t.submitButton}
        </button>
      </form>
    </motion.div>
  );
};

export default InputForm;
