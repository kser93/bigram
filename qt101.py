import sys

from PySide6.QtCore import QObject, QUrl, Slot
from PySide6.QtGui import QGuiApplication, QImage, QPixmap
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickImageProvider
from PIL import Image
from PIL.ImageQt import ImageQt

from misc import get_bigrams_sorted
from misc import rescale_bigrams_scaled_uniform


class Bridge(QObject):
    def __init__(self, bigrams, sensitivity, saturation):
        super().__init__()
        self.bigrams = bigrams
        self.sensitivity = sensitivity / 100
        self.saturation = saturation / 100

    @Slot()
    def on_sensitivity_changed(self, val):
        self.sensitivity = val
        new_source = f'image://bigram/{val}'
        root.findChild(QObject, 'img_bigram').setProperty('source', new_source)

    @Slot()
    def on_saturation_changed(self, val):
        self.saturation = val
        new_source = f'image://bigram/{val}'
        root.findChild(QObject, 'img_bigram').setProperty('source', new_source)

    def create_image(self, size=0x100):
        img = Image.new('RGB', (size, size), '#000000')
        for xy, brightness in rescale_bigrams_scaled_uniform(
                self.bigrams,
                sensitivity=self.sensitivity,
                saturation=self.saturation).items():
            img.putpixel(xy, (brightness, brightness, brightness))
        qt_img = ImageQt(img)
        pix = QPixmap.fromImage(qt_img)
        return pix.toImage()


class BigramImageProvider(QQuickImageProvider):
    def __init__(self):
        super(BigramImageProvider, self).__init__(QQuickImageProvider.Image)

    def requestImage(self, p_id, p_size, p_requested_size):
        if p_id == 'bigram_placeholder':
            with open('bigram_placeholder.bmp', 'rb') as fd:
                raw = fd.read()
                return QImage.fromData(raw)
        else:
            return bridge.create_image()


if __name__ == '__main__':
    with open('./busybox', 'rb') as fd:
        bigrams = get_bigrams_sorted(fd.read())

    bridge = Bridge(bigrams, sensitivity=20, saturation=70)
    app = QGuiApplication(sys.argv)
    qml_engine = QQmlApplicationEngine()
    qml_engine.rootContext().setContextProperty('ctx', bridge)
    qml_engine.addImageProvider('bigram', BigramImageProvider())
    qml_engine.load(QUrl('./qt101.qml'))

    root = qml_engine.rootObjects()[0]
    root.sensitivity_changed.connect(bridge.on_sensitivity_changed)
    root.saturation_changed.connect(bridge.on_saturation_changed)

    sys.exit(app.exec())
