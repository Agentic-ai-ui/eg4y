# 12 · Patterns, privacy, and generative AI (`PAT`, `PRV`, `AI`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §14. Format and severities: [`README.md`](README.md).

---

## Experience patterns

### PAT-01 · Launch screens are not splash screens
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** iOS, iPadOS, tvOS
- **Check:** review
- **Rule:** MUST NOT advertise or brand on the launch screen; it SHOULD be nearly identical to the first screen, contain no text, and match the current orientation and appearance.
- **Source:** [HIG › Launching](https://developer.apple.com/design/human-interface-guidelines/launching) · [HIG › Branding](https://developer.apple.com/design/human-interface-guidelines/branding) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### PAT-02 · Make onboarding fast, interactive, optional
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD teach through interaction and contextual tips, keep required flows brief, make tutorials skippable and findable later, postpone nonessential setup, and ask for ratings or purchases only after people engage.
- **Source:** [HIG › Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### PAT-03 · Show something immediately
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD show placeholder content right away while loading, let people keep working during loads, and download large assets in the background.
- **Source:** [HIG › Loading](https://developer.apple.com/design/human-interface-guidelines/loading) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### PAT-04 · Match feedback to significance
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD integrate status feedback inline, warn only about unexpected and irreversible data loss, confirm only significant completions, explain why a command can’t run, and deliver feedback through more than one channel.
- **Source:** [HIG › Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### PAT-05 · Keep settings minimal and expected
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD ship great defaults, minimize settings, open settings with ⌘, where a keyboard exists, detect information instead of asking for it, and put task-specific options in the task itself.
- **Source:** [HIG › Settings](https://developer.apple.com/design/human-interface-guidelines/settings) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### PAT-06 · Make undo predictable
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** SHOULD support multiple levels of undo and redo through system mechanisms, describe what will be undone (“Undo Typing”), and reveal the result even when it’s off screen.
- **Source:** [HIG › Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### PAT-07 · Minimize data entry
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD gather information from the system when possible, offer choices instead of typing, support paste and drag and drop, validate as people type, and enable Next or Continue only when required data is present.
- **Source:** [HIG › Entering data](https://developer.apple.com/design/human-interface-guidelines/entering-data) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### PAT-08 · Full screen stays in people’s control
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS
- **Check:** review
- **Rule:** SHOULD let people choose when to enter and exit full screen, keep essential controls reachable, let the Dock appear (except in games), and resume where people left off.
- **Source:** [HIG › Going full screen](https://developer.apple.com/design/human-interface-guidelines/going-full-screen) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

## Privacy

### PRV-01 · Request permission in context
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD request only the data a feature needs, at the moment people use that feature, and avoid launch-time requests unless the app can’t function without the data.
- **Source:** [HIG › Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### PRV-02 · Write specific purpose strings
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD write each purpose string as one brief, specific, active sentence in sentence case ending with a period (“The app records during the night to detect snoring sounds.”).
- **Source:** [HIG › Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### PRV-03 · Pre-permission screens: one honest button
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST NOT add actions other than a single “Continue” or “Next” button to a custom screen shown before a permission alert (no “Allow”, no cancel or close), unless required for legal consent.
- **Source:** [HIG › Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### PRV-04 · Never mislead before the tracking prompt
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST NOT precede the App Tracking Transparency alert with screens that offer incentives, imitate a request, show an image of the alert, or annotate it — these cause App Review rejection.
- **Source:** [HIG › Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### PRV-05 · Use system authentication and secure storage
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST NOT store passwords or secrets in plain text; SHOULD prefer passkeys, Sign in with Apple, Password AutoFill, and Face ID/Touch ID/Optic ID over custom schemes, and keep secrets in the keychain.
- **Source:** [HIG › Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

## Generative AI

### AI-01 · Disclose AI; never impersonate humans
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST NOT lead people to think they’re interacting with, or viewing content authored by, a human when it’s AI; clearly identify where the app uses AI and what it can and can’t do.
- **Source:** [HIG › Generative AI](https://developer.apple.com/design/human-interface-guidelines/generative-ai) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### AI-02 · Keep people in control of results
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD let people dismiss, edit, undo, retry, or adjust generated content with controls near the result, and acknowledge when their corrections take effect.
- **Source:** [HIG › Generative AI](https://developer.apple.com/design/human-interface-guidelines/generative-ai) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### AI-03 · Confirm before significant actions
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD NOT automate destructive or hard-to-undo actions (deleting data, purchases); ask for confirmation before acting on someone’s behalf.
- **Source:** [HIG › Generative AI](https://developer.apple.com/design/human-interface-guidelines/generative-ai) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### AI-04 · Protect privacy in AI features
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD prefer on-device models, ask permission before using personal data, minimize and disclose what’s sent to servers or used for training, and offer a clear opt-out.
- **Source:** [HIG › Generative AI](https://developer.apple.com/design/human-interface-guidelines/generative-ai) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### AI-05 · Limit and disclose hallucination risk
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD scope generation narrowly, avoid requesting facts the model can’t verify, communicate that AI output may contain errors, and avoid AI content where a mistake could cause harm.
- **Source:** [HIG › Generative AI](https://developer.apple.com/design/human-interface-guidelines/generative-ai) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### AI-06 · Design the waiting and fallback experience
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD show specific progress messages (“Summarizing key themes from your notes”), consider offering alternative results, provide voluntary feedback controls, coach people when requests are blocked, and keep a non-AI fallback when possible.
- **Source:** [HIG › Generative AI](https://developer.apple.com/design/human-interface-guidelines/generative-ai) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)
