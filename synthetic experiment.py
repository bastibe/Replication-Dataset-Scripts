"""Synthetic Experiment

Evaluates low-pass filtered harmonic tone complexes with white noise
at 20 SNRs with all PDAs in DataSet('Synthetic Experiment') and saves
the resulting pitch tracks in DataSet('Synthetic Data').

"""

from algos import algos
from tqdm import tqdm
from itertools import product
from runforrest import TaskList, defer
import test_signals
import jbof
import numpy

samplerate = 48000  # Hz
duration = 5  # s
basefrequencies = numpy.arange(80, 260, 20)
modulation = numpy.sqrt(2)
lowpass_freq = 2000  # Hz

snrs = range(-20, 45, 5)

num_trials = range(20)

combinations = list(product(snrs, algos, num_trials, basefrequencies))

tasklist = TaskList('synthetic experiment', noschedule_if_exist=True, logfile='synthetic experiment.log')

for snr, algo, trial, basefrequency in tqdm(combinations, smoothing=0, desc='preparing'):
    speech_signal = defer(test_signals.create_htc, duration, basefrequency, modulation, lowpass_freq, samplerate)
    noise_signal = defer(numpy.random.randn, samplerate*duration)
    test_signal = defer(test_signals.mix, speech_signal, noise_signal, snr, samplerate)
    estimate = defer(algo, test_signal, samplerate)
    tasklist.schedule(estimate, metadata=dict(basefrequency=basefrequency,
                                              snr=snr,
                                              algo=algo,
                                              trial=trial))

for item in tqdm(tasklist.run(nprocesses=4, autokill=600), smoothing=0, desc='processing'):
    pass

dataset = jbof.create_dataset('synthetic data')
for task in tqdm(tasklist.done_tasks(), smoothing=0, desc='collecting'):
    metadata = task.metadata
    metadata['noise_dataset'] = 'white noise'
    metadata['speech_dataset'] = 'harmonic tone complex'
    # make metadata JSON-serializable:
    metadata['algo'] = metadata['algo'].__name__
    # add results to dataset:
    item = dataset.add_item(name=f'{metadata["algo"]}_{metadata["basefrequency"]}_{metadata["snr"]}_{metadata["trial"]}',
                            metadata=metadata)
    results = task.returnvalue
    if results is None:
        results = [numpy.array([]), numpy.array([]), numpy.array([])]
    item.add_array('time', results[0].astype('float32'))
    item.add_array('pitch', results[1].astype('float32'))
    item.add_array('probability', results[2].astype('float32'))
