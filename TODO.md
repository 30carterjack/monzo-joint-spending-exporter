# TODO

A list of this project's planned, in-progress, and completed tasks.

# ACTIVE

- [ ] Tidy up type annotations (db.py remaining)

# BACKLOG

- [ ] Add comments to .env.example or add a README.md section on where to generate credentials 
- [ ] Improve obtain_access_token with print statements to make the process clearer to the end-user.
- [ ] add multiline comments (above functions which require it) that explain each function

# POTENTIAL FUTURE FEATURES

- [ ] Update fetch_transactions function to allow the end-user to specify what period they would like to fetch transactions for
- [ ] Create additional function(s) that create DataFrames on spend-by-category

# DONE

- [x] Added basic authentication code
- [x] Refactor basic authentication code into a dedicated function
- [x] Create a simple function which shows which obtains my account list.
- [x] implement a method to obtain access code from monzo redirect url which minimises user interaction
- [x] Implement a local SQLite database for persistent storage of authentication tokens
- [x] Implement an access token handler
- [x] create lists of relevant transaction information (e.g., when, where, how much) using list comps
- [x] compile relevant transaction information into a dataframe
- [x] add a basic export to Excel function
- [x] add a function which takes the excel export and applies useful formatting (e.g., autocolumn width, centering of text)
