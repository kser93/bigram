from collections import Counter
from itertools import tee
from math import ceil
from math import cos
from math import floor
from math import sin
from math import pi
from operator import itemgetter


def pairwise(iterable):
    it_first, it_second = tee(iterable)
    next(it_second, None)
    return zip(it_first, it_second)


def polar_to_descartes(xy, size):
    r, a = xy
    angle = 2 * pi * a / size
    return floor(r * cos(angle)) + size, floor(r * sin(angle)) + size


def get_circle_boundaries(x, y, diam, diam_max):
    xc = diam_max // 2 + x * diam_max
    yc = diam_max // 2 + y * diam_max
    return (xc - diam // 2, yc - diam // 2), (xc + diam // 2, yc + diam // 2)


def get_bigrams(raw):
    if len(raw) < 2:
        raise ValueError('Unable to produce bigrams')

    bigrams = Counter(pairwise(raw))
    return bigrams


# def get_bigrams_normal(raw):
#     bigrams = get_bigrams(raw)
#     return {
#         bigram: cnt / (len(raw) - 1)
#         for bigram, cnt in bigrams.items()
#     }


# def get_bigrams_scaled(raw, scale: int = 256):
#     if type(scale) != int or scale <= 1:
#         raise ValueError('Incorrect scale')
#
#     bigrams = get_bigrams(raw)
#     max_cnt = max(bigrams.values())
#     return {
#         bigram: ceil(
#             (scale - 1) * cnt / max_cnt
#         )
#         for bigram, cnt in bigrams.items()
#     }


def get_unigrams_sorted(raw):
    unigrams = Counter(raw)
    return sorted(unigrams.items(), key=itemgetter(0))


def get_bigrams_sorted(raw):
    return sorted(get_bigrams(raw).items(), key=itemgetter(1))


def _gen_rescale_bigrams_scaled_uniform(
        sorted_bigrams,
        scale: int = 256,
        low_threshold: float = 0.0,
        high_threshold: float = 1.0
):
    for i, (xy, cnt) in enumerate(sorted_bigrams):
        progress = i / len(sorted_bigrams)
        if not low_threshold <= progress <= high_threshold:
            yield xy, 0
        else:
            try:
                scaled_progress = min(progress / (high_threshold - low_threshold), 1.0)
            except ZeroDivisionError:
                scaled_progress = 1.0
            yield (
                xy,
                ceil((scale - 1) * scaled_progress)
            )


def rescale_bigrams_scaled_uniform(
        sorted_bigrams,
        scale: int = 256,
        low_threshold: float = 0.0,
        high_threshold: float = 1.0
):
    if scale <= 1:
        raise ValueError('Incorrect scale')
    if not 0.0 <= low_threshold <= 1.0:
        raise ValueError('Incorrect sensitivity')
    if not 0.0 <= high_threshold <= 1.0:
        raise ValueError('Incorrect saturation')
    if low_threshold > high_threshold:
        raise ValueError('Sensitivity should be lesser than saturation')

    return dict(_gen_rescale_bigrams_scaled_uniform(sorted_bigrams, scale, low_threshold, high_threshold))
