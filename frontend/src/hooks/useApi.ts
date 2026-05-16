/**
 * Custom hook for API calls with loading and error handling
 */

import { useState, useCallback, useEffect, useRef } from "react";

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
  const apiCallRef = useRef(apiCall);
  const immediate = options.immediate ?? true;

  useEffect(() => {
    apiCallRef.current = apiCall;
  }, [apiCall]);

  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: immediate,
    error: null,
  });

  const execute = useCallback(async () => {
    setState({ data: null, loading: true, error: null });
    try {
      const result = await apiCallRef.current();
      setState({ data: result, loading: false, error: null });
      return result;
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "An error occurred";
      setState({ data: null, loading: false, error: errorMessage });
      return null;
    }
  }, []);

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [execute, immediate]);

  return { ...state, refetch: execute };
}
