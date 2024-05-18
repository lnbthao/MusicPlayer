
import io
import json
import os
import random
import socket
import tempfile
import threading

from PIL import Image
import pygame
from PIL.ImageQt import ImageQt

from PyQt6 import QtCore, QtGui, QtWidgets

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QPushButton, QSlider
from pygame import time
from qtawesome import icon
import base64
global time
time = 0

class Ui_MainWindow(object):


    def __init__(self):
        self.next = None
        self.slider_time = QSlider(QtCore.Qt.Orientation.Horizontal) # mới thêm
        self.prev = None
        self.is_playing = False
        self.arrList = []
        self.selected_song_id = None
        self.current_song_id = None
        self.paused_pos = None
        self.loop_enabled = False
        self.ngauNhien = False
        self.random_looping_enabled = False


        pygame.init()
        # sẽ khởi tạo mô-đun mixer của pygame
        pygame.mixer.init()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        self.id = None


        self.main = QtWidgets.QWidget(parent=MainWindow)
        self.main.setObjectName("main")

        self.frame_menu = QtWidgets.QFrame(parent=self.main)
        self.frame_menu.setEnabled(True)
        self.frame_menu.setGeometry(QtCore.QRect(0, 0, 250, 701))
        self.frame_menu.setAutoFillBackground(False)
        self.frame_menu.setStyleSheet("background-color: #222;")
        self.frame_menu.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_menu.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_menu.setObjectName("frame_menu")

        self.menu = QtWidgets.QFrame(parent=self.main)
        self.menu.setEnabled(True)
        self.menu.setGeometry(QtCore.QRect(10, 10, 230, 681))
        self.menu.setAutoFillBackground(False)
        self.menu.setStyleSheet("background-color: #333; border-radius: 20px;")
        self.menu.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.menu.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.menu.setObjectName("menu")

        self.lb_Title = QtWidgets.QLabel(parent=self.menu)
        self.lb_Title.setGeometry(QtCore.QRect(30, 210, 181, 81))
        self.lb_Title.setStyleSheet("color: white; font: 900 23pt \"Trebuchet MS\";")
        self.lb_Title.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.lb_Title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lb_Title.setObjectName("lb_Title")

        self.btn_User1 = QtWidgets.QPushButton(parent=self.menu)
        self.btn_User1.setGeometry(QtCore.QRect(10, 400, 211, 71))
        self.btn_User1.setStyleSheet("color: rgb(0,0,0); background-color: rgb(31, 223, 100); border-radius: 30px; font: 900 16pt \"Trebuchet MS\"; ")
        self.btn_User1.setObjectName("btn_User1")


        self.lb_titleIMG = QtWidgets.QLabel(parent=self.menu)
        self.lb_titleIMG.setGeometry(QtCore.QRect(13, 15, 206, 191))
        self.lb_titleIMG.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lb_titleIMG.setText("")
        pixmap = QPixmap(r"D:\1.SGU\MaNguonMo\Project\MusicPlayer\Admin\logo\logo_1.jpg")
        self.lb_titleIMG.setPixmap(pixmap)
        self.lb_titleIMG.setScaledContents(True)
        self.lb_titleIMG.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.lb_titleIMG.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lb_titleIMG.setObjectName("lb_titleIMG")


        self.frame_User_1 = QtWidgets.QFrame(parent=self.main)
        self.frame_User_1.setGeometry(QtCore.QRect(250, 0, 850, 700))
        self.frame_User_1.setStyleSheet("background-color: #222;\n"
                                         "")
        self.frame_User_1.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_User_1.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_User_1.setObjectName("frame_User_1")

        self.frame_SelectSong = QtWidgets.QFrame(parent=self.frame_User_1)
        self.frame_SelectSong.setGeometry(QtCore.QRect(10, 10, 731, 391))
        self.frame_SelectSong.setStyleSheet("background-color: #333; border-radius: 20px;")
        self.frame_SelectSong.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_SelectSong.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_SelectSong.setObjectName("frame_SelectSong")

        self.cb_genre = QtWidgets.QComboBox(parent=self.frame_SelectSong)
        self.cb_genre.setGeometry(QtCore.QRect(430, 10, 181, 31))
        self.cb_genre.setStyleSheet("color: white; background-color: #444; font: 900 10pt \"Trebuchet MS\"; border-radius: 0px;")
        self.cb_genre.setObjectName("cb_genre")
        self.cb_genre.addItems(["Tất cả","Việt", "Hàn", "Âu Mỹ"])
        self.cb_genre.activated.connect(self.handle_genre_selection)

        self.btn_find = QtWidgets.QPushButton(parent=self.frame_SelectSong)
        self.btn_find.setGeometry(QtCore.QRect(330, 10, 91, 31))
        self.btn_find.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";\n"
