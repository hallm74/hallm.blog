---
author: hallm
pubDatetime: 2024-12-02T18:34:55
title:  Going CMS-Less with Astro, Drafts and Scripts
ogImage: https://getdrafts.com/assets/img/custom/og-image.png
featured: true
draft: false
tags:
    - Astro
    - Programming
    - Apple
description:  Using Drafts to update my Astro blog (Astropaper) has become my go-to method for adding content. I'm sharing my Drafts scripts here in case they're helpful to anyone looking to do something similar.
---

Using Drafts to update my Astro blog has become my go-to method for adding content. I'm sharing my Drafts scripts here in case they're helpful to anyone looking to do something similar.

Since I started working with Jekyll and now Astro, I’ve explored various CMS options like TinaCMS. I even launched my blog with TinaCMS integrated into my development environment, and I’ll probably write an article about setting it up when I have the time.

One important note about my workflow: I typically begin by capturing blog posts or sharing external links, like news stories, using Drafts. Drafts formats the front matter for me, which I then copy into VSCode to create the post. From there, I focus on styling the content and adding code blocks in VSCode, where I can save and preview changes in real time.

I've attached the link to the Drafts Action Group to the bottom of the post.

`This is an ongoing project, and I plan to maintain all updates in this post.`

## Table of Contents

## Safari Share Sheet Script

This script works on iOS, iPadOS, and Safari on Mac.  I mostly use this when I see something external that I think I might would want to post on my blog.  Then later in the day or when I get time, I copy and paste it from Drafts to VSCode.

```md
author: hallm
pubDatetime: [[date|%Y-%m-%dT%H:%M:%S]]
title: [[title]]
featured: true
draft: false
tags:
	- news
description: [[selection]]
---

>[[selection]]

[[[title]]]([[url]])
```

## Astropaper Blog Post

`Step 1 Javascript (Grabs tags that are assigned to the Drafts post`
For Astropaper make sure you have four spaces before the dash in that third line.
```js
let s = ""
if (draft.tags.length > 0) {
	s = draft.tags.map(t => `    - ${t}`).join("\n")
}
draft.setTemplateTag("formatted-tags", s)
```

`Step 2 Create Draft`
```md
---
author: hallm
pubDatetime: [[date|%Y-%m-%dT%H:%M:%S]]
title:  [[title]]
featured: true
draft: false
tags:
[[formatted-tags]]
description:  [[selection_only]]
---
[[body]]
```

## ogImage from Clipboard

When sharing an external link, like a news story, I prefer to fetch the og:image information. This script takes the URL from your clipboard, sends it to the OpenGraph.io API, and inserts the og:image into the front matter on the 4th line.

Currently, it works well for most sites, but I’ve encountered issues with larger news platforms like The New York Times. (Note: You’ll need an API key to use this script.)

`Javascript Action`

```js
async function fetchOpenGraphImage(siteUrl) {
  try {
    // Replace with your OpenGraph.io API key
    const apiKey = "Insert your opengraph key here";
    const apiUrl = `https://opengraph.io/api/1.1/site/${encodeURIComponent(siteUrl)}?app_id=${apiKey}`;

    console.log("Fetching OpenGraph data for URL:", siteUrl);
    console.log("API URL being requested:", apiUrl);

    // Use Drafts HTTP object
    let http = HTTP.create();
    let response = http.request({
      url: apiUrl,
      method: "GET",
      headers: {
        "Accept": "application/json"
      }
    });

    if (!response.success) {
      console.error(`HTTP request failed with status code: ${response.statusCode}`);
      console.error(`Response error details: ${response.responseText}`);
      return null;
    }

    let parsedData;
    try {
      parsedData = JSON.parse(response.responseText);
    } catch (error) {
      console.error("Failed to parse JSON response:", error.message);
      console.error("Raw response that caused the issue:", response.responseText);
      return null;
    }

    let ogImage = parsedData.hybridGraph?.image || null;
    if (ogImage) {
      console.log("Successfully extracted og:image:", ogImage);

      // Insert into line 5
      let content = draft.content.split("\n"); // Split draft content into lines
      while (content.length < 4) {
        content.push(""); // Ensure there are at least 5 lines
      }
      content.splice(4, 0, `ogImage: ${ogImage}`); // Insert at line 5 (index 4)
      draft.content = content.join("\n"); // Rejoin content into a single string
      draft.update();
      return ogImage;
    } else {
      console.error("No og:image found in OpenGraph.io response.");
      return null;
    }
  } catch (error) {
    console.error("Error during fetchOpenGraphImage execution:", error.message);
    return null;
  }
}

// Capture the URL from the clipboard
let clipboardContent = app.getClipboard();
console.log("Clipboard content captured:", clipboardContent);

if (!clipboardContent || !clipboardContent.startsWith("http")) {
  console.error("Invalid or missing URL in clipboard:", clipboardContent);
} else {
  fetchOpenGraphImage(clipboardContent).then((ogImageUrl) => {
    if (ogImageUrl) {
      console.log("Successfully inserted og:image URL into line 5:", ogImageUrl);
    } else {
      console.error("Failed to fetch og:image URL.");
    }
  });
}
```

There’s a third og:image script in the group that prompts for a URL and inserts the og:image tag at the bottom of the post. I didn’t fully finish that one since it was mainly used for testing. I much prefer using the clipboard-based script instead.

[Draft's Action Group with all of the scripts](https://directory.getdrafts.com/g/2Vv)