# Pseudocode for utilities.py

**Importing Required Libraries:**
1. Import the BeautifulSoup library for web scraping.
2. Import the `re` module to use regular expressions.
3. Import `combinations` and `permutations` from itertools module.
4. Import the `requests` module for making HTTP requests.
5. Import the `time` module to handle time-related tasks.
6. Import `ujson` for dealing with JSON data.
7. Import `defaultdict` from `collections` to work with default dictionaries.
8. Import `csv` to work with CSV files.

**Function: get_author_name(name)** (Checks author's formal name)
1. Create a URL string using the name.
2. Make a GET request to the URL and get HTML content.
3. Parse HTML content using BeautifulSoup.
4. Find the 'span' tag that has class "authorName important", extract the text, and return it.
5. If the tag was not found, print the name and a warning.

**Function: get_author_id(name)** (Checks author's ID)
1. This function is similar to `get_author_name`, but it extracts an 'id' from a 'title' tag in the HTML content. 

**Function: fetch_citation(url)** (Collects paper citation)
1. Send a GET request to the URL to fetch the HTML content.
2. Parse the HTML content using BeautifulSoup.
3. For each 'div' with class "headline", extract the paper title and citation URL.
4. If the citation text ends with "Citation\n" or "Citations\n", fetch citation data accordingly.
5. After finishing processing all titles on the current page, check if there's a next page. If so, repeat the process for the next page. 

**Function: fetch_title(url)** (Fetches titles on a page)
1. Send a GET request to the URL to fetch the HTML content.
2. Parse the content with BeautifulSoup.
3. Find all 'div' tags with class "headline", and for each tag, fetch the paper title.
4. Repeat this process for the next page if it exists.

**Function: fetch_single_title(url)** (Fetches a single title)
1. This function works similarly to `fetch_title`, but it only fetches a single title.

**Function: find_joint()**
1. Open and load JSON data from a file.
2. Use `combinations` to find all the pairs of authors.
3. For each pair, calculate the intersection of the publications of the two authors and store it in a `joint` dictionary.
4. Write the `joint` dictionary to a JSON file.

**Function: fetch_list()**
1. Open and read a text file containing the names of all authors.
2. For each author name, fetch the publications and store them in a dictionary `result`.
3. Write `result` to a JSON file.

**Function: search(name)**
1. Build a search URL using the name of the author.

**Function: findnext(start)**
1. This function finds the URL for the 'next' button.

**Function: fetch(url)**
1. This function extracts information from the provided URL page. 

**Function: find_citation()**
1. Open and read a text file containing the names of all authors.
2. For each author name, fetch the citations and store them in a dictionary `result`.
3. Write `result` to a JSON file.

**Function: citation_joint()**
1. Load JSON data from a file.
2. Use `combinations` to find all the pairs of authors.
3. For each pair, calculate the intersection of the publications of the two authors and store it in a `joint` dictionary.
4. Write the `joint` dictionary to a JSON file.

**Function: citation_directed()**
1. Load the citation source JSON file.
2. Create dictionary with author as the key and a set of categorized citations as the value.
3. Generate permutations (ordered combinations) for each pair of authors.
4. Calculate how many times one author cites another's works and records this in a dictionary.
5. Write the dictionary into a JSON file.

**Function: citation_joint_name()**
1. This function is a variation of the `citation_joint()` function, but it writes paper titles instead of counts into a JSON file.

**Function: make_citation_pool()**
1. Load the `citations_source.json` file.
2. Create a dictionary with author as key and a set of author's publication as the value.
3. Prepare the logarithmic base of each citation.
4. Store these value in a pool (JSON file). 

**Function: make_ref_pool()**
1. Open and read data from a CSV file.
2. Prepare the logarithmic base of each reference.
3. Store these values in a pool (JSON file).
