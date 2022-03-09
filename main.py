from nltk.corpus import words
import random

from GameState import GameState
from Trie import Trie


class WordleSolver:
    def __init__(self, answer=""):
        lower_words = [word.lower() for word in words.words()]
        self.possible_words = list(filter(lambda w: len(w) == 5, lower_words))
        self.trie = self.create_trie()
        answer = answer if answer else self.get_random_word()
        self.state = GameState(answer)

    def create_trie(self):
        trie = Trie()
        for word in self.possible_words:
            trie.insert_word(word)
        return trie

    def get_random_word(self):
        return random.choice(self.possible_words)

    def get_random_guess(self):
        return random.choice(self.trie.get_possible_words())

    def update_trie(self, guess, guess_result):
        self.trie.prune(guess, guess_result)

    def make_guess(self):
        if self.state.guess_number < 6:
            guess = self.get_random_guess()
            print(guess)
            self.state.make_guess(guess)
            print(self.state.guess_results[-1])
            self.update_trie(guess, self.state.guess_results[-1])

            if self.state.won:
                print("You won!")
            elif self.state.guess_number == self.state.MAX_GUESSES:
                print("You lost!  Word was: " + self.state.answer)


if __name__ == '__main__':
    solver = WordleSolver()

    for x in range(6):
        solver.make_guess()
