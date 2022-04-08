import utilities as u
import common_references as c
import paperinfo as p

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
    return u.get_author_name(name)
#2
def fetch_author_info(name):
    result = []
    id = u.get_author_id(name)
    result.append(id)
    url = u.search(name)
    titles = u.fetch_title(url)
    result.extend(titles)
    return result


#3
def fetch_paper_info(name):
    return p.paper_info(name)



auto_correct(' Gary J.')


