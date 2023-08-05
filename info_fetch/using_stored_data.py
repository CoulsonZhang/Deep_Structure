import json
import os

path = os.getcwd()

def read_json_file(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

def get_data(author_id, file):
    data = read_json_file(file)
    
    if data['AuthorID'] == author_id:

        # List of journals with duplicates removed
        journal_names = [paper['Journal_Name'][0] for paper in data['Papers'].values()] #change paper['Journal_Name'][0] to paper['Journal_Name'][1] if you want journal IDs instead of names
        unique_journal_names = list(set(journal_names))
        print('Journals:', unique_journal_names)
        print("\n \n \n")

        # List of coauthors with duplicates removed
        co_authors = [author[0] for paper in data['Papers'].values() for author in paper['Authors'] if author[1] != author_id] #change author[0] to author[1] if you want author IDs instead of names
        unique_co_authors = list(set(co_authors))
        print('Coauthors:', unique_co_authors)
        print("Number of coauthors:", len(unique_co_authors))
        print("\n \n \n")

        # List of references with duplicates removed
        references = [reference for paper in data['Papers'].values() for reference in paper['References']]
        unique_references = list(set(references))
        print('References:', unique_references)
        print("\n \n \n")
        
        # List of years published with duplicates removed
        publication_years = [paper['Publication_Year'] for paper in data['Papers'].values()]
        unique_publication_years = list(set(publication_years))
        print('Publication Years:', unique_publication_years)
        print("\n \n \n")

get_data('1054758', path + '/data/papers/LeditzkyFelix_papers.json')

