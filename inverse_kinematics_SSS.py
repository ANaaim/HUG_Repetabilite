import numpy as np
import os
import ezc3d
import time

import Kinetics_LBMC as lbmc

from full_segment_to_c3d import full_segment_to_c3d
from segment_generation import segment_generation as segment_generation


def inverse_kinematics_SSS(name_static, name_dynamic,name_export):

    # Extraction du c3d
    acq_static = ezc3d.c3d(name_static)
    # Point ind name extraction
    points_names_static = acq_static['parameters']['POINT']['LABELS']['value']
    # Extraction du c3d
    acq_dynamic = ezc3d.c3d(name_dynamic)
    # Point ind name extraction
    points_names_dynamic = acq_dynamic['parameters']['POINT']['LABELS']['value']

    # TODO Check the unit in the C3D files
    points_static = lbmc.points_treatment(
        acq_static, 10, unit_point='mm')
    points_dynamic = lbmc.points_treatment(
        acq_dynamic, 10, unit_point='mm')

    [Rsegment_foot_static, Rsegment_tibia_static, Rsegment_thigh_static,
     segment_pelvis_static,
     Lsegment_thigh_static, Lsegment_tibia_static, Lsegment_foot_static,
     Rname_foot, Rname_tibia, Rname_thigh,
     name_pelvis,
     Lname_thigh, Lname_tibia, Lname_foot] = segment_generation(points_static, points_names_static)

    [Rsegment_foot_dynamic, Rsegment_tibia_dynamic, Rsegment_thigh_dynamic,
     segment_pelvis_dynamic,
     Lsegment_thigh_dynamic, Lsegment_tibia_dynamic, Lsegment_foot_dynamic,
     Rname_foot, Rname_tibia, Rname_thigh,
     name_pelvis,
     Lname_thigh, Lname_tibia, Lname_foot] = segment_generation(points_dynamic, points_names_dynamic)
    # Definition of the parameter using the static
    R_segment_foot_final = lbmc.Segment.fromSegment(
        Rsegment_foot_dynamic, segment_static=Rsegment_foot_static)
    R_segment_tibia_final = lbmc.Segment.fromSegment(
        Rsegment_tibia_dynamic, segment_static=Rsegment_tibia_static)
    R_segment_thigh_final = lbmc.Segment.fromSegment(
        Rsegment_thigh_dynamic, segment_static=Rsegment_thigh_static)
    segment_pelvis_final = lbmc.Segment.fromSegment(
        segment_pelvis_dynamic, segment_static=segment_pelvis_static)
    L_segment_thigh_final = lbmc.Segment.fromSegment(
        Lsegment_thigh_dynamic, segment_static=Lsegment_thigh_static)
    L_segment_tibia_final = lbmc.Segment.fromSegment(
        Lsegment_tibia_dynamic, segment_static=Lsegment_tibia_static)
    L_segment_foot_final = lbmc.Segment.fromSegment(
        Lsegment_foot_dynamic, segment_static=Lsegment_foot_static)

    # Joint model definition
    LAnkle_joint_S = lbmc.spherical_model(Lsegment_tibia_static, Lsegment_foot_static,
                                          Lsegment_tibia_static.rd, Lsegment_foot_static.rp)

    LKnee_joint_S = lbmc.spherical_model(Lsegment_thigh_static, Lsegment_tibia_static,
                                         Lsegment_thigh_static.rd, Lsegment_tibia_static.rp)

    LHip_joint_S = lbmc.spherical_model(segment_pelvis_static, Lsegment_thigh_static,
                                        Lsegment_thigh_static.rp, Lsegment_thigh_static.rp)

    RHip_joint_S = lbmc.spherical_model(Rsegment_thigh_static, segment_pelvis_static,
                                        Rsegment_thigh_static.rp, Rsegment_thigh_static.rp)

    RKnee_joint_S = lbmc.spherical_model(Rsegment_tibia_static, Rsegment_thigh_static,
                                         Rsegment_tibia_static.rp, Rsegment_thigh_static.rd)

    RAnkle_joint_S = lbmc.spherical_model(Rsegment_foot_static, Rsegment_tibia_static,
                                          Rsegment_foot_static.rp, Rsegment_tibia_static.rd)
    # Alternate model definition
    RKnee_joint_H = lbmc.hinge_model(
        Rsegment_tibia_static, Rsegment_thigh_static)
    RAnkle_joint_U = lbmc.universal_model(
        Rsegment_foot_static, Rsegment_tibia_static, 'u', 'w')

    full_segment = list([R_segment_foot_final, R_segment_tibia_final,
                         R_segment_thigh_final, segment_pelvis_final,
                         L_segment_thigh_final, L_segment_tibia_final,
                         L_segment_foot_final])

    #full_segment = list([R_segment_thigh_final, segment_pelvis_final])
    # This list has been added to be able to rename and replace the marker of the original file.
    full_segment_marker_name = list([Rname_foot, Rname_tibia,
                                     Rname_thigh, name_pelvis,
                                     Lname_thigh, Lname_tibia,
                                     Lname_foot])
    #full_segment_marker_name = list([Rname_foot, Rname_tibia])
    # TODO check if  Pour faire des modèles à branches... il suffit de faire des liaisons 6 dof entre les différents segments? 
    full_model_test = [RAnkle_joint_S, RKnee_joint_S,
                       RHip_joint_S, LHip_joint_S,
                       LKnee_joint_S, LAnkle_joint_S]
    # full_model_test = [RAnkle_joint_U, RKnee_joint_H,
    #                   RHip_joint_S, LHip_joint_S,
    #                   LKnee_joint_S, LAnkle_joint_S]
    #full_model_test = [RHip_joint_S]

    start_time = time.time()
    lbmc.multi_body_optimisation(full_segment, full_model_test)
    final_time = time.time() - start_time
    nb_frame = acq_dynamic['data']['points'].shape[2]
    print("--- %s frames ---" % (nb_frame))
    print("--- %s seconds ---" % (final_time))

    # C3D writing process
    #new_filename = name_dynamic.replace('.c3d', 'invkin.c3d')
    print(name_export)
    full_segment_to_c3d(name_export, acq_dynamic,
                        full_segment, full_segment_marker_name, unit='m')

