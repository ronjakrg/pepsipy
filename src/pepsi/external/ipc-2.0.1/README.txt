                IPC 2.0 - Isoelectric Point Calculator

WEB SERVER: http://www.ipc2-isoelectric-point.org
LICENSE:    PUBLIC DOMAIN	
AUTHOR:     Lukasz Pawel Kozlowski (lukaszkozlowski.lpk@gmail.com)
            Institute of Informatics, Faculty of Mathematics, Informatics, and 
            Mechanics, University of Warsaw, Warsaw, Poland
FUNDING:    National Science Centre, Poland [2018/29/B/NZ2/01403]
VERSION:    2.0 (pI and pKa prediction with SVR & deep learning)

HOW TO CITE:
(1) Kozlowski LP 'IPC 2.0 - prediction of isoelectric point and pKa dissociation 
constants'. Nucleic Acids Res. 2021; 49 (W1): W285–W292, doi: 10.1093/nar/gkab295

(2) Kozlowski LP 'IPC - Isoelectric Point Calculator' Biology Direct 2016; 11:55. 
doi: 10.1186/s13062-016-0159-9

=======================================================================================
=======================================================================================

The IPC 2.0 software, including the web service, the scripts and the documentation, is 
donated to the public domain. You may therefore freely use it for any legal purpose you 
wish. Nevertheless, deep learning libraries used by web server prediction are 
Tensorflow & Keras which are under Apache and MIT Licenses, respectively.
    
=======================================================================================

Please, report evidence of IPC bugs to the Author:
lukasz[dot]kozlowski[dot]lpk[at]gmail[dot]com

=======================================================================================

Disclaimer of warranty

THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR
IMPLIED, INCLUDING WITHOUT LIMITATION IMPLIED WARRANTIES OF MERCHANTABILITY AND 
FITNESS FOR A PARTICULAR PURPOSE.

=======================================================================================


Brief description of the content

├── datasets        (datasets in csv format)
├── predictions     (results of individual methods in csv format)
├── models          (ML models)
├── scripts         (some scripts used)
└── README.txt      (this file)

=======================================================================================

Datasets:
.
├── IPC2_peptide
│   ├── IPC2_peptide_100.csv
│   ├── IPC2_peptide_25.csv
│   └── IPC2_peptide_75.csv
├── IPC2_pKa
│   ├── IPC2_pKa_100.csv
│   ├── IPC2_pKa_25.csv
│   └── IPC2_pKa_75.csv
└── IPC2_protein
    ├── IPC2_protein_100.csv
    ├── IPC2_protein_25.csv
    ├── IPC2_protein_75.csv
    ├── IPC_protein_100.csv
    ├── IPC_protein_25.csv
    └── IPC_protein_75.csv

The datasets are composed of CSV files with very simple structure:

head ./datasets/IPC2_peptide/IPC2_peptide_100.csv -n 3
exp_pI,sequence
7.928,AAAAAAAAAAAAAAAGAGAGAK
6.418,AAAAAAASFAAEQAGAAALLPLGAAADHHSLYK

or

head ./datasets/IPC2_pKa/IPC2_pKa_100.csv -3
pKa,uncertinity,pdb,chain,aa,position,monomer,trimer,pentamer,heptamer,nonamer,sequence
3.1,0.1,1A2P,C,D,8,D,FDG,TFDGV,NTFDGVA,INTFDGVAD,AQVINTFDGVADYLQTYHKLPDNYITKSEAQALGWVASKGNLADVAPGKSIGGDIFSNREGKLPGKSGRTWREADINYTSGFRNSDRILYSSDWLIYKTTDHYQTFTKIR
3.8,0.1,1A2P,C,D,12,D,ADY,VADYL,GVADYLQ,DGVADYLQT,AQVINTFDGVADYLQTYHKLPDNYITKSEAQALGWVASKGNLADVAPGKSIGGDIFSNREGKLPGKSGRTWREADINYTSGFRNSDRILYSSDWLIYKTTDHYQTFTKIR

