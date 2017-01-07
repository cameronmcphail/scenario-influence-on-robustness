import csv

def read_performance(filepath):
    """Read the performance_values from file for each solution
    
    Returns a 2D list containing reliabilities
        dimension 1 is the solution index
        dimension 2 is the scenario index


    Assumes that the performance in every scenario has already been calculated.
    If the performance hasn't been calculated, that should be done in a 
      separate (model-specific) script.

    Assumes that the file is a csv file (comma delimited)
    """

    # Extract the contents of the csv as a 2D list of strings string
    with open(filepath) as csvfile:
        performance_strings = csv.reader(csvfile)
        strings = []
        for row in performance_strings:
            strings.append(row)


    # Create a list of performance values
    performance = []

    # For each row from the csv file...
    for row in range(len(strings)):
        
        # Create a new row for float (decimal) values
        float_row = []

        # For each column int he row...
        for col in range(len(strings[row])):

            # If it is not the first row or column...
            if row != 0 and col != 0:
                
                # Add the value from the column to the float_row
                float_row.append(float(strings[row][col]))

        if len(float_row) > 0:
            performance.append(float_row)

    return performance


def calculate_robustness_change(metric, performance, maximise=True):
    """ Calculate the robustness for a given metric when one scenario is removed
    
    metric is a metric function
    performance is a 2D list with:
        dimension 1 is the solution index
        dimension 2 is the scenario index
    maximise is true if a higher value represents a better performance

    returns a 2D list of robustness values for the given metric
        dimension 1 is the scenario that was removed
        dimension 2 is the solution index

    Removes each scenario one at a time and recalculates robustness
    """
    
    n_solutions = len(performance)
    n_scenarios = len(performance[0])

    # Create a 2D list with the values of robustness when each scenario is removed
    robustness = []

    # For each scenario...
    for scenario_to_remove in range(n_scenarios):

        # Create a new list of performance values that will exclude scenario_to_remove
        new_performance = []

        # For each solution...
        for solution_idx in range(n_solutions):
            
            # Create a list of solution performance values that exclude scenario_to_remove
            new_solution_performance = []

            # For each scenario...
            for scenario_idx in range(n_scenarios):

                # If the scenario_idx is not being removed...
                if scenario_idx != scenario_to_remove:
                    new_solution_performance.append(performance[solution_idx][scenario_idx])

            # Add the solution performance to the list of all performance
            new_performance.append(new_solution_performance)

        # Calculate the robustness 
        robustness.append(metric(new_performance, maximise=maximise))

    return robustness


def calculate_change(original_value, new_value):
    """ Calculates the percentage change (as a proportion) of the original value to the new value

    original_value is the original value
    new_value is the new/altered value
    
    returns the percentage change (as a proportion)
    (positive if new_value is higher than original_value and negative if new_value is lower)
    """
    return 0 if original_value == 0 and new_value == 0 else float('inf') if original_value == 0 else (new_value - original_value) / original_value


def calculate_influence(original_robustness, influenced_robustness):
    """ Calculates the influence of each scenario by comparing the original robustness values and the influenced values

    original_robustness is a 1D list of robustness values where each index is the solution index
    influenced_robustness is a 2D list of robustness values with:
        dimension 1 is the index of the scenario that was removed
        dimension 2 is the solution index

    returns a 2D list with the influence of each scenario (measured as a proportional change in robustness)
        dimension 1 is the index of the scenario that was removed
        dimension 2 is the solution index
    """
    
    n_scenarios = len(influenced_robustness)
    n_solutions = len(influenced_robustness[0])

    # Create a list of the influence for each scenario that is removed and for each solution
    influence = []

    # For each scenario that is removed...
    for scenario_idx in range(n_scenarios):
        # Create a list of influence values
        influence_on_each_solution = []

        # For each solution...
        for solution_idx in range(n_solutions):
            influence_on_each_solution.append(
                calculate_change(original_robustness[solution_idx], influenced_robustness[scenario_idx][solution_idx])
            )

        # Add the influence from this scenario to the list of influences from all scenarios
        influence.append(influence_on_each_solution)

    return influence


def calculate_sensitivity(metric, performance_filepath, maximise=True):
    """ Calculates the sensitivity of the given robustness metric to the individual scenarios

    metric is a robustness metric function
    performance_filepath is a path to the (comma delimited) file that contains the performance values
    maximise is true if a higher value represents a better performance

    returns a 2D list with the influence of each scenario
        dimension 1 is the scenario index
        dimension 2 is the solution index
    """

    # Read the performance values
    performance = read_performance(performance_filepath)

    # Calculate the robustness when all scenarios are included
    original_robustness = metric(performance, maximise)

    # Calculate the robustness as each scenario is removed
    influenced_robustness = calculate_robustness_change(metric, performance, maximise)

    # Calculate the influence of each metric on the robustness
    influence = calculate_influence(original_robustness, influenced_robustness)

    return { 
        "influence": influence,
        "robustness": original_robustness
    }