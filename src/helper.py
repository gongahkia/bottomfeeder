import json


def unsafe_write_json(data, target_filepath):
    """
    indiscriminately write json data to the specified filepath
    without checking whether a file already exists
    """
    with open(target_filepath, "w") as json_file:
        json.dump(data, json_file, indent=4)


def check_true_number(input_array):
    """
    returns number of unique items in an array
    """
    return len(set(input_array))


# add a python function to remove html artifcats from text and have a nice string

# add a python function to strip strings of :
