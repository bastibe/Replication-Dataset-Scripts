This is part of the dissertation [Pitch of Voiced Speech in the Short-Time Fourier Transform: Algorithms, Ground Truths, and Evaluation Methods](https://bastibe.github.io/Dissertation-Website/)  
(Preprint Manuscript)  
© 2020, Bastian Bechtold. All rights reserved.

# Pitch Estimation Experiments

This directory contains programs that calculate pitch tracks for combinations of speech signals and noise signals.

## Preparing the Corpora

Prior to running the pitch estimation experiments, you need to download the required speech and noise corpora.

Speech signals are taken from the following corpora:

- [CMU-ARCTIC](http://www.festvox.org/cmu_arctic/) (BSD licensed) [1]
- [FDA](http://www.cstr.ed.ac.uk/research/projects/fda/) (free to download) [2]
- [KEELE](https://lost-contact.mit.edu/afs/nada.kth.se/dept/tmh/corpora/KeelePitchDB/) and KEELE_mod (free for noncommercial use) [3]
- [MOCHA-TIMIT](http://www.cstr.ed.ac.uk/research/projects/artic/mocha.html) (free for noncommercial use) [4]
- [PTDB-TUG](https://www.spsc.tugraz.at/databases-and-tools/ptdb-tug-pitch-tracking-database-from-graz-university-of-technology.html) (ODBL license) [5]
- [TIMIT](https://catalog.ldc.upenn.edu/LDC93S1) (commercial license, not included in downloads) [6]

Noise signals are taken from the corpora:

- [NOISEX](http://www.speech.cs.cmu.edu/comp.speech/Section1/Data/noisex.html) (free to download) [7]
- [QUT-NOISE](https://research.qut.edu.au/saivt/databases/qut-noise-databases-and-protocols/) (CC-BY-SA license) [8]

(License texts are included in the corpus files)

These corpora (except for TIMIT) can either be downloaded by running the shell scripts of the same name (i.e. *fda.sh* for downloading the FDA corpus), and then assembling them into a [JBOF](https://jbof.readthedocs.io/en/latest/) dataset using the python script of the same name (i.e. *fda.py* for the FDA corpus), or by downloading the fully assembled [JBOF](https://jbof.readthedocs.io/en/latest/) dataset from [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3921794.svg)](https://doi.org/10.5281/zenodo.3921794) and unzipping them in this directory.

The KEELE_mod corpus is a modified version of the KEELE corpus, where recordings are cut into shorter pieces much like in all the other speech corpora.

The TIMIT corpus can not be provided as a download, as it is not made available under a free license. If you happen to have access to the TIMIT corpus, copy it into the directory *TIMIT_orig*, and the script *timit.py* can import it into a [JBOF](https://jbof.readthedocs.io/en/latest/) dataset like all the other corpora.

## Running the Experiments

- *noisy speech experiment.py* computes pitch tracks for every PDA and speech in noise at various SNRs
- *synthetic experiment.py* computes pitch tracks for every PDA and tone complexes in noise at various SNRs

These experiments take about one year to compute on a 2019 single-core CPU (less on more cores). Their results are collected as a JBOF Dataframe in a "data" directory, and all intermediate tasks and return values are collected in a "experiment" directory.

To run these scripts, the `PDAs` python module needs to be installed. A linux64/Python3.6+ version of this module is available from [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3921794.svg)](https://doi.org/10.5281/zenodo.3921794) as well (requires Matlab and the Curve Fitting Toolbox, Deep Learning Toolbox, Image Processing Toolbox, Parallel Computing Toolbox, Signal Processing Toolbox, Statistics and Machine Learning Toolbox, Symbolic Math Toolbox).

The `PDAs` module includes the following fundamental frequency estimation algorithms:

- AMDF [9]
- AUTOC [10]
- [BANA](http://www2.ece.rochester.edu/projects/wcng/code.html) [11]
- CEP [12]
- [CREPE](https://github.com/marl/crepe) [13]
- [DIO](http://www.kki.yamanashi.ac.jp/~mmorise/world/english/) [14]
- [DNN](http://web.cse.ohio-state.edu/pnl/software.html) [15]
- [KALDI](https://github.com/LvHang/pitch) [16]
- MAPS
- [MBSC](http://www.seas.ucla.edu/spapl/shareware.html) [17]
- [NLS](https://github.com/jkjaer/fastF0Nls) (two versions) [18]
- [PEFAC](http://www.ee.ic.ac.uk/hp/staff/dmb/voicebox/voicebox.html) [19]
- [PRAAT](https://github.com/praat/praat) [20]
- [RAPT](http://www.speech.kth.se/wavesurfer/links.html) [21]
- [RNN](http://web.cse.ohio-state.edu/pnl/software.html) [15]
- [SACC](http://labrosa.ee.columbia.edu/projects/SAcC/) [22]
- [SAFE](http://www.seas.ucla.edu/spapl/weichu/safe/) [23]
- [SHR](https://mathworks.com/matlabcentral/fileexchange/1230) [24]
- SIFT [25]
- [SRH](https://github.com/covarep/covarep) [26]
- [STRAIGHT](https://github.com/HidekiKawahara/legacy_straight) [27]
- [SWIPE](http://www.cise.ufl.edu/~acamacho/english/curriculum.html) [28]
- [YAAPT](http://www.ws.binghamton.edu/zahorian/yaapt.htm) [29]
- [YIN](http://audition.ens.fr/adc/) [30]

These algorithms are included in their native programming language (Matlab for BANA, DNN, MBSC, NLS, NLS2, PEFAC, RAPT, RNN, SACC, SHR, SRH, STRAIGHT, SWIPE, YAAPT, and YIN; C for KALDI, PRAAT, and SAFE; Python for AMDF, AUTOC, CEP, CREPE, MAPS, and SIFT), and adapted to a common Python interface. AMDF, AUTOC, CEP, and SIFT are our partial re-implementations as no original source code could be found.

## References:

1. John Kominek and Alan W Black. CMU ARCTIC database for speech synthesis, 2003.
2. Paul C Bagshaw, Steven Hiller, and Mervyn A Jack. Enhanced Pitch Tracking and the Processing of F0 Contours for Computer Aided Intonation Teaching. In EUROSPEECH, 1993.
3. F Plante, Georg F Meyer, and William A Ainsworth. A Pitch Extraction Reference Database. In Fourth European Conference on Speech Communication and Technology, pages 837–840, Madrid, Spain, 1995.
4. Alan Wrench. MOCHA MultiCHannel Articulatory database: English, November 1999.
5. Gregor Pirker, Michael Wohlmayr, Stefan Petrik, and Franz Pernkopf. A Pitch Tracking Corpus with Evaluation on Multipitch Tracking Scenario. page 4, 2011.
6. John S. Garofolo, Lori F. Lamel, William M. Fisher, Jonathan G. Fiscus, David S. Pallett, Nancy L. Dahlgren, and Victor Zue. TIMIT Acoustic-Phonetic Continuous Speech Corpus, 1993.
7. Andrew Varga and Herman J.M. Steeneken. Assessment for automatic speech recognition: II. NOISEX-92: A database and an experiment to study the effect of additive noise on speech recog- nition systems. Speech Communication, 12(3):247–251, July 1993.
8. David B. Dean, Sridha Sridharan, Robert J. Vogt, and Michael W. Mason. The QUT-NOISE-TIMIT corpus for the evaluation of voice activity detection algorithms. Proceedings of Interspeech 2010, 2010.
9. Myron J. Ross, Harry L. Shaffer, Asaf Cohen, Richard Freudberg, and Harold J. Manley. Average magnitude difference function pitch extractor. Acoustics, Speech and Signal Processing, IEEE Transactions on, 22(5):353—362, 1974.
10. Man Mohan Sondhi. New methods of pitch extraction. Audio and Electroacoustics, IEEE Transactions on, 16(2):262—266, 1968.
11. Na Yang, He Ba, Weiyang Cai, Ilker Demirkol, and Wendi Heinzelman. BaNa: A Noise Resilient Fundamental Frequency Detection Algorithm for Speech and Music. IEEE/ACM Transactions on Audio, Speech, and Language Processing, 22(12):1833–1848, December 2014.
12. Michael Noll. Cepstrum Pitch Determination. The Journal of the Acoustical Society of America, 41(2):293–309, 1967.
13. Jong Wook Kim, Justin Salamon, Peter Li, and Juan Pablo Bello. CREPE: A Convolutional Representation for Pitch Estimation. arXiv:1802.06182 [cs, eess, stat], February 2018. arXiv: 1802.06182.
14. Masanori Morise, Fumiya Yokomori, and Kenji Ozawa. WORLD: A Vocoder-Based High-Quality Speech Synthesis System for Real-Time Applications. IEICE Transactions on Information and Systems, E99.D(7):1877–1884, 2016.
15. Kun Han and DeLiang Wang. Neural Network Based Pitch Tracking in Very Noisy Speech. IEEE/ACM Transactions on Audio, Speech, and Language Processing, 22(12):2158–2168, Decem- ber 2014.
16. Pegah Ghahremani, Bagher BabaAli, Daniel Povey, Korbinian Riedhammer, Jan Trmal, and Sanjeev Khudanpur. A pitch extraction algorithm tuned for automatic speech recognition. In Acoustics, Speech and Signal Processing (ICASSP), 2014 IEEE International Conference on, pages 2494–2498. IEEE, 2014.
17. Lee Ngee Tan and Abeer Alwan. Multi-band summary correlogram-based pitch detection for noisy speech. Speech Communication, 55(7-8):841–856, September 2013.
18. Jesper Kjær Nielsen, Tobias Lindstrøm Jensen, Jesper Rindom Jensen, Mads Græsbøll Christensen, and Søren Holdt Jensen. Fast fundamental frequency estimation: Making a statistically efficient estimator computationally efficient. Signal Processing, 135:188–197, June 2017.
19. Sira Gonzalez and Mike Brookes. PEFAC - A Pitch Estimation Algorithm Robust to High Levels of Noise. IEEE/ACM Transactions on Audio, Speech, and Language Processing, 22(2):518—530, February 2014.
20. Paul Boersma. Accurate short-term analysis of the fundamental frequency and the harmonics-to-noise ratio of a sampled sound. In Proceedings of the institute of phonetic sciences, volume 17, page 97—110. Amsterdam, 1993.
21. David Talkin. A robust algorithm for pitch tracking (RAPT). Speech coding and synthesis, 495:518, 1995.
22. Byung Suk Lee and Daniel PW Ellis. Noise robust pitch tracking by subband autocorrelation classification. In Interspeech, pages 707–710, 2012.
23. Wei Chu and Abeer Alwan. SAFE: a statistical algorithm for F0 estimation for both clean and noisy speech. In INTERSPEECH, pages 2590–2593, 2010.
24. Xuejing Sun. Pitch determination and voice quality analysis using subharmonic-to-harmonic ratio. In Acoustics, Speech, and Signal Processing (ICASSP), 2002 IEEE International Conference on, volume 1, page I—333. IEEE, 2002.
25. Markel. The SIFT algorithm for fundamental frequency estimation. IEEE Transactions on Audio and Electroacoustics, 20(5):367—377, December 1972.
26. Thomas Drugman and Abeer Alwan. Joint Robust Voicing Detection and Pitch Estimation Based on Residual Harmonics. In Interspeech, page 1973—1976, 2011.
27. Hideki Kawahara, Masanori Morise, Toru Takahashi, Ryuichi Nisimura, Toshio Irino, and Hideki Banno. TANDEM-STRAIGHT: A temporally stable power spectral representation for periodic signals and applications to interference-free spectrum, F0, and aperiodicity estimation. In Acous- tics, Speech and Signal Processing, 2008. ICASSP 2008. IEEE International Conference on, pages 3933–3936. IEEE, 2008.
28. Arturo Camacho. SWIPE: A sawtooth waveform inspired pitch estimator for speech and music. PhD thesis, University of Florida, 2007.
29. Kavita Kasi and Stephen A. Zahorian. Yet Another Algorithm for Pitch Tracking. In IEEE International Conference on Acoustics Speech and Signal Processing, pages I–361–I–364, Orlando, FL, USA, May 2002. IEEE.
30. Alain de Cheveigné and Hideki Kawahara. YIN, a fundamental frequency estimator for speech and music. The Journal of the Acoustical Society of America, 111(4):1917, 2002.
