import { useMutation } from "@tanstack/vue-query"

interface AnalyseRequest {
  hashPrefix: string
}

interface AnalyseResponse {
  isBreached: boolean
  breachCount: number
}

export const useAnalyse = () => {
  const config = useRuntimeConfig()

  return useMutation<AnalyseResponse, Error, AnalyseRequest>({
    mutationFn: async (payload) =>
      $fetch(`${config.public.backendBaseUrl}/api/analyse`, {
        method: "POST",
        body: payload
      })
  })
}
