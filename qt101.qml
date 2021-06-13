import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    id: window
    title: "BGRAM-101"
    visible: true
    width: 500
    height: 600
    Material.theme: Material.Dark

    signal low_threshold_changed(real value)
    signal high_threshold_changed(real value)

    Pane {
        width: parent.width
        height: parent.height

        Image {
            id: img_unigram
            objectName: "img_unigram"
            width: 256
            height: 100
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            source: "image://unigram/unigram_placeholder"
        }

        Image {
            id: img_bigram
            objectName: "img_bigram"
            width: 256
            height: 256
            anchors.top: img_unigram.bottom
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
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.topMargin: 10
            Material.accent: Material.Orange
            from: 0
            to: 100
            first.value: 20
            second.value: 70
            first.onMoved: low_threshold_changed(first.position)
            second.onMoved: high_threshold_changed(second.position)
        }
    }
}
