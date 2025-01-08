import random
import json
with open('./Datasets/sinonimDict.json', 'r') as synFile:
    synonyms = json.load(synFile)
class TextAugment:
    def __init__(self, alpha=0.1, num_aug=4, random_state=None):
        self.alpha = alpha
        self.num_aug = num_aug
        self.random_state = random_state
        if random_state is not None:
            random.seed(random_state)
    def synonym_replacement(self, words, n, synonyms):
        new_words = words.copy()
        random_word_list = list(set([word for word in words if word in synonyms]))
        random.shuffle(random_word_list)
        num_replaced = 0
        for random_word in random_word_list:
            synonyms_for_word = synonyms[random_word]["sinonim"]
            if len(synonyms_for_word) >= 1:
                synonym = random.choice(synonyms_for_word)
                new_words = [synonym if word == random_word else word for word in new_words]
                num_replaced += 1
            if num_replaced >= n:
                break
        return new_words
    def random_swap(self, words, n):
        new_words = words.copy()
        for _ in range(n):
            new_words = self.swap_word(new_words)
        return new_words
    def swap_word(self, new_words):
        random_idx_1 = random.randint(0, len(new_words) - 1)
        random_idx_2 = random.randint(0, len(new_words) - 1)
        new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
        return new_words
    def random_deletion(self, words, p):
        if len(words) == 1:
            return words
        new_words = []
        for word in words:
            r = random.uniform(0, 1)
            if r > p:
                new_words.append(word)
        if len(new_words) == 0:
            rand_int = random.randint(0, len(words) - 1)
            return [words[rand_int]]
        return new_words
    def augment_text(self, text):
        words = text.split()
        augmented_texts = []
        num_words = len(words)
        n = max(1, int(self.alpha * num_words))  # Calculate number of words to change
        for _ in range(self.num_aug): #<-- Apply all augmentation techniques in each iteration
            aug_words = words.copy()
            aug_words = self.synonym_replacement(aug_words, n, synonyms)
            aug_words = self.random_swap(aug_words, n)
            aug_words = self.random_deletion(aug_words, self.alpha)
            augmented_text = ' '.join(aug_words)
            while augmented_text in augmented_texts: #<--Check for uniqueness
                #Re-augment if duplicate
                aug_words = words.copy()
                aug_words = self.synonym_replacement(aug_words, n, synonyms)
                aug_words = self.random_swap(aug_words, n)
                aug_words = self.random_deletion(aug_words, self.alpha)
                augmented_text = ' '.join(aug_words)
            augmented_texts.append(augmented_text)
        return augmented_texts