# hallm.blog

Marion Hall's personal blog, based on [AstroPaper 6.1.0](https://github.com/satnaing/astro-paper/releases/tag/v6.1.0).

Use Node 24 (`.nvmrc`) and npm:

```sh
npm ci
npm run dev
npm run build
npm run preview
npm run lint
npm run format:check
```

`npm run test:upgrade` checks the migration snapshot after a build. It is deliberately not a permanent CI gate: normal future article edits change that snapshot.

The production build includes type checking, static HTML and Pagefind indexing. Search requires a production build before previewing.

## Customizations

- Site metadata, pagination and social destinations: `astro-paper.config.ts`.
- Home introduction: `src/pages/index.astro`; About: `src/content/pages/about.md`.
- Posts remain in `src/content/blog` to preserve existing Drafts/GitHub authoring paths; the v6 `posts` collection uses the stable glob loader.
- Existing frontmatter slugs and tag URLs are retained; blank legacy descriptions remain supported without rewriting articles.
- IBM Plex Mono, light/dark colors, custom default OG image and all original images are retained.
- Giscus: `src/components/Comments.astro`. Keep pathname mapping, repository and category unchanged to preserve discussions. Theme updates use the root `data-theme` attribute; client navigation cleans up old observers.
- Drafts are excluded from routes, search, RSS, sitemap and dynamic OG output.

## Hosting and review

Netlify site `hallm` builds `master` with `npm run build` and publishes `dist`. `netlify.toml` pins Node 24 and flags branch/deploy previews as noindex. Draft deploys must use the already built preview output and omit `--prod`.

Before any production release, review mobile/desktop and both themes, route/content parity, Pagefind search, Giscus discussions, RSS, sitemap, metadata and images. Production promotion requires Marion's approval.

## Rollback

Pre-upgrade source: `fc475ae6b44ec744d80391c39af59cf4905e269d`, recorded as local tag `rollback/pre-astropaper-6.1.0-20261017`.

Previous production deploy: `693074a73a07720008893dbb` ([immutable permalink](https://693074a73a07720008893dbb--hallm.netlify.app)). Restore that deployment through Netlify if necessary and revert the upgrade in Git before the next automatic build. Do not change repository or hosting access.
