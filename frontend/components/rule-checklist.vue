<template>
  <section class="rounded-2xl border border-[var(--border-light)] bg-[var(--bg-card)] p-5 backdrop-blur-md">
    <div class="flex items-center justify-between gap-4">
      <h3 class="display-font text-xl font-semibold text-[var(--text-primary)]">Technical Checks</h3>
      <p class="text-sm font-medium text-[var(--text-secondary)]">{{ passedCount }} / {{ totalCount }} Passed</p>
    </div>
    <ul class="mt-5 space-y-3">
      <li
        v-for="rule in sortedRules"
        :key="rule.name"
        class="flex items-start gap-3 rounded-xl bg-black/20 p-3 shadow-inner transition hover:bg-black/30"
      >
        <span
          class="mt-0.5 inline-flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-xs font-bold"
          :class="rule.passed ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'"
        >
          <svg v-if="rule.passed" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </span>
        <div>
          <p class="font-medium text-[var(--text-primary)]">{{ rule.name }}</p>
          <p class="mt-0.5 text-sm text-[var(--text-secondary)]">{{ rule.description }}</p>
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
