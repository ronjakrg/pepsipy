#!/usr/bin/python3

__author__ = "Lukasz Pawel Kozlowski"
__email__  = "lukaszkozlowski.lpk@gmail.com"
__copyrights__ = "Institute of Informatics, University of Warsaw, Poland"

import sys
import os
import numpy as np
import itertools
from math import factorial
from ipc2_lib.ipc import predict_isoelectric_point

def author_information(msg):
    '''add information about Authors'''
    print( '==================================================================================================================\n' )
    print( '\t\t\t\t\tIPC 2.0 - Isoelectric Point Calculator' )
    print( msg )
    print( 'WEB SERVER: \thttp://www.ipc2-isoelectric-point.org\t')
    print( 'LICENSE: \tPUBLIC DOMAIN\t' )    
    print( 'AUTHOR: \t%s (%s)'%(__author__, __email__))
    print( 'VERSION: \t2.0 (pI and pKa with SVR & deep learning)\n' )   
    print( '''HOW TO CITE:\t(1) Kozlowski LP 'IPC 2.0 - prediction of isoelectric point and pKa dissociation constants' 
\t\tNucleic Acids Res. 2021; 49 (W1): W285–W292, doi: 10.1093/nar/gkab295 \n''' )
    print( '''\t\t(2) Kozlowski LP 'IPC – Isoelectric Point Calculator' Biology Direct 2016; 11:55. 
\t\tdoi: 10.1186/s13062-016-0159-9\n''' )    
    print( '==================================================================================================================\n' )   

# 21 aa with 'X' as unknown
aa_letters = ['A', 'C', 'D', 'E', 'F', 
              'G', 'H', 'I', 'K', 'L', 
              'M', 'N', 'P', 'Q', 'R', 
              'S', 'T', 'V', 'W', 'Y', 'X', '0']

aa_alphabet = ''.join(aa_letters)

#441 dipeptides derived from 21 aa
diaa_letters = ['AA', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AK', 'AL', 'AM', 'AN', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AV', 'AW', 'AY', 'AX', 
                'CA', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CV', 'CW', 'CY', 'CX', 
                'DA', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DK', 'DL', 'DM', 'DN', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DV', 'DW', 'DY', 'DX', 
                'EA', 'EC', 'ED', 'EE', 'EF', 'EG', 'EH', 'EI', 'EK', 'EL', 'EM', 'EN', 'EP', 'EQ', 'ER', 'ES', 'ET', 'EV', 'EW', 'EY', 'EX', 
                'FA', 'FC', 'FD', 'FE', 'FF', 'FG', 'FH', 'FI', 'FK', 'FL', 'FM', 'FN', 'FP', 'FQ', 'FR', 'FS', 'FT', 'FV', 'FW', 'FY', 'FX', 
                'GA', 'GC', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GK', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GV', 'GW', 'GY', 'GX', 
                'HA', 'HC', 'HD', 'HE', 'HF', 'HG', 'HH', 'HI', 'HK', 'HL', 'HM', 'HN', 'HP', 'HQ', 'HR', 'HS', 'HT', 'HV', 'HW', 'HY', 'HX', 
                'IA', 'IC', 'ID', 'IE', 'IF', 'IG', 'IH', 'II', 'IK', 'IL', 'IM', 'IN', 'IP', 'IQ', 'IR', 'IS', 'IT', 'IV', 'IW', 'IY', 'IX', 
                'KA', 'KC', 'KD', 'KE', 'KF', 'KG', 'KH', 'KI', 'KK', 'KL', 'KM', 'KN', 'KP', 'KQ', 'KR', 'KS', 'KT', 'KV', 'KW', 'KY', 'KX', 
                'LA', 'LC', 'LD', 'LE', 'LF', 'LG', 'LH', 'LI', 'LK', 'LL', 'LM', 'LN', 'LP', 'LQ', 'LR', 'LS', 'LT', 'LV', 'LW', 'LY', 'LX', 
                'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MI', 'MK', 'ML', 'MM', 'MN', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MV', 'MW', 'MY', 'MX', 
                'NA', 'NC', 'ND', 'NE', 'NF', 'NG', 'NH', 'NI', 'NK', 'NL', 'NM', 'NN', 'NP', 'NQ', 'NR', 'NS', 'NT', 'NV', 'NW', 'NY', 'NX', 
                'PA', 'PC', 'PD', 'PE', 'PF', 'PG', 'PH', 'PI', 'PK', 'PL', 'PM', 'PN', 'PP', 'PQ', 'PR', 'PS', 'PT', 'PV', 'PW', 'PY', 'PX', 
                'QA', 'QC', 'QD', 'QE', 'QF', 'QG', 'QH', 'QI', 'QK', 'QL', 'QM', 'QN', 'QP', 'QQ', 'QR', 'QS', 'QT', 'QV', 'QW', 'QY', 'QX', 
                'RA', 'RC', 'RD', 'RE', 'RF', 'RG', 'RH', 'RI', 'RK', 'RL', 'RM', 'RN', 'RP', 'RQ', 'RR', 'RS', 'RT', 'RV', 'RW', 'RY', 'RX', 
                'SA', 'SC', 'SD', 'SE', 'SF', 'SG', 'SH', 'SI', 'SK', 'SL', 'SM', 'SN', 'SP', 'SQ', 'SR', 'SS', 'ST', 'SV', 'SW', 'SY', 'SX', 
                'TA', 'TC', 'TD', 'TE', 'TF', 'TG', 'TH', 'TI', 'TK', 'TL', 'TM', 'TN', 'TP', 'TQ', 'TR', 'TS', 'TT', 'TV', 'TW', 'TY', 'TX', 
                'VA', 'VC', 'VD', 'VE', 'VF', 'VG', 'VH', 'VI', 'VK', 'VL', 'VM', 'VN', 'VP', 'VQ', 'VR', 'VS', 'VT', 'VV', 'VW', 'VY', 'VX', 
                'WA', 'WC', 'WD', 'WE', 'WF', 'WG', 'WH', 'WI', 'WK', 'WL', 'WM', 'WN', 'WP', 'WQ', 'WR', 'WS', 'WT', 'WV', 'WW', 'WY', 'WX', 
                'YA', 'YC', 'YD', 'YE', 'YF', 'YG', 'YH', 'YI', 'YK', 'YL', 'YM', 'YN', 'YP', 'YQ', 'YR', 'YS', 'YT', 'YV', 'YW', 'YY', 'YX', 
                'XA', 'XC', 'XD', 'XE', 'XF', 'XG', 'XH', 'XI', 'XK', 'XL', 'XM', 'XN', 'XP', 'XQ', 'XR', 'XS', 'XT', 'XV', 'XW', 'XY', 'XX']

