<script lang="ts" module>
  export type AlertAction = { label: string; role?: "default" | "cancel" | "destructive"; onSelect: () => void };
</script>

<script lang="ts">
  let { open, title, message, actions }: {
    open: boolean;
    title: string;
    message?: string;
    actions: [AlertAction] | [AlertAction, AlertAction] | [AlertAction, AlertAction, AlertAction];
  } = $props();

  let dialog: HTMLDialogElement;
  const id = $props.id();
  const cancel = $derived(actions.find((a) => a.role === "cancel"));
  const primary = $derived(actions.find((a) => (a.role ?? "default") === "default"));
  // Two buttons: Cancel leading. Three: default on top, Cancel last (CMP-13).
  const ordered = $derived.by(() => {
    const rank = (a: AlertAction) => (a === primary ? 0 : a === cancel ? 2 : 1);
    return actions.length === 3
      ? [...actions].sort((a, b) => rank(a) - rank(b))
      : [...actions].sort((a, b) => (a === cancel ? -1 : b === cancel ? 1 : 0));
  });

  $effect(() => {
    if (open && !dialog.open) dialog.showModal();
    if (!open && dialog.open) dialog.close();
  });
</script>

<dialog
  bind:this={dialog}
  class="adl-alert"
  role="alertdialog"
  aria-labelledby="{id}-title"
  aria-describedby={message ? `${id}-message` : undefined}
  oncancel={(e) => {
    e.preventDefault();
    (cancel ?? (actions.length === 1 ? actions[0] : undefined))?.onSelect();
  }}
>
  <div class="adl-alert__content">
    <!-- No default action → focus starts on the title so Return triggers nothing risky -->
    <!-- svelte-ignore a11y_autofocus -->
    <h2 id="{id}-title" class="adl-alert__title" tabindex="-1" autofocus={!primary}>{title}</h2>
    {#if message}<p id="{id}-message" class="adl-alert__message">{message}</p>{/if}
  </div>
  <div class="adl-alert__actions">
    {#each ordered as a (a.label)}
      <!-- svelte-ignore a11y_autofocus -->
      <button
        type="button"
        autofocus={a === primary}
        class={["adl-button", a === primary ? "adl-button--prominent" : a.role === "destructive" && "adl-button--destructive"]}
        onclick={a.onSelect}
      >{a.label}</button>
    {/each}
  </div>
</dialog>
