import { useApp } from 'contexts/appContext';

export function usePodcasts() {
  const { 
    state, 
    fetchPodcasts, 
    createPodcast,
    fetchTranslations 
  } = useApp();
  
  return {
    podcasts: state.podcasts,
    translations: state.translations,
    isLoading: state.isLoading,
    error: state.error,
    fetchPodcasts,
    createPodcast,
    refreshData: async () => {
      await Promise.all([fetchPodcasts(), fetchTranslations()]);
    },
  };
}