There are three files *_100.csv (the complete set), *_75.csv (training set) and
*_25.csv (test set).

All ML is done on the *_75.csv and *_25.csv are used only for final statistics.

---------------------------------------------------------------------------------------

IPC2_protein = IPC2_protein (2,324 proteins; 1,743 train; 581 test)  

The dataset consists of proteins derived from two databases: PIP-DB and SWISS-2DPAGE.
The same protein dataset is used in IPC and IPC 2.0. Average protein size: 387 aa.

---------------------------------------------------------------------------------------
IPC2_peptide (119,092 peptides; 89,319 train; 29,773 test)

The dataset consists of the peptides from HiRIEF high-resolution isoelectric focusing 
experiments from Branca et al. 2014 (6) and Johansson et al. 2019 (49). Merged dataset
from seven independent experiments: 3.7-4.9 (8,713 peptides), 3.7-4.9 (7361 peptide), 
3.7-4.9 (35,595 peptides), 3-10 (23,975), 3-10 (15,000 peptides), 6-11 (36,827 peptides),
6-9 (38,057 peptides). Average peptide size: 14.6 aa. 

---------------------------------------------------------------------------------------

IPC2_pKa (1,337 pKa values, 1,077 train, 260 test)

pKa values from PKAD database (157 proteins). Due to small number of samples the test 
set and training set has been build as follow. 260 pKa values from 34 proteins used in
pKa Rosetta method were selected as test set. The remaining samples from PKAD database 
had been designed to training set.

=======================================================================================

Scripts:

There are three, separate prediction tasks that we try to solve in IPC2:
- isoelectric point of proteins,
- isoelectric point of peptides,
- pKa (acid dissociation constant) of charged amino acids.

To do so, we used a number of ML techniques. From the simplest to the most advanced.
IPC (from 2016) used quite simple approach where optimized pKa using a basin-hopping 
and Henderson-Hasselbach equation have been used. This lead to the first version of IPC.

In IPC2, we utilise more advanced algorithms to go even further with prediction accuracy.

First of all, we replace basin-hopping with differential_evolution as it led to better
solutions (in ./scripts/ipc2_lib/IPC.py those new scales are denoted as IPC2_protein and 
IPC2_peptide). Next, we use support vector regression (SVR) on the methods from IPC 1.0.
This gives another level of the improvement. For peptides, we additionally have a big 
dataset (120k) thus we use deep learning. The final model can be described as Deep 
Separable Convolutional Neural Network Based Regressor. For pKa prediction as we did not 
have pKa methods we first made very simple MLP models based on kmers centered in charged
amino acid and then we use 9 of MLP to build final SVR regressor (so called Multilayer 
Perceptron Ensemble Support Vector Regression; MLP-SVR).


For each task you will find scripts like:
ipc*.py               the training script 
ipc*_predictor.py     the testing script (the one you can use to make predictions)

Note that training scripts may have some 3rd party dependices you need to install.
Moreover, it can be very CPU, RAM and time consuming to retrain the ML models.

On the other hand, the prediction scripts are fast:
1) ipc1_predictor.py - ultra fast (18 methods separately or ALL)
2) ipc2_svr_*_predictor.py (either protein or peptide; at least 10-20x slower 
than ipc1 or MLP models)
3) ipc2_*_predictor.py (deep learning models, either protein, peptide or pKa; even 
slower as the input sequences need to be pre-processed into quite complex way).

Still, all prediction scripts should run in the fractions of second per sequence.

The programs had been developed and tested on:
* Linux Ubuntu 20.04 - OS environment,
* python3 (3.8.5) - programming language,
* sklearn (0.23.2) - used for SVR model and statistics, feature selection, etc.,
* numpy (1.18.5) - used for math,
* scipy (1.5.4) - used for math & stats,
* matplotlib (3.3.3) - used for ploting,
* keras (2.4.3) - frontend used for deep learning,
* tensorflow (2.3.1) - backend used for deep learning.

