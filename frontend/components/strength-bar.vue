<template>
  <div class="space-y-3 mt-2">
    <div class="flex items-end justify-between">
      <p class="text-sm font-medium text-[var(--text-secondary)]">Security Rating</p>
      <p class="text-lg font-bold transition-colors duration-300 display-font" :class="toneTextClass">{{ label }}</p>
    </div>
    <div class="relative h-2.5 w-full overflow-hidden rounded-full bg-white/5 shadow-inner">
      <div
        class="absolute left-0 top-0 h-full rounded-full transition-all duration-500 ease-out"
        :class="toneBgClass"
        :style="{ width: `${Math.max(2, score)}%` }"
      />
      <!-- Glow effect -->
      <div
        class="absolute left-0 top-0 h-full w-full rounded-full blur-md transition-all duration-500 ease-out opacity-40 mix-blend-screen"
        :class="toneBgClass"
        :style="{ width: `${Math.max(2, score)}%` }"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue"

const props = defineProps<{
  score: number
}>()

const label = computed(() => {
  if (props.score <= 20) return "Very Weak"
  if (props.score <= 40) return "Weak"
  if (props.score <= 60) return "Fair"
  if (props.score <= 80) return "Strong"
  return "Very Strong"
})

const toneBgClass = computed(() => {
  if (props.score <= 20) return "bg-gradient-to-r from-red-600 to-red-400"
  if (props.score <= 40) return "bg-gradient-to-r from-orange-600 to-orange-400"
  if (props.score <= 60) return "bg-gradient-to-r from-amber-500 to-yellow-400"
  if (props.score <= 80) return "bg-gradient-to-r from-blue-600 to-blue-400"
  return "bg-gradient-to-r from-emerald-500 to-emerald-400"
})

const toneTextClass = computed(() => {
  if (props.score <= 20) return "text-red-400"
  if (props.score <= 40) return "text-orange-400"
  if (props.score <= 60) return "text-amber-400"
  if (props.score <= 80) return "text-blue-400"
  return "text-emerald-400"
})
</script>
