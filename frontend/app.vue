<template>
  <div class="glow-overlay min-h-screen flex flex-col">
    <NuxtPage />
  </div>
</template>

<script setup lang="ts">
useHead({
  title: 'Password Health Check',
  meta: [
    { name: 'description', content: 'Understand your password\'s strength instantly, check for data breaches, and get personalized advice to improve it without the technical jargon.' }
  ],
  link: [
    {
      rel: "preconnect",
      href: "https://fonts.googleapis.com"
    },
    {
      rel: "preconnect",
      href: "https://fonts.gstatic.com",
      crossorigin: "anonymous"
    },
    {
      rel: "stylesheet",
      href: "https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap"
    }
  ]
})
</script>
