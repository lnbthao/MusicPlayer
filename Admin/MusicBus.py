import base64
import os

import MusicDao
import logging

# Thiết lập cấp độ ghi log
logging.basicConfig(level=logging.DEBUG)
class MusicBus:
    def __init__(self, music_dao):
        self.music_dao = music_dao

    def add_music(self, name, singer, genre, mp3, img, con):
        logging.info("Attempting to add music...")
        self.music_dao.insert_music(name, singer, genre, mp3, img, con)
        logging.info("Music added successfully.")

    def delete_music_by_id(self, id):
        self.music_dao.delete_music(id)

    def update_music(self, music_id, name=None, singer=None, genre=None, mp3=None, img=None):
        self.music_dao.update_music(music_id, name, singer, genre, mp3, img)

    # def get_music_by_id(self, music_id):
    #     return self.music_dao.get_music_by_id(music_id)

    def get_all_music(self):
        return self.music_dao.show_all()

    def get_music_list_from_database(self):
        try:
            music_list = self.music_dao.show_all()
            music_info = []
            for music in music_list:
                 # Assuming music[4] is the image file name
                music_info.append((music[0], music[1], music[2], music[3], music[5]))
            return music_info
        except Exception as e:
            print(f"Error getting music list from database: {e}")
            return []



    def get_music_file_path(self, song_id):
        try:
            # Gọi phương thức từ lớp bus để lấy tên tệp của bài hát
            music_file_name = self.music_dao.get_music_file_path(song_id)
            # Xác định thư mục chứa tệp âm nhạc trong dự án của bạn
            music_directory = os.path.join(r"D:\1.SGU\MaNguonMo\Project\MusicPlayer\Admin\mp3")
            # Tạo đường dẫn tuyệt đối đến tệp âm nhạc
            music_file_path = os.path.join(music_directory, music_file_name)

            if os.path.exists(music_file_path):
                return music_file_path
            else:
                return "Song not found"
        except Exception as e:
            print(f"Error getting music file path: {e}")
            return "Error getting music file path"

    def get_image_file_path(self, song_id):
        try:
            # Gọi phương thức từ lớp bus để lấy tên tệp của hình ảnh
            image_file_name = self.music_dao.get_image_file_path(song_id)
            # Xác định thư mục chứa tệp hình ảnh trong dự án của bạn
            image_directory = os.path.join(r"D:\1.SGU\MaNguonMo\Project\MusicPlayer\Admin\img")
            # Tạo đường dẫn tuyệt đối đến tệp hình ảnh
            image_file_path = os.path.join(image_directory, image_file_name)

            if os.path.exists(image_file_path):
                return image_file_path
            else:
                return "Image not found"
        except Exception as e:
            print(f"Error getting image file path: {e}")
            return "Error getting image file path"

    def __str__(self):
        return f"MusicBus with {len(self.get_all_music())} musics."



if __name__ == "__main__":
    music_dao = MusicDao.MusicDao()
    music_bus = MusicBus(music_dao)


