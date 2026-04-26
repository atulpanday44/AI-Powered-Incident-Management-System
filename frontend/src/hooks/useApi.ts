/**
 * Custom hook for API calls with loading and error handling
 */

import { useState, useCallback, useEffect } from "react";

interface UseApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

interface UseApiOptions {
  immediate?: boolean;
}

export function useApi<T>(
  apiCall: () => Promise<T>,
  options: UseApiOptions = { immediate: true }
) {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: options.immediate ?? true,
    error: null,
  });

  const execute = useCallback(async () => {
    setState({ data: null, loading: true, error: null });
    try {
      const result = await apiCall();
      setState({ data: result, loading: false, error: null });
      return result;
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "An error occurred";
      setState({ data: null, loading: false, error: errorMessage });
      throw err;
    }
  }, [apiCall]);

  useEffect(() => {
    if (options.immediate ?? true) {
      execute();
    }
  }, [execute, options]);

  return { ...state, refetch: execute };
}
