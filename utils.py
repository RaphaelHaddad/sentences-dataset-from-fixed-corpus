import random
import re
from ollama import chat, ChatResponse  # ensure the ollama package is installed


def tokenize(text: str):
    # Simple tokenization: extract alphanumeric words and lowercase them.
    return re.findall(r"\b\w+\b", text.lower())

def load_corpus(file_path: str):
    with open(file_path, 'r') as f:
        words = [line.strip() for line in f if line.strip()]
    return words

def update_usage(usage: dict, generated_text: str, corpus: list):
    tokens = tokenize(generated_text)
    # Update usage for each word in corpus if it is found in the generated text.
    for word in corpus:
        lw = word.lower()
        usage[lw] += tokens.count(lw)

def all_used_minimum(usage: dict, min_count: int = 5) -> bool:
    return all(count >= min_count for count in usage.values())

def select_random_words(corpus: list, usage: dict, k: int = 20):
    # Weight each word inversely to its usage count: lower count => higher chance.
    weights = [1 / (usage[word.lower()] + 1) for word in corpus]
    # random.choices might pick duplicates so ensure uniqueness.
    selected = random.choices(corpus, weights=weights, k=k)
    selected = list(set(selected))
    while len(selected) < k:
        extra = random.choice(corpus)
        if extra not in selected:
            selected.append(extra)
    return selected

def generate_sentences_with_ollama(selected_words: list, sentences_per_batch : int = 3, 
                                   min_size_sentence : int = 5, max_size_sentence : int = 10) -> str:
    # Construct a prompt that tells the model to generate sentences_per_batch sentences 
    # (one per line) using the selected words. Also allow use of small words.
    prompt = (f"Please generate {sentences_per_batch} sentences using the following words, "
              "each on a new line:\n" + ", ".join(selected_words) +
              "\nYou are allowed to add common small words like 'the', 'my', 'his', etc. "
              "Only output the sentences, one per line. "
              f"Each sentence must be between {min_size_sentence} and {max_size_sentence} words long. "
              f"Please only return the {sentences_per_batch} sentences, one per line.")
    
    response: ChatResponse = chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
    return response.message.content.strip()

def post_process(text: str, sentences_per_batch : int = 3) -> str:
    """
    Given a generated response text that may include header lines (e.g., iteration info)
    and sentences, extract the last three sentences (assumed one per line),
    then for each sentence:
      - Replace spaces with underscores,
      - Remove characters except for letters, underscores and dots,
      - Ensure the sentence ends with a dot.
    Finally, concatenate the sentences.
    """
    # Split text into lines and remove empty ones.
    sentences = [line.strip() for line in text.split('\n') if line.strip()]
    processed_sentences = []
    for sentence in sentences:
        # Remove all characters except letters, underscores, spaces, and dot.
        sentence = re.sub(r'[^a-zA-Z_. ]', '', sentence)
        # Ensure it ends with a dot.
        if not sentence.endswith('.'):
            sentence += '.'
        processed_sentences.append(sentence)
    # Concatenate all sentences into one string.
    return processed_sentences