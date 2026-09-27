<script setup lang="ts" generic="T extends string">
import { useId } from "vue";

defineProps<{ label: string; options: readonly { value: T; title: string }[] }>();
const model = defineModel<T>({ required: true });
const name = useId();
</script>

<template>
  <fieldset class="adl-segmented">
    <legend class="adl-visually-hidden">{{ label }}</legend>
    <label v-for="o in options" :key="o.value" class="adl-segmented__option">
      <input v-model="model" type="radio" :name="name" :value="o.value" />
      {{ o.title }}
    </label>
  </fieldset>
</template>