The GPU support for deep learning is not required, but it can be very useful if you 
want to re-train the models (the deep learning models are quite big thus the training
will require decent machine with multiple CPUs/GPUs and a lot of RAM memory).

There is only CLI (command line interface). No GUI or Windows versions are planed. 

For low-throughput usage, use a webserver.

=======================================================================================

Models:
Can be either *.pickle (SVR) or *.hd5 + *.json (deep learining)

.
├── aaindex_feature_sel_2020_IPC2_peptide_75.csv
├── aaindex_feature_sel_2020_IPC2_pKa_75.csv
├── aaindex_feature_sel_2020_IPC2_protein_75.csv
├── IPC2_peptide_75_SVR_19.pickle
├── IPC2_peptide_IPC2.peptide1320.hdf5
├── IPC2_peptide_IPC2.peptide1320.json
├── ...
├── IPC2_peptide_75_SVR_18.pickle (SVR model for peptides)
└── IPC2_protein_75_SVR_18.pickle (SVR model for protins)

=======================================================================================

Predictions:
Predictions according different methods (csv format) - most of the files can be 
reproduced by ipc2_*_predictor.py scripts (the predictions for some other methods
had been produced manualy as the software is for instance Windows only with GUI). 
All predictions are in unified format:

head IPC_peptide_25_EMBOSS.csv -n3
exp_pI,pred_pI,seq
6.02,6.09677,AAAAAAAAAAVQGG
4.56,4.48198,AAALFANEEEFKK

Note that the summary scores (e.g. RMSD) from ipc*_predictor.py may vary a little bit as
for simplicity the script does not do 10-fold CV (as it has been done in the publication;
obviously, individual isoelectric points provided by the scripts are exact).

=======================================================================================

Some comands to re-create most of the results presented in the paper.

# First, do all predictions with IPC (1.0.1) methods (this is ultra fast)
# Next, run SVR models (this is much slower as an SVR need all predictions from IPC 1.0
# (18 methods)

# At the end, you can re-run all deep learning models.
#
# Finally using calculate_table_stats.py, you can re-calculate all statistics presented 
# in the publication.
#

cd scripts;
python3 ipc1_predictor.py Bjellqvist ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_Bjellqvist.csv;
python3 ipc1_predictor.py Bjellqvist ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_Bjellqvist.csv;
python3 ipc1_predictor.py Bjellqvist ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_Bjellqvist.csv;
python3 ipc1_predictor.py Bjellqvist ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_Bjellqvist.csv;

python3 ipc1_predictor.py DTASelect ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_DTASelect.csv;
python3 ipc1_predictor.py DTASelect ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_DTASelect.csv;
python3 ipc1_predictor.py DTASelect ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_DTASelect.csv;
python3 ipc1_predictor.py DTASelect ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_DTASelect.csv;

python3 ipc1_predictor.py Dawson ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_Dawson.csv;
python3 ipc1_predictor.py Dawson ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_Dawson.csv;
python3 ipc1_predictor.py Dawson ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_Dawson.csv;
python3 ipc1_predictor.py Dawson ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_Dawson.csv;

python3 ipc1_predictor.py EMBOSS ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_EMBOSS.csv;
python3 ipc1_predictor.py EMBOSS ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_EMBOSS.csv;
python3 ipc1_predictor.py EMBOSS ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_EMBOSS.csv;
python3 ipc1_predictor.py EMBOSS ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_EMBOSS.csv;

python3 ipc1_predictor.py Grimsley ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_Grimsley.csv;
python3 ipc1_predictor.py Grimsley ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_Grimsley.csv;
python3 ipc1_predictor.py Grimsley ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_Grimsley.csv;
python3 ipc1_predictor.py Grimsley ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_Grimsley.csv;

python3 ipc1_predictor.py IPC2_peptide ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_IPC2_peptide.csv;
python3 ipc1_predictor.py IPC2_peptide ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_IPC2_peptide.csv;
python3 ipc1_predictor.py IPC2_peptide ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_IPC2_peptide.csv;
python3 ipc1_predictor.py IPC2_peptide ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_IPC2_peptide.csv;

