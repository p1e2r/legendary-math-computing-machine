import random
from datetime import datetime

# Simple math quiz with difficulty levels and a TUI using rich

try:
    from rich.console import Console
    from rich.prompt import Prompt
    from rich.table import Table
    from rich.panel import Panel
except ImportError:
    # Fallback simple console for environments without rich
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
    class Prompt:
        @staticmethod
        def ask(prompt_text, choices=None, default=None):
            return input(prompt_text + ' ')

console = Console()


def generate_problem(difficulty):
    """Return a (question, answer) tuple based on difficulty.

    easy   : single‑digit addition or subtraction
    medium : two‑digit addition, subtraction or multiplication
    hard   : random operations with 1‑3 operands
    """
    ops = {"easy": [("+", lambda a,b: a+b), ("-", lambda a,b: a-b)],
           "medium": [("+", lambda a,b: a+b), ("-", lambda a,b: a-b), ("*", lambda a,b: a*b)],
           "hard": [("+", lambda a,b: a+b), ("-", lambda a,b: a-b), ("*", lambda a,b: a*b), ("/", lambda a,b: a//b if b else None)]}

    if difficulty == "easy":
        a, b = random.randint(0,9), random.randint(0,9)
        op, fn = random.choice(ops["easy"])
        return f"{a} {op} {b}", fn(a,b)
    if difficulty == "medium":
        a, b = random.randint(10,99), random.randint(10,99)
        op, fn = random.choice(ops["medium"])
        return f"{a} {op} {b}", fn(a,b)
    # hard
    # 1‑3 operands
    num_ops = random.randint(2,3)
    nums = [random.randint(1,20) for _ in range(num_ops)]
    ops_list = [random.choice(ops["hard"]) for _ in range(num_ops-1)]
    # build expression string
    expr_parts = []
    current = nums[0]
    for idx, (op, fn) in enumerate(ops_list):
        expr_parts.append(str(current))
        expr_parts.append(op)
        current = fn(current, nums[idx+1])
    expr_parts.append(str(current))
    return " ".join(expr_parts), current


def run_quiz(num_questions=10):
    console.print(Panel("Math Quiz", style="bold magenta"))
    difficulty = Prompt.ask("Select difficulty", choices=["easy", "medium", "hard"], default="easy")
    score = 0
    for q in range(1, num_questions+1):
        question, answer = generate_problem(difficulty)
        console.print(f"\nQuestion {q}/{num_questions}: {question} = ")
        try:
            user_ans = int(Prompt.ask("Your answer"))
        except ValueError:
            console.print("[red]Invalid input! Skipping question.")
            continue
        if user_ans == answer:
            console.print("[green]Correct! [+1]", style="bold")
            score += 1
        else:
            console.print(f"[red]Wrong! The answer was {answer}.[/red] [-1]", style="bold")
            score -= 1
        console.print(f"Current score: {score}\n")
    console.print(Panel(f"Final score: {score}", style="bold green"))


if __name__ == "__main__":
    run_quiz()
