import re
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


def sanitise(input_string):
    """
    removes HTML tags and unicode artifacts from a string
    """
    no_html = re.sub(r"<.*?>", "", input_string)
    cleaned_text = re.sub(r"[^\x00-\x7F]+", "", no_html)
    return cleaned_text.strip()


def advanced_strip(input_string, strip_array):
    """
    strips any occurrences of specified strings from an input string
    """
    for item in strip_array:
        while input_string.startswith(item):
            input_string = input_string[len(item) :]
    for item in reversed(strip_array):
        while input_string.endswith(item):
            input_string = input_string[: -len(item)]
    return input_string
