<template>
  <section class="rounded-3xl border border-[#d4b36a3d] bg-[#10131ad9] p-5 shadow-[0_18px_60px_-34px_rgba(243,222,172,0.35)]">
    <div class="flex items-center justify-between gap-3">
      <div>
        <p class="text-xs uppercase tracking-[0.28em] text-[#cbb78a]">Guidance</p>
        <h3 class="mt-1 font-serif text-2xl text-[#f3deac]">Plain-English advice</h3>
      </div>
      <span
        class="rounded-full border border-[#d4b36a44] px-3 py-1 text-[11px] uppercase tracking-[0.22em] text-[#e9dcc0]"
      >
        {{ isStreaming ? "Streaming" : "Ready" }}
      </span>
    </div>
    <div class="mt-4 rounded-2xl border border-[#ffffff12] bg-[#0b0d12] p-4">
      <p class="whitespace-pre-wrap break-words text-[15px] leading-7 text-[#f4efe5]">
        {{ adviceText || "Run analysis to generate plain-English guidance." }}<span
          v-if="isStreaming"
          class="ml-0.5 inline-block h-[1em] w-2 translate-y-[0.12em] animate-pulse bg-[#f3deac]"
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
