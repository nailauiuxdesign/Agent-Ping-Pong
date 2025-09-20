import type { User } from "types";

const API_BASE_URL = 'http://localhost:8000';

interface ApiResponse<T = any> {
  data: T;
  message?: string;
}

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchWithAuth(url: string, options: RequestInit = {}): Promise<Response> {
  const token = localStorage.getItem('auth_token');
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.text();
    let errorMessage = 'An error occurred';
    
    try {
      const errorData = JSON.parse(error);
      errorMessage = errorData.message || errorData.detail || errorMessage;
    } catch {
      errorMessage = error || `HTTP ${response.status}`;
    }
    
    throw new ApiError(response.status, errorMessage);
  }

  return response;
}

// Auth API
export async function login(credentials: { email: string; password: string }) {
  const response = await fetchWithAuth('/auth/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  });
  return response.json();
}

export async function register(userData: {
  full_name: string;
  email: string;
  password: string;
}) {
  const response = await fetchWithAuth('/auth/signup', {
    method: 'POST',
    body: JSON.stringify(userData),
  });
  return response.json();
}

export async function logout() {
  const response = await fetchWithAuth('/auth/logout', {
    method: 'POST',
  });
  return response.json();
}

export async function fetchUser() {
  const response = await fetchWithAuth('/user/me');
  return response.json();
}

export async function updateUser(userData: Partial<User>) {
  const response = await fetchWithAuth('/user/me', {
    method: 'PUT',
    body: JSON.stringify(userData),
  });
  return response.json();
}

// Podcast API
export async function fetchPodcasts() {
  const response = await fetchWithAuth('/podcasts');
  return response.json();
}

export async function createPodcast(podcastData: {
  rss_feed_url: string;
  title?: string;
  description?: string;
}) {
  const response = await fetchWithAuth('/podcasts', {
    method: 'POST',
    body: JSON.stringify(podcastData),
  });
  return response.json();
}

export async function validateRssFeed(url: string) {
  const response = await fetchWithAuth('/podcasts/validate-rss', {
    method: 'POST',
    body: JSON.stringify({ url }),
  });
  return response.json();
}

// Translation API
export async function fetchTranslations() {
  const response = await fetchWithAuth('/translations');
  return response.json();
}

export async function createTranslation(data: {
  podcast_id: number;
  target_languages: string[];
}) {
  const response = await fetchWithAuth('/translations', {
    method: 'POST',
    body: JSON.stringify(data),
  });
  return response.json();
}

// File Upload API
export async function uploadVoiceSample(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  const token = localStorage.getItem('auth_token');
  const response = await fetch(`${API_BASE_URL}/upload/voice-sample`, {
    method: 'POST',
    headers: {
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    body: formData,
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || 'Upload failed');
  }

  return response.json();
}