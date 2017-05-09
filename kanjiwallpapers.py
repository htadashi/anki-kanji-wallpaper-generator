#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# A kanji wallpaper generator addon for Anki 
# Version 0.1
#
# Copyright (C) 2017 Hugo Tadashi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See <http://www.gnu.org/licenses/> for a copy of the
# GNU General Public License

# Dependencies:
# - Python Imaging Library (pip install pillow)
# - cjktools (pip install cjktools)
# - Kanji Words for JLPT 0.2 addon (https://ankiweb.net/shared/info/342316189)

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

import Image
import ImageFont
import ImageDraw

import cjktools.resources.kanjidic
from cjktools.resources import kanjidic

import kanjiwords
from kanjiwords import data_filename, pickle_filename, data_dir, _pickle_path, _data_filepath, _kanji_words

# Kanji wallpapers addon folder
addon_folder = "kanji_wallpapers"

# Fonts directory
fonts_directory = "fonts"

# Global variables
_pattern = "Kanji"
_card_type = "is:learn"
_max_entry_words = 8
_font_filename = "GenEiLateGo.otf"
_wallpaper_parameters = {"wallpaper_width": 720,
                         "wallpaper_height": 1280,
                         "kanji_size": 200,
                         "kanji_pos_x": 55,
                         "kanji_pos_y": 370,
                         "readings_size": 35,
                         "kun_readings_pos_x": 300,
                         "kun_readings_pos_y": 410,
                         "on_readings_pos_x": 300,
                         "on_readings_pos_y": 450,
                         "compounds_size": 20,
                         "compounds_pos_x": 55,
                         "compounds_pos_y": 820}

# Create wallpaper
def generate_wallpaper(kanji):

    wallpaper_width = _wallpaper_parameters['wallpaper_width']
    wallpaper_height = _wallpaper_parameters['wallpaper_height']
    kanji_size = _wallpaper_parameters['kanji_size']
    kanji_pos_x = _wallpaper_parameters['kanji_pos_x']
    kanji_pos_y = _wallpaper_parameters['kanji_pos_y']
    readings_size = _wallpaper_parameters['readings_size']
    kun_readings_pos_x = _wallpaper_parameters['kun_readings_pos_x']
    kun_readings_pos_y = _wallpaper_parameters['kun_readings_pos_y']
    on_readings_pos_x = _wallpaper_parameters['on_readings_pos_x']
    on_readings_pos_y = _wallpaper_parameters['on_readings_pos_y']
    compounds_size = _wallpaper_parameters['compounds_size']
    compounds_pos_x = _wallpaper_parameters['compounds_pos_x']
    compounds_pos_y = _wallpaper_parameters['compounds_pos_y']

    img = Image.new("RGB", (wallpaper_width, wallpaper_height), "black")
    draw = ImageDraw.Draw(img)

    kanji_font_file = os.path.join(
        mw.pm.addonFolder(), addon_folder, fonts_directory, _font_filename)

    kanji_font = ImageFont.truetype(kanji_font_file, kanji_size)
    kanji_x_offset = kanji_font.getoffset(kanji)[0]
    draw.text((kanji_pos_x - kanji_x_offset, kanji_pos_y),
              kanji, font=kanji_font)

    kjd = kanjidic.Kanjidic()
    entry = kjd[kanji]

    # Generate on and kun readings
    kun_readings_font = ImageFont.truetype(kanji_font_file, readings_size)
    kun_readings = ', '.join(entry.kun_readings)[:10]
    draw.text((kun_readings_pos_x, kun_readings_pos_y),
              kun_readings, font=kun_readings_font)

    on_readings_font = ImageFont.truetype(kanji_font_file, readings_size)
    on_readings = ', '.join(entry.on_readings)
    draw.text((on_readings_pos_x, on_readings_pos_y),
              on_readings, font=on_readings_font)

    # Generate compound words (based on Kanji Words for JLPT 0.2)
    kanjiwords.kanji_words_init()
    compounds_font = ImageFont.truetype(kanji_font_file, compounds_size)
    k = 1
    if kanji in _kanji_words:
        for entry_word in _kanji_words[kanji]:
            # example: compound=u"読書 【ドクショ】 reading "
            compound = u"%s (%s) : (N%s) %s" % tuple(entry_word)
            compounds_x_offset = compounds_font.getoffset(compound)[0]
            draw.text((compounds_pos_x - compounds_x_offset, compounds_pos_y +
                       compounds_size * k), compound, font=compounds_font)
            if k >= _max_entry_words:
                break
            k = k + 1

    wallpaper_name = u"wallpaper_%s.png" % kanji
    img.save(os.path.join(mw.pm.addonFolder(), wallpaper_name), "PNG")

