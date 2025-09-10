import xmltodict # type: ignore
import os
import copy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("directory", help="path of the test directory", type=str)
parser.add_argument("schema", help="path of the xml schema file", type=str)
args = parser.parse_args()

directory: str = args.directory
schema: str = args.schema

with open(schema) as file:
    schema: dict = xmltodict.parse(file.read())

def test_case_representation(filePath: str) -> dict:
    test_representation = {"test": {}}
    test_representation["test"]["metadata"] = {}
    test_representation["test"]["metadata"]["file"] = filePath
    return test_representation

def extract_test_config(file):
    test_case_modele: str = file.split(".")[0]
    test_case_config: list = file.split(".")[1].split("_")
    return test_case_modele,test_case_config

def select_modele(schema, test_representation, test_case_modele):
    for s in schema["root"]["modele"]:
        if s["@name"] == test_case_modele:
            for m in test_case_modele:
                test_representation["test"]["modele"] = copy.deepcopy(s)

def apply_config(test_case_config, test_representation):
    liste_formulations = test_representation["test"]["modele"]["liste_formulations"]["formulation"]
    liste_formulations = liste_formulations if isinstance(liste_formulations, list) else [liste_formulations]
    liste_formulations_filtered = [] 

    for formulation in liste_formulations:
        if formulation["@name"] in test_case_config:
            liste_formulations_filtered.append(formulation)

    test_representation["test"]["modele"]["liste_formulations"]["formulation"] = liste_formulations_filtered

for root, dirs, files in os.walk(directory):
    for file in files:
        test_representation = test_case_representation(os.path.join(root, file))

        if file.endswith(".txt"):
            test_case_modele, test_case_config = extract_test_config(file)

            select_modele(schema, test_representation, test_case_modele)
            apply_config(test_case_config, test_representation)

            print(test_representation)
pass

# TODO: adpat format to match with the "arcane" database schema
# TODO: flatten json
# TODO: send to neo4j