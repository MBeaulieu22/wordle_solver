class Trie:
    class TrieNode:
        def __init__(self):
            self.children = {}

    def __init__(self):
        self.head_node = self.TrieNode()
        self.must_contain = set()

    def insert_word(self, word):
        current_node = self.head_node

        for c in word:
            if c not in current_node.children:
                current_node.children[c] = self.TrieNode()
            current_node = current_node.children[c]

    def get_possible_words(self):
        possible_words = self.get_possible_words_helper(self.head_node, "", self.must_contain.copy())
        if not possible_words:
            print(self.must_contain)
        return possible_words

    def get_possible_words_helper(self, node, prefix_string, must_contain):
        result = []

        if len(prefix_string) == 5:
            if not must_contain:
                return [prefix_string]
            else:
                return []

        for child in node.children.items():
            if child[0] in must_contain:
                must_contain.remove(child[0])

            result += self.get_possible_words_helper(child[1], prefix_string + child[0], must_contain.copy())
        return result

    def prune(self, guess, guess_results):
        for index in range(5):
            if guess_results[index] == "🟩":
                self.prune_green(index, guess[index], self.head_node)
            elif guess_results[index] == "🟨":
                self.must_contain.add(guess[index])
                self.prune_yellow(index, guess[index], self.head_node)
            else:
                if self.get_char_dict(guess)[guess[index]] < 2:
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
