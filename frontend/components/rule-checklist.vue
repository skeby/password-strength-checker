<template>
  <section class="rounded-3xl border border-[#d4b36a3d] bg-[#10131ad9] p-5">
    <div class="flex items-end justify-between gap-4">
      <div>
        <p class="text-xs uppercase tracking-[0.28em] text-[#cbb78a]">Policy</p>
        <h3 class="mt-1 font-serif text-2xl text-[#f3deac]">Rule checks</h3>
      </div>
      <p class="text-sm text-[#ddd4c1]">{{ passedCount }} of {{ totalCount }} passed</p>
    </div>
    <ul class="mt-5 space-y-2">
      <li
        v-for="rule in sortedRules"
        :key="rule.name"
        class="flex items-start gap-3 rounded-2xl border border-[#ffffff12] bg-[#0b0d12] px-3 py-3"
      >
        <span
          class="mt-[2px] inline-flex h-5 w-5 items-center justify-center rounded-full text-xs font-bold shrink-0"
          :class="rule.passed ? 'bg-green-500/20 text-green-300' : 'bg-red-500/20 text-red-300'"
        >
          {{ rule.passed ? "✓" : "✕" }}
        </span>
        <div>
          <p class="font-medium text-[#f6f2e9]">{{ rule.name }}</p>
          <p class="text-sm leading-6 text-[#d8d0c0]">{{ rule.description }}</p>
        </div>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import { computed } from "vue"
import type { RuleResult } from "~/composables/use-policy-rules"

const props = defineProps<{
  rules: RuleResult[]
}>()

const sortedRules = computed(() => {
  return [...props.rules].sort((a, b) => Number(b.passed) - Number(a.passed))
})

const passedCount = computed(() => sortedRules.value.filter((rule) => rule.passed).length)
const totalCount = computed(() => sortedRules.value.length)
</script>
