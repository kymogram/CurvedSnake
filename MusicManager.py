from threading import Thread

class MusicManager(Thread):
    
    def __init__(self, file, start=False):
        super(MusicManager, self).__init__()
        self.daemon = True
        self.file = file
        self.must_start = start
    
    def run(self):
        import pyglet
        self.music_player = pyglet.media.Player()
        self.music = pyglet.media.load(self.file)
        self.music_player.queue(self.music)
        if self.must_start:
            self.play()
        pyglet.app.run()
    
    def reset(self):
        self.pause()
        self.music_player.seek(0)
        self.play()
    
    def pause(self):
        self.music_player.pause()
    
    def play(self):
        self.music_player.play()
    
    def changeTrack(self, file):
        import pyglet
        self.file = file
        self.music = pyglet.media.load(self.file)
        self.music_player.queue(self.music)
        self.music_player.next()