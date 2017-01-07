import os

#print('Getting ready...')
import influence
#import plot_histograms

import metric_maximax
import metric_maximin
import metric_optimism_pessimism
import metric_insufficient_reason
import metric_starrs_domain

def transpose_2D_list(old_list):
    dim2 = len(old_list)
    dim1 = len(old_list[0])
    new_list = []
    for row in range(dim1):
        new_list.append([])
        for col in range(dim2):
            new_list[row].append(old_list[col][row])
    return new_list

def ensure_directory_exists(directory):
    path = os.path.dirname(directory)
    if not os.path.exists(path):
        os.makedirs(path)

def write_file(filepath, list):
    """Writes a list into a file as a comma delimited text file (csv)
    
    filepath is the path of the file to write
    list is a 2D list of objects

    contents of list are converted to a string
    string is printed to file
    """
    
    # Create a string to write to file
    file_string = ""

    for index in range(len(list[0])):
        file_string += ",Scenario " + str(index + 1)
    file_string += "\n"
    file_string = file_string[1:]

    # For each row in the list...
    for row in list:
        temp_string = ""
        # For each column in the row...
        for col in row:
            # Add the value into the row of strings
            temp_value = "NA" if col == float('inf') else str(col * 100)
            temp_string += "," + temp_value

        # Add the new line character
        file_string += temp_string[1:] + "\n"
    
    ensure_directory_exists(filepath)
    file = open(filepath, mode="w")
    file.write(file_string)
    file.close()

def write_robustness(filepath, names, robustness):
    output_str = ""
    for name in names:
        output_str += "," + name
    output_str += "\n"
    
    n_solutions = len(robustness[0])
    for sol in range(n_solutions):
        sol_str = ''.join("," + str(metric[sol]) for metric in robustness)
        output_str += "Solution " + str(sol + 1) + sol_str + "\n"

    ensure_directory_exists(filepath)
    file = open(filepath, mode="w")
    file.write(output_str)
    file.close()

if __name__ == "__main__":
    input_filepath = "C:\\Users\\mcpha\\Dropbox\\_PhD\\Climate Change Projections\\Reliabilities\\Reliabilities.csv"
    output_filepath = "C:\\Users\\mcpha\\Dropbox\\_PhD\\Climate Change Projections\\Robustness\\"

    metrics = [
        {
            "name": "maximax",
            "function": metric_maximax.calc
        },
        {
            "name": "maximin",
            "function": metric_maximin.calc
        },
        {
            "name": "optimism_pessimism",
            "function": metric_optimism_pessimism.calc
        },
        {
            "name": "insufficient_reason",
            "function": metric_insufficient_reason.calc
        },
        {
            "name": "starrs_domain",
            "function": metric_starrs_domain.calc
        }
    ]

    robustness = []
    metric_names = []
    for metric in metrics:
        print('Calculating influence of ' + metric["name"] + "...")
        rv = influence.calculate_sensitivity(metric["function"], input_filepath)
        influence_values = transpose_2D_list(rv["influence"])
        write_file(output_filepath + "influence_" + metric["name"] + ".csv", influence_values)
        robustness.append(rv["robustness"])
        metric_names.append(metric["name"])

    print('Writing original robustness values...')
    write_robustness(output_filepath + "Robustness.csv", metric_names, robustness)
    #plot_histograms.plot(rv)