#!/usr/bin/env python3
"""Tests for the Apple Design Language hooks — Created by Edison Augustin X.

Run:  python3 -m unittest discover -s hooks/tests -v
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

HOOKS = Path(__file__).resolve().parents[1]
ROOT = HOOKS.parent
SCRIPTS = HOOKS / "scripts"
sys.path.insert(0, str(SCRIPTS))

import hig_lint  # noqa: E402
import prompt_router  # noqa: E402
import session_context  # noqa: E402

RULES = hig_lint.load_rules()
SYSTEM_HEX = hig_lint.load_system_hex()


class LintCase(unittest.TestCase):
    """Helpers: write a temp file, lint it, and inspect rule IDs."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def lint(self, name: str, content: str) -> list[hig_lint.Finding]:
        path = self.dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(content), encoding="utf-8")
        return hig_lint.lint_file(path, RULES, SYSTEM_HEX)

    def rules(self, name: str, content: str) -> set[str]:
        return {f.rule for f in self.lint(name, content)}

    def assertFlags(self, rule: str, name: str, content: str):
        self.assertIn(rule, self.rules(name, content), f"expected {rule} for:\n{content}")

    def assertClean(self, rule: str, name: str, content: str):
        self.assertNotIn(rule, self.rules(name, content), f"did not expect {rule} for:\n{content}")