python3 ipc1_predictor.py IPC_peptide ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_IPC_peptide.csv;
python3 ipc1_predictor.py IPC_peptide ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_IPC_peptide.csv;
python3 ipc1_predictor.py IPC_peptide ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_IPC_peptide.csv;
python3 ipc1_predictor.py IPC_peptide ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_IPC_peptide.csv;

python3 ipc1_predictor.py IPC_protein ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_IPC_protein.csv;
python3 ipc1_predictor.py IPC_protein ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_IPC_protein.csv;
python3 ipc1_predictor.py IPC_protein ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_IPC_protein.csv;
python3 ipc1_predictor.py IPC_protein ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_IPC_protein.csv;

python3 ipc1_predictor.py IPC2_protein ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_IPC2_protein.csv;
python3 ipc1_predictor.py IPC2_protein ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_IPC2_protein.csv;
python3 ipc1_predictor.py IPC2_protein ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_IPC2_protein.csv;
python3 ipc1_predictor.py IPC2_protein ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_IPC2_protein.csv;

python3 ipc1_predictor.py Lehninger ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_Lehninger.csv;
python3 ipc1_predictor.py Lehninger ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_Lehninger.csv;
python3 ipc1_predictor.py Lehninger ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_Lehninger.csv;
python3 ipc1_predictor.py Lehninger ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_Lehninger.csv;

python3 ipc1_predictor.py Nozaki ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_Nozaki.csv;
python3 ipc1_predictor.py Nozaki ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_Nozaki.csv;
python3 ipc1_predictor.py Nozaki ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_Nozaki.csv;
python3 ipc1_predictor.py Nozaki ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_Nozaki.csv;

python3 ipc1_predictor.py Patrickios ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_Patrickios.csv;
python3 ipc1_predictor.py Patrickios ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_Patrickios.csv;
python3 ipc1_predictor.py Patrickios ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_Patrickios.csv;
python3 ipc1_predictor.py Patrickios ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_Patrickios.csv;

python3 ipc1_predictor.py ProMoST ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_ProMoST.csv;
python3 ipc1_predictor.py ProMoST ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_ProMoST.csv;
python3 ipc1_predictor.py ProMoST ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_ProMoST.csv;
python3 ipc1_predictor.py ProMoST ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_ProMoST.csv;

python3 ipc1_predictor.py Rodwell ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_Rodwell.csv;
python3 ipc1_predictor.py Rodwell ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_Rodwell.csv;
python3 ipc1_predictor.py Rodwell ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_Rodwell.csv;
python3 ipc1_predictor.py Rodwell ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_Rodwell.csv;

python3 ipc1_predictor.py Sillero ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_Sillero.csv;
python3 ipc1_predictor.py Sillero ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_Sillero.csv;
python3 ipc1_predictor.py Sillero ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_Sillero.csv;
python3 ipc1_predictor.py Sillero ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_Sillero.csv;

python3 ipc1_predictor.py Solomon ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_Solomon.csv;
python3 ipc1_predictor.py Solomon ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_Solomon.csv;
python3 ipc1_predictor.py Solomon ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_Solomon.csv;
python3 ipc1_predictor.py Solomon ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_Solomon.csv;

python3 ipc1_predictor.py Thurlkill ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_Thurlkill.csv;
python3 ipc1_predictor.py Thurlkill ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_Thurlkill.csv;
python3 ipc1_predictor.py Thurlkill ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_Thurlkill.csv;
python3 ipc1_predictor.py Thurlkill ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_Thurlkill.csv;

python3 ipc1_predictor.py Toseland ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_Toseland.csv;
python3 ipc1_predictor.py Toseland ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_Toseland.csv;
python3 ipc1_predictor.py Toseland ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_Toseland.csv;
python3 ipc1_predictor.py Toseland ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_Toseland.csv;

python3 ipc1_predictor.py Wikipedia ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_Wikipedia.csv;
python3 ipc1_predictor.py Wikipedia ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_Wikipedia.csv;
python3 ipc1_predictor.py Wikipedia ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_Wikipedia.csv;
python3 ipc1_predictor.py Wikipedia ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_Wikipedia.csv;

