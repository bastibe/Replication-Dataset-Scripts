import jbof
import pathlib
import soundfile
import scipy.io
import numpy

import shutil
shutil.rmtree('NOISEX92', ignore_errors=True)

root = pathlib.Path('NOISEX92_orig')
README = (root / 'noise.html').read_text()

dataset = jbof.create_dataset('NOISEX92', {
    'README': README})

for matfile in root.glob('*.mat'):
    data = scipy.io.loadmat(str(matfile))[matfile.stem]
    if numpy.issubdtype(data.dtype, numpy.int16):
        data = data / 2**15
    wavefile = matfile.with_suffix('.wav')
    soundfile.write(wavefile, data, 19980)
    linkend = README.find(matfile.name) + len(matfile.stem) + 6
    textstart = README.find('</a>', linkend)
    textstop = README.find('</li>', textstart)
    title = README[linkend:textstart]
    description = README[textstart+4:textstop]
    description = description.replace('&amp;', '&')
    description = description.replace('\n', '')
    description = title + "\n" + description
    item = dataset.add_item(matfile.stem,
                            {'description': description})
    item.add_array_from_file('signal', wavefile)
    wavefile.unlink()
