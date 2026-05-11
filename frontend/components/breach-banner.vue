<template>
  <div
    class="rounded-3xl border px-4 py-4 shadow-[0_18px_60px_-34px_rgba(255,107,107,0.35)]"
    :class="
      isBreached
        ? 'border-red-400/30 bg-red-500/10 text-red-100'
        : 'border-green-400/30 bg-green-500/10 text-green-100'
    "
  >
    <p class="text-xs uppercase tracking-[0.22em] opacity-80">
      {{ isBreached ? "Attention" : "Safe result" }}
    </p>
    <p class="mt-1 text-lg font-semibold">
      {{ isBreached ? "Found in known breaches" : "No breach match found" }}
    </p>
    <p class="mt-1 text-sm leading-6 opacity-90">
      {{
        isBreached
          ? `This password appears in breach corpora ${breachCount.toLocaleString()} times.`
          : "This exact hash was not returned by HIBP."
      }}
    </p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  isBreached: boolean
  breachCount: number
}>()
</script>
