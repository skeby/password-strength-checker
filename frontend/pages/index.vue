<template>
  <main class="relative isolate min-h-screen overflow-hidden px-4 py-6 md:px-8 md:py-10">
    <div
      class="pointer-events-none absolute inset-x-0 top-[-8rem] h-[28rem] bg-[radial-gradient(circle_at_top,rgba(243,222,172,0.12),transparent_55%)]"
    />
    <div class="mx-auto w-full max-w-7xl">
      <header class="max-w-3xl">
        <p class="text-xs uppercase tracking-[0.32em] text-[#cbb78a]">Security Atelier</p>
        <h1 class="display-font mt-3 text-5xl leading-[0.95] text-[#f6e7bf] md:text-7xl">
          Check a password in one calm step
        </h1>
        <p class="mt-4 max-w-2xl text-base leading-7 text-[#ddd4c1] md:text-lg">
          Type a password, get an instant strength score, a breach check, and plain-English advice.
          Everything stays simple enough for regular use.
        </p>
      </header>

      <section class="mt-8 grid gap-6 xl:grid-cols-[minmax(0,390px)_minmax(0,1fr)]">
        <div class="space-y-4 self-start xl:sticky xl:top-8">
          <section
            class="rounded-[2rem] border border-[#d4b36a33] bg-[#0e1118e6] p-5 shadow-[0_22px_80px_-44px_rgba(243,222,172,0.4)]"
          >
            <div class="flex items-end justify-between gap-4">
              <div>
                <p class="text-[11px] uppercase tracking-[0.22em] text-[#cbb78a]">Password</p>
                <p class="mt-1 text-sm leading-6 text-[#d6ccb9]">
                  No password leaves your browser for scoring.
                </p>
              </div>
              <span
                class="rounded-full border border-[#d4b36a2a] px-3 py-1 text-[10px] uppercase tracking-[0.24em] text-[#e6d8b2]"
              >
                Local first
              </span>
            </div>

            <div class="mt-4">
              <PasswordInput v-model="password" />
            </div>

            <div class="mt-5">
              <StrengthBar :score="strengthScore" />
            </div>

            <button
              class="mt-5 w-full rounded-2xl border border-[#d4b36a80] bg-gradient-to-r from-[#b78f41] to-[#f2d08c] px-4 py-3.5 text-base font-bold text-[#16120a] transition hover:brightness-105 disabled:cursor-not-allowed disabled:opacity-60"
              :disabled="!password.length || isStreaming || analyseMutation.isPending.value"
              @click="runAdvice"
            >
              {{ isStreaming ? "Generating advice..." : analyseMutation.isPending.value ? "Analysing..." : "Check password" }}
            </button>

            <p v-if="modelError" class="mt-3 text-sm text-red-300">
              Model error: {{ modelError }}
            </p>
          </section>

          <div class="grid gap-3 sm:grid-cols-3 xl:grid-cols-1">
            <div class="rounded-2xl border border-[#ffffff14] bg-[#0b0d12] p-4">
              <p class="text-[11px] uppercase tracking-[0.22em] text-[#cbb78a]">Speed</p>
              <p class="mt-2 text-sm leading-6 text-[#f2ead9]">Fast local scoring with zxcvbn and ONNX.</p>
            </div>
            <div class="rounded-2xl border border-[#ffffff14] bg-[#0b0d12] p-4">
              <p class="text-[11px] uppercase tracking-[0.22em] text-[#cbb78a]">Breach</p>
              <p class="mt-2 text-sm leading-6 text-[#f2ead9]">Server-side HIBP lookup on a hash prefix only.</p>
            </div>
            <div class="rounded-2xl border border-[#ffffff14] bg-[#0b0d12] p-4">
              <p class="text-[11px] uppercase tracking-[0.22em] text-[#cbb78a]">Advice</p>
              <p class="mt-2 text-sm leading-6 text-[#f2ead9]">Streamed guidance with one clear next step.</p>
            </div>
          </div>
        </div>

        <div class="space-y-6">
          <StatsRow
            :ml-score="strengthScore"
            :crack-time="zxcvbnResult.crackTime"
            :zxcvbn-score="zxcvbnResult.score"
          />

          <BreachBanner :is-breached="isBreached" :breach-count="breachCount" />

          <AdviceCard :advice-text="adviceText" :is-streaming="isStreaming" />

          <details class="rounded-3xl border border-[#d4b36a2a] bg-[#0e1118cc] p-5">
            <summary class="cursor-pointer list-none text-sm uppercase tracking-[0.24em] text-[#d5c293]">
              View detailed policy checks
            </summary>
            <div class="mt-4">
              <RuleChecklist :rules="policy.rules" />
            </div>
          </details>
        </div>
      </section>
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
