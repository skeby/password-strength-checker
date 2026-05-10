import type { ZxcvbnResult } from "./use-zxcvbn"

const entropyBits = (password: string): number => {
  if (!password.length) {
    return 0
  }

  const frequency: Record<string, number> = {}
  for (const char of password) {
    frequency[char] = (frequency[char] ?? 0) + 1
  }

  let entropy = 0
  for (const count of Object.values(frequency)) {
    const probability = count / password.length
    entropy -= probability * Math.log2(probability)
  }

  return entropy
}

export const extractFeatures = (
  password: string,
  zxcvbn: ZxcvbnResult
): number[] => {
  const hasUppercase = /[A-Z]/.test(password) ? 1 : 0
  const hasLowercase = /[a-z]/.test(password) ? 1 : 0
  const hasDigits = /\d/.test(password) ? 1 : 0
  const hasSpecialChars = /[^A-Za-z0-9]/.test(password) ? 1 : 0
  const uniqueCharRatio = password.length
    ? new Set(password).size / password.length
    : 0
  const charClassCount =
    hasUppercase + hasLowercase + hasDigits + hasSpecialChars

  const hasDictionaryMatch = zxcvbn.hasDictionaryMatch ? 1 : 0
  const hasL33tSub = zxcvbn.hasL33tSub ? 1 : 0
  const hasKeyboardPattern = zxcvbn.hasKeyboardPattern ? 1 : 0
  const hasDatePattern = zxcvbn.hasDatePattern ? 1 : 0
  const hasRepeat = zxcvbn.hasRepeat ? 1 : 0
  const hasSequence = zxcvbn.hasSequence ? 1 : 0

  return [
    password.length,
    entropyBits(password),
    hasUppercase,
    hasLowercase,
    hasDigits,
    hasSpecialChars,
    uniqueCharRatio,
    charClassCount,
    zxcvbn.score,
    zxcvbn.guessesLog10,
    hasDictionaryMatch,
    hasL33tSub,
    hasKeyboardPattern,
    hasDatePattern,
    hasRepeat,
    hasSequence
  ]
}
