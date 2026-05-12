<template>
  <main class="relative isolate flex min-h-screen flex-col items-center justify-center px-4 py-12 md:py-24 overflow-x-hidden">
    <div class="mx-auto w-full max-w-2xl">
      <header class="text-center">
        <div class="inline-flex items-center gap-2 rounded-full border border-[var(--border-light)] bg-white/5 px-4 py-1.5 backdrop-blur-sm">
          <span class="relative flex h-2 w-2">
            <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-blue-400 opacity-75"></span>
            <span class="relative inline-flex h-2 w-2 rounded-full bg-blue-500"></span>
          </span>
          <p class="text-xs font-semibold uppercase tracking-widest text-[var(--text-secondary)]">Password Health Check</p>
        </div>
        <h1 class="display-font mt-6 text-5xl font-extrabold tracking-tight text-[var(--text-primary)] md:text-6xl lg:text-7xl">
          Check your password
        </h1>
        <p class="mx-auto mt-5 max-w-xl text-lg leading-relaxed text-[var(--text-secondary)]">
          Type a password to instantly understand its strength, check for data breaches, and get personalized advice to improve it.
        </p>
      </header>

      <div class="mt-12 space-y-8">
        <!-- Main Input Card -->
        <section class="relative rounded-[2rem] border border-[var(--border-light)] bg-gradient-to-b from-[var(--bg-card)] to-[var(--bg-card-hover)] p-6 shadow-2xl backdrop-blur-xl md:p-8">
          <!-- Ambient glow behind card -->
          <div class="pointer-events-none absolute -inset-px -z-10 rounded-[2rem] bg-gradient-to-b from-blue-500/20 to-purple-500/10 opacity-50 blur-xl transition duration-500"></div>
          
          <PasswordInput v-model="password" />

          <div class="mt-8 transition-all duration-300" :class="{ 'opacity-50 grayscale': !password.length }">
            <StrengthBar :score="strengthScore" />
          </div>

          <button
            class="group mt-8 w-full overflow-hidden rounded-2xl bg-white text-base font-bold text-black transition-all hover:scale-[1.02] hover:bg-gray-100 disabled:pointer-events-none disabled:opacity-50 disabled:hover:scale-100"
            :disabled="!password.length || isStreaming || analyseMutation.isPending.value"
            @click="runAdvice"
          >
            <div class="relative px-6 py-4">
              <span class="relative z-10 flex items-center justify-center gap-2">
                {{ isStreaming ? "Analyzing..." : analyseMutation.isPending.value ? "Checking databases..." : "Get personalized advice" }}
                <svg v-if="!isStreaming && !analyseMutation.isPending.value" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 transition-transform group-hover:translate-x-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </span>
            </div>
          </button>
          
          <p v-if="modelError" class="mt-4 text-center text-sm font-medium text-red-400">
            Error: {{ modelError }}
          </p>
        </section>

        <!-- Results Sections (Fade in when there's a password) -->
        <Transition
          enter-active-class="transition-all duration-500 ease-out"
          enter-from-class="opacity-0 translate-y-4"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition-all duration-300 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 translate-y-4"
        >
          <div v-if="password.length" class="space-y-6">
            <StatsRow
              :ml-score="strengthScore"
              :crack-time="zxcvbnResult.crackTime"
              :zxcvbn-score="zxcvbnResult.score"
            />

            <BreachBanner :is-breached="isBreached" :breach-count="breachCount" />

            <AdviceCard :advice-text="adviceText" :is-streaming="isStreaming" />

            <details class="group mt-8 rounded-2xl border border-[var(--border-light)] bg-black/20 backdrop-blur-sm">
              <summary class="flex cursor-pointer items-center justify-between p-5 font-semibold text-[var(--text-secondary)] transition hover:text-[var(--text-primary)]">
                <span>View Technical Details</span>
                <span class="transition group-open:rotate-180">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </span>
              </summary>
              <div class="p-5 pt-0">
                <RuleChecklist :rules="policy.rules" />
              </div>
            </details>
          </div>
        </Transition>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue"
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
      const hashSuffix = fullHash.slice(5)
      const result = await analyseMutation.mutateAsync({ hashPrefix, hashSuffix })
      isBreached.value = result.isBreached
      breachCount.value = result.breachCount
    }, 600)
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
