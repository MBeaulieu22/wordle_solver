class Trie:
    class TrieNode():
        def __init__(self, frequency=0):
            self.children = {}
            self.frequency = frequency

    def __init__(self, words):
        self.head_node = self.TrieNode()
        self.must_contain = set()
        self.char_frequency = {}
        self.insert_words(words)

    def insert_words(self, words):
        for word in words:
            for c in word:
                self.char_frequency[c] = 1 + self.char_frequency.get(c, 0)
            self.insert_word(word)

    def insert_word(self, word):
        current_node = self.head_node

        for c in word:
            if c not in current_node.children:
                current_node.children[c] = self.TrieNode(self.char_frequency[c])
            current_node = current_node.children[c]

    def get_possible_words(self):
        return self.get_possible_words_helper(self.head_node, "", 0, self.must_contain.copy())

    def get_possible_words_helper(self, node, prefix_string, frequency_score, must_contain):
        result = []

        if len(prefix_string) == 5:
            if not must_contain:
                return [(prefix_string, frequency_score)]
            else:
                return []

        for child in node.children.items():
            must_contain_copy = must_contain.copy()
            if child[0] in must_contain_copy:
                must_contain_copy.remove(child[0])

            if child[0] not in prefix_string:
                frequency_score = frequency_score + child[1].frequency

            result += self.get_possible_words_helper(child[1],
                                                     prefix_string + child[0],
                                                     frequency_score,
                                                     must_contain_copy)
            if child[0] not in prefix_string:
                frequency_score = frequency_score - child[1].frequency

        return result

    def prune(self, guess, guess_results):
        self.must_contain = set()
        for index in range(5):
            if guess_results[index] == "🟩":
                self.must_contain.add(guess[index])
                self.prune_green(index, guess[index], self.head_node)
            elif guess_results[index] == "🟨":
                self.must_contain.add(guess[index])
                self.prune_yellow(index, guess[index], self.head_node)
            else:
                if guess[index] not in self.must_contain:
                    self.prune_red(index, guess[index], self.head_node)
                # TODO: Prune double letter

    def prune_red(self, index, letter, node):
        if letter in node.children:
            del(node.children[letter])

        for c in node.children.items():
            self.prune_red(index, letter, c[1])

    def prune_green(self, index, letter, node):
        if index == 0:
            node.children = {letter: node.children[letter]} if letter in node.children else {}

        else:
            for c in node.children.items():
                self.prune_green(index-1, letter, c[1])

    def prune_yellow(self, index, letter, node):
        if index == 0:
            if letter in node.children:
                del (node.children[letter])
        else:
            for c in node.children.items():
                self.prune_yellow(index - 1, letter, c[1])

    def get_char_dict(self, word):
        char_dict = {}
        for c in word:
            char_dict[c] = 1 + char_dict.get(c, 0)
        return char_dict
