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
