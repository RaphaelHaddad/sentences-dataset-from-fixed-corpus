from generator import OllamaGenerator

if __name__ == "__main__":
    kwargs = {
        "corpus_path": "text_files/top_5000_words_google.txt",  # replace with your actual corpus file path
        "output_path": "text_files/generated_sentences.txt",  # replace with your actual destination file path
        "num_words": 20,
        "sentences_per_batch": 3,
        "min_size_sentence": 5,
        "max_size_sentence": 10,
        "minimum_usage": 5,
    }
    generator = OllamaGenerator(**kwargs)
    generator.loop_generate(max_iterations=1e5)