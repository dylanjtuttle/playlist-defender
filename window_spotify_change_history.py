import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from playlist import config
from playlist.ui.app_screen import AppScreen
from playlist import local_data, playlist_compare
from playlist.spotify import playlists as pl
from datetime import datetime
import copy


FIRST_TIME_SAVING = 1
LATEST_SAVE_WAS_TODAY = 2
NO_CHANGE_SINCE_LAST_SAVE = 3
CHANGE_SINCE_LAST_SAVE = 4


class DisplaySpotifyChangeHistory(AppScreen):
    def __init__(self, app):
        super().__init__(app, title='Display Spotify Change History')
        self.webview = None
        self.main_box = None

    def initialize(self, state=None):
        self.main_box = toga.Box(style=Pack(direction=COLUMN))

        changes_msg = '<p style="color: #743FC4; font-family: Tahoma;">Updating change history... this may take a moment'

        if config.is_macos():
            style_obj = Pack(flex=1, width=500, background_color='transparent')
        else:
            style_obj = Pack(flex=1)
        self.webview = toga.WebView(
            url='https://beeware.org/',
            style=style_obj
        )
        self.main_box.add(self.webview)

        self.webview.set_content("https://example.com", changes_msg)

        self.content = toga.Box(children=[self.main_box])

    def run_report(self):
        new_library = pl.download_playlists()
        library_file_saver(datetime.date(datetime.now()), new_library)
        original_library = local_data.load_playlists('original_library_version')
        library_changes = local_data.load_playlists('library_change_history')
        latest_library = local_data.load_playlists('latest_library_version')
        previous_library = local_data.load_playlists('previous_library_version')
        pre_previous_library = generate_library_from_change_history(original_library, library_changes)

        changes_msg = generate_report(library_changes, latest_library, previous_library, pre_previous_library)

        self.webview.set_content("https://example.com", changes_msg)


def generate_report(change_history, latest_version, previous_version, pre_previous_version):
    """Combines all components into a single string containing the entire html code for the change history display.

    Arguments:
    change_history         - A dictionary containing the 'version_number' of the change history and the 'changes', a list of dictionaries each representing a single set of changes
                             that happened between two dates, formatted as in add_to_change_history() or playlist_compare.compare_playlist_library_versions()
    latest_version         - A list of dictionary playlists, the most recent version of the library already saved to the user's device
    previous_version       - A list of dictionary playlists, the second most recent version of the library already saved to the user's device
    pre_previous_version   - A list of dictionary playlists, the third most recent version of the library already saved to the user's device (not a file saved to the device,
                             but can be generated by generate_library_from_change_history())

    Returns:
    msg - A string containing the html code for the change history display
    """
    msg = _get_html_setup()
    change_history = change_history['changes']
    latest_change = playlist_compare.compare_playlist_library_versions(previous_version['library'], latest_version['library'])
    latest_change['date'] = latest_version['date']
    previous_change = playlist_compare.compare_playlist_library_versions(pre_previous_version['library'], previous_version['library'])
    previous_change['date'] = previous_version['date']
    if len(latest_change['added_playlists']) != 0 or len(latest_change['removed_playlists']) != 0 or len(latest_change['modified_playlists']) != 0:
        latest_change_bool = True
    else:
        latest_change_bool = False
    if len(previous_change['added_playlists']) != 0 or len(previous_change['removed_playlists']) != 0 or len(previous_change['modified_playlists']) != 0:
        previous_change_bool = True
    else:
        previous_change_bool = False
    if len(change_history) == 0 and (not latest_change_bool) and (not previous_change_bool):
        msg += f'<p class="num_playlists">Your library has not been changed yet! Come back some other day to see if anything has changed.</p></body>'
    else:
        counter = 1
        if latest_change_bool:
            msg += _make_collapsible_button(latest_change, counter)
            counter += 1
        if previous_change_bool:
            msg += _make_collapsible_button(previous_change, counter)
            counter += 1
        for change in reversed(change_history):
            msg += _make_collapsible_button(change, counter)
            counter += 1
        msg += '</body>'
        msg += '</html>'
    return msg


