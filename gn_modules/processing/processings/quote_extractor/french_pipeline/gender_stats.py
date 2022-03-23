#!/usr/bin/env python
# coding: utf-8

"""
For now, the quote_extrator and genderization have to be manually launched one after the other.
Both scripts work locally for now.
This current script takes as input the output of genderization.py (a FOLDER of JSON files) and returns a json file where each entry is of the following format:
{
    "doc_id": document_name (string),
    "num_quotes": total number of quotes extracted (int),
    "women_speakers": number of women quoted (int),
    "men_speakers": number of men quoted (int),
    "unknown_speakers": number of speakers of unknown gender (int)
}

PLEASE NOTE: for now there is no distinction between speakers without gender (i.e: organisations, groups of people) and speakers of unknown gender (either that couldn't be resolved by genderization process or that could possibly not fall in the Men/Women category (those two categories can overlap))

TO DO:
- Add mongo database handling
- Build a pipeline for the process quote_extraction > genderization > gender statistcs

"""
import datetime
import getopt
import logging
import os
import sys
import traceback
import json

def get_stats(quotes):
	stats = {}
	n_quotes = len(quotes)
	n_women = 0
	n_men = 0
	n_unknown = 0
	for q in quotes:
		if q["speaker_gender"] == "female":
			n_women += 1
		elif q["speaker_gender"] == "male":
			n_men += 1
		elif q["speaker_gender"] == "unknown":
			n_unknown += 1
	stats = {
		"num_quotes": n_quotes,
		"women_speakers": n_women,
		"men_speakers": n_men,
		"unknown_speakers": n_unknown
		}
	return stats

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hu:p:s:f",["file-path=", "folder-path=", "output-dir="])
		print(opts)
	except getopt.GetoptError:
		print("Please enter a valid command. Use -h for accepted arguments.")
		sys.exit(2)
	file_path = opts[0][1]
	file_prefix = file_path[:-5]
	with open(file_path, 'r') as f:
		loaded = json.load(f)
	stats = get_stats(loaded)
	with open(file_prefix + '_stats.json', 'w') as f:
		json.dump(stats,f)
	

if __name__ == "__main__":
	main()

# main fun
