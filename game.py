import random


class SudokuGenerator:
    def __init__(self):
        pass

    # Returns false if given 3x3 block contains num
    # Ensure the number is not used in the box
    def unUsedInBox(self, grid, rowStart, colStart, num):
        for i in range(3):
            for j in range(3):
                if grid[rowStart + i][colStart + j] == num:
                    return False
        return True

    # Fill a 3x3 matrix
    # Assign valid random numbers to the 3x3 subgrid
    def fillBox(self, grid, row, col):
        for i in range(3):
            for j in range(3):
                while True:
                    # Generate a random number between 1 and 9
                    num = random.randint(1, 9)
                    if self.unUsedInBox(grid, row, col, num):
                        break
                grid[row + i][col + j] = num

    # Check if it's safe to put num in row i
    # Ensure num is not already used in the row
    def unUsedInRow(self, grid, i, num):
        return num not in grid[i]

    # Check if it's safe to put num in column j
    # Ensure num is not already used in the column
    def unUsedInCol(self, grid, j, num):
        for i in range(9):
            if grid[i][j] == num:
                return False
        return True

    # Check if it's safe to put num in the cell (i, j)
    # Ensure num is not used in row, column, or box
    def checkIfSafe(self, grid, i, j, num):
        return (
            self.unUsedInRow(grid, i, num)
            and self.unUsedInCol(grid, j, num)
            and self.unUsedInBox(grid, i - i % 3, j - j % 3, num)
        )

    # Fill the diagonal 3x3 matrices
    # The diagonal blocks are filled to simplify the process
    def fillDiagonal(self, grid):
        for i in range(0, 9, 3):
            # Fill each 3x3 subgrid diagonally
            self.fillBox(grid, i, i)

    # Fill remaining blocks in the grid
    # Recursively fill the remaining cells with valid numbers
    def fillRemaining(self, grid, i, j):
        # If we've reached the end of the grid
        if i == 9:
            return True

        # Move to next row when current row is finished
        if j == 9:
            return self.fillRemaining(grid, i + 1, 0)

        # Skip if cell is already filled
        if grid[i][j] != 0:
            return self.fillRemaining(grid, i, j + 1)

        # Try numbers 1-9 in current cell
        for num in range(1, 10):
            if self.checkIfSafe(grid, i, j, num):
                grid[i][j] = num
                if self.fillRemaining(grid, i, j + 1):
                    return True
                grid[i][j] = 0

        return False

    # Remove K digits randomly from the grid
    # This will create a Sudoku puzzle by removing digits
    def removeKDigits(self, grid, k):
        while k > 0:
            # Pick a random cell
            cellId = random.randint(0, 80)

            # Get the row index
            i = cellId // 9

            # Get the column index
            j = cellId % 9

            # Remove the digit if the cell is not already empty
            if grid[i][j] != 0:
                # Empty the cell
                grid[i][j] = "#"
                # Decrease the count of digits to remove
                k -= 1

    # Generate a Sudoku grid with K empty cells
    def sudokuGenerator(self, k):
        # Initialize an empty 9x9 grid
        grid = [[0] * 9 for _ in range(9)]

        # Fill the diagonal 3x3 matrices
        self.fillDiagonal(grid)

        # Fill the remaining blocks in the grid
        self.fillRemaining(grid, 0, 0)

        # Remove K digits randomly to create the puzzle
        self.removeKDigits(grid, k)

        return grid

    def printGrid(self, grid):
        for r in range(9):
            for d in range(9):
                print(grid[r][d], end=" ")
            print()


if __name__ == "__main__":
    # Seed the random number generator
    random.seed()

    sudokuGenerator = SudokuGenerator()

    # Set the number of empty cells
    k = 20
    sudoku = sudokuGenerator.sudokuGenerator(k)

    # Print the generated Sudoku puzzle
    for c, v in enumerate(sudoku):
        if c % 3 == 0 and c != 0:
            print("---------------------")
        print(
            " | ".join(
                [" ".join(str(num) for num in v[i : i + 3]) for i in range(0, 9, 3)]
            )
        )
        if c % 3 != 2:
            print()

    print("\nSudoku puzzle generated with", k, "empty cells.")

    sudokuGenerator.printGrid(sudoku)
