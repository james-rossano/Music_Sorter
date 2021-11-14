#James Rossano
#musicApiProj.py

import vlc		#plays audio
import pathlib		#finds all audio files in a folder
import random		#used for randomly shuffling songs
from tinytag import TinyTag		#takes the ID3 metadata from an mp3 file

genreConversion = [['Blues' , 0],['Classic Rock' , 1],['Country' , 2],['Dance' , 3],['Disco' , 4],['Funk' , 5],['Grunge' , 6],['Hip-Hop' , 7],['Jazz' , 8],['Metal' , 9],['New Age' , 10],['Oldies' , 11],['Other' , 12],['Pop' , 13],
	['R&B' , 14],['Rap' , 15],['Reggae' , 16],['Rock' , 17],['Techno' , 18],['Industrial' , 19],['Alternative' , 20],['Ska' , 21],['Death Metal' , 22],['Pranks' , 23],['Soundtrack' , 24],['Euro-Techno' , 25],['Ambient' , 26],
	['Trip-Hop' , 27],['Vocal' , 28],['Jazz+Funk' , 29],['Fusion' , 30],['Trance' , 31],['Classical' , 32],['Instrumental' , 33],['Acid' , 34],['House' , 35],['Game' , 36],['Sound Clip' , 37],['Gospel' , 38],['Noise' , 39],
	['Alternative Rock' , 40],['Bass' , 41],['Soul' , 42],['Punk' , 43],['Space' , 44],['Meditative' , 45],['Instrumental Pop' , 46],['Instrumental Rock' , 47],['Ethnic' , 48],['Gothic' , 49],['Darkwave' , 50],['Techno-Industrial' , 51],
	['Electronic' , 52],['Pop-Folk' , 53],['Eurodance' , 54],['Dream' , 55],['Southern Rock' , 56],['Comedy' , 57],['Cult' , 58],['Gangsta' , 59],['Top 40' , 60],['Christian Rap' , 61],['Pop/Funk' , 62],['Jungle' , 63],['Native US' , 64],
	['Cabaret' , 65],['New Wave' , 66],['Psychadelic' , 67],['Rave' , 68],['Showtunes' , 69],['Trailer' , 70],['Lo-Fi' , 71],['Tribal' , 72],['Acid Punk' , 73],['Acid Jazz' , 74],['Polka' , 75],['Retro' , 76],['Musical' , 77],
	['Rock & Roll' , 78],['Hard Rock' , 79],['Folk' , 80],['Folk-Rock' , 81],['National Folk' , 82],['Swing' , 83],['Fast Fusion' , 84],['Bebob' , 85],['Latin' , 86],['Revival' , 87],['Celtic' , 88],['Bluegrass' , 89],['Avantgarde' , 90],
	['Gothic Rock' , 91],['Progressive Rock' , 92],['Psychedelic Rock' , 93],['Symphonic Rock' , 94],['Slow Rock' , 95],['Big Band', 96],['Chorus' , 97],['Easy Listening' , 98],['Acoustic' , 99],['Humour' , 100],['Speech' , 101],
	['Chanson' , 102],['Opera' , 103],['Chamber Music' , 104],['Sonata' , 105],['Symphony' , 106],['Booty Bass' , 107],['Primus' , 108],['Porn Groove' , 109],['Satire' , 110],['Slow Jam' , 111],['Club' , 112],['Tango' , 113],
	['Samba' , 114],['Folklore' , 115],['Ballad' , 116],['Power Ballad' , 117],['Rhythmic Soul' , 118],['Freestyle' , 119],['Duet' , 120],['Punk Rock' , 121],['Drum Solo' , 122],['Acapella' , 123],['Euro-House' , 124],['Dance Hall' , 125],
	['Goa' , 126],['Drum & Bass' , 127],['Club - House' , 128],['Hardcore' , 129],['Terror' , 130],['Indie' , 131],['BritPop' , 132],['Negerpunk' , 133],['Polsk Punk' , 134],['Beat' , 135],['Christian Gangsta Rap' , 136],
	['Heavy Metal' , 137],['Black Metal' , 138],['Crossover' , 139],['Contemporary Christian' , 140],['Christian Rock' , 141],['Merengue' , 142],['Salsa' , 143],['Thrash Metal' , 144],['Anime' , 145],['JPop' , 146],['Synthpop' , 147],
	['Unknown' , 148]]		#ID3 integer to genre conversion table


playlistPath = 'Songs/'
genre = ''
songLibrary = []
songPaths = list(pathlib.Path(playlistPath).glob('*.mp3'))
for item in songPaths:		#organizing all songs into a ordered list
	tag = TinyTag.get(item)
	if tag.genre[0] == '(':
		for type in genreConversion:
			if type[1] == int(tag.genre[1:-1]):
				genre = type[0]
				break
	else:
		genre = tag.genre

	songLibrary.append([str(item)[6:], tag.title, tag.albumartist, genre])


for item in songLibrary:	#Checks if there is unspecified data in the files
	for i in range(len(item)):
		if item[i] == None:
			item[i] = 'Unknown'

