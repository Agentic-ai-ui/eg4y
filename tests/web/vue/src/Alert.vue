<script setup lang="ts">
import { computed, useId, useTemplateRef, watchEffect } from "vue";

export type AlertAction = { label: string; role?: "default" | "cancel" | "destructive"; onSelect: () => void };

const props = defineProps<{
  open: boolean;
  title: string;
  message?: string;
  actions: [AlertAction] | [AlertAction, AlertAction] | [AlertAction, AlertAction, AlertAction];
}>();
const dialog = useTemplateRef<HTMLDialogElement>("dialog");
const titleId = useId();
const messageId = useId();
const cancel = computed(() => props.actions.find((a) => a.role === "cancel"));
const primary = computed(() => props.actions.find((a) => (a.role ?? "default") === "default"));
// Two buttons: Cancel leading. Three: default on top, Cancel last (CMP-13).
const ordered = computed(() => {
  const rank = (a: AlertAction) => (a === primary.value ? 0 : a === cancel.value ? 2 : 1);
  return props.actions.length === 3
    ? [...props.actions].sort((a, b) => rank(a) - rank(b))
    : [...props.actions].sort((a, b) => (a === cancel.value ? -1 : b === cancel.value ? 1 : 0));
});

watchEffect(() => {
  const el = dialog.value;
  if (!el) return;
  if (props.open && !el.open) el.showModal();
  if (!props.open && el.open) el.close();
});

function onEscape() {
  (cancel.value ?? (props.actions.length === 1 ? props.actions[0] : undefined))?.onSelect();
}
</script>

<template>
  <dialog
    ref="dialog"
    class="adl-alert"
    role="alertdialog"
    :aria-labelledby="titleId"
    :aria-describedby="message ? messageId : undefined"
    @cancel.prevent="onEscape"
  >
    <div class="adl-alert__content">
      <!-- No default action → focus starts on the title so Return triggers nothing risky -->
      <h2 :id="titleId" class="adl-alert__title" tabindex="-1" :autofocus="!primary">{{ title }}</h2>
      <p v-if="message" :id="messageId" class="adl-alert__message">{{ message }}</p>
    </div>
    <div class="adl-alert__actions">
      <button
        v-for="a in ordered"
        :key="a.label"
        type="button"
        :autofocus="a === primary"
        :class="['adl-button', a === primary ? 'adl-button--prominent' : a.role === 'destructive' ? 'adl-button--destructive' : '']"
        @click="a.onSelect"
      >{{ a.label }}</button>
    </div>
  </dialog>
</template>
