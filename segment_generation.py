import numpy as np
from Kinetics_LBMC.utils.norm_vector import norm_vector as norm_vector
from Kinetics_LBMC.Segment import Segment as Segment


def segment_generation(points, points_name):
    points_ind = dict()
    for index_point, name_point in enumerate(points_name):
        points_ind[name_point] = index_point
    # Pelvis
    RASI = points[:, points_ind['RASI'], :]
    LASI = points[:, points_ind['LASI'], :]
    RPSI = points[:, points_ind['RPSI'], :]
    LPSI = points[:, points_ind['LPSI'], :]

    midASIS = points[:, points_ind['midASIS'], :]
    PELVIS_X = points[:, points_ind['PELVIC_X'], :]
    PELVIS_Y = points[:, points_ind['PELVIC_Y'], :]
    PELVIS_Z = points[:, points_ind['PELVIC_Z'], :]

    # Right Leg
    RTHAP = points[:, points_ind['RTHAP'], :]
    RTHAD = points[:, points_ind['RTHAD'], :]
    RTHI = points[:, points_ind['RTHI'], :]
    RKNE = points[:, points_ind['RKNE'], :]
    RKNM = points[:, points_ind['RKNM'], :]

    RHJC = points[:, points_ind['RHJC'], :]
    RFEMUR_X = points[:, points_ind['RFEMUR_X'], :]
    RFEMUR_Y = points[:, points_ind['RFEMUR_Y'], :]
    RFEMUR_Z = points[:, points_ind['RFEMUR_Z'], :]

    # Left Leg
    LTHAP = points[:, points_ind['LTHAP'], :]
    LTHAD = points[:, points_ind['LTHAD'], :]
    LTHI = points[:, points_ind['LTHI'], :]
    LKNE = points[:, points_ind['LKNE'], :]
    LKNM = points[:, points_ind['LKNM'], :]

    LHJC = points[:, points_ind['LHJC'], :]
    LFEMUR_X = points[:, points_ind['LFEMUR_X'], :]
    LFEMUR_Y = points[:, points_ind['LFEMUR_Y'], :]
    LFEMUR_Z = points[:, points_ind['LFEMUR_Z'], :]

    # Right Tibia
    RMED = points[:, points_ind['RMED'], :]
    RTIAD = points[:, points_ind['RTIAD'], :]
    RTIB = points[:, points_ind['RTIB'], :]
    RANK = points[:, points_ind['RANK'], :]

    RKJC = points[:, points_ind['RKJC'], :]
    RTIBIA_X = points[:, points_ind['RTIBIA_X'], :]
    RTIBIA_Y = points[:, points_ind['RTIBIA_Y'], :]
    RTIBIA_Z = points[:, points_ind['RTIBIA_Z'], :]

    # Left Tibia
    LMED = points[:, points_ind['LMED'], :]
    LTIAD = points[:, points_ind['LTIAD'], :]
    LTIB = points[:, points_ind['LTIB'], :]
    LANK = points[:, points_ind['LANK'], :]

    LKJC = points[:, points_ind['LKJC'], :]
    LTIBIA_X = points[:, points_ind['LTIBIA_X'], :]
    LTIBIA_Y = points[:, points_ind['LTIBIA_Y'], :]
    LTIBIA_Z = points[:, points_ind['LTIBIA_Z'], :]

    # Right fOOT
    RHEE = points[:, points_ind['RHEE'], :]
    RVMH = points[:, points_ind['RVMH'], :]
    RTOE = points[:, points_ind['RTOE'], :]
    RSMH = points[:, points_ind['RSMH'], :]
    RFMH = points[:, points_ind['RFMH'], :]

    RAJC = points[:, points_ind['RAJC'], :]
    RFOOT_X = points[:, points_ind['RFOOT_X'], :]
    RFOOT_Y = points[:, points_ind['RFOOT_Y'], :]
    RFOOT_Z = points[:, points_ind['RFOOT_Z'], :]

    # Left fOOT
    LHEE = points[:, points_ind['LHEE'], :]
    LVMH = points[:, points_ind['LVMH'], :]
    LTOE = points[:, points_ind['LTOE'], :]
    LSMH = points[:, points_ind['LSMH'], :]
    LFMH = points[:, points_ind['LFMH'], :]

    LAJC = points[:, points_ind['LAJC'], :]
    LFOOT_X = points[:, points_ind['LFOOT_X'], :]
    LFOOT_Y = points[:, points_ind['LFOOT_Y'], :]
    LFOOT_Z = points[:, points_ind['LFOOT_Z'], :]

    # Definition
    u_pelvis = norm_vector(PELVIS_X-midASIS)
    w_pelvis = norm_vector(PELVIS_Z-midASIS)
    rp_pelvis = midASIS
    rd_pelvis = midASIS-(PELVIS_Y-midASIS)
    rm_pelvis = [RASI, LASI, RPSI, LPSI]
    name_pelvis = ['RASI', 'LASI', 'RPSI', 'LPSI']

    # Thigh definition
    Ru_thigh = norm_vector(RFEMUR_X-RHJC)
    Rrp_thigh = RHJC
    Rrd_thigh = RKJC
    Rw_thigh = norm_vector(RFEMUR_Z-RHJC)
    Rrm_thigh = [RTHAP, RTHAD, RTHI, RKNE, RKNM]
    Rname_thigh = ['RTHAP', 'RTHAD', 'RTHI2', 'RKNE', 'RKNM']

    Lu_thigh = norm_vector(LFEMUR_X-LHJC)
    Lrp_thigh = LHJC
    Lrd_thigh = LKJC
    Lw_thigh = norm_vector(LFEMUR_Z-LHJC)
    Lrm_thigh = [LTHAP, LTHAD, LTHI, LKNE, LKNM]
    Lname_thigh = ['LTHAP', 'LTHAD', 'LTHI2', 'LKNE', "LKNM"]

    # Tibia
    Ru_tibia = norm_vector(RTIBIA_X-RKJC)
    Rrp_tibia = RKJC
    Rrd_tibia = RAJC
    Rw_tibia = norm_vector(RTIBIA_Z-RKJC)
    Rrm_tibia = [RMED, RTIAD, RTIB, RANK]
    Rname_tibia = ['RMED', 'RTIAD', 'RTIB2', 'RANK']

    Lu_tibia = norm_vector(LTIBIA_X-LKJC)
    Lrp_tibia = LKJC
    Lrd_tibia = LAJC
    Lw_tibia = norm_vector(LTIBIA_Z-LKJC)
    Lrm_tibia = [LMED, LTIAD, LTIB, LANK]
    Lname_tibia = ['LMED', 'LTIAD', 'LTIB2', 'LANK']

    # Foot
    Ru_foot = norm_vector(RFOOT_X-RAJC)
    Rrp_foot = RAJC
    Rrd_foot = RSMH
    Rw_foot = norm_vector(RFOOT_Z-RAJC)
    Rrm_foot = [RHEE, RVMH, RTOE, RSMH, RFMH]
    Rname_foot = ['RHEE', 'RVMH', 'RTOE', 'RSMH', 'RFMH']

    Lu_foot = norm_vector(LFOOT_X-LAJC)
    Lrp_foot = LAJC
    Lrd_foot = LSMH
    Lw_foot = norm_vector(LFOOT_Z-LAJC)
    Lrm_foot = [LHEE, LVMH, LTOE, LSMH, LFMH]
    Lname_foot = ['LHEE', 'LVMH', 'LTOE', 'LSMH', 'LFMH']

    segment_pelvis = Segment(u_pelvis, rp_pelvis, rd_pelvis, w_pelvis, rm_pelvis,
                             'Buv', 'Bwu',
                             'Pelvis', rigid_parameter=True)
    Rsegment_thigh = Segment(Ru_thigh, Rrp_thigh, Rrd_thigh, Rw_thigh, Rrm_thigh,
                             'Buv', 'Buw',
                             'RThigh', rigid_parameter=True)
    Rsegment_tibia = Segment(Ru_tibia, Rrp_tibia, Rrd_tibia, Rw_tibia, Rrm_tibia,
                             'Buv', 'Buw',
                             'RTibia', rigid_parameter=True)
    Rsegment_foot = Segment(Ru_foot, Rrp_foot, Rrd_foot, Rw_foot, Rrm_foot,
                            'Buw', 'Bwu',
                            'RFoot', rigid_parameter=True)
    # on inverse rp et rd ici pour pouvoir faire une chaine cinématique
    Lsegment_thigh = Segment(Lu_thigh, Lrp_thigh, Lrd_thigh, Lw_thigh, Lrm_thigh,
                             'Buv', 'Buw',
                             'LThigh', rigid_parameter=True)
    Lsegment_tibia = Segment(Lu_tibia, Lrp_tibia, Lrd_tibia, Lw_tibia, Lrm_tibia,
                             'Buv', 'Buw',
                             'LTibia', rigid_parameter=True)
    Lsegment_foot = Segment(Lu_foot, Lrp_foot, Lrd_foot, Lw_foot, Lrm_foot,
                            'Buw', 'Bwu',
                            'LFoot', rigid_parameter=True)

    return[Rsegment_foot, Rsegment_tibia, Rsegment_thigh, segment_pelvis,
           Lsegment_thigh, Lsegment_tibia, Lsegment_foot,
           Rname_foot, Rname_tibia, Rname_thigh, name_pelvis,
           Lname_thigh, Lname_tibia, Lname_foot]
