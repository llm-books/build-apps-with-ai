#!/usr/bin/env python3
"""Extract every \\begin{prompt}...\\end{prompt} block from the LaTeX chapter
files and write one cleanly-formatted Markdown file per prompt, under
prompts/chapter-NN/NN-slug.md. Also generates prompts/README.md as an index.

Usage: python3 extract-prompts.py
"""
import re
import sys
from pathlib import Path
from textwrap import dedent

# --- Configuration ---------------------------------------------------------
LATEX_CHAPTERS = Path("/Users/haderom/Documents/books/my book/latex/chapters")
REPO = Path(__file__).resolve().parent
PROMPTS = REPO / "prompts"

# Skip-list: prompts that aren't useful to readers
# (none currently; placeholder for future)
SKIP_KEYWORDS = []


# --- LaTeX → Markdown cleanup ----------------------------------------------

def unwrap_paragraphs(s: str) -> str:
    """Unwrap hard-line-wrapped paragraphs from pandoc's LaTeX output.
    A blank line still separates paragraphs; single newlines inside a
    paragraph become spaces."""
    paragraphs = re.split(r"\n\s*\n", s)
    unwrapped = []
    for p in paragraphs:
        # Don't unwrap if it contains list markers or env begin/end —
        # those need their newline structure to be parsed correctly.
        if re.search(r"\\begin\{|\\end\{|\\item", p):
            unwrapped.append(p)
        else:
            unwrapped.append(re.sub(r"\s*\n\s*", " ", p).strip())
    return "\n\n".join(unwrapped)


