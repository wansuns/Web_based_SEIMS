from collections import Counter
import math
import numpy as np
import tensorflow as tf

class Tokenizer:

    def __init__(self, token_dict):
        # 词->编号的映射
        self.token_dict = token_dict
        # 编号->词的映射
        self.token_dict_rev = {value: key for key, value in self.token_dict.items()}
        # 词汇表大小
        self.vocab_size = len(self.token_dict)

    def id_to_token(self, token_id):
        return self.token_dict_rev[token_id]

    def token_to_id(self, token):
        return self.token_dict.get(token, self.token_dict['[UNK]'])

    def encode(self, tokens):
        token_ids = [self.token_to_id('[CLS]'), ]
        for token in tokens:
            token_ids.append(self.token_to_id(token))
        token_ids.append(self.token_to_id('[SEP]'))
        return token_ids

    def decode(self, token_ids):
        spec_tokens = {'[CLS]', '[SEP]'}
        tokens = []
        for token_id in token_ids:
            token = self.id_to_token(token_id)
            if token in spec_tokens:
                continue
            tokens.append(token)
        return ''.join(tokens)


disallowed_words =  ['（', '）', '(', ')', '__', '《', '》', '【', '】', '[', ']']
max_len = 64
min_word_frequency = 8
batch_size = 16

# 加载数据集
with open('app01/utils/train/poetry.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    lines = [line.replace('：', ':') for line in lines]
# 数据集列表
poetry = []
for line in lines:
    # 有且只能有一个冒号用来分割标题
    if line.count(':') != 1:
        continue
    # 后半部分不能包含禁止词
    __, last_part = line.split(':')
    ignore_flag = False
    for dis_word in disallowed_words:
        if dis_word in last_part:
            ignore_flag = True
            break
    if ignore_flag:
        continue
    if len(last_part) > max_len - 2:
        continue
    poetry.append(last_part.replace('\n', ''))

# 统计词频
counter = Counter()
for line in poetry:
    counter.update(line)
_tokens = [(token, count) for token, count in counter.items() if count >= min_word_frequency]
_tokens = sorted(_tokens, key=lambda x: -x[1])
_tokens = [token for token, count in _tokens]
_tokens = ['[PAD]', '[UNK]', '[CLS]', '[SEP]'] + _tokens
token_id_dict = dict(zip(_tokens, range(len(_tokens))))
tokenizer = Tokenizer(token_id_dict)
# 混洗数据
np.random.shuffle(poetry)


class PoetryDataGenerator:

    def __init__(self, data, random=False):
        self.data = data
        self.batch_size = batch_size
        self.steps = int(math.floor(len(self.data) / self.batch_size))
        self.random = random

    def sequence_padding(self, data, length=None, padding=None):

        if length is None:
            length = max(map(len, data))
        if padding is None:
            padding = tokenizer.token_to_id('[PAD]')
        outputs = []
        for line in data:
            padding_length = length - len(line)
            if padding_length > 0:
                outputs.append(np.concatenate([line, [padding] * padding_length]))
            else:
                outputs.append(line[:length])
        return np.array(outputs)

    def __len__(self):
        return self.steps

    def __iter__(self):
        total = len(self.data)
        if self.random:
            np.random.shuffle(self.data)
        for start in range(0, total, self.batch_size):
            end = min(start + self.batch_size, total)
            batch_data = []
            for single_data in self.data[start:end]:
                batch_data.append(tokenizer.encode(single_data))
            batch_data = self.sequence_padding(batch_data)
            yield batch_data[:, :-1], tf.one_hot(batch_data[:, 1:], tokenizer.vocab_size)
            del batch_data

    def for_fit(self):
        while True:
            # 委托生成器
            yield from self.__iter__()
