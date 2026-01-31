import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, GraduationCap, MapPin, Award, ChevronRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { translations } from '../i18n';

const Home = ({ language }) => {
    const navigate = useNavigate();
    const t = translations[language];

    return (
        <div className="home-container" style={{ padding: '2rem', display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="glass-panel"
                onClick={() => navigate('/farmer-details')}
                style={{
                    maxWidth: '900px',
                    width: '100%',
                    padding: '3rem',
                    cursor: 'pointer',
                    position: 'relative',
                    overflow: 'hidden'
                }}
            >
                {/* Click Hint Overlay */}
                <div className="click-hint" style={{
                    position: 'absolute',
                    top: '1rem',
                    right: '1rem',
                    background: 'rgba(47, 133, 90, 0.1)',
                    color: 'var(--primary)',
                    padding: '0.5rem 1rem',
                    borderRadius: '20px',
                    fontSize: '0.8rem',
                    fontWeight: '600',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                }}>
                    {t.clickToStart} <ChevronRight size={16} />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '3rem', alignItems: 'center' }}>

                    {/* Left Side: Team & Info */}
                    <div>
                        <div style={{ marginBottom: '2rem' }}>
                            <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: 'var(--primary-dark)' }}>Project Team</h2>
                            <p style={{ lineHeight: '1.6', fontSize: '1.1rem', color: 'var(--text-main)', marginBottom: '1.5rem' }}>
                                “{t.homeDescription}”
                            </p>
                        </div>

                        <div style={{ marginBottom: '2rem' }}>
                            <h3 style={{ fontSize: '1.2rem', marginBottom: '1rem', color: 'var(--primary)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                <Users size={20} /> {t.teamMembersTitle}
                            </h3>
                            <ul style={{ listStyle: 'none', paddingLeft: '1rem', borderLeft: '3px solid var(--accent)' }}>
                                <li style={{ marginBottom: '0.5rem', fontSize: '1.1rem' }}>{t.teamMember1}</li>
                                <li style={{ marginBottom: '0.5rem', fontSize: '1.1rem' }}>{t.teamMember2}</li>
                                <li style={{ fontSize: '1.1rem' }}>{t.teamMember3}</li>
                            </ul>
                        </div>

                        <div>
                            <p style={{ fontWeight: '700', fontSize: '1.2rem', color: 'var(--primary-dark)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                <GraduationCap size={24} /> {t.instituteName}
                            </p>
                        </div>
                    </div>

                    {/* Right Side: Mentor & Branding */}
                    <div style={{
                        background: 'rgba(255, 255, 255, 0.5)',
                        padding: '2rem',
                        borderRadius: '20px',
                        textAlign: 'center',
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        height: '100%'
                    }}>
                        <div style={{ marginBottom: '2rem' }}>
                            <Award size={48} color="var(--accent)" style={{ marginBottom: '1rem' }} />
                            <h3 style={{ fontSize: '1.5rem', color: 'var(--primary-dark)', marginBottom: '0.5rem' }}>{t.mentorDetailsTitle}</h3>
                            <p style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{t.mentorName}</p>
                            <p style={{ color: 'var(--text-light)', marginBottom: '0.5rem' }}>{t.mentorRole}</p>
                            <p style={{ fontSize: '0.9rem', color: 'var(--primary)' }}>{t.mentorOrg}</p>
                        </div>
                    </div>
                </div>

            </motion.div>
        </div>
    );
};

export default Home;
