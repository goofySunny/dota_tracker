from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem, QWidget, QLabel
from PyQt6.QtCore import QTimer, QByteArray, QThread, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap, QIcon

import api
from PyQt6 import uic
import sys

# Brought to you by @Sunny
# Description: This class is the main GUI of the application

class ImageLoader(QThread):
    finished = pyqtSignal(QListWidgetItem, str)

    def __init__(self, listItem, item):
        super().__init__()
        self.listItem = listItem
        self.item = item

    def run(self):
        imageName = api.getItemImage(self.item["img"], self.item["dname"])
        self.finished.emit(self.listItem, imageName)

# Ui members names :
# actionExit, heroList
class MainWindow(QMainWindow):
    
    loaders = []
    
    def __init__(self):
        super().__init__()
        uic.loadUi("MainWindow.ui", self)
        
        QTimer.singleShot(100, self.loadData)
        
        self.actionExit.triggered.connect(self.closeWindow)
        
    def loadData(self):
        listItems = api.getHeroes()
        
        for key in listItems.keys():
            listItemWidget = QListWidgetItem()
            listItemWidget.setText(listItems[key]["localized_name"])
            listItemWidget.setData(Qt.ItemDataRole.UserRole, listItems[key])
            self.heroList.addItem(listItemWidget)
        
        self.heroList.itemDoubleClicked.connect(self.heroDoubleClicked)
        
    def heroDoubleClicked(self, item):
        self.showHeroSpecificPage(item.data(Qt.ItemDataRole.UserRole)['id'])        
        
    def showHeroSpecificPage(self, id):
        self.heroList.hide()
        
        if len(api.ITEM_BY_ID) == 0:
            api.getAllItems()
        
        self.heroPage = QWidget(self)
        uic.loadUi("HeroView.ui", self.heroPage)
        
        self.populateHeroSpecificPage(id)
        
        self.heroPage.show()
            
    # QLabel variables include : itemIcon, itemTitle, itemDescription (QLabels);
    def itemDoubleClicked(self, item):
        item = item.data(Qt.ItemDataRole.UserRole)
        self.showItemSpecificPage(item)

    def showItemSpecificPage(self, item):
        self.heroPage.hide()
        self.heroList.hide()
        self.itemView = QWidget(self)
        uic.loadUi("ItemView.ui", self.itemView)
        icon = QIcon(api.getItemImage(item["img"], item["dname"]))
        self.itemView.itemIcon.setPixmap(icon.pixmap(64,64))
        self.itemView.itemTitle.setText(item["dname"])
        self.itemView.itemDescription.setText(item["lore"])
        self.itemView.show()

    def closeWindow(self):
        confirm = QMessageBox.question(self,
                                       "Confirmation",
                                       "Are you sure you want to exit the application?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                       QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.close()

    def populateHeroSpecificPage(self, id):
        
        if len(api.ITEM_BY_ID) == 0:
            QTimer.singleShot(100, self.populateItems)
            return
        
        response = api.itemPopularityByHeroId(id)
        for key in response["start_game_items"].keys():
            listItem = QListWidgetItem()
            item = api.ITEM_BY_ID[key]
            listItem.setData(Qt.ItemDataRole.UserRole, item)
            listItem.setText(item["dname"])
            
            loader = ImageLoader(listItem, item)
            loader.finished.connect(self.setIcon)
            loader.start()
            self.loaders.append(loader)
             
            self.heroPage.starterItems.addItem(listItem)
            
        for key in response["early_game_items"].keys():
            listItem = QListWidgetItem()
            item = api.ITEM_BY_ID[key]
            listItem.setData(Qt.ItemDataRole.UserRole, item)
            listItem.setText(item["dname"])

            loader = ImageLoader(listItem, item)
            loader.finished.connect(self.setIcon)
            loader.start()
            self.loaders.append(loader)

            self.heroPage.earlyGame.addItem(listItem)
            
        for key in response["mid_game_items"].keys():
            listItem = QListWidgetItem()
            item = api.ITEM_BY_ID[key]
            listItem.setText(item["dname"])
            listItem.setData(Qt.ItemDataRole.UserRole, item)
            
            loader = ImageLoader(listItem, item)
            loader.finished.connect(self.setIcon)
            loader.start()
            self.loaders.append(loader)
            
            self.heroPage.midGame.addItem(listItem)
            
        for key in response["late_game_items"].keys():
            listItem = QListWidgetItem()
            item = api.ITEM_BY_ID[key]
            listItem.setData(Qt.ItemDataRole.UserRole, item)
            listItem.setText(item["dname"])

            loader = ImageLoader(listItem, item)
            loader.finished.connect(self.setIcon)
            loader.start()
            
            self.loaders.append(loader)

            self.heroPage.lateGame.addItem(listItem)

        self.heroPage.starterItems.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.heroPage.earlyGame.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.heroPage.midGame.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.heroPage.lateGame.itemDoubleClicked.connect(self.itemDoubleClicked)

    def setIcon(self, listItem, fileName):
        listItem.setIcon(QIcon(fileName))
        
app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
