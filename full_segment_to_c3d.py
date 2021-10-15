
import numpy as np
import ezc3d_snippet


def full_segment_to_c3d(filename, acq, full_segment, full_segment_marker_name, unit='mm'):
    # C3D writing process.-----------------------------------------------------------------
    nb_frame = acq['data']['points'].shape[2]
    # calcul of the number of point to plot
    nb_point_to_replace = 0
    for segment in full_segment:
        nb_point_to_replace += len(segment.nm_list)
    # intialisation
    point_to_replace = np.zeros((4, nb_point_to_replace, nb_frame))
    name_point_to_replace = []
    ind_point = 0

    for ind_segment, segment in enumerate(full_segment):
        for ind_rm in range(len(segment.nm_list)):
            name_point_to_replace.append(
                full_segment_marker_name[ind_segment][ind_rm])

            temp = np.dot(
                segment.nm_list[ind_rm].T, segment.Q)*1000
            point_to_replace[0, ind_point, :] = temp[0, :]
            point_to_replace[1, ind_point, :] = -temp[2, :]
            point_to_replace[2, ind_point, :] = temp[1, :]
            ind_point += 1
    if False:
        acq = ezc3d_snippet.replace(
            acq, name_point_to_replace, point_to_replace)
    else:
        for ind_el, element in enumerate(name_point_to_replace):
            name_point_to_replace[ind_el] = element+'test'
        acq = ezc3d_snippet.add(
            acq, name_point_to_replace, point_to_replace)
    # Add the u rp rd w point to the file ----------------------------------------------------
    point_to_add = np.zeros((4, len(full_segment)*4, nb_frame))
    name_point_to_add = []
    for ind_segment, segment in enumerate(full_segment):
        name_segment = segment.segment_name
        list_point_to_add = [segment.rp+0.0001*segment.u,
                             segment.rp, segment.rd, segment.rd+0.0001*segment.w]
        list_name = ['u', 'rp', 'rd', 'w']

        for ind_point, point in enumerate(list_point_to_add):

            name_temp = list_name[ind_point] + '_'+name_segment
            name_point_to_add.append(name_temp)
            if unit == 'm':
                temp = point * 1000
            else:
                temp = point

            point_to_add[0, ind_segment*4+ind_point, :] = temp[0, :]
            point_to_add[1, ind_segment*4+ind_point, :] = -temp[2, :]
            point_to_add[2, ind_segment*4+ind_point, :] = temp[1, :]
            point_to_add[3, ind_segment*4+ind_point, :] = 1

    acq = ezc3d_snippet.add(
        acq, name_point_to_add, point_to_add)

    # Here we remove unicode and replace them with a value compatible with ezc3d
    #acq = ezc3d_snippet.correction_unicode_metadata(acq, "SUBJECTS")

    # Snippet of correction for the data when we need to add new point
    # These parameter need to have the same size as point to be able to write the files
    acq = ezc3d_snippet.update_residual_camera_mask(acq)

    # Changing the file name to export the value
    acq.write(filename)
