import type { ZxcvbnResult } from "./use-zxcvbn"

export interface RuleResult {
  name: string
  passed: boolean
  description: string
}

export interface PolicyResult {
  rules: RuleResult[]
  rulesPassed: number
  rulesTotal: number
}

export const usePolicyRules = (
  password: string,
  zxcvbn: ZxcvbnResult
): PolicyResult => {
  const specialRegex = /[!@#$%^&*()_+\-=[\]{}|;:,.<>?]/
  const rules: RuleResult[] = [
    {
      name: "Minimum length",
      passed: password.length >= 8,
      description: "At least 8 characters."
    },
    {
      name: "Strong length",
      passed: password.length >= 12,
      description: "At least 12 characters."
    },
    {
      name: "Uppercase letters",
      passed: /[A-Z]/.test(password),
      description: "Contains at least one uppercase letter."
    },
    {
      name: "Lowercase letters",
      passed: /[a-z]/.test(password),
      description: "Contains at least one lowercase letter."
    },
    {
      name: "Digits",
      passed: /\d/.test(password),
      description: "Contains at least one number."
    },
    {
      name: "Special characters",
      passed: specialRegex.test(password),
      description: "Contains at least one supported symbol."
    },
    {
      name: "No sequential patterns",
      passed: !zxcvbn.hasSequence,
      description: "Avoids common sequences like 123 or abc."
    },
    {
      name: "No repeated characters",
      passed: !zxcvbn.hasRepeat,
      description: "Avoids obvious repeated chunks."
    },
    {
      name: "No dictionary words",
      passed: !zxcvbn.hasDictionaryMatch,
      description: "Avoids common words and variants."
    },
    {
      name: "No keyboard patterns",
      passed: !zxcvbn.hasKeyboardPattern,
      description: "Avoids keyboard walks like qwerty."
    },
    {
      name: "Not common password",
      passed: zxcvbn.score !== 0,
      description: "Does not match highly common passwords."
    }
  ]

  const rulesPassed = rules.filter((rule) => rule.passed).length
  return { rules, rulesPassed, rulesTotal: rules.length }
}
