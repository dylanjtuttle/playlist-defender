def compare_playlist_versions(old_version, new_version):
    """Compare two playlists and return a dictionary containing added and removed songs.

    Arguments:
    old_version -- a list representing the old version of a playlist, containing dictionaries where each dictionary represents a song
    new_version -- a list representing the new version of a playlist to be compared to the old playlist

    Returns:
    playlist_changes -- a dictionary containing two keys:
        'added_songs', pointing to a list of dictionaries representing songs found on new_version but not old_version
        'removed_songs', pointing to a list of dictionaries representing songs on old_version but not new_version

    Possible Errors:
    TypeError -- Neither old_version or new_version can be of type None. If this is the case, a TypeError will be raised.
    """
    added_songs = []
    removed_songs = []

    for old_track in old_version:
        if old_track not in new_version:
            removed_songs.append(old_track)
    for new_track in new_version:
        if new_track not in old_version:
            added_songs.append(new_track)

    playlist_changes = {'added_songs': added_songs, 'removed_songs': removed_songs}
    return playlist_changes


def compare_playlist_library_versions(old_version, new_version):
    """Compare two playlist library files and return a dictionary containing added, removed, and modified playlists.

    NOTE: This function assumes that the 'name' key of a playlist is a unique identifier. That is, two different playlists can not possess the same name.

    Arguments:
    old_version -- some older version of a library, a list containing dictionaries, each representing a playlist
    new_version -- a new version of the same library, to be compared to the old version

    Returns:
    library_changes -- a dictionary containing three keys:
        'added_playlists', pointing to a list of dictionaries, containing the name of the added playlist and the songs that have been added by proxy
        'removed_playlists', pointing to a list of dictionaries, containing the name of the removed playlist and the songs that have been removed by proxy
        'modified_playlists', pointing to a list of dictionaries, containing the name of the modified playlist and the songs that have been added and/or removed

    Possible Errors:
    TypeError -- In the case of empty playlists, libraries, or song metadata, empty lists/dictionaries MUST be used.
                 If any of these are passed as type None, a TypeError will be raised.
    """
    added_playlists = []
    removed_playlists = []
    modified_playlists = []

    for old_playlist in old_version:
        matching_new_playlists = [new_playlist for new_playlist in new_version if new_playlist['name'] == old_playlist['name']]

        if len(matching_new_playlists) == 0:  # if there were no name matches, add the playlist to removed_playlists
            removed_playlists.append({'name': old_playlist['name'],
                                      'removed_songs': old_playlist['tracks']})
        else:
            new_playlist = matching_new_playlists[0]
            changes = compare_playlist_versions(old_playlist['tracks'], new_playlist['tracks'])
            if len(changes['added_songs']) != 0 or len(changes['removed_songs']) != 0:  # if changes have been made to the playlist in question, add it to modified playlists
                modified_playlists.append({'name': old_playlist['name'],
                                           'added_songs': changes['added_songs'],
                                           'removed_songs': changes['removed_songs']})

    for new_playlist in new_version:
        if not any(old_playlist['name'] == new_playlist['name'] for old_playlist in old_version):
            # We already accounted for all playlists that have been modified (since they would always be found in both old and new),
            # so now we want to only append playlists that are actually brand new.
            added_playlists.append({'name': new_playlist['name'],
                                    'added_songs': new_playlist['tracks']})
    library_changes = {'added_playlists': added_playlists, 'removed_playlists': removed_playlists, 'modified_playlists': modified_playlists}
    return library_changes