python3 ipc2_peptide_svr_predictor.py ../models/IPC2_peptide_75_SVR_19.pickle ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_IPC2.peptide.svr.19.csv;
python3 ipc2_peptide_svr_predictor.py ../models/IPC2_peptide_75_SVR_19.pickle ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_IPC2.peptide.svr.19.csv;

python3 ipc2_protein_svr_predictor.py ../models/IPC2_protein_75_SVR_19.pickle ../datasets/IPC2_protein/IPC2_protein_25.csv ../predictions/IPC2_protein_25_IPC2.protein.svr.19.csv;
python3 ipc2_protein_svr_predictor.py ../models/IPC2_protein_75_SVR_19.pickle ../datasets/IPC2_protein/IPC2_protein_75.csv ../predictions/IPC2_protein_75_IPC2.protein.svr.19.csv;

python3 ipc2_peptide_dense_1320_predictor.py ../models/IPC2_peptide_IPC2.peptide1320 ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_IPC2.peptide1320.csv;
python3 ipc2_peptide_dense_1320_predictor.py ../models/IPC2_peptide_IPC2.peptide1320 ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_IPC2.peptide1320.csv

python3 ipc2_peptide_dense_19_predictor.py ../models/IPC2_peptide_IPC2.peptide19 ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_IPC2.peptide19.csv
python3 ipc2_peptide_dense_19_predictor.py ../models/IPC2_peptide_IPC2.peptide19 ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_IPC2.peptide19.csv

python3 ipc2_peptide_conv2d_channels_predictor.py ../models/IPC2_peptide_IPC2.peptide.SepConv2D_Adam_selu.selu.selu.64.22_5.50.3_3.400.22x60 ../models/aaindex_feature_sel_2020_IPC2_peptide_75.csv ../models/IPC2_peptide_75_SVR_19.pickle ../datasets/IPC2_peptide/IPC2_peptide_75.csv ../predictions/IPC2_peptide_75_IPC2.peptide.Conv2D.csv
python3 ipc2_peptide_conv2d_channels_predictor.py ../models/IPC2_peptide_IPC2.peptide.SepConv2D_Adam_selu.selu.selu.64.22_5.50.3_3.400.22x60 ../models/aaindex_feature_sel_2020_IPC2_peptide_75.csv ../models/IPC2_peptide_75_SVR_19.pickle ../datasets/IPC2_peptide/IPC2_peptide_25.csv ../predictions/IPC2_peptide_25_IPC2.peptide.Conv2D.csv

python3 ipc2_pKa_dense_ohe_predictor.py 3 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq3.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 5 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq5.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 7 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq7.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 9 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq9.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 11 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq11.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 13 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq13.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 15 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq15.csv;

python3 ipc2_pKa_dense_aaindex_predictor.py 3 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.aaIndex3.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 5 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.aaIndex5.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 7 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.aaIndex7.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 9 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.aaIndex9.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 11 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.aaIndex11.csv;

python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 3 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq3.aaIndex3.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 5 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq5.aaIndex5.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 7 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq7.aaIndex7.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 9 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq9.aaIndex9.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 11 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq11.aaIndex11.csv;

python3 ipc2_pKa_dense_ohe_predictor.py 3 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq3.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 5 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq5.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 7 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq7.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 9 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq9.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 11 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq11.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 13 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq13.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 15 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq15.csv;

python3 ipc2_pKa_dense_aaindex_predictor.py 3 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.aaIndex3.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 5 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.aaIndex5.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 7 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.aaIndex7.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 9 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.aaIndex9.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 11 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.aaIndex11.csv;

python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 3 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq3.aaIndex3.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 5 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq5.aaIndex5.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 7 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq7.aaIndex7.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 9 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq9.aaIndex9.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 11 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq11.aaIndex11.csv;

