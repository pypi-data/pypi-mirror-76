from ..pipeline import pipe, ppipe, p
import ray

examples = [
    {'headline': 'Web ads for junk food could be banned in the UK', 'source': 'Guardian', 'nwords':11},
    {'headline': 'The Olympics will be delayed', 'source': 'Guardian', 'nwords':5},
    {'headline': 'Wirecard collapses after fraud scandal', 'source': 'Guardian', 'nwords':5},
    {'date': '2020-07-28', 'headline': 'Usability of Footnotes', 'source': 'https://news.ycombinator.com/item?id=23964200'}
]


def test_pipe():

    records = examples[:]

    def uppercase(x):
        return x.upper()

    def cleanup(x, words):
        for w in words:
            x = x.replace(w, '')
        return x.strip()

    # pass a list of dicts
    _res = pipe(
        iter(records),  # works without the iter() as well
        p('headline', uppercase, 'headline'),
        p('headline', lambda x: x.lower(), 'new_headline'),
        p('headline', cleanup, 'clean_headline', words=['THE'])
    )

    res = list(_res)

    assert len(res) == len(examples)

    assert res[0]['headline'] == 'WEB ADS FOR JUNK FOOD COULD BE BANNED IN THE UK'
    assert res[1]['clean_headline'] == 'OLYMPICS WILL BE DELAYED'


def test_ppipe():

    def uppercase(x):
        return x.upper()

    def cleanup(x, words):
        for w in words:
            x = x.replace(w, '')
        return x.strip()

    many_examples = examples[:] * 50

    # pass a list of dicts
    _res = ppipe(
        many_examples,  # works without the iter() as well
        p('headline', uppercase, 'headline'),
        p('headline', cleanup, 'clean_headline', words=['THE']),
        p('clean_headline', lambda x: x.upper(), 'clean_headline'),
        chunksize=10
    )

    ray.init()
    res = list(_res)
    ray.shutdown()

    assert len(res) == len(many_examples)
    assert res[-1]['clean_headline'] == 'USABILITY OF FOOTNOTES'
