<template>
  <div
    class="rounded-xl border px-4 py-3"
    :class="
      isBreached
        ? 'border-red-400/40 bg-red-500/10 text-red-200'
        : 'border-green-400/40 bg-green-500/10 text-green-200'
    "
  >
    <p class="font-semibold">
      {{ isBreached ? "Found in known breaches" : "No breach match found" }}
    </p>
    <p class="text-sm opacity-90">
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
