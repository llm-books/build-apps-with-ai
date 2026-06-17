# Errata — Build Apps with AI

This page tracks corrections, clarifications, and version-specific notes for the book.

If you spot something missing from this list, **please open an issue** so the next reader doesn't get stuck on the same thing.

---

## Edition 1 (first printing, 2026)

*No errata yet — this page will populate as readers report issues.*

---

## How errata get added

When a reader opens an issue and the report is confirmed:

1. The fix is posted here, citing the chapter, page (if known), and what to do differently
2. The book itself is updated in the next revision (every 2–4 months typically)
3. The changelog (`changelog.md`) records that the change was made

---

## Tool-version notes

These aren't book bugs — they're things that may change with new tool versions.

### Expo SDK

- The book targets Expo SDK 53+
- If you're on a newer SDK, most prompts work as-is; Claude Code handles version differences automatically
- If you hit "package X is incompatible with SDK Y" errors, run `npx expo install --check` and let it fix the dependency versions

### Claude Code

- The book assumes Claude Code's current interactive UI (numbered permission prompts, arrow-key selection, `/clear` and `/exit` commands)
- If Anthropic changes the interactive UX significantly, errata will be added here

### Firebase Console

- Firebase redesigns its console roughly once a year
- The general flow stays the same: create project → add web app → enable Authentication → create Firestore
- If the specific button labels in Chapter 12 don't match what you see, look for similarly-named options in the same area

### Google Play / Apple App Store

- App store policies and submission flows change frequently
- The high-level steps in Chapters 18 and 19 remain correct, but specific menus may have moved
- When in doubt, search Google for "[store name] [current year] submit app guide" for the latest walkthrough
