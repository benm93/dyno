# dyno

## Overview

This is a web app built with Python and Fast API.

The user can upload a FASTA file containing several sequences. Then, the user can enter a search query in the form of a string of nucleotides and the application will return the names of the sequences containing that query string.

The user can specify the max distance for this search. This is the maximum Hamming Distance that will be still be considered a match between the query string and a matching region of a sequence. Set max_distance to 0 in order to only accept exact matches. 

This application is packaged and deployed using Docker, Github Actions, and Amazon ECS.

## Scope
Due to time constraints, I chose to leave out several components:
- Domain name / SSL certificate setup in Route 53
- Load balancer
- Database
- Database cache

## Notes
- Run ```conda env create -f environment.yml``` in order to 
create the environment. Then run ```conda activate dyno```.
- Update environment after environment.yml changes by running ```conda env update --file environment.yml --prune```
- Run in dev mode ```fastapi dev backend/api.py```
- Run production:  ```fastapi run backend/api.py --port 80```
- Run tests with ```python -m unittest discover -s ./backend -p "test_*.py"```
- Navigate to ```{Web App IP Address}/logs``` to see the API Documentation.