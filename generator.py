from utils import (
    load_corpus,
    update_usage,
    all_used_minimum,
    select_random_words,
    generate_sentences_with_ollama,
    post_process,
)


class OllamaGenerator:
    def __init__(self, **kwargs):
        self.corpus = load_corpus(kwargs["corpus_path"])
        self.usage = {word.lower(): 0 for word in self.corpus}
        self.output_path = kwargs["output_path"]
        self.kwargs = kwargs

    def generate(self):
        selected_words = select_random_words(
            self.corpus,
            self.usage,
            k=self.kwargs["num_words"],
        )
        try:
            generated_sentences = generate_sentences_with_ollama(
                selected_words,
                sentences_per_batch=self.kwargs["sentences_per_batch"],
                min_size_sentence=self.kwargs["min_size_sentence"],
                max_size_sentence=self.kwargs["max_size_sentence"],
            )
            processed_sentences = post_process(
                generated_sentences,
                sentences_per_batch=self.kwargs["sentences_per_batch"],
            )
            return processed_sentences
        except Exception as e:
                print(f"Error in ollama call: {e}")
                return [""]
    


    def loop_generate(self, max_iterations=10000):
        iteration = 0
        # Loop until every word in our corpus has been used at least 5 times.
        while not all_used_minimum(self.usage, self.kwargs["minimum_usage"]) and iteration < max_iterations:
            iteration += 1
            processed_sentences = self.generate()
            # Write iteration header and original sentences to output file.
            with open(self.output_path, 'a') as out:
                for sentence in processed_sentences:
                    out.write(sentence + "\n")
            # Update usage counts by checking which corpus words appear in the generated sentences.
            for sentence in processed_sentences:
                update_usage(self.usage, sentence, self.corpus)
            print(f"Iteration {iteration} complete.")
        
        print(f"Finished: All words have been used at least {self.kwargs['minimum_usage']} times.")