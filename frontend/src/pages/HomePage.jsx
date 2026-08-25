import React from 'react';

const HomePage = ({ stats, onQuickAction }) => {
  const quickActions = [
    {
      title: 'Leadership Update',
      description: 'Comprehensive business overview with key metrics and insights',
      query: 'Give me a leadership update'
    },
    {
      title: 'Pipeline Summary',
      description: 'View active deals, opportunities, and sales forecast',
      query: "What's our pipeline summary?"
    },
    {
      title: 'Operations Status',
      description: 'Check work order execution and delivery status',
      query: 'Show me operations status'
    },
    {
      title: 'Billing & Collections',
      description: 'Track revenue, payments, and outstanding amounts',
      query: 'How is billing and collection?'
    }
  ];

  const formatLastRefresh = (timestamp) => {
    if (!timestamp) return 'Not synced';
    const date = new Date(timestamp);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000 / 60);
    if (diff < 1) return 'Just now';
    if (diff < 60) return `${diff}m ago`;
    return date.toLocaleTimeString();
  };

  return (
    <div className="home-page">
      <div className="home-hero">
        <h1 className="hero-title">Business Intelligence Dashboard</h1>
        <p className="hero-subtitle">Real-time insights from your Monday.com data powered by AI</p>
      </div>

      <div className="stats-overview">
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-label">Total Deals</span>
            <div className="stat-badge deals">Pipeline</div>
          </div>
          <p className="stat-value">{stats?.totalDeals ?? '—'}</p>
          <div className="stat-footer">Active opportunities</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-label">Work Orders</span>
            <div className="stat-badge operations">Operations</div>
          </div>
          <p className="stat-value">{stats?.totalWorkOrders ?? '—'}</p>
          <div className="stat-footer">In progress</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-label">Data Quality</span>
            <div className="stat-badge quality">Health</div>
          </div>
          <p className="stat-value">{stats?.dataQuality ? `${stats.dataQuality}%` : '—'}</p>
          <div className="stat-footer">Completeness score</div>
        </div>
        
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-label">Last Sync</span>
            <div className="stat-badge sync">Status</div>
          </div>
          <p className="stat-value-small">{formatLastRefresh(stats?.lastRefresh)}</p>
          <div className="stat-footer">Data freshness</div>
        </div>
      </div>

      <div className="section">
        <h2 className="section-title">Quick Actions</h2>
        <p className="section-subtitle">Get instant answers to common business questions</p>
        
        <div className="actions-grid">
          {quickActions.map((action, index) => (
            <button 
              key={index}
              className="action-card-new"
              onClick={() => onQuickAction(action.query)}
            >
              <h3>{action.title}</h3>
              <p>{action.description}</p>
              <div className="action-arrow">→</div>
            </button>
          ))}
        </div>
      </div>

      <div className="section">
        <h2 className="section-title">Platform Capabilities</h2>
        <div className="features-grid-new">
          <div className="feature-card-new">
            <div className="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
            </div>
            <h3>Natural Language Queries</h3>
            <p>Ask questions in plain English and receive instant, contextual insights from your business data</p>
          </div>
          
          <div className="feature-card-new">
            <div className="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="3" width="7" height="7"/>
                <rect x="14" y="3" width="7" height="7"/>
                <rect x="14" y="14" width="7" height="7"/>
                <rect x="3" y="14" width="7" height="7"/>
              </svg>
            </div>
            <h3>Automated Analytics</h3>
            <p>Intelligent calculations across pipeline, operations, and billing with real-time updates</p>
          </div>
          
          <div className="feature-card-new">
            <div className="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
              </svg>
            </div>
            <h3>Data Quality Monitoring</h3>
            <p>Continuous assessment of data completeness with actionable recommendations for improvement</p>
          </div>
          
          <div className="feature-card-new">
            <div className="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 20V10M6 20V4M18 20v-7"/>
              </svg>
            </div>
            <h3>Executive Insights</h3>
            <p>Strategic recommendations and opportunity identification based on comprehensive data analysis</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
