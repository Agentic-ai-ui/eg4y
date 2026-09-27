<script lang="ts">
  import type { Snippet } from "svelte";

  let { open, title, confirmLabel, confirmDisabled = false, oncancel, onconfirm, children }: {
    open: boolean;
    title: string;
    confirmLabel?: string;
    confirmDisabled?: boolean;
    oncancel: () => void;
    onconfirm?: () => void;
    children: Snippet;
  } = $props();

  let dialog: HTMLDialogElement;
  const titleId = $props.id();

  $effect(() => {
    if (open && !dialog.open) dialog.showModal();
    if (!open && dialog.open) dialog.close();
  });
</script>

<!-- Native <dialog>: focus containment, inert page, Esc (CMP-07, CMP-08). Cancel leading, confirm trailing (CMP-09). -->
<dialog
  bind:this={dialog}
  class="adl-sheet"
  aria-labelledby={titleId}
  oncancel={(e) => {
    e.preventDefault();
    oncancel();
  }}
>
  <div class="adl-sheet__header">
    <button type="button" class="adl-button adl-button--plain" onclick={oncancel}>Cancel</button>
    <h2 id={titleId} class="adl-sheet__title">{title}</h2>
    {#if confirmLabel}
      <button type="button" class="adl-button adl-button--plain" disabled={confirmDisabled} onclick={onconfirm}>{confirmLabel}</button>
    {/if}
  </div>
  <div class="adl-sheet__body">{@render children()}</div>
</dialog>