class CoverageTests(unittest.TestCase):
    def test_every_hook_rule_has_a_detector(self):
        hook_rules = {r["id"] for r in RULES.values() if r["check"] == "hook"}
        self.assertEqual(hook_rules, hig_lint.DETECTED_RULES)

    def test_list_rules_exits_zero(self):
        out = subprocess.run([sys.executable, str(SCRIPTS / "hig_lint.py"), "--list-rules"], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertNotIn("MISSING", out.stdout)

    def test_severity_comes_from_rules_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "V.swift"
            p.write_text('Text("x").preferredColorScheme(.dark)\n')
            f = hig_lint.lint_file(p, RULES, SYSTEM_HEX)[0]
            self.assertEqual(f.severity, RULES["COL-07"]["severity"])
            self.assertTrue(f.link.startswith("rules/04-color.md#col-07"))


class SwiftTests(LintCase):
    def test_lay01_device_checks(self):
        self.assertFlags("LAY-01", "V.swift", "if UIDevice.current.userInterfaceIdiom == .pad { }\n")
        self.assertFlags("LAY-01", "V.swift", "let w = UIScreen.main.bounds.width\n")
        self.assertClean("LAY-01", "V.swift", "@Environment(\\.horizontalSizeClass) var sizeClass\n")

    def test_gls02_and_gls08_glass_usage(self):
        many = "\n".join(f'Image(systemName: "a{i}").glassEffect()' for i in range(5))
        self.assertFlags("GLS-02", "V.swift", many)
        self.assertFlags("GLS-08", "V.swift", 'A().glassEffect()\nB().glassEffect()\n')
        self.assertClean("GLS-08", "V.swift", 'GlassEffectContainer { A().glassEffect(); B().glassEffect() }\n')
        self.assertClean("GLS-02", "V.swift", 'A().glassEffect()\n')

    def test_gls04_custom_bar_backgrounds(self):
        self.assertFlags("GLS-04", "V.swift", ".toolbarBackground(Color.blue, for: .navigationBar)\n")
        self.assertFlags("GLS-04", "V.swift", ".presentationBackground(.thinMaterial)\n")
        self.assertFlags("GLS-04", "V.swift", "let a = UINavigationBarAppearance()\na.configureWithOpaqueBackground()\n")
        self.assertClean("GLS-04", "V.swift", ".toolbarBackground(.hidden, for: .navigationBar)\n")

    def test_col01_color_literals(self):
        self.assertFlags("COL-01", "V.swift", "Text(\"x\").foregroundStyle(Color(red: 0, green: 0.5, blue: 1))\n")
        self.assertFlags("COL-01", "V.swift", "let c = UIColor(red: 1, green: 0, blue: 0, alpha: 1)\n")
        self.assertFlags("COL-01", "V.swift", "let c = #colorLiteral(red: 1, green: 0, blue: 0, alpha: 1)\n")
        self.assertClean("COL-01", "V.swift", "Text(\"x\").foregroundStyle(.secondary).tint(.blue)\n")
        self.assertClean("COL-01", "BrandColors.swift", "static let brand = Color(red: 0.2, green: 0.4, blue: 0.9)\n")

    def test_col07_forced_scheme(self):
        self.assertFlags("COL-07", "V.swift", "RootView().preferredColorScheme(.light)\n")
        self.assertFlags("COL-07", "V.swift", "window.overrideUserInterfaceStyle = .dark\n")

    def test_typ01_typ02_fixed_and_tiny_sizes(self):
        found = self.rules("V.swift", 'Text("x").font(.system(size: 9, weight: .bold))\n')
        self.assertTrue({"TYP-01", "TYP-02"} <= found)
        self.assertFlags("TYP-01", "V.swift", "label.font = UIFont.systemFont(ofSize: 17)\n")
        self.assertClean("TYP-02", "V.swift", 'Text("x").font(.system(size: 13))\n')
        self.assertClean("TYP-01", "V.swift", 'Text("x").font(.body)\n')

    def test_typ02_uses_macos_minimum_for_appkit_files(self):
        code = 'import AppKit\nlet f = NSFont.systemFont(ofSize: 10)\nlet g = Font.system(size: 10)\n'
        self.assertClean("TYP-02", "M.swift", code)
        self.assertFlags("TYP-02", "M.swift", 'import AppKit\nlet g = Font.system(size: 9)\n')

    def test_typ03_light_weights(self):
        self.assertFlags("TYP-03", "V.swift", 'Text("x").fontWeight(.thin)\n')
        self.assertFlags("TYP-03", "V.swift", 'Text("x").font(.system(.body, weight: .ultraLight))\n')
        self.assertClean("TYP-03", "V.swift", 'Text("x").fontWeight(.semibold)\n')

    def test_typ04_system_font_by_name(self):
        self.assertFlags("TYP-04", "V.swift", 'Text("x").font(.custom("SF Pro Display", size: 20, relativeTo: .title))\n')
        self.assertFlags("TYP-04", "V.swift", 'let f = UIFont(name: "SFPro-Regular", size: 17)\n')

    def test_typ05_custom_font_scaling(self):
        self.assertFlags("TYP-05", "V.swift", 'Text("x").font(.custom("Brand", size: 17))\n')
        self.assertClean("TYP-05", "V.swift", 'Text("x").font(.custom("Brand", size: 17, relativeTo: .body))\n')
        self.assertFlags("TYP-05", "V.swift", 'label.font = UIFont(name: "Brand", size: 17)\n')
        self.assertClean("TYP-05", "V.swift", 'let base = UIFont(name: "Brand", size: 17)!\nlabel.font = UIFontMetrics(forTextStyle: .body).scaledFont(for: base)\n')

    def test_typ08_line_limit(self):
        self.assertFlags("TYP-08", "V.swift", 'Text(title).lineLimit(1)\n')
        self.assertClean("TYP-08", "V.swift", 'Text(title).lineLimit(3)\n')

    def test_mot02_reduce_motion(self):
        self.assertFlags("MOT-02", "V.swift", 'Button("Go") { withAnimation(.spring) { open.toggle() } }\n')
        self.assertClean("MOT-02", "V.swift", '@Environment(\\.accessibilityReduceMotion) var reduceMotion\nButton("Go") { withAnimation(reduceMotion ? nil : .spring) { open.toggle() } }\n')

    def test_a11y01_small_targets(self):
        code = '''
        Button(action: share) {
            Image(systemName: "square.and.arrow.up")
        }
        .frame(width: 24, height: 24)
        .accessibilityLabel("Share")
        '''
        self.assertFlags("A11Y-01", "V.swift", code)
        self.assertClean("A11Y-01", "V.swift", code.replace(".frame(width: 24, height: 24)", ".frame(width: 44, height: 44)"))
        self.assertClean("A11Y-01", "V.swift", 'Image("logo").frame(width: 24, height: 24).accessibilityHidden(true)\n')

    def test_a11y03_icon_only_buttons(self):
        self.assertFlags("A11Y-03", "V.swift", 'Button(action: share) {\n    Image(systemName: "square.and.arrow.up")\n}\n')
        self.assertFlags("A11Y-03", "V.swift", 'Image(systemName: "gear")\n    .onTapGesture { open() }\n')
        self.assertClean("A11Y-03", "V.swift", 'Button(action: share) {\n    Image(systemName: "square.and.arrow.up")\n}\n.accessibilityLabel("Share")\n')
        self.assertClean("A11Y-03", "V.swift", 'Button("Share", systemImage: "square.and.arrow.up") { share() }\n')
        self.assertClean("A11Y-03", "V.swift", 'Label("Share", systemImage: "square.and.arrow.up")\n')

    def test_a11y04_asset_images(self):
        self.assertFlags("A11Y-04", "V.swift", 'VStack {\n    Image("hero")\n        .resizable()\n}\n')
        self.assertClean("A11Y-04", "V.swift", 'Image("hero").accessibilityLabel("Sunset over Lisbon")\n')
        self.assertClean("A11Y-04", "V.swift", 'Image(decorative: "confetti")\n')

    def test_wrt02_click_here(self):
        self.assertFlags("WRT-02", "V.swift", 'Text("Click here to learn more")\n')
        self.assertFlags("WRT-02", "Localizable.strings", '"cta" = "Click here";\n')

    def test_nav09_text_back_close(self):
        self.assertFlags("NAV-09", "V.swift", 'Button("Back") { dismiss() }\n')
        self.assertFlags("NAV-09", "V.swift", 'Button("‹ Back") { dismiss() }\n')
        self.assertFlags("NAV-09", "V.swift", 'Button { dismiss() } label: { Text("Close") }\n')
        self.assertClean("NAV-09", "V.swift", 'Button(role: .close) { dismiss() }\n')

    def test_cmp13_yes_no(self):
        self.assertFlags("CMP-13", "V.swift", '.alert("Delete?", isPresented: $x) { Button("Yes") { }; Button("No") { } }\n')
        self.assertClean("CMP-13", "V.swift", '.alert("Delete “Trip”?", isPresented: $x) { Button("Delete", role: .destructive) { }; Button("Cancel", role: .cancel) { } }\n')

    def test_cmp21_password_textfield(self):
        self.assertFlags("CMP-21", "V.swift", 'TextField("Password", text: $pw)\n')
        self.assertClean("CMP-21", "V.swift", 'SecureField("Password", text: $pw)\n')

    def test_comments_are_ignored(self):
        self.assertClean("COL-07", "V.swift", '// Avoid .preferredColorScheme(.light) here\n/* UIScreen.main.bounds */\n')
        self.assertClean("LAY-01", "V.swift", '/* UIScreen.main.bounds */\n')


class SuppressionTests(LintCase):
    def test_suppression_with_reason_same_line(self):
        self.assertClean("COL-07", "V.swift", 'Player().preferredColorScheme(.dark) // hig-ignore: COL-07 — immersive video stays dark\n')

    def test_suppression_with_reason_line_above(self):
        self.assertClean("COL-07", "V.swift", '// hig-ignore: COL-07 - immersive video stays dark\nPlayer().preferredColorScheme(.dark)\n')

    def test_suppression_without_reason_is_ignored(self):
        self.assertFlags("COL-07", "V.swift", 'Player().preferredColorScheme(.dark) // hig-ignore: COL-07\n')

    def test_suppression_only_covers_named_rule(self):
        self.assertFlags("TYP-02", "V.swift", 'Text("x").font(.system(size: 9)) // hig-ignore: TYP-01 — legacy view\n')

    def test_multiple_ids(self):
        self.assertEqual(set(), self.rules("V.swift", 'Text("x").font(.system(size: 9)) // hig-ignore: TYP-01, TYP-02 — watch complication preview\n') & {"TYP-01", "TYP-02"})


class WebTests(LintCase):
    def test_css_tiny_text_and_light_weight(self):
        found = self.rules("s.css", ".legal { font-size: 9px; font-weight: 300; }\n")
        self.assertTrue({"TYP-02", "TYP-03"} <= found)
        self.assertClean("TYP-02", "s.css", ".caption { font-size: 0.75rem; }\n")

    def test_css_bundled_apple_font(self):
        self.assertFlags("TYP-04", "s.css", '@font-face { font-family: "SF Pro"; src: url(SF-Pro.woff2); }\n')
        self.assertClean("TYP-04", "s.css", '@font-face { font-family: "Inter"; src: url(Inter.woff2); }\n')

    def test_css_color_scheme(self):
        self.assertFlags("COL-07", "s.css", ":root { color-scheme: light; }\n")
        self.assertClean("COL-07", "s.css", ":root { color-scheme: light dark; }\n")

    def test_css_hard_coded_system_color(self):
        blue = [h for h, k in SYSTEM_HEX.items() if k == "blue"][0]
        self.assertFlags("COL-01", "s.css", f".link {{ color: {blue}; }}\n")
        self.assertClean("COL-01", "s.css", ".link { color: #123456; }\n")

    def test_css_motion(self):
        self.assertFlags("MOT-02", "s.css", ".card { transition: transform 200ms; }\n")
        self.assertClean("MOT-02", "s.css", ".card { transition: transform 200ms; }\n@media (prefers-reduced-motion: reduce) { .card { transition: none; } }\n")

    def test_css_small_targets(self):
        self.assertFlags("A11Y-01", "s.css", "button.icon { width: 24px; height: 24px; }\n")
        self.assertClean("A11Y-01", "s.css", "button.icon { width: 24px; height: 24px; min-width: 44px; min-height: 44px; }\n")
        self.assertClean("A11Y-01", "s.css", ".badge { width: 16px; height: 16px; }\n")

    def test_html_rules(self):
        html = '''
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
        <meta name="color-scheme" content="light">
        <link rel="preload" href="/fonts/SF-Pro-Text-Regular.woff2" as="font">
        <img src="hero.jpg">
        <button><svg viewBox="0 0 24 24"></svg></button>
        <input name="password" type="text">
        <a href="/pricing">Click here</a>
        '''
        found = self.rules("index.html", html)
        self.assertTrue({"A11Y-05", "COL-07", "TYP-04", "A11Y-04", "A11Y-03", "CMP-21", "WRT-02"} <= found, found)

    def test_html_clean(self):
        html = '''
        <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
        <meta name="color-scheme" content="light dark">
        <img src="hero.jpg" alt="Sunset over Lisbon">
        <img src="divider.svg" alt="">
        <button aria-label="Share"><svg viewBox="0 0 24 24"></svg></button>
        <button>Save</button>
        <input name="password" type="password" autocomplete="current-password">
        '''
        found = self.rules("index.html", html)
        self.assertFalse(found & {"A11Y-05", "COL-07", "A11Y-04", "A11Y-03", "CMP-21"}, found)

    def test_inline_style_block(self):
        self.assertFlags("TYP-02", "index.html", "<style>.tiny { font-size: 8px }</style>\n")

    def test_jsx_rules(self):
        jsx = '''
        const isIPhone = /iPhone|iPad/.test(navigator.userAgent);
        export const Cap = () => <p style={{ fontSize: 9, fontWeight: 300 }}>x</p>;
        export const Icon = () => <button onClick={go}><Icon /></button>;
        '''
        found = self.rules("App.tsx", jsx)
        self.assertTrue({"LAY-01", "TYP-02", "TYP-03", "A11Y-03"} <= found, found)

    def test_styled_components(self):
        self.assertFlags("TYP-02", "Button.ts", "const Small = styled.span`font-size: 9px;`;\n")

    def test_plist_and_font_files(self):
        plist = '<plist><dict><key>UIAppFonts</key><array><string>SF-Pro-Text-Regular.otf</string><string>Brand.otf</string></array></dict></plist>'
        self.assertFlags("TYP-04", "Info.plist", plist)
        font = self.dir / "Fonts" / "SF-Pro-Display-Bold.otf"
        font.parent.mkdir(parents=True, exist_ok=True)
        font.write_bytes(b"\x00")
        self.assertEqual({f.rule for f in hig_lint.lint_file(font, RULES, SYSTEM_HEX)}, {"TYP-04"})

    def test_skill_code_snippets_pass_the_checker(self):
        import re
        refs = ROOT / "skills" / "apple-design-language" / "references"
        count = 0
        for md in sorted(refs.glob("*.md")):
            for i, (lang, code) in enumerate(re.findall(r"```(swift|css|html)\n(.*?)```", md.read_text(encoding="utf-8"), re.S)):
                findings = self.lint(f"{md.stem}-{i:02d}.{lang}", code)
                self.assertEqual([], [(f.rule, f.line, f.message) for f in findings], f"{md.name} snippet {i} ({lang})")
                count += 1
        self.assertGreater(count, 20)

    def test_tokens_css_is_clean(self):
        tokens = ROOT / "skills" / "apple-design-language" / "assets" / "tokens.css"
        self.assertEqual([], hig_lint.lint_file(tokens, RULES, SYSTEM_HEX))


class CliTests(LintCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(SCRIPTS / "hig_lint.py"), *args], capture_output=True, text=True)

    def test_exit_codes_and_directory_scan(self):
        (self.dir / "ok.swift").write_text('Text("Hi").font(.body)\n')
        clean = self.run_cli(str(self.dir))
        self.assertEqual(clean.returncode, 0, clean.stdout)
        (self.dir / "bad.swift").write_text('Text("Hi").preferredColorScheme(.light)\n')
        bad = self.run_cli(str(self.dir))
        self.assertEqual(bad.returncode, 1)
        self.assertIn("COL-07", bad.stdout)

    def test_json_format(self):
        (self.dir / "bad.swift").write_text('Text("Hi").lineLimit(1)\n')
        out = self.run_cli("--format", "json", str(self.dir))
        data = json.loads(out.stdout)
        self.assertEqual(data["files_checked"], 1)
        self.assertEqual(data["findings"][0]["rule"], "TYP-08")
        self.assertEqual(out.returncode, 0)  # warnings only


