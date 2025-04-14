import copy


class Node:
    def __init__(self, board, moves):
        self.board = copy.deepcopy(board)
        self.moves = moves[:]
        self.cost = 0
        self.heuristic = 0

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def where_zero(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if self.board[r][c] == 0:
                    return r, c
        return None, None

    def get_moves(self):
        return self.moves

    def get_board(self):
        return self.board

    def add_new(self, new_direction):
        new_board = copy.deepcopy(self.board)
        return Node(new_board, self, new_direction)

    def get_last_move(self):
        if len(self.moves) == 0:
            return ""
        return self.moves[-1]

    def move(self, direction, rows, cols):
        r, c = self.where_zero()
        new_r, new_c = r, c

        if self.get_last_move() == "L" and direction == "R":
            return None
        if self.get_last_move() == "R" and direction == "L":
            return None
        if self.get_last_move() == "U" and direction == "D":
            return None
        if self.get_last_move() == "D" and direction == "U":
            return None

        if not self.is_move_legal(direction, rows, cols):
            return None

        new_board = [row[:] for row in self.get_board()]

        if direction == "L":
            new_c -= 1
        if direction == "R":
            new_c += 1
        if direction == "U":
            new_r -= 1
        if direction == "D":
            new_r += 1

        new_board[r][c], new_board[new_r][new_c] = new_board[new_r][new_c], new_board[r][c]

        new_moves = self.moves + direction
        return Node(new_board, new_moves)

    def is_move_legal(self, direction, rows, cols):
        r, c = self.where_zero()
        if r == 0 and direction == "U":
            return False
        if r == rows - 1 and direction == "D":
            return False
        if c == 0 and direction == "L":
            return False
        if c == cols - 1 and direction == "R":
            return False
        else:
            return True

    def goal(self, rows, cols):
        expected = []
        n = 1

        for i in range(rows):
            row = []
            for j in range(cols):
                if i == rows - 1 and j == cols - 1:
                    row.append(0)
                else:
                    row.append(n)
                    n += 1
            expected.append(row)

        return expected

    def get_path(self):
        return self.moves

    def the_end(self, visited, processed, time, length, info):
        info.set_length_found(length)
        info.set_processed_states(processed)
        info.set_searching_time(time)
        info.set_visited_states(visited)
