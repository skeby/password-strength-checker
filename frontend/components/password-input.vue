<template>
  <div class="space-y-2">
    <label class="text-sm uppercase tracking-[0.2em] text-[#f3deac]">Password</label>
    <div class="relative">
      <input
        :type="isVisible ? 'text' : 'password'"
        :value="modelValue"
        placeholder="Enter password"
        autocomplete="new-password"
        class="w-full rounded-xl border border-[#d4b36a66] bg-[#12121ab3] px-4 py-3 pr-24 text-base text-[#f5efe0] outline-none transition focus:border-[#f3deac] focus:ring-2 focus:ring-[#d4b36a55]"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
      <button
        type="button"
        class="absolute right-3 top-1/2 -translate-y-1/2 rounded-md border border-[#d4b36a66] px-2 py-1 text-xs font-semibold uppercase tracking-wide text-[#f3deac] transition hover:bg-[#d4b36a33]"
        @click="isVisible = !isVisible"
      >
        {{ isVisible ? "Hide" : "Show" }}
      </button>
    </div>
    <p class="text-right text-xs text-[#d7cfbd]">{{ modelValue.length }} characters</p>
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