class playSongs:		#song player class
	songPlaying = False
	songCycle = None
	shuffleSet = []
	chosenArtist = 'NONE'
	chosenGenre = 'NONE'

	def songInfo(self, title, type):	#Gives metadata on a specified song
		if type == 'TITLE':
			titleType = 1
		elif type == 'PATH':
			titleType = 0

		for item in songLibrary:
			if item[titleType].upper() == title or item[titleType] == title:
				print('Title: ' + item[1] + ' / Artist: ' + item[2] + ' / Genre: ' + item[3])
				return
		print('There are no songs in this library by the name: ' + '"' + title + '"')

	def shuffleSongs(self):		#Shuffles all songs in a library randomly
		if self.songPlaying == False:
			self.songCycle = 'SHUFFLE'
			self.songPlaying = True
			if len(self.shuffleSet) == 0:
				for item in songLibrary:
					self.shuffleSet.append(item[0])
			randNum = random.randint(0, len(self.shuffleSet)-1)
			result = self.shuffleSet[randNum]
			self.songInfo(result, 'PATH')
			self.shuffleSet.pop(randNum)
			return playlistPath + result
		else:
			print('A song is already playing')
			return False

	def playArtist(self, artist):		#Plays a specified artist
		if self.songPlaying == False:
			if self.songCycle != 'ARTIST':
				self.songCycle = 'ARTIST'
				self.shuffleSet = []

			if self.shuffleSet == []:
				for item in songLibrary:
					if item[2].upper() == artist:
						self.shuffleSet.append(item[0])
				if self.shuffleSet == []:
					print('There are no songs by that artist in this library')
					return False
			self.chosenArtist = artist
			self.songPlaying = True
			randNum = random.randint(0, len(self.shuffleSet) - 1)
			result = self.shuffleSet[randNum]
			self.songInfo(result, 'PATH')
			self.shuffleSet.pop(randNum)
			return playlistPath + result
		else:
			print('A song is already playing')
			return False

	def playGenre(self, genre):		#Plays a specified artist
		if self.songPlaying == False:
			if self.songCycle != 'GENRE':
				self.songCycle = 'GENRE'
				self.shuffleSet = []

			if self.shuffleSet == []:
				for item in songLibrary:
					if item[3].upper() == genre:
						self.shuffleSet.append(item[0])
				if self.shuffleSet == []:
					print('There are no songs by that genre in this library')
					return False
			self.chosenGenre = genre
			self.songPlaying = True
			randNum = random.randint(0, len(self.shuffleSet) - 1)
			result = self.shuffleSet[randNum]
			self.songInfo(result, 'PATH')
			self.shuffleSet.pop(randNum)
			return playlistPath + result
		else:
			print('A song is already playing')
			return False

	def playSong(self, title):		#Plays a specified song via the song title
		if self.songPlaying == False:
			for item in songLibrary:
				if item[1].upper() == title:
					self.songPlaying = True
					self.songInfo(item[0], 'PATH')
					return playlistPath + item[0]
			print('There are no songs in this library by that name')
			return False
		else:
			print('A song is already playing')
			return False

	def stopPlaying(self,type):		#stops the current song from playing
		if type == 'FULL':
			self.songCycle = ''
		if self.songPlaying == True:
			self.songPlaying = False
			return True
		else:
			print('No song is playing')
			return False

	def nextSong(self):		#Skips to the next song in a song cycle
		if self.songCycle == 'GENRE':
			result = self.playGenre(self.chosenGenre)
			return result
		elif self.songCycle == 'ARTIST' and self.chosenArtist != '':
			result = self.playArtist(self.chosenArtist)
			return result
		elif self.songCycle == 'SHUFFLE':
			result = self.shuffleSongs()
			return result
		else:
			print('you are not in a song cycle')
			return False

	def listAllSongs(self):		#lists all songs in a song library
		for item in songLibrary:
			print(item[1])

sL = playSongs()

direction = ''
print('Use the PS, SS, PA, SI, PG, LS, QUIT, STOP, or NEXT commands')
while direction != False:	#Main control loop
	direction = input('Command: ')
	direction = direction.upper()
	if direction.replace(' ','') == 'QUIT':		#conditionals for user input
		direction = False

	elif direction.replace(' ','') == 'STOP':
		result = sL.stopPlaying('FULL')
		if result == True:
			audioFile.stop()

	elif direction.replace(' ','') == 'NEXT':
		result = sL.stopPlaying('QUICK')
		if result == True:
			audioFile.stop()
		else:
			print('You are not in a song cycle')
			continue
		result = sL.nextSong()
		if result != False:
			audioFile = vlc.MediaPlayer(result)
			audioFile.play()

	elif direction[0:3] == 'PS ':
		result = sL.playSong(direction[3:])
		if result != False:
			audioFile = vlc.MediaPlayer(result)
			audioFile.play()

	elif direction.replace(' ','') == 'SS':
		result = sL.shuffleSongs()
		if result != False:
			audioFile = vlc.MediaPlayer(result)
			audioFile.play()

	elif direction[0:3] == 'PA ':
		result = sL.playArtist(direction[3:])
		if result != False:
			audioFile = vlc.MediaPlayer(result)
			audioFile.play()

	elif direction[0:3] == 'PG ':
		result = sL.playGenre(direction[3:])
		if result != False:
			audioFile = vlc.MediaPlayer(result)
			audioFile.play()

	elif direction[0:3] == 'SI ':
		sL.songInfo(direction[3:],'TITLE')

	elif direction.replace(' ','') == 'LS':
		sL.listAllSongs()
	else:	#If none of the commands were specified
		print('That was an unknown command, please check for typos or read the readme for correct usage.')