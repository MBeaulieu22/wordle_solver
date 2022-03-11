from nltk.corpus import words
import random

from GameState import GameState
from Trie import Trie


class WordleSolver:
    def __init__(self, answer="", debug_mode=False):
        lower_words = [word.lower() for word in words.words()]
        self.possible_words = list(filter(lambda w: len(w) == 5, lower_words))
        self.trie = Trie(self.possible_words)
        self.debug_mode = debug_mode
        answer = answer if answer else self.get_random_word()
        self.state = GameState(answer)

    def get_random_word(self):
        return random.choice(self.possible_words)

    def get_guess_word(self):
        possibilities = self.trie.get_possible_words()
        possibilities.sort(key=lambda p: p[1], reverse=True)
        return random.choice(possibilities[0:10])[0]

    def update_trie(self, guess, guess_result):
        self.trie.prune(guess, guess_result)

    def make_guess(self):
        guess = self.get_guess_word()
        if self.debug_mode:
            print(guess)
        self.state.make_guess(guess)

        if self.debug_mode:
            print(self.state.guess_results[-1])

        self.update_trie(guess, self.state.guess_results[-1])


def play_game():
    solver = WordleSolver()

    while not solver.state.game_over():
        solver.make_guess()
    print("Won: {}, Answer: {}, Guesses: {}".format(solver.state.won,
                                                    solver.state.answer,
                                                    len(solver.state.guess_results)))
    return solver.state


if __name__ == '__main__':
    win_count, guess_count = 0, 0
    game_count = 1000
    for test in range(game_count):
        state = play_game()
        if state.won:
            guess_count += len(state.guess_results)
            win_count += 1

    print("Won {} / {} Games! Average guess of {} on wins"
          .format(win_count,
                  game_count,
                  float(guess_count) / win_count))


