import random

class FlashcardManager:
    def __init__(self):
        self.flashcards = []
        self.current_card = None
        self.score = 0
        self.total_attempts = 0

    def add_card(self, question, answer):
        self.flashcards.append({"question": question, "answer": answer})
        return len(self.flashcards) == 1

    def get_next_card(self):
        if self.flashcards:
            self.current_card = random.choice(self.flashcards)
            return self.current_card
        return None

    def check_answer(self, user_answer):
        if self.current_card and user_answer:
            self.total_attempts += 1
            is_correct = user_answer.lower() == self.current_card["answer"].lower()
            if is_correct:
                self.score += 1
            return is_correct
        return None

    def update_card(self, new_question, new_answer):
        if self.current_card:
            self.current_card["question"] = new_question
            self.current_card["answer"] = new_answer
            return True
        return False

    def delete_current_card(self):
        if self.current_card:
            self.flashcards.remove(self.current_card)
            return True
        return False