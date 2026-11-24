import type { GlossaryEntry } from "./types";

const category = "Science" as const;

export const SCIENCE_TERMS: GlossaryEntry[] = [
  {
    id: "satellite",
    term: "satellite",
    definition:
      "A machine placed in orbit around Earth or another body to observe, communicate or navigate.",
    category,
  },
  {
    id: "orbit",
    term: "orbit",
    definition:
      "The curved path an object follows around a larger body because of gravity.",
    category,
  },
  {
    id: "orbital-elements",
    term: "orbital elements",
    definition:
      "The set of numbers that describes a satellite's orbit: its shape, tilt, size and position at a given time.",
    category,
  },
  {
    id: "tle",
    term: "TLE",
    aliases: ["two-line element set"],
    definition:
      "A compact two-line text record of a satellite's orbital elements, published so others can predict where it will be.",
    category,
  },
  {
    id: "sgp4",
    term: "SGP4",
    definition:
      "A standard model that takes a satellite's TLE and predicts its position at a chosen time.",
    category,
  },
  {
    id: "ephemeris",
    term: "ephemeris",
    definition:
      "A table or calculation of where a satellite or celestial object will be at specific times.",
    category,
  },
  {
    id: "horizon",
    term: "horizon",
    definition:
      "The line where the sky appears to meet the ground from a viewer's position; a satellite is visible only when it is above it.",
    category,
  },
  {
    id: "overpass",
    term: "overpass",
    aliases: ["satellite pass"],
    definition:
      "One trip in which a satellite rises above the horizon, crosses the sky and sets again.",
    category,
  },
  {
    id: "azimuth",
    term: "azimuth",
    definition:
      "The compass direction of an object in the sky, measured in degrees clockwise from north.",
    category,
  },
  {
    id: "elevation-angle",
    term: "elevation angle",
    definition:
      "How high an object sits above the horizon, measured in degrees from 0 at the horizon to 90 straight up.",
    category,
  },
  {
    id: "ground-track",
    term: "ground track",
    definition:
      "The path on Earth's surface directly beneath a satellite as it moves.",
    category,
  },
  {
    id: "sky-chart",
    term: "sky chart",
    definition:
      "A map of the sky from a particular place and time, showing where objects appear.",
    category,
  },
  {
    id: "sidereal-time",
    term: "sidereal time",
    definition:
      "Time measured by Earth's rotation relative to the stars, used to point telescopes and track objects.",
    category,
  },
  {
    id: "conjunction",
    term: "conjunction",
    definition:
      "A moment when two objects in the sky appear very close together, or when satellites pass dangerously near each other.",
    category,
  },
  {
    id: "hohmann-transfer",
    term: "Hohmann transfer",
    definition:
      "A fuel-efficient two-burn manoeuvre that moves a spacecraft between two circular orbits.",
    category,
  },
  {
    id: "bi-elliptic-transfer",
    term: "bi-elliptic transfer",
    definition:
      "A three-burn orbit change that can use less fuel than a Hohmann transfer when the orbits differ greatly.",
    category,
  },
  {
    id: "delta-v",
    term: "delta-v",
    definition:
      "The total change in speed a spacecraft needs for a manoeuvre; it is the main measure of fuel cost.",
    category,
  },
  {
    id: "light-curve",
    term: "light curve",
    definition:
      "A graph of how bright an object is over time, used to find planets, variable stars and rotation.",
    category,
  },
  {
    id: "planetary-transit",
    term: "planetary transit",
    definition:
      "When a planet passes in front of its star, blocking a small amount of light and revealing that it exists.",
    category,
  },
  {
    id: "occultation",
    term: "occultation",
    definition:
      "When one object passes in front of another and hides it from view.",
    category,
  },
  {
    id: "magnitude",
    term: "magnitude",
    definition:
      "The size of something; in astronomy, a brightness scale where smaller numbers mean brighter objects.",
    category,
  },
  {
    id: "exoplanet",
    term: "exoplanet",
    definition:
      "A planet that orbits a star other than the Sun.",
    category,
  },
  {
    id: "tess",
    term: "TESS",
    aliases: ["Transiting Exoplanet Survey Satellite"],
    definition:
      "A NASA space telescope that watches bright nearby stars for the small dips caused by passing planets.",
    category,
  },
  {
    id: "sdss",
    term: "SDSS",
    aliases: ["Sloan Digital Sky Survey"],
    definition:
      "A long-running survey that has mapped millions of stars and galaxies and released the data publicly.",
    category,
  },
  {
    id: "nasa",
    term: "NASA",
    definition:
      "The United States space agency, which runs missions and publishes many open space datasets.",
    category,
  },
  {
    id: "jpl",
    term: "JPL",
    aliases: ["Jet Propulsion Laboratory"],
    definition:
      "A NASA research centre that builds spacecraft and publishes tools and data for orbit and mission work.",
    category,
  },
  {
    id: "gibs",
    term: "GIBS",
    aliases: ["Global Imagery Browse Services"],
    definition:
      "A NASA service that serves near-real-time satellite imagery as map tiles.",
    category,
  },
  {
    id: "lightkurve",
    term: "Lightkurve",
    definition:
      "A Python library for downloading and cleaning space-telescope light curves.",
    category,
  },
  {
    id: "astropy",
    term: "Astropy",
    definition:
      "A Python library for astronomy calculations such as coordinates, units and time.",
    category,
  },
  {
    id: "schrodinger-equation",
    term: "Schrödinger equation",
    aliases: ["Schrodinger equation"],
    definition:
      "The core equation of quantum mechanics: it describes how a particle's wavefunction changes over time.",
    category,
  },
  {
    id: "wave-packet",
    term: "wave packet",
    definition:
      "A localised bundle of waves used to represent a particle that is not spread across all space.",
    category,
  },
  {
    id: "wavefunction",
    term: "wavefunction",
    definition:
      "The mathematical object that stores the probability of finding a particle in each possible position.",
    category,
  },
  {
    id: "potential-barrier",
    term: "potential barrier",
    definition:
      "A region where a particle's energy would have to rise; quantum mechanics allows it to tunnel through.",
    category,
  },
  {
    id: "quantum-tunneling",
    term: "quantum tunnelling",
    aliases: ["quantum tunneling", "tunneling"],
    definition:
      "A quantum effect where a particle passes through an energy barrier it could not cross in everyday physics.",
    category,
  },
  {
    id: "interference",
    term: "interference",
    definition:
      "When two waves add together to become stronger or cancel out, producing a pattern.",
    category,
  },
  {
    id: "reflection",
    term: "reflection",
    definition:
      "When a wave bounces back after hitting a boundary.",
    category,
  },
  {
    id: "transmission",
    term: "transmission",
    definition:
      "How much of a wave passes through a barrier, or how easily something spreads from one place or person to another.",
    category,
  },
  {
    id: "superposition",
    term: "superposition",
    definition:
      "A quantum state that is a combination of several possibilities at once.",
    category,
  },
  {
    id: "energy-level",
    term: "energy level",
    definition:
      "One of the fixed amounts of energy a quantum system is allowed to have.",
    category,
  },
  {
    id: "one-dimensional",
    term: "one-dimensional",
    aliases: ["one dimensional", "1D"],
    definition:
      "A problem where only one direction or variable matters, such as position along a straight line.",
    category,
  },
  {
    id: "pde",
    term: "PDE",
    aliases: ["partial differential equation"],
    definition:
      "An equation that relates how a quantity changes in more than one direction or in time.",
    category,
  },
  {
    id: "ode",
    term: "ODE",
    aliases: ["ordinary differential equation"],
    definition:
      "An equation that relates a quantity to its own rate of change, usually over time.",
    category,
  },
  {
    id: "numerical-method",
    term: "numerical method",
    definition:
      "A way to approximate a maths answer with repeated calculations when no exact formula is practical.",
    category,
  },
  {
    id: "finite-difference",
    term: "finite difference",
    definition:
      "Approximating a derivative by comparing values at nearby points on a grid.",
    category,
  },
  {
    id: "grid",
    term: "grid",
    definition:
      "A set of evenly spaced points used to compute a simulation or draw a map.",
    category,
  },
  {
    id: "time-step",
    term: "time step",
    definition:
      "The small jump forward in time that a simulation makes on each calculation.",
    category,
  },
  {
    id: "boundary-condition",
    term: "boundary condition",
    definition:
      "A rule that says what happens at the edges of a simulated region.",
    category,
  },
  {
    id: "rk4",
    term: "RK4",
    aliases: ["Runge-Kutta"],
    definition:
      "A common method that takes four small estimates per step to solve differential equations accurately.",
    category,
  },
  {
    id: "analytic-solution",
    term: "analytic solution",
    definition:
      "An exact answer written as a formula, rather than an approximation computed step by step.",
    category,
  },
  {
    id: "simulation",
    term: "simulation",
    definition:
      "Running a model of a system step by step to see how it behaves over time.",
    category,
  },
  {
    id: "system-identification",
    term: "system identification",
    definition:
      "Working out the equations or settings of a system by watching how it responds to inputs.",
    category,
  },
  {
    id: "sindy",
    term: "SINDy",
    aliases: ["sparse identification of nonlinear dynamics"],
    definition:
      "A method that discovers simple governing equations from measured data.",
    category,
  },
  {
    id: "convergence",
    term: "convergence",
    definition:
      "When a repeated calculation gets closer and closer to a stable answer.",
    category,
  },
  {
    id: "tolerance",
    term: "tolerance",
    definition:
      "The small error allowed before a calculation is treated as close enough to the exact answer.",
    category,
  },
  {
    id: "numerical-error",
    term: "numerical error",
    definition:
      "The gap between an approximate computed answer and the exact one.",
    category,
  },
  {
    id: "signal-processing",
    term: "signal processing",
    definition:
      "Cleaning, filtering and measuring signals such as audio, sensor readings or images.",
    category,
  },
  {
    id: "spectrum",
    term: "spectrum",
    aliases: ["spectra"],
    definition:
      "The mix of frequencies or wavelengths in a signal or beam of light.",
    category,
  },
  {
    id: "sensor",
    term: "sensor",
    definition:
      "A device that measures something physical, such as temperature, motion, light or location.",
    category,
  },
  {
    id: "smiles",
    term: "SMILES",
    definition:
      "A short text notation for writing a chemical structure as a string a computer can parse.",
    category,
    caseSensitive: true,
  },
  {
    id: "rdkit",
    term: "RDKit",
    definition:
      "An open-source toolkit for reading, drawing and analysing molecules in code.",
    category,
  },
  {
    id: "lipinski",
    term: "Lipinski's rule of five",
    aliases: ["Lipinski"],
    definition:
      "Four simple rules that estimate whether a drug-like molecule is likely to be absorbed well by the body.",
    category,
  },
  {
    id: "molecular-fingerprint",
    term: "molecular fingerprint",
    definition:
      "A compact pattern of numbers that records which chemical features a molecule has, used to compare molecules.",
    category,
  },
  {
    id: "pubchem",
    term: "PubChem",
    definition:
      "A public database of chemical compounds, their structures and their properties.",
    category,
  },
  {
    id: "moleculenet",
    term: "MoleculeNet",
    definition:
      "A collection of standard chemistry datasets used to compare machine-learning models fairly.",
    category,
  },
  {
    id: "cheminformatics",
    term: "cheminformatics",
    definition:
      "Using computers to store, search and analyse chemical structures and properties.",
    category,
  },
  {
    id: "bioinformatics",
    term: "bioinformatics",
    definition:
      "Using computers to analyse biological data such as DNA, RNA and protein sequences.",
    category,
  },
  {
    id: "dna",
    term: "DNA",
    definition:
      "The molecule that stores the instructions for building and running a living thing.",
    category,
  },
  {
    id: "codon",
    term: "codon",
    definition:
      "A group of three DNA or RNA letters that codes for one amino acid or a stop signal.",
    category,
  },
  {
    id: "orf",
    term: "ORF",
    aliases: ["open reading frame"],
    definition:
      "A stretch of DNA that can be read as a run of codons without an early stop.",
    category,
  },
  {
    id: "fasta",
    term: "FASTA",
    definition:
      "A plain-text format for a DNA, RNA or protein sequence with a short header line.",
    category,
  },
  {
    id: "uniprot",
    term: "UniProt",
    definition:
      "A public catalogue of protein sequences and what is known about them.",
    category,
  },
  {
    id: "ncbi",
    term: "NCBI",
    aliases: ["National Center for Biotechnology Information"],
    definition:
      "A United States public database that hosts DNA, protein and biomedical research data.",
    category,
  },
  {
    id: "sequence-alignment",
    term: "sequence alignment",
    definition:
      "Lining up two DNA, RNA or protein sequences to see where they match, differ or have gaps.",
    category,
  },
  {
    id: "needleman-wunsch",
    term: "Needleman-Wunsch",
    definition:
      "An algorithm that finds the best overall alignment of two sequences from end to end.",
    category,
  },
  {
    id: "smith-waterman",
    term: "Smith-Waterman",
    definition:
      "An algorithm that finds the best matching local region within two sequences.",
    category,
  },
  {
    id: "epidemiology",
    term: "epidemiology",
    definition:
      "The study of how disease spreads through a population and what reduces it.",
    category,
  },
  {
    id: "sir-model",
    term: "SIR model",
    aliases: ["SIR", "SIR curve"],
    definition:
      "A simple epidemic model that moves people between susceptible, infected and recovered groups.",
    category,
    caseSensitive: true,
  },
  {
    id: "r0",
    term: "R0",
    aliases: ["basic reproduction number"],
    definition:
      "The average number of people one infected person would pass an infection to in a fully susceptible population.",
    category,
    caseSensitive: true,
  },
  {
    id: "bioacoustics",
    term: "bioacoustics",
    definition:
      "Studying animals and ecosystems through the sounds they make.",
    category,
  },
  {
    id: "birdclef",
    term: "BirdCLEF",
    definition:
      "A recurring challenge and dataset for identifying bird species from recorded audio.",
    category,
  },
  {
    id: "gis",
    term: "GIS",
    aliases: ["geographic information system"],
    definition:
      "Software and methods for storing, combining and displaying data that has a location on Earth.",
    category,
  },
  {
    id: "geospatial",
    term: "geospatial",
    definition:
      "Data or analysis that involves positions on Earth, such as coordinates, routes or regions.",
    category,
  },
  {
    id: "gtfs",
    term: "GTFS",
    aliases: ["General Transit Feed Specification"],
    definition:
      "A standard set of text files that describes public-transport stops, routes, trips and timetables.",
    category,
  },
  {
    id: "raptor",
    term: "RAPTOR",
    definition:
      "A fast algorithm for finding public-transport journeys by scanning routes in rounds of transfers.",
    category,
    caseSensitive: true,
  },
  {
    id: "gps",
    term: "GPS",
    aliases: ["Global Positioning System"],
    definition:
      "A satellite system that lets a device work out its position on Earth.",
    category,
  },
  {
    id: "postgis",
    term: "PostGIS",
    definition:
      "An add-on that gives the PostgreSQL database the ability to store and query geographic shapes.",
    category,
  },
  {
    id: "raster",
    term: "raster",
    definition:
      "Data stored as a grid of cells, such as a satellite image where each cell is a pixel.",
    category,
  },
  {
    id: "remote-sensing",
    term: "remote sensing",
    definition:
      "Measuring the Earth from satellites or aircraft instead of visiting the place in person.",
    category,
  },
  {
    id: "sentinel-2",
    term: "Sentinel-2",
    aliases: ["Sentinel"],
    definition:
      "A pair of European satellites that regularly photograph land and water in visible and infrared light.",
    category,
  },
  {
    id: "ndvi",
    term: "NDVI",
    aliases: ["normalized difference vegetation index"],
    definition:
      "A number calculated from red and near-infrared light that indicates how much healthy green vegetation is present.",
    category,
  },
  {
    id: "geofence",
    term: "geofence",
    definition:
      "A virtual boundary around a real place; software can notice when a device enters or leaves it.",
    category,
  },
  {
    id: "weather-forecast",
    term: "weather forecast",
    aliases: ["weather model"],
    definition:
      "A prediction of future temperature, rain and wind made by simulating the atmosphere.",
    category,
  },
  {
    id: "open-meteo",
    term: "Open-Meteo",
    definition:
      "A free weather API that provides forecasts and historical weather data.",
    category,
  },
  {
    id: "openaq",
    term: "OpenAQ",
    definition:
      "A public platform that collects and shares air-quality measurements from around the world.",
    category,
  },
  {
    id: "usgs",
    term: "USGS",
    aliases: ["United States Geological Survey"],
    definition:
      "A United States science agency that publishes open data about earthquakes, water, land and minerals.",
    category,
  },
  {
    id: "earthquake",
    term: "earthquake",
    definition:
      "A sudden release of energy in Earth's crust that sends seismic waves through the ground.",
    category,
  },
  {
    id: "sumo",
    term: "SUMO",
    aliases: ["Simulation of Urban MObility"],
    definition:
      "An open-source traffic simulator used to model vehicles, roads and congestion.",
    category,
    caseSensitive: true,
  },
];
