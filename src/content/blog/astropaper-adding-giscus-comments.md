---
author: hallm
pubDatetime: 2024-12-15T11:13:35
title: How to integrate Giscus comments into AstroPaper 
featured: true
draft: false
ogImage: ../../assets/images/giscuscomments.png
tags:
    - Astropaper
description: Simple code changes to Astropaper to add Giscus comments
---

Since launching my blog, I’ve been searching for a simple comment system that doesn’t require running Astro in server-side mode or relying on something like Disqus. Giscus seems to be a great solution, with the only downside being that users need a GitHub account. However, since most of my blog’s readers are likely GitHub users, this shouldn’t be a significant issue.

Additionally, Giscus should help reduce spam comments, a common problem with WordPress sites. The code was originally written and published in the Astropaper tutorial site, either by the author or a contributor. I’m including it here for reference, focusing on the parts relevant to integrating it with this blog. For the full article, check out [this link](https://astro-paper.pages.dev/posts/how-to-integrate-giscus-comments/).

## Table of Contents

## Prequisitess

* the repository is public
* the [Giscus app](https://github.com/apps/giscus) is installed 
* the Discussions feature is turned on for your repository

## Giscus App

After the prerequisites are done go to [Giscus.app](https://giscus.app)
* Enter the username/repo
* Leave Page Discussion mapping at title contains page pathname
* Choose the category.  I chose General.

Copy your script tags.  It should look like below

```html
<script src="https://giscus.app/client.js"
        data-repo="[ENTER REPO HERE]"
        data-repo-id="[ENTER REPO ID HERE]"
        data-category="[ENTER CATEGORY NAME HERE]"
        data-category-id="[ENTER CATEGORY ID HERE]"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="bottom"
        data-theme="preferred_color_scheme"
        data-lang="en"
        crossorigin="anonymous"
        async>
</script>
```

## Adding Giscus to existing Astropaper site

First install Giscus react component.

```bash
npm i @giscus/react
```

Now create a new Comments.tsx React component in `src/components`

```js
import Giscus, { type Theme } from "@giscus/react";
import { GISCUS } from "@config";
import { useEffect, useState } from "react";

interface CommentsProps {
  lightTheme?: Theme;
  darkTheme?: Theme;
}

export default function Comments({
  lightTheme = "light",
  darkTheme = "dark",
}: CommentsProps) {
  const [theme, setTheme] = useState(() => {
    const currentTheme = localStorage.getItem("theme");
    const browserTheme = window.matchMedia("(prefers-color-scheme: dark)")
      .matches
      ? "dark"
      : "light";

    return currentTheme || browserTheme;
  });

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    const handleChange = ({ matches }: MediaQueryListEvent) => {
      setTheme(matches ? "dark" : "light");
    };

    mediaQuery.addEventListener("change", handleChange);

    return () => mediaQuery.removeEventListener("change", handleChange);
  }, []);

  useEffect(() => {
    const themeButton = document.querySelector("#theme-btn");
    const handleClick = () => {
      setTheme(prevTheme => (prevTheme === "dark" ? "light" : "dark"));
    };

    themeButton?.addEventListener("click", handleClick);

    return () => themeButton?.removeEventListener("click", handleClick);
  }, []);

  return (
    <div className="mt-8">
      <Giscus theme={theme === "light" ? lightTheme : darkTheme} {...GISCUS} />
    </div>
  );
}
```

Now we need to define the `Giscus` config in `src/config.ts`

```js
import type { GiscusProps } from "@giscus/react";

...

export const GISCUS: GiscusProps = {
  repo: "[ENTER REPO HERE]",
  repoId: "[ENTER REPO ID HERE]",
  category: "[ENTER CATEGORY NAME HERE]",
  categoryId: "[ENTER CATEGORY ID HERE]",
  mapping: "pathname",
  reactionsEnabled: "1",
  emitMetadata: "0",
  inputPosition: "bottom",
  lang: "en",
  loading: "lazy",
};
```

From the authors notes if you specifiy a theme in the configuration here it will override the lightTheme and darkTheme properties.

For the last thing we just need to add the new Comments component to `src/layouts/PostDetails.astro`

`Be sure to put the import at the top with the other imports and then search for the ShareLinks portion of the code to add the Comments component.`

```astro
+ import Comments from "@components/Comments";

      <ShareLinks />
    </div>

+    <Comments client:only="react" />

  </main>
  <Footer />
</Layout>
```

If everything is right you should see a comments section below each post like the image below.

![Giscus Comments](@assets/images/giscuscomments.png)

[How to integrate Giscus comments into AstroPaper | AstroPaper](https://astro-paper.pages.dev/posts/how-to-integrate-giscus-comments/)