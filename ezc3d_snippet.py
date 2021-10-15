import numpy as np


def replace(acq, list_name, point_value):
    numbers_of_label_found = 1
    end_of_label_not_found = True
    while end_of_label_not_found:
        new_label_name = 'LABELS'+str(numbers_of_label_found+1)
        if new_label_name in acq['parameters']['POINT'].keys():
            numbers_of_label_found += 1
        else:
            end_of_label_not_found = False
    # Creation of the full list
    full_list_name = acq['parameters']['POINT']['LABELS']['value'].copy()
    for ind_label in range(numbers_of_label_found-1):
        list_temp = acq['parameters']['POINT']['LABELS' +
                                               str(ind_label+2)]['value'].copy()
        full_list_name += list_temp

    # We rewrite the full index to make correspond marker name to the position
    points_ind = dict()
    for index_point, name_point in enumerate(full_list_name):
        points_ind[name_point] = index_point

    for ind_label, name_marker in enumerate(list_name):
        acq['data']['points'][:, points_ind[name_marker],
                              :] = point_value[:, ind_label, :]

    return acq


def add(acq, list_name, point_value):
    numbers_of_label_found = 1
    end_of_label_not_found = True
    while end_of_label_not_found:
        new_label_name = 'LABELS'+str(numbers_of_label_found+1)
        if new_label_name in acq['parameters']['POINT'].keys():
            numbers_of_label_found += 1
        else:
            end_of_label_not_found = False

    full_list_name = acq['parameters']['POINT']['LABELS']['value'].copy()
    for ind_label in range(numbers_of_label_found-1):
        list_temp = acq['parameters']['POINT']['LABELS' +
                                               str(ind_label+2)]['value'].copy()

        full_list_name += list_temp
    # We add point
    # for ind_point, name_point in enumerate(list_name):
    full_list_name += list_name

    acq['data']['points'] = np.append(
        acq['data']['points'], point_value[:, :, :], axis=1)

    # It is possible that we are above the 255 limit for LABELS
    # Integrate multiple value of LABELS

    acq['parameters']['POINT']['LABELS']['value'] = full_list_name[0:255]
    number_of_label_needed = int(len(full_list_name)/255+1)
    for ind_label in range(number_of_label_needed-1):
        # As we have already included the first element it is +1 and +2 instead of +0 and +1
        beg_list = 255*(ind_label+1)
        end_list = 255*(ind_label+2)
        if end_list < len(full_list_name):
            list_temp = full_list_name[beg_list:end_list]
        else:
            list_temp = full_list_name[beg_list:]
        if 'LABELS'+str(ind_label+2) not in acq['parameters']['POINT'].keys():
            acq['parameters']['POINT']['LABELS'+str(ind_label+2)] = {'type': -1,
                                                                     'description': '',
                                                                     'is_locked': False,
                                                                     'value': list_temp}
        else:
            acq['parameters']['POINT']['LABELS' +
                                       str(ind_label+2)]['value'] = list_temp
    return acq


def update_residual_camera_mask(acq):
    """
    This function allow to update automaticly two element of the acq structure that
    need to have the same size as acq['data']['point']
    """
    point_value = acq['data']['points']

    a = acq['data']["meta_points"]["residuals"]
    acq['data']["meta_points"]["residuals"] = np.concatenate(
        (a, np.repeat(a[:, -2:-1, :], point_value.shape[1] - a.shape[1], axis=1)), axis=1)
    a = acq['data']["meta_points"]["camera_masks"]
    acq['data']["meta_points"]["camera_masks"] = np.concatenate(
        (a, np.repeat(a[:, -2:-1, :], point_value.shape[1] - a.shape[1], axis=1)), axis=1)

    return acq


def correction_unicode_metadata(acq, metadata_type):
    list_unicode = {'\udce9': 'e',  # é
                    '\udcea': 'e',  # è
                    '\udce0': 'a',  # à
                    '\udcc9': 'E',  # É
                    }
    for key in acq['parameters'][metadata_type].keys():
        if "value" in acq['parameters'][metadata_type][key]:
            if isinstance(acq['parameters'][metadata_type][key]["value"][0], str):
                for unicode_value in list_unicode.keys():

                    acq['parameters'][metadata_type][key]["value"][0] = acq['parameters'][metadata_type][key]["value"][0].replace(
                        unicode_value, list_unicode[unicode_value])
    return acq
