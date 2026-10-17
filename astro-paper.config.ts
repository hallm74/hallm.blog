import { defineAstroPaperConfig } from "./src/types/config";

export default defineAstroPaperConfig({
  site: {
    url: "https://hallm.blog/",
    title: "hallm",
    description: "Tech Musings from a Curious Mind",
    author: "Marion Hall",
    profile: "https://hallm.blog/about/",
    ogImage: "astropaper-og.jpg",
    lang: "en",
    timezone: "UTC",
    dir: "ltr",
  },
  posts: {
    perPage: 5,
    perIndex: 4,
    scheduledPostMargin: 15 * 60 * 1000,
  },
  features: {
    lightAndDarkMode: true,
    dynamicOgImage: true,
    showArchives: true,
    showBackButton: true,
    editPost: { enabled: false },
    search: "pagefind",
  },
  socials: [
    {
      name: "github",
      url: "https://github.com/hallm74/hallm.blog",
    },
    {
      name: "instagram",
      url: "https://www.instagram.com/hallm/",
    },
    {
      name: "linkedin",
      url: "https://www.linkedin.com/in/satcom/",
    },
    {
      name: "mail",
      url: "mailto:hallm@hallm.blog",
    },
    {
      name: "x",
      url: "https://x.com/hallm",
    },
    {
      name: "telegram",
      url: "https://t.me/hallm74",
    },
    {
      name: "mastodon",
      url: "https://techhub.social/@hallm",
    },
    {
      name: "bluesky",
      url: "https://bsky.app/profile/hallm74.bsky.social",
    },
  ],
  shareLinks: [
    { name: "whatsapp", url: "https://wa.me/?text=" },
    { name: "facebook", url: "https://www.facebook.com/sharer.php?u=" },
    { name: "x", url: "https://x.com/intent/post?url=" },
    { name: "telegram", url: "https://t.me/share/url?url=" },
    { name: "pinterest", url: "https://pinterest.com/pin/create/button/?url=" },
    { name: "mail", url: "mailto:?subject=See%20this%20post&body=" },
  ],
});
