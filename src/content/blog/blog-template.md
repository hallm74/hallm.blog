---
author: hallm
pubDatetime: 2025-12-01T23:37:00Z
title: Blog Template
featured: false
draft: true
tags:
  - recipes
ogImage: ../../assets/images/codetemplate.jpg
description:
 Use this template to scaffold a new blog post. Update the frontmatter fields, then replace the content below with your writing.
---

## Table of Contents

# Blog Post Template (Replace Me)

This file is a template. Delete the instructional content and write your post, but keep the frontmatter at the top updated.

---

## Frontmatter Guidance

- **`author`**: Set to your handle (e.g., `hallm`).
- **`pubDatetime`**: ISO string when you plan to publish (e.g., `2025-12-31T12:00:00`).
- **`title`**: Human‑readable post title.
- **`ogImage`**: Path to an image for social cards. Use an existing image in `src/assets/images/` or generate dynamic OG via `pages/og.png.ts`.
- **`featured`**: Set `true` to show on homepage hero; otherwise `false`.
- **`draft`**: Keep `true` while writing; set `false` to publish.
- **`tags`**: Lowercase keywords. Use existing tags where possible. See `utils/getUniqueTags.ts`.
- **`description`**: One–two sentences for cards, SEO, and sharing.

---

## Markdown Cheatsheet

### Headings

- `# H1`
- `## H2`
- `### H3`

### Emphasis

- **Bold**: `**bold**`
- Italic: `*italic*`
- Underline: `<u>underline</u>` (HTML tag; Markdown has no native underline)

### Lists

- Unordered:
  - `- Item`
  - `- Nested item`
- Ordered:
  1. `1. First`
  2. `2. Second`

### Links & Images

- Link: `[visible text](https://example.com)`
- Image: `![alt text](/assets/path/image.png)`

### Code

- Inline: ``Use `code` for short snippets``
- Block:

```ts
// fenced code block with language for highlighting
function greet(name: string) {
  return `Hello, ${name}!`;
}
```

### Blockquotes

> Use `>` at the start of a line to create a quote.

### Tables

| Column | Description |
|---|---|
| A | Example row |
| B | Another row |

### Horizontal Rule

`---` or `***` on a line by itself.

---

## Astro Paper Notes (Repo‑Specific)

- Place media in `public/assets/` or `src/assets/images/`. Use relative paths in posts (e.g., `../../assets/images/your-image.png`).
- Dynamic OG images can be generated via `utils/generateOgImages.tsx` and `pages/og.png.ts`. For a simple static image, set `ogImage` in frontmatter.
- Use `src/components/Tag.astro` and tag pages under `pages/tags/` are auto‑generated from your post tags.

---

## Start Writing Here

Replace this section with your content. A suggested outline:

1. Introduction (what, why)
2. Background/context
3. Main points with examples
4. Conclusion with takeaways and links

> Tip: Keep paragraphs short and scan‑friendly. Use headings and lists.