# Create settings dialog
def createSettingsDialog():
    global _selected_deck
    global _pattern
    global _card_type
    global _wallpaper_parameters
    global _max_entry_words

    settings_dialog = QDialog(mw)
    settings_dialog_layout = QVBoxLayout()
    settings_dialog.setLayout(settings_dialog_layout)

    kanji_cards_box = QGroupBox("Kanji cards")
    kanji_cards_box_layout = QVBoxLayout()
    kanji_cards_box.setLayout(kanji_cards_box_layout)

    hl = QHBoxLayout()
    kanji_cards_box_layout.addLayout(hl)

    hl.addWidget(QLabel("Deck:"))
    deck_combo = QComboBox()
    hl.addWidget(deck_combo)
    for deck in mw.col.decks.all():
        deck_combo.addItem(deck['name'])

    hl.addWidget(QLabel("Kanji field:"))
    pattern_field = QLineEdit()
    pattern_field.setPlaceholderText("(default: \"kanji\")")
    hl.addWidget(pattern_field)

    settings_dialog_layout.addWidget(kanji_cards_box)

    hl2 = QHBoxLayout()
    kanji_cards_box_layout.addLayout(hl2)

    hl2.addWidget(QLabel("Type of cards:"))
    card_type_field = QLineEdit()
    card_type_field.setPlaceholderText("(default: \"is:learn\")")
    hl2.addWidget(card_type_field)

    wallpapers_box = QGroupBox("Wallpaper settings")
    wallpapers_box_layout = QFormLayout()
    wallpapers_box.setLayout(wallpapers_box_layout)

    resolution_list = ["720x1280", "800x600", "1024x768",
                       "1280x960", "1280x1024", "1600x1200","Custom"]
    resolution_combo = QComboBox()
    resolution_combo.addItems(resolution_list)

    spin_max_entries = QSpinBox()
    spin_max_entries.setRange(1, 50)
    spin_max_entries.setValue(_max_entry_words)

    wallpapers_box_layout.addRow(
        QLabel("Wallpaper resolution"), resolution_combo)
    wallpapers_box_layout.addRow(
        QLabel("Maximum number of example words"), spin_max_entries)

    settings_dialog_layout.addWidget(wallpapers_box)

    hl3 = QHBoxLayout()
    settings_dialog_layout.addLayout(hl3)

    gen = QPushButton("Generate")
    hl3.addWidget(gen)
    gen.connect(gen, SIGNAL("clicked()"), settings_dialog, SLOT("accept()"))

    cls = QPushButton("Close")
    hl3.addWidget(cls)
    cls.connect(cls, SIGNAL("clicked()"), settings_dialog, SLOT("reject()"))

    if settings_dialog.exec_():

        _selected_deck = deck_combo.currentText()
        if len(pattern_field.text().strip()) != 0:
            _pattern = pattern_field.text().lower()
        if len(card_type_field.text().strip()) != 0:
            _card_type = card_type_field.text().lower()
        _max_entry_words = spin_max_entries.value()    

        wallpaper_resolution = resolution_combo.currentText()
        if wallpaper_resolution == "720x1280":
            _wallpaper_parameters["wallpaper_width"] = 720
            _wallpaper_parameters["wallpaper_height"] = 1280
            _wallpaper_parameters["kanji_size"] = 200
            _wallpaper_parameters["kanji_pos_x"] = 55
            _wallpaper_parameters["kanji_pos_y"] = 370
            _wallpaper_parameters["readings_size"] = 35
            _wallpaper_parameters["kun_readings_pos_x"] = 300
            _wallpaper_parameters["kun_readings_pos_y"] = 410
            _wallpaper_parameters["on_readings_pos_x"] = 300
            _wallpaper_parameters["on_readings_pos_y"] = 450
            _wallpaper_parameters["compounds_size"] = 20
            _wallpaper_parameters["compounds_pos_x"] = 55
            _wallpaper_parameters["compounds_pos_y"] = 820
        if wallpaper_resolution == "800x600":
            _wallpaper_parameters["wallpaper_width"] = 800
            _wallpaper_parameters["wallpaper_height"] = 600
            _wallpaper_parameters["kanji_size"] = 200
            _wallpaper_parameters["kanji_pos_x"] = 55
            _wallpaper_parameters["kanji_pos_y"] = 100
            _wallpaper_parameters["readings_size"] = 35
            _wallpaper_parameters["kun_readings_pos_x"] = 300
            _wallpaper_parameters["kun_readings_pos_y"] = 140
            _wallpaper_parameters["on_readings_pos_x"] = 300
            _wallpaper_parameters["on_readings_pos_y"] = 190
            _wallpaper_parameters["compounds_size"] = 20
            _wallpaper_parameters["compounds_pos_x"] = 55
            _wallpaper_parameters["compounds_pos_y"] = 310
        if wallpaper_resolution == "1024x768":
            _wallpaper_parameters["wallpaper_width"] = 1024
            _wallpaper_parameters["wallpaper_height"] = 768
            _wallpaper_parameters["kanji_size"] = 250
            _wallpaper_parameters["kanji_pos_x"] = 55
            _wallpaper_parameters["kanji_pos_y"] = 100
            _wallpaper_parameters["readings_size"] = 55
            _wallpaper_parameters["kun_readings_pos_x"] = 300
            _wallpaper_parameters["kun_readings_pos_y"] = 140
            _wallpaper_parameters["on_readings_pos_x"] = 300
            _wallpaper_parameters["on_readings_pos_y"] = 190
            _wallpaper_parameters["compounds_size"] = 30
            _wallpaper_parameters["compounds_pos_x"] = 55
            _wallpaper_parameters["compounds_pos_y"] = 400
        if wallpaper_resolution == "1280x960":
            _wallpaper_parameters["wallpaper_width"] = 1280
            _wallpaper_parameters["wallpaper_height"] = 960
            _wallpaper_parameters["kanji_size"] = 250
            _wallpaper_parameters["kanji_pos_x"] = 55
            _wallpaper_parameters["kanji_pos_y"] = 100
            _wallpaper_parameters["readings_size"] = 55
            _wallpaper_parameters["kun_readings_pos_x"] = 300
            _wallpaper_parameters["kun_readings_pos_y"] = 140
            _wallpaper_parameters["on_readings_pos_x"] = 300
            _wallpaper_parameters["on_readings_pos_y"] = 190
            _wallpaper_parameters["compounds_size"] = 30
            _wallpaper_parameters["compounds_pos_x"] = 55
            _wallpaper_parameters["compounds_pos_y"] = 400
        if wallpaper_resolution == "1280x1024":
            _wallpaper_parameters["wallpaper_width"] = 1280
            _wallpaper_parameters["wallpaper_height"] = 1024
            _wallpaper_parameters["kanji_size"] = 250
            _wallpaper_parameters["kanji_pos_x"] = 55
            _wallpaper_parameters["kanji_pos_y"] = 100
            _wallpaper_parameters["readings_size"] = 55
            _wallpaper_parameters["kun_readings_pos_x"] = 300
            _wallpaper_parameters["kun_readings_pos_y"] = 140
            _wallpaper_parameters["on_readings_pos_x"] = 300
            _wallpaper_parameters["on_readings_pos_y"] = 190
            _wallpaper_parameters["compounds_size"] = 30
            _wallpaper_parameters["compounds_pos_x"] = 55
            _wallpaper_parameters["compounds_pos_y"] = 400
        if wallpaper_resolution == "1600x1200":
            _wallpaper_parameters["wallpaper_width"] = 1600
            _wallpaper_parameters["wallpaper_height"] = 1200
            _wallpaper_parameters["kanji_size"] = 250
            _wallpaper_parameters["kanji_pos_x"] = 55
            _wallpaper_parameters["kanji_pos_y"] = 100
            _wallpaper_parameters["readings_size"] = 55
            _wallpaper_parameters["kun_readings_pos_x"] = 300
            _wallpaper_parameters["kun_readings_pos_y"] = 140
            _wallpaper_parameters["on_readings_pos_x"] = 300
            _wallpaper_parameters["on_readings_pos_y"] = 190
            _wallpaper_parameters["compounds_size"] = 30
            _wallpaper_parameters["compounds_pos_x"] = 55
            _wallpaper_parameters["compounds_pos_y"] = 400
        if wallpaper_resolution == "Custom":
            custom_dialog_result = createCustomDialog()
            if custom_dialog_result == 0:
                return 0

        mw.progress.start(immediate=True)
        start_generation()
        mw.progress.finish()

