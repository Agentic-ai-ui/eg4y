# Vue and Svelte recipes

> Part of the **apple-design-language** skill — Created by Edison Augustin X.
> Vue 3.5 (`<script setup>`, TypeScript) · Svelte 5 (runes) · Same classes and behavior as the [React recipes](react-recipes.md) and [HTML + CSS](html-css-recipes.md); principles in [`web-adaptation.md`](web-adaptation.md).

Both frameworks use the shared [`tokens.css`](../assets/tokens.css) and [`components.css`](../assets/components.css), so a Vue or Svelte app looks and behaves exactly like its React or plain-HTML twin — only the component logic changes. Each set below was type-checked (`vue-tsc`, `svelte-check`, strict), built with Vite, and run in Chromium with axe-core (WCAG 2.2 AA) at phone and tablet widths in light, dark, Increase Contrast, and Reduce Motion, including keyboard checks of the sheet, alert, menu, switch, and segmented control.

## Contents
1. [Setup](#1-setup)
2. [Vue](#2-vue)
3. [Svelte](#3-svelte)
4. [Nuxt and SvelteKit notes](#4-nuxt-and-sveltekit-notes)

---

## 1. Setup

Copy `tokens.css` and `components.css` into your project and import them once (Vue: `main.ts`; Svelte: the root component or `+layout.svelte`). Keep the viewport and color-scheme metadata from [`web-adaptation.md` › Setup](web-adaptation.md#3-setup). For icons, use an open-licensed set (`lucide-vue-next`, `@lucide/svelte`, Phosphor, Heroicons…) — never SF Symbols on the web (BRD-03).

## 2. Vue

### Media queries

```ts
import { onScopeDispose, readonly, ref, type Ref } from "vue";

/** Reactive CSS media query. Starts at `serverValue` where `window` is missing (SSR). */
export function useMediaQuery(query: string, serverValue = false): Readonly<Ref<boolean>> {
  const matches = ref(serverValue);
  if (typeof window !== "undefined") {
    const list = window.matchMedia(query);
    const update = () => (matches.value = list.matches);
    update();
    list.addEventListener("change", update);
    onScopeDispose(() => list.removeEventListener("change", update));
  }
  return readonly(matches);
}

export const usePrefersReducedMotion = () => useMediaQuery("(prefers-reduced-motion: reduce)");
export const usePrefersMoreContrast = () => useMediaQuery("(prefers-contrast: more)");
```

### App shell: tab bar ⇄ sidebar (NAV-06, SYNC-01)

```vue
<script setup lang="ts">
import type { Component } from "vue";

export type Section = { id: string; title: string; href: string; icon: Component };
defineProps<{ sections: readonly Section[]; currentId: string }>();
</script>

<template>
  <div class="adl-app">
    <div class="adl-app__layout">
      <nav class="adl-nav adl-glass" aria-label="Primary">
        <ul class="adl-nav__list">
          <li v-for="s in sections" :key="s.id">
            <a class="adl-nav__link" :href="s.href" :aria-current="s.id === currentId ? 'page' : undefined">
              <component :is="s.icon" aria-hidden="true" />
              <span>{{ s.title }}</span>
            </a>
          </li>
        </ul>
      </nav>
      <main class="adl-app__main"><slot /></main>
    </div>
  </div>
</template>
```

### Switch row and segmented control (CMP-23 – CMP-25)

```vue
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
```

```vue
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
```

### Sheet (CMP-07 – CMP-09)

```vue
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
```

### Alert (CMP-11 – CMP-13)

```vue
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
```

### Menu (CMP-16, CMP-17)

```vue
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
```

### A screen

```vue
<script setup lang="ts">
import { ref } from "vue";
import { House, Library, Search, Settings, Plus, Ellipsis } from "lucide-vue-next";
import AppShell, { type Section } from "./AppShell.vue";
import SwitchRow from "./SwitchRow.vue";
import SegmentedPicker from "./SegmentedPicker.vue";
import Sheet from "./Sheet.vue";
import Alert from "./Alert.vue";
import ActionMenu from "./ActionMenu.vue";
import { usePrefersReducedMotion } from "./useMediaQuery";

const sections: Section[] = [
  { id: "home", title: "Home", href: "#home", icon: House },
  { id: "library", title: "Library", href: "#library", icon: Library },
  { id: "search", title: "Search", href: "#search", icon: Search },
  { id: "settings", title: "Settings", href: "#settings", icon: Settings },
];
const sync = ref(true);
const sort = ref<"recent" | "title">("recent");
const sheet = ref(false);
const alert = ref(false);
const name = ref("");
const reduced = usePrefersReducedMotion();
</script>

<template>
  <AppShell :sections="sections" current-id="library">
    <header class="adl-toolbar adl-glass">
      <div class="adl-toolbar__leading">
        <ActionMenu label="More" :icon="Ellipsis" :items="[
          { label: 'Share', onSelect: () => {} },
          { label: 'Delete All', destructive: true, onSelect: () => (alert = true) },
        ]" />
      </div>
      <span class="adl-toolbar__title"></span>
      <div class="adl-toolbar__trailing">
        <button type="button" class="adl-icon-button" aria-label="Add Book" title="Add Book" @click="sheet = true">
          <Plus aria-hidden="true" />
        </button>
      </div>
    </header>
    <h1 class="adl-large-title">Library</h1>
    <div class="adl-grouped">
      <SegmentedPicker v-model="sort" label="Sort by" :options="[{ value: 'recent', title: 'Recent' }, { value: 'title', title: 'Title' }]" />
      <section class="adl-list-section">
        <h2 class="adl-list-section__header">Collections</h2>
        <ul class="adl-list" role="list">
          <li><a class="adl-list__row adl-list__row--link" href="#all"><span class="adl-list__title">All Books</span><span class="adl-list__value">128</span></a></li>
          <li><a class="adl-list__row adl-list__row--link" href="#reading"><span class="adl-list__title">Reading Now</span><span class="adl-list__value">3</span></a></li>
        </ul>
        <p class="adl-list-section__footer">{{ reduced ? "Reduce Motion is on." : "Tap a collection to open it." }}</p>
      </section>
      <section class="adl-list-section">
        <h2 class="adl-list-section__header">Options</h2>
        <ul class="adl-list" role="list"><li><SwitchRow v-model="sync" label="iCloud Sync" /></li></ul>
      </section>
      <section class="adl-list-section">
        <ul class="adl-list" role="list">
          <li><button type="button" class="adl-list__row adl-list__row--destructive" @click="alert = true">Delete All</button></li>
        </ul>
      </section>
      <button type="button" class="adl-button adl-button--prominent" @click="sheet = true">Add Book</button>
      <button type="button" class="adl-button" @click="sort = 'title'">Sort by Title</button>
    </div>
    <Sheet :open="sheet" title="New Book" confirm-label="Add" :confirm-disabled="name.trim() === ''" @cancel="sheet = false" @confirm="sheet = false">
      <div class="adl-field">
        <label class="adl-field__label" for="book-title">Title</label>
        <input id="book-title" v-model="name" class="adl-field__input" aria-describedby="book-title-hint" />
        <p id="book-title-hint" class="adl-field__hint">Shown on the spine.</p>
      </div>
    </Sheet>
    <Alert :open="alert" title="Delete all books?" message="This removes 128 books from this device." :actions="[
      { label: 'Cancel', role: 'cancel', onSelect: () => (alert = false) },
      { label: 'Delete', role: 'destructive', onSelect: () => (alert = false) },
    ]" />
  </AppShell>
</template>
```

## 3. Svelte

### Media queries

Svelte 5.7+ includes reactive media queries (`MediaQuery` in `svelte/reactivity`) and a ready-made `prefersReducedMotion` in `svelte/motion` — no custom store needed.

```ts
import { MediaQuery } from "svelte/reactivity";

// Svelte 5.7+ ships reactive media queries; `prefersReducedMotion` is also exported from "svelte/motion".
export { prefersReducedMotion } from "svelte/motion";
export const prefersMoreContrast = new MediaQuery("prefers-contrast: more");
export const prefersDark = new MediaQuery("prefers-color-scheme: dark");
```

### App shell: tab bar ⇄ sidebar (NAV-06, SYNC-01)

```svelte
<script lang="ts" module>
  import type { Component, Snippet } from "svelte";
  export type Section = { id: string; title: string; href: string; icon: Component };
</script>

<script lang="ts">
  let { sections, currentId, children }: { sections: readonly Section[]; currentId: string; children: Snippet } = $props();
</script>

<div class="adl-app">
  <div class="adl-app__layout">
    <nav class="adl-nav adl-glass" aria-label="Primary">
      <ul class="adl-nav__list">
        {#each sections as s (s.id)}
          <li>
            <a class="adl-nav__link" href={s.href} aria-current={s.id === currentId ? "page" : undefined}>
              <s.icon aria-hidden="true" />
              <span>{s.title}</span>
            </a>
          </li>
        {/each}
      </ul>
    </nav>
    <main class="adl-app__main">{@render children()}</main>
  </div>
</div>
```

### Switch row and segmented control (CMP-23 – CMP-25)

```svelte
<script lang="ts">
  let { label, checked = $bindable(), disabled = false }: { label: string; checked: boolean; disabled?: boolean } = $props();
</script>

<!-- The whole row is the hit target (A11Y-01, CMP-23) -->
<label class="adl-list__row adl-switch-row">
  <span class="adl-list__title">{label}</span>
  <input class="adl-switch" type="checkbox" role="switch" bind:checked {disabled} />
</label>
```

```svelte
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
```

### Sheet (CMP-07 – CMP-09)

```svelte
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
```

### Alert (CMP-11 – CMP-13)

`autofocus` is deliberate here — it implements the HIG’s rule that Cancel is never the default — so the compiler’s `a11y_autofocus` warning is silenced with a comment.

```svelte
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
```

### Menu (CMP-16, CMP-17)

`$props.id()` must be a plain top-level initializer, so derive the menu id in a second step.

```svelte
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
```

### A screen

```svelte
<script lang="ts">
  import { House, Library, Search, Settings, Plus, Ellipsis } from "@lucide/svelte";
  import AppShell, { type Section } from "./AppShell.svelte";
  import SwitchRow from "./SwitchRow.svelte";
  import SegmentedPicker from "./SegmentedPicker.svelte";
  import Sheet from "./Sheet.svelte";
  import Alert from "./Alert.svelte";
  import ActionMenu from "./ActionMenu.svelte";
  import { prefersReducedMotion } from "./media";

  const sections: Section[] = [
    { id: "home", title: "Home", href: "#home", icon: House },
    { id: "library", title: "Library", href: "#library", icon: Library },
    { id: "search", title: "Search", href: "#search", icon: Search },
    { id: "settings", title: "Settings", href: "#settings", icon: Settings },
  ];
  let sync = $state(true);
  let sort = $state<"recent" | "title">("recent");
  let sheet = $state(false);
  let alert = $state(false);
  let name = $state("");
</script>

<AppShell {sections} currentId="library">
  <header class="adl-toolbar adl-glass">
    <div class="adl-toolbar__leading">
      <ActionMenu label="More" icon={Ellipsis} items={[
        { label: "Share", onSelect: () => {} },
        { label: "Delete All", destructive: true, onSelect: () => (alert = true) },
      ]} />
    </div>
    <span class="adl-toolbar__title"></span>
    <div class="adl-toolbar__trailing">
      <button type="button" class="adl-icon-button" aria-label="Add Book" title="Add Book" onclick={() => (sheet = true)}>
        <Plus aria-hidden="true" />
      </button>
    </div>
  </header>
  <h1 class="adl-large-title">Library</h1>
  <div class="adl-grouped">
    <SegmentedPicker bind:value={sort} label="Sort by" options={[{ value: "recent", title: "Recent" }, { value: "title", title: "Title" }]} />
    <section class="adl-list-section">
      <h2 class="adl-list-section__header">Collections</h2>
      <ul class="adl-list" role="list">
        <li><a class="adl-list__row adl-list__row--link" href="#all"><span class="adl-list__title">All Books</span><span class="adl-list__value">128</span></a></li>
        <li><a class="adl-list__row adl-list__row--link" href="#reading"><span class="adl-list__title">Reading Now</span><span class="adl-list__value">3</span></a></li>
      </ul>
      <p class="adl-list-section__footer">{prefersReducedMotion.current ? "Reduce Motion is on." : "Tap a collection to open it."}</p>
    </section>
    <section class="adl-list-section">
      <h2 class="adl-list-section__header">Options</h2>
      <ul class="adl-list" role="list"><li><SwitchRow bind:checked={sync} label="iCloud Sync" /></li></ul>
    </section>
    <section class="adl-list-section">
      <ul class="adl-list" role="list">
        <li><button type="button" class="adl-list__row adl-list__row--destructive" onclick={() => (alert = true)}>Delete All</button></li>
      </ul>
    </section>
    <button type="button" class="adl-button adl-button--prominent" onclick={() => (sheet = true)}>Add Book</button>
    <button type="button" class="adl-button" onclick={() => (sort = "title")}>Sort by Title</button>
  </div>
  <Sheet open={sheet} title="New Book" confirmLabel="Add" confirmDisabled={name.trim() === ""} oncancel={() => (sheet = false)} onconfirm={() => (sheet = false)}>
    <div class="adl-field">
      <label class="adl-field__label" for="book-title">Title</label>
      <input id="book-title" bind:value={name} class="adl-field__input" aria-describedby="book-title-hint" />
      <p id="book-title-hint" class="adl-field__hint">Shown on the spine.</p>
    </div>
  </Sheet>
  <Alert open={alert} title="Delete all books?" message="This removes 128 books from this device." actions={[
    { label: "Cancel", role: "cancel", onSelect: () => (alert = false) },
    { label: "Delete", role: "destructive", onSelect: () => (alert = false) },
  ]} />
</AppShell>
```

## 4. Nuxt and SvelteKit notes

- **Metadata.** Nuxt: `useHead({ meta: [{ name: "viewport", content: "width=device-width, initial-scale=1, viewport-fit=cover" }, { name: "color-scheme", content: "light dark" }] })` or `app.head` in `nuxt.config`. SvelteKit: put both `<meta>` tags in `src/app.html`. Never add `maximum-scale` or `user-scalable=no` (A11Y-05).
- **Server rendering.** `useMediaQuery` starts at `serverValue` on the server; Svelte’s `MediaQuery` accepts a fallback as its second argument. Appearance, contrast, and motion styling live in CSS, so pages render correctly before hydration.
- **Current route.** Derive `aria-current="page"` from the router (`useRoute()` in Nuxt, `page.url.pathname` from `$app/state` in SvelteKit) and pass the router’s link component the same class.
