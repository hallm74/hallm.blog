import kebabcase from "lodash.kebabcase";

// Keep existing tag URLs stable across the theme upgrade.
export const slugifyStr = (str: string): string => kebabcase(str);
export const slugifyAll = (arr: string[]) => arr.map(str => slugifyStr(str));
