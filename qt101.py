import sys

from PySide6.QtCore import QObject, QUrl, Slot
from PySide6.QtGui import QGuiApplication, QIcon, QImage, QPixmap
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickImageProvider
from PIL import Image, ImageDraw, ImageOps
from PIL.ImageQt import ImageQt

from math import ceil
from misc import get_unigrams_sorted
from misc import get_bigrams_sorted
from misc import rescale_bigrams_scaled_uniform


class Bridge(QObject):
    def __init__(self, unigrams, bigrams, low_threshold, high_threshold):
        super().__init__()
        self.unigrams = unigrams
        self.bigrams = bigrams
        self.low_threshold = low_threshold / 100
        self.high_threshold = high_threshold / 100

    @Slot()
    def on_low_threshold_changed(self, val):
        self.low_threshold = val
        new_source = f'image://bigram/{val}'
        root.findChild(QObject, 'img_bigram').setProperty('source', new_source)

    @Slot()
    def on_high_threshold_changed(self, val):
        self.high_threshold = val
        new_source = f'image://bigram/{val}'
        root.findChild(QObject, 'img_bigram').setProperty('source', new_source)

    def create_bigram_image(self, size=0x100):
        img = Image.new('RGB', (size, size), '#000000')
        for xy, brightness in rescale_bigrams_scaled_uniform(
                self.bigrams,
                low_threshold=self.low_threshold,
                high_threshold=self.high_threshold).items():
            img.putpixel(xy, (brightness, brightness, brightness))
        qt_img = ImageQt(img)
        pix = QPixmap.fromImage(qt_img)
        return pix.toImage()

    def create_unigram_image(self, size=0x100):
        img = Image.new('RGB', (size, 100), '#000000')
        ctx = ImageDraw.Draw(img)
        scale = 100
        max_cnt = max(map(
            lambda x: x[1],
            self.unigrams
        ))
        unigrams_scaled = {
            unigram: ceil(scale * cnt / max_cnt)
            for unigram, cnt in self.unigrams
        }
        for i, (xy, height) in enumerate(unigrams_scaled.items()):
            ctx.line([(i, 0), (i, height)], fill='#FFFFFF')

        qt_img = ImageQt(ImageOps.flip(img))
        pix = QPixmap.fromImage(qt_img)
        return pix.toImage()


class BigramImageProvider(QQuickImageProvider):
    def __init__(self):
        super(BigramImageProvider, self).__init__(QQuickImageProvider.Image)

    def requestImage(self, p_id, p_size, p_requested_size):
        if p_id == 'bigram_placeholder':
            with open('icon.png', 'rb') as fd:
                raw = fd.read()
                return QImage.fromData(raw)
        else:
            return bridge.create_bigram_image()


class UnigramImageProvider(QQuickImageProvider):
    def __init__(self):
        super(UnigramImageProvider, self).__init__(QQuickImageProvider.Image)

    def requestImage(self, p_id, p_size, p_requested_size):
        return bridge.create_unigram_image()


if __name__ == '__main__':
    with open('./busybox', 'rb') as fd:
        raw = fd.read()
        unigrams = get_unigrams_sorted(raw)
        bigrams = get_bigrams_sorted(raw)

    bridge = Bridge(unigrams, bigrams, low_threshold=20, high_threshold=70)
    app = QGuiApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    qml_engine = QQmlApplicationEngine()
    qml_engine.rootContext().setContextProperty('ctx', bridge)
    qml_engine.addImageProvider('bigram', BigramImageProvider())
    qml_engine.addImageProvider('unigram', UnigramImageProvider())
    qml_engine.load(QUrl('./qt101.qml'))

    root = qml_engine.rootObjects()[0]
    root.low_threshold_changed.connect(bridge.on_low_threshold_changed)
    root.high_threshold_changed.connect(bridge.on_high_threshold_changed)

    sys.exit(app.exec())
