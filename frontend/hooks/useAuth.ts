import { useApp } from "contexts/appContext";


export function useAuth() {
  const { state, login, logout, register } = useApp();
  
  return {
    user: state.auth.user,
    isAuthenticated: state.auth.isAuthenticated,
    isLoading: state.auth.isLoading,
    error: state.auth.error,
    login,
    logout,
    register,
  };
}