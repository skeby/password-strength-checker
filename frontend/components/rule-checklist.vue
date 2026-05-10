<template>
  <section class="rounded-2xl border border-[#d4b36a3d] bg-[#12121abf] p-4">
    <h3 class="font-serif text-xl text-[#f3deac]">Policy rules</h3>
    <ul class="mt-4 space-y-2">
      <li
        v-for="rule in sortedRules"
        :key="rule.name"
        class="flex items-start gap-3 rounded-lg border border-[#ffffff14] px-3 py-2"
      >
        <span
          class="mt-[2px] inline-flex h-5 w-5 items-center justify-center rounded-full text-xs font-bold"
          :class="rule.passed ? 'bg-green-500/20 text-green-300' : 'bg-red-500/20 text-red-300'"
        >
          {{ rule.passed ? "✓" : "✕" }}
        </span>
        <div>
          <p class="font-medium text-[#f6f2e9]">{{ rule.name }}</p>
          <p class="text-sm text-[#d8d0c0]">{{ rule.description }}</p>
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
</script>
