import jbof
import pathlib
import soundfile
import numpy

import shutil
shutil.rmtree('KEELE', ignore_errors=True)

root = pathlib.Path('KEELE_orig')
README = (root / 'keele_pitch_database.htm').read_text()

dataset = jbof.create_dataset('KEELE', {
    'README': README})

for file in root.glob('*.pes'):
    # pet: text transcription
    metadata = {}
    transcription = []
    with file.with_suffix('.pet').open() as f:
        for line in f:
            if line == '\n':
                pass
            elif not line.startswith('LBO'):
                key, value = line.split(':', 1)
                metadata[key] = value.strip()
                if key == 'SAM':
                    metadata['samplerate'] = value.strip()
            else:
                _, line = line.split(':', 1) # discard 'LBO'
                start, _, stop, text = line.split(',', 3)
                transcription.append({'begin': int(start),
                                      'end': int(stop),
                                      'text': text.strip()})

    metadata['transcription'] = transcription
    item = dataset.add_item(file.stem, metadata)

    # pes: speech data file
    signal, samplerate = soundfile.read(str(file), samplerate=20000, channels=1, format='RAW', subtype='PCM_16')
    soundfile.write('tmp.wav', signal, samplerate)
    item.add_array_from_file('signal', 'tmp.wav')
    pathlib.Path('tmp.wav').unlink()
    # pel: laryngograph signal
    signal, samplerate = soundfile.read(str(file.with_suffix('.pel')), samplerate=20000, channels=1, format='RAW', subtype='PCM_16')
    soundfile.write('tmp.wav', signal, samplerate)
    item.add_array_from_file('laryngograph', 'tmp.wav')
    pathlib.Path('tmp.wav').unlink()
    # pev : pitch track
    metadata = {'samplerate': 100}
    pitch = []
    with file.with_suffix('.pev').open() as f:
        for line in f:
            if line == '\n':
                pass
            elif ':' in line:
                key, value = line.split(':', 1)
                metadata[key] = value.strip()
            else:
                if int(line) == 0:
                    pitch.append(0)
                else:
                    pitch.append(1/(int(line) * 1/20_000))
    time = numpy.arange(len(pitch)) * 1/100
    item.add_array('pitch', numpy.rec.fromarrays([time, pitch], names=['time', 'pitch']),
                   metadata)
