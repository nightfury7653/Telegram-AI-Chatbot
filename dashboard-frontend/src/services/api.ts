// src/services/api.ts

// Define types for our API responses
export interface SentimentDistribution {
    _id: string;
    count: number;
  }
  
  export interface DailyMessage {
    _id: string;
    count: number;
  }
  
  export interface AnalyticsData {
    total_users: number;
    total_messages: number;
    sentiment_distribution: SentimentDistribution[];
    daily_messages: DailyMessage[];
  }
  
  // Configuration object for API settings
  const API_CONFIG = {
    BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
    HEADERS: {
      'Content-Type': 'application/json',
    },
  };
  
  // Generic error handler
  class APIError extends Error {
    constructor(message: string, public status?: number) {
      super(message);
      this.name = 'APIError';
    }
  }
  
  // Generic fetch wrapper with error handling
  async function fetchWrapper<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${endpoint}`, {
        ...options,
        headers: {
          ...API_CONFIG.HEADERS,
          ...options.headers,
        },
      });
  
      if (!response.ok) {
        throw new APIError(`API Error: ${response.statusText}`, response.status);
      }
  
      return await response.json();
    } catch (error) {
      if (error instanceof APIError) {
        throw error;
      }
      throw new APIError(`Network Error: ${(error as Error).message}`);
    }
  }
  
  // API methods
  export const analyticsAPI = {
    // Get all analytics data
    getAnalytics: () => fetchWrapper<AnalyticsData>('/analytics'),
  
    // Get specific date range analytics
    getAnalyticsRange: (startDate: string, endDate: string) =>
      fetchWrapper<AnalyticsData>(`/analytics/range?start=${startDate}&end=${endDate}`),
  
    // Get sentiment distribution
    getSentimentDistribution: () =>
      fetchWrapper<SentimentDistribution[]>('/analytics/sentiment'),
  
    // Get daily message counts
    getDailyMessages: () => fetchWrapper<DailyMessage[]>('/analytics/messages/daily'),
  
    // Get total user count
    getTotalUsers: () => fetchWrapper<{ total_users: number }>('/analytics/users/total'),
  };