<script setup lang="ts">
import { useId, useTemplateRef, type Component } from "vue";

export type MenuItem = { label: string; destructive?: boolean; onSelect: () => void };
defineProps<{ label: string; icon: Component; items: readonly MenuItem[] }>();
const menuId = `menu-${useId().replace(/[^a-zA-Z0-9_-]/g, "")}`;
const anchor = `--${menuId}`;
const menu = useTemplateRef<HTMLDivElement>("menu");

function select(item: MenuItem) {
  menu.value?.hidePopover();
  item.onSelect();
}
</script>

<template>
  <button
    type="button"
    class="adl-icon-button"
    :aria-label="label"
    :title="label"
    :popovertarget="menuId"
    :style="{ anchorName: anchor }"
  >
    <component :is="icon" aria-hidden="true" />
  </button>
  <div :id="menuId" ref="menu" popover="auto" class="adl-menu adl-glass" :style="{ positionAnchor: anchor }">
    <button
      v-for="item in items"
      :key="item.label"
      type="button"
      :class="['adl-menu__item', { 'adl-menu__item--destructive': item.destructive }]"
      @click="select(item)"
    >{{ item.label }}</button>
  </div>
</template>
