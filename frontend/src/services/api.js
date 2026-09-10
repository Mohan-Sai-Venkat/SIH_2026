import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:4040/api";

export const DEMO_MODE =
  import.meta.env.VITE_DEMO_MODE === "true";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getDashboardData = async () => {
  const response = await api.get("/dashboard");
  return response.data;
};

export const getMaintenanceTasks = async () => {
  const response = await api.get("/maintenance");
  return response.data;
};

export const getCorridors = async () => {
  const response = await api.get("/corridors");
  return response.data;
};

export const getWeeklyPlan = async () => {
  const response = await api.get("/plans/weekly");
  return response.data;
};

export const getMonthlyPlan = async () => {
  const response = await api.get("/plans/monthly");
  return response.data;
};

export const getAIInsights = async () => {
  const response = await api.get("/ai/insights");
  return response.data;
};

export const generateAIBlockPlan = async (data) => {
  const response = await api.post("/ai/block-plan", data);
  return response.data;
};

export const checkBackendHealth = async () => {
  const response = await api.get("/health");
  return response.data;
};

export default api;
