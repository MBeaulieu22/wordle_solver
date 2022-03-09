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
        guess = self.get_random_guess()
        self.state.make_guess(guess)
        self.update_trie(guess, self.state.guess_results[-1])


def play_game():
    solver = WordleSolver()

    while not solver.state.game_over():
        solver.make_guess()
    return solver.state


if __name__ == '__main__':
    win_count = 0
    for test in range(1000):
        state = play_game()
        if state.won:
            win_count += 1
        else:
            print("{} Lost on: {}".format(test, state.answer))

    print("Won {} / 1000 Games!").format(win_count)


