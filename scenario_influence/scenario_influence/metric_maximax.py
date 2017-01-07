def calc(performance, maximise=True):
    """Returns the maximax (optimistic) metric for a set of solutions

    'performance' is a 2D list of the performance metric used to
        evaluate each solution in each scenario
        dimension 1 is the solution index
        dimension 2 is the scenario index

    'maximise' is a boolean value (assumed true) that is
        true  if the aim is to maximise the value of performance (e.g. profit)
        false if the aim is to minimise the value of performance (e.g. cost)

    returns a 1D list of the maximax robustness for each solution
    """

    if maximise:
        # We find the best-case (maximum) performance for each solution
        robustness = [max(solution) for solution in performance]
    else:
        # We find the best-case (minimum) performance for each solution
        robustness = [min(solution) for solution in performance]

    return robustness

if __name__ == "__main__":
    performance = [[0.7, 0.8, 0.9], [0.8, 0.9, 1.0]]
    robustness = calc(performance)
    print(robustness)