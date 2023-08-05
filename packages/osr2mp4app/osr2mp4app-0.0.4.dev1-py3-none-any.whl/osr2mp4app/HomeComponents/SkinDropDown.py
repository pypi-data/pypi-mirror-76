import configparser
import glob
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QComboBox, QGraphicsBlurEffect
from autologging import traced, logged

from abspath import abspath
from config_data import current_config
from helper.helper import getsize, changesize, save
from PyQt5.QtGui import QColor
import logging

from helper.username_parser import read_properties_file


@logged(logging.getLogger(__name__))
@traced("changesize", "blur_me", exclude=True)
class SkinDropDown(QComboBox):
	def __init__(self, parent):
		super(SkinDropDown, self).__init__(parent)

		self.default_x = 620
		self.default_y = 245
		self.img_drop = os.path.join(abspath, "res/Drop_Scale.png")
		self.img_listview = os.path.join(abspath, "res/listview.png")
		self.setToolTip("Skin that will be used in the video")

		self.activated.connect(self.activated_)
		self.main_window = parent

		self.addItems(["Default Skin"])
		self.setStyleSheet("""
		QComboBox {
			 border-image : url(%s);
			 color: white;
		}
		
		QComboBox::drop-down {
			 border-bottom-right-radius: 1px;
		}

		QListView {
			 outline: none;
			 color: white;
			 font: bold;
			 border-image : url(%s);
		}
		
		QScrollBar:vertical {
		 width: 0px;
		 height: 0px;
		}
		QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
		 width: 0px;
		 height: 0px;
		 background: none;
		}
		
		QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
		 background: none;
		}
		QTextEdit, QListView {
		background-color: rgba(0, 0, 0, 0);
		background-attachment: scroll;
		}
 
			 """ % (self.img_drop, self.img_listview))
		self.setItemData(0, QColor(QtCore.Qt.transparent), QtCore.Qt.BackgroundRole)
		self.setItemData(1, QColor(QtCore.Qt.transparent), QtCore.Qt.BackgroundRole)
		self.setItemData(2, QColor(QtCore.Qt.transparent), QtCore.Qt.BackgroundRole)
		self.setup()

	def setup(self):

		self.default_width, self.default_height = getsize(self.img_drop)
		self.default_width /= 1.5
		self.default_height /= 1.5

		self.setGeometry(self.default_x, self.default_y, self.default_width, self.default_height)
		self.setIconSize(QtCore.QSize(self.default_width, self.default_height))
		self.view().setIconSize(QtCore.QSize(0, 0))  # for linux machines otherwise texts got hidden
		self.setMaxVisibleItems(7)

		self.blur_effect = QGraphicsBlurEffect()
		self.blur_effect.setBlurRadius(0)
		self.setGraphicsEffect(self.blur_effect)

	def activated_(self, index):
		current_config["Skin path"] = os.path.join(current_config["osu! path"], "Skins", self.itemText(index))
		save()
		logging.info(current_config["Skin path"])

	def get_skins(self):
		name = "Default Skin"
		if os.path.isdir(current_config["Skin path"]):
			name = os.path.basename(current_config["Skin path"])

		skin_list = [f for f in glob.glob(os.path.join(current_config["osu! path"], "Skins/*"), recursive=True)]
		for x in skin_list:
			skinname = os.path.basename(x)
			self.addItem(skinname)
		self.setCurrentIndex(self.findText(name))

	def set_skin_osu(self):
		c = glob.glob(os.path.join(current_config["osu! path"], "osu!.*.cfg"))
		logging.info(c)
		if c:
			cfg = [x for x in c if "osu!.cfg" not in x]
			logging.info(cfg)
			props = read_properties_file(cfg[0])
			name = props['skin']
			current_config["Skin path"] = os.path.join(current_config["osu! path"], "Skins", name)
			self.setCurrentIndex(self.findText(name))

	def changesize(self):
		changesize(self)
		self.view().setIconSize(QtCore.QSize(0, 0))  # for linux machines otherwise texts got hidden

	def blur_me(self, blur):
		if blur:
			self.blur_effect.setBlurRadius(25)
		else:
			self.blur_effect.setBlurRadius(0)
