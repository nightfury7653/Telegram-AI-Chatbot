import React, { useState, useEffect, useCallback } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { PieChart, Pie, Cell } from 'recharts';
import { Users, MessageSquare, TrendingUp, RefreshCw } from 'lucide-react';

interface SentimentDistribution {
  _id: string;
  count: number;
}

interface DailyMessage {
  _id: string;
  count: number;
}

interface AnalyticsData {
  total_users: number;
  total_messages: number;
  sentiment_distribution: SentimentDistribution[];
  daily_messages: DailyMessage[];
}

const COLORS = ['#4ade80', '#f87171', '#60a5fa'];
const API_URL = (import.meta.env.VITE_API_URL as string) || 'http://localhost:5000/api';
const MAX_RETRIES = 3;
const RETRY_DELAY = 2000; // 2 seconds

interface StatCardProps {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  value: number;
  className?: string;
}

const StatCard = ({ icon: Icon, title, value, className = "" }: StatCardProps) => (
  <div className={`bg-white rounded-lg shadow p-6 text-center ${className}`}>
    <Icon className="w-8 h-8 mx-auto mb-2" />
    <p className="text-gray-600 font-medium">{title}</p>
    <h3 className="text-2xl font-bold">{value?.toLocaleString() || '0'}</h3>
  </div>
);

const AnalyticsDashboard = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  const fetchData = useCallback(async (retryAttempt = 0) => {
    try {
      setLoading(true);
      setError(null);

      // First check API health
      const healthCheck = await fetch(`${API_URL}/health`).catch(() => null);
      if (!healthCheck?.ok) {
        throw new Error('API service is not available');
      }

      const response = await fetch(`${API_URL}/analytics`);
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `Server error: ${response.status}`);
      }
      
      const analyticsData = await response.json();
      
      // Validate data structure
      if (!analyticsData || typeof analyticsData !== 'object') {
        throw new Error('Invalid data format received');
      }
      
      // Ensure daily messages are sorted by date
      analyticsData.daily_messages = (analyticsData.daily_messages || []).sort(
        (a: DailyMessage, b: DailyMessage) => 
          new Date(a._id).getTime() - new Date(b._id).getTime()
      );

      setData(analyticsData);
      setRetryCount(0); // Reset retry count on success
    } catch (err) {
      console.error('Error fetching analytics:', err);
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      
      if (retryAttempt < MAX_RETRIES) {
        setError(`${errorMessage} - Retrying... (${retryAttempt + 1}/${MAX_RETRIES})`);
        setTimeout(() => {
          fetchData(retryAttempt + 1);
        }, RETRY_DELAY);
      } else {
        setError(`${errorMessage} - Max retries reached. Please try again later.`);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();

    // Refresh data every 5 minutes if no errors
    const interval = setInterval(() => {
      if (!error) {
        fetchData();
      }
    }, 5 * 60 * 1000);

    return () => clearInterval(interval);
  }, [fetchData, error]);

  const handleManualRefresh = () => {
    fetchData();
  };

  if (loading && !data) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Loading analytics data...</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">No analytics data available</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Bot Analytics Dashboard</h1>
        <button
          onClick={handleManualRefresh}
          className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded hover:bg-gray-200"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <StatCard
          icon={Users}
          title="Total Users"
          value={data.total_users}
          className="text-blue-600"
        />
        <StatCard
          icon={MessageSquare}
          title="Total Messages"
          value={data.total_messages}
          className="text-green-600"
        />
        <StatCard
          icon={TrendingUp}
          title="Avg Messages/Day"
          value={Math.round(data.total_messages / (data.daily_messages?.length || 30))}
          className="text-yellow-600"
        />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Message Volume Trend</h2>
          <div className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data.daily_messages}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="_id" 
                  tickFormatter={(value) => {
                    try {
                      return new Date(value).toLocaleDateString();
                    } catch (e) {
                      return value;
                    }
                  }}
                />
                <YAxis />
                <Tooltip 
                  labelFormatter={(value) => {
                    try {
                      return new Date(value).toLocaleDateString();
                    } catch (e) {
                      return value;
                    }
                  }}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="count" 
                  stroke="#8884d8" 
                  name="Messages"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Sentiment Distribution</h2>
          <div className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data.sentiment_distribution}
                  cx="50%"
                  cy="50%"
                  outerRadius={120}
                  dataKey="count"
                  nameKey="_id"
                  label={({ name, percent }) => 
                    `${name} (${(percent * 100).toFixed(0)}%)`
                  }
                >
                  {data.sentiment_distribution.map((entry, index) => (
                    <Cell 
                      key={`cell-${index}`} 
                      fill={COLORS[index % COLORS.length]} 
                    />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;