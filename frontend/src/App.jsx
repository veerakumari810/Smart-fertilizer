import React, { useState } from 'react';
import axios from 'axios';
import InputForm from './components/InputForm';
import Results from './components/Results';
import Chatbot from './components/Chatbot';
import { translations } from './i18n';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [language, setLanguage] = useState('en');

  const handlePredict = async (formData) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      // Ensure backend is running at localhost:8000
      const response = await axios.post('http://localhost:8000/predict', formData);
      setResult({ ...response.data, landArea: formData.landArea });
    } catch (err) {
      setError(translations[language].chatError || "Failed to fetch recommendation. Ensure backend is running.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const t = translations[language];

  return (
    <div className="app-container">
      <header style={{
        textAlign: 'center',
        padding: '3rem 1rem',
        background: 'rgba(255,255,255,0.4)',
        backdropFilter: 'blur(10px)',
        marginBottom: '2rem',
        borderBottom: '1px solid rgba(255,255,255,0.5)'
      }}>
        <h1 style={{ fontSize: '2.5rem', color: '#2F855A' }}>{t.appTitle}</h1>
        <p style={{ fontSize: '1.2rem', color: '#4A5568' }}>{t.appSubtitle}</p>
      </header>

      <main className="container">
        {!result && (
          <InputForm onSubmit={handlePredict} isLoading={loading} language={language} setLanguage={setLanguage} />
        )}

        {error && (
          <div style={{ color: 'red', textAlign: 'center', marginTop: '1rem', padding: '1rem', background: '#fff0f0', borderRadius: '8px' }}>
            {error}
          </div>
        )}

        {result && (
          <div>
            <div style={{ marginBottom: '2rem' }}>
              <button
                onClick={() => setResult(null)}
                style={{
                  background: 'transparent',
                  border: '2px solid var(--primary)',
                  color: 'var(--primary)',
                  padding: '0.5rem 1rem',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontWeight: '600'
                }}
              >
                {t.backButton}
              </button>
            </div>
            <Results result={result} language={language} />
          </div>
        )}
      </main>

      <footer style={{ textAlign: 'center', padding: '2rem', color: '#718096', marginTop: '4rem' }}>
        <p>{t.footerText}</p>
      </footer>
      <Chatbot language={language} />
    </div>
  );
}

export default App;
