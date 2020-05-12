import deezer
import vlc
import random

deezer_client = deezer.Client()

def print_radios():
    radios = deezer_client.get_radios()
    sorted_radios = sorted(remove_duplicate(radios), key=lambda radio: radio.title)
    for radio in sorted_radios :
        print(radio.title + ' ' + str(radio.id))

def ask_radio():
    radio_id = int(input("\nQuel genre de musique souhaitez-vous ? (Saisissez l'id) "))
    radio = deezer_client.get_radio(radio_id)
    return radio

def remove_duplicate(radios):
    seen_titles = set()
    new_list = []
    for obj in radios:
        if obj.title not in seen_titles:
            new_list.append(obj)
            seen_titles.add(obj.title)
    return new_list

def get_random_radio():
    radios = deezer_client.get_radios()
    radio_number = random.randrange(0, len(radios) -1)
    return radios[radio_number]

def get_random_track(radio):
    tracks = radio.get_tracks()
    track_number = random.randrange(0, len(tracks) -1)
    return tracks[track_number]

def find_two_other_artists(radio, artist0):
    result = []

    while len(result) < 2 :
        other_track = get_random_track(radio)
        if (other_track.artist.id != artist0.id) & (other_track.artist not in result):
            result.append(other_track.artist)

    return result

def main():

	nb_point = 0
	nb_total = 0
	print_radios()

	while True:

		print('-----------------------------------------------------------------------------------------------------------------------')

		radio = ask_radio()

		nb_track = len(radio.get_tracks())
		nb_total = nb_total + 1

		if  nb_track < 4 :
			print("\nLa radio '" + radio.title + "' ne contient pas assez de morceaux.\n Choisissez une autre radio !")
		else:
			print("\nVous avez choisi '" + radio.title + "'.\nTrès bon choix!")

			print("Recherche parmi " + str(nb_track) + " morçeaux...")

			track = get_random_track(radio)

			artist0 =  track.artist

			artists = find_two_other_artists(radio, artist0)

			artists.append(artist0)

			random.shuffle(artists)

			player = vlc.MediaPlayer(track.preview)
			player.play()

			print('\nChoisir parmi les artistes:')

			print('\n1: '+ artists[0].name)
			print('2: '+ artists[1].name)
			print('3: '+ artists[2].name)

			choice_number = int(input("\nChoisir 1, 2 ou 3 : "))

			choice_artist = artists[choice_number - 1]

			if choice_artist == artist0 :
				print("\nTu as gagné !")
				nb_point = nb_point + 1

			else :
				print("\nPerdu, c'était " + artist0.name + " !")


			print("Vous avez " + str(nb_point) + " points sur " + str(nb_total))

			player.stop()

if __name__ == "__main__":
    main()



