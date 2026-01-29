import React from 'react';
import { motion } from 'framer-motion';
import { translations } from '../i18n';

const Results = ({ result, language }) => {
    if (!result) return null;

    const t = translations[language];
    const perAcre = result.Fertilizer_Quantity_kg_per_acre || 0;
    const landArea = result.landArea || 1;
    const totalQuantity = (perAcre * landArea).toFixed(2);

    return (
        <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="container"
        >
            <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                <h2>{t.resultsTitle}</h2>
                <p className="subtitle">{t.resultsSubtitle}</p>
            </div>

            <div className="glass-panel" style={{ padding: '2rem', marginBottom: '2rem', borderLeft: '8px solid var(--primary)' }}>
                <h3 style={{ color: 'var(--primary-dark)', fontSize: '1.2rem', marginBottom: '0.5rem' }}>{t.smartSuggestion}</h3>
                <p style={{ fontSize: '1.2rem', fontWeight: '500' }}>{result.Suggestion}</p>
            </div>

            {/* FERTILIZER RECOMMENDATION SECTION */}
            <div style={{ marginBottom: '3rem' }}>
                <h3 style={{ color: 'var(--primary-dark)', fontSize: '1.5rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span>🧪</span>
                    {language === 'en' ? 'Recommended Fertilizer' : 'సిఫార్సు చేయబడిన ఎరువు'}
                </h3>

                <div className="result-grid">
                    {/* Fertilizer Type Card */}
                    <motion.div
                        className="glass-panel stat-card"
                        whileHover={{ scale: 1.05 }}
                        style={{ background: 'linear-gradient(135deg, #2F855A 0%, #276749 100%)', color: 'white' }}
                    >
                        <div className="stat-label" style={{ color: 'rgba(255,255,255,0.8)' }}>{t.recommendedFertilizer}</div>
                        <div className="stat-value" style={{ color: 'white', fontSize: '2rem' }}>{result.Recommended_Fertilizer_Type}</div>
                        <div style={{ fontSize: '0.9rem', opacity: 0.9, marginTop: '10px' }}>{t.optimalChoice} {result.Season}</div>
                    </motion.div>

                    {/* Quantity Per Acre Card */}
                    <motion.div className="glass-panel stat-card" whileHover={{ scale: 1.05 }}>
                        <div className="stat-label">{t.applicationQuantity}</div>
                        <div className="stat-value">{perAcre} <span style={{ fontSize: '1rem', color: '#718096' }}>{t.perAcre}</span></div>
                        <p style={{ fontSize: '0.9rem', color: '#718096' }}>{t.applyEvenly}</p>
                    </motion.div>

                    {/* Total Quantity Card */}
                    <motion.div className="glass-panel stat-card" whileHover={{ scale: 1.05 }} style={{ background: 'linear-gradient(135deg, #D69E2E 0%, #B7791F 100%)', color: 'white' }}>
                        <div className="stat-label" style={{ color: 'rgba(255,255,255,0.8)' }}>{t.totalQuantity}</div>
                        <div className="stat-value" style={{ color: 'white' }}>{totalQuantity} <span style={{ fontSize: '1rem', color: 'rgba(255,255,255,0.8)' }}>kg</span></div>
                        <p style={{ fontSize: '0.9rem', color: 'rgba(255,255,255,0.9)' }}>{landArea} {language === 'en' ? 'acres' : 'ఎకరాలు'}</p>
                    </motion.div>

                    {/* Success Prob Card */}
                    <motion.div className="glass-panel stat-card" whileHover={{ scale: 1.05 }}>
                        <div className="stat-label">{t.successProbability}</div>
                        <div className="stat-value">{(result.Crop_Success_Probability * 100).toFixed(0)}%</div>

                        <div className="progress-container">
                            <div
                                className="progress-bar"
                                style={{ width: `${result.Crop_Success_Probability * 100}%` }}
                            ></div>
                        </div>
                        <p style={{ fontSize: '0.9rem', color: '#718096', marginTop: '10px' }}>{t.predictedYield}</p>
                    </motion.div>
                </div>

                {/* Fertilizer Purpose and Additional Info */}
                {result.Fertilizer_Purpose && (
                    <div className="glass-panel" style={{ padding: '1.5rem', marginTop: '1.5rem', borderLeft: '4px solid var(--primary)' }}>
                        <h4 style={{ color: 'var(--primary-dark)', marginBottom: '0.5rem', fontSize: '1.1rem' }}>
                            {language === 'en' ? '📋 Purpose' : '📋 ఉద్దేశ్యం'}
                        </h4>
                        <p style={{ fontSize: '1rem', lineHeight: '1.6' }}>{result.Fertilizer_Purpose}</p>

                        {result.Additional_Fertilizer_Info && (
                            <>
                                <h4 style={{ color: 'var(--primary-dark)', marginTop: '1rem', marginBottom: '0.5rem', fontSize: '1.1rem' }}>
                                    {language === 'en' ? '💡 Additional Information' : '💡 అదనపు సమాచారం'}
                                </h4>
                                <p style={{ fontSize: '0.95rem', lineHeight: '1.6', color: '#4A5568' }}>{result.Additional_Fertilizer_Info}</p>
                            </>
                        )}
                    </div>
                )}
            </div>

            {/* IRRIGATION GUIDANCE SECTION */}
            {result.Irrigation_Method && (
                <div style={{ marginBottom: '3rem' }}>
                    <h3 style={{ color: '#2563EB', fontSize: '1.5rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <span>💧</span>
                        {language === 'en' ? 'Irrigation Guidance' : 'నీటిపారుదల మార్గదర్శకత్వం'}
                    </h3>

                    <div className="result-grid">
                        {/* Irrigation Method Card */}
                        <motion.div
                            className="glass-panel stat-card"
                            whileHover={{ scale: 1.05 }}
                            style={{ background: 'linear-gradient(135deg, #2563EB 0%, #1E40AF 100%)', color: 'white' }}
                        >
                            <div className="stat-label" style={{ color: 'rgba(255,255,255,0.8)' }}>
                                {language === 'en' ? 'Method' : 'పద్ధతి'}
                            </div>
                            <div style={{ fontSize: '1.1rem', fontWeight: '600', marginTop: '10px', lineHeight: '1.4' }}>
                                {result.Irrigation_Method}
                            </div>
                        </motion.div>

                        {/* Irrigation Timing Card */}
                        <motion.div className="glass-panel stat-card" whileHover={{ scale: 1.05 }}>
                            <div className="stat-label">
                                {language === 'en' ? '⏰ Critical Timing' : '⏰ కీలక సమయం'}
                            </div>
                            <p style={{ fontSize: '0.95rem', lineHeight: '1.5', marginTop: '10px' }}>
                                {result.Irrigation_Timing}
                            </p>
                        </motion.div>

                        {/* Irrigation Frequency Card */}
                        <motion.div className="glass-panel stat-card" whileHover={{ scale: 1.05 }}>
                            <div className="stat-label">
                                {language === 'en' ? '📅 Frequency' : '📅 ఫ్రీక్వెన్సీ'}
                            </div>
                            <p style={{ fontSize: '0.95rem', lineHeight: '1.5', marginTop: '10px' }}>
                                {result.Irrigation_Frequency}
                            </p>
                        </motion.div>
                    </div>

                    {/* Irrigation Tips */}
                    <div className="glass-panel" style={{ padding: '1.5rem', marginTop: '1.5rem', borderLeft: '4px solid #2563EB', background: 'linear-gradient(135deg, rgba(37, 99, 235, 0.05) 0%, rgba(30, 64, 175, 0.05) 100%)' }}>
                        <h4 style={{ color: '#1E40AF', marginBottom: '0.5rem', fontSize: '1.1rem' }}>
                            {language === 'en' ? '💡 Water Management Tips' : '💡 నీటి నిర్వహణ చిట్కాలు'}
                        </h4>
                        <p style={{ fontSize: '1rem', lineHeight: '1.6', color: '#1F2937' }}>{result.Irrigation_Tips}</p>
                    </div>
                </div>
            )}

            {/* Soil Health Insights Section */}
            <div style={{ marginTop: '3rem' }}>
                <h3>{t.detailedInsights}</h3>
                <div style={{ marginTop: '1rem' }}>
                    <ul className="insight-list">
                        {result.Insights && result.Insights.length > 0 ? (
                            result.Insights.map((insight, idx) => (
                                <motion.li
                                    key={idx}
                                    className="insight-item"
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: idx * 0.1 }}
                                >
                                    <span style={{ fontSize: '1.2rem' }}>🧪</span>
                                    {insight}
                                </motion.li>
                            ))
                        ) : (
                            <li className="insight-item">{t.healthyRanges}</li>
                        )}
                    </ul>
                </div>
            </div>
        </motion.div>
    );
};

export default Results;
