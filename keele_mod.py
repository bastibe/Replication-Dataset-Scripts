import jbof
import soundfile
import numpy
from pathlib import Path

labels = dict(
    f1nw0000=[17984, 69419, 123732, 216172, 255018, 310410, 335228, 390980, 448890, 493851, 528740, 556664],
    f2nw0000=[123435, 220527, 279986, 334930, 368799, 439172, 499008, 587821],
    f3nw0000=[63009, 91278, 128062, 211507, 260212, 322540, 389637, 439704, 485343, 531664, 572535],
    f4nw0000=[51166, 141150, 232376, 277779, 403352, 460125, 541169],
    f5nw0000=[71306, 108040, 143909, 257568, 313748, 391105, 490070, 557919, 675467],
    m1nw0000=[34223, 77629, 107680, 140651, 243323, 289651, 332222, 359351, 388566, 425712, 465361, 528801, 588484, 646080, 679470],
    m2nw0000=[68697, 125293, 257705, 315368, 338149, 394388, 448136, 500105, 546734],
    m3nw0000=[74348, 104997, 183594, 226382, 273722, 300123, 352015, 398749, 476435],
    m4nw0000=[63975, 124940, 221279, 268320, 326651, 352241, 417722, 474547, 520835, 569381, 627712],
    m5nw0000=[69754, 141758, 247965, 307369, 375323, 483330, 560735, 616088, 673692, 747496])

import KEELE

import shutil
shutil.rmtree('KEELE_mod', ignore_errors=True)

dataset = jbof.create_dataset('KEELE_mod', {
    'README': KEELE.dataset.metadata['README']})

for item in KEELE.dataset.all_items():
    metadata = item.metadata
    pitch = item.pitch
    pitch_sr = int(pitch.metadata['samplerate'])
    laryngograph = item.laryngograph
    laryngograph_sr = int(laryngograph.metadata['samplerate'])
    signal = item.signal
    signal_sr = int(signal.metadata['samplerate'])

    breaks = [0, *labels[item.name], len(signal)]

    for idx in range(len(breaks)-1):
        signal_start = breaks[idx]
        signal_stop = breaks[idx+1]
        this_signal = signal[signal_start:signal_stop]
        pitch_start = int(signal_start / signal_sr * pitch_sr)
        pitch_stop = int(signal_stop / signal_sr * pitch_sr)
        this_pitch = pitch[pitch_start:pitch_stop]
        this_pitch['time'] -= this_pitch['time'][0]
        laryngograph_start = int(signal_start / signal_sr * laryngograph_sr)
        laryngograph_stop = int(signal_stop / signal_sr * laryngograph_sr)
        this_laryngograph = laryngograph[laryngograph_start:laryngograph_stop]

        this_item = dataset.add_item(f'{item.name}_{idx}',
                                     metadata=dict(**metadata,
                                                   section_start=signal_start/signal_sr,
                                                   section_end=signal_stop/signal_sr))
        this_item.add_array('signal', this_signal, metadata=signal.metadata,
                            fileformat='wav', samplerate=signal_sr)
        this_item.add_array('pitch', this_pitch, metadata=pitch.metadata, fileformat='npy')
        this_item.add_array('laryngograph', this_laryngograph, metadata=laryngograph.metadata,
                            fileformat='wav', samplerate=laryngograph_sr)
