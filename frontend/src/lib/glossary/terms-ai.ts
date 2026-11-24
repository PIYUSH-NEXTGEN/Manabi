import type { GlossaryEntry } from "./types";

const category = "AI & data" as const;

export const AI_TERMS: GlossaryEntry[] = [
  {
    id: "ai",
    term: "AI",
    aliases: ["artificial intelligence"],
    definition:
      "Software that learns patterns from examples instead of following only rules a person wrote by hand.",
    category,
  },
  {
    id: "machine-learning",
    term: "machine learning",
    aliases: ["ML"],
    definition:
      "A way of building software where a program improves at a task by studying many examples.",
    category,
  },
  {
    id: "model",
    term: "model",
    definition:
      "A simplified representation of something used to reason about it; in machine learning, the trained part that makes predictions.",
    category,
  },
  {
    id: "dataset",
    term: "dataset",
    definition:
      "A collection of examples, usually with answers attached, used to train or test a model.",
    category,
  },
  {
    id: "label",
    term: "label",
    definition:
      "The correct answer attached to one example, such as \"has disease\" or \"does not have disease\".",
    category,
  },
  {
    id: "training",
    term: "training",
    definition:
      "The process of showing a model many examples so it can adjust itself and make better guesses.",
    category,
  },
  {
    id: "inference",
    term: "inference",
    definition:
      "Using a model that has already been trained to make a prediction on new input.",
    category,
  },
  {
    id: "feature",
    term: "feature",
    aliases: ["features"],
    definition:
      "A noticeable part of a product; in machine learning, one measurable clue given to a model, such as a price or a pixel value.",
    category,
  },
  {
    id: "feature-engineering",
    term: "feature engineering",
    definition:
      "Turning raw data into useful clues, such as turning a date into day-of-week and holiday flags.",
    category,
  },
  {
    id: "classification",
    term: "classification",
    definition:
      "A task where the model picks one or more categories, such as spam or not spam.",
    category,
  },
  {
    id: "regression",
    term: "regression",
    definition:
      "A task where the model predicts a number, such as a price, a temperature or a waiting time.",
    category,
  },
  {
    id: "clustering",
    term: "clustering",
    definition:
      "Grouping examples that look alike without being told in advance what the groups mean.",
    category,
  },
  {
    id: "supervised-learning",
    term: "supervised learning",
    definition:
      "Training with examples that already have correct answers attached.",
    category,
  },
  {
    id: "unsupervised-learning",
    term: "unsupervised learning",
    definition:
      "Finding structure in data that has no correct answers attached.",
    category,
  },
  {
    id: "reinforcement-learning",
    term: "reinforcement learning",
    aliases: ["RL"],
    definition:
      "Training an agent by letting it try actions and rewarding the ones that lead to a good result.",
    category,
  },
  {
    id: "reward",
    term: "reward",
    definition:
      "Something of value given for an action; in reinforcement learning, a score that tells an agent how good a move was.",
    category,
  },
  {
    id: "neural-network",
    term: "neural network",
    definition:
      "A model made of layers of simple number operations that learn to spot patterns together.",
    category,
  },
  {
    id: "deep-learning",
    term: "deep learning",
    definition:
      "Machine learning with neural networks that have many layers, which lets them learn complex patterns.",
    category,
  },
  {
    id: "weight",
    term: "weight",
    definition:
      "A number inside a model that training adjusts; together, the weights store what the model learned.",
    category,
  },
  {
    id: "bias",
    term: "bias",
    definition:
      "A systematic skew in data or a model that makes some groups or cases consistently wrong.",
    category,
  },
  {
    id: "activation",
    term: "activation function",
    aliases: ["activation"],
    definition:
      "A small rule inside a neural network that decides how strongly a signal passes on.",
    category,
  },
  {
    id: "relu",
    term: "ReLU",
    aliases: ["rectified linear unit"],
    definition:
      "A common activation rule that passes positive numbers through and turns negatives into zero.",
    category,
  },
  {
    id: "backpropagation",
    term: "backpropagation",
    definition:
      "The method neural networks use to work out how much each weight contributed to an error, so it can be corrected.",
    category,
  },
  {
    id: "gradient",
    term: "gradient",
    definition:
      "The direction and size of change that would make a model's error go up or down.",
    category,
  },
  {
    id: "gradient-descent",
    term: "gradient descent",
    aliases: ["SGD", "stochastic gradient descent"],
    definition:
      "Training by repeatedly nudging the model's weights a small step against the gradient to reduce error.",
    category,
  },
  {
    id: "loss-function",
    term: "loss function",
    aliases: ["loss"],
    definition:
      "A formula that turns a model's mistakes into one number that training tries to make smaller.",
    category,
  },
  {
    id: "optimizer",
    term: "optimizer",
    definition:
      "The rule that decides exactly how far and in what way to move the weights after each training step.",
    category,
  },
  {
    id: "epoch",
    term: "epoch",
    definition:
      "One full pass through the training examples during training.",
    category,
  },
  {
    id: "batch",
    term: "batch",
    definition:
      "A group of items handled together; in training, a small group of examples processed before one weight update.",
    category,
  },
  {
    id: "overfitting",
    term: "overfitting",
    definition:
      "When a model memorises the training examples but does badly on new ones.",
    category,
  },
  {
    id: "underfitting",
    term: "underfitting",
    definition:
      "When a model is too simple or poorly trained to learn the pattern, so it does badly everywhere.",
    category,
  },
  {
    id: "regularization",
    term: "regularization",
    definition:
      "A penalty that discourages a model from becoming too complicated, which helps it generalise.",
    category,
  },
  {
    id: "hyperparameter",
    term: "hyperparameter",
    definition:
      "A setting chosen by the person, such as learning rate or tree depth, rather than learned by the model.",
    category,
  },
  {
    id: "cross-validation",
    term: "cross-validation",
    definition:
      "Testing a model several times on different held-out parts of the data to get a fairer score.",
    category,
  },
  {
    id: "train-test-split",
    term: "train/test split",
    aliases: ["train and test split", "train-test"],
    definition:
      "Keeping some examples out of training so they can be used later to check how well the model really works.",
    category,
  },
  {
    id: "data-leakage",
    term: "data leakage",
    aliases: ["target leakage"],
    definition:
      "When training accidentally sees information that would not be available at prediction time, making results look better than they are.",
    category,
  },
  {
    id: "baseline",
    term: "baseline",
    definition:
      "A simple, honest first result, such as always guessing the most common answer, used to judge whether a smarter model is worth it.",
    category,
  },
  {
    id: "accuracy",
    term: "accuracy",
    definition:
      "The share of all predictions that were correct. It can be misleading when one answer is much more common than the others.",
    category,
  },
  {
    id: "precision",
    term: "precision",
    definition:
      "Of the cases a model flagged, the share that were actually correct. High precision means few false alarms.",
    category,
  },
  {
    id: "recall",
    term: "recall",
    definition:
      "Of the real cases that existed, the share the model found. High recall means few missed cases.",
    category,
  },
  {
    id: "f1",
    term: "F1 score",
    aliases: ["F1"],
    definition:
      "A single score that balances precision and recall, useful when both false alarms and missed cases matter.",
    category,
  },
  {
    id: "confusion-matrix",
    term: "confusion matrix",
    definition:
      "A small table showing how often each real answer was predicted as each possible answer.",
    category,
  },
  {
    id: "roc-auc",
    term: "ROC AUC",
    aliases: ["AUROC", "ROC curve", "AUC"],
    definition:
      "A score for ranking: it measures how often the model gives a truly positive case a higher score than a negative one.",
    category,
  },
  {
    id: "precision-at-k",
    term: "precision@k",
    aliases: ["precision at k"],
    definition:
      "Of the top k results a system returned, the share that were relevant.",
    category,
  },
  {
    id: "calibration",
    term: "calibration",
    definition:
      "Adjusting a system so its outputs match reality, such as making stated confidence or sensor readings accurate.",
    category,
  },
  {
    id: "confidence",
    term: "confidence",
    definition:
      "How strongly a model believes one answer, usually shown as a number from 0 to 1.",
    category,
  },
  {
    id: "uncertainty",
    term: "uncertainty",
    definition:
      "How unsure a measurement or prediction is, and how much it could reasonably be off.",
    category,
  },
  {
    id: "distribution-shift",
    term: "distribution shift",
    definition:
      "When new data looks different from the data a model was trained on, so its accuracy drops.",
    category,
  },
  {
    id: "class-imbalance",
    term: "class imbalance",
    definition:
      "When one answer is far more common than another, which can teach a model to ignore the rare one.",
    category,
  },
  {
    id: "cnn",
    term: "CNN",
    aliases: ["convolutional neural network"],
    definition:
      "A neural network that slides small filters across an image to learn edges, shapes and objects.",
    category,
  },
  {
    id: "transformer",
    term: "transformer",
    definition:
      "A neural-network design that uses attention to weigh which parts of the input matter to each other.",
    category,
  },
  {
    id: "attention",
    term: "attention",
    definition:
      "A model's way of deciding which words or pieces of the input are most relevant to the current step.",
    category,
  },
  {
    id: "embedding",
    term: "embedding",
    definition:
      "A list of numbers that represents a word, image or record so similar things end up close together.",
    category,
  },
  {
    id: "tokenization",
    term: "tokenization",
    definition:
      "Splitting text into small pieces called tokens, such as words or word parts, before a model reads it.",
    category,
  },
  {
    id: "llm",
    term: "LLM",
    aliases: ["large language model"],
    definition:
      "A large text model trained to predict the next token, which lets it answer questions and write text.",
    category,
  },
  {
    id: "gpt",
    term: "GPT",
    definition:
      "A family of large language models made by OpenAI; the name is also used loosely for text-generation models.",
    category,
  },
  {
    id: "prompt",
    term: "prompt",
    definition:
      "The instructions or example text given to a language model for one request.",
    category,
  },
  {
    id: "fine-tuning",
    term: "fine-tuning",
    definition:
      "Continuing to train an existing model on your own smaller dataset so it fits your specific task.",
    category,
  },
  {
    id: "transfer-learning",
    term: "transfer learning",
    definition:
      "Starting from a model already trained on a big general dataset, then adapting it to a new but related task.",
    category,
  },
  {
    id: "rag",
    term: "RAG",
    aliases: ["retrieval-augmented generation"],
    definition:
      "Letting a language model look up relevant documents first, then answer using those passages instead of memory alone.",
    category,
    caseSensitive: true,
  },
  {
    id: "retrieval",
    term: "retrieval",
    definition:
      "Finding the most relevant stored passages or records for a question, usually by comparing embeddings.",
    category,
  },
  {
    id: "gan",
    term: "GAN",
    aliases: ["generative adversarial network"],
    definition:
      "Two neural networks competing: one makes fake examples and the other tries to spot them, which pushes both to improve.",
    category,
  },
  {
    id: "gnn",
    term: "GNN",
    aliases: ["graph neural network"],
    definition:
      "A neural network that works on nodes and links, passing messages along the graph's edges.",
    category,
  },
  {
    id: "gradient-boosting",
    term: "gradient boosting",
    aliases: ["XGBoost"],
    definition:
      "A group of small decision trees where each new tree focuses on fixing the mistakes of the trees before it.",
    category,
  },
  {
    id: "decision-tree",
    term: "decision tree",
    aliases: ["CART"],
    definition:
      "A model that makes a series of yes/no splits on features to reach an answer.",
    category,
  },
  {
    id: "ensemble",
    term: "ensemble",
    definition:
      "Combining several models' predictions, often by voting or averaging, to get a steadier result.",
    category,
  },
  {
    id: "tf-idf",
    term: "TF-IDF",
    definition:
      "A way to score words by how often they appear in one document compared with how common they are overall.",
    category,
  },
  {
    id: "nlp",
    term: "NLP",
    aliases: ["natural language processing"],
    definition:
      "The field of getting computers to work with human language, such as text classification or search.",
    category,
  },
  {
    id: "ocr",
    term: "OCR",
    aliases: ["optical character recognition"],
    definition:
      "Turning an image of text, such as a photo or scan, into text a computer can read.",
    category,
  },
  {
    id: "computer-vision",
    term: "computer vision",
    definition:
      "The field of getting computers to understand images and video, such as finding objects or measuring motion.",
    category,
  },
  {
    id: "optical-flow",
    term: "optical flow",
    definition:
      "Estimating how each part of an image moved between two frames by tracking brightness patterns.",
    category,
  },
  {
    id: "spectrogram",
    term: "spectrogram",
    definition:
      "A picture of sound that shows which frequencies are present over time; it lets models read audio like an image.",
    category,
  },
  {
    id: "multimodal",
    term: "multimodal",
    definition:
      "Using more than one kind of input, such as text, images and audio, in the same model or product.",
    category,
  },
  {
    id: "multi-label",
    term: "multi-label",
    definition:
      "A classification task where one example can have several correct labels at once, not just one.",
    category,
  },
  {
    id: "soft-label",
    term: "soft label",
    definition:
      "An answer given as a probability or score instead of a hard yes/no, which keeps useful uncertainty.",
    category,
  },
  {
    id: "explainability",
    term: "explainability",
    aliases: ["interpretability"],
    definition:
      "Being able to say, in human terms, why a model produced a particular result.",
    category,
  },
  {
    id: "shap",
    term: "SHAP",
    definition:
      "A method that explains a prediction by estimating how much each input feature pushed the result up or down.",
    category,
  },
  {
    id: "grad-cam",
    term: "Grad-CAM",
    definition:
      "A method that highlights the parts of an image a vision model paid most attention to.",
    category,
  },
  {
    id: "human-in-the-loop",
    term: "human-in-the-loop",
    definition:
      "A design where a person reviews, corrects or approves the model's suggestions before they take effect.",
    category,
  },
  {
    id: "evaluation",
    term: "evaluation",
    definition:
      "Measuring how well a system works on cases it was not trained on, using clear and fair tests.",
    category,
  },
  {
    id: "benchmark",
    term: "benchmark",
    definition:
      "A standard test or comparison used to check whether one system is actually better than another.",
    category,
  },
  {
    id: "synthetic-data",
    term: "synthetic data",
    definition:
      "Artificial examples generated to look like real data, useful when real examples are scarce or private.",
    category,
  },
  {
    id: "anomaly-detection",
    term: "anomaly detection",
    definition:
      "Spotting examples that are unusual compared with the normal pattern, such as fraud or a broken sensor.",
    category,
  },
  {
    id: "recommender-system",
    term: "recommender system",
    definition:
      "Software that suggests items a person may like, based on their past choices and on patterns from other people.",
    category,
  },
  {
    id: "cold-start",
    term: "cold-start problem",
    definition:
      "The difficulty of making good suggestions for a new user or item that has no history yet.",
    category,
  },
  {
    id: "record-matching",
    term: "record matching",
    aliases: ["entity resolution", "record linkage"],
    definition:
      "Deciding when two records from different sources describe the same real thing, such as the same person or place.",
    category,
  },
  {
    id: "tanimoto",
    term: "Tanimoto similarity",
    aliases: ["Tanimoto"],
    definition:
      "A number from 0 to 1 that says how much two sets, often molecular fingerprints, overlap.",
    category,
  },
  {
    id: "metric",
    term: "metric",
    definition:
      "A number used to judge performance, such as error, accuracy, latency or cost.",
    category,
  },
  {
    id: "mae",
    term: "MAE",
    aliases: ["mean absolute error"],
    definition:
      "The average size of a prediction error, ignoring whether it was too high or too low.",
    category,
  },
  {
    id: "rmse",
    term: "RMSE",
    aliases: ["root mean squared error"],
    definition:
      "A prediction-error score that punishes large misses more strongly than small ones.",
    category,
  },
  {
    id: "smape",
    term: "SMAPE",
    aliases: ["symmetric mean absolute percentage error"],
    definition:
      "A percentage-based error score that is easier to compare across series with very different sizes.",
    category,
  },
  {
    id: "psnr",
    term: "PSNR",
    aliases: ["peak signal-to-noise ratio"],
    definition:
      "A score for how close a reconstructed image is to the original, based on the size of the errors.",
    category,
  },
  {
    id: "ssim",
    term: "SSIM",
    aliases: ["structural similarity"],
    definition:
      "A score that compares the structure and contrast of two images, which often matches human judgement better than raw error.",
    category,
  },
  {
    id: "kl-divergence",
    term: "KL divergence",
    definition:
      "A measure of how much one probability distribution differs from another.",
    category,
  },
  {
    id: "mdp",
    term: "MDP",
    aliases: ["Markov decision process"],
    definition:
      "A formal model of a decision problem with states, actions, rewards and uncertain outcomes.",
    category,
  },
  {
    id: "mcts",
    term: "MCTS",
    aliases: ["Monte Carlo tree search"],
    definition:
      "A search method that tries many random playouts and focuses on the moves that looked most promising.",
    category,
  },
  {
    id: "minimax",
    term: "minimax",
    definition:
      "A strategy that picks the move with the best worst-case outcome, assuming the opponent plays well.",
    category,
  },
  {
    id: "q-learning",
    term: "Q-learning",
    definition:
      "A reinforcement-learning method that learns a score for each action in each state by trial and error.",
    category,
  },
  {
    id: "policy",
    term: "policy",
    definition:
      "A rule or plan for how to act; in reinforcement learning, the agent's strategy for choosing actions.",
    category,
  },
  {
    id: "exploration-exploitation",
    term: "exploration versus exploitation",
    aliases: ["exploration-exploitation", "exploration vs exploitation"],
    definition:
      "The trade-off between trying new actions to learn more and repeating the action that already works well.",
    category,
  },
];
