# Sentence Dataset Generator from Fixed Corpus


![Sentence Generation Example](images/keyboard.gif) **WHY ALL THE SENTENCES DATASET HAVE MILLIONS OF SAMPLES ???**

The tool operates as follows:

## Introduction

Surprisingly, there isn't a readily available tool to efficiently generate sentences from a large corpus of words. While Large Language Models (LLMs) are powerful, their limited context windows and difficulties in long-range inference make them unsuitable for this task. This project provides a simple tool to address this gap. It's designed to help you create datasets, such as those needed when collecting typing data for keyboard optimization or other similar applications where controlled sentence generation is required.

## How It Works



1.  **Corpus Loading:** Loads a text file containing a list of words (your corpus).
2.  **Usage Tracking:** Keeps track of how many times each word from the corpus has been used in generated sentences.
3.  **Word Selection:** Randomly selects a subset of words from the corpus, weighting the selection to favor less frequently used words.
4.  **Sentence Generation:** Uses the Ollama API to prompt a local LLM to generate sentences using the selected words.  The prompt specifies the number of sentences, and length constraints.
5.  **Post-processing:** Cleans and formats the generated sentences.
6.  **Iteration:** Repeats steps 3-5 until all words in the corpus have been used a minimum number of times.

## Requirements

*   Python 3.6+
*   Ollama ([https://ollama.com/](https://ollama.com/))
*   Sufficient RAM (8GB or more recommended) to run Ollama and the LLM model locally.

## Installation

1.  Install the `ollama` Python package:

    ```bash
    pip install ollama
    ```

    See the [official Ollama documentation](https://github.com/jmorganca/ollama) for detailed installation instructions and troubleshooting.

2.  Clone this repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

## Usage

1.  **Prepare your corpus:** Create a text file (e.g., `top_5000_words_google.txt`) with one word per line.
2.  **Configure the generator:** Modify the `kwargs` dictionary in `main.py` to suit your needs:

    *   `corpus_path`: Path to your corpus file.
    *   `output_path`: Path to the output file where generated sentences will be saved.
    *   `num_words`: Number of words to use in each sentence generation prompt.
    *   `sentences_per_batch`: Number of sentences to generate per prompt.
    *   `min_size_sentence`: Minimum number of words per sentence.
    *   `max_size_sentence`: Maximum number of words per sentence.
    *   `minimum_usage`: Minimum number of times each word should be used.
3.  **Run the generator:**

    ```bash
    python main.py
    ```

The generated sentences will be saved to the specified output file.

## Example

```python
from generator import OllamaGenerator

if __name__ == "__main__":
    kwargs = {
        "corpus_path": "text_files/top_5000_words_google.txt",
        "output_path": "text_files/generated_sentences.txt",
        "num_words": 20,
        "sentences_per_batch": 3,
        "min_size_sentence": 5,
        "max_size_sentence": 10,
        "minimum_usage": 5,
    }
    generator = OllamaGenerator(**kwargs)
    generator.loop_generate(max_iterations=1e5)
```

This example will generate sentences using words from `top_5000_words_google.txt`, saving the output to `generated_sentences.txt`. The generator will attempt to use each word at least 5 times.
