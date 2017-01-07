def calc(performance, maximise=True):
    """Returns the maximin (pessimistic) metric for a set of solutions

    Metric obtained from:
    Wald, A. (1950) Statistical decision functions. New York; Chapman & Hall: London.

    'performance' is a 2D list of the performance metric used to
        evaluate each solution in each scenario
        dimension 1 is the solution index
        dimension 2 is the scenario index

    'maximise' is a boolean value (assumed true) that is
        true  if the aim is to maximise the value of performance (e.g. profit)
        false if the aim is to minimise the value of performance (e.g. cost)

    returns a 1D list of the maximin robustness for each solution
    """

    if maximise:
        # We find the worst-case (minimum) performance for each solution
        robustness = [min(solution) for solution in performance]
    else:
        # We find the worst-case (maximum) performance for each solution
        robustness = [max(solution) for solution in performance]

    return robustness

if __name__ == "__main__":
    performance = [[0.7, 0.8, 0.9], [0.8, 0.9, 1.0]]
    robustness = calc(performance)
    print(robustness)