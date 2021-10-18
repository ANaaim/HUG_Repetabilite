import os
from inverse_kinematics_SSS import inverse_kinematics_SSS as inverse_kinematics_SSS
import itertools

# Define the repertory of the data and the repertory for the export
data_repertory = 'data'
data_repertory_export = 'data_export'

##----------------------------------------------------------------------------------
# Extraction of the file by participant
# List of all files contains in the data repertory
list_file_data = os.listdir(os.path.join('.','data'))
# Extracrion all the participant number for each file
all_number_subject = []
for name_file in list_file_data:
    all_number_subject.append(name_file[1:3])

# Initialize the dictionary containing the files name for each participant
dict_subject = dict()
for ind_subject in set(all_number_subject):
    dict_subject[ind_subject] = list()

# We use the full list of files and we add for the corresponding participant indices 
# the corresponding files
for name_file in list_file_data:
    dict_subject[name_file[1:3]].append(name_file)
##-----------------------------------------------------------------------------------

##-----------------------------------------------------------------------------------
# Multi-body optimisation
for ind_subject in set(all_number_subject):
    # We generate a list of number of files for each participant
    list_number_case = [*range(len(dict_subject[ind_subject]))]
    # We generate a list of all combination possible
    list_combinaison = list(itertools.combinations(list_number_case,2))
    list_lettre = ['a','b','c']
    # for each combination we define the corresponding letter with the former
    # list
    for combinaison in list_combinaison:
        letter_1 = list_lettre[combinaison[0]]
        letter_2 = list_lettre[combinaison[1]]
        filename_1 = os.path.join('.', data_repertory, 'P'+ind_subject+letter_1+'.c3d')
        filename_2 = os.path.join('.', data_repertory, 'P'+ind_subject+letter_2+'.c3d')
        temp_text = letter_1+'vs'+letter_2

        filename_export = os.path.join('.', data_repertory_export, 'P'+ind_subject+temp_text+'.c3d')
        inverse_kinematics_SSS(filename_1, filename_2,filename_export)
##---------------------------------------------------------------------------------------------------
# Extraction des données d'intérets (distance par marqueurs ? )