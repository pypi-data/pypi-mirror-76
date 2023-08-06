import logging
import numpy as np

from enum import Enum
from typing import Tuple, Dict


_logger = logging.getLogger(__name__)


class GameCoreType(str, Enum):
    OLD_RANDOM_SNAIL = "random-snail",
    BINARY_SEARCH = "binary-search",
    TERNARY_SEARCH = "ternary-search"

    @staticmethod
    def of(value: str):
        for game_core_type in GameCoreType:
            if value == game_core_type:
                return game_core_type
        else:
            return None


def guess_number_game_core_random_snail(number: int, segment: Tuple):
    """This is the original implementation of the INEFFICIENT version of
    the number guessing algorithm (game_core_v2). It is added here as is.

    First, we set any random number, and then we decrease or
    we increase it depending on whether it is more or less than necessary.
    The function takes a guess and returns the number of attempts.
    Like a slow snail randomly thrown on a segment.

    Parameters:
        number (int): a number which the implemented algorithm must guess correctly
        segment (Tuple): the segment the given number belongs to (number ∈ segment)
    """
    count = 0
    iterations = 0
    predicted_number = np.random.randint(segment[0], segment[1])
    while number != predicted_number:  # В этой строке происходит первая попытка сравнения! (count = 0)
        count += 1
        iterations += 1
        if number > predicted_number:
            predicted_number += 1
        elif number < predicted_number:
            predicted_number -= 1

    return count, iterations


def guess_number_game_core_binary_search(number: int, segment: Tuple):
    """Binary search based algorithm to guess a number efficiently.

    Parameters:
        number (int): a number which the implemented algorithm must guess correctly
        segment (Tuple): the segment the given number belongs to (number ∈ segment)
    """
    count = 0
    iterations = 0
    lower = segment[0]
    upper = segment[1] + 1

    predicted_number = lower + (upper - lower) // 2
    while number != predicted_number:  # В этой строке происходит первая попытка сравнения! (count = 0)
        count += 1
        iterations += 1
        if number > predicted_number:
            lower = predicted_number + 1
        elif number < predicted_number:
            upper = predicted_number - 1
        predicted_number = lower + (upper - lower) // 2

    return count, iterations


def guess_number_game_core_ternary_search(number: int, segment: Tuple):
    """Binary search based algorithm to guess a number efficiently.

    Parameters:
        number (int): a number which the implemented algorithm must guess correctly
        segment (Tuple): the segment the given number belongs to (number ∈ segment)
    """
    count = 0
    iterations = 0
    lower = segment[0]
    upper = segment[1] + 1

    middle_1 = lower + (upper - lower) // 3
    middle_2 = upper - (upper - lower) // 3
    while middle_1 != number and middle_2 != number:  # В этой строке происходит первая попытка сравнения! (count = 0)
        count += 2  # В условии цикла мы сделали сравнение два раза, формально это увеличивает число count на 2.
        iterations += 1  # Также считаем формально число итераций цикла while.
        if number < middle_1:
            upper = middle_1 - 1
        elif number > middle_2:
            lower = middle_2 + 1
        else:
            lower = middle_1 + 1
            upper = middle_2 - 1

        middle_1 = lower + (upper - lower) // 3
        middle_2 = upper - (upper - lower) // 3

    return count, iterations


GAME_CORES = {
    GameCoreType.OLD_RANDOM_SNAIL: guess_number_game_core_random_snail,
    GameCoreType.BINARY_SEARCH: guess_number_game_core_binary_search,
    GameCoreType.TERNARY_SEARCH: guess_number_game_core_ternary_search
}


def get_game_core(game_core_type: GameCoreType):
    return GAME_CORES[game_core_type]


def score_game(game_core_type: GameCoreType,
               attempts: int = 1000,
               segment: Tuple = (1, 100),
               ) -> Dict:
    """Run the game a specified number of times to see how quickly the game guesses a number.

    Parameters:
        game_core_type (GameCoreType): a game core type
        attempts (int): the number of attempts a game algorithm has to demonstrate its efficiency
        segment (Tuple): the segment the given number belongs to (number ∈ segment)

    Returns:
        a dictionary with the structure {"mean-count": N1, "mean-iterations": N2} where {N1, N2} ∈ ℕ.
    """
    efficiency_measuments = list()
    np.random.seed(1)  # We make the RANDOM SEED fixed, in order to make our experiment reproducible!
    random_array = np.random.randint(segment[0], segment[1] + 1, size=attempts)
    game_core = get_game_core(game_core_type)

    for number in random_array:  # The main loop to test the given game core
        efficiency_parameters = game_core(number, segment)
        efficiency_measuments.append(efficiency_parameters)

    # All counts for all guessed numbers
    counts = [efficiency_parameters[0] for efficiency_parameters in efficiency_measuments]
    _logger.debug(f"""Counts for {game_core_type}:\n{counts}""")

    # All loop iterations for all guessed numbers
    iterations = [efficiency_parameters[1] for efficiency_parameters in efficiency_measuments]
    _logger.debug(f"""Iterations for {game_core_type}:\n{iterations}""")

    mean_count = round(np.mean(counts), 1)
    mean_iterations = round(np.mean(iterations), 1)

    print(f"- Ваш алгоритм \"{game_core_type.value}\" угадывает число в среднем за\n"
          + f"\t{mean_count} попыток ({int(mean_count)} целых) "
          + f"с {mean_iterations} ({int(mean_iterations)} целых) итерациями основного цикла в среднем.")

    return {
        "mean-count": mean_count,
        "mean-iterations": mean_iterations
    }
