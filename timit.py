import jbof
import pathlib
import re

import shutil
shutil.rmtree('TIMIT', ignore_errors=True)

root = pathlib.Path('TIMIT_orig')
README = (root / 'README.DOC').read_text()

dataset = jbof.create_dataset('TIMIT', {'README': README})

sentences = {}
for line in (root/'TIMIT/DOC/PROMPTS.TXT').open():
    if line.startswith(';'): continue
    sentence, identifier = line.rsplit('(', maxsplit=1)
    identifier = identifier.strip(' ()\n')
    sentence = sentence.strip()
    sentences[identifier] = sentence

speakers = {}
dialects = {1: 'New England',
            2: 'Northern',
            3: 'North Midland',
            4: 'South Midland',
            5: 'Southern',
            6: 'New York City',
            7: 'Western',
            8: 'Army Brat (moved around)'}
uses = {'TRN': 'System training speaker',
        'TST': 'System test speaker'}
races = {'WHT': 'White',
         'BLK': 'Black',
         'AMR': 'American Indian',
         'SPN': 'Spanish-American',
         'ORN': 'Oriental',
         'HIS': 'Hispanic',
         'HSP': 'Hispanic',
         '???': 'Unknown'}
educations = {'HS': 'High School',
              'AS': 'Associate Degree',
              'BS': "Bachelor's Degree (BS or BA)",
              'MS': "Master's Degree (MS or MA)",
              'PHD': 'Doctorate Degree (PhD, JD, or MD)',
              '??': 'Unknown'}
def heights(height):
    feet, inches = height.split("'")
    return 0.3048*int(feet) + 0.0254*int(inches.strip('"'))

for line in (root/'TIMIT/DOC/SPKRINFO.TXT').open():
    if line.startswith(';'): continue
    identifier, sex, dr, use, rec, birth, height, race, edu, comments = re.split(r'\s+', line, maxsplit=9)
    speakers[identifier] = dict(sex=sex, dialect=dialects[int(dr)], use=uses[use], recording_date=rec,
                                birth_date=birth, height=heights(height), race=races[race],
                                education=educations[edu], comments=comments)

# these are only given in the commented part, for some reason:
phonetic_codes = {
    'bourgeoisie': '/b uh2 r zh w aa1 z iy/',
    'lined': '/l ay1 n d/',
    'simmered': '/s ih1 m axr d/',
    'teeny': '/t iy1 n iy/',
}
for line in (root/'TIMIT/DOC/TIMITDIC.TXT').open():
    if line.startswith(';'): continue
    word, code = line.split('  ', maxsplit=1)
    code = code.strip()
    phonetic_codes[word] = code

import itertools
for file in itertools.chain(root.glob('TIMIT/TEST/*/*/*.WAV'),
                            root.glob('TIMIT/TRAIN/*/*/*.WAV')):
    _, sex_and_speaker, _, _, *_ = reversed(file.parts)
    sentence_id = file.stem
    speaker_id = sex_and_speaker[1:]
    metadata = dict(**speakers[speaker_id], speaker_id=speaker_id,
                    sentence_id=sentence_id, sentence=sentences[sentence_id.lower()],
                    phonetic_codes=[phonetic_codes[word.lower()]
                                    for word in sentences[sentence_id.lower()].split()
                                    if word.lower() in phonetic_codes])

    for line in file.with_suffix('.TXT').open():
        sentence_start, sentence_stop, sentence = line.split(' ', maxsplit=2)
        metadata['sentence_time'] = dict(start=int(sentence_start),
                                         stop=int(sentence_stop),
                                         text=sentence)

    word_times = []
    for line in file.with_suffix('.PHN').open():
        word_start, word_stop, word = line.split(' ', maxsplit=2)
        word_times.append(dict(start=int(word_start),
                               stop=int(word_stop),
                               text=word))
    metadata['word_times'] = word_times

    phoneme_times = []
    for line in file.with_suffix('.PHN').open():
        phoneme_start, phoneme_stop, phoneme = line.split(' ', maxsplit=2)
        phoneme_times.append(dict(start=int(phoneme_start),
                               stop=int(phoneme_stop),
                                  text=phoneme))
    metadata['phoneme_times'] = phoneme_times

    item = dataset.add_item(sentence_id+speaker_id, metadata)
    item.add_array_from_file('signal', file)
