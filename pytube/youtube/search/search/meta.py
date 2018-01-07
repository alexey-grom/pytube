# encoding: utf-8


BY_RELEVANCE = 'by-relevance'
BY_UPLOAD_DATE = 'by-upload-date'
BY_VIEWS_COUNT = 'by-views-count'
BY_RATING = 'by-rating'

ALL = 'all'
VIDEOS = 'videos'
CHANNELS = 'channels'
PLAYLISTS = 'playlists'
MOVIES = 'movies'
SHOWS = 'shows'

TYPES = [
    ALL,
    VIDEOS,
    CHANNELS,
    PLAYLISTS,
    MOVIES,
    SHOWS,
]

ORDERS = [
    BY_RELEVANCE,
    BY_UPLOAD_DATE,
    BY_VIEWS_COUNT,
    BY_RATING,
]

OPTION_VALUES = {
    BY_RELEVANCE: {
        ALL: 'CAA%253D',
        VIDEOS: 'CAASAhAB',
        CHANNELS: 'CAASAhAC',
        PLAYLISTS: 'CAASAhAD',
        MOVIES: 'CAASAhAE',
        SHOWS: 'CAASAhAF',
    },
    BY_UPLOAD_DATE: {
        ALL: 'CAI%253D',
        VIDEOS: 'CAISAhAB',
        CHANNELS: 'CAISAhAC',
        PLAYLISTS: 'CAISAhAD',
        MOVIES: 'CAISAhAE',
        SHOWS: 'CAISAhAF',
    },
    BY_VIEWS_COUNT: {
        ALL: 'CAM%253D',
        VIDEOS: 'CAMSAhAB',
        CHANNELS: 'CAMSAhAC',
        PLAYLISTS: 'CAMSAhAD',
        MOVIES: 'CAMSAhAE',
        SHOWS: 'CAMSAhAF',
    },
    BY_RATING: {
        ALL: 'CAE%253D',
        VIDEOS: 'CAESAhAB',
        CHANNELS: 'CAESAhAC',
        PLAYLISTS: 'CAESAhAD',
        MOVIES: 'CAESAhAE',
        SHOWS: 'CAESAhAF',
    },
}
