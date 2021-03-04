from pydub import AudioSegment

files_path = 'audio_data/'
file_name = '1DDD'

# startMin = 0
# startSec = 0
#
# endMin = 1
# endSec = 0
#
# # Time to miliseconds
# startTime = startMin*60*1000+startSec*1000
# endTime = endMin*60*1000+endSec*1000


# startMin = 0
# startSec = 0
#
# endMin = 1
# endSec = 0

# Time to miliseconds
startTime = 12.32*1000
endTime = 96.14*1000

# startTime_2 = 32.84*1000
# endTime_2 = 48.44*1000

# Opening file and extracting segment
song = AudioSegment.from_mp3( files_path+file_name+'.mp3' )
extract = song[startTime:endTime]
# extract_2=song[startTime_2:endTime_2]

# Saving
extract.export(file_name+'-extract.wav', format="wav")
# extract_2.export(file_name+'-extract2.wav', format="wav")

# import wave
# import contextlib
# fname = '1CCC.wav'
# with contextlib.closing(wave.open(fname,'r')) as f:
#     frames = f.getnframes()
#     rate = f.getframerate()
#     duration = frames / float(rate)
#     print(frames)
#     print(rate)