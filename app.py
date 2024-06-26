import random

def generate_wordsearch(words, size):
    grid = [['' for _ in range(size)] for _ in range(size)]

    for word in words:
        placed = False
        while not placed:
            direction = random.choice(['horizontal', 'vertical', 'diagonal'])
            if direction == 'horizontal':
                row = random.randint(0, size - 1)
                col = random.randint(0, size - len(word))
                if all(grid[row][col + k] == '' or grid[row][col + k] == word[k] for k in range(len(word))):
                    for k in range(len(word)):
                        grid[row][col + k] = word[k]
                    placed = True
            elif direction == 'vertical':
                row = random.randint(0, size - len(word))
                col = random.randint(0, size - 1)
                if all(grid[row + k][col] == '' or grid[row + k][col] == word[k] for k in range(len(word))):
                    for k in range(len(word)):
                        grid[row + k][col] = word[k]
                    placed = True
            else:
                row = random.randint(0, size - len(word))
                col = random.randint(0, size - len(word))
                if all(grid[row + k][col + k] == '' or grid[row + k][col + k] == word[k] for k in range(len(word))):
                    for k in range(len(word)):
                        grid[row + k][col + k] = word[k]
                    placed = True

    for i in range(size):
        for j in range(size):
            if grid[i][j] == '':
                grid[i][j] = chr(random.randint(65, 90))

    return grid

def print_grid(grid, found_word_coords_list=None):
    size = len(grid)
    print('  ', end='')
    for i in range(size):
        print(f'{i+1:2}', end=' ')
    print()
    for i in range(size):
        print(f'{chr(65 + i):2}', end=' ')
        for j in range(size):
            if found_word_coords_list and any((i, j) in found_word_coords for found_word_coords in found_word_coords_list):
                print('\033[4;30;1m' + grid[i][j] + '\033[0m' + '  ', end=' ')
            else:
                print(grid[i][j] + '  ', end='')
        print()


def validate_coordinates(coordinates, size):
    try:
        start, end = coordinates.split(' to ')
        start_row = ord(start[0].upper()) - ord('A')
        start_col = int(start[1:]) - 1
        end_row = ord(end[0].upper()) - ord('A')
        end_col = int(end[1:]) - 1

        if start_row < 0 or start_row >= size or start_col < 0 or start_col >= size:
            return None
        if end_row < 0 or end_row >= size or end_col < 0 or end_col >= size:
            return None

        return start_row, start_col, end_row, end_col
    except ValueError:
        return None

def check_word_location(grid, words, coordinates):
    start_row, start_col, end_row, end_col = coordinates

    for word in words:
        word_length = len(word)
        if start_row == end_row and end_col - start_col + 1 == word_length:
            if ''.join(grid[start_row][start_col:end_col + 1]) == word:
                return [(start_row, j) for j in range(start_col, end_col + 1)]
        elif start_col == end_col and end_row - start_row + 1 == word_length:
            word_vertical = ''.join(grid[i][start_col] for i in range(start_row, end_row + 1))
            if word_vertical == word:
                return [(i, start_col) for i in range(start_row, end_row + 1)]
        elif end_row - start_row + 1 == word_length and end_col - start_col + 1 == word_length:
            word_diagonal = ''.join(grid[start_row + k][start_col + k] for k in range(word_length))
            if word_diagonal == word:
                return [(start_row + k, start_col + k) for k in range(word_length)]

    return []


def main():
    found_woord_coords_list = []

    print("Welcome to CLI Word Search!")
    print("Select word search difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    difficulty_choice = int(input("Enter choice: "))
    
    if difficulty_choice == 1:
        difficulty = 10
    elif difficulty_choice == 2:
        difficulty = 15
    elif difficulty_choice == 3:
        difficulty = 20
    else:
        print("Invalid choice. Setting difficulty to Medium.")
        difficulty = 12

    print("Enter 10 words to be hidden in the word search.")
    words = [input(f"Enter word {i+1}: ").upper() for i in range(10)]
    wordsearch_grid = generate_wordsearch(words, difficulty)

    print("\nHere's your word search:")
    print_grid(wordsearch_grid)

    while True:
        user_input = input("\nEnter the location (e.g., 'A2 to C4') of a word to check or 'exit' to end: ")
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break

        coordinates = validate_coordinates(user_input, difficulty)
        if coordinates:
            found_word_coords = check_word_location(wordsearch_grid, words, coordinates)
            if found_word_coords:
                print("Successful! You found a word.")
                found_woord_coords_list.append(found_word_coords)
                print_grid(wordsearch_grid, found_woord_coords_list)
            else:
                print("No word found at that location. Try again!")
                print_grid(wordsearch_grid, found_woord_coords_list)
        else:
            print("Invalid input format. Please enter coordinates in the format 'A2 to C4'.")

if __name__ == "__main__":
    main()
