<template>
  <div
    class="relative overflow-hidden rounded-2xl border px-5 py-5 backdrop-blur-md transition-all"
    :class="
      isBreached
        ? 'border-red-500/30 bg-red-500/10'
        : 'border-emerald-500/30 bg-emerald-500/10'
    "
  >
    <div class="relative z-10 flex items-start gap-4">
      <div class="mt-1 shrink-0 rounded-full p-2" :class="isBreached ? 'bg-red-500/20 text-red-400' : 'bg-emerald-500/20 text-emerald-400'">
        <svg v-if="isBreached" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <div>
        <p class="text-lg font-bold display-font" :class="isBreached ? 'text-red-400' : 'text-emerald-400'">
          {{ isBreached ? "Exposed in Data Breaches" : "No Known Leaks Found" }}
        </p>
        <p class="mt-1.5 text-sm leading-relaxed text-[var(--text-secondary)]">
          {{
            isBreached
              ? `This password has been found ${breachCount.toLocaleString()} times in known data leaks. You should definitely change it.`
              : "We couldn't find this password in any known data breach databases. This is a good sign!"
          }}
        </p>
      </div>
    </div>
    <!-- Ambient glow -->
    <div 
      class="absolute -right-10 -top-10 h-32 w-32 rounded-full blur-3xl"
      :class="isBreached ? 'bg-red-500/20' : 'bg-emerald-500/20'"
    />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  isBreached: boolean
  breachCount: number
}>()
</script>
