
import React, { useState } from 'react';
import styles from './chatkit.module.css';

const Chatbot = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const toggleChat = () => {
        setIsOpen(!isOpen);
    };

    const sendMessage = async () => {
        if (input.trim() === '') return;

        const userMessage = { sender: 'user', text: input };
        setMessages((prevMessages) => [...prevMessages, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            // Use environment variable for API endpoint, fallback to localhost
            const apiEndpoint = process.env.REACT_APP_RAG_API_URL || 'http://127.0.0.1:8000/query';

            // Call the RAG API with the query only
            const response = await fetch(apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: input
                }),
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();
            const botMessage = {
                sender: 'bot',
                text: data.answer || data.response || 'Sorry, I could not process your request.'
            };
            setMessages((prevMessages) => [...prevMessages, botMessage]);
        } catch (error) {
            console.error('Error sending message:', error);

            // Provide a more user-friendly error message based on the type of error
            let errorMessageText = 'Sorry, an error occurred.';

            if (error.message.includes('Failed to fetch')) {
                errorMessageText = 'Sorry, an error occurred: Could not connect to the chatbot service. Please make sure the backend server is running on http://127.0.0.1:8000.';
            } else {
                errorMessageText = `Sorry, an error occurred: ${error.message || 'Something went wrong.'}`;
            }

            const errorMessage = {
                sender: 'bot',
                text: errorMessageText
            };
            setMessages((prevMessages) => [...prevMessages, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    };

    return (
        <div className={styles.chatContainer}>
            <button className={styles.chatIcon} onClick={toggleChat}>
                💬
            </button>

            {isOpen && (
                <div className={styles.chatWindow}>
                    <div className={styles.chatHeader}>
                        <h3>Chatbot</h3>
                        <button onClick={toggleChat}>X</button>
                    </div>
                    <div className={styles.chatMessages}>
                        {messages.map((msg, index) => (
                            <div key={index} className={`${styles.message} ${styles[msg.sender]}`}>
                                {msg.text}
                            </div>
                        ))}
                        {isLoading && (
                            <div className={`${styles.message} ${styles.bot}`}>
                                <div className={styles.typingIndicator}>
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        )}
                    </div>
                    <div className={styles.chatInput}>
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Ask a question..."
                            disabled={isLoading}
                        />
                        <button onClick={sendMessage} disabled={isLoading}>Send</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Chatbot;