# Create settings dialog for custom resolution wallpaper
def createCustomDialog():
    custom_dialog = QDialog(mw)
    custom_dialog_layout = QVBoxLayout()
    custom_dialog.setLayout(custom_dialog_layout)

    form_layout = QFormLayout()
    custom_dialog_layout.addLayout(form_layout)

    spin_wallpaper_width = QSpinBox()
    spin_wallpaper_width.setRange(1, 65536)
    spin_wallpaper_width.setValue(1600)
    spin_wallpaper_height = QSpinBox()
    spin_wallpaper_height.setRange(1, 65536)
    spin_wallpaper_height.setValue(1200)
    spin_kanji_size = QSpinBox()
    spin_kanji_size.setRange(1, 65536)
    spin_kanji_size.setValue(250)
    spin_kanji_pos_x = QSpinBox()
    spin_kanji_pos_x.setRange(1, 65536)
    spin_kanji_pos_x.setValue(55)
    spin_kanji_pos_y = QSpinBox()
    spin_kanji_pos_y.setRange(1, 65536)
    spin_kanji_pos_y.setValue(100)
    spin_readings_size = QSpinBox()
    spin_readings_size.setRange(1, 65536)
    spin_readings_size.setValue(55)
    spin_kun_readings_pos_x = QSpinBox()
    spin_kun_readings_pos_x.setRange(1, 65536)
    spin_kun_readings_pos_x.setValue(300)
    spin_kun_readings_pos_y = QSpinBox()
    spin_kun_readings_pos_y.setRange(1, 65536)
    spin_kun_readings_pos_y.setValue(140)
    spin_on_readings_pos_x = QSpinBox()
    spin_on_readings_pos_x.setRange(1, 65536)
    spin_on_readings_pos_x.setValue(300)
    spin_on_readings_pos_y = QSpinBox()
    spin_on_readings_pos_y.setRange(1, 65536)
    spin_on_readings_pos_y.setValue(190)
    spin_compounds_size = QSpinBox()
    spin_compounds_size.setRange(1, 65536)
    spin_compounds_size.setValue(30)
    spin_compounds_pos_x = QSpinBox()
    spin_compounds_pos_x.setRange(1, 65536)
    spin_compounds_pos_x.setValue(55)
    spin_compounds_pos_y = QSpinBox()
    spin_compounds_pos_y.setRange(1, 65536)
    spin_compounds_pos_y.setValue(400)

    form_layout.addRow(
        QLabel("Wallpaper width"), spin_wallpaper_width)
    form_layout.addRow(
        QLabel("Wallpaper height"), spin_wallpaper_height)
    form_layout.addRow(
        QLabel("Kanji font size"), spin_kanji_size)
    form_layout.addRow(
        QLabel("Kanji x position"), spin_kanji_pos_x)
    form_layout.addRow(
        QLabel("Kanji y position"), spin_kanji_pos_y)
    form_layout.addRow(
        QLabel("Kun/On readings font size"), spin_readings_size)
    form_layout.addRow(
        QLabel("Kun readings x position"), spin_kun_readings_pos_x)
    form_layout.addRow(
        QLabel("Kun readings y position"), spin_kun_readings_pos_y)
    form_layout.addRow(
        QLabel("On readings x position"), spin_on_readings_pos_x)
    form_layout.addRow(
        QLabel("On readings y position"), spin_on_readings_pos_y)
    form_layout.addRow(
        QLabel("Compound words font size"), spin_compounds_size)
    form_layout.addRow(
        QLabel("Compound words x position"), spin_compounds_pos_x)
    form_layout.addRow(
        QLabel("Compound words y position"), spin_compounds_pos_y)

    hlb = QHBoxLayout()
    custom_dialog_layout.addLayout(hlb)

    gen = QPushButton("Ok")
    hlb.addWidget(gen)
    gen.connect(gen, SIGNAL("clicked()"), custom_dialog, SLOT("accept()"))

    cls = QPushButton("Cancel")
    hlb.addWidget(cls)
    cls.connect(cls, SIGNAL("clicked()"), custom_dialog, SLOT("reject()"))

    if custom_dialog.exec_():
        _wallpaper_parameters["wallpaper_width"] = spin_wallpaper_width.value()
        _wallpaper_parameters["wallpaper_height"] = spin_wallpaper_height.value()
        _wallpaper_parameters["kanji_size"] = spin_kanji_size.value()
        _wallpaper_parameters["kanji_pos_x"] = spin_kanji_pos_x.value()
        _wallpaper_parameters["kanji_pos_y"] = spin_kanji_pos_y.value()
        _wallpaper_parameters["readings_size"] = spin_readings_size.value()
        _wallpaper_parameters["kun_readings_pos_x"] = spin_kun_readings_pos_x.value()
        _wallpaper_parameters["kun_readings_pos_y"] = spin_kun_readings_pos_y.value()
        _wallpaper_parameters["on_readings_pos_x"] = spin_on_readings_pos_x.value()
        _wallpaper_parameters["on_readings_pos_y"] = spin_on_readings_pos_y.value()
        _wallpaper_parameters["compounds_size"] = spin_compounds_size.value()
        _wallpaper_parameters["compounds_pos_x"] = spin_compounds_pos_x.value()
        _wallpaper_parameters["compounds_pos_y"] = spin_compounds_pos_y.value()
        return 1
    else:
        custom_dialog.close()
        return 0
        
# Start wallpaper generation
def start_generation():

    ids = mw.col.findCards("\"deck:%s\" %s" % (_selected_deck, _card_type))
    for id in ids:
        card = mw.col.getCard(id)
        note = card.note()
        generate_wallpaper(note[_pattern])

action = QAction("Generate Kanji Wallpapers", mw)
action.triggered.connect(createSettingsDialog)
mw.form.menuTools.addSeparator()
mw.form.menuTools.addAction(action)
