import zxcvbn from "zxcvbn"

interface ZxcvbnSequenceItem {
  pattern?: string
  l33t?: boolean
}

export interface ZxcvbnResult {
  score: number
  guessesLog10: number
  crackTime: string
  warning: string
  suggestions: string[]
  hasDictionaryMatch: boolean
  hasL33tSub: boolean
  hasKeyboardPattern: boolean
  hasDatePattern: boolean
  hasRepeat: boolean
  hasSequence: boolean
}

const hasPattern = (sequence: ZxcvbnSequenceItem[], pattern: string) =>
  sequence.some((item) => item.pattern === pattern)

export const useZxcvbn = (password: string): ZxcvbnResult => {
  const result = zxcvbn(password ?? "")
  const sequence = (result.sequence ?? []) as ZxcvbnSequenceItem[]

  return {
    score: result.score ?? 0,
    guessesLog10: result.guesses_log10 ?? 0,
    crackTime: String(
      result.crack_times_display?.offline_slow_hashing_1e4_per_second ??
        "Unknown"
    ),
    warning: result.feedback?.warning ?? "",
    suggestions: result.feedback?.suggestions ?? [],
    hasDictionaryMatch: hasPattern(sequence, "dictionary"),
    hasL33tSub: sequence.some((item) => item.l33t === true),
    hasKeyboardPattern: hasPattern(sequence, "spatial"),
    hasDatePattern: hasPattern(sequence, "date"),
    hasRepeat: hasPattern(sequence, "repeat"),
    hasSequence: hasPattern(sequence, "sequence")
  }
}
