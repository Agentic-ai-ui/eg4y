<script lang="ts" module>
  export type MenuItem = { label: string; destructive?: boolean; onSelect: () => void };
</script>

<script lang="ts">
  import type { Component } from "svelte";

  let { label, icon: Icon, items }: { label: string; icon: Component; items: readonly MenuItem[] } = $props();
  const uid = $props.id();
  const menuId = `menu-${uid.replace(/[^a-zA-Z0-9_-]/g, "")}`;
  let menu: HTMLDivElement;
</script>

<button
  type="button"
  class="adl-icon-button"
  aria-label={label}
  title={label}
  popovertarget={menuId}
  style:anchor-name="--{menuId}"
>
  <Icon aria-hidden="true" />
</button>
<div id={menuId} bind:this={menu} popover="auto" class="adl-menu adl-glass" style:position-anchor="--{menuId}">
  {#each items as item (item.label)}
    <button
      type="button"
      class={["adl-menu__item", item.destructive && "adl-menu__item--destructive"]}
      onclick={() => {
        menu.hidePopover();
        item.onSelect();
      }}
    >{item.label}</button>
  {/each}
</div>
