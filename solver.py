import game
import random
import argparse
import time

print("Welcome to the sudoku Solver!")


class CSP:
    def __init__(self, puzzle, use_mrv: bool = True, inference: bool = True):
        self.puzzle = puzzle
        self.variables = [(i, j) for i in range(9) for j in range(9)]
        self.domains = {}  # Domains for each variables
        self.constraints = {}  # Constraints between variables
        self.inference = inference
        self.initialize_domains()
        self.initialize_constraints()
        self.backtrack_count = 0
        self.use_mrv = use_mrv

    def initialize_domains(self):
        for var in self.variables:
            i, j = var
            if self.puzzle[i][j] == "#":
                self.domains[var] = set(range(1, 10))  # Possible values 1-9
            else:
                self.domains[var] = {self.puzzle[i][j]}  # Fixed value

    def initialize_constraints(self):
        for var in self.variables:
            i, j = var
            self.constraints[var] = set()
            # Row and Column constraints
            for k in range(9):
                if k != j:
                    self.constraints[var].add((i, k))  # Same row
                if k != i:
                    self.constraints[var].add((k, j))  # Same column
            # 3x3 Box constraints
            box_row_start = (i // 3) * 3
            box_col_start = (j // 3) * 3
            for r in range(box_row_start, box_row_start + 3):
                for c in range(box_col_start, box_col_start + 3):
                    if (r, c) != var:
                        self.constraints[var].add((r, c))  # Same box

    def is_consistent(self, var, value):
        for neighbor in self.constraints[var]:
            # Only check neighbors that are already assigned
            if len(self.domains[neighbor]) == 1:
                if value == next(iter(self.domains[neighbor])):
                    return False
        return True

    # Backtracking to solve sudoku CSP Can Enable or Disable inference
    def backtrack(self):
        # Check if assignment is complete
        if all(len(self.domains[var]) == 1 for var in self.variables):
            return True

        # Select unassigned variable with the smallest domain (MRV heuristic)
        if self.use_mrv:
            var = min(
                (v for v in self.variables if len(self.domains[v]) > 1),
                key=lambda v: len(self.domains[v]),
            )
        else:
            var = next(v for v in self.variables if len(self.domains[v]) > 1)

        for value in list(self.domains[var]):
            if self.is_consistent(var, value):
                # Temporarily assign value
                original_domain = self.domains[var].copy()
                self.domains[var] = {value}

                # Inference step
                removed = []
                if self.inference:
                    result = self.inference_step(var, value)
                    if result is False:
                        # Restore domains before continuing
                        self.domains[var] = original_domain
                        continue
                    else:
                        removed = result

                # Recur
                if self.backtrack():
                    return True

                # Undo assignment
                self.domains[var] = original_domain
                for neighbor, val in removed:
                    self.domains[neighbor].add(val)

        self.backtrack_count += 1
        return False

    def inference_step(self, var, value):
        removed = []

        for neighbor in self.constraints[var]:
            if value in self.domains[neighbor] and len(self.domains[neighbor]) > 1:
                self.domains[neighbor].remove(value)
                removed.append((neighbor, value))

                if len(self.domains[neighbor]) == 0:
                    # Restore before failing
                    for n, v in removed:
                        self.domains[n].add(v)
                    return False

        return removed

    def solve(self):
        if self.backtrack():
            return {var: next(iter(self.domains[var])) for var in self.variables}
        else:
            return None

    def print_solution(self):
        solution = self.solve()
        print(solution)
        if solution:
            print("\nSolution found:\n")
            for i in range(9):
                row = []
                for j in range(9):
                    row.append(solution[(i, j)])
                print(" ".join(str(num) for num in row))
        else:
            print("No solution found.")

    def print_constraints(self):
        for var, neighbors in self.constraints.items():
            print(f"Variable {var} has constraints with: {neighbors}")

    def print_domains(self):
        for var, domain in self.domains.items():
            print(f"Variable {var} has domain: {domain}")


def benchmark(mode, runs):
    sudokuGen = game.SudokuGenerator()

    difficulty_map = {"easy": 20, "medium": 40, "hard": 55}
    k = difficulty_map[mode]

    print(f"\nRunning Benchmark ({runs} runs) - Mode: {mode}\n")

    configs = [
        ("No MRV, No Inference", False, False),
        ("MRV Only", True, False),
        ("Inference Only", False, True),
        ("MRV + Inference", True, True),
    ]

    for name, use_mrv, inference in configs:
        total_backtracks = 0
        total_time = 0

        for _ in range(runs):
            sudoku = sudokuGen.sudokuGenerator(k)

            csp = CSP(sudoku, use_mrv=use_mrv, inference=inference)

            start = time.time()
            csp.solve()
            end = time.time()

            total_backtracks += csp.backtrack_count
            total_time += end - start

        print(f"--- {name} ---")
        print(f"Average Backtracks: {total_backtracks / runs:.2f}")
        print(f"Average Time: {total_time / runs:.4f} sec\n")


def main(args):
    if args.benchmark:
        benchmark(args.mode, args.runs)
        return

    random.seed()
    sudokuGen = game.SudokuGenerator()

    difficulty_map = {"easy": 20, "medium": 40, "hard": 55}

    k = difficulty_map[args.mode]

    sudoku = sudokuGen.sudokuGenerator(k)
    sudokuGen.printGrid(sudoku)
    print("\nSolving the Sudoku Puzzle...\n")

    csp = CSP(sudoku, use_mrv=args.mrv, inference=args.inference)
    csp.print_constraints()
    csp.print_domains()
    csp.solve()
    print("\nSolved Sudoku Puzzle:\n")
    csp.print_solution()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sudoku Solver using CSP")
    parser.add_argument(
        "mode",
        choices=["easy", "medium", "hard"],
        help="Select difficulty level of Sudoku",
    )
    parser.add_argument(
        "--inference",
        action="store_true",
        help="Enable inference during backtracking search",
    )
    parser.add_argument(
        "--mrv",
        action="store_true",
        help="Enable MRV during backtracking search",
    )
    parser.add_argument(
        "--benchmark", action="store_true", help="Run benchmark comparison"
    )

    parser.add_argument(
        "--runs", type=int, default=5, help="Number of runs for benchmark"
    )

    args = parser.parse_args()
    main(args)
