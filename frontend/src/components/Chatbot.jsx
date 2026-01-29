import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import './Chatbot.css';
import { translations } from '../i18n';

const Chatbot = ({ language: appLanguage }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [chatLanguage, setChatLanguage] = useState(appLanguage || 'en');
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef(null);

    const t = translations[chatLanguage];

    // Initialize welcome message when chatbot opens
    useEffect(() => {
        if (isOpen && messages.length === 0) {
            setMessages([{ type: 'bot', text: t.chatbotWelcome }]);
        }
    }, [isOpen]);

    // Update welcome message when language changes
    useEffect(() => {
        if (messages.length > 0 && messages[0].type === 'bot') {
            setMessages(prev => [
                { type: 'bot', text: t.chatbotWelcome },
                ...prev.slice(1)
            ]);
        }
    }, [chatLanguage]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isOpen]);

    const detectGreeting = (text) => {
        const lower = text.toLowerCase().trim();

        // English greetings
        if (lower === 'hi' || lower === 'hello' || lower === 'hey' || lower === 'namaste') {
            return chatLanguage === 'en' ? t.greetingHi : t.greetingHi;
        }

        // Thanks
        if (lower.includes('thank') || lower.includes('thanks') || lower === 'dhanyavad' || lower.includes('ధన్యవాద')) {
            return chatLanguage === 'en' ? t.greetingThanks : t.greetingThanks;
        }

        // Telugu greetings
        if (lower.includes('హలో') || lower.includes('నమస్కారం')) {
            return t.greetingHi;
        }

        return null;
    };

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = { type: 'user', text: input };
        setMessages(prev => [...prev, userMessage]);
        const userInput = input;
        setInput('');
        setIsTyping(true);

        // Check for greetings first
        const greetingResponse = detectGreeting(userInput);
        if (greetingResponse) {
            setTimeout(() => {
                setMessages(prev => [...prev, { type: 'bot', text: greetingResponse }]);
                setIsTyping(false);
            }, 500);
            return;
        }

        try {
            const response = await axios.post('http://localhost:8000/chat', {
                query: userInput,
                language: chatLanguage
            });
            const botMessage = { type: 'bot', text: response.data.reply };
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, { type: 'bot', text: t.chatError }]);
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <>
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        className="chatbot-window"
                        initial={{ opacity: 0, y: 20, scale: 0.9 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 20, scale: 0.9 }}
                    >
                        <div className="chat-header">
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <h3 style={{ margin: 0 }}>{t.chatbotTitle}</h3>
                                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                                    <button
                                        onClick={() => setChatLanguage('en')}
                                        style={{
                                            padding: '0.3rem 0.6rem',
                                            borderRadius: '6px',
                                            border: chatLanguage === 'en' ? '2px solid white' : '2px solid rgba(255,255,255,0.3)',
                                            background: chatLanguage === 'en' ? 'white' : 'transparent',
                                            color: chatLanguage === 'en' ? 'var(--primary)' : 'white',
                                            cursor: 'pointer',
                                            fontWeight: '600',
                                            fontSize: '0.75rem'
                                        }}
                                    >
                                        EN
                                    </button>
                                    <button
                                        onClick={() => setChatLanguage('te')}
                                        style={{
                                            padding: '0.3rem 0.6rem',
                                            borderRadius: '6px',
                                            border: chatLanguage === 'te' ? '2px solid white' : '2px solid rgba(255,255,255,0.3)',
                                            background: chatLanguage === 'te' ? 'white' : 'transparent',
                                            color: chatLanguage === 'te' ? 'var(--primary)' : 'white',
                                            cursor: 'pointer',
                                            fontWeight: '600',
                                            fontSize: '0.75rem'
                                        }}
                                    >
                                        తెలుగు
                                    </button>
                                    <button
                                        onClick={() => setIsOpen(false)}
                                        style={{ background: 'none', border: 'none', color: 'white', cursor: 'pointer', fontSize: '1.2rem', marginLeft: '0.5rem' }}
                                    >✕</button>
                                </div>
                            </div>
                        </div>

                        <div className="chat-messages">
                            {messages.map((msg, idx) => (
                                <div
                                    key={idx}
                                    style={{
                                        alignSelf: msg.type === 'user' ? 'flex-end' : 'flex-start',
                                        maxWidth: '80%'
                                    }}
                                >
                                    <div className={`message ${msg.type}`}>
                                        {msg.text}
                                    </div>
                                </div>
                            ))}
                            {isTyping && (
                                <div className="typing-indicator">
                                    <div className="dot"></div>
                                    <div className="dot"></div>
                                    <div className="dot"></div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        <div className="chat-input-area">
                            <input
                                className="chat-input"
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                                placeholder={t.chatPlaceholder}
                            />
                            <button className="chat-send-btn" onClick={handleSend}>
                                ➤
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <motion.button
                className="chatbot-fab"
                onClick={() => setIsOpen(!isOpen)}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
            >
                {isOpen ? '✕' : '💬'}
            </motion.button>
        </>
    );
};

export default Chatbot;