"color: rgb(0,0,0); background-color: rgb(31, 223, 100); border-radius: 15px; font: 900 12pt \"Trebuchet MS\";")
        self.btn_find.setObjectName("btn_find")
        self.btn_find.clicked.connect(self.findData)

        self.tf_find = QtWidgets.QLineEdit(parent=self.frame_SelectSong)
        self.tf_find.setGeometry(QtCore.QRect(10, 10, 311, 31))
        self.tf_find.setStyleSheet("color: white; background-color: #444; border-radius: 15px; font: 900 10pt \"Trebuchet MS\";")
        self.tf_find.setText("")
        self.tf_find.setObjectName("tf_find")

        self.scrollArea = QtWidgets.QScrollArea(parent=self.frame_SelectSong)
        self.scrollArea.setGeometry(QtCore.QRect(15, 60, 701, 321))
        self.scrollArea.setStyleSheet("background-color: #333; border-radius: 0px;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 709, 319))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        # Thêm một QVBoxLayout vào scrollAreaWidgetContents
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setObjectName("scrollLayout")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)


        self.frame_PlayMusic = QtWidgets.QFrame(parent=self.frame_User_1)
        self.frame_PlayMusic.setGeometry(QtCore.QRect(10, 410, 731, 281))
        self.frame_PlayMusic.setStyleSheet("background-color: #333; border-radius: 20px;")
        self.frame_PlayMusic.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_PlayMusic.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_PlayMusic.setObjectName("frame_PlayMusic")

        self.lb_image_2 = QtWidgets.QLabel(parent=self.frame_PlayMusic)
        self.lb_image_2.setGeometry(QtCore.QRect(50, 10, 200, 200))
        self.lb_image_2.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lb_image_2.setText("")
        self.lb_image_2.setObjectName("lb_image_2")

        self.slider_time = QtWidgets.QSlider(parent=self.frame_PlayMusic)
        self.slider_time.setGeometry(QtCore.QRect(341, 250, 320, 22))
        self.slider_time.setOrientation(QtCore.Qt.Orientation.Horizontal)

        self.slider_time.setStyleSheet("""
                    QSlider::groove:horizontal {
                        border: none;
                        height: 8px;
                        background: #404040;
                        border-radius: 4px;
                    }

                    QSlider::sub-page:horizontal {
                        background: #1db954;
                        border-radius: 4px;
                    }

                    QSlider::add-page:horizontal {
                        background: #404040;
                        border-radius: 4px;
                    }

                    QSlider::handle:horizontal {
                        background: #fff;
                        border: none;
                        width: 12px;
                        height: 12px;
                        margin: -3px 0;
                        border-radius: 6px;
                    }

                    QSlider::handle:horizontal:hover {
                        background: #1ed760;
                    }

                    QSlider::handle:horizontal:focus {
                        background: #1db954;
                    }

                    /* Thêm border-radius cho đầu slider */
                     QSlider::add-page:horizontal:after {
                        border-radius: 6px;
                    }

                    QSlider::sub-page:horizontal:before {
                        border-radius: 6px;
                    }
                """)

        self.slider_time.setMinimum(0)  # Thời gian tối thiểu là 0
        self.slider_time.setMaximum(100)  # Thời gian tối đa có thể là bất kỳ giá trị nào
        # self.slider_time.setValue(0)  # Thời gian ban đầu là 0
        self.slider_time.sliderMoved.connect(self.on_time_slider_changed)
        self.slider_time.sliderReleased.connect(self.on_slider_released)# Kết nối sự kiện
        self.slider_time.setObjectName("slider_time")

        self.lb_current_time = QtWidgets.QLabel(self.frame_PlayMusic)
        self.lb_current_time.setGeometry(QtCore.QRect(290, 250, 50, 22))
        self.lb_current_time.setStyleSheet("color: white;")
        self.lb_current_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.lb_current_time.setObjectName("lb_current_time")

        self.lb_total_time = QtWidgets.QLabel(self.frame_PlayMusic)  # Tạo nhãn mới cho tổng thời gian
        self.lb_total_time.setGeometry(QtCore.QRect(660, 250, 50, 22))  # Đặt vị trí và kích thước cho nhãn
        self.lb_total_time.setStyleSheet("color: white;")
        self.lb_total_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.lb_total_time.setObjectName("lb_total_time")

        self.timer = QtCore.QTimer()

        # Thiết lập timer để cập nhật mỗi giây
        self.timer.timeout.connect(self.update_time_slider)

        # Thiết lập trạng thái ban đầu của UI
        self.slider_time.setMinimum(0)
        # self.slider_time.setValue(time)

        self.volume_slider = QtWidgets.QSlider(parent=self.frame_PlayMusic)
        self.volume_slider.setGeometry(QtCore.QRect(630, 10, 16, 161))
        self.volume_slider.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)  # Giá trị mặc định là 50
        self.volume_slider.valueChanged.connect(self.on_volume_slider_changed)
        self.volume_slider.setObjectName("volume_slider")

        self.btn_play = QPushButton(parent=self.frame_PlayMusic)
        self.btn_play.setGeometry(QtCore.QRect(440, 180, 101, 61))
        self.btn_play.setObjectName("btn_play")
        self.btn_play.setIcon(icon("fa.play-circle", color='white'))
        self.btn_play.setIconSize(QtCore.QSize(70, 70))
        self.btn_play.clicked.connect(self.play_or_stop)

        self.btn_next = QtWidgets.QPushButton(parent=self.frame_PlayMusic)
        self.btn_next.setGeometry(QtCore.QRect(540, 190, 51, 41))
        self.btn_next.setObjectName("btn_next")
        self.btn_next.setIcon(icon("fa.step-forward", color='white'))
        self.btn_next.setIconSize(QtCore.QSize(50, 50))
        self.btn_next.clicked.connect(self.play_next_song)

        self.btn_pre = QtWidgets.QPushButton(parent=self.frame_PlayMusic)
        self.btn_pre.setGeometry(QtCore.QRect(390, 190, 51, 41))
        self.btn_pre.setObjectName("btn_pre")
        self.btn_pre.setIcon(icon("fa.step-backward", color='white'))
        self.btn_pre.setIconSize(QtCore.QSize(50, 50))
        self.btn_pre.clicked.connect(self.play_prev_song)

        self.btn_loop = QtWidgets.QPushButton(parent=self.frame_PlayMusic)
        self.btn_loop.setGeometry(QtCore.QRect(320, 190, 51, 41))
        self.btn_loop.setObjectName("btn_loop")
        self.btn_loop.setIcon(icon("fa.repeat", color='white'))  # Thay đổi biểu tượng thành biểu tượng vòng lặp
        self.btn_loop.setIconSize(QtCore.QSize(50, 50))
        self.btn_loop.clicked.connect(self.toggle_looping)

        self.btn_random_loop = QtWidgets.QPushButton(parent=self.frame_PlayMusic)
        self.btn_random_loop.setGeometry(QtCore.QRect(620, 190, 51, 41))
        self.btn_random_loop.setObjectName("btn_random_loop")
        self.btn_random_loop.setIcon(icon("fa.random", color='white'))  # Biểu tượng vòng lặp ngẫu nhiên
        self.btn_random_loop.setIconSize(QtCore.QSize(50, 50))
        self.btn_random_loop.clicked.connect(self.toggle_random_looping)
        
        self.lb_title_2 = QtWidgets.QLabel(parent=self.frame_PlayMusic)
        self.lb_title_2.setGeometry(QtCore.QRect(50, 220, 240, 41))
        self.lb_title_2.setStyleSheet("color: white; font: 900 12pt \"Trebuchet MS\";")
        self.lb_title_2.setObjectName("lb_title_2")

        self.lb_gif = QtWidgets.QLabel(parent=self.frame_PlayMusic)
        self.lb_gif.setGeometry(QtCore.QRect(390, 10, 201, 161))
        self.lb_gif.setStyleSheet("background-color:rgb(255, 255, 255)")
        pixmap = QPixmap(r"D:\1.SGU\MaNguonMo\Project\MusicPlayer\Admin\logo\gif.jpg")
        self.lb_gif.setPixmap(pixmap)
        self.lb_gif.setScaledContents(True)


        # Tạo một QMovie từ đường dẫn tệp ảnh GIF
        # movie = QtGui.QMovie(r"D:\OSSD_Phieu\DoAn\MusicPlayer\Admin\logo\eyebrow.gif")
        # # Đặt QMovie làm hình ảnh của QLabel
        # self.lb_gif.setMovie(movie)
        # # Bắt đầu phát QMovie
        # movie.start()
        MainWindow.setCentralWidget(self.main)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_find.setText(_translate("MainWindow", "Find"))
        self.lb_title_2.setText(_translate("MainWindow", "NAME"))
        self.lb_Title.setText(_translate("MainWindow", "Chill N Free"))
        self.btn_User1.setText(_translate("MainWindow", "PLAYLIST"))
        self.lb_current_time.setText(_translate("MainWindow", "0:00"))


    def on_volume_slider_changed(self, value):
        # Chuyển đổi giá trị từ phần trăm thành khoảng từ 0.0 đến 1.0
        volume = value / 100.0
        pygame.mixer.music.set_volume(volume)

    def handle_genre_selection(self):
        arrFind = []
        selected_genre = self.cb_genre.currentText()
        if selected_genre == 'Tất cả':
            self.update_music_list(self.arrList)
        else:
            for item in self.arrList:
                if item['type'] == selected_genre:
                    arrFind.append(item)
            self.update_music_list(arrFind)

    def findData(self):
        arrFind = []
        for item in self.arrList:
            data = self.tf_find.text()
            if data.lower() in item['name'].lower():
                arrFind.append(item)
        self.update_music_list(arrFind)

