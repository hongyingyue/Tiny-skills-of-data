from moviepy.editor import *
import os
import cv2


class Clips_maker(object):
    def __init__(self):
        pass

    def walk_forwards(self):
        clip1 = VideoFileClip('./video/00.MOV',audio=False).fx(vfx.resize,(1440,1080)).crop(630,0,1440,1080).fx( vfx.speedx, 0.5)
        clip1.write_videofile("./clips/1.mp4")

        clip2 = VideoFileClip('./video/05.MOV', audio=False).fx(vfx.resize,(1440,1080)).crop(315, 0, 1125, 1080).fx(vfx.speedx, 0.5)
        clip2=clip2.subclip(0, 6)
        clip2.write_videofile("./clips/2.mp4")

    def turn_around(self):
        clip3= VideoFileClip('./video/10.MOV', audio=False).fx(vfx.resize,(831,1109)).crop(11,0,821,1080).fx(vfx.speedx, 0.87)# (1512,2016)
        clip3=clip3.subclip(0,3)
        clip3.write_videofile("./clips/3.mp4")

        clip4 = VideoFileClip('./video/21.MOV', audio=False).fx(vfx.resize,(831,1109)).crop(11,0,821,1080).fx(vfx.speedx, 0.87)
        clip4=clip4.subclip(2,4)
        clip4 = clip4.fx(vfx.mirror_x)
        clip4.write_videofile("./clips/4.mp4")

        #把两个视频放在一个画面上同时播放
        clip3.set_position([0, 0])
        clip4.set_position([clip3.w, 0])
        clip34=CompositeVideoClip([clip3, clip4], size=(clip3.w, clip3.h))
        clip34.write_videofile("./clips/3.mp4")

    def dog(self):
        clip5= VideoFileClip("./pic/1.gif").fx(vfx.resize,(831,1109)).crop(11,0,821,1080).fx(vfx.speedx, 0.6)
        clip5 = clip5.subclip(0, 3)
        clip5.write_videofile("./clips/5.mp4")

    def walk_together(self):
        clip6 = VideoFileClip('./video/21.MOV', audio=False).fx(vfx.resize, (831, 1109)).crop(11, 0, 821, 1080).fx(vfx.speedx, 0.3)
        clip6.write_videofile("./clips/6.mp4")

    def kiss(self):
        clip7 = VideoFileClip('./video/51.MOV', audio=False).fx(vfx.resize, (831, 1109)).crop(11, 0, 821, 1080).fx(vfx.speedx, 0.5)
        clip7 = clip7.subclip(1,4)
        clip7.write_videofile("./clips/7.mp4")


class video_maker(object):
    def __init__(self):
        self.list=[]
        for root, dirs, files in os.walk("./clips"):
            files.sort()
            for file in files:
                if os.path.splitext(file)[1] == '.mp4':
                    filePath = os.path.join(root, file)
                    video = VideoFileClip(filePath)
                    self.list.append(video)

    def video_concat(self):
        self.video = concatenate_videoclips(self.list)


    def subtitle_adder(self):
        pass

    def music_adder(self):
        audioclip1 = AudioFileClip('./music/hongying.mp3').subclip(31, 38).volumex(0.9) #7
        audioclip2=AudioFileClip('./music/一生所爱.mp3').subclip(46,60).volumex(1.8) #10
        #audioclip3 = AudioFileClip('./music/hongying.mp3').subclip(51, 54) #3
        audioclip=concatenate_audioclips([audioclip1, audioclip2])
        self.video= self.video.set_audio(audioclip)
        self.video.to_videofile("./target.mp4", remove_temp=False)


if __name__=='__main__':
    clip=Clips_maker()
    #clip.walk_forwards()
    #clip.turn_around()
    #clip.dog()
    #clip.kiss()


    video=video_maker()
    video.video_concat()
    video.music_adder()
