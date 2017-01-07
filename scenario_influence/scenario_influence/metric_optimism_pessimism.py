import metric_maximin
import metric_maximax

def calc(performance, maximise=True, alpha=0.5):
    """Returns the Optimism-Pessimism metric for a set of solutions

    Metric obtained from:
    Hurwicz, L. (1953) 'Optimality criterion for decision making under ignorance', Uncertainty and Expectations in Economics: Essays in Honour of GLS Shackle.

    'performance' is a 2D list of the performance metric used to
        evaluate each solution in each scenario
        dimension 1 is the solution index
        dimension 2 is the scenario index

    'alpha' is a factor that shows what proportion of the optimism rule to use
        0 < alpha < 1

    'maximise' is a boolean value (assumed true) that is
        true  if the aim is to maximise the value of performance (e.g. profit)
        false if the aim is to minimise the value of performance (e.g. cost)

    returns a 1D list of the optimism-pessimism metric of robustness for each solution
    """

    # Get the optimistic robustness
    optimistic = metric_maximax.calc(performance, maximise)
    
    # Get the pessimistic robustness
    pessimistic = metric_maximin.calc(performance, maximise)

    # Combine the optimistic and pessimistic values
    robustness = []
    for solution in range(len(optimistic)):
        robustness.append(alpha * optimistic[solution] + (1 - alpha) * pessimistic[solution])

    return robustness

if __name__ == "__main__":
    performance = [[0.7, 0.8, 0.9], [0.8, 0.9, 1.0]]
    robustness = calc(performance, 0.5)
    print(robustness)