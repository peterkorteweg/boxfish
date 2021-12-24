# Scraper

**Dec 2021**

1. Soups: create a reverse lookup: create config based on url and table
   1. ~~Soups: find parent/descendant functions~~
   2. ~~Config: build_rows(config, str1, str2)~~
   3. ~~Soups: test build_rows in steps~~
2. Wiki: <li> lists?
3. Test selenium page (funda)
4. Jupyter: website/config/soups/scrape
5. Update readme
6. Config: add option: concatenate: true/false. If true all data is concatenated in a single list/dataframe/file.
7. Create POC: Funda / Padi / IMDB / NBER
8. Website/soups: error handling
9. Websites: create next page functions. Config: build_next_page(config, href)
10. Websites: pagination: infinity pages. Example without infinity? See Real Python Requests. https://realpython.com/python-requests/
11. Websites: identify what is required for authentication. Examples: Mutual Art





**Project tasks**

1. Docs. Schrijven van project uitleg (zie cookbook)
2. Deployment. Git deployment (tutorial?)



**New code features**

1. Tests cases for PADI, Funda and Narrenschip
2. Module: Tasky. Zie onder.
3. Scripts. Tasky inregelen voor Funda
4. Module. Add logging

6. Other. Review codementor(?) / stackoverflow account



**Recurring**

1. Testing. Check if  all main modules have test functions

2. Documentation. Check if main modules: website and config have Jupyter Notebooks



**Misc**

When to use Non type? Empty dict, empty string.







## New features

1. Tasky
2. Reverse search: config creator




 ### Tasky function 

**Oct 2021**

Lightweight conditional task execution. Task will be executed in case of

I File exists or not exists

II specific time has elapsed

 

If file exists or not exists

Frequency: minute, hour, day, week, month

 

Week/month: choose start item?

Tasky(task=, marker=, file_exists = True, file_not_exists = True, frequency = “M”, multiple = 2)

Difference with scheduler: tasky will not monitor time in the background. It can only act if time has passed. 

Generalization: offer same options as scheduler

 

https://stackoverflow.com/questions/4249542/run-a-task-every-x-minutes-with-windows-task-scheduler

 

Note: task scheduler can deal with computer off

Maybe use 1 batch file with if statements works fine:

Schedule windows task every day

Execute code if file_not exists and monthday>..

 

Final statement: remove files

Or in a single call: 

1 remove old file if necessary (timestamp)

2 check if file exists

3 create file if condition met

Return condition

 

If execute_now() …

 



Older



**Nov 2021**

**Code improvements**

1. ~~Soups: Create sample tables for test function of soups.get_table~~
2. ~~Soups: Create function to cut-and-paste a subset of html text and save it to an html file~~ Nov 2021
3. ~~Jupyter: requests/selenium~~
4. ~~Website: create test functions: get_website, get_data~~Nov 2021
5. Jupyter: website/config/soups/scrape
6. ~~Refactoring: move soups to scrape~~
7. Soups: create a reverse lookup: create config based on url and table
   1. ~~Soups: add base to url: use current url to create full url~~
   2. ~~find: do we want to find navigable strings or only tags?~~
   3. ~~results = find_items_by_string. aitem = find_item_by_string(str)~~
   4. ~~aparent = get_common_parent(aitem1,aitem2)~~
   5. ~~afilter = get_filter(aitem1,aitem2) with afilter dict with keys [elem, class]~~
8. ~~Driver: set defaults values of params in driver instead of config~~~~
9. ~~Config: update/revert (.bak)~~





