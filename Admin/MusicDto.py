class MusicDTO:
    def __init__(self, id, name, singer, genre, mp3,img):
        self.id = str(id)
        self.name = str(name)
        self.singer = str(singer)
        self.genre = str(genre)
        self.mp3 = str(mp3)
        self.img = str(img)

# String representation for debugging
    def __str__(self):
        return f"MusicDTO(id='{self.id}', name='{self.name}', singer='{self.singer}', genre='{self.genre}', mp3='{self.mp3}')"