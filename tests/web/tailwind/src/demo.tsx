import { useState } from "react";
import { createRoot } from "react-dom/client";
import { House, Search, Settings, Plus, Ellipsis, Library } from "lucide-react";
import { AppShell, type Section } from "./AppShell";
import { Button } from "./Button";
import { ListSection, LinkRow, ActionRow, SwitchRow } from "./List";
import { Sheet } from "./Sheet";
import { Alert } from "../../react/src/Alert";
import { ActionMenu } from "../../react/src/ActionMenu";
import { SegmentedPicker } from "../../react/src/SegmentedPicker";
import { TextField } from "../../react/src/TextField";
import "./app.css";

const sections = [
  { id: "home", title: "Home", href: "#home", icon: <House /> },
  { id: "library", title: "Library", href: "#library", icon: <Library /> },
  { id: "search", title: "Search", href: "#search", icon: <Search /> },
  { id: "settings", title: "Settings", href: "#settings", icon: <Settings /> },
] as const satisfies readonly Section[];

function App() {
  const [sync, setSync] = useState(true);
  const [sort, setSort] = useState<"recent" | "title">("recent");
  const [sheet, setSheet] = useState(false);
  const [alert, setAlert] = useState(false);
  const [name, setName] = useState("");
  return (
    <AppShell sections={sections} currentId="library">
      <header className="adl-glass sticky top-0 z-5 flex min-h-control items-center gap-2 border-0 border-b px-4 py-2">
        <div className="flex flex-1 items-center gap-1">
          <ActionMenu label="More" icon={<Ellipsis />} items={[
            { label: "Share", onSelect: () => {} },
            { label: "Delete All", destructive: true, onSelect: () => setAlert(true) },
          ]} />
        </div>
        <div className="flex flex-1 items-center justify-end gap-1">
          <button type="button" aria-label="Add Book" title="Add Book" onClick={() => setSheet(true)}
            className="grid min-h-control min-w-control place-items-center rounded-full text-accent-text active:bg-fill">
            <Plus aria-hidden="true" />
          </button>
        </div>
      </header>
      <h1 className="mx-[16px] mt-2 mb-3 text-large-title font-bold hyphens-auto">Library</h1>
      <div className="bg-background-grouped px-[16px] pt-1 pb-6">
        <SegmentedPicker label="Sort by" value={sort} onChange={setSort}
          options={[{ value: "recent", title: "Recent" }, { value: "title", title: "Title" }]} />
        <ListSection header="Collections" footer="Tap a collection to open it.">
          <LinkRow href="#all" title="All Books" value="128" />
          <LinkRow href="#reading" title="Reading Now" value="3" />
        </ListSection>
        <ListSection header="Options">
          <SwitchRow label="iCloud Sync" checked={sync} onChange={setSync} />
        </ListSection>
        <ListSection>
          <ActionRow title="Delete All" destructive onSelect={() => setAlert(true)} />
        </ListSection>
        <div className="flex gap-2">
          <Button variant="prominent" onClick={() => setSheet(true)}>Add Book</Button>
          <Button onClick={() => setSort("title")}>Sort by Title</Button>
        </div>
      </div>
      <Sheet open={sheet} title="New Book" onCancel={() => setSheet(false)}
        confirm={{ label: "Add", onConfirm: () => setSheet(false), disabled: name.trim() === "" }}>
        <TextField label="Title" value={name} onChange={(e) => setName(e.currentTarget.value)} hint="Shown on the spine." />
      </Sheet>
      <Alert open={alert} title="Delete all books?" message="This removes 128 books from this device."
        actions={[{ label: "Cancel", role: "cancel", onSelect: () => setAlert(false) },
                  { label: "Delete", role: "destructive", onSelect: () => setAlert(false) }]} />
    </AppShell>
  );
}
createRoot(document.getElementById("root")!).render(<App />);
