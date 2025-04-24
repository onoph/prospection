# Python project to automate your prospection process on LinkedIn

# Step 1
- install the dependencies with 
  - pip install -r requirements.txt

# Step 2
- load the data from mantiks and builtwith (see the main_parse_files.py)
- This will parse all the files and store them in a local database (sqlite3)

# Step 3 (optional but recommanded)
- install the chrome plugin (see the readme in the plugin directory)

# Step 4
- Launch the main_add_linkedin_company.py file and just relax :)
- This will add all the companies in your LinkedIn account 
  - it will search for the companies not added (from the local database)
  - it will open the LinkedIn page of the company on your browser (use Chrome, especially if you use the plugin)
  - if you have installed the plugin it will automatically click on "Follow" button (only French supported, but you can easily tune the plugin)
    - With the auto mode -> the company will be assumed to be added (from a database point of view)
  
  - if you have chosen to add the companies manually you will have to press "Y" in the main_add...py file
  
If you want to see how many companies remain to be added, launch main_inspect_db.py 

Warning: this is experimental but did work pretty well for me
You should not try to add too many companies at a time, you could experiment issues