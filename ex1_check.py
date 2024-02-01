import ex1
import search


def run_problem(func, targs=(), kwargs={}):
    result = (-3, "default")
    try:
        result = func(*targs, **kwargs)

    except Exception as e:
        result = (-3, e)
        print(result)
        raise e
    return result

# check_problem: problem, search_method, timeout
# timeout_exec: search_method, targs=[problem], timeout_duration=timeout
def solve_problems(problem, algorithm):
    for row in problem:
        print(row)

    try:
        p = ex1.create_pacman_problem(problem)
    except Exception as e:
        print("Error creating problem: ", e)
        return None

    if algorithm == "gbfs":
        result = run_problem((lambda p: search.breadth_first_graph_search(p)),targs=[p])
    else:
        result = run_problem((lambda p: search.astar_search(p, p.h)), targs=[p])

    if result and isinstance(result[0], search.Node):
        solve = result[0].path()[::-1]
        solution = [pi.action for pi in solve][1:]
        print(len(solution), solution)
    else:
        print("no solution")

# ['R', 'L', 'U', 'R', 'R', 'R', 'U', 'U', 'L', 'L', 'L']
problem0 = ((11, 10, 50, 10),
            (10, 99, 99, 11),
            (20, 10, 10, 10),
            (77, 10, 10, 10))


# 34 ['R', 'U', 'R', 'R', 'R', 'L', 'R', 'U', 'R', 'D', 'D', 'R', 'L', 'L', 'L', 'L', 'L', 'L', 'D', 'R', 'D', 'R', 'D', 'D', 'U', 'R', 'R', 'R', 'R', 'R', 'D', 'R', 'D', 'D']
# 52 ['D', 'R', 'R', 'R', 'D', 'R', 'L', 'U', 'L', 'L', 'L', 'D', 'L', 'L', 'U', 'U', 'U', 'U', 'R', 'R', 'R', 'D', 'D', 'D', 'R', 'D', 'R', 'R', 'D', 'D', 'D', 'L', 'U', 'R', 'U', 'U', 'L', 'U', 'L', 'L', 'L', 'L', 'L', 'U', 'U', 'U', 'R', 'R', 'R', 'R', 'R',
problem3 = (
            (10, 21, 10, 11, 11, 10, 11, 99),
            (10, 99, 99, 10, 10, 99, 10, 10),
            (10, 99, 77, 10, 99, 99, 99, 99),
            (10, 10, 10, 10, 10, 10, 99, 99),
            (11, 10, 10, 99, 10, 10, 10, 99),
            (10, 99, 99, 10, 99, 99, 10, 99),
            (99, 30, 99, 10, 10, 10, 11, 99),
            (99, 10, 99, 10, 99, 10, 40, 99),
        )
problem1 = ((20,10,10,10,10),
         (10,10,10,10,10),
         (10,11,10,10,10),
         (10,11,10,10,10),
         (77,11,10,10,10))
#solution1: len(solution) = 7
problem2 = ((21,31,41,11,11,11,11,11,11,11,11,11),
(11,99,99,99,99,11,99,99,99,99,99,11),
(11,99,99,99,99,11,99,99,99,99,99,11),
(11,11,11,99,99,11,11,11,11,11,11,11),
(99,99,11,99,99,11,99,99,11,99,99,99),
(99,99,11,99,99,11,99,99,11,99,99,99),
(11,11,11,11,11,11,99,99,11,11,11,11),
(11,99,99,99,99,99,99,99,99,99,99,11),
(11,99,99,99,99,99,99,99,99,99,99,11),
(11,11,11,11,11,11,11,11,11,11,11,77))
#solution2: len(solution) = 98

problem4 = ((10, 10, 10, 11),
            (10, 99, 10, 50),
            (10, 10, 10, 10),
            (77, 10, 10, 10))
# 6 ['R', 'R', 'U', 'R', 'U', 'U']
# 6 ['U', 'U', 'U', 'R', 'R', 'R']
def main():
    problem = problem3 #or problem2
    algorithm = "gbfs" #or "astar"

    solve_problems(problem, algorithm)

if __name__ == '__main__':
    main()