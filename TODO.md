# TODO

A list of this project's planned, in-progress, and completed tasks.

# ACTIVE

# BACKLOG

- [ ] Investigate if sample code for basic metrics (e.g., spend over n days / period) is available, or if this will need to be produced.
- [ ] Add comments to .env.example or add a README.md section on where to generate credentials 
- [ ] Improve obtain_access_token with print statements to make the process clearer to the end-user.
- [ ] Create a script which checks if the user has created a .env file (useful for setup)
- [ ] Tidy up type annotations
- [ ] add a multiline comments (above functions which require it) that explain each function
- [ ] refactor fetch_transactions to provide options on what period to fetch transactions for

# DONE

- [x] Added basic authentication code
- [x] Refactor basic authentication code into a dedicated function
- [x] Create a simple function which shows which obtains my account list.
- [x] implement a method to obtain access code from monzo redirect url which minimises user interaction
- [x] Implement a local SQLite database for persistent storage of authentication tokens
- [x] Implement an access token handler