- Import necessary libraries
    - BeautifulSoup from bs4 for web scraping
    - re for regular expressions, for text pattern searching
    - combinations and permutations from itertools for generating combinations and permutations
    - defaultdict from collections for creating dictionaries with default values
    - requests for sending HTTP requests
    - time for adding delay to prevent server overwhelm
    - ujson for parsing JSON
    - csv for working with CSV files

-  function to get the author's formal name from the link of their profile `get_author_name(name)`
    - Construct the URL
    - Make a GET request to the URL
    - Parse the returned HTML content with BeautifulSoup
    - Locate and return the author's formal name

-  similar function to `get_author_name`, but instead it returns the author's id from the parsed content `get_author_id(name)`
    - Construct the URL
    - Make a GET request to the URL
    - Parse the returned HTML content with BeautifulSoup
    - Extract and return the author's ID from the parsed content

-  function `fetch_citation(url)` to that handles the collection of paper citations
    - Make a GET request to the URL
    - Parse the returned HTML content with BeautifulSoup
    - Cycle through the page 'headlines' to collect various data including title and citation info
    - Check if there is next page using `findnext()` function and recurse if there is

-  function `fetch_title(url)` that fetches the titles from a page
    - Make a GET request to the URL
    - Parse the returned HTML content with BeautifulSoup
    - Extract title info from each 'headline' on the page
    - Recurse through next pages if they exist using the `findnext()` function

-  function `fetch_single_title(url)` that fetches a single paper title from a page
    - Make a GET request to the URL
    - Parse the returned HTML content with BeautifulSoup
    - Extract and return the unique paper title from the parsed content

-  function `find_joint()`
    - Open the JSON file containing the author's paper data
    - Calculate the pairs of authors who have written together using the `combinations()` function
    - Record the number of joint papers for each pair into a dictionary
    - Store the results in a JSON file

-  function `fetch_list()` that reads author names from a text file and fetches their published papers
    - Create a dictionary to hold author's papers
    - For each author, fetch their published papers using the `fetch()` function
    - Record each author's paper data in a JSON file

-  function `search(name)` that prepares the URL for searching
    - Return the constructed URL string

-  function `findnext(url)` that finds the URL of the 'next' button on the webpage
    - Use BeautifulSoup to parse HTML from the input URL
    - Extract and return the 'next' URL

-  function `fetch(url)` that extracts information from an input URL page
    - Follow a similar process as in `fetch_citation` but record different details

-  function `find_citation()`
    - Open the file containing author names
    - Convert the author names into a list
    - For each author name in the list, construct a search URL and fetch the citation data
    - Store the citation data for each author in a dictionary and save it in a JSON file

-  function `citation_joint()`
    - Open the file containing fetched citation data
    - Calculate the number of shared citations between all pairs of authors and store the results in a dictionary
    - Save the resulting dictionary to a JSON file

-  function `citation_directed()`
    - Open the file containing fetched citation data
    - Calculate how many times one author cited another for all pairs of authors
    - Save the resulting dictionary in a JSON file

-  function `citation_joint_name()`
    - Open the file containing fetched citation data
    - For each possible author pair, find and record the list of joint citations
    - Save the resulting dictionary to a file

-  function `make_citation_pool()`
    - Open the file containing fetched citation data
    - For each author, create a list of their cited papers and a set of all their citations
    - Count how many times each author cited each paper
    - Save the resulting dictionary to a JSON file

-  function `make_ref_pool()`
    - Open the CSV file containing reference data
    - Create a dictionary where each author is linked to all their cited paper IDs
    - Calculate the number of times each author made each reference
    - Save the resulting dictionary to a JSON file
