<script setup lang="ts">
import { ref } from "vue";
import { House, Library, Search, Settings, Plus, Ellipsis } from "@lucide/vue";
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
