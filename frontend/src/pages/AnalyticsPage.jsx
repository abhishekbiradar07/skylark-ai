import React, { useState, useEffect } from 'react';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { api } from '../api';

const COLORS = ['#FF3621', '#FF8A3C', '#FFB84D', '#00C9A7', '#00B8D4', '#7B61FF'];

const AnalyticsPage = () => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      // Fetch data by asking questions
      const [pipeline, operations, billing, sectors] = await Promise.all([
        api.chat("What's our pipeline summary?"),
        api.chat("Show me operations summary"),
        api.chat("What's the billing status?"),
        api.chat("Compare pipeline and execution by sector")
      ]);

      setAnalyticsData({
        pipeline: pipeline.metrics,
        operations: operations.metrics,
        billing: billing.metrics,
        sectors: sectors.metrics
      });
    } catch (error) {
      console.error('Failed to load analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="analytics-page">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading analytics...</p>
        </div>
      </div>
    );
  }

  // Transform data for charts
  const pipelineBySector = analyticsData?.sectors?.by_sector?.map(s => ({
    name: s.sector,
    pipeline: s.deals?.pipeline || 0,
    deals: s.deals?.count || 0
  })) || [];

  const operationsBySector = analyticsData?.sectors?.by_sector?.map(s => ({
    name: s.sector,
    billed: s.work_orders?.billed || 0,
    workOrders: s.work_orders?.count || 0
  })) || [];

  const billingData = [
    { name: 'Billed', value: analyticsData?.billing?.billing?.total_billed || 0 },
    { name: 'Collected', value: analyticsData?.billing?.billing?.total_collected || 0 },
    { name: 'Outstanding', value: analyticsData?.billing?.billing?.outstanding || 0 }
  ];

  const sectorHealthData = analyticsData?.sectors?.sector_health?.map(s => ({
    name: s.sector,
    pipeline: s.deals?.pipeline || 0,
    execution: s.work_orders?.billed || 0,
    health: s.health
  })) || [];

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <h2>Analytics Dashboard</h2>
        <button className="refresh-btn-small" onClick={loadAnalytics}>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path d="M13.65 2.35C12.2 0.9 10.21 0 8 0 3.58 0 0 3.58 0 8s3.58 8 8 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L9 7h7V0l-2.35 2.35z"/>
          </svg>
          Refresh
        </button>
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h3>Pipeline by Sector</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={pipelineBySector}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" />
              <XAxis dataKey="name" stroke="#888" />
              <YAxis stroke="#888" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}
                formatter={(value) => `₹${(value / 1000000).toFixed(2)}M`}
              />
              <Legend />
              <Bar dataKey="pipeline" fill="#FF3621" name="Pipeline (₹)" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3>Operations by Sector</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={operationsBySector}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" />
              <XAxis dataKey="name" stroke="#888" />
              <YAxis stroke="#888" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}
                formatter={(value) => `₹${(value / 1000000).toFixed(2)}M`}
              />
              <Legend />
              <Bar dataKey="billed" fill="#00C9A7" name="Billed (₹)" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3>Billing Overview</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={billingData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {billingData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `₹${(value / 1000000).toFixed(2)}M`} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3>Sector Health Matrix</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={sectorHealthData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" />
              <XAxis dataKey="name" stroke="#888" />
              <YAxis stroke="#888" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}
                formatter={(value) => `₹${(value / 1000000).toFixed(2)}M`}
              />
              <Legend />
              <Bar dataKey="pipeline" fill="#FF3621" name="Pipeline" />
              <Bar dataKey="execution" fill="#00C9A7" name="Execution" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage;
