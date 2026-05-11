import { useMutation } from "@tanstack/vue-query"
import { ref } from "vue"

interface AdvisePayload {
  strengthScore: number
  zxcvbnScore: number
  crackTime: string
  warning: string
  suggestions: string[]
  hasDictionaryMatch: boolean
  hasL33tSub: boolean
  hasKeyboardPattern: boolean
  hasDatePattern: boolean
  hasRepeat: boolean
  hasSequence: boolean
  rulesPassed: number
  rulesTotal: number
  isBreached: boolean
  breachCount: number
}

const parseSseChunk = (chunk: string): string => {
  return chunk
    .split("\n")
    .filter((line) => line.startsWith("data:"))
    .map((line) => line.slice(5).replace(/^ /, ""))
    .join("\n")
}

export const useAdvise = () => {
  const config = useRuntimeConfig()
  const adviceText = ref("")
  const isStreaming = ref(false)

  const mutation = useMutation<void, Error, AdvisePayload>({
    mutationFn: async (payload) => {
      adviceText.value = ""
      isStreaming.value = true

      try {
        const response = await fetch(`${config.public.backendBaseUrl}/api/advise`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        })

        if (!response.ok || !response.body) {
          throw new Error("Failed to open advice stream.")
        }

        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        let buffer = ""

        while (true) {
          const { done, value } = await reader.read()
          if (done) {
            break
          }

          buffer += decoder.decode(value, { stream: true })
          const events = buffer.split("\n\n")
          buffer = events.pop() ?? ""

          for (const eventChunk of events) {
            const data = parseSseChunk(eventChunk)
            if (data === "[DONE]") {
              return
            }
            adviceText.value += data
          }
        }
      } finally {
        isStreaming.value = false
      }
    }
  })

  return {
    adviceText,
    isStreaming,
    startAdvise: mutation.mutateAsync,
    ...mutation
  }
}
