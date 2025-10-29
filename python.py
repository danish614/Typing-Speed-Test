import time
import random

def edit_distance(a: str, b: str) -> int:
    """Calculate Levenshtein distance (number of mistakes)."""
    n, m = len(a), len(b)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1):
        dp[i][0] = i
    for j in range(m+1):
        dp[0][j] = j
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,
                dp[i][j-1] + 1,
                dp[i-1][j-1] + cost
                
            )
    return dp[n][m]

def compute_wpm_and_accuracy(target: str, typed: str, elapsed_seconds: float):
    edits = edit_distance(target, typed)
    max_len = max(len(target), 1)
    correct_chars = max_len - edits if edits <= max_len else 0
    minutes = elapsed_seconds / 60.0 if elapsed_seconds > 0 else 1/60
    wpm = (correct_chars / 5.0) / minutes
    accuracy = max(0.0, (1 - edits / max_len) * 100)
    return round(wpm, 2), edits, round(accuracy, 2)

def typing_test(sentences, tries=3):
    print("=== Typing Speed Test ===\n")
    print(f"You will get {tries} tries. Type the shown paragraph and press Enter.\n")
    best = {"wpm": 0, "accuracy": 0, "edits": None, "typed": "", "time": 0.0}

    for attempt in range(1, tries+1):
        target_sentence = random.choice(sentences)
        print(f"--- Try {attempt} ---")
        print("Type this paragraph:\n")
        print(f"> {target_sentence}\n")
        input("Press Enter when you are ready...")

        start = time.time()
        typed = input("\nStart typing: ")
        end = time.time()
        elapsed = end - start

        wpm, edits, accuracy = compute_wpm_and_accuracy(target_sentence, typed, elapsed)

        print(f"\nResult for Try {attempt}:")
        print(f"Time taken: {round(elapsed, 2)} sec")
        print(f"WPM: {wpm}")
        print(f"Mistakes: {edits}")
        print(f"Accuracy: {accuracy}%")
        print("-" * 40)

        if wpm > best["wpm"]:
            best.update({"wpm": wpm, "accuracy": accuracy, "edits": edits, "typed": typed, "time": elapsed})

    print("\n=== Summary (Best Try) ===")
    print(f"Best WPM: {best['wpm']}")
    print(f"Mistakes: {best['edits']}")
    print(f"Accuracy: {best['accuracy']}%")
    print(f"Time Taken: {round(best['time'], 2)} sec")
    print("\nKeep practicing! 🚀")

if __name__ == "__main__":
    paragraphs = [
        "The quick brown fox jumps over the lazy dog near the river bank on a sunny day.",
        "Python is a versatile programming language that is easy to learn and powerful for automation.",
        "Technology is evolving faster than ever, changing the way we live, learn, and communicate every day."
    ]
    typing_test(paragraphs, tries=3)
