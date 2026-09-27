<script setup lang="ts">
defineProps<{ label: string; disabled?: boolean }>();
const checked = defineModel<boolean>({ required: true });
</script>

<template>
  <!-- The whole row is the hit target (A11Y-01, CMP-23) -->
  <label class="adl-list__row adl-switch-row">
    <span class="adl-list__title">{{ label }}</span>
    <input v-model="checked" class="adl-switch" type="checkbox" role="switch" :disabled="disabled" />
  </label>
</template>
