# encoding: utf-8


def video_summary(player_config):
    # TODO: this
    result = {
        'title': player_config['title'],
        'keywords': player_config['keywords'],
        'relative_loudness': player_config['relative_loudness'],
        'timestamp': player_config['timestamp'],
        'allow_ratings': player_config['allow_ratings'],
        'video_id': player_config['video_id'],
        'author': player_config['author'],
        'length_seconds': player_config['length_seconds'],
        'avg_rating': player_config['avg_rating'],
        'thumbnail_url': player_config['thumbnail_url'],
        'loudness': player_config['loudness'],
        'view_count': player_config['view_count'],
    }
    return result
