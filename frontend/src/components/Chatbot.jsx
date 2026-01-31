
import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import './Chatbot.css';
import { translations } from '../i18n';

const Chatbot = ({ language }) => {
    const [isOpen, setIsOpen] = useState(false);
    // REMOVED local chatLanguage state. Strictly use prop 'language'.
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [isListening, setIsListening] = useState(false);
    const messagesEndRef = useRef(null);

    const t = translations[language] || translations['en'];

    // Initialize welcome message when chatbot opens
    useEffect(() => {
        if (isOpen && messages.length === 0) {
            setMessages([{ type: 'bot', text: t.chatbotWelcome }]);
        }
    }, [isOpen, t.chatbotWelcome]); // Added t.chatbotWelcome to dependency array for completeness

    // Update messages when language changes
    useEffect(() => {
        if (messages.length > 0 && messages[0].type === 'bot') {
            setMessages(prev => [
                { type: 'bot', text: t.chatbotWelcome },
                ...prev.slice(1)
            ]);
        }
    }, [language, t.chatbotWelcome]); // Changed dependency from chatLanguage to language

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isOpen]);

    // Voice Support - Speech Recognition
    const startListening = () => {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert("Voice input is not supported in this browser. Please use Chrome or Edge.");
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();

        // STRICT: Use the selected language for voice recognition
        recognition.lang = language === 'te' ? 'te-IN' : 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
            setIsListening(true);
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            setInput(transcript);
            // Auto-send after voice input
            handleSend(transcript);
        };

        recognition.onerror = (event) => {
            console.error("Speech recognition error", event.error);
            setIsListening(false);
        };

        recognition.onend = () => {
            setIsListening(false);
        };

        recognition.start();
    };

    // Voice Support - Text to Speech
    const speakResponse = (text, lang) => {
        if (!('speechSynthesis' in window)) return;

        // Cancel current speech if any
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        // STRICT: Use the passed language for speech synthesis
        utterance.lang = lang === 'te' ? 'te-IN' : 'en-US';

        // Adjust rate/pitch for better "farmer-friendly" tone
        utterance.rate = 0.9;
        utterance.pitch = 1.0;

        window.speechSynthesis.speak(utterance);
    };

    const handleSend = async (manualInput = null) => {
        const textToSend = manualInput || input;
        if (!textToSend.trim()) return;

        const userMessage = { type: 'user', text: textToSend };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsTyping(true);

        // STRICT: Always send the selected language, ignoring auto-detection or mismatched input scripts
        const requestLanguage = language;

        try {
            const response = await axios.post('http://localhost:8000/chat', {
                query: textToSend,
                language: requestLanguage
            });

            const botReply = response.data.reply;
            const botMessage = { type: 'bot', text: botReply };

            setMessages(prev => [...prev, botMessage]);

            // Speak the response
            speakResponse(botReply, requestLanguage);

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
                                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                    <h3 style={{ margin: 0 }}>{t.chatbotTitle}</h3>
                                    {isListening && <span className="listening-indicator">🔴 Listening...</span>}
                                </div>
                                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
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
                                    <div className={`message ${msg.type} `}>
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
                            <button
                                className={`voice - btn ${isListening ? 'listening' : ''} `}
                                onClick={startListening}
                                title="Speak"
                            >
                                {isListening ? '⏹️' : '🎤'}
                            </button>
                            <input
                                className="chat-input"
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                                placeholder={language === 'te' ? 'టైప్ చేయండి లేదా మాట్లాడండి...' : t.chatPlaceholder}
                            />
                            <button className="chat-send-btn" onClick={() => handleSend()}>
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
