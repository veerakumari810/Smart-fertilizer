import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, MapPin, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { translations } from '../i18n';

const FarmerDetails = ({ setFarmerData, language }) => {
    const navigate = useNavigate();
    const t = translations[language];
    const [name, setName] = useState('');
    const [location, setLocation] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        // Load existing data if available
        const savedName = localStorage.getItem('farmerName');
        const savedLocation = localStorage.getItem('farmerLocation');
        if (savedName) setName(savedName);
        if (savedLocation) setLocation(savedLocation);
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!name.trim() || !location.trim()) {
            setError(t.fillAllFieldsError);
            return;
        }

        const data = { name, location };
        setFarmerData(data);
        localStorage.setItem('farmerName', name);
        localStorage.setItem('farmerLocation', location);

        navigate('/input');
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="glass-panel"
                style={{ maxWidth: '500px', width: '100%', padding: '3rem' }}
            >
                <h2 style={{ textAlign: 'center', marginBottom: '2rem', color: 'var(--primary-dark)' }}>
                    {t.farmerDetailsTitle}
                </h2>

                <form onSubmit={handleSubmit}>
                    <div className="input-group">
                        <label>
                            <User size={16} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
                            {t.farmerNameLabel}
                        </label>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder={t.enterNamePlaceholder}
                            className="premium-input"
                        />
                    </div>

                    <div className="input-group">
                        <label>
                            <MapPin size={16} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
                            {t.farmerLocationLabel}
                        </label>
                        <input
                            type="text"
                            value={location}
                            onChange={(e) => setLocation(e.target.value)}
                            placeholder={t.enterLocationPlaceholder}
                            className="premium-input"
                        />
                    </div>

                    {error && <p style={{ color: 'red', marginBottom: '1rem', textAlign: 'center' }}>{error}</p>}

                    <button type="submit" className="btn-primary" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem' }}>
                        {t.nextStepButton} <ArrowRight size={20} />
                    </button>
                </form>
            </motion.div>
        </div>
    );
};

export default FarmerDetails;
