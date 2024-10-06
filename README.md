# Nista - Personalized Stylist

## Project description

Emulates a real personalized stylist, using computer vision, large language models and machine learning.
Packaged into a user friendly application.

- Uses Flask/Python3 for backend
- Uses HTML, CSS, JS for frontend


## Folder structure description

### static

Holds CSS, JS, Image files

### templates

Holds HTML files

### utility

Holds Python scripts that provide additional functionality to the flask server

- ### cv
    - Computer vision utilities (skin tone, race, body ratio detection)

- ### llm
    - Large Language Model utilities
- ### ml
    - Machine Learning Model utilities

### samples
Holds sample clothing images


### .keys (**IMPORTANT, YOU MUST CREATE THIS FILE WHILE CLONING**)

Not added to the repo, contains secret keys
-   first line should contain flask secret key


# Instructions to download and run

1. Clone repo with git or download and extract zip file
2. Set up python virtual environment in root directory
3. Install all dependencies listed in requirements.txt, alternatively run
   `pip install -r requirements.txt` on cmd/powershell
    or `pip3 install -r requirements.txt` on terminal
4. Create .keys file and put a random string in the first line
5. Create latestTrends.txt
6. Run main.py (within virtual environment)