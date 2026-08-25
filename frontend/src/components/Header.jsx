import React from 'react';

const Header = ({ currentPage, onNavigate, onRefresh, isRefreshing }) => {
  return (
    <header className="header">
      <div className="header-container">
        <div className="header-left">
          <div className="logo">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <rect width="32" height="32" rx="6" fill="url(#gradient)"/>
              <path d="M16 8L22 13L16 18L10 13L16 8Z" fill="white" opacity="0.9"/>
              <path d="M16 14L22 19L16 24L10 19L16 14Z" fill="white" opacity="0.6"/>
              <defs>
                <linearGradient id="gradient" x1="0" y1="0" x2="32" y2="32">
                  <stop offset="0%" stopColor="#FF3621"/>
                  <stop offset="100%" stopColor="#FF8A3C"/>
                </linearGradient>
              </defs>
            </svg>
            <span className="logo-text">Skylark</span>
            <span className="logo-subtitle">Business Intelligence</span>
          </div>
        </div>

        <nav className="header-nav">
          <button 
            className={`nav-btn ${currentPage === 'home' ? 'active' : ''}`}
            onClick={() => onNavigate('home')}
          >
            Dashboard
          </button>
          <button 
            className={`nav-btn ${currentPage === 'chat' ? 'active' : ''}`}
            onClick={() => onNavigate('chat')}
          >
            AI Assistant
          </button>
        </nav>

        <div className="header-right">
          <button 
            className={`refresh-btn-header ${isRefreshing ? 'loading' : ''}`}
            onClick={onRefresh}
            disabled={isRefreshing}
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
              <path d="M13.65 2.35C12.2 0.9 10.21 0 8 0 3.58 0 0 3.58 0 8s3.58 8 8 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L9 7h7V0l-2.35 2.35z"/>
            </svg>
            {isRefreshing ? 'Syncing...' : 'Sync Data'}
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
