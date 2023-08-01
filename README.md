# Department's Deep Structure
IGL Spring 2022: Department's Deep Structure


https://ymb.web.illinois.edu/teaching/igl-projects-s22/


## Files

`info_fetch/common_references.py` collects all papers (using their ID on MathSciNet) referenced by each faculty member and stores them as json files in `data/common_references/` (both for individuals in files of the form `{name}_references.json` and all together in `profdict_common_refs_2023.json`). 

`data/common_references/common_references_2023.csv` stores the matrix of common references (i.e. a matrix with rows and columns indexed by faculty members, with the $(i,j)^{th}$ entry being the number of papers referenced by both faculty $i$ and $j$).

`info_fetch/get_coauthors.py` collects, for each faculty member, all coauthors and their MathSciNet ID. Results are stored in `data/dict_of_coauthors.json`.

`info_fetch/get_author_ids.py` collects the MathSciNet ID for each faculty member. Results are stored in `data/dict_of_author_ids.json`. When there are multiple authors with the same name, the author ID has to be corrected by hand.

`info_fetch/get_citations.py` collects, for each faculty member, all papers that have cited their publications. Results are stored as a dictionary for each faculty member in `data/citations/` as  `{name}_citations.json`. The key is the MR number of the paper, and the value is a list of papers (each paper is itself represented as a list with two elements, first the title, second the MR number) that have cited the paper in the key.
