## Available Data Sets:

### Collaboration Distance
- "Collaboration distance" is obtained from a tool on https://mathscinet.ams.org/.
- This distance represents minimumly how many papers away two authors are. For example, if A coauthored a paper with B, but A worked with C, C worked with D, and D worked with B, then the collaboration distance between A and B would be 3 (A-C-D-B). Similarly, collaboration distance between A and C is 1, between A and D is 2.

### Number of Joint Publication
- This data represents how many paper each pair of faculties co-authored.
- This dataset is symmetrical.

### Number of Shared Citation
- This data represents how many times each pair of faculties are cited in the same paper.
- For example, if there are 10 papers that cited both faculty A and B, then entry (A, B) of this dataset would be 10.
- This dataset is symmetrical.

### Number of Directed Citation
- This data represents how many times one faculty cited another faculty in all his/her publications.
- For example, if A cited B 10 times in all of A's publications, then the entry (A, B) would be 10.
- This dataset is NOT symmetrical.

### Number of Common Journal
- This data represents how many papers each pair of faculties published in same journals.
- For example, if A published 3 papers in journal X and 4 papers in journal Y, while B published 2 papers in journal X and 5 papers in journal Y, then entry (A, B) of this dataset would be 3+2+4+5 = 14.
- This dataset is symmetrical.

### Number of Common Reference
- This data represents how many papers each pair of faculties both refered to in their publishings.
- For example, if A refered to paper x, y, z in her papers, and B refered to paper w, x, y in his papers, then entry (A, B) of this dataset would be 2.
- This dataset is symmetrical.

### Citation Matrix
- This data represents how many time for any author has citation(s) for one specific paper.
- For example, if A's paper has been citated by a paper called P. Then in the matrix, cell in the row A and column P has value of 1.
- This dataset is NOT symmetrical. 

### Reference Matrix
- This data represents how many time for any author has reference(s) for one specific paper.
- For example, if A's paper has been referenced by a paper called P. Then in the matrix, cell in the row A and column P has value of 1.
- This dataset is NOT symmetrical. 
