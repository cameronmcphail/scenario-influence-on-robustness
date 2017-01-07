def calc(performance, maximise=True, threshold=0.95):
    """Returns the Starr's Domain Criterion metric for a set of solutions

    Metric obtained from:
    Starr, M. K. (1963) Product design and decision theory. Prentice-Hall.

    'performance' is a 2D list of the performance metric used to
        evaluate each solution in each scenario
        dimension 1 is the solution index
        dimension 2 is the scenario index

    'threshold' is a value that defines whether solutions pass or fail
        it is used to check that the performance is better than or equal
        to the threshold

    'maximise' is a boolean value (assumed true) that is:
        true  if the aim is to maximise the value of performance (e.g. profit)
        false if the aim is to minimise the value of performance (e.g. cost)

    returns a 1D list of the robustness for each solution using Starr's Domain Criterion
    """

    robustness = []

    for solution in performance:
        # A count of the number of scenarios that a solution 'passes' in
        count = 0

        for scenario in solution:
            # If higher values are better...
            if maximise:
                # If the solution 'passes' in this scenario
                if scenario >= threshold:
                    # Count the number of scenarios that 'pass'
                    count += 1
            # If lower values are better...
            else:
                # If the solution 'passes' in this scenario
                if scenario <= threshold:
                    # Count the number of scenarios that 'pass'
                    count += 1
        
        # Get the proportion of scenarios that a solution 'passes' in
        robustness.append(count / len(solution))
    
    return robustness

if __name__ == "__main__":
    performance = [[0.7, 0.8, 0.9], [0.8, 0.9, 1.0]]
    robustness = calc(performance, 0.95)
    print(robustness)