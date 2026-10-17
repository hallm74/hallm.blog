/** Keep preview assets on the preview while canonical content URLs stay in production. */
export function deploymentOrigin(siteUrl: string): string {
  if (import.meta.env.PUBLIC_PREVIEW !== "true") return new URL(siteUrl).origin;
  const previewUrl =
    import.meta.env.PUBLIC_ASSET_ORIGIN ||
    process.env.DEPLOY_PRIME_URL ||
    process.env.DEPLOY_URL;
  if (!previewUrl) {
    throw new Error(
      "Preview build requires PUBLIC_ASSET_ORIGIN or Netlify's deploy URL so OG images do not point to production."
    );
  }
  const origin = new URL(previewUrl);
  if (origin.protocol !== "https:") {
    throw new Error(
      "Preview social metadata requires an HTTPS deployment URL."
    );
  }
  return origin.origin;
}

export function socialImageUrl(image: string, siteUrl: string): string {
  const url = new URL(image, siteUrl);
  // Preserve deliberately external frontmatter images. Rebase this site's assets.
  if (url.origin !== new URL(siteUrl).origin) return url.href;
  return new URL(
    url.pathname + url.search + url.hash,
    deploymentOrigin(siteUrl)
  ).href;
}
