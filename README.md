# IGL Spring 2022: Department's Deep Structure
This repository contains code for the [Illinois Geometry Lab](https://math.illinois.edu/research/igl) project "Department's Deep Structure" from Spring 2022. A description of the project can be found [here](https://ymb.web.illinois.edu/teaching/igl-projects-s22/).

Briefly, the code in this repository collects data about publications by math faculty from [MathSciNet](https://mathscinet.ams.org/mathscinet/index.html) and uses it to cluster the department faculty into research areas using hierarchical clustering. 



## Files
There are two main python scripts that fetch data: `get_publication_data.py` and `get_citations.py`.

- `info_fetch/get_publication_data.py` collects, for each faculty member, all papers published by that faculty member, the journal the paper was published in, the year of publication, the classification codes for that paper, the authors of the paper, and the MathSciNet ID of the paper. The collected data is stored in `data/papers/`. Results are stored as a nested dictionary with the following structure:

    - The root level of the dictionary has keys that are the MathSciNet ID of each faculty member, with values being another dictionary storing all the relevant data for that faculty member.
    - Within the faculty member dictionary, there is a key "AuthorID" that maps to the faculty member's MathSciNet ID, and a "Papers" key that maps to yet another nested dictionary, where each key is a paper ID (e.g., "MR4604472") and each value is a "paper dictionary" storing the information for that paper.
    - Here is what the keys of a "paper dictionary" look like:
        * "Title": The title of the paper.
        * "PaperID": The MathSciNet ID of the paper.
        * "Authors": A list of pairs, where each pair contains an author's name and their MathSciNet ID.
        * "Journal_Name": The name of the journal the paper was published in and the journal ID, as a list.
        * "Publication_Year": The year the paper was published.
        * "References": A list of the MathSciNet IDs of papers that are referenced by the paper in question. If there are no references, this list can be empty.
        * "Codes": The classification codes for the paper.
    - For example: 
    ```json
    {
        "Papers": {
            "MR4195744": {
                "Title": "Long gaps in sieved sets.",
                "PaperID": "MR4195744",
                "Authors": [
                    ["Ford, Kevin", "325647"],
                    ["Konyagin, Sergei", "188475"],
                    ["Maynard, James", "1007204"],
                    ["Pomerance, Carl", "140915"],
                    ["Tao, Terence", "361755"]
                ],
                "Journal_Name": ["J. Eur. Math. Soc. (JEMS)", "5961"],
                "Publication_Year": "2021",
                "References": [
                    "MR4592874",
                    "MR3718451",
                    "MR0148632",
                    "MR2200366",
                    "MR3718451",
                    "MR2647984",
                    "MR0424730",
                    "MR0404173",
                    "MR0447191",
                    "MR1511191",
                    "MR3742457",
                    "MR1512273",
                    "MR1550517",
                    "MR4195744"
                ],
                "Codes": "11N35,(11B05,11N32)"
            },
            "MR4588563": { 
                "Title": "..." }
        }
    }
    ```

    - The classification code for each paper is stored as a single string, so extracting the primary secondary classification codes requires some string manipulation. 

- `info_fetch/get_citations.py` collects, for each faculty member, all papers that have cited their publications. Results are stored as a dictionary for each faculty member in `data/citations/` as  `{name}_citations.json`. The key is the MR number of the paper, and the value is a list of papers (each paper is itself represented as a list with two elements, first the title, second the MR number) that have cited the paper in the key. For example:

```json
{
    "MR4524115": [
        ["Relations among Ramanujan-type congruences II: Ramanujan-type congruences in half-integral weights.", "MR4587277"], 
        ["Congruence relations for\nr\n-colored partitions.", "MR4569268"]
    ],     

    "MR4039543": 
        [...]
```
    
- `info_fetch/using_stored_data.py` shows how to use the data obtained from `get_publication_data.py` for each faculty member to extract relevant information (list of coauthors, list of journals published in, list of papers referenced etc.).

- Before you run either `get_publication_data.py` or `get_citations.py`, make sure to update `credential.py` with your netID and password.

#### Some other files:

- `info_fetch/common_references.py` collects all papers (using their ID on MathSciNet) referenced by each faculty member and stores them as json files in `data/common_references/` (both for individuals in files of the form `{name}_references.json` and all together in `profdict_common_refs_2023.json`). 

- `info_fetch/get_coauthors.py` collects, for each faculty member, all coauthors and their MathSciNet ID. Results are stored in `data/dict_of_coauthors.json`.

* Both `info_fetch/get_coauthors.py` and `info_fetch/common_references.py` are subsumed by `info_fetch/get_publication_data.py`.

- `info_fetch/get_author_ids.py` collects the MathSciNet ID for each faculty member. Results are stored in `data/dict_of_author_ids.json`. When there are multiple authors with the same name, the author ID has to be corrected by hand.

- The folder `Clustering` has code that carries out hierarchical clustering using the collected data and produces dendrograms, one for each distance measure based on publication data collected. There is also code for making consensus trees, which combines the results of clustering using different distance measures.

## Poster

The poster from Spring 2022 is below. 

![image](https://github.com/sujeet-bhalerao/Deep_Structure/blob/main/Image/poster.png)