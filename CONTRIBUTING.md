# Contributing

Thanks for wanting to help improve *Build Apps with AI*. This page tells you the fastest way to get your contribution accepted.

There are three ways to contribute, depending on what you want to do.

---

## 1. Report a problem with the book

**Use this when:** something in the book doesn't work, an error message isn't covered, a tool's UI has changed, or a step is unclear.

1. Go to the [Issues tab](../../issues)
2. Click **New issue** → choose **"Something in the book isn't working"**
3. Fill in the template (chapter, step, what you expected, what happened, error message, what you've tried)
4. Submit

You do not need a GitHub account beyond the free one. You do not need to know Git. **This is the most useful contribution most readers will make.**

---

## 2. Suggest an improved prompt

**Use this when:** you've found a way to write one of the book's prompts that produces noticeably better results from Claude Code.

1. Go to the [Issues tab](../../issues)
2. Click **New issue** → choose **"I found a better prompt"**
3. Paste the original prompt, your improved version, and what makes it better
4. Submit

If the new version is clearly better, it will be added to the chapter's prompts folder and credited to you, and may make it into the next book revision.

---

## 3. Submit a Pull Request

**Use this when:** you've fixed a typo in a prompt, improved the README, added a missing chapter file, or made any other concrete change you want merged.

If you've used GitHub before, the flow is standard:

1. **Fork** this repo (button at the top right of GitHub)
2. **Clone** your fork locally
3. Create a branch: `git checkout -b fix/typo-in-chapter-7-prompt-2`
4. Make your change, commit, push
5. Open a **Pull Request** against this repo's `main` branch

If you haven't used GitHub before, **option 1 or 2 above is much easier**. Opening an issue is the same outcome with less work.

### What I'm likely to merge fast

- Typo fixes in prompts or README
- Updated commands when a tool's CLI changes (e.g., new flag names)
- Errata additions citing a specific book reference
- Issue template improvements

### What I'll want to discuss first

- Restructuring of the `prompts/` folder layout
- Major rewrites of the README
- New top-level files (open an issue first to discuss the addition)

### What I'll politely decline

- Stylistic preferences without a functional reason
- Sweeping reformatting (e.g., "convert all prompts to YAML")
- Code samples for a different tech stack (this book is React Native + Expo + Firebase; alternatives belong in your own repo, which I'd be happy to link)

---

## Code of conduct

Be kind. Most readers of this book are first-time builders trying to learn. Treat their questions and PRs with the patience you wanted when you were starting out.

Disrespectful comments (toward readers, contributors, or referenced tools and companies) will be removed. Repeat offenders will be blocked from the repo.

---

## Questions?

If you're not sure whether something belongs in an issue, a PR, or a discussion, just open it in [Discussions](../../discussions) and ask. There's no wrong door.
