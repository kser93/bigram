import PIL.Image

from misc import get_bigrams_sorted
from misc import rescale_bigrams_scaled_uniform
from misc import polar_to_descartes


if __name__ == '__main__':
	size = 0x100
	filename = './busybox'
	with open(filename, 'rb') as fd:
		bigrams = get_bigrams_sorted(fd.read())

	img = PIL.Image.new('RGB', (2*size, 2*size), '#000000')
	for sat in range(0, 101, 5):
		sens = max(0, sat - 5)
		for xy, brightness in rescale_bigrams_scaled_uniform(bigrams, sensitivity=sens/100, saturation=sat/100).items():
			img.putpixel(polar_to_descartes(xy, size), (brightness, brightness, brightness))

		img.putpixel(polar_to_descartes((0x90, 0x90), size), (0xFF, 0, 0))
		img.save(f'./out_{sat}_polar.bmp')
