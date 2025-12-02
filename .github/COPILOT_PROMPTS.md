# Copilot Prompts: Blog Post Generator

Note: Copilot does not auto-train from files in your repo. However, Copilot Chat can reference files when you point it to them, and having this guide in `.github/` makes it discoverable and conventional.

## Quick Post Command

```
Create a new blog post using `src/content/blog/blog-template.md` as the reference.
Frontmatter:
- author: hallm
- pubDatetime: <YYYY-MM-DDThh:mm:ss>
- title: <Post Title>
- ogImage: ../../assets/images/og-default.png
- featured: false
- draft: true
 - tags:
   - tag-one
   - tag-two
- description: <1-2 sentence summary>

Body:
- Write concise, scan-friendly sections with H2/H3 headings.
- Use bold for key terms, italics sparingly.
- Use `<u>` for underline when needed.
- Include at least one unordered list and one ordered list.
- Include one fenced code block with language.
- Include one blockquote.
- Include one internal link to another post if relevant.
- Keep paragraphs ≤ 3 sentences when possible.

Return the final Markdown ready to paste into `src/content/blog/<slug>.md`.
Slug: Generate from title using lowercase hyphens.
```

## Structured Prompt (Detailed)

```
You are generating Markdown content for an Astro Paper blog.
Follow the exact frontmatter and formatting conventions.

1) Create frontmatter with these fields:
---
author: hallm
pubDatetime: 2025-12-02T12:00:00
title: How I Organize My Dev Environment
ogImage: ../../assets/images/og-default.png
featured: false
draft: true
tags:
  - productivity
  - dev-tools
description: A practical walkthrough of my development environment setup and daily workflow.
---

2) Write the body as:
- H1 is not needed; start at H2.
- Sections: Introduction, Tools, Workflow, Tips, Conclusion.
- Use bold for key actions and code for commands. Underline using `<u>` only when helpful.
- Include:
  - One unordered list (3–5 items)
  - One ordered list (3–5 steps)
  - One fenced code block labeled `bash`
  - One blockquote
  - One table with 2–3 rows

3) Constraints:
- Keep paragraphs short (max 3 sentences).
- Avoid fluff; be practical.
- Use relative image paths if you include images.
- Do not add external scripts.

Return only the final Markdown.
```

## Copilot Chat Shortcuts

- "Generate blog frontmatter from title '...' and tags [a,b], set draft true."
- "Create a section outline with H2/H3 for a post about '...'."
- "Rewrite this paragraph to be shorter and scan-friendly."
- "Convert this plain text into Markdown lists, code blocks, and a quote." 

## Examples

### Example: Fitness Post Skeleton

```
---
author: hallm
pubDatetime: 2025-12-02T12:00:00
title: My Fitness Journey – Part 2
ogImage: ../../assets/images/og-default.png
featured: false
draft: true
tags:
  - fitness
  - health
description: Building momentum with sleep, hydration, and consistency.
---

## Sleep and Recovery

Quality sleep drives progress. **Protect your routine**.

- Consistent bedtime
- Dark, cool room
- Limit late screens

> Small improvements compound; recovery multiplies effort.

### Hydration Basics

1. Start with water upon waking.
2. Track intake during the day.
3. Add electrolytes for longer sessions.

```bash
echo "Track it to improve it"
```
```

## Notes

- This file being in `.github/` doesn't change Copilot's model behavior. It helps keep prompts handy and discoverable.
- Point Copilot Chat to this file or to `src/content/blog/blog-template.md` when asking for content to ensure it uses your conventions.
- For dynamic OG generation, see `pages/og.png.ts` and `utils/generateOgImages.tsx`.
