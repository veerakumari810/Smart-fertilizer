import React, { useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route, useNavigate, Navigate } from 'react-router-dom';
import InputForm from './components/InputForm';
import Results from './components/Results';
import Chatbot from './components/Chatbot';
import Home from './components/Home';
import FarmerDetails from './components/FarmerDetails';
import { translations } from './i18n';

function AppContent() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [language, setLanguage] = useState('en');
  const [farmerData, setFarmerData] = useState(null);

  const navigate = useNavigate();
  const t = translations[language];

  const handlePredict = async (formData) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      // Ensure backend is running at localhost:8000
      const response = await axios.post('http://localhost:8000/predict', formData);
      setResult({ ...response.data, landArea: formData.landArea });
      navigate('/result');
    } catch (err) {
      setError(translations[language].chatError || "Failed to fetch recommendation. Ensure backend is running.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

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
        <h1 style={{ fontSize: '2.5rem', color: '#2F855A', cursor: 'pointer' }} onClick={() => navigate('/')}>{t.appTitle}</h1>
        <p style={{ fontSize: '1.2rem', color: '#4A5568' }}>{t.appSubtitle}</p>

        {/* Language Toggle in Header for Global Access */}
        <div style={{ position: 'absolute', top: '20px', right: '20px', display: 'flex', gap: '0.5rem' }}>
          <button
            onClick={() => setLanguage('en')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '8px',
              border: language === 'en' ? '2px solid var(--primary)' : '2px solid #ddd',
              background: language === 'en' ? 'var(--primary)' : 'white',
              color: language === 'en' ? 'white' : '#333',
              cursor: 'pointer',
              fontWeight: '600',
              fontSize: '0.85rem'
            }}
          >
            EN
          </button>
          <button
            onClick={() => setLanguage('te')}
            style={{
              padding: '0.4rem 0.8rem',
              borderRadius: '8px',
              border: language === 'te' ? '2px solid var(--primary)' : '2px solid #ddd',
              background: language === 'te' ? 'var(--primary)' : 'white',
              color: language === 'te' ? 'white' : '#333',
              cursor: 'pointer',
              fontWeight: '600',
              fontSize: '0.85rem'
            }}
          >
            తెలుగు
          </button>
        </div>
      </header>

      <main className="container">
        <Routes>
          <Route path="/" element={<Home language={language} />} />
          <Route
            path="/farmer-details"
            element={<FarmerDetails setFarmerData={setFarmerData} language={language} />}
          />
          <Route
            path="/input"
            element={
              <InputForm
                onSubmit={handlePredict}
                isLoading={loading}
                language={language}
                setLanguage={setLanguage}
              />
            }
          />
          <Route
            path="/result"
            element={
              result ? (
                <div>
                  <div style={{ marginBottom: '2rem' }}>
                    <button
                      onClick={() => {
                        setResult(null);
                        navigate('/input');
                      }}
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
                  <Results result={result} farmerData={farmerData} language={language} />
                </div>
              ) : (
                <Navigate to="/input" replace />
              )
            }
          />
        </Routes>

        {error && (
          <div style={{ color: 'red', textAlign: 'center', marginTop: '1rem', padding: '1rem', background: '#fff0f0', borderRadius: '8px' }}>
            {error}
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

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
