from __future__ import division

__author__ = 'flashton'

import os, sys, re
from record_class import PatientRecord
import numpy as np
import matplotlib.pyplot as plt
import pylab
import math


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
        if file.startswith('140'):
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


def find_12h_average(res_dict):

    for file in os.listdir(root_dir):
        if file.startswith('140'):
            with open('%s/%s' % (root_dir, file)) as fi:
                ranges = {(0, 12):[], (13, 24):[], (25, 36):[], (37, 48):[]}
                pat_id = file.split('.')[0]

                for l in fi.readlines():
                    res = re.search('NIMAP', l)
                    if res:


                        hour = int(l.split(',')[0].split(':')[0])
                        nimap = float(l.strip().split(',')[2])

                        for r in ranges:
                            if hour in range(r[0], r[1]):
                                ranges[r].append(nimap)

                bp_window = []

                for r in ranges:
                    if len(ranges[r]) > 0:
                        a = np.array(ranges[r])
                        bp_window.append(int(round(np.median(a))))

                if len(bp_window) == len(ranges):
                    res_dict[pat_id].nimap_window = bp_window

    return res_dict



def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))



def make_distance_matrix(res_dict):
    diff_matrix = {}
    for patient1 in res_dict:
        if len(res_dict[patient1].nimap_window) == 4:
            diff_matrix[patient1] = {}
            for patient2 in res_dict:
                
                if len(res_dict[patient2].nimap_window) == 4:
                    if patient1 != patient2:

                        if patient2 in diff_matrix and patient1 not in diff_matrix[patient2]:
                            #print patient1, res_dict[patient1].nimap_window
                            #print patient2, res_dict[patient2].nimap_window
                            #print angle(res_dict[patient1].nimap_window, res_dict[patient2].nimap_window)
                            diff_matrix[patient1][patient2] = angle(res_dict[patient1].nimap_window, res_dict[patient2].nimap_window)

                    elif patient1 == patient2:
                        diff_matrix[patient1][patient2] = 0                        


    return diff_matrix


def print_matrix(fo, diff_matrix):
    ig_list = [140953, 140734, 140915]
    outhandle = open(fo, 'w')
    outhandle.write('strain1'+"\t"+'strain2'+"\t"+'angle_difference'+"\n") 
    for strain1 in diff_matrix:
        for strain2 in diff_matrix[strain1]:
            if strain1 not in ig_list:
                if strain2 not in ig_list:

                    outhandle.write(strain1+"\t"+strain2+"\t"+str(diff_matrix[strain1][strain2])+"\n") 


#def reshape_matrix(diff_matrix):


def check_matrix(fo):
    res_dict = {}
    inhandle = open(fo)
    
    for line in inhandle.readlines():
        split_line = line.strip().split('\t')
        if split_line[0] in res_dict:
            res_dict[split_line[0]] += 1
        else:
            res_dict[split_line[0]] = 1

        if split_line[1] in res_dict:
            res_dict[split_line[1]] += 1
        else:
            res_dict[split_line[1]] = 1

    for each in res_dict:
        print each, res_dict[each]






res_dict = read_outcomes(outcomes_file, PatientRecord)

#draw_histo(res_dict)

#res_dict = get_blood_pressure_list(root_dir, res_dict)
#res_dict = get_bp_stats(res_dict)

find_12h_average(res_dict)
dm = make_distance_matrix(res_dict)
fo = '/Users/flashton/Dropbox/PyCharm projects/mimic_analysis/data/distance_matrix.txt'
print_matrix(fo, dm)

for each in res_dict:
    if each.startswith('140'):
        print each, res_dict[each].in_hospital_death, res_dict[each].nimap_window

#check_matrix(fo)

#print dm

#box_whisker(res_dict)


