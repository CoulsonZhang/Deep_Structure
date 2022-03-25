import utilities as u
import common_references as c

#1. read file (list of author txt file)
#1.5 function auto correct name
#2. Function to get info structure of all authors
#3. Function to get info structure of all papers

#4 generate matrix1
#5 generate matrix2 .....

#1
def get_names(filename):
    with open(filename, 'r') as file:
        data = file.read()
        names = data.split('\n')
    for i in range(len(names)):
        names[i] = auto_correct(names[i])

    return names
#1.5
def auto_correct(name):
    #auto check name in mathscinet website
    pass
#2
def fetch_author_info(name):
    pass

#3
def fetch_paper_info(name):
    u.find_citation()
    pass





