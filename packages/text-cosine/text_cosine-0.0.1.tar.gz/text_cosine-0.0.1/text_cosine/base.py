
import math

weight_func_map = {
    "len": lambda x: len(x),
    "fq": lambda x: 1
}

def _get_weight(field, wtype):
    """
    field: string field content
    wtype: weight type
        - len : length sensitive cosine
        - fq  : frequence sensitive cosine
    """
    weight_map = {}
    assert wtype in weight_func_map, "not supported weight type"
    get_weight = weight_func_map[wtype]
    for word in field.split():
        weight_map[word] = weight_map.get(word, 0) + get_weight(word)
    base = math.sqrt(sum(w * w for w in weight_map.values()))
    return weight_map, base

def item_match(x, y, semi_match):
    if semi_match:
        ml = min(len(x), len(y))
        return x[:ml] == y[:ml] 
    else:
        return x == y

def words_match(xs, ys, semi_match=False):
    xls = sorted(xs, key=lambda x: len(x), reverse=True)
    pairs = []
    for x in xls:
        nys = []
        if not x: continue
        for i in range(len(ys)):
            y = ys[i]
            if not y: continue
            if item_match(x, y, semi_match):
                pairs.append( (x, y) )
            else:
                nys.append(y)
        ys = nys
    return pairs

def text_cosine(a, b, wtype="len", semi_match=False):
    weight_1, base_1 = _get_weight(a, wtype=wtype)
    weight_2, base_2 = _get_weight(b, wtype=wtype)
    res = 0.0
    if base_1 and base_2:
        weight_square_sum = 0.00
        strs1, strs2 = list(weight_1.keys()), list(weight_2.keys())
        matched_word_pairs = words_match(strs1, strs2, semi_match=semi_match)
        for w1, w2 in matched_word_pairs:
            weight_square_sum += weight_1[w1] * weight_2[w2]
        res = round(weight_square_sum/(base_1 * base_2), 2)
    return res



