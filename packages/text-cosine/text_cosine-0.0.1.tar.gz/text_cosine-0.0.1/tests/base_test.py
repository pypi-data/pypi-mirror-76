from reference_linking.text_cosine import words_match, text_cosine

def base_check(func, items):
    for args, kwargs, y in items:
        out = func(*args, **kwargs)
        assert out == y, "Input: {args} {kwargs} \nOutput: {out}\nExpect: {y}".format(
            args=args, kwargs=kwargs, y=y, out=out)

word_match_items = [
    [ 
        [["vandesompele","j"], ["jo", "vandesompele"]], {"semi_match": False}, 
        [("vandesompele", "vandesompele")]
    ],
    [
        [["vandesompele","j"], ["jo", "vandesompele"]], {"semi_match": True}, 
        [("vandesompele", "vandesompele"), ("j", "jo")]
    ],
    [
        [["chemical", "reviews"], ["chem", "rev"]], {"semi_match": False},
        []
    ],
    [
        [["chemical", "reviews"], ["chem", "rev"]], {"semi_match": True},
        [("chemical", "chem"), ("reviews", "rev")]
    ],    
    [
        [[], []], {"semi_match": False},
        []
    ],
    [
        [[], []], {"semi_match": True},
        []
    ]
]

def test_words_match():
    base_check(words_match, word_match_items)

text_cosine_items = [
    [["vandesompele j", "jo vandesompele"], {"semi_match": False}, 0.98],
    [["vandesompele j", "jo vandesompele"], {"semi_match": True}, 1.0],
    [["a b j", "a b c"], {"semi_match": False}, 0.67],
    [["a b j", "a b c"], {"semi_match": True}, 0.67],
    [["abc def", "abc def cde"], {"semi_match": False}, 0.82],
    [["abc def", "abc defghh cde"], {"semi_match": True}, 0.87],
    [["", ""], {"semi_match": False}, 0.0],
    [["", ""], {"semi_match": True}, 0.0],
]

def test_text_cosine():
    base_check(text_cosine, text_cosine_items)
