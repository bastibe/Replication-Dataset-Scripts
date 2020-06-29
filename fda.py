import jbof
import pathlib
import soundfile
import numpy

import shutil
shutil.rmtree('FDA', ignore_errors=True)

root = pathlib.Path('FDA_orig')
README = (root / 'README').read_text()
sentences = {int(k): v for k, v in [l.strip().split(' ', 1) for l in (root / 'orthographic.index').open()]}

dataset = jbof.create_dataset('FDA', {'README': README})

import itertools
for file in itertools.chain(root.glob('rl/*.sig'),
                            root.glob('sb/*.sig')):
    speech, speech_samplerate = soundfile.read(str(file), samplerate=20_000,
                                               channels=1, format='RAW',
                                               subtype='PCM_16', endian='BIG')
    laryngograph, laryngograph_samplerate = soundfile.read(str(file.with_suffix('.lar')),
                                                           samplerate=20_000, channels=1,
                                                           format='RAW', subtype='PCM_16',
                                                           endian='BIG')

    metadata = {'sentence': sentences[int(file.stem[2:])]}

    with file.with_suffix('.fx').open() as f:
        pitch_metadata = {}
        lines = iter(f)
        for line in lines:
            if '\t' in line:
                k, v = line.split('\t', maxsplit=1)
                pitch_metadata[k] = v.strip()
            if '\x0c' in line:
                # consume the remaining lines:
                time = []
                pitch = []
                had_hole = False
                for line in lines:
                    if not line.strip(): continue
                    if '=' not in line:
                        t, f = (float(x) for x in line.split())
                        if had_hole:
                            time.append((t-3.5)/1000)
                            pitch.append(0)
                        had_hole = False
                    else:
                        t = t + 3.5
                        f = 0
                        had_hole = True
                    time.append(t/1000)
                    pitch.append(f)
                pitch = numpy.rec.fromarrays([time, pitch], names=['time', 'pitch'])

    item = dataset.add_item(file.stem, metadata)
    item.add_array('pitch', pitch, pitch_metadata)
    soundfile.write('signal.wav', speech, speech_samplerate)
    item.add_array_from_file('signal', 'signal.wav')
    soundfile.write('laryngograph.wav', laryngograph, laryngograph_samplerate)
    item.add_array_from_file('laryngograph', 'laryngograph.wav')
