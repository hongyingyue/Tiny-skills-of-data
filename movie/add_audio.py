from moviepy.editor import *
import cv2

def add_audio(file1,file2):
    videoclip = VideoFileClip(file1)
    audioclip_video=VideoFileClip(file2)
    audioclip=audioclip_video.audio
    #audioclip=AudioFileClip('attraction.mp3').subclip(0,43)
    videoclip = videoclip.set_audio(audioclip)
    videoclip.write_videofile('output_with_audio.mp4')


def concat_video(*files):
    all_file=[]
    for file in files:
        all_file.append(VideoFileClip(file))
    finalclip = concatenate_videoclips(all_file) #, transition=VideoFileClip("logo.avi"))
    finalclip.write_videofile("concat1.mp4")

def concat_video2(file1,file2):
    clip1 = VideoFileClip('3.MP4').rotate(-90).subclip(0, 3)
    clip2 = VideoFileClip(file1).subclip(3,8)
    clip3=VideoFileClip(file2).subclip(8,11)
    clip4=VideoFileClip('3.MP4').subclip(5,7)
    clip5=VideoFileClip(file1).subclip(11,15)
    final=concatenate_videoclips([clip1,clip2,clip3,clip4,clip5])
    final=final.fl_image(crop_image)
    final.write_videofile('concat2.mp4')


def make_frame(filename):
    video=VideoFileClip(filename=filename).rotate(-90)#.subclip(3,9)
    #text_clip=TextClip("Quality Field Sensor Training 2018",fontsize=70,color='green')
    #text_clip=text_clip.set_pos(('left','top')).set_duration(5)
    #video_out=CompositeVideoClip([video,text_clip])
    video.write_videofile('exa4.MP4')

def add_text(image):
    img=image.copy()
    text='QFS 2018: demo use only'
    font=cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,text,(100,1700),font,1.5,(221,28,119),4)
    return img

def crop_image(image):
    img=image.copy()
    img_new=img[130:-130,:,:]
    return img_new


#add_audio('video10.avi','10.MP4')
#concat_video('exa1.MP4','exa2.MP4','exa3.MP4','exa4.MP4')
#make_frame('video16.avi')

#audioclip=AudioFileClip('attraction.mp3').subclip(0,43)
#videoclip = VideoFileClip('my_concatenate.mp4').set_audio(audioclip)
#videoclip.write_videofile('Final.mp4')


#video=VideoFileClip('Final2.mp4')
#out_clip=video.fl_image(add_text)
#out_clip.write_videofile('Final3.mp4')

concat_video2('out1.mp4','out2.mp4')

