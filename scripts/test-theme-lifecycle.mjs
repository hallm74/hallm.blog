import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";
import ts from "typescript";

const compile = source =>
  ts.transpile(source, {
    target: ts.ScriptTarget.ES2022,
    module: ts.ModuleKind.CommonJS,
  });

// Exercise the actual component script with a delayed iframe and changing theme.
const observers = [];
const root = { dataset: { theme: "light" } };
const classes = new Map();
class Observer {
  constructor(callback) {
    this.callback = callback;
    observers.push(this);
  }
  observe() {}
  disconnect() {
    this.disconnected = true;
  }
}
class Element {
  children = [];
  get childElementCount() {
    return this.children.length;
  }
  appendChild(child) {
    this.children.push(child);
  }
  querySelector(selector) {
    return selector === "script" ? this.children[0] : this.frameFixture;
  }
}
const component = fs.readFileSync(
  new URL("../src/components/Comments.astro", import.meta.url),
  "utf8"
);
const script = component.match(/<script>([\s\S]*?)<\/script>/)[1];
vm.runInNewContext(compile(script), {
  HTMLElement: Element,
  MutationObserver: Observer,
  customElements: {
    get: name => classes.get(name),
    define: (name, value) => classes.set(name, value),
  },
  document: {
    documentElement: root,
    createElement: () => ({
      attrs: {},
      setAttribute(key, value) {
        this.attrs[key] = value;
      },
    }),
  },
});
const comments = new (classes.get("hallm-comments"))();
comments.connectedCallback();
root.dataset.theme = "dark";
observers[0].callback();
assert.equal(
  comments.children[0].attrs["data-theme"],
  "dark",
  "async loader must see the latest theme"
);
const messages = [];
const listeners = new Map();
comments.frameFixture = {
  contentWindow: {
    postMessage: (message, origin) => messages.push({ message, origin }),
  },
  addEventListener: (event, listener) => listeners.set(event, listener),
  removeEventListener: event => listeners.delete(event),
};
observers[1].callback();
root.dataset.theme = "light";
observers[0].callback();
listeners.get("load")();
assert.equal(
  messages.at(-1).message.giscus.setConfig.theme,
  "light",
  "iframe load must resync theme"
);
assert.equal(messages.at(-1).origin, "https://giscus.app");
comments.disconnectedCallback();
assert.ok(
  observers.every(observer => observer.disconnected),
  "observers must disconnect on navigation"
);
assert.equal(listeners.size, 0, "iframe listener must be removed");

function themeFixture(stored) {
  const storage = new Map(stored ? [["theme", stored]] : []);
  const attrs = new Map();
  let preferenceChanged;
  let clicked;
  const button = {
    setAttribute() {},
    addEventListener: (_, callback) => {
      clicked = callback;
    },
  };
  const document = {
    firstElementChild: {
      setAttribute: (key, value) => attrs.set(key, value),
      classList: { toggle() {} },
    },
    body: {},
    querySelector: selector =>
      selector === "#theme-btn"
        ? button
        : {
            setAttribute() {},
            getAttribute() {
              return null;
            },
          },
    addEventListener() {},
  };
  vm.runInNewContext(
    compile(
      fs.readFileSync(
        new URL("../src/scripts/theme.ts", import.meta.url),
        "utf8"
      )
    ),
    {
      exports: {},
      document,
      localStorage: {
        getItem: key => storage.get(key) ?? null,
        setItem: (key, value) => storage.set(key, value),
      },
      window: {
        getComputedStyle: () => ({ backgroundColor: "white" }),
        matchMedia: () => ({
          matches: false,
          addEventListener: (_, callback) => {
            preferenceChanged = callback;
          },
        }),
      },
    }
  );
  return {
    storage,
    attrs,
    osChange: matches => preferenceChanged({ matches }),
    click: () => clicked(),
  };
}
const explicit = themeFixture("light");
explicit.osChange(true);
assert.equal(
  explicit.attrs.get("data-theme"),
  "light",
  "manual choice must override OS changes"
);
const automatic = themeFixture();
automatic.osChange(true);
assert.equal(automatic.attrs.get("data-theme"), "dark");
assert.equal(
  automatic.storage.has("theme"),
  false,
  "OS changes must not become manual preferences"
);
automatic.click();
assert.equal(automatic.storage.get("theme"), "light");
automatic.osChange(true);
assert.equal(automatic.attrs.get("data-theme"), "light");
process.stdout.write(
  "PASS: delayed Giscus load, theme resync, observer cleanup, and manual-vs-OS preference behavior.\n"
);
