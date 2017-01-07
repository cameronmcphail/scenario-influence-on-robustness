import metric_maximin
import metric_maximax
import metric_optimism_pessimism
import metric_insufficient_reason
import metric_starrs_domain

def calc_all(performance, threshold, maximise=True):
    """Returns the robustness values for a variety of metrics

    'performance' is a 2D list of the performance metric used to
        evaluate each solution in each scenario
        dimension 1 is the solution index
        dimension 2 is the scenario index

    returns an list of class instances which include the name of the metric
     and the value of the robustness metric for each solution:
    [
        .name = "Metric 1 name"
        .robustness = [<1D list>],

        .name = "Metric 2 name"
        .robustness = [<1D list>]
    ]
    """

    class robustnessMetric:
        """Contains the name and values or a robustness metric"""
        def __init__(self, name, robustness):
            self.name = name
            self.robustness = robustness

    robustness = []
    robustness.append(robustnessMetric("Maximin", maximin.calc(performance, maximise)))
    robustness.append(robustnessMetric("Maximax", maximax.calc(performance, maximise)))
    robustness.append(robustnessMetric("Optimism-Pessimism", optimism_pessimism.calc(performance, 0.5, maximise)))
    robustness.append(robustnessMetric("Principle of Insufficient Reason", insufficient_reason.calc(performance)))
    robustness.append(robustnessMetric("Starr's Domain Criterion", starrs_domain.calc(performance, 0.95, maximise)))
    
    return robustness

if __name__ == "__main__":
    performance = [[0.7, 0.8, 0.9], [0.8, 0.9, 1.0]]
    robustness = calc_all(performance, 0.95)
    for metric in robustness:
        print(metric.name, metric.robustness)