#!/usr/bin/env python3
import json
import os.path as path
from os import mkdir

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from deemix.utils.localpaths import getConfigFolder


class SpotifyHelper:
    def __init__(self, configFolder=None):
        self.credentials = {}
        self.spotifyEnabled = False
        self.sp = None
        if not configFolder:
            self.configFolder = getConfigFolder()
        else:
            self.configFolder = configFolder
        self.emptyPlaylist = {
            'collaborative': False,
            'description': "",
            'external_urls': {'spotify': None},
            'followers': {'total': 0, 'href': None},
            'id': None,
            'images': [],
            'name': "Something went wrong",
            'owner': {
                'display_name': "Error",
                'id': None
            },
            'public': True,
            'tracks' : [],
            'type': 'playlist',
            'uri': None
        }
        self.initCredentials()

    def initCredentials(self):
        if not path.isdir(self.configFolder):
            mkdir(self.configFolder)
        if not path.isfile(path.join(self.configFolder, 'authCredentials.json')):
            with open(path.join(self.configFolder, 'authCredentials.json'), 'w') as f:
                json.dump({'clientId': "", 'clientSecret': ""}, f, indent=2)
        with open(path.join(self.configFolder, 'authCredentials.json'), 'r') as credentialsFile:
            self.credentials = json.load(credentialsFile)
        self.checkCredentials()

    def checkCredentials(self):
        if self.credentials['clientId'] == "" or self.credentials['clientSecret'] == "":
            spotifyEnabled = False
        else:
            try:
                self.createSpotifyConnection()
                self.sp.user_playlists('spotify')
                self.spotifyEnabled = True
            except Exception as e:
                self.spotifyEnabled = False
        return self.spotifyEnabled

    def getCredentials(self):
        return self.credentials

    def setCredentials(self, spotifyCredentials):
        spotifyCredentials['clientId'] = spotifyCredentials['clientId'].strip()
        spotifyCredentials['clientSecret'] = spotifyCredentials['clientSecret'].strip()
        with open(path.join(self.configFolder, 'authCredentials.json'), 'w') as f:
            json.dump(spotifyCredentials, f, indent=2)
        self.credentials = spotifyCredentials
        self.checkCredentials()

    def createSpotifyConnection(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=self.credentials['clientId'],
                                                              client_secret=self.credentials['clientSecret'])
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def _convert_playlist_structure(self, spotify_obj):
        if len(spotify_obj['images']):
            url = spotify_obj['images'][0]['url']
        else:
            url = False
        deezer_obj = {
            'checksum': spotify_obj['snapshot_id'],
            'collaborative': spotify_obj['collaborative'],
            'creation_date': "XXXX-00-00",
            'creator': {
                'id': spotify_obj['owner']['id'],
                'name': spotify_obj['owner']['display_name'],
                'tracklist': spotify_obj['owner']['href'],
                'type': "user"
            },
            'description': spotify_obj['description'],
            'duration': 0,
            'fans': spotify_obj['followers']['total'] if 'followers' in spotify_obj else 0,
            'id': spotify_obj['id'],
            'is_loved_track': False,
            'link': spotify_obj['external_urls']['spotify'],
            'nb_tracks': spotify_obj['tracks']['total'],
            'picture': url,
            'picture_small': url,
            'picture_medium': url,
            'picture_big': url,
            'picture_xl': url,
            'public': spotify_obj['public'],
            'share': spotify_obj['external_urls']['spotify'],
            'title': spotify_obj['name'],
            'tracklist': spotify_obj['tracks']['href'],
            'type': "playlist"
        }
        if not url:
            deezer_obj['picture_small'] = "https://e-cdns-images.dzcdn.net/images/cover/d41d8cd98f00b204e9800998ecf8427e/56x56-000000-80-0-0.jpg"
            deezer_obj['picture_medium'] = "https://e-cdns-images.dzcdn.net/images/cover/d41d8cd98f00b204e9800998ecf8427e/250x250-000000-80-0-0.jpg"
            deezer_obj['picture_big'] = "https://e-cdns-images.dzcdn.net/images/cover/d41d8cd98f00b204e9800998ecf8427e/500x500-000000-80-0-0.jpg"
            deezer_obj['picture_xl'] = "https://e-cdns-images.dzcdn.net/images/cover/d41d8cd98f00b204e9800998ecf8427e/1000x1000-000000-80-0-0.jpg"
        return deezer_obj

    def get_trackid_spotify(self, dz, track_id, fallbackSearch, spotifyTrack=None):
        if not self.spotifyEnabled:
            raise spotifyFeaturesNotEnabled
        singleTrack = False
        if not spotifyTrack:
            if path.isfile(path.join(self.configFolder, 'spotifyCache.json')):
                with open(path.join(self.configFolder, 'spotifyCache.json'), 'r') as spotifyCache:
                    cache = json.load(spotifyCache)
            else:
                cache = {'tracks': {}, 'albums': {}}
            if str(track_id) in cache['tracks']:
                return cache['tracks'][str(track_id)]
            singleTrack = True
            spotify_track = self.sp.track(track_id)
        else:
            spotify_track = spotifyTrack
        dz_track = 0
        if 'external_ids' in spotify_track and 'isrc' in spotify_track['external_ids']:
            try:
                dz_track = dz.get_track_by_ISRC(spotify_track['external_ids']['isrc'])
                dz_track = dz_track['id'] if 'id' in dz_track and 'title' in dz_track else 0
            except:
                dz_track = dz.get_track_from_metadata(spotify_track['artists'][0]['name'], spotify_track['name'],
                                                      spotify_track['album']['name']) if fallbackSearch else 0
        elif fallbackSearch:
            dz_track = dz.get_track_from_metadata(spotify_track['artists'][0]['name'], spotify_track['name'],
                                                  spotify_track['album']['name'])
        if singleTrack:
            cache['tracks'][str(track_id)] = dz_track
            with open(path.join(self.configFolder, 'spotifyCache.json'), 'w') as spotifyCache:
                json.dump(cache, spotifyCache)
        return dz_track

    def get_albumid_spotify(self, dz, album_id):
        if not self.spotifyEnabled:
            raise spotifyFeaturesNotEnabled
        if path.isfile(path.join(self.configFolder, 'spotifyCache.json')):
            with open(path.join(self.configFolder, 'spotifyCache.json'), 'r') as spotifyCache:
                cache = json.load(spotifyCache)
        else:
            cache = {'tracks': {}, 'albums': {}}
        if str(album_id) in cache['albums']:
            return cache['albums'][str(album_id)]
        spotify_album = self.sp.album(album_id)
        dz_album = 0
        if 'external_ids' in spotify_album and 'upc' in spotify_album['external_ids']:
            try:
                dz_album = dz.get_album_by_UPC(spotify_album['external_ids']['upc'])
                dz_album = dz_album['id'] if 'id' in dz_album else 0
            except:
                try:
                    dz_album = dz.get_album_by_UPC(int(spotify_album['external_ids']['upc']))
                    dz_album = dz_album['id'] if 'id' in dz_album else 0
                except:
                    dz_album = 0
        cache['albums'][str(album_id)] = dz_album
        with open(path.join(self.configFolder, 'spotifyCache.json'), 'w') as spotifyCache:
            json.dump(cache, spotifyCache)
        return dz_album

    def convert_spotify_playlist(self, dz, playlist_id, settings):
        if not self.spotifyEnabled:
            raise spotifyFeaturesNotEnabled
        spotify_playlist = self.sp.playlist(playlist_id)
        result = {
            'title': spotify_playlist['name'],
            'artist': spotify_playlist['owner']['display_name'],
            'size': spotify_playlist['tracks']['total'],
            'downloaded': 0,
            'failed': 0,
            'progress': 0,
            'errors': [],
            'type': 'spotify_playlist',
            'settings': settings or {},
            'id': playlist_id
        }
        if len(spotify_playlist['images']):
            result['cover'] = spotify_playlist['images'][0]['url']
        else:
            result[
                'cover'] = "https://e-cdns-images.dzcdn.net/images/cover/d41d8cd98f00b204e9800998ecf8427e/75x75-000000-80-0-0.jpg"
        playlistAPI = self._convert_playlist_structure(spotify_playlist)
        playlistAPI['various_artist'] = dz.get_artist(5080)
        tracklistTmp = spotify_playlist['tracks']['items']
        result['collection'] = []
        tracklist = []
        while spotify_playlist['tracks']['next']:
            spotify_playlist['tracks'] = self.sp.next(spotify_playlist['tracks'])
            tracklistTmp += spotify_playlist['tracks']['items']
        for item in tracklistTmp:
            if item['track']:
                tracklist.append(item['track'])
        totalSize = len(tracklist)
        result['size'] = totalSize
        if path.isfile(path.join(self.configFolder, 'spotifyCache.json')):
            with open(path.join(self.configFolder, 'spotifyCache.json'), 'r') as spotifyCache:
                cache = json.load(spotifyCache)
        else:
            cache = {'tracks': {}, 'albums': {}}
        for pos, track in enumerate(tracklist, start=1):
            if str(track['id']) in cache['tracks']:
                trackID = cache['tracks'][str(track['id'])]
            else:
                trackID = self.get_trackid_spotify(dz, 0, settings['fallbackSearch'], track)
                cache['tracks'][str(track['id'])] = trackID
            if trackID == 0:
                deezerTrack = {
                    'SNG_ID': 0,
                    'SNG_TITLE': track['name'],
                    'DURATION': 0,
                    'MD5_ORIGIN': 0,
                    'MEDIA_VERSION': 0,
                    'FILESIZE': 0,
                    'ALB_TITLE': track['album']['name'],
                    'ALB_PICTURE': "",
                    'ART_ID': 0,
                    'ART_NAME': track['artists'][0]['name']
                }
            else:
                deezerTrack = dz.get_track_gw(trackID)
            if 'EXPLICIT_LYRICS' in deezerTrack and deezerTrack['EXPLICIT_LYRICS'] == "1":
                playlistAPI['explicit'] = True
            deezerTrack['_EXTRA_PLAYLIST'] = playlistAPI
            deezerTrack['POSITION'] = pos
            deezerTrack['SIZE'] = totalSize
            deezerTrack['FILENAME_TEMPLATE'] = settings['playlistTracknameTemplate']
            result['collection'].append(deezerTrack)
        if not 'explicit' in playlistAPI:
            playlistAPI['explicit'] = False
        with open(path.join(self.configFolder, 'spotifyCache.json'), 'w') as spotifyCache:
            json.dump(cache, spotifyCache)
        return result

    def get_user_playlists(self, user):
        if not self.spotifyEnabled:
            raise spotifyFeaturesNotEnabled
        result = []
        playlists = self.sp.user_playlists(user)
        while playlists:
            for playlist in playlists['items']:
                result.append(self._convert_playlist_structure(playlist))
            if playlists['next']:
                playlists = self.sp.next(playlists)
            else:
                playlists = None
        return result

    def get_playlist_tracklist(self, id):
        if not self.spotifyEnabled:
            raise spotifyFeaturesNotEnabled
        playlist = self.sp.playlist(id)
        tracklist = playlist['tracks']['items']
        while playlist['tracks']['next']:
            playlist['tracks'] = self.sp.next(playlist['tracks'])
            tracklist += playlist['tracks']['items']
        playlist['tracks'] = tracklist
        return playlist


class spotifyFeaturesNotEnabled(Exception):
    pass
