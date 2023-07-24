import string


def remove_non_alpha(s: str) -> str:
    """Removes non-alphanumeric characters."""
    return "".join(letter for letter in s if letter.isalpha())


def damerau_levenshtein_distance(str1: str, str2: str, transposition_cost: int | float) -> int:
    """https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
    Helps to evaluate correctness of user_input"""

    m = [[0 for _ in range(len(str2) + 1)] for _ in range(len(str1) + 1)]

    for i in range(len(str1) + 1):
        for j in range(len(str2) + 1):
            if i == 0:
                m[i][j] = j
            elif j == 0:
                m[i][j] = i
            else:
                if str1[i - 1] != str2[j - 1]:
                    m[i][j] = 1 + min(m[i][j - 1],
                                      m[i - 1][j],
                                      m[i - 1][j - 1]
                                      )
                    if i > 1 and j > 1 and str1[i - 1] == str2[j - 2] and str1[i - 2] == str2[j - 1]:
                        m[i][j] = min(m[i][j],
                                      m[i - 2][j - 2] + transposition_cost)
                else:
                    m[i][j] = m[i - 1][j - 1]

    max_len = max(len(str1), len(str2))
    return m[-1][-1] / max(max_len, 1)  # avoid dividing by 0


def adjust_strings(
        ignore_capitalization: bool,
        ignore_punctuation: bool,
        correct_answer: str,
        user_input: str
) -> tuple[str, str]:
    # remove non-alpha characters (if applicable)
    if ignore_punctuation:
        user_input = remove_non_alpha(user_input)
        correct_answer = remove_non_alpha(correct_answer)
    # remove capitalization (if applicable)
    if ignore_capitalization:
        user_input = user_input.lower()
        correct_answer = correct_answer.lower()
    return user_input, correct_answer


def apply_dld(
        ignore_capitalization: bool,
        ignore_punctuation: bool,
        correct_answer: str,
        user_input: str,
        transposition_cost: float | int
) -> tuple[float, bool]:
    if ignore_punctuation or ignore_capitalization:
        user_input, correct_answer = adjust_strings(
            ignore_capitalization, ignore_punctuation,
            correct_answer, user_input)
    # calculate the D-L distance
    dld = damerau_levenshtein_distance(user_input, correct_answer, transposition_cost)
    return dld


def evaluate_user_input(
        ignore_capitalization: bool,
        ignore_punctuation: bool,
        correct_answer: str,
        user_input: str,
        transposition_cost: float | int,
        threshold: float
):
    result = apply_dld(
        ignore_capitalization, ignore_punctuation,
        correct_answer, user_input, transposition_cost
    )
    if result == 0:
        return "correct_answer"
    elif result <= threshold:
        return "partially_correct_answer"
    else:
        return "incorrect_answer"


def extract_special_letters(words: list[str]) -> list[str]:
    special_letters = []
    for word in words:
        for letter in word:
            if letter not in string.printable and letter not in special_letters:
                special_letters.append(letter)

    return special_letters
