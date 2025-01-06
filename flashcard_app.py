import tkinter as tk
from tkinter import messagebox, simpledialog
from colors import Colors
from ui_components import create_button, create_label
from flashcard_manager import FlashcardManager

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Quiz App")
        self.root.geometry("700x600")
        self.root.configure(bg=Colors.BACKGROUND)

        self.manager = FlashcardManager()
        self.setup_ui()

    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg=Colors.BACKGROUND)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_container, bg=Colors.BACKGROUND)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        create_label(header_frame, "Flashcard Quiz", 28, bold=True).pack(side=tk.LEFT)
        
        self.score_label = create_label(header_frame, "Score: 0 / 0", 14)
        self.score_label.pack(side=tk.RIGHT, pady=10)

        # Card Frame
        self.card_frame = tk.Frame(
            main_container,
            bg=Colors.CARD_BG,
            relief=tk.RAISED,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#E0E0E0"
        )
        self.card_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        self.question_label = tk.Label(
            self.card_frame,
            text="Add a flashcard to start",
            font=("Helvetica", 18),
            bg=Colors.CARD_BG,
            fg=Colors.TEXT,
            wraplength=600,
            justify="center"
        )
        self.question_label.pack(expand=True, pady=40)

        # Answer Section
        answer_section = tk.Frame(main_container, bg=Colors.BACKGROUND)
        answer_section.pack(fill=tk.X, pady=10)

        answer_label = create_label(answer_section, "Type your answer here:", 14)
        answer_label.pack(anchor="w", padx=5, pady=(0, 5))

        self.answer_entry = tk.Entry(
            answer_section,
            font=("Helvetica", 16),
            justify="center",
            relief=tk.FLAT,
            bg=Colors.CARD_BG,
            fg=Colors.TEXT
        )
        self.answer_entry.pack(fill=tk.X, ipady=10)

        # Buttons
        buttons_frame = tk.Frame(main_container, bg=Colors.BACKGROUND)
        buttons_frame.pack(fill=tk.X, pady=20)

        # Primary Actions
        primary_buttons = tk.Frame(buttons_frame, bg=Colors.BACKGROUND)
        primary_buttons.pack(fill=tk.X, pady=(0, 10))

        self.check_button = create_button(
            primary_buttons, "Check Answer", self.check_answer,
            Colors.SECONDARY, state=tk.DISABLED
        )
        self.check_button.pack(side=tk.LEFT, expand=True, padx=5)

        self.add_card_button = create_button(
            primary_buttons, "Add Flashcard", self.open_add_card_window,
            Colors.SUCCESS
        )
        self.add_card_button.pack(side=tk.LEFT, expand=True, padx=5)

        # Secondary Actions
        secondary_buttons = tk.Frame(buttons_frame, bg=Colors.BACKGROUND)
        secondary_buttons.pack(fill=tk.X)

        self.edit_card_button = create_button(
            secondary_buttons, "Edit Card", self.edit_flashcard,
            Colors.WARNING, state=tk.DISABLED
        )
        self.edit_card_button.pack(side=tk.LEFT, expand=True, padx=5)

        self.delete_card_button = create_button(
            secondary_buttons, "Delete Card", self.delete_flashcard,
            Colors.DANGER, state=tk.DISABLED
        )
        self.delete_card_button.pack(side=tk.LEFT, expand=True, padx=5)

    def open_add_card_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Flashcard")
        add_window.geometry("500x350")
        add_window.configure(bg=Colors.BACKGROUND)
        add_window.transient(self.root)
        add_window.grab_set()

        create_label(add_window, "Create New Flashcard", 20, bold=True).pack(pady=20)

        # Question Frame
        question_frame = tk.Frame(add_window, bg=Colors.BACKGROUND)
        question_frame.pack(fill=tk.X, padx=20, pady=10)

        create_label(question_frame, "Question:", 12).pack(anchor="w")

        question_entry = tk.Entry(
            question_frame,
            font=("Helvetica", 14),
            relief=tk.FLAT,
            bg=Colors.CARD_BG,
            fg=Colors.TEXT
        )
        question_entry.pack(fill=tk.X, ipady=8, pady=5)

        # Answer Frame
        answer_frame = tk.Frame(add_window, bg=Colors.BACKGROUND)
        answer_frame.pack(fill=tk.X, padx=20, pady=10)

        create_label(answer_frame, "Answer:", 12).pack(anchor="w")

        answer_entry = tk.Entry(
            answer_frame,
            font=("Helvetica", 14),
            relief=tk.FLAT,
            bg=Colors.CARD_BG,
            fg=Colors.TEXT
        )
        answer_entry.pack(fill=tk.X, ipady=8, pady=5)

        def save_card():
            question = question_entry.get().strip()
            answer = answer_entry.get().strip()

            if question and answer:
                if self.manager.add_card(question, answer):
                    self.load_next_card()
                    self.check_button.config(state=tk.NORMAL)
                    self.edit_card_button.config(state=tk.NORMAL)
                    self.delete_card_button.config(state=tk.NORMAL)
                messagebox.showinfo("Success", "Flashcard added successfully!")
                add_window.destroy()
            else:
                messagebox.showwarning("Error", "Both question and answer are required.")

        create_button(
            add_window,
            "Save Flashcard",
            save_card,
            Colors.SUCCESS
        ).pack(pady=30)

    def load_next_card(self):
        card = self.manager.get_next_card()
        if card:
            self.question_label.config(text=card["question"])
            self.animate_card()
            self.answer_entry.delete(0, tk.END)
        else:
            self.question_label.config(text="Add a flashcard to start")
            self.check_button.config(state=tk.DISABLED)
            self.edit_card_button.config(state=tk.DISABLED)
            self.delete_card_button.config(state=tk.DISABLED)

    def animate_card(self):
        def flash(count=0):
            if count < 3:
                self.card_frame.configure(bg="#F3F4F6")
                self.root.after(100, lambda: self.card_frame.configure(bg=Colors.CARD_BG))
                self.root.after(200, lambda: flash(count + 1))
        flash()

    def check_answer(self):
        user_answer = self.answer_entry.get().strip()
        if not user_answer:
            messagebox.showwarning("Error", "Please enter an answer.")
            return

        result = self.manager.check_answer(user_answer)
        if result:
            messagebox.showinfo("Correct! 🎉", "Great job! That's the right answer!")
        else:
            messagebox.showinfo("Incorrect ❌", 
                              f"The correct answer was:\n{self.manager.current_card['answer']}")
        
        self.update_score_label()
        self.load_next_card()

    def update_score_label(self):
        self.score_label.config(
            text=f"Score: {self.manager.score} / {self.manager.total_attempts}"
        )

    def edit_flashcard(self):
        if self.manager.current_card:
            new_question = simpledialog.askstring(
                "Edit Question",
                "Enter new question:",
                initialvalue=self.manager.current_card["question"]
            )
            new_answer = simpledialog.askstring(
                "Edit Answer",
                "Enter new answer:",
                initialvalue=self.manager.current_card["answer"]
            )

            if new_question and new_answer:
                self.manager.update_card(new_question, new_answer)
                messagebox.showinfo("Success", "Flashcard updated successfully!")
                self.load_next_card()

    def delete_flashcard(self):
        if self.manager.current_card:
            if messagebox.askyesno("Confirm Delete", 
                                 "Are you sure you want to delete this flashcard?"):
                self.manager.delete_current_card()
                messagebox.showinfo("Deleted", "Flashcard deleted successfully!")
                self.load_next_card()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()