python3 ipc2_pKa_dense_ohe_predictor.py 3 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.seq3.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 5 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.seq5.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 7 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.seq7.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 9 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.seq9.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 11 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.seq11.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 13 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.seq13.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 15 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.seq15.csv;

python3 ipc2_pKa_dense_aaindex_predictor.py 3 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.aaIndex3.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 5 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.aaIndex5.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 7 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.aaIndex7.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 9 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.aaIndex9.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 11 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.aaIndex11.csv;

python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 3 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.seq3.aaIndex3.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 5 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.seq5.aaIndex5.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 7 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.seq7.aaIndex7.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 9 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.seq9.aaIndex9.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 11 ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.seq11.aaIndex11.csv;

python3 ipc2_pKa_dense_ohe_aaindex_mix_predictor.py 13 5 ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.seq13.aaIndex5.csv;

#python3 ipc2_pKa_svr_predictor.py ../models/IPC2_pKa_75_SVR_9.pickle ../datasets/IPC2_pKa/IPC2_pKa_25.csv ../predictions/IPC2_pKa_25_IPC2.mlp-svr.9.csv

python3 ipc2_pKa_dense_ohe_predictor.py 3  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq3.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 5  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq5.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 7  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq7.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 9  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq9.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 11  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq11.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 13  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq13.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 15  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq15.csv;

python3 ipc2_pKa_dense_aaindex_predictor.py 3  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.aaIndex3.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 5  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.aaIndex5.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 7  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.aaIndex7.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 9  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.aaIndex9.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 11  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.aaIndex11.csv;

python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 3  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq3.aaIndex3.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 5  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq5.aaIndex5.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 7  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq7.aaIndex7.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 9  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq9.aaIndex9.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 11  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq11.aaIndex11.csv;

python3 ipc2_pKa_dense_ohe_predictor.py 3  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq3.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 5  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq5.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 7  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq7.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 9  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq9.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 11  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq11.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 13  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq13.csv;
python3 ipc2_pKa_dense_ohe_predictor.py 15  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq15.csv;

python3 ipc2_pKa_dense_aaindex_predictor.py 3  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.aaIndex3.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 5  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.aaIndex5.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 7  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.aaIndex7.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 9  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.aaIndex9.csv;
python3 ipc2_pKa_dense_aaindex_predictor.py 11  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.aaIndex11.csv;

python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 3  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq3.aaIndex3.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 5  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq5.aaIndex5.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 7  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq7.aaIndex7.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 9  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq9.aaIndex9.csv;
python3 ipc2_pKa_dense_ohe_aaindex_predictor.py 11  ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv  ../predictions/IPC2_pKa_25_Gray_IPC2.seq11.aaIndex11.csv;
python3 ipc2_pKa_dense_ohe_aaindex_mix_predictor.py 13 5 ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv ../predictions/IPC2_pKa_25_Gray_IPC2.seq13.aaIndex5.csv;

python3 ipc2_pKa_svr_predictor.py ../models/IPC2_pKa_75_SVR_9.pickle ../datasets/IPC2_pKa/IPC2_pKa_25_Gray.csv ../predictions/IPC2_pKa_25_Gray_IPC2.mlp-svr.9.csv
python3 ipc2_pKa_svr_predictor.py ../models/IPC2_pKa_75_SVR_9.pickle ../datasets/IPC2_pKa/IPC2_pKa_75.csv ../predictions/IPC2_pKa_75_IPC2.mlp-svr.9.csv

python3 calculate_table_stats.py IPC2_protein_25 supp;
python3 calculate_table_stats.py IPC2_protein_75 supp;
python3 calculate_table_stats.py IPC2_protein_25 main;
python3 calculate_table_stats.py IPC2_protein_75 main;

python3 calculate_table_stats.py IPC2_peptide_25 supp;
python3 calculate_table_stats.py IPC2_peptide_75 supp;
python3 calculate_table_stats.py IPC2_peptide_25 main;
python3 calculate_table_stats.py IPC2_peptide_75 main;

python3 calculate_table_stats.py IPC2_pKa_25 supp;


#version 2.0.1 (fasta parser bug fix, 11.2022)
