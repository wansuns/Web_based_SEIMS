import numpy as np


def generate_random_poetry(tokenizer, model, s=''):

    # 随机生成一首诗
    token_ids = tokenizer.encode(s)
    token_ids = token_ids[:-1]
    while len(token_ids) < 64:
        output = model(np.array([token_ids, ], dtype=np.int32))
        _probas = output.numpy()[0, -1, 3:]
        del output
        # print(_probas)
        p_args = _probas.argsort()[::-1][:100]
        # 排列后的概率顺序
        p = _probas[p_args]
        # 先对概率归一
        p = p / sum(p)
        # 再按照预测出的概率，随机选择一个词作为预测结果
        target_index = np.random.choice(len(p), p=p)
        target = p_args[target_index] + 3
        token_ids.append(target)
        if target == 3:
            break
    return tokenizer.decode(token_ids)


def generate_acrostic(tokenizer, model, head):
    # 随机生成一首藏头诗
    token_ids = tokenizer.encode('')
    token_ids = token_ids[:-1]
    punctuations = ['，', '。']
    punctuation_ids = {tokenizer.token_to_id(token) for token in punctuations}
    # 缓存生成的诗的list
    poetry = []
    for ch in head:
        # 先记录下这个字
        poetry.append(ch)
        # 将藏头诗的字符转成token id
        token_id = tokenizer.token_to_id(ch)
        # 加入到列表中去
        token_ids.append(token_id)
        # 开始生成一个短句
        while True:
            output = model(np.array([token_ids, ], dtype=np.int32))
            _probas = output.numpy()[0, -1, 3:]
            del output
            # 按照出现概率，对所有token倒序排列
            p_args = _probas.argsort()[::-1][:100]
            # 排列后的概率顺序
            p = _probas[p_args]
            # 先对概率归一
            p = p / sum(p)
            # 再按照预测出的概率，随机选择一个词作为预测结果
            target_index = np.random.choice(len(p), p=p)
            target = p_args[target_index] + 3
            # 保存
            token_ids.append(target)
            if target > 3:
                poetry.append(tokenizer.id_to_token(target))
            if target in punctuation_ids:
                break
    return ''.join(poetry)
