import os
import fnmatch

music_formats=['mp3','opus']
path=['./music']
music_files=[]
musicfiles=open('musicfiles','wb')
def locate(pattern, root):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
        	m=os.path.join(path, filename)
        	print m 	
        	musicfiles.write(m+'\n')
def generatefilepaths():
	for p in path:
		locate('*.mp3',p)
	musicfiles.close()


