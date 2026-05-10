<template>
  <div class="space-y-2">
    <div class="flex items-center justify-between">
      <p class="text-xs uppercase tracking-[0.18em] text-[#d8d0bf]">Strength</p>
      <p class="text-sm font-semibold" :class="toneClass">{{ label }}</p>
    </div>
    <div class="grid grid-cols-5 gap-2">
      <div
        v-for="segment in 5"
        :key="segment"
        class="h-3 rounded-full border border-[#ffffff1a] transition-all duration-300"
        :class="segment <= activeSegments ? toneClass : 'bg-[#ffffff12]'"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue"

const props = defineProps<{
  score: number
}>()

const activeSegments = computed(() => Math.max(1, Math.ceil(props.score / 20)))
const label = computed(() => {
  if (props.score <= 20) return "Very Weak"
  if (props.score <= 40) return "Weak"
  if (props.score <= 60) return "Fair"
  if (props.score <= 80) return "Strong"
  return "Very Strong"
})

const toneClass = computed(() => {
  if (props.score <= 20) return "bg-red-500 text-red-300"
  if (props.score <= 40) return "bg-orange-500 text-orange-300"
  if (props.score <= 60) return "bg-yellow-500 text-yellow-300"
  if (props.score <= 80) return "bg-teal-500 text-teal-300"
  return "bg-green-500 text-green-300"
})
</script>
