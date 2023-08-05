import json
import operator
from moviepy.editor import *
from bgeditor.common.utils import cache_file, download_file
from bgeditor.dao.Lyric import Lyric
from PIL import Image
import numpy as np
def create_video(list_comp_data, path_video):
    print('get list')
    arr_comps=[]
    for comp_data in list_comp_data:
        arr_comps.append(Component.convert(comp_data))

    arr_comps.sort(key=lambda obj: obj.index)
    arr_composite = []
    max_duration = 0
    for comp in arr_comps:
        if comp.duration + comp.start_time > max_duration:
            max_duration = comp.duration + comp.start_time
        arr_composite.append(comp.make())
    CompositeVideoClip(arr_composite).subclip(0, max_duration).write_videofile(path_video, fps=24, codec='libx264')


class Component:
    def __init__(self, json_data):
        self.index = json_data['index']
        self.position = json_data['position']
        self.start_time = json_data['startTime']
        self.duration = json_data['duration']
        print("init")
    @staticmethod
    def convert(json_data):
        if json_data['type'] == "text":
            return TextComp(json_data)
        if json_data['type'] == "image":
            return ImageComp(json_data)
        if json_data['type'] == "video":
            return VideoComp(json_data)
        if json_data['type'] == "lyric":
            return LyricComp(json_data)
    def setup(self):
        print('setup')
    def order(self):
        print('order')
    def get_clip(self):
        print('get clip')
    def make(self):
        rs = self.get_clip()
        rs = rs.set_position((self.position['x'], self.position['y']))
        if self.start_time > 0:
            rs = rs.set_start(self.start_time).crossfadein(0.5)
        if self.duration > 0:
            rs = rs.set_duration(self.duration).crossfadeout(0.5)
        if self.position['rotation'] != 0:
            rs = rs.rotate(self.position['rotation'])
        return rs




class TextComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.font_url = json_data['font_url']
        self.font_size = json_data['fontSize']
        self.bg_color = json_data['backgroundColor']
        self.color = json_data['color']
        self.text = json_data['text']
        self.stroke_color = json_data['stroke_color']
        self.stroke_width = json_data['stroke_width']

    def get_clip(self):
        self.font_path = cache_file(self.font_url)
        rs = TextClip(txt=self.text, font = self.font_path, fontsize=self.font_size, color=self.color,
                        bg_color=self.bg_color, size=(self.position['width'], self.position['height']),
                        stroke_color=self.stroke_color, stroke_width=self.stroke_width)
        return rs


class ImageComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.image_url = json_data['image_url']
        self.ext = json_data['ext']
    def get_clip(self):
        self.image_path = download_file(self.image_url, ext=self.ext)
        im = Image.open(self.image_path)
        width, height = im.size
        if width != self.position['width'] or height != self.position['height']:
            im1 = im.resize((self.position['width'], self.position['height']))
            rs = ImageClip(np.asarray(im1))
        else:
            rs = ImageClip(self.image_path)
        return rs


class VideoComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.video_url = json_data['video_url']
        self.ext = json_data['ext']
    def get_clip(self):
        self.video_path = download_file(self.video_url, ext=self.ext)
        rs = VideoFileClip(self.video_path)
        w, h = rs.size
        if self.position['width'] != w or self.position['height'] != h:
            rs = rs.resize((self.position['width'], self.position['height']))
        return rs


class LyricComp(Component):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.font_url = json_data['font_url']
        self.font_size = json_data['fontSize']
        self.bg_color = json_data['backgroundColor']
        self.color = json_data['color']
        self.stroke_color = json_data['stroke_color']
        self.stroke_width = json_data['stroke_width']
        self.audio_url = json_data['audio_url']
        self.audio_ext = json_data['audio_ext']
    def get_clip(self):
        self.audio_path = download_file(self.audio_url, ext=self.audio_ext)
        self.audio_moviepy = AudioFileClip(self.audio_path)
        self.lyric = Lyric(self.json_data['lyric_sync'], self.font_url, self.font_size, self.color,
                           self.audio_moviepy.duration,
                           self.position['width'], self.position['height'])
        self.duration = self.audio_moviepy.duration
        self.lyric.init()
        self.lyric.optimize_font()
        return self.lyric.make().set_audio(self.audio_moviepy)
