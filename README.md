# Department's Deep Structure
IGL project: Department's Deep Structure
detailed page:

https://ymb.web.illinois.edu/teaching/igl-projects-s22/

## To Do:
- Make a class for paper record 
> - save all info (paper title, list of author, list of math id, id of journal, last identifiers)
- reference fetch function compatibility
> - trouble: differnt pages have various format in pure string type
> - Current solution: only get those paper that is collected in MathSciNet
- entry integration (all function, class structure may be utilized)
- Auto name correction (search) by MathSciNet engine

## Finished:
- search result page info fetch (paper title, authors' name)
- "next" page url fetch 
- Paper detailed intro page url fetch 
- Paper reference page url fetch
- Joint publication number between any pair of authors

## File
utilities.py stores all completed functions

facilities.txt stores all "formal" name of UIUC math faculties

names.txt stores all name of UIUC math faculties

joint.json stores joint publication number between any pair of authors stored in facilities.txt

Other files are temporary files used during developing



![image](https://github.com/CoulsonZhang/Deep_Structure/blob/main/Image/UIUC_logo.png)
