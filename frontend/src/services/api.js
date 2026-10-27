import axios from "axios";

export const API_BASE_URL = (
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"
).replace(/\/+$/, "");

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Automatically attach stored JWT Bearer token to authenticated requests
api.interceptors.request.use(
  (config) => {
    try {
      const raw = localStorage.getItem("skillpath_session");
      if (raw) {
        const session = JSON.parse(raw);
        if (session?.token) {
          config.headers.Authorization = `Bearer ${session.token}`;
        }
      }
    } catch {
      // Ignore JSON parse errors
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Resilient port fallback: if connection refused on 8001 or 8000, attempt the alternate port
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    // Network error (no response) and not already retried
    if (!error.response && originalRequest && !originalRequest._retried) {
      const currentUrl = originalRequest.baseURL || api.defaults.baseURL || "";
      let alternateUrl = null;

      if (currentUrl.includes(":8001")) {
        alternateUrl = currentUrl.replace(":8001", ":8000");
      } else if (currentUrl.includes(":8000")) {
        alternateUrl = currentUrl.replace(":8000", ":8001");
      }

      if (alternateUrl) {
        originalRequest._retried = true;
        originalRequest.baseURL = alternateUrl;
        try {
          const res = await axios(originalRequest);
          api.defaults.baseURL = alternateUrl;
          return res;
        } catch (retryError) {
          return Promise.reject(retryError);
        }
      }
    }
    return Promise.reject(error);
  }
);

export async function analyzeStudent(studentData) {
  const formData = new FormData();

  formData.append("name", studentData.name);
  formData.append("cgpa", studentData.cgpa);
  formData.append("target_role", studentData.target_role);
  formData.append("location", studentData.location);
  formData.append("github_url", studentData.github_url);

  formData.append(
    "technical_score",
    studentData.technical_score
  );

  formData.append(
    "aptitude_score",
    studentData.aptitude_score
  );

  formData.append(
    "problem_solving_score",
    studentData.problem_solving_score
  );

  formData.append(
    "communication_score",
    studentData.communication_score
  );

  formData.append(
    "interview_confidence_score",
    studentData.interview_confidence_score
  );

  formData.append("file", studentData.file);

  const response = await api.post(
    "/api/analyze-student",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
}

export default api;