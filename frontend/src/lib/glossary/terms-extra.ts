import type { GlossaryEntry } from "./types";

const ai = "AI & data" as const;
const web = "Web & code" as const;
const science = "Science" as const;
const systems = "Systems & security" as const;
const world = "World & work" as const;

export const EXTRA_TERMS: GlossaryEntry[] = [
  {
    id: "token",
    term: "token",
    aliases: ["tokens"],
    definition:
      "One small piece of text, such as a word or word part, that a language model reads.",
    category: ai,
  },
  {
    id: "tokenizer",
    term: "tokenizer",
    definition:
      "A tool that splits text into tokens before a model reads it.",
    category: ai,
  },
  {
    id: "autograd",
    term: "autograd",
    aliases: ["automatic differentiation"],
    definition:
      "Software that automatically computes gradients for a model, so you do not have to derive them by hand.",
    category: ai,
  },
  {
    id: "tool-use",
    term: "tool use",
    aliases: ["tool-use"],
    definition:
      "Letting an AI model call outside functions or APIs to fetch data or perform actions.",
    category: ai,
  },
  {
    id: "image-translation",
    term: "image-to-image translation",
    aliases: ["image translation"],
    definition:
      "Turning an image from one style or domain into another, such as a photo into a painting.",
    category: ai,
  },
  {
    id: "layout-parsing",
    term: "layout parsing",
    aliases: ["layout-parsing"],
    definition:
      "Reading a document's structure, such as headings, tables and columns, not just its raw text.",
    category: ai,
  },
  {
    id: "community-detection",
    term: "community detection",
    aliases: ["community-detection"],
    definition:
      "Finding groups of nodes in a graph that are more connected to each other than to the rest.",
    category: ai,
  },
  {
    id: "ranking",
    term: "ranking",
    definition:
      "Ordering results from most to least relevant.",
    category: ai,
  },
  {
    id: "realtime",
    term: "real time",
    aliases: ["realtime", "real-time"],
    definition:
      "Handling events as they happen, with little or no delay.",
    category: web,
  },
  {
    id: "network-model",
    term: "network model",
    aliases: ["network-model"],
    definition:
      "A model of people or things as nodes and links, used to study how something spreads.",
    category: ai,
  },
  {
    id: "unit-normalization",
    term: "unit normalization",
    aliases: ["unit-normalization", "unit-aware"],
    definition:
      "Converting measurements to a common unit before comparing or combining them.",
    category: ai,
  },
  {
    id: "alpha-beta",
    term: "alpha-beta pruning",
    aliases: ["alpha-beta"],
    definition:
      "A search shortcut that skips moves which cannot improve the result, so game AI can look further ahead.",
    category: ai,
  },
  {
    id: "deepfake",
    term: "deepfake",
    definition:
      "A fake image, video or recording made with AI to look or sound real.",
    category: ai,
  },
  {
    id: "fairness",
    term: "fairness",
    definition:
      "Making sure a model does not systematically disadvantage a group of people.",
    category: ai,
  },
  {
    id: "misinformation",
    term: "misinformation",
    definition:
      "False or misleading information spread as if it were true.",
    category: ai,
  },
  {
    id: "patchcore",
    term: "PatchCore",
    definition:
      "An anomaly-detection method that compares image patches with a stored memory of normal examples.",
    category: ai,
  },
  {
    id: "mnist",
    term: "MNIST",
    definition:
      "A classic dataset of handwritten digits used to learn and compare image classifiers.",
    category: ai,
  },
  {
    id: "plantvillage",
    term: "PlantVillage",
    definition:
      "A public dataset of labelled plant-leaf photos, mostly taken under controlled conditions.",
    category: ai,
  },
  {
    id: "plantdoc",
    term: "PlantDoc",
    definition:
      "A dataset of plant-disease photos taken in real field conditions.",
    category: ai,
  },
  {
    id: "trashnet",
    term: "TrashNet",
    definition:
      "A public dataset of waste photos sorted into recycling categories.",
    category: ai,
  },
  {
    id: "mvtec",
    term: "MVTec AD",
    aliases: ["MVTec"],
    definition:
      "A standard dataset of industrial images used to test anomaly detection.",
    category: ai,
  },
  {
    id: "esol",
    term: "ESOL",
    definition:
      "A public dataset of molecules with measured water solubility.",
    category: ai,
  },
  {
    id: "hc3",
    term: "HC3",
    definition:
      "A dataset of human and chatbot answers used to study AI-generated text.",
    category: ai,
  },
  {
    id: "nodejs",
    term: "Node.js",
    aliases: ["Nodejs"],
    definition:
      "A runtime that lets JavaScript run outside the browser, usually on a server.",
    category: web,
  },
  {
    id: "browser-extension",
    term: "browser extension",
    aliases: ["Chrome extension"],
    definition:
      "A small add-on that adds features to a web browser.",
    category: web,
  },
  {
    id: "lazy-loading",
    term: "lazy loading",
    aliases: ["lazy-loading"],
    definition:
      "Loading code, images or data only when they are needed, so the first screen appears faster.",
    category: web,
  },
  {
    id: "fastapi",
    term: "FastAPI",
    definition:
      "A Python framework for building APIs quickly, with automatic documentation.",
    category: web,
  },
  {
    id: "pytorch",
    term: "PyTorch",
    definition:
      "An open-source deep-learning library that builds models as differentiable programs.",
    category: web,
  },
  {
    id: "pytorch-geometric",
    term: "PyTorch Geometric",
    definition:
      "A library for building graph neural networks with PyTorch.",
    category: web,
  },
  {
    id: "huggingface",
    term: "Hugging Face",
    aliases: ["Huggingface"],
    definition:
      "A company and hub for sharing machine-learning models, datasets and tools.",
    category: web,
  },
  {
    id: "networkx",
    term: "NetworkX",
    definition:
      "A Python library for building, drawing and analysing graphs.",
    category: web,
  },
  {
    id: "opencv",
    term: "OpenCV",
    definition:
      "An open-source library of computer-vision tools for images and video.",
    category: web,
  },
  {
    id: "sentence-transformers",
    term: "Sentence Transformers",
    definition:
      "A library that turns sentences into embeddings for search and similarity.",
    category: web,
  },
  {
    id: "statsmodels",
    term: "statsmodels",
    definition:
      "A Python library for statistical models, tests and time-series analysis.",
    category: web,
  },
  {
    id: "sympy",
    term: "SymPy",
    definition:
      "A Python library for symbolic maths, such as solving equations exactly.",
    category: web,
  },
  {
    id: "geopandas",
    term: "GeoPandas",
    definition:
      "A Python library that adds geographic data handling to Pandas.",
    category: web,
  },
  {
    id: "rasterio",
    term: "Rasterio",
    definition:
      "A Python library for reading and writing geospatial raster data.",
    category: web,
  },
  {
    id: "pint",
    term: "Pint",
    definition:
      "A Python library that keeps track of physical units during calculations.",
    category: web,
  },
  {
    id: "repository",
    term: "repository",
    aliases: ["repo"],
    definition:
      "A project's folder of code plus its saved history, often hosted on GitHub.",
    category: web,
  },
  {
    id: "commit",
    term: "commit",
    definition:
      "A saved snapshot of code changes, with a message explaining what changed.",
    category: web,
  },
  {
    id: "branch",
    term: "branch",
    definition:
      "A separate line of development that lets you work without changing the main version.",
    category: web,
  },
  {
    id: "merge",
    term: "merge",
    definition:
      "Combining the changes from one branch into another.",
    category: web,
  },
  {
    id: "diff",
    term: "diff",
    definition:
      "A line-by-line comparison of two versions of code or data.",
    category: web,
  },
  {
    id: "pagination",
    term: "pagination",
    definition:
      "Splitting a long list of results into smaller pages.",
    category: web,
  },
  {
    id: "dependency",
    term: "dependency",
    aliases: ["dependencies"],
    definition:
      "A library or package that your project relies on.",
    category: web,
  },
  {
    id: "iss",
    term: "ISS",
    aliases: ["International Space Station"],
    definition:
      "The International Space Station: a crewed laboratory that orbits Earth about every 90 minutes.",
    category: science,
  },
  {
    id: "altitude",
    term: "altitude",
    definition:
      "Height above sea level or above a reference surface such as Earth's surface.",
    category: science,
  },
  {
    id: "orbital-mechanics",
    term: "orbital mechanics",
    aliases: ["orbital-mechanics"],
    definition:
      "The physics of how objects move in space under gravity.",
    category: science,
  },
  {
    id: "ip-address",
    term: "IP address",
    aliases: ["IP"],
    definition:
      "A numeric address that identifies a device on a network so data can reach it.",
    category: systems,
    caseSensitive: true,
  },
  {
    id: "mage",
    term: "MAGE",
    definition:
      "A benchmark dataset of machine-generated and human-written text used to study AI-text detection.",
    category: ai,
    caseSensitive: true,
  },
  {
    id: "webcam",
    term: "webcam",
    definition:
      "A camera connected to or built into a computer, usually used for video calls or capture.",
    category: web,
  },
  {
    id: "face-detection",
    term: "face detection",
    definition:
      "Finding where faces appear in an image, without deciding who they belong to.",
    category: ai,
  },
  {
    id: "face-recognition",
    term: "face recognition",
    definition:
      "Identifying or verifying a person from an image of their face.",
    category: ai,
  },
  {
    id: "manifest-v3",
    term: "manifest v3",
    definition:
      "The current rules and API model for Chrome extensions, including stricter permissions and background workers.",
    category: web,
  },
  {
    id: "content-script",
    term: "content script",
    definition:
      "A script that a browser extension injects into a web page to read or change it.",
    category: web,
  },
  {
    id: "keep-alive",
    term: "keep-alive",
    aliases: ["keep alive"],
    definition:
      "Keeping a network connection open so later requests can reuse it instead of starting over.",
    category: web,
  },
  {
    id: "http-status-code",
    term: "HTTP status code",
    aliases: ["status code"],
    definition:
      "A three-digit number in an HTTP response that says whether the request worked, and why not if it failed.",
    category: web,
  },
  {
    id: "payload",
    term: "payload",
    definition:
      "The actual data carried inside a request, response or message, separate from its headers and framing.",
    category: web,
  },
  {
    id: "fintech",
    term: "fintech",
    definition:
      "Technology used to provide financial services such as payments, lending or banking.",
    category: world,
  },
  {
    id: "carbon-footprint",
    term: "carbon footprint",
    definition:
      "The total greenhouse-gas emissions caused by a product, activity or person.",
    category: science,
  },
  {
    id: "open-food-facts",
    term: "Open Food Facts",
    definition:
      "A public, open database of food products and their ingredients, nutrition and environmental scores.",
    category: world,
  },
  {
    id: "green-score",
    term: "Green-Score",
    aliases: ["Green Score"],
    definition:
      "An environmental score from Open Food Facts that estimates a food product's impact.",
    category: world,
  },
  {
    id: "attribution",
    term: "attribution",
    definition:
      "Crediting or recording where a piece of data, quote or creative work came from.",
    category: world,
  },
  {
    id: "matching",
    term: "matching",
    definition:
      "Deciding which items or people go together, usually by comparing their features or preferences.",
    category: ai,
  },
  {
    id: "permission",
    term: "permission",
    definition:
      "A rule that says whether a user may view, change or perform something.",
    category: systems,
  },
  {
    id: "opt-in",
    term: "opt-in",
    aliases: ["opt in", "opted-in"],
    definition:
      "A choice a person actively makes to share data or receive something, rather than being signed up by default.",
    category: systems,
  },
  {
    id: "protocol",
    term: "protocol",
    definition:
      "An agreed set of rules for how computers exchange data, such as HTTP or TCP.",
    category: web,
  },
  {
    id: "framework",
    term: "framework",
    definition:
      "A reusable set of code and conventions that gives structure to an application.",
    category: web,
  },
  {
    id: "autoencoder",
    term: "autoencoder",
    definition:
      "A neural network trained to compress data and reconstruct it, often used to spot unusual inputs.",
    category: ai,
  },
  {
    id: "compression",
    term: "compression",
    definition:
      "Reducing the size of data or media so it takes less space or bandwidth.",
    category: web,
  },
];
