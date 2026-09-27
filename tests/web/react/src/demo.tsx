import { useState } from "react";
import { createRoot } from "react-dom/client";
import { House, Search, Settings, Plus, Ellipsis, Share, Trash2, Library } from "lucide-react";
import { AppShell, type Section } from "./AppShell";
import { Toolbar } from "./Toolbar";
import { Button, IconButton } from "./Button";
import { SwitchRow } from "./Switch";
import { SegmentedPicker } from "./SegmentedPicker";
import { Sheet } from "./Sheet";
import { Alert } from "./Alert";
import { ActionMenu } from "./ActionMenu";
import { ListSection, LinkRow, ActionRow } from "./List";
import { TextField } from "./TextField";
import { usePrefersReducedMotion } from "./hooks";

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
  const reduced = usePrefersReducedMotion();
  return (
    <AppShell sections={sections} currentId="library">
      <Toolbar
        leading={<ActionMenu label="More" icon={<Ellipsis />} items={[
          { label: "Share", icon: <Share />, onSelect: () => {} },
          { label: "Delete All", icon: <Trash2 />, destructive: true, onSelect: () => setAlert(true) },
        ]} />}
        trailing={<IconButton label="Add Book" icon={<Plus />} onClick={() => setSheet(true)} />}
      />
      <h1 className="adl-large-title">Library</h1>
      <div className="adl-grouped">
        <SegmentedPicker label="Sort by" value={sort} onChange={setSort}
          options={[{ value: "recent", title: "Recent" }, { value: "title", title: "Title" }]} />
        <ListSection header="Collections" footer={reduced ? "Reduce Motion is on." : "Tap a collection to open it."}>
          <LinkRow href="#all" title="All Books" value="128" />
          <LinkRow href="#reading" title="Reading Now" value="3" />
        </ListSection>
        <ListSection header="Options">
          <li><SwitchRow label="iCloud Sync" checked={sync} onChange={setSync} /></li>
        </ListSection>
        <ListSection>
          <ActionRow title="Delete All" destructive onSelect={() => setAlert(true)} />
        </ListSection>
        <Button variant="prominent" onClick={() => setSheet(true)}>Add Book</Button>{" "}
        <Button onClick={() => setSort("title")}>Sort by Title</Button>
      </div>
      <Sheet open={sheet} title="New Book" onCancel={() => setSheet(false)}
        confirm={{ label: "Add", onConfirm: () => setSheet(false), disabled: name.trim() === "" }}>
        <TextField label="Title" value={name} onChange={(e) => setName(e.currentTarget.value)}
          hint="Shown on the spine." error={name.length > 40 ? "Use 40 characters or fewer." : undefined} />
      </Sheet>
      <Alert open={alert} title="Delete all books?" message="This removes 128 books from this device."
        actions={[{ label: "Cancel", role: "cancel", onSelect: () => setAlert(false) },
                  { label: "Delete", role: "destructive", onSelect: () => setAlert(false) }]} />
    </AppShell>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