class HookProtocolTests(LintCase):
    """Exercise the exact stdin/stdout contract Claude Code uses for PostToolUse."""

    def hook(self, payload: dict, env: dict | None = None) -> subprocess.CompletedProcess:
        e = {**os.environ, **(env or {})}
        return subprocess.run([sys.executable, str(SCRIPTS / "hig_lint.py"), "--hook"], input=json.dumps(payload),
                              capture_output=True, text=True, env=e)

    def payload(self, path: Path) -> dict:
        return {"session_id": "t", "hook_event_name": "PostToolUse", "tool_name": "Write", "cwd": str(self.dir),
                "tool_input": {"file_path": str(path), "content": ""}, "tool_response": {"filePath": str(path)}}

    def test_errors_block_with_reason(self):
        p = self.dir / "V.swift"
        p.write_text('Text("x").font(.system(size: 9))\n')
        out = self.hook(self.payload(p))
        self.assertEqual(out.returncode, 0)
        data = json.loads(out.stdout)
        self.assertEqual(data["decision"], "block")
        self.assertIn("TYP-02", data["reason"])

    def test_warnings_become_additional_context(self):
        p = self.dir / "V.swift"
        p.write_text('Text("x").font(.body).lineLimit(1)\n')
        data = json.loads(self.hook(self.payload(p)).stdout)
        self.assertNotIn("decision", data)
        self.assertEqual(data["hookSpecificOutput"]["hookEventName"], "PostToolUse")
        self.assertIn("TYP-08", data["hookSpecificOutput"]["additionalContext"])

    def test_clean_file_prints_nothing(self):
        p = self.dir / "V.swift"
        p.write_text('Text("x").font(.body)\n')
        out = self.hook(self.payload(p))
        self.assertEqual((out.returncode, out.stdout), (0, ""))

    def test_unsupported_and_missing_files_are_ignored(self):
        p = self.dir / "notes.md"
        p.write_text("click here\n")
        self.assertEqual(self.hook(self.payload(p)).stdout, "")
        self.assertEqual(self.hook(self.payload(self.dir / "missing.swift")).stdout, "")

    def test_min_severity_and_disable(self):
        p = self.dir / "V.swift"
        p.write_text('Text("x").font(.body).lineLimit(1)\n')
        self.assertEqual(self.hook(self.payload(p), {"HIG_LINT_MIN_SEVERITY": "error"}).stdout, "")
        p.write_text('Text("x").preferredColorScheme(.light)\n')
        self.assertEqual(self.hook(self.payload(p), {"HIG_LINT": "off"}).stdout, "")

    def test_bad_input_never_fails(self):
        out = subprocess.run([sys.executable, str(SCRIPTS / "hig_lint.py"), "--hook"], input="not json", capture_output=True, text=True)
        self.assertEqual((out.returncode, out.stdout), (0, ""))

    def test_output_is_capped(self):
        p = self.dir / "V.swift"
        p.write_text("".join(f'Text("x").font(.system(size: 9)) // {i}\n' for i in range(400)))
        data = json.loads(self.hook(self.payload(p)).stdout)
        self.assertLess(len(data["reason"]), 10000)


