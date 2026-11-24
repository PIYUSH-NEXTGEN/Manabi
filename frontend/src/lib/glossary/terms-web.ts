import type { GlossaryEntry } from "./types";

const category = "Web & code" as const;

export const WEB_TERMS: GlossaryEntry[] = [
  {
    id: "html",
    term: "HTML",
    definition:
      "The language that describes the structure of a web page: headings, paragraphs, links and forms.",
    category,
  },
  {
    id: "css",
    term: "CSS",
    definition:
      "The language that controls how a web page looks: colours, spacing, layout and animation.",
    category,
  },
  {
    id: "javascript",
    term: "JavaScript",
    definition:
      "The programming language that runs in web browsers and makes pages interactive.",
    category,
  },
  {
    id: "typescript",
    term: "TypeScript",
    definition:
      "A version of JavaScript with type labels that catch many mistakes before the code runs.",
    category,
  },
  {
    id: "react",
    term: "React",
    definition:
      "A JavaScript library for building user interfaces out of reusable pieces called components.",
    category,
  },
  {
    id: "hook",
    term: "hook",
    aliases: ["hooks"],
    definition:
      "A React function that lets a component use features such as state or side effects.",
    category,
  },
  {
    id: "component",
    term: "component",
    definition:
      "A reusable, self-contained piece of a user interface, such as a button, card or page section.",
    category,
  },
  {
    id: "jsx",
    term: "JSX",
    definition:
      "The HTML-like syntax React uses inside JavaScript to describe what a component should render.",
    category,
  },
  {
    id: "virtual-dom",
    term: "virtual DOM",
    definition:
      "An in-memory copy of the page that React compares with the previous copy to make only the necessary updates.",
    category,
  },
  {
    id: "dom",
    term: "DOM",
    aliases: ["document object model"],
    definition:
      "The browser's tree-shaped model of a page, which scripts can read and change.",
    category,
  },
  {
    id: "bundler",
    term: "bundler",
    definition:
      "A tool that combines many source files and packages into the few files a browser can load efficiently.",
    category,
  },
  {
    id: "vite",
    term: "Vite",
    definition:
      "A fast build tool and development server for web apps, often used with React.",
    category,
  },
  {
    id: "npm",
    term: "npm",
    definition:
      "The default package manager for JavaScript; it downloads libraries and runs project scripts.",
    category,
  },
  {
    id: "esm",
    term: "ESM",
    aliases: ["ECMAScript modules"],
    definition:
      "The standard way modern JavaScript splits code into modules and imports one file from another.",
    category,
  },
  {
    id: "commonjs",
    term: "CommonJS",
    definition:
      "An older module format used mainly by Node.js, where files exchange values with require and module.exports.",
    category,
  },
  {
    id: "module",
    term: "module",
    definition:
      "A file or package that groups related code and exposes only the parts others should use.",
    category,
  },
  {
    id: "api",
    term: "API",
    aliases: ["application programming interface"],
    definition:
      "A defined way for one piece of software to ask another for data or actions.",
    category,
  },
  {
    id: "rest-api",
    term: "REST API",
    definition:
      "A web API that uses ordinary HTTP requests and URLs to read or change resources.",
    category,
  },
  {
    id: "endpoint",
    term: "endpoint",
    definition:
      "One specific URL an API exposes, such as /api/problems or /api/login.",
    category,
  },
  {
    id: "json",
    term: "JSON",
    definition:
      "A plain-text format for structured data, built from objects, lists, strings and numbers.",
    category,
  },
  {
    id: "schema",
    term: "schema",
    definition:
      "A description of what data is allowed to look like: which fields exist and what types they hold.",
    category,
  },
  {
    id: "http",
    term: "HTTP",
    definition:
      "The request-and-response rules browsers and servers use to exchange pages, data and files.",
    category,
  },
  {
    id: "https",
    term: "HTTPS",
    definition:
      "HTTP with encryption, so other people on the network cannot read or alter the traffic.",
    category,
  },
  {
    id: "url",
    term: "URL",
    aliases: ["uniform resource locator"],
    definition:
      "The address of something on the web, such as a page, an image or an API endpoint.",
    category,
  },
  {
    id: "dns",
    term: "DNS",
    aliases: ["domain name system"],
    definition:
      "The internet's address book: it turns a name like example.com into the numeric address of a server.",
    category,
  },
  {
    id: "cors",
    term: "CORS",
    aliases: ["cross-origin resource sharing"],
    definition:
      "Browser rules that decide whether a page from one site may call an API on a different site.",
    category,
  },
  {
    id: "webhook",
    term: "webhook",
    definition:
      "A message one service sends to another when something happens, instead of the second service asking repeatedly.",
    category,
  },
  {
    id: "websocket",
    term: "WebSocket",
    definition:
      "A connection that stays open so the server and browser can send messages to each other at any time.",
    category,
  },
  {
    id: "tcp",
    term: "TCP",
    aliases: ["transmission control protocol"],
    definition:
      "A network protocol that delivers a reliable, ordered stream of bytes between two computers.",
    category,
  },
  {
    id: "socket",
    term: "socket",
    definition:
      "One end of a network connection that a program reads from and writes to.",
    category,
  },
  {
    id: "pwa",
    term: "PWA",
    aliases: ["progressive web app"],
    definition:
      "A website built to feel like an app: it can be installed, work offline and send notifications.",
    category,
  },
  {
    id: "service-worker",
    term: "service worker",
    definition:
      "A background script in the browser that can cache files and keep a web app working without a network.",
    category,
  },
  {
    id: "indexeddb",
    term: "IndexedDB",
    definition:
      "A database built into browsers for storing structured data and files that persist between visits.",
    category,
  },
  {
    id: "cache",
    term: "cache",
    definition:
      "A local copy of data kept so the next request can be answered faster instead of fetched again.",
    category,
  },
  {
    id: "offline-first",
    term: "offline-first",
    definition:
      "A design where the app keeps working without a network and syncs later when a connection returns.",
    category,
  },
  {
    id: "sync",
    term: "sync",
    aliases: ["syncing", "synchronization"],
    definition:
      "Making the copy on a device and the copy on a server agree, even after edits happened on both sides.",
    category,
  },
  {
    id: "conflict-resolution",
    term: "conflict resolution",
    definition:
      "Deciding what to do when two people or devices changed the same data before syncing.",
    category,
  },
  {
    id: "queue",
    term: "queue",
    definition:
      "A line of jobs waiting to be handled, so work can happen in order and without blocking the user.",
    category,
  },
  {
    id: "web-worker",
    term: "Web Worker",
    aliases: ["worker thread"],
    definition:
      "A background thread in the browser that runs heavy code without freezing the page.",
    category,
  },
  {
    id: "event-loop",
    term: "event loop",
    definition:
      "The browser's scheduler: it runs queued callbacks one at a time and keeps the page responsive.",
    category,
  },
  {
    id: "async",
    term: "async",
    aliases: ["asynchronous"],
    definition:
      "Work that starts now and finishes later, so the program can keep doing other things while it waits.",
    category,
  },
  {
    id: "promise",
    term: "promise",
    definition:
      "An object that represents a result that will arrive later, either successfully or with an error.",
    category,
  },
  {
    id: "callback",
    term: "callback",
    definition:
      "A function passed to other code so it can be called later, often when some work finishes.",
    category,
  },
  {
    id: "race-condition",
    term: "race condition",
    definition:
      "A bug where the result depends on unpredictable timing, such as two requests changing the same value at once.",
    category,
  },
  {
    id: "debounce",
    term: "debounce",
    definition:
      "Waiting until rapid events stop before running the action, such as searching only after typing pauses.",
    category,
  },
  {
    id: "rate-limiting",
    term: "rate limiting",
    aliases: ["rate limit", "rate limits"],
    definition:
      "Capping how many requests a user or service may make in a period, to prevent overload and abuse.",
    category,
  },
  {
    id: "retry",
    term: "retry",
    aliases: ["retries"],
    definition:
      "Trying a failed operation again, often a limited number of times, before giving up.",
    category,
  },
  {
    id: "backoff",
    term: "backoff",
    definition:
      "Waiting longer between each retry so a struggling service has time to recover.",
    category,
  },
  {
    id: "idempotency",
    term: "idempotency",
    aliases: ["idempotent"],
    definition:
      "A property where repeating the same request has the same effect as doing it once, which makes retries safe.",
    category,
  },
  {
    id: "dead-letter-queue",
    term: "dead-letter queue",
    definition:
      "A holding place for jobs that failed too many times, so they can be inspected instead of lost.",
    category,
  },
  {
    id: "cron",
    term: "cron",
    definition:
      "A scheduler that runs a command automatically at fixed times, such as every night.",
    category,
  },
  {
    id: "webassembly",
    term: "WebAssembly",
    aliases: ["WASM"],
    definition:
      "A database operation that combines rows from two tables using a value they share.",
    category,
    caseSensitive: true,
  },
  {
    id: "gpu",
    term: "GPU",
    aliases: ["graphics processing unit"],
    definition:
      "A chip built to do many number calculations in parallel, used for graphics and for training and running models.",
    category,
  },
  {
    id: "webgl",
    term: "WebGL",
    definition:
      "A browser API that uses the GPU to draw interactive 3D graphics.",
    category,
  },
  {
    id: "canvas",
    term: "canvas",
    definition:
      "An HTML element that gives you a blank surface to draw graphics, charts or animations with code.",
    category,
  },
  {
    id: "threejs",
    term: "Three.js",
    aliases: ["threejs"],
    definition:
      "A JavaScript library that makes 3D scenes, cameras and models easier to build on top of WebGL.",
    category,
  },
  {
    id: "web-audio",
    term: "Web Audio API",
    aliases: ["Web Audio"],
    definition:
      "A browser API for loading, processing and playing sound with fine control over effects.",
    category,
  },
  {
    id: "qr-code",
    term: "QR code",
    aliases: ["QR"],
    definition:
      "A square barcode that a phone camera can scan to open a link or read a short piece of data.",
    category,
  },
  {
    id: "barcode",
    term: "barcode",
    definition:
      "A machine-readable pattern of lines or squares that identifies a product or record.",
    category,
  },
  {
    id: "sms",
    term: "SMS",
    aliases: ["text message"],
    definition:
      "A short text message sent to a phone number over the mobile network.",
    category,
  },
  {
    id: "otp",
    term: "OTP",
    aliases: ["one-time password"],
    definition:
      "A short code that works once, usually sent by SMS or email to prove it is really you.",
    category,
  },
  {
    id: "geolocation",
    term: "geolocation",
    definition:
      "The browser or device feature that reports where the user is, usually after they give permission.",
    category,
  },
  {
    id: "map-tile",
    term: "map tile",
    definition:
      "One small square image or data patch that map software loads and stitches together to show a map.",
    category,
  },
  {
    id: "cdn",
    term: "CDN",
    aliases: ["content delivery network"],
    definition:
      "A network of servers around the world that serves files from a location close to each user.",
    category,
  },
  {
    id: "observability",
    term: "observability",
    definition:
      "Being able to see what a running system is doing through logs, metrics and traces.",
    category,
  },
  {
    id: "latency",
    term: "latency",
    definition:
      "The delay between asking for something and getting the result.",
    category,
  },
  {
    id: "throughput",
    term: "throughput",
    definition:
      "How much work a system can finish in a given amount of time.",
    category,
  },
  {
    id: "sla",
    term: "SLA",
    aliases: ["service-level agreement"],
    definition:
      "A promised level of service, such as uptime or response time, that a provider agrees to meet.",
    category,
  },
  {
    id: "uptime",
    term: "uptime",
    definition:
      "The share of time a service is working and available.",
    category,
  },
  {
    id: "ci-cd",
    term: "CI/CD",
    aliases: ["CI", "continuous integration", "continuous delivery"],
    definition:
      "Automation that tests every change and, when it passes, builds and deploys it.",
    category,
  },
  {
    id: "pull-request",
    term: "pull request",
    aliases: ["PR"],
    definition:
      "A proposed set of code changes that teammates can review and discuss before it is merged.",
    category,
  },
  {
    id: "readme",
    term: "README",
    definition:
      "The main document in a project that explains what it does, how to run it and how to contribute.",
    category,
  },
  {
    id: "pytest",
    term: "pytest",
    definition:
      "A popular Python tool for writing and running automated tests.",
    category,
  },
  {
    id: "vitest",
    term: "Vitest",
    definition:
      "A fast JavaScript test runner that works closely with Vite projects.",
    category,
  },
  {
    id: "unit-test",
    term: "unit test",
    aliases: ["unit tests"],
    definition:
      "A small automated test that checks one function or piece of code in isolation.",
    category,
  },
  {
    id: "lighthouse",
    term: "Lighthouse",
    definition:
      "A browser tool that scores a page on speed, accessibility and other quality checks.",
    category,
  },
  {
    id: "accessibility",
    term: "accessibility",
    aliases: ["a11y"],
    definition:
      "Building so people with different abilities can use the product, including with a keyboard or screen reader.",
    category,
  },
  {
    id: "regex",
    term: "regex",
    aliases: ["regular expression"],
    definition:
      "A compact pattern for matching or extracting text, such as finding all dates in a document.",
    category,
  },
  {
    id: "parser",
    term: "parser",
    definition:
      "Code that reads text and turns it into a structured form the rest of the program can use.",
    category,
  },
  {
    id: "recursion",
    term: "recursion",
    definition:
      "A technique where a function calls itself on a smaller version of the same problem.",
    category,
  },
  {
    id: "dynamic-programming",
    term: "dynamic programming",
    definition:
      "Solving a problem by storing the answers to smaller repeated subproblems instead of recomputing them.",
    category,
  },
  {
    id: "graph",
    term: "graph",
    definition:
      "A set of items connected by links, useful for modelling roads, friendships or dependencies.",
    category,
  },
  {
    id: "tree",
    term: "tree",
    definition:
      "A graph with no loops, where each item has one parent and zero or more children.",
    category,
  },
  {
    id: "hash",
    term: "hash",
    definition:
      "A fixed-size fingerprint computed from data, used for fast lookup or for checking whether content changed.",
    category,
  },
  {
    id: "algorithm",
    term: "algorithm",
    definition:
      "A clear, finite set of steps for solving a problem or computing a result.",
    category,
  },
  {
    id: "data-structure",
    term: "data structure",
    definition:
      "A way of organising data in memory, such as a list, map, tree or queue.",
    category,
  },
  {
    id: "big-o",
    term: "Big O",
    definition:
      "A notation for how an algorithm's running time or memory grows as the input gets larger.",
    category,
  },
  {
    id: "compiler",
    term: "compiler",
    definition:
      "A program that translates source code into another form, often machine code, before it runs.",
    category,
  },
  {
    id: "interpreter",
    term: "interpreter",
    definition:
      "A program that runs source code directly, translating and executing it step by step.",
    category,
  },
  {
    id: "runtime",
    term: "runtime",
    definition:
      "The environment and support code that a program needs while it is actually running.",
    category,
  },
  {
    id: "garbage-collection",
    term: "garbage collection",
    definition:
      "Automatic cleanup of memory that a program no longer uses, so the programmer does not have to free it by hand.",
    category,
  },
  {
    id: "memory-leak",
    term: "memory leak",
    definition:
      "A bug where a program keeps memory it no longer needs, so usage grows until it slows down or crashes.",
    category,
  },
  {
    id: "sandbox",
    term: "sandbox",
    definition:
      "An isolated space where code can run without being able to harm the rest of the system.",
    category,
  },
  {
    id: "ui",
    term: "UI",
    aliases: ["user interface"],
    definition:
      "The parts of a product a person sees and interacts with: screens, buttons, forms and messages.",
    category,
  },
  {
    id: "ux",
    term: "UX",
    aliases: ["user experience"],
    definition:
      "How a product feels to use: whether the flow is clear, fast and pleasant.",
    category,
  },
  {
    id: "mvp",
    term: "MVP",
    aliases: ["minimum viable product"],
    definition:
      "The smallest version of a product that still solves the core problem for a real user.",
    category,
  },
];
