#!/usr/bin/python3

__author__ = "Lukasz Pawel Kozlowski"
__email__  = "lukaszkozlowski.lpk@gmail.com"
__webserver__ = "http://www.ipc2-isoelectric-point.org/"
__license__ = "PUBLIC DOMAIN"

from ipc2_lib.ipc import predict_isoelectric_point
from ipc2_lib.ipc import predict_isoelectric_point_ProMoST
from ipc2_lib.ipc import calculate_molecular_weight
from ipc2_lib.ipc import scales

from keras.models import model_from_json

from ipc2_lib.essentials import get_hydrophobicity
from ipc2_lib.essentials import get_charge
from ipc2_lib.essentials import aa_alphabet, state2bin_matrix, normalize
from ipc2_lib.essentials import aa_letters

import numpy as np
import sys, os, pickle, random

def get_ohe(dataset_tab, flat=1):
    '''Generate features in ohe format from aa sequence'''

    features2d = []   #X
    labels = []     #Y
    for query in dataset_tab:
        single_sequence, score = query
        #print(single_sequence)
        
        if flat==1: 
            features = seq2ohe(single_sequence).flatten().tolist()
        else:
            features = seq2ohe(single_sequence).T.tolist()
            #features = seq2ohe(single_sequence).tolist()
            
        labels.append(score)
        features2d.append(features)
        
    features2d = np.array(features2d)
    labels = np.array(labels)
    
    return features2d, labels

def seq2ohe(tmp_seq):
    '''sequence to ohe'''
    char_to_int = dict((c, i) for i, c in enumerate(aa_alphabet))
    integer_encoded = [char_to_int[char] for char in tmp_seq]
    onehot_encoded = list()
    for value in integer_encoded:
        letter = [0. for _ in range(len(aa_alphabet))]
        letter[value] = 1.
        onehot_encoded.append(letter)   
    #this transpose the matrix and make 22 rows of L (seq length)
    onehot_encoded = np.array(onehot_encoded).T
    return onehot_encoded

def get_ohe2(dataset_tab, flat=1):
    '''Generate features in ohe format from aa sequence'''

    features2d = []   #X
    labels = []     #Y
    for query in dataset_tab:
        single_sequence, score = query
        #print(single_sequence)
        
        if flat==1: 
            features = seq2ohe2(single_sequence).flatten().tolist()
        else:
            features = seq2ohe2(single_sequence).T.tolist()
            #features = seq2ohe(single_sequence).tolist()
            
        labels.append(score)
        features2d.append(features)
        
    features2d = np.array(features2d)
    labels = np.array(labels)
    
    return features2d, labels

def seq2ohe2(tmp_seq):
    '''sequence to ohe'''
    stripped_aa_alphabet = aa_alphabet[:-1]
    char_to_int = dict((c, i) for i, c in enumerate(stripped_aa_alphabet))
    integer_encoded = [char_to_int[char] for char in tmp_seq]
    onehot_encoded = list()
    for value in integer_encoded:
        letter = [0. for _ in range(len(stripped_aa_alphabet))]
        letter[value] = 1.
        onehot_encoded.append(letter)   
    #this transpose the matrix and make 22 rows of L (seq length)
    onehot_encoded = np.array(onehot_encoded).T
    return onehot_encoded

def count_charged_aa(tmp_seq):
    acidic = ['D', 'E', 'C', 'Y']
    basic = ['K', 'R', 'H']
    
    #actually this is better than 'count' in the whole sequence
    N_aa = state2bin_matrix(tmp_seq[0])  
    C_aa = state2bin_matrix(tmp_seq.replace('0', '')[-1]) 
    
    charge_vector = [tmp_seq[1:-1].count('D'), tmp_seq[1:-1].count('E'), 
                     tmp_seq[1:-1].count('C'), tmp_seq[1:-1].count('Y'),
                     tmp_seq[1:-1].count('K'), tmp_seq[1:-1].count('R'), 
                     tmp_seq[1:-1].count('H'),
                     ] + N_aa + C_aa
    return charge_vector

def find_charged(full_seq, seq_nb, tail_len, half_mer):
    charged2pred = ['D','H', 'E', 'Y', 'K']
    val_tab = []
    
    #N-terminus
    current_kmer = full_seq[tail_len-half_mer:tail_len+(half_mer+1)]
    aa = current_kmer[half_mer]
    val_tab.append([current_kmer, [seq_nb, aa, 1]])
    
    #we number aa in from 1 (non-pythonic way), and we omit N and C termini
    for i in range(tail_len+1, len(full_seq)-tail_len-1):
        if full_seq[i] in charged2pred:
            position = i-tail_len+1
            current_kmer = full_seq[i-half_mer:i+half_mer+1]
            aa = full_seq[i]
            val_tab.append([current_kmer, [seq_nb, aa, position]])

    #C-terminus
    current_kmer = full_seq[-(tail_len+half_mer+1):-(tail_len-half_mer)]
    aa = current_kmer[half_mer]
    position = len(full_seq)-tail_len-tail_len
    
    val_tab.append([current_kmer, [seq_nb, aa, position]])
    return val_tab

