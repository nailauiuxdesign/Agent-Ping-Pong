import type { AppState, User, Podcast, Translation } from '../types';

export const initialState: AppState = {
  auth: {
    user: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,
  },
  podcasts: [],
  translations: [],
  episodes: [],
  isLoading: false,
  error: null,
};

type AppAction = 
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_AUTH_LOADING'; payload: boolean }
  | { type: 'SET_AUTH_ERROR'; payload: string | null }
  | { type: 'LOGIN_SUCCESS'; payload: User }
  | { type: 'LOGOUT' }
  | { type: 'UPDATE_USER'; payload: User }
  | { type: 'SET_PODCASTS'; payload: Podcast[] }
  | { type: 'ADD_PODCAST'; payload: Podcast }
  | { type: 'SET_TRANSLATIONS'; payload: Translation[] }
  | { type: 'UPDATE_TRANSLATION'; payload: Translation };

export function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    
    case 'SET_AUTH_LOADING':
      return {
        ...state,
        auth: { ...state.auth, isLoading: action.payload }
      };
    
    case 'SET_AUTH_ERROR':
      return {
        ...state,
        auth: { ...state.auth, error: action.payload }
      };
    
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        auth: {
          user: action.payload,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        }
      };
    
    case 'LOGOUT':
      return {
        ...initialState,
        auth: { ...initialState.auth }
      };
    
    case 'UPDATE_USER':
      return {
        ...state,
        auth: { ...state.auth, user: action.payload }
      };
    
    case 'SET_PODCASTS':
      return { ...state, podcasts: action.payload };
    
    case 'ADD_PODCAST':
      return {
        ...state,
        podcasts: [...state.podcasts, action.payload]
      };
    
    case 'SET_TRANSLATIONS':
      return { ...state, translations: action.payload };
    
    case 'UPDATE_TRANSLATION':
      return {
        ...state,
        translations: state.translations.map(t =>
          t.id === action.payload.id ? action.payload : t
        )
      };
    
    default:
      return state;
  }
}