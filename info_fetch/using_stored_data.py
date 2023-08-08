

import json
import os
import glob
import re

path = os.getcwd()

def read_json_file(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data


def format_author_name(file_name):
    name_with_underscores = os.path.basename(file_name).replace('_papers.json', '')
    # Insert a space before each capital letter to format the name
    formatted_name = re.sub(r"(?<=\w)([A-Z])", r" \1", name_with_underscores)
    return formatted_name

def get_data(author_id, file):
        
    if data['AuthorID'] == author_id:

        # List of journals with duplicates removed
        journal_names = [paper['Journal_Name'][0] for paper in data['Papers'].values() if paper['Journal_Name']] #change paper['Journal_Name'][0] to paper['Journal_Name'][1] if you want journal IDs instead of names
        unique_journal_names = list(set(journal_names))
        #print('Journals:', unique_journal_names)
        print("Number of journals:", len(unique_journal_names))

        # List of coauthors with duplicates removed
        co_authors = [author[0] for paper in data['Papers'].values() for author in paper['Authors'] if author[1] != author_id] #change author[0] to author[1] if you want author IDs instead of names
        unique_co_authors = list(set(co_authors))
        #print('Coauthors:', unique_co_authors)
        print("Number of coauthors:", len(unique_co_authors))

        # List of references with duplicates removed
        references = [reference for paper in data['Papers'].values() for reference in paper['References']]
        unique_references = list(set(references))
        #print('References:', unique_references)
        print("Number of refs", len(unique_references))
            
        # List of years published with duplicates removed
        publication_years = [paper['Publication_Year'] for paper in data['Papers'].values()]
        unique_publication_years = list(set(publication_years))
        print('Publication Years:', unique_publication_years)
        print("\n ")


with open(path + "/data/author_ids.json") as file:
    author_ids = json.load(file)

paper_files = glob.glob(path + '/data/papers/*_papers.json')
for author_name, author_id in author_ids.items(): 
    print(" author name:", author_name, "\n")
    for file in paper_files:
        data = read_json_file(file)
        prof_name = format_author_name(file) 
        get_data(author_id, data)

