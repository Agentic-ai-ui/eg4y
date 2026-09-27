import type { Metadata, Viewport } from "next";
import "./tokens.css";
import "./components.css";

// Server Component: viewport and metadata exports are only supported here.
export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover", // lets env(safe-area-inset-*) report real insets (LAY-02)
  colorScheme: "light dark", // follow the system appearance (COL-07)
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#FFFFFF" },
    { media: "(prefers-color-scheme: dark)", color: "#000000" },
  ],
  // Never set maximumScale or userScalable: people must be able to zoom (A11Y-05).
};

export const metadata: Metadata = {
  title: "Library",
  appleWebApp: { capable: true, title: "Library", statusBarStyle: "default" },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