class PromptRouterTests(unittest.TestCase):
    def test_routes_apple_ui_prompts(self):
        note = prompt_router.route("Build a SwiftUI tab bar with a search tab for iPhone and iPad")
        self.assertIn("apple-design-language", note)
        self.assertIn("navigation.md", note)
        self.assertIn("platforms.md", note)

    def test_web_for_apple_devices(self):
        note = prompt_router.route("make our react web app header feel native on iPhone Safari")
        self.assertIn("web-adaptation.md", note)

    def test_ignores_unrelated_prompts(self):
        self.assertEqual("", prompt_router.route("Write a Python script that parses apple orchard CSV data"))
        self.assertEqual("", prompt_router.route("Fix the failing unit test in the billing service"))

    def test_hook_io(self):
        out = subprocess.run([sys.executable, str(SCRIPTS / "prompt_router.py")],
                             input=json.dumps({"hook_event_name": "UserPromptSubmit", "prompt": "Review my SwiftUI alert copy"}),
                             capture_output=True, text=True)
        self.assertEqual(out.returncode, 0)
        self.assertIn("review-checklist.md", out.stdout)
        self.assertIn("writing.md", out.stdout)


class SessionContextTests(unittest.TestCase):
    def run_hook(self, project: Path) -> str:
        env = {**os.environ, "CLAUDE_PROJECT_DIR": str(project)}
        out = subprocess.run([sys.executable, str(SCRIPTS / "session_context.py")],
                             input=json.dumps({"hook_event_name": "SessionStart", "source": "startup", "cwd": str(project)}),
                             capture_output=True, text=True, env=env)
        self.assertEqual(out.returncode, 0)
        return out.stdout

    def test_brief_in_ui_project(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "App.swift").write_text("import SwiftUI\n")
            out = self.run_hook(Path(d))
            self.assertIn("apple-design-language", out)
            self.assertLess(len(out.splitlines()), 12)

    def test_silent_when_instructions_already_loaded(self):
        self.assertEqual("", self.run_hook(ROOT))

    def test_silent_outside_ui_projects(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "main.go").write_text("package main\n")
            self.assertEqual("", self.run_hook(Path(d)))


class ConfigTests(unittest.TestCase):
    def test_hooks_json_shape(self):
        data = json.loads((HOOKS / "hooks.json").read_text())
        self.assertIn("description", data)
        for event in ("PostToolUse", "UserPromptSubmit", "SessionStart"):
            handlers = [h for group in data["hooks"][event] for h in group["hooks"]]
            for h in handlers:
                self.assertEqual(h["type"], "command")
                script = h["args"][0].replace("${CLAUDE_PLUGIN_ROOT}", str(ROOT))
                self.assertTrue(Path(script).is_file(), script)

    def test_settings_example_points_at_real_scripts(self):
        data = json.loads((HOOKS / "settings.example.json").read_text())
        for event, groups in data["hooks"].items():
            for group in groups:
                for h in group["hooks"]:
                    script = h["args"][0].replace("${CLAUDE_PROJECT_DIR}", str(ROOT))
                    self.assertTrue(Path(script).is_file(), script)


if __name__ == "__main__":
    unittest.main()
