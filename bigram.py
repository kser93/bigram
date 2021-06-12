import PIL.Image

from misc import get_bigrams_sorted
from misc import rescale_bigrams_scaled_uniform


if __name__ == '__main__':
	size = 0x100
	filename = './busybox'
	with open(filename, 'rb') as fd:
		bigrams = get_bigrams_sorted(fd.read())

	img = PIL.Image.new('RGB', (size, size), '#000000')
	for high_threshold in range(0, 101, 5):
		low_threshold = max(0, high_threshold - 5)
		for xy, brightness in rescale_bigrams_scaled_uniform(
				bigrams, low_threshold=low_threshold / 100, high_threshold=high_threshold / 100
		).items():
			img.putpixel(xy, (brightness, brightness, brightness))

		img.putpixel((0x90, 0x90), (0xFF, 0, 0))
		img.save(f'./out_{high_threshold}.bmp')
