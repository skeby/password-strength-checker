<template>
  <main class="mx-auto min-h-screen w-full max-w-6xl px-4 py-10 md:px-8">
    <header class="mb-8 space-y-3">
      <p class="text-xs uppercase tracking-[0.3em] text-[#cab17a]">Security Atelier</p>
      <h1 class="font-serif text-4xl leading-tight text-[#f3deac] md:text-5xl">
        AI-powered Password Strength Checker
      </h1>
      <p class="max-w-2xl text-[#d8cfbe]">
        Real-time local scoring with zxcvbn and ONNX inference, breach intelligence via
        HIBP, and concise streamed guidance from Claude.
      </p>
    </header>

    <div class="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
      <section class="space-y-4 rounded-3xl border border-[#d4b36a4a] bg-[#0f1118cc] p-5 shadow-[0_20px_80px_-40px_rgba(212,179,106,0.45)]">
        <PasswordInput v-model="password" />
        <StrengthBar :score="strengthScore" />
        <StatsRow
          :ml-score="strengthScore"
          :crack-time="zxcvbnResult.crackTime"
          :zxcvbn-score="zxcvbnResult.score"
        />

        <BreachBanner :is-breached="isBreached" :breach-count="breachCount" />

        <button
          class="w-full rounded-xl border border-[#d4b36a80] bg-gradient-to-r from-[#b38a3f] to-[#f0cc83] px-4 py-3 font-bold text-[#17120a] transition hover:brightness-105 disabled:cursor-not-allowed disabled:opacity-60"
          :disabled="!password.length || isStreaming"
          @click="runAdvice"
        >
          {{ isStreaming ? "Generating advice..." : "Check password" }}
        </button>

        <p v-if="modelError" class="text-sm text-red-300">
          Model error: {{ modelError }}
        </p>
      </section>

      <div class="space-y-6">
        <RuleChecklist :rules="policy.rules" />
        <AdviceCard :advice-text="adviceText" :is-streaming="isStreaming" />
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue"
import { extractFeatures } from "~/composables/use-feature-extractor"
import { useAnalyse } from "~/composables/use-analyse"
import { useAdvise } from "~/composables/use-advise"
import { useModelInference } from "~/composables/use-model-inference"
import { usePolicyRules } from "~/composables/use-policy-rules"
import { useZxcvbn } from "~/composables/use-zxcvbn"

const password = ref("")
const strengthScore = ref(0)
const isBreached = ref(false)
const breachCount = ref(0)
const breachDebounce = ref<ReturnType<typeof setTimeout> | null>(null)

const zxcvbnResult = computed(() => useZxcvbn(password.value))
const policy = computed(() => usePolicyRules(password.value, zxcvbnResult.value))
const features = computed(() => extractFeatures(password.value, zxcvbnResult.value))

const analyseMutation = useAnalyse()
const { adviceText, isStreaming, startAdvise } = useAdvise()
const { predictStrength, loadModel, error: modelError } = useModelInference()
onMounted(() => loadModel())



const sha1 = async (value: string): Promise<string> => {
  const encoded = new TextEncoder().encode(value)
  const digest = await crypto.subtle.digest("SHA-1", encoded)
  return Array.from(new Uint8Array(digest))
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("")
    .toUpperCase()
}

watch(
  features,
  async (vector) => {
    strengthScore.value = await predictStrength(vector)
  },
  { immediate: true }
)

watch(
  password,
  async (value) => {
    if (breachDebounce.value) {
      clearTimeout(breachDebounce.value)
    }

    if (!value) {
      isBreached.value = false
      breachCount.value = 0
      return
    }

    breachDebounce.value = setTimeout(async () => {
      const fullHash = await sha1(value)
      const hashPrefix = fullHash.slice(0, 5)

      const result = await analyseMutation.mutateAsync({ hashPrefix })
      isBreached.value = result.isBreached
      breachCount.value = result.breachCount
    }, 400)
  },
  { immediate: true }
)

const runAdvice = async () => {
  if (!password.value) {
    return
  }

  await startAdvise({
    strengthScore: strengthScore.value,
    zxcvbnScore: zxcvbnResult.value.score,
    crackTime: zxcvbnResult.value.crackTime,
    warning: zxcvbnResult.value.warning,
    suggestions: zxcvbnResult.value.suggestions,
    hasDictionaryMatch: zxcvbnResult.value.hasDictionaryMatch,
    hasL33tSub: zxcvbnResult.value.hasL33tSub,
    hasKeyboardPattern: zxcvbnResult.value.hasKeyboardPattern,
    hasDatePattern: zxcvbnResult.value.hasDatePattern,
    hasRepeat: zxcvbnResult.value.hasRepeat,
    hasSequence: zxcvbnResult.value.hasSequence,
    rulesPassed: policy.value.rulesPassed,
    rulesTotal: policy.value.rulesTotal,
    isBreached: isBreached.value,
    breachCount: breachCount.value
  })
}
</script>
