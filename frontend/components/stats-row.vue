<template>
  <div class="grid gap-4 sm:grid-cols-3">
    <div class="rounded-2xl border border-[var(--border-light)] bg-[var(--bg-card)] p-4 backdrop-blur-md transition hover:bg-[var(--bg-card-hover)]">
      <p class="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)]">AI Assessment</p>
      <p class="mt-2 text-3xl font-extrabold display-font text-[var(--text-primary)]">{{ mlScore }}<span class="text-lg text-[var(--text-secondary)] font-medium">/100</span></p>
    </div>
    <div class="rounded-2xl border border-[var(--border-light)] bg-[var(--bg-card)] p-4 backdrop-blur-md transition hover:bg-[var(--bg-card-hover)]">
      <p class="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)]">Time to Hack</p>
      <p class="mt-2 text-lg font-bold leading-7 text-[var(--text-primary)]">{{ crackTime }}</p>
    </div>
    <div class="rounded-2xl border border-[var(--border-light)] bg-[var(--bg-card)] p-4 backdrop-blur-md transition hover:bg-[var(--bg-card-hover)]">
      <p class="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)]">Pattern Safety</p>
      <div class="mt-3 flex gap-1.5">
        <span
          v-for="index in 4"
          :key="index"
          class="h-2 w-full rounded-full transition-colors"
          :class="index <= zxcvbnScore ? (zxcvbnScore < 3 ? 'bg-orange-500' : 'bg-emerald-500') : 'bg-white/10'"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  mlScore: number
  crackTime: string
  zxcvbnScore: number
}>()
</script>
