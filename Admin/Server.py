
import socket
import threading

from PyQt6.QtCore import pyqtSlot, QThread, pyqtSignal
from qtpy import QtCore

from Admin.MusicBus import MusicBus
from Admin.MusicDao import MusicDao

# Khởi tạo các đối tượng MusicBus và MusicDAO
music_dao = MusicDao()
music_bus = MusicBus(music_dao)



class ServerThread(QtCore.QThread):
    new_connection = QtCore.Signal(str)
    server_stopped = pyqtSignal()

    @pyqtSlot(str)
    def update_label(self, message):
        self.new_connection.emit(message)

    def __init__(self,music_bus,music_dao, parent=None):
        super(ServerThread, self).__init__(parent)
        self.music_dao = music_dao
        self.music_bus = music_bus
        self._running = True

    def run(self):
        host = '172.20.10.3'
        port = 3306

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.bind((host, port))
            server.listen(5)  # Số lượng kết nối đồng thời tối đa
        except Exception as e:
            print(f"Could not bind or listen to port {port}: {e}")
            self.new_connection.emit(f"Could not start server: {e}")
            return

        print("Server is listening...")
        self.new_connection.emit("Server is listening...")

        while self._running:

            try:
                server.settimeout(1)  # Thêm timeout để có thể kiểm tra self._running
                client_socket, client_address = server.accept()
                print(f"Connected with {client_address}")

                # Cập nhật giao diện người dùng
                self.new_connection.emit(f"Connected with {client_address}")

                # Xử lý client trong một luồng riêng biệt
                thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                thread.start()

            except socket.timeout:
                continue  # Quay lại vòng lặp và kiểm tra _running flag
            except Exception as e:
                print(f"Error accepting connections: {e}")
                self.new_connection.emit(f"Error accepting connections: {e}")

        server.close()
        self.server_stopped.emit()  # Phát tín hiệu thông báo server đã dừng

    def quit(self):
        self._running = False
        super(ServerThread, self).quit()


    # Hàm xử lý yêu cầu của client
    def handle_client(self, client_socket):
        try:
            while True:
                # Nhận yêu cầu từ client
                request = client_socket.recv(1024).decode('utf-8')

                if not request:
                    break  # Ngắt kết nối nếu không nhận được yêu cầu nào từ client

                if request == "GET_MUSIC_LIST":
                    self.new_connection.emit(f"SERVER nhận yêu cầu từ client: {request}")
                    # Gọi phương thức để lấy danh sách nhạc từ cơ sở dữ liệu
                    music_list = self.music_bus.get_music_list_from_database()
                    print(music_list)


                    music_list_str = "\n".join([str(music) for music in music_list])

                    client_socket.sendall((music_list_str + '\n').encode('utf-8'))

                    print("Đã cung cấp danh sách nhạc cho client.")
                    self.new_connection.emit("Đã cung cấp danh sách nhạc cho client.")

                elif request.startswith("GET_MUSIC_DATA"):
                    parts = request.split("_")
                    print(parts)
                    if len(parts) >= 2:
                        song_id = int(parts[3])
                        print(song_id)
                    music_file_path = self.music_bus.get_music_file_path(song_id)
                    image_file_path = self.music_bus.get_image_file_path(song_id)
                    print(music_file_path,image_file_path)
                    if music_file_path and image_file_path:
                        try:
                            # Gửi dữ liệu âm nhạc
                            with open(music_file_path, 'rb') as f:
                                while True:
                                    data = f.read(1024)
                                    if not data:
                                        break
                                    # print("Give music data chunk:", len(data))
                                    client_socket.sendall(data)
                            client_socket.sendall(b'END_OF_MUSIC')  # Delimiter cho dữ liệu âm nhạc

                            # Gửi dữ liệu hình ảnh
                            with open(image_file_path, 'rb') as f:
                                while True:
                                    data = f.read(1024)
                                    if not data:
                                        break
                                    print("Give image data chunk:", len(data))
                                    client_socket.sendall(data)
                            client_socket.sendall(b'END_OF_IMAGE')  # Delimiter cho dữ liệu hình ảnh
                        except Exception as e:
                            print(f"Error sending music or image data: {e}")
                        finally:
                            break
                    else:
                        client_socket.sendall(b'Song or image not found')

        except Exception as e:
            print(f"Error handling client request: {e}")
        finally:
            client_socket.close()




