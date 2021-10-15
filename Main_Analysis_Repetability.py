import os
from inverse_kinematics_SSS import inverse_kinematics_SSS as inverse_kinematics_SSS

list_static = ["P10a.c3d", "P10b.c3d"]
list_dynamic = ["P10b.c3d", "P10a.c3d"]

data_repertory = 'data'

# This list is used in order to rewrite the subject metadata without accent and allow the text to be utf8 compatible
# Only the common accent have been taken into account.

for name_static, name_dynamic in zip(list_static, list_dynamic):
    filename_static = os.path.join(
        '.', data_repertory, name_static)
    filename_dynamic = os.path.join(
        '.', data_repertory, name_dynamic)
    inverse_kinematics_SSS(filename_static, filename_dynamic)
