# playlist-defender
An abridged version of the Playlist Defender repository, consisting of only the files of the project I made major contributions to.

This is not a complete repository. Cloning this repo and attempting to run this code will not do anything. These are the four most relevant files I created while working as an intern on the Playlist Defender project with my Dad. The repository we worked on was private and it made the most sense to simply upload these files so they are easier to find, too.

## How the project worked:
Playlist Defender was created to keep track of a user's playlists over time, noting as songs are added and removed.

After authenticating their account with Spotify, the user can enter the 'Change History' screen. Every time they enter this screen, the app automatically downloads a new copy of the user's playlists, compares the new copy with the most recent copy already saved to the device, and displays the changes, along with any changes that were found from previous runnings of the app in a timeline.

## My Contributions:
### playlist_compare.py
The central feature of the app required us to have some way to compare two versions of a user's playlist library. There were existing functions in the project that downloaded library copies, saved them as JSON files, and extracted them to the form:

```python 
library_version = {'version': '1.0',
                             'date': 'YYYY-MM-DD',
                             'library': [{'name': 'Playlist Name 1',
                                          'tracks': [{'title': 'Song Title 1',
                                                      'artist': 'Song Artist Name 1',
                                                      'album': 'Song Album Name 1'},
                                                     {'title': 'Song Title 2',
                                                      'artist': 'Song Artist Name 2',
                                                      'album': 'Song Album Name 2'}]},
                                         {'name': 'Playlist Name 2',
                                          'tracks': [{'title': 'Song Title 1',
                                                      'artist': 'Song Artist Name 1',
                                                      'album': 'Song Album Name 1'},
                                                     {'title': 'Song Title 2',
                                                      'artist': 'Song Artist Name 2',
                                                      'album': 'Song Album Name 2'}]}]}
```

So I took these library formats and created two functions to perform the necessary comparing.

#### compare_playlist_versions(old_version, new_version)
This function took input of the form `library_version['library']['tracks']` and compared the two versions by finding song dictionaries that occurred in one version but not the other. It then returned this information in the form:

```
playlist_changes = {'added_songs': [list of added songs], 'removed_songs': [list of removed songs]}
```

#### compare_playlist_library_versions(old_version, new_version)
This function utilized the previous function to take input of the form `library_version['library']` and compare the two library versions. This time, there is an additional case. If the function finds a playlist that occurs in one version but not the other, it will be filed into either added or removed playlists. However, there are playlists that occured in both versions of the library, yet are different, because some of its songs have been added or removed.

Once the playlists have been sorted into these categories, the function returns this information in the form:

```
library_changes = {'added_playlists': [list of added playlists], 'removed_playlists': [list of removed playlists], 'modified_playlists': [list of modified playlists]}
```

Where each entry in the list of playlists is a dictionary containing the name of the added/removed/modified playlist, and the songs that were added or removed by proxy.

### window_spotify_change_history.py
This file actually generated the the change history screen of the application, and so utilized several other files from throughout the project in order to download the library, compare the various versions, and display them to the user.

The class `DisplaySpotifyChangeHistory()` utilized [BeeWare Toga](https://github.com/beeware/toga), an object-oriented, Python native, OS native GUI toolkit. The handful of methods in this class generate the change history output, set up the window object, and populate it with the output using Bootstrap in HTML and CSS.

The most interesting part of this file occurs in the file handling section, where the logic of downloading and saving the library versions is formulated. The file management system I devised works as such:

  * The original library version is saved in entirety, named `original_library_version.json`
  * The two latest library versions are also saved in their entirety, named `latest_library_version.json` and `previous_library_version.json`
  * Every other version is stored in a single file containing only the changes in between them, stamped with the date when each version was downloaded, named `library_change_history.json`

Therefore, every time a new version is downloaded, a series of changes must be made to each of these four files, depending on several edge cases, like:

  * Is it the first time the user has run the app?
  * Did the user already download a library version today?
  * Has the library even changed since the last version?

The algorithm relied on these four functions: `file_save_case_picker()`, `add_to_change_history()`, `generate_library_from_change_history()`, and `library_file_saver()`, plus a couple of minor helper functions. Through these functions, the app determined if any of the edge cases had occured, and updated each of the four files accordingly.

Once the files had been updated, the app called upon `playlist_compare.py` to compare the many versions going all the way back to the original, and then used a handful of other generating functions to insert this information into HTML code, and display it in an easy to read timeline format for the user.

### test_playlist_compare.py
This file contains automated unit tests for `playlist_compare.py`. They cover a variety of test cases, ensuring that the comparing functions act in reliable ways when library versions are identical, one or both of them are empty, song matches are only partial (if the song titles match but not the artist names, etc.), and more.

### test_change_history.py
This set of unit tests ensures that `file_save_case_picker()` correctly picks the edge cases for saving library versions mentioned above, `generate_library_from_change_history()` correctly builds the requested library version from the original version plus the changes, and `add_to_change_history()` correctly compares two versions and adds the changes to the change history.
