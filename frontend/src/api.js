import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000/api' : 'https://skylark-backend.onrender.com/api');

export const api = {
  async getHealth() {
    const { data } = await axios.get(`${API_BASE}/health`);
    return data;
  },

  async refreshData() {
    const { data } = await axios.post(`${API_BASE}/refresh`);
    return data;
  },

  async getDeals() {
    const { data } = await axios.get(`${API_BASE}/data/deals`);
    return data;
  },

  async getWorkOrders() {
    const { data } = await axios.get(`${API_BASE}/data/work-orders`);
    return data;
  },

  async getDataQuality() {
    const { data } = await axios.get(`${API_BASE}/data-quality`);
    return data;
  },

  async chat(message) {
    const { data } = await axios.post(`${API_BASE}/chat`, { message });
    return data;
  }
};
