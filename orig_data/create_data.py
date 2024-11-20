import pandas as pd
import sys
from os.path import realpath
sys.path.append(realpath('.'))
from app import LABEL

print('FAKENHATE')
df_fh = pd.read_json('orig_data/fakehate.json')
df_fn = df_fh[df_fh['task'] == 'fake news']
df_hs = df_fh[df_fh['task'] == 'hate speech']
df_fn['label'] = df_fn['label'].apply(lambda x: [LABEL['fake news'].index(x)])
df_hs['label'] = df_hs['label'].apply(lambda x: [int(x)])
df_fn['test'] = [['fake news detection'] for _ in range(len(df_fn))]
df_hs['test'] = [['hate speech detection'] for _ in range(len(df_hs))]
df_fn.rename(columns={'title':'headline'},inplace=True)
df_hs['headline'] = None
df_fh = pd.concat([df_fn,df_hs],ignore_index=True)
df_fh['task'] = df_fh['task'].apply(lambda x: [x])
df_fh['media'] = None
print('\tFake news detection:',len(df_fh[df_fh['task'].apply(lambda x: 'fake news' in x)]))
print('\tHate speech detection:',len(df_fh[df_fh['task'].apply(lambda x: 'hate speech' in x)]))

print('\nStereotype + Irony')
with open('orig_data/StereotypeIdentification - IronyDetection - 50.txt', 'r') as file:
    stereo_irony = [line.strip() for line in file if line.strip()]
j = stereo_irony.index('---')
df_si = pd.DataFrame(stereo_irony[:j] + stereo_irony[j+1:], columns=['text'])
df_si['task'] = [['stereotype','irony']]*len(df_si)
df_si['label'] = [[LABEL['stereotype'].index('Stereotypical'), LABEL['irony'].index('Ironic')]]*j + [[LABEL['stereotype'].index('Stereotypical'), LABEL['irony'].index('Non Ironic')]]*(len(df_si)-j)
df_si['test'] = [['stereotype identification'] + ['irony detection']]*len(df_si)
df_si['media'] = None
df_si['headline'] = None
print('\tStereotype identification:',len(df_si[df_si['task'].apply(lambda x: 'stereotype' in x)]))
print('\tIrony detection:',len(df_si[df_si['task'].apply(lambda x: 'irony' in x)]))

print('\nExists tweets')
df_exists_tweets = pd.read_excel('orig_data/tweets.xlsx')
labels = pd.read_excel('orig_data/tweets_labels.xlsx')
df_exists_tweets = df_exists_tweets.merge(labels, on='id')
trans = {
    'No sexista': [1],
    'Sexista directo NO ESTERIOTIPOS': [0,1 ],
    'Sexista directo ESTERIOTIPOS': [0, 0],
}
df_exists_tweets['label'] = df_exists_tweets['label'].apply(lambda x: trans[x])
task, test = [], []
for lab in df_exists_tweets['label']:
    if len(lab) == 1:
        task.append(['sexism'])
        test.append(['sexism identification in tweets'])
    else:
        task.append(['sexism','stereotype'])
        test.append(['sexism identification in tweets','stereotype identification in sexist tweets'])
df_exists_tweets['task'] = task
df_exists_tweets['test'] = test
df_exists_tweets['headline'] = None
df_exists_tweets['media'] = None
print('\tSexism identification in memes:',len(df_exists_tweets[df_exists_tweets['task'].apply(lambda x: 'sexism' in x)]))
print('\tStereotype identification in sexist tweets:',len(df_exists_tweets[df_exists_tweets['task'].apply(lambda x: 'stereotype' in x)]))