def get_aaindex(aaindex_file = '../results/aaindex_feature_sel_2020_IPC2_peptide_75.csv'):
    aa_index = open(aaindex_file).readlines()
    aa_index_list = []
    for aa in aa_index:
        foo = aa.strip().split(',')
        name = foo[0]
        #print(foo)
        aa_tab = [float(n) for n in foo[2:]]
        #print(aa_tab)
        # we add X as an average (could be average weighted by % 
        # occurence of amino acids but for simplicity we do not do that
        aa_X = round(sum(aa_tab)/len(aa_tab), 2) 
        aa_tab.append(aa_X)
        aa_tab.append(0)
        
        #we normalize to (0,1)
        aa_tab = normalize(aa_tab)
        
        #AA ordering in AAindex db (X for unknown and 0 for padding)
        # A R N D C Q E G H I L K M F P S T W Y V X 0
        aa_dict = {}
        aa_names = 'A R N D C Q E G H I L K M F P S T W Y V X 0'.split()
        for n in range(0,len(aa_tab)):
            aa_dict[aa_names[n]] = aa_tab[n]            
        aa_index_list.append([name, aa_dict])
    return aa_index_list

def get_ohe_aaIndex(dataset_tab, aaindex_file='../models/aaindex_feature_sel_2020_IPC2_pKa_75.csv'):
     
    #20 features
    aaindex_list = get_aaindex(aaindex_file)
    
    features2d = []   #X
    labels = []     #Y
    for query in dataset_tab:

        single_sequence, score = query
        seq_len = len(single_sequence)
        # features from seq
        features = seq2ohe2(single_sequence).flatten().tolist()
        # features from aaIndex
        for aaindex in aaindex_list:
            for n in range(0, len(single_sequence)):
                features.append(aaindex[1][single_sequence[n]])
        labels.append(score)
        features2d.append(features)
        
    features2d = np.array(features2d)
    labels = np.array(labels)
    
    return features2d, labels

def get_ohe_aaIndex_mix(dataset_tab1, dataset_tab2, aaindex_file='../models/aaindex_feature_sel_2020_IPC2_pKa_75.csv'):
     
    #20 features
    aaindex_list = get_aaindex(aaindex_file)
    features2d = []   #X
    labels = []     #Y
    for n in range(len(dataset_tab1)):
        single_sequence, score = dataset_tab1[n]
        # features from seq
        features = seq2ohe2(single_sequence).flatten().tolist()
        
        single_sequence, score = dataset_tab2[n]
        # features from aaIndex
        for aaindex in aaindex_list:
            for n in range(0, len(single_sequence)):
                features.append(aaindex[1][single_sequence[n]])
        labels.append(score)
        features2d.append(features)
        
    features2d = np.array(features2d)
    labels = np.array(labels)
    
    return features2d, labels

def get_aaIndex_only(dataset_tab, aaindex_file='../models/aaindex_feature_sel_2020_IPC2_pKa_75.csv'):
    
    #20 features
    aaindex_list = get_aaindex(aaindex_file)
    
    features2d = []   #X
    labels = []     #Y
    for query in dataset_tab:

        single_sequence, score = query
        seq_len = len(single_sequence)
        # features from aaIndex
        features = []
        for aaindex in aaindex_list:
            for n in range(0, len(single_sequence)):
                features.append(aaindex[1][single_sequence[n]])
        labels.append(score)
        features2d.append(features)
        
    features2d = np.array(features2d)
    labels = np.array(labels)
    
    return features2d, labels

def get_pKa_MLPs(dataset_tab, models):
    '''runs all MLP needed for SVR for pKa'''
        
    models_pred = []
    #print(len(models), type(models))
    # pretty ugly, but we do not expect different order
    # and we want to avoid loading models multiple times
    kmers_tab = [5,7,9,11,13,15,3,5,7]
    
    for n in range(len(models)):
        #get kmer as needed
        kmers = get_kmers(dataset_tab, kmers_tab[n])
        
        #prepare the input for the model
        if n<6: X_val,   Y_val   = get_ohe2(kmers)
        else: X_val,   Y_val   = get_ohe_aaIndex(kmers)
        
        #finally, make the predictions
        predictions = models[n].predict(X_val)
        xs = [n[0] for n in predictions.tolist()]    
        #print(len(xs), xs[:3])
        models_pred.append(xs)

    #swap rows with columns
    models_pred = np.array(models_pred).T
    
    #print(len(models_pred), len(models_pred[0]))
    #print(models_pred[0])
    return models_pred ,Y_val
    

def get_kmers(dataset, mer):
    tail = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    dataset_tab = []
    half_mer = int((mer-1)/2)
    #pKa,uncertinity,pdb,chain,aa,position,monomer,trimer,pentamer,heptamer,nonamer,sequence
    for line in dataset:
        pKa,uncertinity,pdb,chain,aa,position,monomer,trimer,pentamer,heptamer,nonamer,current_seq = line.split(',')
        exp_pKa = float(pKa)
        current_seq = tail + current_seq.strip() + tail
        kmer = current_seq[int(position)-(half_mer+1)+len(tail):int(position)+half_mer+len(tail)]
        current_seq = kmer.strip().replace('Z', 'Q').replace('U', 'C').replace('B', 'N')
        dataset_tab.append([current_seq, exp_pKa,])
    return dataset_tab
