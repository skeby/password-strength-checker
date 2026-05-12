<template>
  <div class="group relative">
    <div class="absolute -inset-0.5 rounded-2xl bg-gradient-to-r from-blue-500/20 to-purple-500/20 opacity-0 blur transition duration-500 group-focus-within:opacity-100" />
    <div class="relative flex items-center overflow-hidden rounded-2xl border border-[var(--border-light)] bg-[#0f0f13] shadow-inner transition-colors duration-300 focus-within:border-blue-500/50 focus-within:bg-[#14141a]">
      <input
        :type="isVisible ? 'text' : 'password'"
        :value="modelValue"
        placeholder="Type a password to test..."
        autocomplete="new-password"
        class="w-full bg-transparent px-5 py-4 pr-24 text-lg font-medium text-[var(--text-primary)] placeholder-[var(--text-secondary)] outline-none"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
      <button
        type="button"
        class="absolute right-3 top-1/2 -translate-y-1/2 rounded-xl bg-white/5 px-3 py-1.5 text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] backdrop-blur-sm transition-colors hover:bg-white/10 hover:text-[var(--text-primary)]"
        @click="isVisible = !isVisible"
      >
        {{ isVisible ? "Hide" : "Show" }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"

defineProps<{
  modelValue: string
}>()

defineEmits<{
  (e: "update:modelValue", value: string): void
}>()

const isVisible = ref(false)
</script>
