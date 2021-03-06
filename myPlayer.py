import MusicParser
import sys
import time
import mutagen
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton, QAction, QMenuBar, qApp, QApplication, QSlider, QVBoxLayout, QLabel, QMessageBox, QWidget
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap, QIcon
from PyQt5.QtCore import QUrl, QDirIterator, Qt
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent

#Two Window for song list
class Window2(QWidget):
    def __init__(self):
        super(Window2, self).__init__()
        self.setWindowTitle('MyPlayer Songs')
        self.resize(550, 700)
        self.setWindowIcon(QIcon('Plug_2.png'))



class Ui_Dialog(QMainWindow):

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.palette = QPalette()
        self.VerticalLayout = QVBoxLayout()
        self.userAction = -1  # 0- stopped, 1- playing 2-paused
        self.width = 550
        self.height = 700
        self.PlayerIsActive = 0 # 0 - not active, 1 - active
        self.nameFont = 'Plug_2.png'

        self.msgBox = QMessageBox()

    def setupUi(self, Dialog):
        Dialog.resize(self.width, self.height)
        Dialog.setWindowTitle('MyPlayer')
        Dialog.setWindowIcon(QIcon(self.nameFont))


        # Add MainMenu
        self.mainMenu = QMenuBar(Dialog)
        self.fileMenu = self.mainMenu.addMenu('File')
        self.ChangeThemeMenu = self.mainMenu.addMenu('Change')
        self.DataBaseSongs = self.mainMenu.addMenu('Recommend')
        self.helpMenu = self.mainMenu.addMenu('About')


        # Add In Menu Actions
        self.openAction = QAction('Open File')
        self.openAction.setShortcut('Ctrl+O')
        self.openActions = QAction('Open Directory')
        self.exitAction = QAction('Exit')
        self.exitAction.setShortcut('Ctrl+Q')

        self.loadBackgroung = QAction('Load my background')
        self.changeBlack = QAction('Change Black')
        self.changeWhite = QAction('Change white')

        self.RecommendedDataBase = QAction('Recommended data base of songs')

        self.Developer = QAction('About Developer')
        self.Program = QAction('About Program')
        self.Help_ = QAction('Help')


        # Add to Menus Actions
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.openActions)
        self.fileMenu.addAction(self.exitAction)
        self.ChangeThemeMenu.addAction(self.changeBlack)
        self.ChangeThemeMenu.addAction(self.changeWhite)
        self.ChangeThemeMenu.addAction(self.loadBackgroung)
        self.DataBaseSongs.addAction(self.RecommendedDataBase)
        self.helpMenu.addAction(self.Developer)
        self.helpMenu.addAction(self.Program)
        self.helpMenu.addAction(self.Help_)


        # Create Slider Volume
        self.volumeslider = QSlider(Qt.Horizontal, Dialog)
        self.volumeslider.setFocusPolicy(Qt.NoFocus)
        self.volumeslider.setGeometry(420, 650, 120, 30)
        self.volumeslider.setValue(100)
        self.volumeslider.setTickInterval(20)
        self.volumeslider.setTickPosition(QSlider.TicksBelow)
        self.volumeslider.valueChanged[int].connect(self.changeVolume)

        #Create Slider Status of song
        self.songSlider = QSlider(Qt.Horizontal, Dialog)
        self.songSlider.setGeometry(17, 602, 521, 15)
        self.songSlider.setRange(0, 0)
        self.songSlider.sliderMoved.connect(self.set_position)



        # Add labels
        self.timeInStart = QLabel(Dialog)
        self.timeInStart.setGeometry(10, 612, 70, 25)
        self.AllTimeSong = QLabel(Dialog)
        self.AllTimeSong.setGeometry(500, 610, 70, 25)
        self.PictureAlbum = QLabel(Dialog)
        self.PictureAlbum.setGeometry(20, 170, 300, 300)
        self.showInfoToMusic_1 = QLabel(Dialog)
        self.showInfoToMusic_2 = QLabel(Dialog)
        self.showInfoToMusic_3 = QLabel(Dialog)
        self.showInfoToMusic_4 = QLabel(Dialog)

        # Add labals in Vertical layout widget
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(350, 230, 200, 200))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.showInfoToMusic_1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.showInfoToMusic_1)
        self.showInfoToMusic_1.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.showInfoToMusic_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.showInfoToMusic_2)
        self.showInfoToMusic_2.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.showInfoToMusic_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.showInfoToMusic_3)
        self.showInfoToMusic_3.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.showInfoToMusic_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.showInfoToMusic_4)
        self.showInfoToMusic_4.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))


        #Create buttons
            #initialization
        self.PlayBtn = QPushButton(Dialog)
        self.StopBtn = QPushButton(Dialog)
        self.BreakBtn = QPushButton(Dialog)
        self.NextBtn = QPushButton(Dialog)
        self.PrevBtn = QPushButton(Dialog)
        self.shuffleBtn = QPushButton(Dialog)


            #Show buttons
        self.PlayBtn.setGeometry(QtCore.QRect(245, 630, 60, 60))
        self.PlayBtn.setStyleSheet('''background: transparent;
                                         border-image: url(Play.png) ''')

        self.StopBtn.setGeometry(QtCore.QRect(190, 635, 55, 55))
        self.StopBtn.setStyleSheet('''background: transparent;
                                         border-image: url(Stop.png)''')


        self.BreakBtn.setGeometry(QtCore.QRect(305, 635, 55, 55))
        self.BreakBtn.setStyleSheet('''background: transparent;
                                         border-image: url(Break.png) ''')

        self.NextBtn.setGeometry(QtCore.QRect(355, 635, 55, 55))
        self.NextBtn.setStyleSheet('''background: transparent;
                                         border-image: url(Next_song.png) ''')

        self.PrevBtn.setGeometry(QtCore.QRect(140, 635, 55, 55))
        self.PrevBtn.setStyleSheet('''background: transparent;
                                         border-image: url(Prev_song.png) ''')

        self.shuffleBtn.setGeometry(QtCore.QRect(90, 635, 55, 55))
        self.shuffleBtn.setStyleSheet('''background: transparent;
                                            border-image: url(Shuffle_.png) ''')



        # Events
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.RecommendedDataBase.triggered.connect(self.connect_list)

        self.exitAction.triggered.connect(self.quit_trigger)
        self.openAction.triggered.connect(self.file_open)
        self.openActions.triggered.connect(self.addFiles)

        self.PlayBtn.clicked.connect(self.playMusic)
        self.BreakBtn.clicked.connect(self.stopMusic)
        self.StopBtn.clicked.connect(self.pauseMusic)

        self.PrevBtn.clicked.connect(self.prevSong)
        self.shuffleBtn.clicked.connect(self.shufflelist)
        self.NextBtn.clicked.connect(self.nextSong)

        self.loadBackgroung.triggered.connect(self.LoadYourBackground)
        self.changeBlack.triggered.connect(self.ChangeBlackTheme)
        self.changeWhite.triggered.connect(self.ChangeWhiteTheme)

        self.Developer.triggered.connect(self.AboutDeveloper)
        self.Program.triggered.connect(self.AboutProgram)
        self.Help_.triggered.connect(self.Help)

        self.ChangeBlackTheme()

        QtCore.QMetaObject.connectSlotsByName(Dialog)


    # Triggered function
    def AboutDeveloper(self):
        textOnDev = open('Developer.txt').read()
        self.msgBox.setStyleSheet('QMessageBox {background-image: url(BlackFont.png)}')
        self.msgBox.setText('About Developer')
        self.msgBox.setInformativeText(textOnDev)
        self.msgBox.setStandardButtons(QMessageBox.Close)
        self.msgBox.show()

    def AboutProgram(self):
        TextOnDev = open('Program.txt').read()
        self.msgBox.setStyleSheet('QMessageBox {background-image: url(BlackFont.png)}')
        self.msgBox.setText('About Program')
        self.msgBox.setInformativeText(TextOnDev)
        self.msgBox.setStandardButtons(QMessageBox.Close)
        self.msgBox.show()

    def Help(self):
        TextOnDev = open('Help.txt').read()
        self.msgBox.setStyleSheet('QMessageBox {background-image: url(BlackFont.png)}')
        self.msgBox.setText('Help')
        self.msgBox.setInformativeText(TextOnDev)
        self.msgBox.setStandardButtons(QMessageBox.Close)
        self.msgBox.show()

    def connect_list(self):
        self.w2 = Window2()
        dic_music = MusicParser.parse()
        x = 550
        y = 50
        for i, j in dic_music.items():
            #h = QLabel(self.w2)
            #h.setGeometry(10,0, x,y)
            verticalLayoutWidget = QtWidgets.QWidget(self.w2)
            verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, x, y))
            verticalLayout = QtWidgets.QVBoxLayout(verticalLayoutWidget)
            verticalLayout.setContentsMargins(0, 0, 0, 0)
            left_label = QLabel(verticalLayoutWidget)
            verticalLayout.addWidget(left_label)
            left_label.setFont(QtGui.QFont("Times", 9, QtGui.QFont.Bold))
            left_label.setText(i + ' - ' + j)
            y += 60

        self.w2.show()

    def position_changed(self, position):
        self.songSlider.setValue(position)
        self.timeInStart.setText(str(time.strftime("%M:%S", time.gmtime(position / 1000))))

    def duration_changed(self, duration):
        self.songSlider.setRange(0, duration)

    def set_position(self, position):
        self.player.setPosition(position)

    def quit_trigger(self):
        qApp.quit()

    def file_open(self):
        self.song = QFileDialog.getOpenFileName(self, "Open Song", "", "Sound Files (*.mp3 *.ogg *.wav *.m4a)")
        if self.song[0] != '':
            self.PlayerIsActive = 1
            url = QUrl.fromLocalFile(self.song[0])
            if self.playlist.mediaCount() == 0:
                self.playlist.addMedia(QMediaContent(url))
                self.player.setPlaylist(self.playlist)
                self.player.play()
                self.userAction = 1

            else:
                self.playlist.addMedia(QMediaContent(url))

        if self.PlayerIsActive == 1:
            self.showImage()
            self.ShowInfoAboutSong()
            self.showSlider()

    def showSlider(self):
        self.songSlider.setMaximum(self.long)

    def showImage(self):
        self.audioFile = mutagen.File(self.song[0])
        pixmap_1 = QPixmap('Plug_2.png').scaled(300, 300)
        try:
            photo = self.audioFile.tags.getall('APIC')[0].data
            pixmap = QPixmap()
            pixmap.loadFromData(photo)
            pixmap.scaled(300, 300)
            self.PictureAlbum.setPixmap(pixmap)
        except IndexError:
            self.PictureAlbum.setPixmap(pixmap_1)


    def ShowInfoAboutSong(self):
        #Open song in mutagen
        audioFile = mutagen.File(self.song[0])
        #Create time label (all time song)
        self.long = audioFile.info.length

        #Open all info about song and editing
        singer = audioFile.tags.getall('TPE1')
        song_title = audioFile.tags.getall('TIT2')
        YearOfSong = audioFile.tags.getall('TDRC')
        Bitrate = (audioFile.info.bitrate) // 1000
        singer = str(singer[0])
        song_title = str(song_title[0])

        #show all info on labels
        try:
            self.AllTimeSong.setText(str(time.strftime("%M:%S", time.gmtime(round(self.long)))))
            self.showInfoToMusic_1.setToolTip(singer.encode('latin1').decode('cp1251'))
            self.showInfoToMusic_2.setToolTip(song_title.encode('latin1').decode('cp1251'))
            self.showInfoToMusic_1.setText(singer.encode('latin1').decode('cp1251'))
            self.showInfoToMusic_2.setWordWrap(True)
            self.showInfoToMusic_2.setText(song_title.encode('latin1').decode('cp1251'))
            self.showInfoToMusic_2.setWordWrap(True)
            self.showInfoToMusic_3.setText(str(YearOfSong[0]))
            self.showInfoToMusic_4.setText(str(Bitrate) + ' kbps')

        except IndexError:
            self.showInfoToMusic.setText('')
        except UnicodeEncodeError:
            self.showInfoToMusic_2.setText(song_title)
            self.showInfoToMusic_1.setText(singer)


    def show_more_music(self):
        try:
            self.audioFile = mutagen.File(self.sp_songs[self.playlist.currentIndex()])
            pixmap_1 = QPixmap('Plug_2.png').scaled(300, 300)
            try:
                photo = self.audioFile.tags.getall('APIC')[0].data
                pixmap = QPixmap()
                pixmap.loadFromData(photo)
                pixmap.scaled(300, 300)
                self.PictureAlbum.setPixmap(pixmap)
            except IndexError:
                self.PictureAlbum.setPixmap(pixmap_1)

        except IndexError:
            pass
        try:
            self.index = 0
            audioFile = mutagen.File(self.sp_songs[self.playlist.currentIndex()])
            self.long = audioFile.info.length
            singer = audioFile.tags.getall('TPE1')
            song_title = audioFile.tags.getall('TIT2')
            YearOfSong = audioFile.tags.getall('TDRC')
            Bitrate = (audioFile.info.bitrate) // 1000
            singer = str(singer[0])
            song_title = str(song_title[0])
            try:
                self.AllTimeSong.setText(str(time.strftime("%M:%S", time.gmtime(round(self.long)))))
                self.showInfoToMusic_1.setToolTip(singer.encode('latin1').decode('cp1251'))
                self.showInfoToMusic_2.setToolTip(song_title.encode('latin1').decode('cp1251'))
                self.showInfoToMusic_1.setText(singer.encode('latin1').decode('cp1251'))
                self.showInfoToMusic_2.setWordWrap(True)
                self.showInfoToMusic_2.setText(song_title.encode('latin1').decode('cp1251'))
                self.showInfoToMusic_2.setWordWrap(True)
                self.showInfoToMusic_3.setText(str(YearOfSong[0]))
                self.showInfoToMusic_4.setText(str(Bitrate) + ' kbps')
            except IndexError:
                self.showInfoToMusic.setText('')
            except UnicodeEncodeError:
                self.showInfoToMusic_2.setText(song_title)
                self.showInfoToMusic_1.setText(singer)
        except IndexError:
            pass

    def addFiles(self):
        if self.playlist.mediaCount() != 0:
            self.folderIterator()
        else:
            self.folderIterator()
            self.player.setPlaylist(self.playlist)
            self.player.playlist().setCurrentIndex(0)
            self.player.play()
            self.userAction = 1
            self.PlayerIsActive = 1
            self.show_more_music()
            self.playlist.currentIndexChanged.connect(self.show_more_music)


    def folderIterator(self):
        folderChosen = QFileDialog.getExistingDirectory(self, 'Open Music Folder', '')
        if folderChosen != None:
            it = QDirIterator(folderChosen)
            it.next()
            self.sp_songs = []
            while it.hasNext():
                if it.fileInfo().isDir() == False and it.filePath() != '.':
                    fInfo = it.fileInfo()
                    if fInfo.suffix() in ('mp3', 'ogg', 'wav', 'm4a'):
                        self.sp_songs.append(it.filePath())
                        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))
                it.next()
            if it.fileInfo().isDir() == False and it.filePath() != '.':
                self.sp_songs.append(it.filePath())
                fInfo = it.fileInfo()
                if fInfo.suffix() in ('mp3', 'ogg', 'wav', 'm4a'):
                    self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))


    def ChangeBlackTheme(self):
        oImage = QImage("BlackFont.png")
        sImage = oImage.scaled(QtCore.QSize(self.width, self.height))
        self.palette.setBrush(QPalette.Window, QBrush(sImage))
        self.palette.setColor(QPalette.Text, Qt.white)
        self.palette.setColor(QPalette.WindowText, Qt.white)
        self.palette.setColor(QPalette.ToolTipText, Qt.white)
        QApplication.setPalette(self.palette)


    def ChangeWhiteTheme(self):
        oImage = QImage("WhiteFont_.jpg")
        sImage = oImage.scaled(QtCore.QSize(self.width, self.height))
        self.palette.setBrush(QPalette.Window, QBrush(sImage))
        self.palette.setColor(QPalette.Text, Qt.black)
        self.palette.setColor(QPalette.WindowText, Qt.black)
        self.palette.setColor(QPalette.ToolTipText, Qt.black)
        QApplication.setPalette(self.palette)


    def LoadYourBackground(self):
        font = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.JPEG )")
        oImage = QImage(font[0])
        sImage = oImage.scaled(QtCore.QSize(self.width, self.height))
        self.palette.setBrush(QPalette.Window, QBrush(sImage))
        self.palette.setColor(QPalette.Text, Qt.white)
        self.palette.setColor(QPalette.WindowText, Qt.white)
        self.palette.setColor(QPalette.ToolTipText, Qt.white)
        QApplication.setPalette(self.palette)


    def playMusic(self):
        if self.playlist.mediaCount() == 0:
            self.file_open()

        elif self.playlist.mediaCount() != 0:
            self.player.play()
            self.userAction = 1
            self.PlayerIsActive = 1

    def pauseMusic(self):
        self.userAction = 2
        self.player.pause()
        self.PlayerIsActive = 0

    def stopMusic(self):
        self.PlayerIsActive = 0
        self.userAction = 0
        self.player.stop()
        self.playlist.clear()

    def changeVolume(self, value):
        self.player.setVolume(value)

    def prevSong(self):
        if self.playlist.mediaCount() == 0:
            self.file_open()
        elif self.playlist.mediaCount() != 0:
            self.player.playlist().previous()
            try:
                self.show_more_music()
            except AttributeError:
                pass

    def shufflelist(self):
        if self.playlist.mediaCount() == 0:
            self.file_open()
        elif self.playlist.mediaCount() != 0:
            try:
                self.show_more_music()
                self.playlist.shuffle()
            except AttributeError:
                pass

    def nextSong(self):
        if self.playlist.mediaCount() == 0:
            self.file_open()
        elif self.playlist.mediaCount() != 0:
            try:
                self.player.playlist().next()
                self.show_more_music()
            except AttributeError:
                pass



if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()

    sys.exit(app.exec_())


