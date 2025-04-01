# see:
# https://www.dsm.fordham.edu/~moniot/taxman.html

import datetime, pprint

def play(g):
    green = g['green']
    grey = g['grey']
    taken = g['taken']
    taxman_sum = g['taxman_sum']
    total_sum = g['total_sum']
    sequence = g['sequence']
    set_sequence = set(sequence)

    if taxman_sum >= total_sum / 2:
        # taxman took more than a half => player lost anyway, terminate branch
        return {}
    elif not green:
        # no more moves and taxman took less than a half => player wins
        print(f' WON, length = {len(sequence)}, taxman_sum = {taxman_sum}, player_sum = {total_sum - taxman_sum}, sequence = {str(sequence)}')

    for n in green:
        # taxman takes all factors except what was taken by player
        next_taken = (taken | factors[n]) - set_sequence - {n}

        # not taken by taxman or player:
        # everything green except taken by taxman or by player
        not_taken = green.keys() - next_taken - set_sequence - {n}

        # green: everything not yet taken that has factors also not yet taken => can be taken by player on the next move
        next_green = {a for a in not_taken if (factors[a] - next_taken - set_sequence - {n})}

        # grey: everything not yet talen that has no factors not yet taken => cannot be taken by player on the next move
        next_grey = (grey - next_taken) | (not_taken - next_green)

        # write state, make next move
        next_sequence = sequence + [n]
        green[n] = {'green': {k: {} for k in next_green}, 'grey': next_grey, 'taken': next_taken, 'taxman_sum': sum(next_taken) + sum(next_grey), 'total_sum': total_sum, 'sequence': next_sequence}
        green[n] = play(green[n])
    return g

numbers = set(range(1, int(input('Pot size: ')) + 1))

# factors for each number in a pot
factors = {a: {b for b in numbers if b != a and a % b == 0} for a in numbers}

# initial state
grey = {1}
taken = set()
total_sum = sum(numbers)
initial_state = {'green': {n: {} for n in numbers if n not in grey}, 'grey': grey, 'taken': taken, 'length': 0, 'taxman_sum': 0, 'total_sum': total_sum, 'sequence': []}

t1 = datetime.datetime.now()
games = play(initial_state)
t2 = datetime.datetime.now()
print(t2 - t1)

#pprint.pprint(games)
