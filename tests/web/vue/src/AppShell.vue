<script setup lang="ts">
import type { Component } from "vue";

export type Section = { id: string; title: string; href: string; icon: Component };
defineProps<{ sections: readonly Section[]; currentId: string }>();
</script>

<template>
  <div class="adl-app">
    <div class="adl-app__layout">
      <nav class="adl-nav adl-glass" aria-label="Primary">
        <ul class="adl-nav__list">
          <li v-for="s in sections" :key="s.id">
            <a class="adl-nav__link" :href="s.href" :aria-current="s.id === currentId ? 'page' : undefined">
              <component :is="s.icon" aria-hidden="true" />
              <span>{{ s.title }}</span>
            </a>
          </li>
        </ul>
      </nav>
      <main class="adl-app__main"><slot /></main>
    </div>
  </div>
</template>
