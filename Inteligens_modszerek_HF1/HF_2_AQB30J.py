import time

# BEÁLLÍTÁSOK

DEPTH = 5  # Teljes mélység (9 elegendő 3x3-hoz)
USE_AB = True
PLAYER = 'X'  # Ki kezd

BOARDS = {
    'empty': '.........',
    'mid': 'X.O..O...'
}


# STATISZTIKA

class Stats:
    def __init__(self):
        self.expanded = 0
        self.pruned = 0

    def reset(self):
        self.expanded = 0
        self.pruned = 0


stats = Stats()

# JÁTÉK LOGIKA

def print_board(board):
    """3x3 tábla kiírása."""
    for i in range(3):
        print(board[i * 3:(i + 1) * 3])
    print()


def check_winner(board):
    """Ellenőrzi a nyertest."""
    # Sorok
    for i in range(3):
        row = board[i * 3:(i + 1) * 3]
        if row == 'XXX':
            return 'X'
        if row == 'OOO':
            return 'O'

    # Oszlopok
    for i in range(3):
        col = board[i] + board[i + 3] + board[i + 6]
        if col == 'XXX':
            return 'X'
        if col == 'OOO':
            return 'O'

    # Átlók
    diag1 = board[0] + board[4] + board[8]
    diag2 = board[2] + board[4] + board[6]
    if diag1 == 'XXX' or diag2 == 'XXX':
        return 'X'
    if diag1 == 'OOO' or diag2 == 'OOO':
        return 'O'

    return None


def is_full(board):
    """Tele van-e a tábla."""
    return '.' not in board


def get_moves(board):
    """Elérhető lépések."""
    return [i for i in range(9) if board[i] == '.']


def make_move(board, pos, player):
    """Lépés végrehajtása."""
    b = list(board)
    b[pos] = player
    return ''.join(b)

# MINIMAX

def evaluate(board):
    """Tábla értékelése X szempontjából."""
    winner = check_winner(board)
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    else:
        return 0


def minimax(board, depth, is_max, alpha, beta, use_ab):
    """Minimax alfa-béta metszéssel."""
    stats.expanded += 1

    winner = check_winner(board)
    if winner == 'X':
        return None, 1
    elif winner == 'O':
        return None, -1
    elif is_full(board):
        return None, 0

    if depth == 0:
        return None, 0

    moves = get_moves(board)
    best_move = moves[0] if moves else None

    if is_max:  # X játékos
        best_val = -999
        for move in moves:
            new_board = make_move(board, move, 'X')
            _, val = minimax(new_board, depth - 1, False, alpha, beta, use_ab)

            if val > best_val:
                best_val = val
                best_move = move

            if use_ab:
                alpha = max(alpha, val)
                if beta <= alpha:
                    stats.pruned += 1
                    break

        return best_move, best_val

    else:  # O játékos
        best_val = 999
        for move in moves:
            new_board = make_move(board, move, 'O')
            _, val = minimax(new_board, depth - 1, True, alpha, beta, use_ab)

            if val < best_val:
                best_val = val
                best_move = move

            if use_ab:
                beta = min(beta, val)
                if beta <= alpha:
                    stats.pruned += 1
                    break

        return best_move, best_val

# JÁTÉK SZIMULÁCIÓ

def play_game(start_board, use_ab, show_steps=True):
    """Teljes játék lejátszása."""
    board = start_board
    current_player = PLAYER
    move_count = 0

    if show_steps:
        print(f"Kezdő állapot:")
        print_board(board)

    while True:
        winner = check_winner(board)
        if winner:
            if show_steps:
                print(f"{winner} NYERT!")
            return winner

        if is_full(board):
            if show_steps:
                print("DÖNTETLEN!")
            return 'D'

        # Következő lépés számítása
        stats.reset()
        start = time.perf_counter()

        is_max = (current_player == 'X')
        move, value = minimax(board, DEPTH, is_max, -999, 999, use_ab)

        elapsed = (time.perf_counter() - start) * 1000

        if move is None:
            break

        board = make_move(board, move, current_player)
        move_count += 1

        if show_steps:
            print(f"Lépés #{move_count} - {current_player} lép a {move} pozícióra")
            print(
                f"  → move={move} value={value} expanded={stats.expanded} pruned={stats.pruned} time_ms={elapsed:.2f}")
            print_board(board)

        # Játékos váltás
        current_player = 'O' if current_player == 'X' else 'X'

    return None

# FŐ PROGRAM

def main():
    print("=" * 70)
    print("TIC-TAC-TOE MINIMAX MEGOLDÓ")
    print("=" * 70)
    print(f"Beállítások: DEPTH={DEPTH}, PLAYER={PLAYER}")
    print()

    # Alfa-béta metszéssel
    print("\n" + "=" * 70)
    print("ALFA-BÉTA METSZÉSSEL (USE_AB = True)")
    print("=" * 70)

    for name, board in BOARDS.items():
        print(f"\n{'─' * 70}")
        print(f"Tábla: {name.upper()}")
        print(f"{'─' * 70}")
        result = play_game(board, True, show_steps=True)
        print(f"Eredmény: {result}")

    # Alfa-béta nélkül
    print("\n\n" + "=" * 70)
    print("ALFA-BÉTA NÉLKÜL (USE_AB = False)")
    print("=" * 70)

    for name, board in BOARDS.items():
        print(f"\n{'─' * 70}")
        print(f"Tábla: {name.upper()}")
        print(f"{'─' * 70}")
        result = play_game(board, False, show_steps=True)
        print(f"Eredmény: {result}")

    # Összehasonlítás
    print("\n\n" + "=" * 70)
    print(" TELJESÍTMÉNY ÖSSZEHASONLÍTÁS")
    print("=" * 70)

    for name, board in BOARDS.items():
        print(f"\n{name.upper()} tábla:")

        # Alfa-bétával
        stats.reset()
        start = time.perf_counter()
        play_game(board, True, show_steps=False)
        time_ab = (time.perf_counter() - start) * 1000
        exp_ab = stats.expanded
        prune_ab = stats.pruned

        # Alfa-béta nélkül
        stats.reset()
        start = time.perf_counter()
        play_game(board, False, show_steps=False)
        time_no_ab = (time.perf_counter() - start) * 1000
        exp_no_ab = stats.expanded

        print(f"  Alfa-béta:     expanded={exp_ab:6d}, pruned={prune_ab:5d}, time={time_ab:8.2f}ms")
        print(f"  Alfa-béta OFF: expanded={exp_no_ab:6d}, pruned=    0, time={time_no_ab:8.2f}ms")
        print(
            f"  Megtakarítás:  {100 * (exp_no_ab - exp_ab) / exp_no_ab:.1f}% csomópont, {100 * (time_no_ab - time_ab) / time_no_ab:.1f}% idő")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()