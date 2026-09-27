import { House, Library, Search, Settings } from "lucide-react";
import { AppNav, type Section } from "../../components/AppNav";

const sections: Section[] = [
  { title: "Home", href: "/", icon: <House /> },
  { title: "Library", href: "/library", icon: <Library /> },
  { title: "Search", href: "/search", icon: <Search /> },
  { title: "Settings", href: "/settings", icon: <Settings /> },
];

// A Server Component: only AppNav ships JavaScript, because it reads the pathname.
export default function TabsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="adl-app">
      <div className="adl-app__layout">
        <AppNav sections={sections} />
        <main className="adl-app__main">{children}</main>
      </div>
    </div>
  );
}
