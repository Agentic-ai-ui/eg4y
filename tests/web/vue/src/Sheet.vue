<script setup lang="ts">
import { useId, useTemplateRef, watchEffect } from "vue";

const props = defineProps<{ open: boolean; title: string; confirmLabel?: string; confirmDisabled?: boolean }>();
const emit = defineEmits<{ cancel: []; confirm: [] }>();
const dialog = useTemplateRef<HTMLDialogElement>("dialog");
const titleId = useId();

watchEffect(() => {
  const el = dialog.value;
  if (!el) return;
  if (props.open && !el.open) el.showModal();
  if (!props.open && el.open) el.close();
});
</script>

<template>
  <!-- Native <dialog>: focus containment, inert page, Esc (CMP-07, CMP-08). Cancel leading, confirm trailing (CMP-09). -->
  <dialog ref="dialog" class="adl-sheet" :aria-labelledby="titleId" @cancel.prevent="emit('cancel')">
    <div class="adl-sheet__header">
      <button type="button" class="adl-button adl-button--plain" @click="emit('cancel')">Cancel</button>
      <h2 :id="titleId" class="adl-sheet__title">{{ title }}</h2>
      <button
        v-if="confirmLabel"
        type="button"
        class="adl-button adl-button--plain"
        :disabled="confirmDisabled"
        @click="emit('confirm')"
      >{{ confirmLabel }}</button>
    </div>
    <div class="adl-sheet__body"><slot /></div>
  </dialog>
</template>
