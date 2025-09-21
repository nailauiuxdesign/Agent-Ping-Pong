import React, { createContext, useContext, useReducer, useEffect, type ReactNode } from 'react';
import { appReducer, initialState } from 'reducers/appReducer';
import type { AppState, User } from '../types';
import * as api from '../services/api';

interface AppContextType {
  state: AppState;
  dispatch: React.Dispatch<any>;
  // Action creators
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  fetchUser: () => Promise<void>;
  updateUser: (userData: Partial<User>) => Promise<void>;
  fetchPodcasts: () => Promise<void>;
  createPodcast: (podcastData: CreatePodcastData) => Promise<void>;
  fetchTranslations: () => Promise<void>;
  uploadVoiceSample: (file: File) => Promise<string>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

interface RegisterData {
  full_name: string;
  email: string;
  password: string;
}

interface CreatePodcastData {
  rss_feed_url: string;
  title?: string;
  description?: string;
}

export function AppProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  // Initialize app - check for existing auth
  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      dispatch({ type: 'SET_LOADING', payload: true });
      try {
        await fetchUser();
      } catch (error) {
        localStorage.removeItem('auth_token');
        dispatch({ type: 'SET_AUTH_ERROR', payload: 'Session expired' });
      }
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const login = async (email: string, password: string) => {
    dispatch({ type: 'SET_AUTH_LOADING', payload: true });
    dispatch({ type: 'SET_AUTH_ERROR', payload: null });

    try {
      const response = await api.login({ email, password });
      localStorage.setItem('auth_token', response.token);
      
      // Fetch user data after login
      const userData = await api.fetchUser();
      dispatch({ type: 'LOGIN_SUCCESS', payload: userData });

      // If user is authenticated, fetch their data
      if (userData.onboarding_completed) {
        await Promise.all([
          fetchPodcasts(),
          fetchTranslations()
        ]);
      }
    } catch (error: any) {
      dispatch({ type: 'SET_AUTH_ERROR', payload: error.message || 'Login failed' });
    } finally {
      dispatch({ type: 'SET_AUTH_LOADING', payload: false });
    }
  };

  const logout = async () => {
    try {
      await api.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('auth_token');
      dispatch({ type: 'LOGOUT' });
    }
  };

  const register = async (userData: RegisterData) => {
    dispatch({ type: 'SET_AUTH_LOADING', payload: true });
    dispatch({ type: 'SET_AUTH_ERROR', payload: null });

    try {
      const response = await api.register(userData);
      localStorage.setItem('auth_token', response.token);
      
      const user = await api.fetchUser();
      dispatch({ type: 'LOGIN_SUCCESS', payload: user });
    } catch (error: any) {
      dispatch({ type: 'SET_AUTH_ERROR', payload: error.message || 'Registration failed' });
    } finally {
      dispatch({ type: 'SET_AUTH_LOADING', payload: false });
    }
  };

  const fetchUser = async () => {
    try {
      const user = await api.fetchUser();
      dispatch({ type: 'UPDATE_USER', payload: user });
      return user;
    } catch (error: any) {
      dispatch({ type: 'SET_AUTH_ERROR', payload: error.message });
      throw error;
    }
  };

  const updateUser = async (userData: Partial<User>) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const updatedUser = await api.updateUser(userData);
      dispatch({ type: 'UPDATE_USER', payload: updatedUser });
    } catch (error: any) {
      dispatch({ type: 'SET_ERROR', payload: error.message || 'Failed to update user' });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const fetchPodcasts = async () => {
    try {
      const podcasts = await api.fetchPodcasts();
      dispatch({ type: 'SET_PODCASTS', payload: podcasts });
    } catch (error: any) {
      dispatch({ type: 'SET_ERROR', payload: error.message || 'Failed to fetch podcasts' });
    }
  };

  const createPodcast = async (podcastData: CreatePodcastData) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const newPodcast = await api.createPodcast(podcastData);
      dispatch({ type: 'ADD_PODCAST', payload: newPodcast });
      
      // Fetch updated translations after creating podcast
      await fetchTranslations();
    } catch (error: any) {
      dispatch({ type: 'SET_ERROR', payload: error.message || 'Failed to create podcast' });
      throw error;
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const fetchTranslations = async () => {
    try {
      const translations = await api.fetchTranslations();
      dispatch({ type: 'SET_TRANSLATIONS', payload: translations });
    } catch (error: any) {
      dispatch({ type: 'SET_ERROR', payload: error.message || 'Failed to fetch translations' });
    }
  };

  const uploadVoiceSample = async (file: File) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const response = await api.uploadVoiceSample(file);
      
      // Update user with new voice sample URL
      const updatedUser = { ...state.auth.user!, voice_sample_url: response.file_url };
      dispatch({ type: 'UPDATE_USER', payload: updatedUser });
      
      return response.file_url;
    } catch (error: any) {
      dispatch({ type: 'SET_ERROR', payload: error.message || 'Failed to upload voice sample' });
      throw error;
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const contextValue: AppContextType = {
    state,
    dispatch,
    login,
    logout,
    register,
    fetchUser,
    updateUser,
    fetchPodcasts,
    createPodcast,
    fetchTranslations,
    uploadVoiceSample,
  };

  return <AppContext.Provider value={contextValue}>
    {children}
  </AppContext.Provider>;
}

export const useApp = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};