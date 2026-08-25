import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { api } from '../api';

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const handleQuickQuery = (event) => {
      const query = event.detail;
      if (query) {
        handleSend(query);
      }
    };

    window.addEventListener('quickQuery', handleQuickQuery);
    return () => window.removeEventListener('quickQuery', handleQuickQuery);
  }, []);

  const handleSend = async (message = input) => {
    if (!message.trim() || isLoading) return;

    const userMessage = { role: 'user', content: message };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await api.chat(message);
      
      const assistantMessage = {
        role: 'assistant',
        content: response.answer,
        metadata: {
          intent: response.intent,
          dataSources: response.data_sources,
          dataQuality: response.data_quality
        }
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: 'I encountered an error processing your request. Please try again or rephrase your question.',
        error: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const suggestedQueries = [
    "What's our total pipeline by sector?",
    "Show me top 10 deals by value",
    "What's the billing and collection status?",
    "Compare pipeline and execution across sectors"
  ];

  return (
    <div className="chat-page-new">
      <div className="chat-container-new">
        <div className="chat-messages-new">
          {messages.length === 0 ? (
            <div className="chat-welcome">
              <div className="welcome-header">
                <h2>AI Business Intelligence Assistant</h2>
                <p>Ask me anything about your deals, work orders, and business metrics. I'll provide insights based on your Monday.com data.</p>
              </div>
              
              <div className="suggested-queries-grid">
                <h3>Try asking:</h3>
                <div className="suggestions">
                  {suggestedQueries.map((query, index) => (
                    <button
                      key={index}
                      className="suggestion-btn"
                      onClick={() => handleSend(query)}
                    >
                      {query}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <>
              {messages.map((msg, index) => (
                <div key={index} className={`message-new ${msg.role}`}>
                  <div className="message-header-new">
                    <span className="message-sender">{msg.role === 'user' ? 'You' : 'AI Assistant'}</span>
                  </div>
                  <div className="message-body">
                    <ReactMarkdown
                      components={{
                        table: ({node, ...props}) => (
                          <div className="table-wrapper">
                            <table {...props} />
                          </div>
                        )
                      }}
                    >
                      {msg.content}
                    </ReactMarkdown>
                    {msg.metadata?.dataSources && msg.metadata.dataSources.length > 0 && (
                      <div className="message-sources">
                        <strong>Data Sources:</strong> {msg.metadata.dataSources.join(', ')}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="message-new assistant">
                  <div className="message-header-new">
                    <span className="message-sender">AI Assistant</span>
                  </div>
                  <div className="message-body">
                    <div className="typing-indicator-new">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
            </>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-area">
          <div className="chat-input-wrapper-new">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question about your business data..."
              rows="1"
              disabled={isLoading}
            />
            <button
              className="send-btn-new"
              onClick={() => handleSend()}
              disabled={!input.trim() || isLoading}
            >
              <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                <path d="M2 2l16 8-16 8V2zm2 6v4l8-2-8-2z"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
