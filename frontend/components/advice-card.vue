<template>
  <section class="relative overflow-hidden rounded-2xl border border-[var(--border-light)] bg-gradient-to-br from-[var(--bg-card)] to-[var(--bg-card-hover)] p-6 backdrop-blur-md">
    <div class="flex items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        <h3 class="display-font text-xl font-semibold text-[var(--text-primary)]">AI Feedback</h3>
      </div>
      <span
        class="rounded-full bg-white/5 px-3 py-1 text-[11px] font-semibold uppercase tracking-wider text-[var(--text-secondary)] backdrop-blur-sm"
      >
        {{ isStreaming ? "Analyzing..." : "Ready" }}
      </span>
    </div>
    <div class="mt-4 rounded-xl bg-black/20 p-5 shadow-inner">
      <p class="whitespace-pre-wrap break-words text-base leading-relaxed text-[var(--text-primary)]">
        {{ adviceText || "Click 'Get personalized advice' to receive tailored suggestions on how to improve this password." }}<span
          v-if="isStreaming"
          class="ml-1 inline-block h-4 w-2 animate-pulse rounded-sm bg-purple-400 align-middle"
        />
      </p>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  adviceText: string
  isStreaming: boolean
}>()
</script>