#Cập nhật danh sách nhạc lên QListWidget.
    def update_music_list(self, arr):
        # Xóa các widget cũ
        while self.scrollLayout.count():
            widget = self.scrollLayout.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()
        # Tạo layout cho container chứa tất cả các widget bài hát
        container_layout = QtWidgets.QVBoxLayout()
        for item in arr:
            song_id = item['id']
            song_name = item['name']
            singer = item['singer']
            genre = item['type']

            image_file = item['image_path']

            # Tạo QWidget cho mỗi bài hát
            widget = QtWidgets.QWidget()
            widget.setFixedHeight(100)
            # Tạo layout cho widget của từng bài hát
            widget_layout = QtWidgets.QHBoxLayout(widget)
            # Tạo các QLabel để hiển thị thông tin bài hát
            lb_ID = QtWidgets.QLabel(f" {song_id}.")
            lb_song_name = QtWidgets.QLabel(f" {song_name}")
            lb_singer = QtWidgets.QLabel(f" {singer} ")
            lb_genre = QtWidgets.QLabel(f" {genre}")
            # Thiết lập font cho các QLabel
            font = QtGui.QFont("Arial", 10)
            lb_ID.setFont(font)
            lb_song_name.setFont(font)
            lb_singer.setFont(font)

            btn_select = QtWidgets.QPushButton("Select")
            btn_select.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";\n"
            "color: rgb(0,0,0); background-color: rgb(31, 223, 100); border-radius: 5px; font: 900 12pt \"Trebuchet MS\";")
            btn_select.setText("Select")
            btn_select.clicked.connect(lambda _, song_id1=song_id: self.select_song(song_id1,play_music=True))
            # Thêm các QLabel và QPushButton vào layout của widget

            # widget_layout.addWidget(lb_img)
            widget_layout.addWidget(lb_ID)
            widget_layout.addWidget(lb_song_name)
            widget_layout.addWidget(lb_singer)
            widget_layout.addWidget(lb_genre)
            widget_layout.addWidget(btn_select)

            widget.setStyleSheet("background-color: #444; color: white; border-radius: 10px;")
            # Đặt layout cho widget
            widget.setLayout(widget_layout)
            # Thêm widget vào container
            container_layout.addWidget(widget)

        # Tạo container để chứa tất cả các widget bài hát
        container = QtWidgets.QWidget()
        container.setLayout(container_layout)
        # Tạo và cấu hình QScrollArea
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container)
        # Đặt QScrollArea làm layout chính cho scrollAreaWidgetContents
        self.scrollLayout.addWidget(scroll_area)

    def select_song(self, song_id, play_music=False):
        song_info = None
        for item in self.arrList:
            if item['id'] == song_id:
                song_info = [
                    item['id'],
                    item['name'],
                    item['singer'],
                    item['type'],
                    item['image_path']
                ]

        if song_info:
            song_id = song_info[0]
            song_name = song_info[1]
            singer = song_info[2]
            print(song_name)
            print(singer)
            self.lb_title_2.setText(f"{song_name} - {singer}")
            self.selected_song_id=song_id
            print("Id đang được chọn: ",self.selected_song_id)

            if play_music:
                self.play_selected_song(self.selected_song_id, immediate_play=True)
                self.btn_play.setIcon(icon("fa.pause-circle", color='white'))  # Đặt biểu tượng là nút pause
            else:
                self.play_selected_song(self.selected_song_id, immediate_play=False)

    def request_music_list(self):
        host = 'localhost'
        port = 3306
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((host,port))
                # Gửi yêu cầu danh sách nhạc
                client.sendall(b'GET_MUSIC_LIST')
                # Nhận và cập nhật dữ liệu nhạc từ server
                music_list = client.recv(1024).decode('utf-8')
                print("Received music list from server:")
                print(music_list)
                records = music_list.strip().split('\n')
                for record in records:
                    fields = record.strip('()').split(', ')
                    if len(fields) == 5:  # Kiểm tra xem có đúng 5 giá trị trong danh sách không
                        song_id = int(fields[0])
                        song_name = fields[1].strip("'")
                        artist = fields[2].strip("'")
                        genre = fields[3].strip("'")
                        image_path = fields[4].strip("'")

                        song_info = {
                            "id": song_id,
                            "name": song_name,
                            "singer": artist,
                            "type": genre,
                            "image_path": image_path
                        }
                        self.arrList.append(song_info)
                        print(song_info)
                    else:
                        print("Invalid record format:", record)

                # Cập nhật danh sách nhạc lên giao diện người dùng
                self.update_music_list(self.arrList)

                if self.arrList:
                    self.select_song(self.arrList[-1]['id'], False)

        except ConnectionResetError as e:
            print("Kết nối đã bị đóng bởi máy chủ từ xa.")
        except Exception as e:
            print(f"Có lỗi xảy ra: {e}")

    def play_selected_song(self, song_id, immediate_play=False):
        host = 'localhost'
        port = 3306

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((host, port))

                request = f'GET_MUSIC_DATA_{song_id}'
                client.sendall(request.encode())
                print(f"yêu cầu lấy dữ liệu của id: {song_id}")

                pygame.init()
                pygame.mixer.init()

                # Nhận dữ liệu âm nhạc từ server và lưu vào một tệp tạm
                self.music_file_data = tempfile.SpooledTemporaryFile(max_size=10000000)
                self.image_file_data = tempfile.SpooledTemporaryFile(max_size=10000000)

                receiving_music = True
                while True:
                    data = client.recv(1024)
                    if not data:
                        break
                    if b'END_OF_MUSIC' in data:
                        self.music_file_data.write(data.split(b'END_OF_MUSIC')[0])
                        receiving_music = False
                        remaining_data = data.split(b'END_OF_MUSIC')[1]
                        self.image_file_data.write(remaining_data)
                        continue
                    if b'END_OF_IMAGE' in data:
                        self.image_file_data.write(data.split(b'END_OF_IMAGE')[0])
                        break
                    if receiving_music:
                        self.music_file_data.write(data)
                    else:
                        self.image_file_data.write(data)

                self.music_file_data.seek(0)
                self.image_file_data.seek(0)

                # Kiểm tra định dạng tệp trước khi tải vào pygame
                music_bytes = self.music_file_data.read()
                self.music_file_data.seek(0)

                try:
                    sound = pygame.mixer.Sound(io.BytesIO(music_bytes))
                    total_time = sound.get_length()
                except pygame.error as e:
                    print(f"Lỗi định dạng tệp: {e}")
                    return

                pygame.mixer.music.load(io.BytesIO(music_bytes))
                self.current_song_id = song_id

                # Lấy tổng thời lượng bài hát và cập nhật UI
                self.slider_time.setMaximum(int(total_time * 1000))  # Chuyển đổi giây thành milliseconds
                self.lb_total_time.setText(self.format_time(total_time))

                if immediate_play:
                    pygame.mixer.music.play()
                    self.is_playing = True  # Đã bắt đầu phát nhạc
                    self.btn_play.setIcon(icon("fa.pause-circle", color='white'))  # Đặt biểu tượng là nút pause
                    self.timer.start(1000)
                else:
                    self.is_playing = False  # Không phát ngay lập tức
                    self.btn_play.setIcon(icon("fa.play-circle", color='white'))

                # Xử lý dữ liệu hình ảnh
                image_bytes = self.image_file_data.read()
                self.image_file_data.seek(0)
                self.handle_image_data(image_bytes)  # Xử lý hiển thị hình ảnh

        except Exception as e:
            print(f"Error playing selected song: {e}")

    def handle_image_data(self, image_bytes):
        try:
            # Tạo hình ảnh từ dữ liệu nhận được
            image = Image.open(io.BytesIO(image_bytes))
            image.save('temp_image.jpg')
            pixmap = QPixmap('temp_image.jpg')
            self.lb_image_2.setPixmap(pixmap)
            self.lb_image_2.setScaledContents(True)
            print("Dữ liệu hình ảnh đã được xử lý:",image)
        except Exception as e:
            print(f"Lỗi khi xử lý hình ảnh: {e}")

    def stop_music(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            # self.timer.stop() # mới đc thêm
            print("Music stopped.")

    def play_or_stop(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.paused_pos = pygame.mixer.music.get_pos() / 1000.0  # Lưu trữ vị trí hiện tại khi dừng
            self.btn_play.setIcon(icon("fa.play-circle", color='white'))
            self.timer.stop()
        else:
            if self.paused_pos is not None:  # Nếu đã lưu trữ vị trí khi dừng
                pygame.mixer.music.unpause()  # Tiếp tục phát nhạc từ vị trí đó
                self.timer.start(1000)  # Bắt đầu đồng hồ đếm thời gian
                self.btn_play.setIcon(icon("fa.pause-circle", color='white'))
                self.paused_pos = None  # Đặt lại vị trí đã dừng
            else:
                if pygame.mixer.music.get_busy() and pygame.mixer.music.get_pos() > 0:
                    pygame.mixer.music.unpause()  # Nếu nhạc đang tạm dừng và có trong trạng thái phát, tiếp tục phát từ vị trí hiện tại
                else:
                    pygame.mixer.music.play()  # Phát từ đầu
                    self.update_time_slider()  # Cập nhật thanh trượt thời gian
                    self.timer.start(1000)  # Bắt đầu đồng hồ đếm thời gian
                self.btn_play.setIcon(icon("fa.pause-circle", color='white'))
        self.is_playing = not self.is_playing

        threading.Thread(target=self.monitor_music_end).start()

    def monitor_music_end(self):
        while pygame.mixer.music.get_busy():
            pass
        self.btn_play.setIcon(icon("fa.play-circle", color='white'))
        self.is_playing = False

    def get_next_song_id(self, direction='next'):
        if self.current_song_id is not None:
            for index, item in enumerate(self.arrList):
                if item['id'] == self.current_song_id:
                    if direction == 'next':
                        next_index = (index + 1) % len(self.arrList)
                    elif direction == 'pre':
                        next_index = (index - 1) % len(self.arrList)
                    return self.arrList[next_index]['id']
        return None

    def play_next_song(self):
        next_song_id = self.get_next_song_id(direction='next')
        if next_song_id:
            print("id tiếp:", next_song_id)
            self.stop_music()  # Dừng nhạc trước khi phát bài hát tiếp theo
            self.select_song(next_song_id, play_music=True)
            self.selected_song_id = next_song_id

    def play_prev_song(self):
        prev_song_id = self.get_next_song_id(direction='pre')
        if prev_song_id:
            print("Bài hát trước đó:", prev_song_id)
            self.stop_music()  # Dừng nhạc trước khi phát bài hát trước đó
            self.select_song(prev_song_id, play_music=True)
            self.selected_song_id = prev_song_id

    def on_time_slider_changed(self):
        if self.slider_time.isSliderDown():  # Check if the slider is being dragged
            pos = self.slider_time.value() / 1000.0  # Convert milliseconds to seconds
            self.lb_current_time.setText(self.format_time(pos))  # Update the current time display

    def on_slider_released(self):
        # Khi người dùng thả thanh trượt, cập nhật vị trí của bài hát và phát nhạc từ vị trí mới
        pos = self.slider_time.value() / 1000.0
        pygame.mixer.music.play(start=pos)
        self.timer.start(1000)  # Bắt đầu đồng hồ đếm thời gian
        self.is_playing = True  # Đánh dấu là đang phát nhạc
        self.btn_play.setIcon(icon("fa.pause-circle", color='white'))

        # Cập nhật thời gian hiện tại của bài hát và vị trí của thanh trượt

        self.lb_current_time.setText(self.format_time(pos))
        # self.slider_time.setValue(int(pos * 1000))  # Đặt lại vị trí của thanh trượt
        global time
        time = int(pos * 1000)
        self.slider_time.setValue(time)


        if pos >= self.slider_time.maximum() / 1000.0 and not self.loop_enabled:
            self.on_music_end()

        print(
            f"Slider released at position: {self.slider_time.value()} ms, Current time set to: {self.format_time(pos)}")

    def update_time_slider(self):
        # Kiểm tra xem bài hát đã kết thúc chưa
        if not pygame.mixer.music.get_busy():
            self.on_music_end()  # Gọi hàm on_music_end để xử lý sự kiện khi bài hát kết thúc
            return  # Dừng xử lý tiếp theo nếu bài hát đã kết thúc

        if self.is_playing:
            # Lấy vị trí hiện tại của bài hát
            current_pos = pygame.mixer.music.get_pos()

            # Kiểm tra nếu current_pos hợp lệ (khác -1)
            if current_pos != -1:
                current_time = current_pos / 1000.0
                self.slider_time.setValue(int(current_time * 1000))
                self.lb_current_time.setText(self.format_time(current_time))


            else:
                # Xử lý khi current_pos không hợp lệ (có thể log lỗi hoặc đặt giá trị mặc định)
                self.slider_time.setValue(0)
                self.lb_current_time.setText(self.format_time(0))

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds:02}"
    # -----------------------------------------------------------------------------------------------------------

    def toggle_random_looping(self):
        self.random_looping_enabled = not self.random_looping_enabled
        if self.random_looping_enabled:
            self.btn_random_loop.setIcon(icon("fa.random", color='green'))
            # # Nếu lặp lại ngẫu nhiên được bật, gọi hàm play_selected_song với một ID bài hát ngẫu nhiên
            self.ngauNhien = True
            print(self.ngauNhien)
        else:
            # Nếu lặp lại ngẫu nhiên bị tắt, dừng phát nhạc (nếu có)
            self.btn_random_loop.setIcon(icon("fa.random", color='white'))
            self.ngauNhien = False
            print(self.ngauNhien)


    def toggle_looping(self):
        self.loop_enabled = not self.loop_enabled
        if self.loop_enabled:
            self.btn_loop.setIcon(icon("fa.repeat", color='green'))
        else:
            self.btn_loop.setIcon(icon("fa.repeat", color='white'))

    # Sửa đổi phương thức on_music_end để kiểm tra và xử lý việc lặp lại bài hát khi kết thúc

    def on_music_end(self):
        if not pygame.mixer.music.get_busy():
            if self.loop_enabled:  # Nếu chế độ lặp lại được bật
                self.play_selected_song(self.current_song_id, immediate_play=True)  # Phát lại bài hát hiện tại
            else:
                if self.ngauNhien:
                    vitri = random.randint(0,
                                           len(self.arrList) - 1)  # Giả sử self.all_song_ids là danh sách tất cả các ID bài hát
                    id_random = None
                    for index, item in enumerate(self.arrList):
                        if index == vitri:
                            id_random = item['id']
                            break
                    self.select_song(id_random, play_music=True)
                else:
                    self.play_next_song()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # Gọi phương thức request_music_list từ ui (thể hiện của Ui_MainWindow)
    ui.request_music_list()  # Thay client bằng đối tượng kết nối của bạn
    sys.exit(app.exec())
