from __future__ import division

__author__ = 'flashton'

import os, sys, re
from record_class import PatientRecord
import numpy as np
import matplotlib.pyplot as plt
import pylab

root_dir = '/Users/flashton/Dropbox/PyCharm projects/mimic_analysis/data/set_a'
outcomes_file = '/Users/flashton/Dropbox/PyCharm projects/mimic_analysis/data/outcomes'

#for each_file in os.listdir(root_dir):
#    print each_file

def read_outcomes(outcomes_file, PatientRecord):
    res_dict = {}
    with open(outcomes_file) as fi:
        for each in fi.readlines():

            split_line = each.strip().split(',')
            if split_line[0] != 'RecordID':
                patient_record = PatientRecord()
                patient_record.record_id = split_line[0]
                patient_record.in_hospital_death = int(split_line[5])
                patient_record.saps = int(split_line[1])
                patient_record.sofa = int(split_line[2])
                res_dict[split_line[0]] = patient_record

    return res_dict

def draw_histo(res_dict):
    saps_alive = []
    sofa_alive = []
    saps_dead = []
    sofa_dead = []

    for pr in res_dict:
        if res_dict[pr].in_hospital_death == 0:

            saps_alive.append(res_dict[pr].saps)
            sofa_alive.append(res_dict[pr].sofa)

        elif res_dict[pr].in_hospital_death == 1:

            saps_dead.append(res_dict[pr].saps)
            sofa_dead.append(res_dict[pr].sofa)

        #print res_dict[pr].saps[0]

    print saps_alive
    print saps_dead
    #bin =
    #plt.scatter(saps, sofa, c = death)
    #plt.gray()
    plt.hist(sofa_alive, bins=40, histtype='stepfilled', color='b', label='sofa_alive')
    plt.hist(sofa_dead, bins=40, histtype='stepfilled', color='r', alpha = 0.5, label='sofa_dead')
    plt.legend()

    pylab.savefig('/Users/flashton/Dropbox/PyCharm projects/mimic_analysis/results/sofa_saps_death_hist.png')

def get_blood_pressure_list(root_dir, res_dict):

    for file in os.listdir(root_dir):
        with open('%s/%s' % (root_dir, file)) as fi:
            pat_id = file.split('.')[0]
            for l in fi.readlines():
                res = re.search('NIMAP', l)
                if res:
                    res_dict[pat_id].nimap_array.append(float(l.strip().split(',')[2]))
                    #print l.strip().split(',')[2]

    return res_dict
    #print len(res_dict[pat_id].nimap_array)

def get_bp_stats(res_dict):
    for pat_id in res_dict:
        if len(res_dict[pat_id].nimap_array) > 10:
            a = np.array(res_dict[pat_id].nimap_array)
            res_dict[pat_id].nimap_median = np.median(a)
            res_dict[pat_id].nimap_stdev = np.std(a)

    return res_dict

def box_whisker(res_dict):
    m_dead = []
    m_alive = []
    std_dead = []
    std_alive = []

    for pat_id in res_dict:
        if len(res_dict[pat_id].nimap_array) > 10:
            if res_dict[pat_id].in_hospital_death == 0:
                m_alive.append(res_dict[pat_id].nimap_median)
                std_alive.append(res_dict[pat_id].nimap_stdev)

            elif res_dict[pat_id].in_hospital_death == 1:
                m_dead.append(res_dict[pat_id].nimap_median)
                std_dead.append(res_dict[pat_id].nimap_stdev)

    counts, bins, bars = plt.hist([m_dead, m_alive], bins=20, stacked = True, normed=True)

    d, a = counts
    print d
    print a

    prop_a = []
    prop_d = []

    for i, n in enumerate(a):
        total = n + d[i]
        prop_a.append(n / total)
        prop_d.append(d[i] / total)


    print prop_a
    print prop_d
    #x = range(0, len(m))
    #plt.errorbar(x, m, std)
    #plt.hist([prop_a, prop_d], bins = 20, stacked = True)

    pylab.savefig('/Users/flashton/Dropbox/PyCharm projects/mimic_analysis/results/median_bp_hist.png')










res_dict = read_outcomes(outcomes_file, PatientRecord)

#draw_histo(res_dict)

res_dict = get_blood_pressure_list(root_dir, res_dict)

res_dict = get_bp_stats(res_dict)

box_whisker(res_dict)