ss_letters = ['H', 'E', '-']
acc_letters = ['B', '-']
dis_letters = ['D', '-']
score_letters = [str(n) for n in range(0, 10)]

positive_aa = ['K', 'R']    #1
negative_aa = ['D', 'E']    #-1
aromatic_aa = ['F', 'W', 'H', 'Y']

kd = {  'A': 1.8,'R':-4.5,'N':-3.5,'D':-3.5,'C': 2.5,
        'Q':-3.5,'E':-3.5,'G':-0.4,'H':-3.2,'I': 4.5,
        'L': 3.8,'K':-3.9,'M': 1.9,'F': 2.8,'P':-1.6,
        'S':-0.8,'T':-0.7,'W':-0.9,'Y':-1.3,'V': 4.2, 'X': 0.0 }
        
volume =  {'A': 88.6,  'R': 173.4, 'N': 114.1, 'D': 111.1, 
        'C': 108.5, 'E': 138.4, 'Q': 143.8, 'G': 60.1, 
        'H': 153.2, 'I': 166.7, 'L': 166.7, 'K': 168.6, 
        'M': 162.9, 'F': 189.9, 'P': 112.7, 'S': 89.0, 
        'T': 116.1, 'W': 227.8, 'Y': 193.6, 'V': 140.0, 'X':141.26}

normalized_volume = {'A': 0.1699, 'C': 0.2886, 'D': 0.3041, 'E': 0.4669,
                     'F': 0.774,  'G': 0.0,    'H': 0.5552, 'I': 0.6357,
                     'K': 0.647,  'L': 0.6357, 'M': 0.613,  'N': 0.322,
                     'P': 0.3137, 'Q': 0.4991, 'R': 0.6756, 'S': 0.1723,
                     'T': 0.3339, 'V': 0.4764, 'W': 1.0, 'X': 0.484,  'Y': 0.7961}


mass =  {'A': 71.0788,  'R': 156.1875, 'N': 114.1038, 'D': 115.0886, 
         'C': 103.1388, 'E': 129.1155, 'Q': 128.1307, 'G': 57.0519, 
         'H': 137.1411, 'I': 113.1594, 'L': 113.1594, 'K': 128.1741, 
         'M': 131.1926, 'F': 147.1766, 'P': 97.1167,  'S': 87.0782, 
         'T': 101.1051, 'W': 186.2132, 'Y': 163.176, 'V': 99.1326, 'X':118.886}

normalized_mass = {'A': 0.1086, 'C': 0.3568, 'D': 0.4493, 'E': 0.5579, 'F': 0.6978,
                   'G': 0.0,    'H': 0.6201, 'I': 0.4344, 'K': 0.5506, 'L': 0.4344,
                   'M': 0.574,  'N': 0.4417, 'P': 0.3102, 'Q': 0.5503, 'R': 0.7675,
                   'S': 0.2325, 'T': 0.3411, 'V': 0.3258, 'W': 1.0,    'X': 0.4787, 'Y': 0.8216}

