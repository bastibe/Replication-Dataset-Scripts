import jbof
import pathlib
import soundfile
import numpy

import shutil
shutil.rmtree('CMU_Arctic', ignore_errors=True)

root = pathlib.Path('CMU_Arctic_orig')
README = (root / 'CMU_Arctic_Databases.html').read_text()

dataset = jbof.create_dataset('CMU_Arctic', {'README': README})

for directory in root.iterdir():
    if directory.is_file(): continue
    acronym = directory.name[7:10]
    prompts = {}
    for line in (directory / 'etc' / 'txt.done.data').open('rt'):
        key, sentence = line.strip('( )').split(maxsplit=1)
        prompts[key] = sentence.strip('"')
    for wave in directory.glob('wav/*.wav'):
        name = wave.stem
        if not name in prompts:
            print(acronym, name)
        item = dataset.add_item(f'{acronym}_{name}', metadata={'transcription': prompts.get(name, None)})
        item.add_array_from_file('signal', wave)
