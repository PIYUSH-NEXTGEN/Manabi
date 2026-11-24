import type { GlossaryEntry } from "./types";

const systems = "Systems & security" as const;
const world = "World & work" as const;

export const SYSTEMS_TERMS: GlossaryEntry[] = [
  {
    id: "encryption",
    term: "encryption",
    definition:
      "Scrambling data with a key so only someone with the right key can read it.",
    category: systems,
  },
  {
    id: "hashing",
    term: "hashing",
    definition:
      "Turning data into a fixed-size fingerprint. It cannot be reversed, and the same input always gives the same output.",
    category: systems,
  },
  {
    id: "sha1",
    term: "SHA-1",
    aliases: ["SHA1"],
    definition:
      "An older hashing algorithm. It is fine for checking file fingerprints but too weak for modern password security.",
    category: systems,
  },
  {
    id: "salt",
    term: "salt",
    definition:
      "Random data added to a password before hashing so two people with the same password still get different hashes.",
    category: systems,
  },
  {
    id: "authentication",
    term: "authentication",
    definition:
      "Proving who you are, usually with a password, a code or a login provider.",
    category: systems,
  },
  {
    id: "authorization",
    term: "authorization",
    definition:
      "Deciding what an authenticated person is allowed to see or do.",
    category: systems,
  },
  {
    id: "oauth",
    term: "OAuth",
    definition:
      "A standard way to let a user sign in to one service with another account without sharing that account's password.",
    category: systems,
  },
  {
    id: "jwt",
    term: "JWT",
    aliases: ["JSON Web Token"],
    definition:
      "A signed token that carries a small set of claims about a user between services.",
    category: systems,
  },
  {
    id: "csrf",
    term: "CSRF",
    aliases: ["cross-site request forgery"],
    definition:
      "An attack that tricks a logged-in browser into sending a request the user never intended.",
    category: systems,
  },
  {
    id: "xss",
    term: "XSS",
    aliases: ["cross-site scripting"],
    definition:
      "An attack that injects malicious script into a page so it runs in other users' browsers.",
    category: systems,
  },
  {
    id: "sql-injection",
    term: "SQL injection",
    definition:
      "An attack that hides database commands inside user input so the database executes them.",
    category: systems,
  },
  {
    id: "rbac",
    term: "RBAC",
    aliases: ["role-based access control"],
    definition:
      "Giving permissions to roles such as student or admin, then assigning people to those roles.",
    category: systems,
  },
  {
    id: "kyc",
    term: "KYC",
    aliases: ["know your customer"],
    definition:
      "Checks that a financial service must run to confirm a customer's identity before doing business with them.",
    category: systems,
  },
  {
    id: "audit-log",
    term: "audit log",
    definition:
      "An append-only record of who did what and when, kept so actions can be reviewed later.",
    category: systems,
  },
  {
    id: "pii",
    term: "PII",
    aliases: ["personally identifiable information"],
    definition:
      "Data that can identify a specific person, such as a name, phone number or address.",
    category: systems,
  },
  {
    id: "multi-tenant",
    term: "multi-tenant",
    definition:
      "One running app serves many separate organisations while keeping each one's data apart.",
    category: systems,
  },
  {
    id: "etag",
    term: "ETag",
    aliases: ["entity tag"],
    definition:
      "A short fingerprint a server sends with a file so the browser can skip downloading it again when it has not changed.",
    category: systems,
  },
  {
    id: "transaction",
    term: "transaction",
    definition:
      "A group of changes that must all succeed or all roll back together; also one payment or exchange.",
    category: systems,
  },
  {
    id: "acid",
    term: "ACID",
    definition:
      "Four guarantees that make database transactions reliable: atomicity, consistency, isolation and durability.",
    category: systems,
    caseSensitive: true,
  },
  {
    id: "reconciliation",
    term: "reconciliation",
    definition:
      "Comparing two sets of records to find and explain the differences between them.",
    category: systems,
  },
  {
    id: "ledger",
    term: "ledger",
    definition:
      "A running record of money movements, usually kept so every entry can be traced.",
    category: systems,
  },
  {
    id: "double-entry",
    term: "double-entry bookkeeping",
    aliases: ["double-entry"],
    definition:
      "Bookkeeping where every transaction is recorded as matching debits and credits so the books stay balanced.",
    category: world,
  },
  {
    id: "payment-gateway",
    term: "payment gateway",
    aliases: ["Stripe", "Razorpay"],
    definition:
      "A service that securely passes card or bank payments between a business and the payment network.",
    category: systems,
  },
  {
    id: "upi",
    term: "UPI",
    aliases: ["Unified Payments Interface"],
    definition:
      "India's instant bank-to-bank payment system, usually triggered from a phone app.",
    category: systems,
  },
  {
    id: "emv",
    term: "EMV",
    definition:
      "The chip standard used by most bank cards, which makes copying card data much harder.",
    category: systems,
  },
  {
    id: "pin-code",
    term: "PIN",
    aliases: ["PIN code", "personal identification number"],
    definition:
      "A short number used to unlock a card, phone or account.",
    category: systems,
    caseSensitive: true,
  },
  {
    id: "database",
    term: "database",
    definition:
      "An organised store of data that can be searched, filtered and updated.",
    category: systems,
  },
  {
    id: "sql",
    term: "SQL",
    aliases: ["structured query language"],
    definition:
      "The standard language for asking a relational database for data or changing it.",
    category: systems,
  },
  {
    id: "sqlite",
    term: "SQLite",
    definition:
      "A small file-based database built into many apps and phones.",
    category: systems,
  },
  {
    id: "postgres",
    term: "PostgreSQL",
    aliases: ["Postgres"],
    definition:
      "A powerful open-source relational database used by many production apps.",
    category: systems,
  },
  {
    id: "query",
    term: "query",
    definition:
      "A request for specific data from a database or search system.",
    category: systems,
  },
  {
    id: "join",
    term: "JOIN",
    definition:
      "A database operation that combines rows from two tables using a value they share.",
    category: systems,
  },
  {
    id: "migration",
    term: "migration",
    definition:
      "A versioned change to a database's structure, applied in order so every environment stays in sync.",
    category: systems,
  },
  {
    id: "orm",
    term: "ORM",
    aliases: ["object-relational mapper"],
    definition:
      "A library that lets code work with database rows as objects instead of writing SQL by hand.",
    category: systems,
  },
  {
    id: "time-series",
    term: "time series",
    aliases: ["time-series"],
    definition:
      "A sequence of values recorded over time, such as daily prices or hourly sensor readings.",
    category: systems,
  },
  {
    id: "csv",
    term: "CSV",
    aliases: ["comma-separated values"],
    definition:
      "A plain-text table where commas separate the columns.",
    category: systems,
  },
  {
    id: "pandas",
    term: "Pandas",
    definition:
      "A Python library for loading, cleaning and analysing tabular data.",
    category: systems,
  },
  {
    id: "numpy",
    term: "NumPy",
    definition:
      "A Python library for fast numerical arrays and maths.",
    category: systems,
  },
  {
    id: "scipy",
    term: "SciPy",
    definition:
      "A Python library of scientific algorithms built on top of NumPy.",
    category: systems,
  },
  {
    id: "scikit-learn",
    term: "scikit-learn",
    aliases: ["sklearn"],
    definition:
      "A Python library of standard machine-learning models and evaluation tools.",
    category: systems,
  },
  {
    id: "matplotlib",
    term: "Matplotlib",
    definition:
      "A Python library for making charts and plots.",
    category: systems,
  },
  {
    id: "plotly",
    term: "Plotly",
    definition:
      "A charting library for interactive plots in browsers and notebooks.",
    category: systems,
  },
  {
    id: "seaborn",
    term: "Seaborn",
    definition:
      "A Python charting library built on Matplotlib with ready-made statistical plot styles.",
    category: systems,
  },
  {
    id: "streamlit",
    term: "Streamlit",
    definition:
      "A Python tool that turns scripts into simple interactive web apps.",
    category: systems,
  },
  {
    id: "jupyter",
    term: "Jupyter",
    definition:
      "A notebook environment that mixes code, output and notes in one document.",
    category: systems,
  },
  {
    id: "xarray",
    term: "xarray",
    definition:
      "A Python library for labelled multi-dimensional arrays, common in weather and climate data.",
    category: systems,
  },
  {
    id: "data-visualization",
    term: "data visualization",
    aliases: ["data visualisation"],
    definition:
      "Showing data as charts or maps so patterns are easier to see.",
    category: systems,
  },
  {
    id: "statistics",
    term: "statistics",
    definition:
      "The maths of collecting, summarising and drawing conclusions from data.",
    category: systems,
  },
  {
    id: "correlation",
    term: "correlation",
    definition:
      "A measure of how two things move together. It does not prove that one causes the other.",
    category: systems,
  },
  {
    id: "causation",
    term: "causation",
    definition:
      "When a change in one thing actually produces a change in another.",
    category: systems,
  },
  {
    id: "prediction-interval",
    term: "prediction interval",
    definition:
      "A range that is likely to contain a future value, given the model's uncertainty.",
    category: systems,
  },
  {
    id: "provenance",
    term: "provenance",
    definition:
      "The record of where data came from and how it has been changed since.",
    category: systems,
  },
  {
    id: "ngo",
    term: "NGO",
    aliases: ["non-governmental organization"],
    definition:
      "A non-governmental organisation, usually a non-profit working on a social or environmental mission.",
    category: world,
  },
  {
    id: "ecommerce",
    term: "ecommerce",
    aliases: ["e-commerce"],
    definition:
      "Buying and selling goods or services online.",
    category: world,
  },
  {
    id: "rss",
    term: "RSS",
    aliases: ["really simple syndication"],
    definition:
      "A simple feed format that lets apps follow new posts from a website.",
    category: world,
  },
  {
    id: "m3u",
    term: "M3U",
    definition:
      "A plain-text playlist format that lists where media files or streams are located.",
    category: world,
  },
  {
    id: "musicbrainz",
    term: "MusicBrainz",
    definition:
      "An open database of music artists, releases and recordings.",
    category: world,
  },
  {
    id: "listenbrainz",
    term: "ListenBrainz",
    definition:
      "An open service that records and shares what music people listen to.",
    category: world,
  },
  {
    id: "lastfm",
    term: "Last.fm",
    aliases: ["Lastfm"],
    definition:
      "A music service that tracks listening history and recommends similar artists.",
    category: world,
  },
  {
    id: "stylometry",
    term: "stylometry",
    aliases: ["stylometric"],
    definition:
      "Identifying an author from patterns in how they write, such as word choice and sentence length.",
    category: world,
  },
  {
    id: "pdf",
    term: "PDF",
    aliases: ["portable document format"],
    definition:
      "A fixed-layout document format that looks the same on different devices.",
    category: world,
  },
  {
    id: "markdown",
    term: "Markdown",
    definition:
      "A lightweight way to write formatted text using plain characters like # and *.",
    category: world,
  },
  {
    id: "citation",
    term: "citation",
    definition:
      "A reference that says where a fact, quote or dataset came from.",
    category: world,
  },
  {
    id: "moderation",
    term: "content moderation",
    aliases: ["moderation"],
    definition:
      "Reviewing user content to remove abuse, spam or illegal material.",
    category: world,
  },
  {
    id: "notifications",
    term: "notifications",
    aliases: ["notification"],
    definition:
      "Messages a product sends to tell a user that something happened or needs attention.",
    category: world,
  },
  {
    id: "workflow",
    term: "workflow",
    definition:
      "A defined sequence of steps and decisions for completing a process.",
    category: world,
  },
  {
    id: "scheduling",
    term: "scheduling",
    definition:
      "Deciding when tasks or events should happen, often around other constraints.",
    category: world,
  },
  {
    id: "routing",
    term: "routing",
    definition:
      "Choosing the path or the person that a request, vehicle or task should go to.",
    category: world,
  },
  {
    id: "multilingual",
    term: "multilingual",
    definition:
      "Working with more than one language.",
    category: world,
  },
  {
    id: "translation",
    term: "translation",
    definition:
      "Converting text or speech from one language into another.",
    category: world,
  },
  {
    id: "open-source",
    term: "open source",
    aliases: ["open-source"],
    definition:
      "Software whose source code is public and can be used, changed and shared under a licence.",
    category: world,
  },
];
