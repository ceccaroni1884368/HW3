# HW3
 Homework 3 - ADM


 * `collector.py`: a python file that contains the line of code needed to collect your data from the `html` page (from which you get the urls) and Wikipedia.
 * `collector_utils.py`: a python file that stores the function you used in `collector.py`.
 * `parser.py`: a python file that contains the line of code needed to parse the entire collection of `html` pages and save those in `tsv` files.
 * `parser_utils.py`: a python file that gathers the function you used in `parser.py`.
 * `index.py`: a python file that once executed generate the indexes of the Search engines.
 * `index_utils.py`: a python file that contains the functions you used for creating indexes.
 * `utils.py`: a python file that gather functions you need in more than one of the previous files like (`collector`, `parser`, etc.)
 * `main.py`: a python file that once executed build up the search engine. This file is very important because it is going to be the one you will launch during the exam, ideed you will perform live queries on your search engine. In order to let everything go the best, you have to be sure that the engine will work on pre-computed indeces. Thus, **forget to allow the main file to build the index from scratch**. When the user executes the file it should be able to choose:
 	* `search_engine`: a parameter that the user set to choose the search engine to run. According to the request of the homework, you can get 1,2 or 3.
 	* Any other parameters you would like.
 * `exercise_4.py`: python file that contains the implementation of the algorithm that solves problem 4.

 * `main.ipynb`: a Jupyter notebook
