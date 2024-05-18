import mysql.connector
import logging


class MusicDao:
    def __init__(self):
        self.connection = self.connect_mysql()
        self.cursor = self.connection.cursor()

    def connect_mysql(self):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='musicplayer'
        )
        return connection

    def create_database(self):
        con = self.connect_mysql()
        cursor = con.cursor()
        cursor.execute('create database if not exists musicplayer')
        cursor.execute('use musicplayer')
        print('Cơ sở dữ liệu là ', 'musicplayer')
        cursor.execute(
            'create table if not exists music (id int(11) primary key auto_increment,song_name varchar(255), singer_name varchar(255), genre varchar(100),mp3 varchar(255),img varchar(255))')
        return con

    def insert_music(self, name, singer, genre, mp3, img, con):
        cursor = con.cursor()
        cursor.execute("INSERT INTO music (song_name, singer_name, genre, mp3, img) VALUES (%s, %s, %s, %s, %s)",
                       (name, singer, genre, mp3, img))
        con.commit()
        cursor.close()

    def delete_music(self, id):
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM music WHERE id=%s", (id,))
            count = cursor.rowcount
            self.connection.commit()
            cursor.close()
            if count > 0:
                print("Xóa thành công")
            else:
                print("Không có dòng nào được xóa với ID đã cho")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            print("Lỗi xảy ra khi xóa âm nhạc")

    def show_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM music")
        records = cursor.fetchall()
        cursor.close()
        return records

    def get_music_file_path(self, song_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT mp3 FROM music WHERE id = %s", (song_id,))
            result = cursor.fetchone()
            if result:
                music_file_path = result[0]
                return music_file_path
            else:
                print("Không tìm thấy bản ghi với ID đã cho.")
                return None
        except Exception as e:
            print(f"Lỗi khi lấy đường dẫn tệp nhạc từ cơ sở dữ liệu: {e}")
            return None
        finally:
            cursor.close()

    def get_image_file_path(self, song_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT img FROM music WHERE id = %s", (song_id,))
            result = cursor.fetchone()
            if result:
                img_file_path = result[0]
                return img_file_path
            else:
                print("Không tìm thấy bản ghi với ID đã cho.")
                return None
        except Exception as e:
            print(f"Lỗi khi lấy đường dẫn tệp nhảnh từ cơ sở dữ liệu: {e}")
            return None
        finally:
            cursor.close()

    def search_music(self, search_txt):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM music WHERE song_name LIKE %s OR singer_name LIKE %s OR genre LIKE %s", (f"%{search_txt}%", f"%{search_txt}%", f"%{search_txt}%"))
            records = cursor.fetchall()
            cursor.close()
            return records
        except Exception as e:
            print(f"Lỗi khi tìm kiếm âm nhạc: {e}")
            return None

    # def search_music(con):
    #     search_term = input("Nhập mã Nhạc hoặc tên Nhạc cần tìm: ")
    #     cursor = con.cursor()
    #     cursor.execute("SELECT * FROM music WHERE id = %s OR song_name LIKE %s",
    #                    (search_term, '%' + search_term + '%'))
    #     records = cursor.fetchall()
    #     if records:
    #         print("---KẾT QUẢ TÌM KIẾM---")
    #         for r in records:
    #             print(r[0], "\t", r[1], "\t", r[2], "\t", r[3], "\t", r[4],"\t", r[5])
    #     else:
    #         print("Không tìm thấy bài nhạc nào với thông tin bạn đã nhập.")
    #     cursor.close()
    #
    #
    # def search_music_by_name(con):
    #     search_term = input("Nhập tên bài nhạc cần tìm: ")
    #     cursor = con.cursor()
    #     cursor.execute("SELECT * FROM music WHERE song_name LIKE %s", ('%' + search_term + '%',))
    #     records = cursor.fetchall()
    #     if records:
    #         print("---KẾT QUẢ TÌM KIẾM---")
    #         for r in records:
    #             print(r[0], "\t", r[1], "\t", r[2], "\t", r[3], "\t", r[4],"\t", r[5])
    #     else:
    #         print("Không tìm thấy bài nhạc với tên bạn đã nhập.")
    #     cursor.close()

    def update_music(self, music_id, name=None, singer=None, genre=None, mp3=None, img=None):
        cursor = self.connection.cursor()

        # Xây dựng câu lệnh SQL UPDATE dựa trên các tham số được cung cấp
        sql = "UPDATE music SET "

        # Duyệt qua các tham số và thêm vào câu lệnh SQL nếu giá trị không phải là None
        updates = []
        if name is not None:
            updates.append(f"song_name = '{name}'")
        if singer is not None:
            updates.append(f"singer_name = '{singer}'")
        if genre is not None:
            updates.append(f"genre = '{genre}'")
        if mp3 is not None:
            updates.append(f"mp3 = '{mp3}'")
        if img is not None:
            updates.append(f"img = '{img}'")

        # Nối các phần của câu lệnh UPDATE lại với nhau, sử dụng dấu phẩy để phân tách
        sql += ", ".join(updates)

        # Thêm điều kiện WHERE để chỉ cập nhật bản ghi cụ thể
        sql += f" WHERE id = {music_id}"

        try:
            cursor.execute(sql)
            self.connection.commit()
            print("Cập nhật thông tin bài nhạc thành công.")
        except Exception as e:
            print(f"Lỗi khi cập nhật dữ liệu: {str(e)}")
        finally:
            cursor.close()

# print("-------------CHƯƠNG TRÌNH CHÍNH-----------------")
# music_dao = MusicDao()
# music_dao.create_database()
#
# while True:
#     print("1. Nhập bài nhạc")
#     print("2. Hiển thị tất cả bài nhạc")
#     print("3. Xóa bài nhạc")
#     print("4. Tìm kiếm bài nhạc theo mã hoặc tên")
#     print("5. Tìm kiếm bài nhạc theo tên")
#     print("6. Sửa thông tin bài nhạc")
#     print("7. Thoát")
#     choose = input("Chọn một chức năng:")
#
#     if choose == "1":
#         name = input("Nhập tên bài nhạc: ")
#         singer = input("Nhập tên ca sĩ: ")
#         genre = input("Nhập thể loại nhạc: ")
#         mp3 = input("Nhập đường dẫn file mp3: ")
#         img = input("Nhập đường dẫn file ảnh: ")
#         music_dao.insert_music(None, name, singer, genre, mp3, img)
#     elif choose == "2":
#         records = music_dao.show_all()
#         if records:
#             print("---DANH SÁCH BÀI NHẠC---")
#             for r in records:
#                 print(r[0], "\t", r[1], "\t", r[2], "\t", r[3], "\t", r[4], "\t", r[5])
#         else:
#             print("Không có bài nhạc nào trong cơ sở dữ liệu.")
#     elif choose == "3":
#         id = input("Nhập mã bài nhạc cần xóa:")
#         music_dao.delete_music(id)
#     elif choose == "4":
#         music_dao.search_music()
#     elif choose == "5":
#         music_dao.search_music_by_name()
#     elif choose == "6":
#         music_dao.update_music()
#     elif choose == "7":
#         break
#     else:
#         print("Bạn chọn sai rồi")
#
# print("KẾT THÚC CHƯƠNG TRÌNH")



