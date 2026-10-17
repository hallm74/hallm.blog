import { getCollection } from "astro:content";
import { postFilter } from "@/utils/postFilter";
import { slugifyStr } from "@/utils/slugify";
export { GET } from "./[...slug]/index.png";

export async function getStaticPaths() {
  const posts = await getCollection("posts");
  return posts
    .filter(post => postFilter(post) && !post.data.ogImage)
    .map(post => ({
      params: { legacyOg: slugifyStr(post.data.title) },
      props: post,
    }));
}
