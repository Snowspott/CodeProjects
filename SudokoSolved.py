from copy import deepcopy
import re

class Cell:
  def __init__(s, str_index, num):
    s.num = None if num == '-' else int(num)
    #s.row = 6
    #s.row = str_index % 3
    s.row = str_index // 6
    #if s.row > 3:
    #    s.row =3

    #s.col = 6
    s.col = str_index % 6
    #print(s.row, s.col) # grei for debug, "hvorfor virker du ikke?"
    #rint(s.col )
    s.box = [ [0, 1, 2],
              [3, 4, 5] ][s.row // 3][s.col // 2]
    #print(s.box )
    s.possi = set(range(1,7)) if not s.num else set()


class Sudoku:
  def __init__(s, board_string):
    s.board = [Cell(i, c) for i, c in enumerate(board_string)]

  def korekt(s):
    return True

  def Rekker(s, num):
    return [cell for cell in s.board if cell.row == num]

  def Koloner(s, num):
    return [cell for cell in s.board if cell.col == num]

  def IndreBox(s, num):
    return [cell for cell in s.board if cell.box == num]

  def solve(s):
    for _ in range(10):
      s.check_individuals()
      s.scan_groups()
      if s.solved():
        break
    if not s.solved():
      s.start_guessing()

  def solved(s):
    return all(cell.num for cell in s.board)

  def unsolved(s):
    return [cell for cell in s.board if not cell.num]

  def check_individuals(s):
    for cell in s.unsolved():
      s.try_solve_cell(cell)

  def try_solve_cell(s, cell):
    cell.possi -= {each.num for each in s.Rekker(cell.row)}
    cell.possi -= {each.num for each in s.Koloner(cell.col)}
    cell.possi -= {each.num for each in s.IndreBox(cell.box)}
    if len(cell.possi) == 1:
      s.Generate_Solution_based_on_cell(cell)

  def Generate_Solution_based_on_cell(s, cell):
    cell.num = cell.possi.pop()
    s.update_relatives(cell)

  def update_relatives(s, cell):
    for each in s.Rekker(cell.row):
      each.possi -= {cell.num}
    for each in s.Koloner(cell.col):
      each.possi -= {cell.num}
    for each in s.IndreBox(cell.box):
      each.possi -= {cell.num}

  def scan_groups(s):
    for row in range(6):
      s.find_unique(s.Rekker(row))
    for col in range(6):
      s.find_unique(s.Koloner(col))
    for box in range(6):
      s.find_unique(s.IndreBox(box))

  def find_unique(s, cell_list):
    possi_count = {i: 0 for i in range(1, 7)}
    for cell in cell_list:
      for num in cell.possi:
        possi_count[num] += 1
    unique_num = {num for num in possi_count if possi_count[num] == 1}
    for ans in unique_num:
      for cell in cell_list:
        if ans in cell.possi:
          cell.possi = {ans}
          s.Generate_Solution_based_on_cell(cell)

  def start_guessing(s):
    s.try_find_correct_guess([s])

  def map_guesses(s, obj):
    return [Guess(obj.board, num).solve() for num in obj.unsolved()[0].possi]

  def try_find_correct_guess(s, guesses):
    guesses = [guess for guess in guesses if guess.korekt()]
    if not guesses:
      return "no valid guess"
    find_solved = [obj.board for obj in guesses if obj.solved()]
    if find_solved:
      s.board = find_solved[0]
    else:
      more_guesses = []  #algoritme for å gjette seg fra,
      for guess in guesses:
        more_guesses += s.map_guesses(guess)
      s.try_find_correct_guess(more_guesses[:11])

  def __repr__(s):
    board = '''
    +-------+-------+
    | X X X | X X X |
    | X X X | X X X | 
    +-------+-------+
    | X X X | X X X | 
    | X X X | X X X |
    +-------+-------+
    | X X X | X X X | 
    | X X X | X X X | 
    +-------+-------+
    '''
    for cell in s.board:
      board = re.sub('X', str(cell.num or ' '), board, count = 1)
    return board

  def to_pos(s):  # Algorimte, som viser antal mulige, i vær celle, vis din soduko ikke er komplett.
    MuligeValg = '''
    +---------+---------+---------+---------+---------+---------+
    |XXXXXXXXX XXXXXXXXX XXXXXXXXX|XXXXXXXXX XXXXXXXXX XXXXXXXXX|
    |XXXXXXXXX XXXXXXXXX XXXXXXXXX|XXXXXXXXX XXXXXXXXX XXXXXXXXX|
    +---------+---------+---------|---------+---------+---------|
    |XXXXXXXXX XXXXXXXXX XXXXXXXXX|XXXXXXXXX XXXXXXXXX XXXXXXXXX|
    |XXXXXXXXX XXXXXXXXX XXXXXXXXX|XXXXXXXXX XXXXXXXXX XXXXXXXXX|
    +---------+---------+---------|---------+---------+---------|
    |XXXXXXXXX XXXXXXXXX XXXXXXXXX|XXXXXXXXX XXXXXXXXX XXXXXXXXX|
    |XXXXXXXXX XXXXXXXXX XXXXXXXXX|XXXXXXXXX XXXXXXXXX XXXXXXXXX|
    +---------+---------+---------+---------+---------+---------+
    '''
    for cell in s.board:
      MuligeValg = re.sub('XXXXXXXXX', ''.join([str(i) for i in cell.possi]).center(9), MuligeValg, count = 1)
    return MuligeValg


class Guess(Sudoku):
  def __init__(s, in_board, num):
    s.board = deepcopy(in_board)
    s.guess(num)

  def solve(s):
    for _ in range(6):
      s.check_individuals()
      s.scan_groups()
      if s.solved():
        break
    return s

  def guess(s, num):
    cell =s.unsolved()[0]
    cell.possi = {num}
    s.Generate_Solution_based_on_cell(cell)

  def korekt(s):
    return all([any(cell.possi) for cell in s.board if not cell.num])


#TEST =  '-6-------6243-451----2-----45---13-2'
TEST =  '-6-------6243-4-1----2-----45---1--2'
#TEST =   '123456456123-----------------------4'
s = Sudoku(TEST)


if __name__ == '__main__':
  s = Sudoku(TEST)
  s.solve()
  print(s)
 #print(s.to_pos()) # Aktiver denne vis du vil se hva du har av valg!!!
