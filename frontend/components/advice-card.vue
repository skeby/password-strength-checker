<template>
  <section class="rounded-2xl border border-[#d4b36a3d] bg-[#12121abf] p-4">
    <div class="flex items-center justify-between">
      <h3 class="font-serif text-xl text-[#f3deac]">AI advice</h3>
      <span
        class="rounded-full border border-[#d4b36a44] px-2 py-1 text-xs uppercase tracking-wide text-[#e9dcc0]"
      >
        {{ isStreaming ? "Streaming" : "Ready" }}
      </span>
    </div>
    <p class="mt-3 whitespace-pre-line text-[#ece7dc]">
      {{ adviceText || "Run analysis to generate plain-English guidance." }}<span
        v-if="isStreaming"
        class="ml-0.5 inline-block h-4 w-2 animate-pulse bg-[#f3deac]"
      />
    </p>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  adviceText: string
  isStreaming: boolean
}>()
</script>
