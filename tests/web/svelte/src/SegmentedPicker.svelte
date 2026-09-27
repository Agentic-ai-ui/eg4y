<script lang="ts" generics="T extends string">
  let { label, options, value = $bindable() }: { label: string; options: readonly { value: T; title: string }[]; value: T } = $props();
  const name = $props.id();
</script>

<fieldset class="adl-segmented">
  <legend class="adl-visually-hidden">{label}</legend>
  {#each options as o (o.value)}
    <label class="adl-segmented__option">
      <input type="radio" {name} value={o.value} bind:group={value} />
      {o.title}
    </label>
  {/each}
</fieldset>