#     # C3D writing process.-----------------------------------------------------------------
#     nb_frame = acq_dynamic['data']['points'].shape[2]
#     # calcul of the number of point to plot
#     nb_point_to_replace = 0
#     for segment in full_segment:
#         nb_point_to_replace += len(segment.nm_list)
#     # intialisation
#     point_to_replace = np.zeros((4, nb_point_to_replace, nb_frame))
#     name_point_to_replace = []
#     ind_point = 0

#     for ind_segment, segment in enumerate(full_segment):
#         for ind_rm in range(len(segment.nm_list)):
#             name_point_to_replace.append(
#                 full_segment_marker_name[ind_segment][ind_rm])

#             temp = np.dot(
#                 segment.nm_list[ind_rm].T, segment.Q)*1000
#             point_to_replace[0, ind_point, :] = temp[0, :]
#             point_to_replace[1, ind_point, :] = -temp[2, :]
#             point_to_replace[2, ind_point, :] = temp[1, :]
#             ind_point += 1
#     acq_dynamic = ezsnip.replace(
#         acq_dynamic, name_point_to_replace, point_to_replace)
#     # Add the u rp rd w point to the file ----------------------------------------------------
#     point_to_add = np.zeros((4, len(full_segment)*4, nb_frame))
#     name_point_to_add = []
#     for ind_segment, segment in enumerate(full_segment):
#         name_segment = segment.segment_name
#         list_point_to_add = [segment.rp+0.1*segment.u,
#                              segment.rp, segment.rd, segment.rd+0.1*segment.w]
#         list_name = ['u', 'rp', 'rd', 'w']

#         for ind_point, point in enumerate(list_point_to_add):

#             name_temp = list_name[ind_point] + '_'+name_segment
#             name_point_to_add.append(name_temp)
#             new_point = np.zeros((4, 1, nb_frame))
#             temp = point * 1000
#             point_to_add[0, ind_segment*4+ind_point, :] = temp[0, :]
#             point_to_add[1, ind_segment*4+ind_point, :] = -temp[2, :]
#             point_to_add[2, ind_segment*4+ind_point, :] = temp[1, :]
#             point_to_add[3, ind_segment*4+ind_point, :] = 1

#     acq_dynamic = ezsnip.add(acq_dynamic, name_point_to_add, point_to_add)

#     # Here we remove unicode and replace them with a value compatible with ezc3d
#     acq_dynamic = ezsnip.correction_unicode_metadata(acq_dynamic, "SUBJECTS")

#     # Snippet of correction for the data when we need to add new point
#     # These parameter need to have the same size as point to be able to write the files
#     acq_dynamic = ezsnip.update_residual_camera_mask(acq_dynamic)

#     # Changing the file name to export the value
#     new_filename = filename_dynamic.replace('.c3d', 'invkin.c3d')
#     print(new_filename)
#     start_time_writing = time.time()
#     acq_dynamic.write(new_filename)
#     final_time_writing = time.time() - start_time_writing
#     print(final_time_writing)
#     # Information about the optimisation time
#     print("--- %s frames ---" % (nb_frame))
#     print("--- %s seconds ---" % (final_time))
#     print("--- %s seconds ---" % (final_time/nb_frame))
#     list_nb_frame.append(nb_frame)
#     list_time.append(final_time)

# # Final information for
# for nb_frame, final_time, filename in zip(list_nb_frame, list_time, list_dynamic):
#     print(filename)
#     print("--- %s frames ---" % (nb_frame))
#     print("--- %s seconds ---" % (final_time))
#     print("--- %s seconds ---" % (final_time/nb_frame))
