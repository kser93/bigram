import collections
from PIL import Image, ImageDraw, ImageOps

from math import ceil
from operator import itemgetter

if __name__ == '__main__':
    filename = './busybox'
    with open(filename, 'rb') as fd:
        unigrams = collections.Counter(fd.read())

    img = Image.new('RGB', (0x200, 100), '#000000')
    ctx = ImageDraw.Draw(img)
    scale = 100
    max_cnt = max(unigrams.values())
    unigrams_scaled = {
        unigram: ceil(scale * cnt / max_cnt)
        for unigram, cnt in unigrams.items()
    }
    for i, (xy, height) in enumerate(
            sorted(unigrams_scaled.items(), key=itemgetter(0))
    ):
        ctx.line([(2*i, 0), (2*i, height)], fill='#FFFFFF')

    ImageOps.flip(img).show()
