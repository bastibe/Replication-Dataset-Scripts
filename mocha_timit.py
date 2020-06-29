import jbof
import pathlib
import soundfile
import numpy
from tqdm import tqdm

import shutil
shutil.rmtree('MOCHA_TIMIT', ignore_errors=True)

root = pathlib.Path('MOCHA_TIMIT_orig')

README = (root / 'README_v1.2.txt').read_text()
LICENSE = (root / 'LICENCE.txt').read_text()
sentences = {int(k.strip('.')): v for k, v in [l.strip().split(' ', 1) for l in (root / 'mocha-timit.txt').open() if l.strip()]}

dataset = jbof.create_dataset('MOCHA_TIMIT', {'README': README,
                                              'LICENSE': LICENSE})

for file in tqdm(list(root.glob('*/*.wav')), smoothing=0):
    # wav:
    speech, speech_samplerate = soundfile.read(str(file))
    # lar:
    laryngograph, laryngograph_samplerate = soundfile.read(str(file.with_suffix('.lar')))
    # lab:
    labels = []
    if file.with_suffix('.lab').exists():
        with file.with_suffix('.lab').open() as f:
            for line in f:
                start, stop, label = line.split()
                labels.append([float(start), float(stop), label])
    # ema:
    articulograph_metadata = {'samplerate': 500}
    with file.with_suffix('.ema').open('rb') as f:
        while True:
            line = f.readline().decode().strip()
            if not line:
                continue
            if line == 'EST_Header_End':
                break
            key, value = line.split()
            articulograph_metadata[key] = value
        articulograph = numpy.frombuffer(f.read(), 'f4')
        articulograph = articulograph.reshape([-1, 22])
    # epg:
    palatograph_metadata = {'samplerate': 200}
    with file.with_suffix('.epg').open('rb') as f:
        palatograph = numpy.frombuffer(f.read(), 'u1')
    palatograph = palatograph.reshape([-1, 12])[:, 4:] # ignore first four bytes
    # convert to binary:
    palatograph = numpy.array([bool(sample >> offset & 1) for offset in range(8) for sample in palatograph.ravel()])
    palatograph = palatograph.reshape([-1, 8, 8])

    metadata = {'sentence': sentences.get(int(file.stem[-3:])),
                'speaker': file.stem[:-4]}
    if labels:
        metadata['labels'] = labels

    item = dataset.add_item(file.stem, metadata)
    soundfile.write('signal.wav', speech, speech_samplerate)
    item.add_array_from_file('signal', 'signal.wav')
    soundfile.write('laryngograph.wav', laryngograph, laryngograph_samplerate)
    item.add_array_from_file('laryngograph', 'laryngograph.wav')
    item.add_array('articulograph', articulograph, metadata=articulograph_metadata)
    item.add_array('palatograph', palatograph, metadata=palatograph_metadata)
