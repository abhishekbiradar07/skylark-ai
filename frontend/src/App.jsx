import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import ChatPage from './pages/ChatPage';
import { api } from './api';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [stats, setStats] = useState(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const loadStats = async () => {
    try {
      const [health, deals, workOrders, quality] = await Promise.all([
        api.getHealth(),
        api.getDeals(),
        api.getWorkOrders(),
        api.getDataQuality()
      ]);

      setStats({
        totalDeals: deals.total_deals,
        totalWorkOrders: workOrders.total_work_orders,
        dataQuality: Math.round((quality.deals.completeness_score + quality.work_orders.completeness_score) / 2),
        lastRefresh: health.cache_info?.last_refresh,
        dealsQuality: quality.deals,
        workOrdersQuality: quality.work_orders
      });
    } catch (error) {
      console.error('Failed to load stats:', error);
      setStats({
        totalDeals: '—',
        totalWorkOrders: '—',
        dataQuality: '—',
        lastRefresh: null
      });
    }
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);
    try {
      await api.refreshData();
      await loadStats();
    } catch (error) {
      console.error('Refresh failed:', error);
      alert('Failed to refresh data. Please try again.');
    } finally {
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    loadStats();
  }, []);

  const navigateToChat = (query) => {
    setCurrentPage('chat');
    setTimeout(() => {
      window.dispatchEvent(new CustomEvent('quickQuery', { detail: query }));
    }, 100);
  };

  return (
    <div className="app">
      <Header 
        currentPage={currentPage} 
        onNavigate={setCurrentPage}
        onRefresh={handleRefresh}
        isRefreshing={isRefreshing}
      />
      <main className="main-content">
        {currentPage === 'home' && <HomePage stats={stats} onQuickAction={navigateToChat} />}
        {currentPage === 'chat' && <ChatPage />}
      </main>
    </div>
  );
}

export default App;
