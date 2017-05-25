import csv
import sys
import pprint

import spotipy
import spotipy.util as util

scope = 'user-library-modify'
client_id = ''
client_secret = ''
username = ''
redirect_uri = 'http://localhost/'

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)
    pp = pprint.PrettyPrinter(indent=2)

    with open('artistalbum.csv') as csvfile:
        rows = csv.reader(csvfile)
        for artist, album in rows:
            print('Processing {} - {}\n'.format(artist, album))

            albums_data = sp.search('{} - {}'.format(artist, album), type='album')\
                    .get('albums').get('items')
            filtered_data = [p for p in albums_data if p.get('album_type') != 'single']

            if len(filtered_data) == 0:
                print('WARNING: No albums found for {} - {}, continuing'.format(artist, album))
                continue

            selection = 0
            if len(filtered_data) > 2:
                print('More than one source found, select from the following (-1 to skip):\n')
                for count,external_url in enumerate([p.get('external_urls')
                                                     for p in filtered_data]):
                    print('[{}] {}'.format(count, external_url))
                selection = input('\nSelection: ')
                if selection == -1:
                    continue

            album_to_add = filtered_data[selection]
            sp.current_user_saved_albums_add([album_to_add.get('uri')])

            print('\n{}\n'.format('*' * 20))
else:
    print("Can't get token for {}".format(username))