print('\nExists memes')
df_exists_memes = pd.read_excel('orig_data/memes.xlsx')
labels = pd.read_excel('orig_data/memes_labels.xlsx')
df_exists_memes = df_exists_memes.merge(labels, on='id')
df_exists_memes['label'] = df_exists_memes['label'].apply(lambda x: trans[x])
task, test = [], []
for lab in df_exists_memes['label']:
    if len(lab) == 1:
        task.append(['sexism'])
        test.append(['sexism identification in memes'])
    else:
        task.append(['sexism','stereotype'])
        test.append(['sexism identification in memes','stereotype identification in sexist memes'])
df_exists_memes['task'] = task
df_exists_memes['test'] = test
df_exists_memes['headline'] = None
df_exists_memes.rename(columns={'img':'media','text':'meme_text'},inplace=True)
df_exists_memes['media_type'] = 'image'
print('\tSexism identification in memes:',len(df_exists_memes[df_exists_memes['task'].apply(lambda x: 'sexism' in x)]))
print('\tStereotype identification in sexist memes:',len(df_exists_memes[df_exists_memes['task'].apply(lambda x: 'stereotype' in x)]))

print('\nExists tiktoks')
blacklist = [6881533203593612546,6921493004075273477,6957481796338601221,7095423419453295877,7097021280775441669,7101465072320384261]
df_exists_tiktoks = pd.read_excel('orig_data/tiktoks.xlsx')
labels = pd.read_excel('orig_data/tiktoks_labels.xlsx')
df_exists_tiktoks = df_exists_tiktoks.merge(labels, on='id')
df_exists_tiktoks = df_exists_tiktoks[~df_exists_tiktoks['id'].isin(blacklist)]
df_exists_tiktoks['label'] = df_exists_tiktoks['label'].apply(lambda x: trans[x])
task, test = [], []
for lab in df_exists_tiktoks['label']:
    if len(lab) == 1:
        task.append(['sexism'])
        test.append(['sexism identification in tiktoks'])
    else:
        task.append(['sexism','stereotype'])
        test.append(['sexism identification in tiktoks','stereotype identification in sexist tiktoks'])
df_exists_tiktoks['task'] = task
df_exists_tiktoks['test'] = test
df_exists_tiktoks.rename(columns={'title':'headline'},inplace=True)
df_exists_tiktoks['media'] = df_exists_tiktoks['id'].apply(lambda x: str(x)+'.mp4')
df_exists_tiktoks['media_type'] = 'video'
print('\tSexism identification in tiktoks:',len(df_exists_tiktoks[df_exists_tiktoks['task'].apply(lambda x: 'sexism' in x)]))
print('\tStereotype identification in sexist tiktoks:',len(df_exists_tiktoks[df_exists_tiktoks['task'].apply(lambda x: 'stereotype' in x)]))

print('\nLOCO')
df_loco = pd.read_json('orig_data/loco.json')
df_loco.rename(columns={'txt':'text', 'title':'headline','subcorpus':'label','date':'_date'},inplace=True)
df_loco['label'] = df_loco['label'].apply(lambda x: [int(LABEL['conspiracy'].index(x.capitalize()))])
df_loco['task'] = [['conspiracy']]*len(df_loco)
df_loco['test'] = [['conspiracy detection in articles']]*len(df_loco)
df_loco['media'] = None
print('\tConspiracy detection:',len(df_loco[df_loco['task'].apply(lambda x: 'conspiracy' in x)]))

print('\n\nFINAL')
data = pd.concat([df_fh,df_si, df_exists_tweets,df_exists_memes, df_exists_tiktoks, df_loco],ignore_index=True)
print('\tFake news:',sum(data['task'].apply(lambda x: 'fake news' in x)))
print('\tHate speech:',sum(data['task'].apply(lambda x: 'hate speech' in x)))
print('\tStereotype:',sum(data['task'].apply(lambda x: 'stereotype' in x)))
print('\tIrony:',sum(data['task'].apply(lambda x: 'irony' in x)))
print('\tSexism:',sum(data['task'].apply(lambda x: 'sexism' in x)))
print('Total:',len(data))
data.to_json('data.json',orient='records')