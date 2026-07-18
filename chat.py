"""Run this to talk to Axiom:  python chat.py"""
from axiom.agent import Axiom


def main():
    bot = Axiom()
    print("Axiom is awake. Type 'quit' to exit.\n")
    while True:
        try:
            user = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAxiom> Bye!")
            break
        if user.lower() in {"quit", "exit"}:
            print("Axiom> Bye!")
            break
        if not user:
            continue
        print("Axiom>", bot.say(user), "\n")


if __name__ == "__main__":
    main()
