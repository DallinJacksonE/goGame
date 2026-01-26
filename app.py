import copy


class GoGame:
    def __init__(self, size=9):
        self.size = size
        self.board = [[None for _ in range(self.size)]
                      for _ in range(self.size)]
        self.pastBoardState = copy.deepcopy(self.board)
        self.currentTurn = 'black'
        self.capturedTokens = {'black': 0, 'white': 0}

    def getOpponent(self, color):
        return 'white' if color == 'black' else 'white'

    def onBoard(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def validTurn(self, x, y):
        # Check if on board
        if not self.onBoard(x, y):
            return False, "Move out of bounds"

        if self.board[y][x] is not None:
            return False, "Stone already placed"

        return True

    def getGroup(self, x, y, board):

        color = board[y][x]
        group = set()
        liberties = set()
        visited = set()
        stack = [(x, y)]

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue

            visited.add((cx, cy))
            group.add((cx, cy))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if self.onBoard(nx, ny):
                    if board[ny][nx] is None:
                        liberties.add((nx, ny))
                    elif board[ny][nx] == color and (nx, ny) not in visited:
                        stack.append((nx, ny))

        return group, len(liberties)

    def placeStone(self, x, y):
        valid, message = self.validTurn(x, y)
        if not valid:
            return False, message

        # Place the stone tentatively
        self.board[y][x] = self.current_turn
        opponent = self.getOpponent(self.current_turn)

        # Check for captures (enemy groups with 0 liberties)
        captured_groups = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if self.onBoard(nx, ny):
                if self.board[ny][nx] == opponent:
                    group, liberties = self.getGroup(nx, ny, self.board)
                    if liberties == 0:
                        captured_groups.append(group)

        # Remove captured stones
        stones_captured_count = 0
        for group in captured_groups:
            for cx, cy in group:
                self.board[cy][cx] = None
                stones_captured_count += 1

        # Add to score
        self.captured_stones[self.current_turn] += stones_captured_count

        # Check for Suicide (if no captures made, and I have 0 liberties, it's illegal)
        my_group, my_liberties = self.get_group(x, y, self.board)
        if my_liberties == 0 and stones_captured_count == 0:
            self.board = self.pastBoardState  # Undo
            return False, "Suicide move is not allowed"

        # Switch turn
        self.current_turn = opponent
        return True, "Move successful"

    def to_dict(self):
        return {
            'board': self.board,
            'current_turn': self.current_turn,
            'captured': self.captured_stones,
            'size': self.size
        }
