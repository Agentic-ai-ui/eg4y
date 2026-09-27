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
