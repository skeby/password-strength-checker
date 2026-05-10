<template>
  <div class="grid gap-3 sm:grid-cols-3">
    <div class="rounded-xl border border-[#d4b36a44] bg-[#11131da6] p-3">
      <p class="text-xs uppercase tracking-[0.16em] text-[#cbb78a]">ML score</p>
      <p class="mt-2 text-2xl font-extrabold text-[#f3deac]">{{ mlScore }}/100</p>
    </div>
    <div class="rounded-xl border border-[#d4b36a44] bg-[#11131da6] p-3">
      <p class="text-xs uppercase tracking-[0.16em] text-[#cbb78a]">Crack time</p>
      <p class="mt-2 text-sm font-medium text-[#f4f0e7]">{{ crackTime }}</p>
    </div>
    <div class="rounded-xl border border-[#d4b36a44] bg-[#11131da6] p-3">
      <p class="text-xs uppercase tracking-[0.16em] text-[#cbb78a]">zxcvbn</p>
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