def latex_to_text(s: str) -> str:
    """Convert a chunk of LaTeX (inside a prompt env) to clean plain text /
    Markdown that a reader can paste into Claude Code."""

    # Step 0: unwrap pandoc's hard line breaks within paragraphs
    s = unwrap_paragraphs(s)

    # Inline code: \code{X} and \texttt{X} → backticks
    s = re.sub(r"\\code\{([^}]+)\}", r"`\1`", s)
    s = re.sub(r"\\texttt\{([^}]+)\}", r"`\1`", s)

    # Bold / italic — strip wrappers, keep text
    s = re.sub(r"\\textbf\{([^}]+)\}", r"**\1**", s)
    s = re.sub(r"\\textit\{([^}]+)\}", r"*\1*", s)
    s = re.sub(r"\\emph\{([^}]+)\}", r"*\1*", s)

    # Smart quotes (pandoc-style LaTeX uses '' and ``)
    s = re.sub(r"``", "“", s)            # left double quote
    s = re.sub(r"''", "”", s)            # right double quote
    s = re.sub(r"\\textquotesingle\{\}", "'", s)
    s = re.sub(r"\\textquotesingle ", "'", s)
    s = re.sub(r"\\textquotedbl\{\}", '"', s)
    s = re.sub(r"\\textquoteleft\{\}", "'", s)
    s = re.sub(r"\\textquoteright\{\}", "'", s)

    # Escaped special characters
    s = s.replace(r"\#", "#")
    s = s.replace(r"\$", "$")
    s = s.replace(r"\%", "%")
    s = s.replace(r"\&", "&")
    s = s.replace(r"\_", "_")
    s = s.replace(r"\{", "{")
    s = s.replace(r"\}", "}")
    s = s.replace(r"\textbackslash", "\\")
    s = s.replace(r"\textasciitilde", "~")
    s = s.replace(r"\textgreater{}", ">")
    s = s.replace(r"\textless{}", "<")

    # En/em dashes
    s = s.replace("---", "—")            # em dash
    s = s.replace("--", "–")             # en dash

    # Math-like operators
    s = s.replace(r"\times", "×")
    s = s.replace("$\\times$", "×")
    s = re.sub(r"\$([^$]+)\$", r"\1", s)      # strip $...$ math wrappers

    # Spacing commands → nothing
    s = re.sub(r"\\(medskip|smallskip|bigskip|noindent|par)\b", "", s)
    s = re.sub(r"\\par\b", "", s)

    # itemize/enumerate envs → markdown
    s = convert_lists(s)

    # Collapse multiple blank lines, strip leading/trailing whitespace per line
    s = re.sub(r"\n[ \t]+\n", "\n\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = s.strip()

    return s


def _unwrap_item(t: str) -> str:
    """Paragraph-aware whitespace collapse: blank lines are preserved as
    paragraph breaks; within a paragraph, all whitespace collapses to one space.
    This lets a nested list (already converted to markdown, where bullets are
    separated by blank lines) survive this pass."""
    paragraphs = re.split(r"\n\s*\n", t.strip())
    return "\n\n".join(re.sub(r"\s+", " ", p).strip() for p in paragraphs).strip()


def convert_lists(s: str) -> str:
    """Convert LaTeX itemize / enumerate to markdown bullets / numbers.
    Nested lists are output with blank lines between items so the outer
    paragraph-aware collapse doesn't fuse them."""

    def itemize_repl(m):
        body = m.group(1)
        parts = re.split(r"\\item\b\s*", body)
        items = [_unwrap_item(p) for p in parts if p.strip()]
        # Use blank lines between items so they survive outer paragraph-collapse
        return "\n\n" + "\n\n".join(f"- {it}" for it in items) + "\n\n"

    def enumerate_repl(m):
        body = m.group(1)
        parts = re.split(r"\\item\b\s*", body)
        items = [_unwrap_item(p) for p in parts if p.strip()]
        return "\n\n" + "\n\n".join(f"{i+1}. {it}" for i, it in enumerate(items)) + "\n\n"

    # Process innermost lists first
    while True:
        new = re.sub(r"\\begin\{itemize\}((?:(?!\\begin\{(?:itemize|enumerate)\}).)*?)\\end\{itemize\}",
                     itemize_repl, s, flags=re.DOTALL)
        if new == s:
            break
        s = new
    while True:
        new = re.sub(r"\\begin\{enumerate\}((?:(?!\\begin\{(?:itemize|enumerate)\}).)*?)\\end\{enumerate\}",
                     enumerate_repl, s, flags=re.DOTALL)
        if new == s:
            break
        s = new
    # Outer wrappers that contained nested lists
    s = re.sub(r"\\begin\{itemize\}(.*?)\\end\{itemize\}",
               itemize_repl, s, flags=re.DOTALL)
    s = re.sub(r"\\begin\{enumerate\}(.*?)\\end\{enumerate\}",
               enumerate_repl, s, flags=re.DOTALL)
    return s


# --- Slug generation -------------------------------------------------------

def slugify(text: str, max_len: int = 50) -> str:
    s = text.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    return s[:max_len].rstrip("-") or "prompt"


def derive_title(prompt_body: str) -> str:
    """Pick a short title for the prompt from its first sentence / verb phrase."""
    # First non-empty paragraph (post-unwrap)
    first = prompt_body.strip().split("\n", 1)[0].strip()
    # Take up to the first colon or period — whichever comes first
    cut = len(first)
    for sep in (":", "."):
        idx = first.find(sep)
        if 0 < idx < cut:
            cut = idx
    first = first[:cut].strip()
    # Cap at 60 chars, ending on a word boundary
    if len(first) > 60:
        truncated = first[:60]
        last_space = truncated.rfind(" ")
        if last_space > 30:
            first = truncated[:last_space] + "…"
        else:
            first = truncated + "…"
    return first


# --- Per-chapter extraction ------------------------------------------------

CHAPTER_RE = re.compile(r"^ch(\d{2})-(.+?)\.tex$")
PROMPT_RE = re.compile(r"\\begin\{prompt\}(.*?)\\end\{prompt\}", re.DOTALL)
STEP_RE = re.compile(r"\\begin\{step\}\{(\d+)\}(.*?)\\end\{step\}", re.DOTALL)


def chapter_files():
    out = []
    for p in sorted(LATEX_CHAPTERS.glob("ch*-*.tex")):
        m = CHAPTER_RE.match(p.name)
        if not m:
            continue
        num = int(m.group(1))
        slug = m.group(2)
        # Pretty title from slug
        title = slug.replace("-", " ").title()
        # Some title polish
        title = (title
                 .replace("Habitflow", "HabitFlow")
                 .replace("Habitstorage", "habitStorage")
                 .replace("Streaks And History", "Streaks and History")
                 .replace("Charts And Analytics", "Charts and Analytics")
                 .replace("Daily Reminders", "Daily Reminders")
                 .replace("Real App", "Real App"))
        out.append((num, slug, title, p))
    return out


def extract_chapter(num: int, slug: str, title: str, path: Path):
    text = path.read_text()

    # Build a map: position-in-source → preceding step number (if any)
    step_positions = []
    for m in STEP_RE.finditer(text):
        step_positions.append((m.start(), int(m.group(1))))

    def preceding_step(pos):
        last = None
        for sp, sn in step_positions:
            if sp < pos:
                last = sn
            else:
                break
        return last

    chapter_dir = PROMPTS / f"chapter-{num:02d}"
    chapter_dir.mkdir(parents=True, exist_ok=True)

    prompts = []
    for i, pm in enumerate(PROMPT_RE.finditer(text), start=1):
        body_latex = pm.group(1).strip()
        body_md = latex_to_text(body_latex)
        if not body_md:
            continue

        short_title = derive_title(body_md)
        step = preceding_step(pm.start())

        slug_name = f"{i:02d}-{slugify(short_title)}.md"
        out_path = chapter_dir / slug_name

        # Compose the file
        header = f"# {short_title}"
        meta_parts = [f"**Chapter {num} — {title}**"]
        if step is not None:
            meta_parts.append(f"Used in: Step {step}")
        meta = "  \n".join(meta_parts)

        contents = f"""{header}

{meta}

---

```
{body_md}
```
"""
        out_path.write_text(contents)
        prompts.append({
            "num": i,
            "step": step,
            "title": short_title,
            "filename": slug_name,
        })

    return prompts


# --- Build the index README ------------------------------------------------

def build_index(all_prompts: dict):
    lines = [
        "# Prompts Index",
        "",
        "Every prompt from *Build Apps with AI*, organized by chapter. "
        "Click a file to view it, then use GitHub's “Copy raw file” button (top-right of the file view) to copy it cleanly.",
        "",
        f"**Total prompts:** {sum(len(v) for v in all_prompts.values())}",
        "",
        "---",
        "",
    ]
    for (num, slug, title, _path), prompts in sorted(all_prompts.items()):
        if not prompts:
            continue
        lines.append(f"## Chapter {num} — {title}")
        lines.append("")
        lines.append(f"[Open chapter folder](chapter-{num:02d}/)")
        lines.append("")
        for p in prompts:
            step_str = f"_Step {p['step']}_" if p['step'] is not None else "_intro_"
            lines.append(f"- [{p['title']}](chapter-{num:02d}/{p['filename']}) — {step_str}")
        lines.append("")
    (PROMPTS / "README.md").write_text("\n".join(lines))


# --- Main ------------------------------------------------------------------

def main():
    if not LATEX_CHAPTERS.exists():
        print(f"Error: cannot find {LATEX_CHAPTERS}", file=sys.stderr)
        sys.exit(1)

    # Clear any previous extraction
    if PROMPTS.exists():
        import shutil
        shutil.rmtree(PROMPTS)
    PROMPTS.mkdir()

    all_prompts = {}
    total = 0
    for num, slug, title, path in chapter_files():
        prompts = extract_chapter(num, slug, title, path)
        all_prompts[(num, slug, title, path)] = prompts
        total += len(prompts)
        print(f"  Chapter {num:2d}: {len(prompts):2d} prompts  →  prompts/chapter-{num:02d}/")

    build_index(all_prompts)
    print(f"\nExtracted {total} prompts across {len(all_prompts)} chapters.")
    print(f"Index: prompts/README.md")


if __name__ == "__main__":
    main()
