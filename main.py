# date: 2020/10/03
# github name: pyMike
# creator name: Michael Glaude
# description:  Recursive search to find word locations on a 2 dimensional array/board.
    # given a 2D array of characters , create a function to check if the word exists in the grid.
    # characters can be neighbors horizontally or vertically (not diagonal)
    # uses recursion for the search and prints out the solutions for verification.

#--------------------------------------------------------------------------------------------
def move(board, position, direction ):
    """Return a new 'legal neighboaring' position"""
    n_cols = len(board[0])
    n_rows = len(board)
    x = position[0] + direction[0]
    y = position[1] + direction[1]

    if (x>=0 and x< n_rows) & (y>=0 and y < n_cols):
        # this move is withing bounds of board
        return (x, y)
    else:
        return None   #...outside bounds of board
#--------------------------------------------------------------------------------------------
def possible_neighbors(board, position):
    """Generates possible possitions of neighbors on board."""
    # general case: moves = { up, down, left, right }
    up = (-1, 0)
    down = (1, 0)
    left = (0, -1)
    right = (0, 1)
    moves = [ up, down, left, right]   #...can add any kind of move here if need be...for different games!
    move_list = []
    for direction in moves:
        new_position = move(board, position, direction)
        if new_position != None:
            move_list.append(new_position)
    return move_list
#--------------------------------------------------------------------------------------------
def search_word_from_position(board, word, beg_position):
    """Searches for word starting from position (recursive search)."""
    position_lst = [beg_position]
    #Assuming word is at least len(word) = 1.
    if len( word ) == 1:
        # Do not search neighbores...this is end of word.
        if word == board[beg_position[0]][beg_position[1]]:
            return [beg_position]  # None, True, list?
        else:
            return []

    next_letter = word[1]

    neighbors = possible_neighbors(board, beg_position)
    solution_list = []
    matching_neighbors = []

    for neighbor in neighbors:
        i,j = neighbor
        print("checking neighbor at", i,j)
        if next_letter == board[i][j]:
            #Found matching neighbor.
            matching_neighbors.append(neighbor)
            #recursively find sub-word starting at neighbor positon...
            solution = search_word_from_position(board, word[1:], neighbor)
            if solution != []:
                solution_list.append(solution)

    if solution_list != []:
        return [ beg_position, solution_list ]
    else:
        return []

#--------------------------------------------------------------------------------------------
def find_starting_positions(board, word):
    # Find all possible starting points of word on board...
    word_starting_points = []
    for row, row_lst in enumerate(board):
        for col, col_value in enumerate(row_lst):
            position = (row, col)
            if word[0] == board[row][col]:
                # Found a staring position...
                word_starting_points.append(position)
    return word_starting_points

#--------------------------------------------------------------------------------------------
# convert to matrix
def run_search( board, word ):
    """Return list of legal moves...p1, p2 are (i,j) tuples indicating positions"""
    # Note: it's unclear based on question what are the set of legal moves...reason to clearify.
    # Questions:
    # 1) Can I assume I can backup to previous character?
    #    ...Yes...I will assume I can backup.
    #    ...furthermore...this would allow for palindrome words to work.
    # 2) Can I start the word anywhere on board?
    #    ...Assuming yes.
    #
    # Legal moves for differnt possitions...
    # if corner( 0, 0): moves = {down, right}
    # if corner( 0, row_len): moves = {down, left}
    # if corner( row_len, 0): moves = {up, right}
    # if corner( row_len, col_len): moves = {up, left}
    #
    # if left edge moves = { up, down, right }
    # if right edge moves = { up, down, left }
    # if top edge moves = { down, left, right }
    # if bottom edge moves = { up, left, right }
    #
    # general case: moves = { up, down, left, right }
    up = (-1,0)
    down = (1,0)
    left = (0, -1)
    right = (0, 1)

    # Find starting point of word...
    print(f"word = {word}")
    print("Board =")
    print_board(board)

    # Find the possible positions the word can start at...
    starting_points = find_starting_positions(board, word)
    print(f"starting_points= {starting_points}")

    # Cicle through all starting possitions of word...
    solutions = []
    if starting_points != []:
        for position in starting_points:
            # Recursive search for word starting at position...
            moves = search_word_from_position(board, word, position)
            print(f"found --> position= {position}, moves = {moves}")
            if moves != []:
                #solutions.append( [position] + moves )
                solutions.append( moves )

    # Display result...
    if solutions == []:
        print(f"Word: {word} not found on board")
    else:
        print(f"All possible solutions of finding {word} on board...")
        print_board(board)
        for solution in solutions:
            print(f"Word: {word} found on board at ...")
            print(solution)

def print_board(board):
    for i, row in enumerate(board):
        for j, letter in enumerate(row):
            print(f"{letter}({i},{j}), ", end='')
        print('')

#--------------------------------------------------------------------------------------------
if __name__== "__main__":
    board = [
        ['A', 'B', 'C'],
        ['S', 'F', 'P'],
        ['A', 'D', 'E']
    ]

    # Running some test cases
    print('-TESTS-'*(80//7))
    word = "A"
    run_search(board, word )
    print('-'*80)

    word = "X"             #...does not exist on board.
    run_search(board, word )
    print('-'*80)

    word = "AB"
    run_search(board, word )
    print('-'*80)

    word = "ABC"
    run_search(board, word )
    print('-'*80)

    word = "ABCPEDFBA"
    run_search(board, word )
    print('-'*80)

    print("Palindrom case: can backup on itself...")
    word = "ABCBA"   #...trying palindrom ...should backup on itself!
    run_search(board, word )
    print('-'*80)

    # More complex case with a "New broad" with possible bifurcations i.e. multiple paths along route of word.
    print("More Complex case:  New Board, Multiple paths, two starting points, five paths from A to E...")
    print("Note: output is a tree structure difficult to read ...output could be much improved!")
    board = [
       ['A', 'B', 'C'],
       ['B', 'C', 'D'],
       ['A', 'D', 'E']
     ]
    word = "ABCDE"  # ...example many solutions for same starting point
                    # ...i.e. there are two staring points and a total five paths from A to E.
    run_search(board, word)
    print('-' * 80)
