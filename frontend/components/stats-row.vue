<template>
  <div class="grid gap-3 sm:grid-cols-3">
    <div class="rounded-2xl border border-[#d4b36a33] bg-[#0b0d12] p-3">
      <p class="text-[11px] uppercase tracking-[0.22em] text-[#cbb78a]">ML score</p>
      <p class="mt-2 text-2xl font-extrabold text-[#f3deac]">{{ mlScore }}/100</p>
    </div>
    <div class="rounded-2xl border border-[#d4b36a33] bg-[#0b0d12] p-3">
      <p class="text-[11px] uppercase tracking-[0.22em] text-[#cbb78a]">Crack time</p>
      <p class="mt-2 text-sm font-medium leading-6 text-[#f4f0e7]">{{ crackTime }}</p>
    </div>
    <div class="rounded-2xl border border-[#d4b36a33] bg-[#0b0d12] p-3">
      <p class="text-[11px] uppercase tracking-[0.22em] text-[#cbb78a]">zxcvbn</p>
      <div class="mt-2 flex gap-1">
        <span
          v-for="index in 4"
          :key="index"
          class="h-3 w-3 rounded-full border border-[#f3deac66]"
          :class="index <= zxcvbnScore ? 'bg-[#f3deac]' : 'bg-transparent'"
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
