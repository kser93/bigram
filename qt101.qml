import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    id: window
    title: "bigram101"
    visible: true
    width: 500
    height: 500
    Material.theme: Material.Dark

    signal sensitivity_changed(real value)
    signal saturation_changed(real value)

    Pane {
        width: parent.width
        height: parent.height

        Image {
            id: img_bigram
            objectName: "img_bigram"
            width: 256
            height: 256
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottomMargin: 30
            source: "image://bigram/bigram_placeholder"
        }

        RangeSlider {
            id: rng_sld_boundaries
            objectName: "rng_sld_boundaries"
            anchors.top: img_bigram.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.topMargin: 10
            Material.accent: Material.Orange
            from: 0
            to: 100
            first.value: 20
            second.value: 70
            first.onMoved: sensitivity_changed(first.position)
            second.onMoved: saturation_changed(second.position)
        }
    }
}
