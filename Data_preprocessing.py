from numpy import save
import pandas as pd
from torchtext.data import Field, TabularDataset, Iterator , BucketIterator
from sklearn.model_selection import train_test_split
from inltk.inltk import setup
from inltk.inltk import tokenize

english_txt = open('C:\\Users\\yatha\\Desktop\\dataset\\finalrepo\\train\\alt\\en-hi\\train.en' , encoding='utf-8').read().split('\n')
hindi_txt = open('C:\\Users\\yatha\\Desktop\\dataset\\finalrepo\\train\\alt\\en-hi\\train.hi' , encoding='utf-8').read().split('\n')

raw_data = {'english' : [line for line in english_txt[1:100]] , 
            'hindi' : [line for line in hindi_txt[1:100]]}

df = pd.DataFrame(raw_data , columns=['english' , 'hindi'])

train , test = train_test_split(df , test_size=0.2)
train.to_csv('dataset_en_hi/train.csv' , index=False)
test.to_csv('dataset_en_hi/test.csv' , index=False)

hindi_vocab = setup('hi')
english_vocab = setup('en')

def tokenizer_en(text):
        return tokenize(text ,'en')
def tokenizer_hi(text):
        return tokenize(text ,'hi')

english = Field(sequential=True , use_vocab=True , tokenize=tokenizer_en , lower=True)
hindi = Field(sequential=True , use_vocab=True , tokenize=tokenizer_hi)


fields = {'english' : ('eng' , english) , 'hindi' : ('hin' , hindi)} 

train_data , test_data = TabularDataset.splits(path='dataset_en_hi/' , train='train.csv' , test='test.csv' , format='csv' , fields=fields)

english.build_vocab(train_data , min_freq=1 , max_size=10000)
hindi.build_vocab(train_data , min_freq=1 , max_size=10000)

def save_vocab_eng(vocab = english.vocab, path = 'saved_vocab/train.en'):
    with open(path, 'w+', encoding='utf-8') as f:     
        for token, index in vocab.stoi.items():
            f.write(f'{index}\t{token}\n')
def save_vocab_hin(vocab = hindi.vocab, path = 'saved_vocab/train.hi'):
    with open(path, 'w+', encoding='utf-8') as f:     
        for token, index in vocab.stoi.items():
            f.write(f'{index}\t{token}\n')

def read_vocab_eng(path = 'saved_vocab/train.en'):
    vocab = dict()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            index, token = line.split('\t')
            vocab[token] = int(index)
    return vocab

def read_vocab_hin(path = 'saved_vocab/train.hi'):
    vocab = dict()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            index, token = line.split('\t')
            vocab[token] = int(index)
    return vocab

save_vocab_eng()
save_vocab_hin()
english.vocab = read_vocab_eng()
hindi.vocab =  read_vocab_hin()

src_vocab_size = len(english.vocab)
trg_vocab_size = len(hindi.vocab)
print(src_vocab_size)
print(trg_vocab_size)
'''train_iterator , test_iterator = BucketIterator.splits((train_data , test_data) ,
     batch_size=32 , sort_key=lambda x: len(x.eng) , 
     sort_within_batch=True , repeat=False , device='cuda')


for batch in train_iterator:
    print(batch)'''