def _get_html_setup():
    """Generate html code for setting up the basic style of the collapsing change history display
    """
    msg = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Playlist Defender Library Change History</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"></script>
    <style>
    body {background-image: url(https://i.imgur.com/i0XZ5cD.png); background-repeat: repeat-x; font-family: Tahoma;}
    .bs-example{margin: 20px;}
    .accordion .fa{margin-right: 0.5rem; font-size: 24px; font-weight: bold; text-align: left; top: 2px;}
    .lib_change {color: #FFFFFF; text-align: left; margin-left: 20px; margin-top: 10px}
    .num_playlists {color: #743FC4;}
    .playlist_name {color: #378EA6; text-align: left;}
    .num_songs {color: #7A7A7A; margin-left: 20px; margin-top: -10px}
    .song_name {color: #3D3D3D; margin-left: 40px; margin-top: -10px}
    .artist_album {color: #A1A1A1; font-size: 14px}
    .justify {text-align: left; color: #743FC4}
    </style>
    <script>
    $(document).ready(function(){
        // Add down arrow icon for collapse element which is open by default
        $(".collapse.show").each(function(){
            $(this).prev(".card-header").find(".fa").addClass("fa-angle-down").removeClass("fa-angle-right");
        });

        // Toggle right and down arrow icon on show hide of collapse element
        $(".collapse").on('show.bs.collapse', function(){
            $(this).prev(".card-header").find(".fa").removeClass("fa-angle-right").addClass("fa-angle-down");
        }).on('hide.bs.collapse', function(){
            $(this).prev(".card-header").find(".fa").removeClass("fa-angle-down").addClass("fa-angle-right");
        });
    });
    </script>
    </head>
    <body>
    <h1 class="lib_change">Change <br> History</h1>"""
    return msg


def _make_collapsible_button(playlist_change, counter):
    """Generate html code for a collapsible accordion displaying song information for a playlist that has been either added or removed

    Arguments:
    playlist_change - a single set of playlist changes as formatted by add_to_change_history() or playlist_compare.compare_playlist_library_versions()
    counter         - An int that helps to specify a set of unique IDs for a given accordion, so each can open and collapse independently of each other

    Returns:
    msg - The html code that displays the accordion in string format
    """
    msg = f'<div class="bs-example"><div class="accordion" id="accordionExample{str(counter)}"><div class="card"><div class="card-header" ' \
          f'id="heading{str(counter)}"><h2 class="mb-0">'
    msg += f'<button type="button" class="btn btn-link justify" data-toggle="collapse" data-target="#collapse{str(counter)}"><i class="fa fa-angle-right"></i> '
    msg += f'{_get_overview(playlist_change)}'
    msg += f'</h2></div><div id="collapse{str(counter)}" class="collapse" aria-labelledby="heading{str(counter)}" data-parent="#accordionExample{str(counter)}">' \
           f'<div class="card-body">'
    msg += f'{_get_changes_body(playlist_change)}'
    msg += '</div></div></div></div></div>'
    return msg


def _get_overview(playlist_change):
    """Parses through a single set of library changes and returns a text preview of the changes,
    combining all songs added or removed from any modified playlist into one top level overview. For example:
    'May 23 (1 Playlists Added, 2 Playlists Removed, 3 Songs Added, 1 Song Removed)'

    Arguments:
    playlist_change - a single set of playlist changes as formatted by add_to_change_history() or playlist_compare.compare_playlist_library_versions()

    Returns:
    The string overview of the set of changes
    """
    msg = f'{_get_date_in_words(playlist_change["date"])} ('
    in_parentheses = []
    if len(playlist_change['added_playlists']) != 0:
        in_parentheses.append(f'{len(playlist_change["added_playlists"])} Playlists Added')
    if len(playlist_change['removed_playlists']) != 0:
        in_parentheses.append(f'{len(playlist_change["removed_playlists"])} Playlists Removed')
    if len(playlist_change['modified_playlists']) != 0:
        num_added_songs = 0
        num_removed_songs = 0
        for modified_playlist in playlist_change['modified_playlists']:
            num_added_songs += len(modified_playlist['added_songs'])
            num_removed_songs += len(modified_playlist['removed_songs'])
        if num_added_songs > 0:
            in_parentheses.append(f'{num_added_songs} Songs Added')
        if num_removed_songs > 0:
            in_parentheses.append(f'{num_removed_songs} Songs Removed')
    overview = ", ".join(in_parentheses)
    return msg + overview + ')'


def _get_changes_body(playlist_change):
    """Generates the html code for the body of the collapsible accordion containing the actual playlist changes.

    Arguments:
    playlist_change - a single set of playlist changes as formatted by add_to_change_history() or playlist_compare.compare_playlist_library_versions()

    Returns:
    msg - the html code for the single set of playlist changes, to be used as the body of a collapsible accordion"""
    msg = ''
    if len(playlist_change['added_playlists']) != 0:
        msg += f'<p class="num_playlists">{len(playlist_change["added_playlists"])} Playlists Added</p>'
        for added_playlist in playlist_change['added_playlists']:
            msg += f'<p class="playlist_name">{added_playlist["name"]}</p>'
            msg += f'<p class="num_songs">{len(added_playlist["added_songs"])} Songs Added</p>'
            msg += _make_song_list_html(added_playlist["added_songs"])

    if len(playlist_change["removed_playlists"]) != 0:
        msg += f'<p class="num_playlists">{len(playlist_change["removed_playlists"])} Playlists Removed</p>'
        for removed_playlist in playlist_change['removed_playlists']:
            msg += f'<p class="playlist_name">{removed_playlist["name"]}</p>'
            msg += f'<p class="num_songs">{len(removed_playlist["removed_songs"])} Songs Removed</p>'
            msg += _make_song_list_html(removed_playlist["removed_songs"])

    if len(playlist_change["modified_playlists"]) != 0:
        msg += f'<p class="num_playlists">{len(playlist_change["modified_playlists"])} Playlists Modified</p>'
        for modified_playlist in playlist_change['modified_playlists']:
            msg += f'<p class="playlist_name">{modified_playlist["name"]}</p>'
            if len(modified_playlist["added_songs"]) != 0:
                msg += f'<p class="num_songs">{len(modified_playlist["added_songs"])} Songs Added</p>'
                msg += _make_song_list_html(modified_playlist["added_songs"])
            if len(modified_playlist["removed_songs"]) != 0:
                msg += f'<p class="num_songs">{len(modified_playlist["removed_songs"])} Songs Removed</p>'
                msg += _make_song_list_html(modified_playlist["removed_songs"])
    return msg


def _make_song_list_html(song_list):
    """Generates html code for a general list of songs inside of a playlist.
    """
    return '<p class="song_name">' + '<br>'.join([f'{song["title"]} <span class="artist_album">{song["artist"]} - {song["album"]}</span>' for song in song_list]) + '</p>'


def _get_date_in_words(number_date):
    """Takes in a str date in the format 'yyyy-mm-dd' and returns the date in words, for example 'Aug 2' or 'Jan 10'"""
    month_list = ['Jan ', 'Feb ', 'Mar ', 'Apr ', 'May ', 'Jun ', 'Jul ', 'Aug ', 'Sep ', 'Oct ', 'Nov ', 'Dec ']
    month = int(number_date[5:7]) - 1
    day = str(int(number_date[-2:]))
    return month_list[month] + day


# FILE HANDLING SECTION


def library_file_saver(todays_date, new_library):
    """Saves the user's playlist library according to the case determined by _file_save_case_picker()"""
    latest_library_version = local_data.load_library_snapshot('latest_library_version')
    new_library = {'version': '1.0', 'source': 'spotify', 'date': str(todays_date), 'library': new_library}
    case = file_save_case_picker(latest_library_version, new_library, todays_date)
    if case == FIRST_TIME_SAVING:
        local_data.save_library_snapshot(new_library, 'original_library_version')
        local_data.save_library_snapshot(new_library, 'previous_library_version')
        local_data.save_library_snapshot(new_library, 'latest_library_version')
        local_data.save_library_changes({'version': '1.0', 'source': 'spotify', 'changes': []}, 'library_change_history')

    elif case == LATEST_SAVE_WAS_TODAY:
        local_data.save_library_snapshot(new_library, 'latest_library_version')

    # Do nothing if case == NO_CHANGE_SINCE_LAST_SAVE

    elif case == CHANGE_SINCE_LAST_SAVE:
        original_library_version = local_data.load_library_snapshot('original_library_version')
        previous_library_version = local_data.load_library_snapshot('previous_library_version')
        library_change_history = local_data.load_library_changes('library_change_history')

        # Add previous library to change history and remove it
        pre_previous_library_version = generate_library_from_change_history(original_library_version, library_change_history)  # latest-2
        new_change_history = add_to_change_history(pre_previous_library_version, previous_library_version, library_change_history)
        local_data.save_library_changes(new_change_history, 'library_change_history')

        # Rename latest library to previous library
        local_data.save_library_snapshot(latest_library_version, 'previous_library_version')

        # Save new latest library
        local_data.save_library_snapshot(new_library, 'latest_library_version')


def add_to_change_history(old_version, new_version, change_history):
    """Compares two files, adds any changes to the change history, and returns new change history.
    Note that the change history should only store changes up to and including the pre-previous version.
    For example, if this is the first, second or third time someone has saved a file, all changes can be accurately stored by the three files.
    It is only when there are four or more changes that we need to start storing the n-3 remaining changes in the history.

    Arguments:
    old_version    - the old version of the playlist library. The changes between this library and the one previous to it should be
                     the most recent entry of the change history already
    new_version    - the new version of the playlist library. The changes between old_version and new_version will be added to the change history
    change_history - A dictionary containing the 'version_number' of the change history and the 'changes'

    Returns:
    library_change_history - The updated version of the change history, which may be identical to the one inputted if there were no changes between old_version and new_version
    """
    library_change_history = copy.deepcopy(change_history)
    changes = playlist_compare.compare_playlist_library_versions(old_version['library'], new_version['library'])
    if len(changes['added_playlists']) != 0 or len(changes['removed_playlists']) != 0 or len(changes['modified_playlists']) != 0:
        library_change_history['changes'].append({'date': new_version['date'],
                                                  'added_playlists': changes['added_playlists'],
                                                  'removed_playlists': changes['removed_playlists'],
                                                  'modified_playlists': changes['modified_playlists']})
    return library_change_history


def generate_library_from_change_history(original_library_version, library_change_history):
    """Creates the pre-previous library version from the original library + the change history

    Arguments:
    original_library_version - A list of dictionary playlists. The first version of the user's playlist library ever saved to the device
    library_change_history   - A dictionary containing the 'version_number' of the change history and the 'changes'

    Returns:
    updated_library_version - The pre-previous version of the library"""
    updated_library_version = copy.deepcopy(original_library_version)
    if len(library_change_history['changes']) > 0:
        updated_library_version['date'] = library_change_history['changes'][-1]['date']  # date stamp of most recent change
    for change in library_change_history['changes']:
        for added_playlist in change['added_playlists']:
            updated_library_version['library'].append({'name': added_playlist['name'],
                                                       'tracks': added_playlist['added_songs']})

        for removed_playlist in change['removed_playlists']:
            del updated_library_version['library'][_get_playlist_index_by_name(updated_library_version['library'], removed_playlist['name'])]

        for modified_playlist in change['modified_playlists']:
            for playlist in updated_library_version['library']:
                if playlist['name'] == modified_playlist['name']:
                    for added_song in modified_playlist['added_songs']:
                        playlist['tracks'].append(added_song)

                    for removed_song in modified_playlist['removed_songs']:
                        del playlist['tracks'][_get_song_index_by_name(playlist['tracks'], removed_song['title'])]
    return updated_library_version


def file_save_case_picker(latest_library_version, new_library, todays_date):
    """Decides what to do with a library file the user has just downloaded.

    Arguments:
    latest_library_version - A dictionary containing a version number, date stamp, and the library, a list of dictionaries representing playlists.
                             The latest version of the user's playlist library already saved to the device
    new_library            - A dictionary containing a version number, date stamp, and the library, a list of dictionaries representing playlists.
                             A version of the user's playlist library that has just been downloaded

    Returns:
    'first_time_saving'         - if the user has never saved any files before, i.e. this is their first time saving a library
    'latest_save_was_today'     - if the user has already saved a library file today
    'no_change_since_last_save' - if the library has not changed since the most recent save
    'change_since_last_save'    - if the library has changed since the most recent save
    """
    # CASE 1: FIRST TIME SAVING
    if latest_library_version is None or latest_library_version.get('source') is None:
        return FIRST_TIME_SAVING
    else:
        # CASE 2: MOST RECENT SAVE WAS TODAY
        if latest_library_version['date'] == str(todays_date):
            return LATEST_SAVE_WAS_TODAY
        else:
            changes = playlist_compare.compare_playlist_library_versions(latest_library_version['library'], new_library['library'])
            # CASE 3: MOST RECENT SAVE WAS NOT TODAY, LIBRARY HAS NOT CHANGED SINCE
            if len(changes['added_playlists']) == 0 and len(changes['removed_playlists']) == 0 and len(changes['modified_playlists']) == 0:
                return NO_CHANGE_SINCE_LAST_SAVE
            # CASE 4: MOST RECENT SAVE WAS NOT TODAY, LIBRARY HAS CHANGED SINCE
            else:
                return CHANGE_SINCE_LAST_SAVE


def _get_playlist_index_by_name(library_list, playlist_name):
    """Takes in a LIST of playlists and the string name of a playlist one wants to find the index of and returns the index of that playlist, or None if it can't be found"""
    for playlist in library_list:
        if playlist['name'] == playlist_name:
            return library_list.index(playlist)
    return None


def _get_song_index_by_name(playlist_list, song_name):
    """Takes in a LIST of songs and the string name of a song one wants to find the index of and returns the index of that song, or None if it can't be found"""
    for song in playlist_list:
        if song['title'] == song_name:
            return playlist_list.index(song)
    return None
