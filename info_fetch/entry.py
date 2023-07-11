import utilities as u
#import common_references as c
#import paperinfo as p

#1. read file (list of author txt file)
#1.5 function auto correct name (integrated)
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
        names[i] = u.get_author_name(names[i])
    return names

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


if __name__ == "__main__":
    filename = input('Please Put the filename which contains the authors name\n')
    try:
        authorname = get_names(filename)
        print(authorname)
        #for name in authorname:
            #print(fetch_author_info(name))  
            #print(fetch_paper_info(name))
    except FileNotFoundError:
        print("File Not found")





