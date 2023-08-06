
""" 
    This is the nester module and provides a function called print_list
    that may or may not include nested list
"""

def print_list(the_list):
    """ This function takes a positional argument called 'the_list', which is any
    Python list (of, possibly, nested lists). Each data item in the provided list
    is (recursively) printed to the screen on its own line. """
    
    for sub_list in the_list:
        if isinstance(sub_list, list):
            print_list(sub_list)
        else :
            print(sub_list)
