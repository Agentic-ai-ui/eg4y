<script lang="ts">
  let { label, checked = $bindable(), disabled = false }: { label: string; checked: boolean; disabled?: boolean } = $props();
</script>

<!-- The whole row is the hit target (A11Y-01, CMP-23) -->
<label class="adl-list__row adl-switch-row">
  <span class="adl-list__title">{label}</span>
  <input class="adl-switch" type="checkbox" role="switch" bind:checked {disabled} />
</label>
