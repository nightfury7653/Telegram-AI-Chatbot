// src/api/analytics.ts
export async function fetchAnalyticsData() {
    try {
      const response = await fetch('http://localhost:5000/api/analytics');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching analytics:', error);
      throw error;
    }
  }