vdWalls = {'A':  67.0, 'R': 148.0, 'N':  96.0, 'D':  91.0, 'C': 86.0, 
           'E': 109.0, 'Q': 114.0, 'G':  48.0, 'H': 118.0, 'I': 124.0, 
           'L': 124.0, 'K': 135.0, 'M': 124.0, 'F': 135.0, 'P': 90.0, 
           'S':  73.0, 'T':  93.0, 'W': 163.0, 'Y': 141.0, 'V': 105.0, 'X': 109.2}

normalized_vdWalls = {'A': 0.1652, 'C': 0.3304, 'D': 0.3739, 'E': 0.5304, 'F': 0.7565, 
                      'G': 0.0,    'H': 0.6087, 'I': 0.6609, 'K': 0.7565, 'L': 0.6609,
                      'M': 0.6609, 'N': 0.4174, 'P': 0.3652, 'Q': 0.5739, 'R': 0.8696,
                      'S': 0.2174, 'T': 0.3913, 'V': 0.4957, 'W': 1.0,    'X': 0.5322, 'Y': 0.8087}

#https://en.wikipedia.org/wiki/Proteinogenic_amino_acid (23.12.2020)
wiki_pI_dict = {'A': 6.01, 'C': 5.05, 'D':  2.85, 'E': 3.15, 
                'F': 5.49, 'G': 6.06, 'H':  7.6,  'I': 6.05, 
                'K': 9.6,  'L': 6.01, 'M':  5.74, 'N': 5.41, 
                'P': 6.3,  'Q': 5.65, 'R': 10.76, 'S': 5.68, 
                'T': 5.6,  'U': 5.47, 'V':  6.0,  'W': 5.89, 
                'Y': 5.64, 'X': 6.0}

pKa_scale = {'Cterm': 3.2, 'D': 3.453,  'E': 4.16, 
             'C': 8.3, 'Y': 10.89, 'H': 6.576, 
             'Nterm': 8.2, 'K': 10.66, 'R':  12}

def fasta_reader(inputFile):
    '''reads fasta file and return table [ [head1, seq1], [head2, seq2], ...]'''
    fasta_lines = open(inputFile).readlines()
    fasta_lines = [n for n in fasta_lines if n[0]!='#']
    fastaTab = ''.join(fasta_lines)
    fastaTab = '\n'+fastaTab
    fastaTab = fastaTab.split('\n>')[1:]
    fastaList = []
    for n in range(0, len(fastaTab)):
        tmp = fastaTab[n].split(os.linesep)
        head = '>'+tmp[0].strip()
        seq = ''.join(tmp[1:])
        fastaList.append([head, seq])
    return fastaList

def state2bin_matrix(state, alphabet=aa_letters):
    ''' convert the state into binary matrix using given alphabet'''
    bin_matrix = []
    for letter in alphabet:
        if state==letter: bin_matrix.append(1)
        else: bin_matrix.append(0)
    return bin_matrix
    
def extract_float_dipeptide_frequencies(ref_seq):
    '''count dipeptides frequencies in float'''
    diaa_matrix_freq = []
    for diaa in diaa_letters:
        diaa_matrix_freq.append(round(ref_seq.count(diaa)/(len(ref_seq)-1), 5))

    return diaa_matrix_freq

def normalize(values, new_min = 0, new_max = 1):
    '''normalize data to given range''' 
    old_min = min(values)
    old_max = max(values)
    old_range = old_max - old_min
    new_range = new_max - new_min
    if old_range ==0: old_range=1
    scale = new_range / old_range
    normalized = [(n - old_min) * scale + new_min for n in values]
    return normalized

def get_hydrophobicity(sequence, window=5):
    '''hydrophobicity according Kyte & Doolittle scale '''
    # Kyte & Doolittle index of hydrophobicity
    max_kd = max(list(kd.values()))
    min_kd = min(list(kd.values()))
    hydrophobicity_tab = [kd[n] for n in sequence]
    smoothed_kd3 = normalize(savitzky_golay(np.asarray(hydrophobicity_tab), 7, 3), min_kd, max_kd)
    smoothed_kd3 = normalize(smoothed_kd3) #[0,1]
    smoothed_kd3 = [round(n,4) for n in smoothed_kd3]
    return smoothed_kd3

def get_charge(sequence):
    '''calculte the charge'''
    # K = R = 1; H=0.5; D = E = -1
    positive_count = sequence.count('K') + sequence.count('R') + (sequence.count('R')/2)
    negative_count = sequence.count('D') + sequence.count('E')
    charge = positive_count - negative_count
    return charge

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError as msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')
