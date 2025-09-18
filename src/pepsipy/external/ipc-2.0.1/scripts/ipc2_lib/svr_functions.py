#!/usr/bin/python3

__author__ = "Lukasz Pawel Kozlowski"
__email__  = "lukaszkozlowski.lpk@gmail.com"
__webserver__ = "http://www.ipc2-isoelectric-point.org/"
__license__ = "PUBLIC DOMAIN"

from ipc2_lib.ipc import predict_isoelectric_point
from ipc2_lib.ipc import predict_isoelectric_point_ProMoST
from ipc2_lib.ipc import scales
from ipc2_lib.essentials import pKa_scale

import numpy as np
import sys, pickle

def get_pI_features(dataset_tab):
    '''Generate features in bin and float format from aa sequence'''

    features2d = []   #X
    labels = []     #Y
    
    available_pKa_sets = list(scales.keys())
    available_pKa_sets.sort()
    #print(available_pKa_sets)
    for query in dataset_tab:
        single_sequence, score = query
        features =[]
        for scale in available_pKa_sets:
            tmp_ip = round(predict_isoelectric_point(single_sequence, scale), 5)
            features.append(tmp_ip)
        features.append(round(predict_isoelectric_point_ProMoST(single_sequence), 5))
        labels.append(score)
        features2d.append(features)
    return features2d, labels


def get_pKa_features(dataset_tab):
    '''Generate features for pKa'''

    features2d = []   #X
    labels = []     #Y
    
    available_pKa_sets = list(scales.keys())
    available_pKa_sets.sort()
    for query in dataset_tab:
        monomer, trimer, pentamer, heptamer, pentamer, heptamer, nonamer, exp_pKa = query
        
        #additional information - is it N or C terminal aa
        isN = 0
        isC = 0
        if nonamer.endswith('XXXX'): isC=1
        if nonamer.startswith('XXXX'): isN=1
        if isN==1: continue
        if isC==1: continue
        if monomer!='D': continue
        print(monomer, exp_pKa)
        features =[]
        #print('exp_pKa: '+str(exp_pKa))
        #for scale in available_pKa_sets:
            #if isC==1: tmp_pKa = scales[scale]['Cterm']
            #elif isN==1: tmp_pKa = scales[scale]['Nterm']
            #elif monomer=='D': tmp_pKa = scales[scale]['pKAsp']
            #elif monomer=='E': tmp_pKa = scales[scale]['pKGlu']
            #elif monomer=='C': tmp_pKa = scales[scale]['pKCys']
            #elif monomer=='Y': tmp_pKa = scales[scale]['pKTyr']
            #elif monomer=='H': tmp_pKa = scales[scale]['pk_his']
            #elif monomer=='K': tmp_pKa = scales[scale]['pKLys']
            #elif monomer=='R': tmp_pKa = scales[scale]['pKArg']    
            #features.append(tmp_pKa)
        #features.append(wiki_pI[monomer])
        if isC==1: features.append(pKa_scale['Cterm'])
        elif isN==1: features.append(pKa_scale['Nterm'])
        else: features.append(pKa_scale[monomer])
        labels.append(exp_pKa)
        features2d.append(features)
    #print(features2d[:5], labels[:5])
    #print(zz)
    return features2d, labels
