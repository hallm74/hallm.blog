import type { APIRoute } from "astro";

const getRobotsTxt = (sitemapURL: URL) => `
User-agent: *
Allow: /

Sitemap: ${sitemapURL.href}
`;

export const GET: APIRoute = ({ site }) => {
  const sitemapURL = new URL("sitemap-index.xml", site);
  return new Response(
    import.meta.env.PUBLIC_PREVIEW === "true"
      ? "User-agent: *\nDisallow: /\n"
      : getRobotsTxt(sitemapURL)
  );
};
