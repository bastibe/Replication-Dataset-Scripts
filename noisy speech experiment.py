"""Noisy Speech Experiment

Evaluates 20 speech samples from all speech corpora with every noise
from every noise database at 10 SNRs with every PDA in DataSet('Noisy
Speech Experiment'), and saves the resulting pitch tracks in
DataSet('Noisy Speech Data').

"""

from algos import algos
from tqdm import tqdm
import random
from itertools import product
from runforrest import TaskList, defer
import test_signals
import jbof
import numpy

# speech datasets:
FDA = jbof.DataSet('FDA/')
KEELE = jbof.DataSet('KEELE/')
KEELE_mod = jbof.DataSet('KEELE_mod/')
PTDB_TUG = jbof.DataSet('PTDB_TUG/')
MOCHA_TIMIT = jbof.DataSet('MOCHA_TIMIT/')
CMU_Arctic = jbof.DataSet('CMU_Arctic/')
try: # TIMIT might not be available
    TIMIT = jbof.DataSet('TIMIT/')
except:
    TIMIT = None

# noise datasets:
NOISEX92 = jbof.ZIPDataSet('NOISEX92.zip')
QUT_NOISE = jbof.ZIPDataSet('QUT_NOISE.zip')


samplerate = 48000
snrs = range(-20, 21, 5)  # up to and including 20 dB SNR
noises = [QUT_NOISE, NOISEX92]
speech_datasets = [PTDB_TUG, KEELE_mod, FDA, CMU_Arctic, MOCHA_TIMIT]
if TIMIT is not None:
    speech_datasets.append(TIMIT)

num_trials = range(20)

combinations = list(product(snrs, noises, speech_datasets, algos, num_trials))

tasklist = TaskList('noisy speech experiment', noschedule_if_exist=True, logfile='noisy speech experiment.log')

# calculate pitches for all algorithms and combinations of sound files

for snr, noise_dataset, speech_dataset, algo, trial in tqdm(combinations, smoothing=0, desc='preparing'):
    for noise_item in noise_dataset.all_items():
        speech_item = random.choice(list(speech_dataset.all_items()))
        speech_signal = defer(speech_item).signal
        if noise_dataset == QUT_NOISE:
            noise_start = random.uniform(5*60, 25*60)
        else:  # NOISEX92:
            noise_start = random.uniform(0, 3*60)
        test_signal = defer(test_signals.create_test_signal, speech_item, noise_item, noise_start, snr, samplerate)
        estimate = defer(algo, test_signal, samplerate)
        tasklist.schedule(estimate, metadata=dict(speech=speech_item,
                                                  speech_dataset=speech_dataset.name,
                                                  noise=noise_item,
                                                  noise_dataset=noise_dataset.name,
                                                  snr=snr,
                                                  algo=algo,
                                                  trial=trial,
                                                  noise_start=noise_start,
                                                  samplerate=samplerate))

for item in tqdm(tasklist.run(nprocesses=16, autokill=600), smoothing=0, desc='processing'):
    pass

dataset = jbof.create_dataset('noisy speech data')
for task in tqdm(tasklist.done_tasks(), smoothing=0, desc='collecting'):
    metadata = task.metadata
    metadata['duration'] = len(metadata['speech'].signal) / metadata['speech'].signal.metadata['samplerate']
    metadata['runtime'] = task.runtime

    # make metadata JSON-serializable:
    metadata['speech'] = metadata['speech'].name
    metadata['noise'] = metadata['noise'].name
    metadata['algo'] = metadata['algo'].__name__

    # add results to dataset:
    item = dataset.add_item(name=f'{metadata["algo"]}_{metadata["speech"]}_{metadata["noise"]}_{metadata["snr"]}_{metadata["trial"]}',
                            metadata=metadata)
    results = task.returnvalue
    if results is None:
        results = [numpy.array([]), numpy.array([]), numpy.array([])]
    item.add_array('time', results[0].astype('float32'))
    item.add_array('pitch', results[1].astype('float32'))
    item.add_array('probability', results[2].astype('float32'))
