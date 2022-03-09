class GameState:
    MAX_GUESSES = 6

    def __init__(self, answer):
        self.guess_number = 0
        self.words_guessed = []
        self.answer = answer
        self.guess_results = []
        self.won = False

    def get_answer_char_dict(self):
        char_dict = {}
        for c in self.answer:
            char_dict[c] = 1 + char_dict.get(c, 0)
        return char_dict

    def make_guess(self, guess):
        self.guess_number += 1
        self.words_guessed.append(guess)

        if guess == self.answer:
            self.won = True

        self.guess_results.append(self.get_guess_result(guess))

    def get_guess_result(self, guess):
        guess_result = ""
        tmp_dict = self.get_answer_char_dict()
        for index in range(5):
            if self.answer[index] == guess[index]:
                guess_result += "🟩"
                tmp_dict[guess[index]] -= 1
            elif tmp_dict.get(guess[index], 0) > 0:
                guess_result += "🟨"
                tmp_dict[guess[index]] -= 1
            else:
                guess_result += "🟥"
        return guess_result
