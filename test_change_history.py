import unittest
from playlist.ui import window_gpm_change_history as wg
from datetime import datetime

latest = [None,
          {'version': '1.0', 'date': str(datetime.date(datetime.now())), 'library': [{'name': 'a', 'tracks': [{'title': 'a', 'artist': 'a', 'album': 'a'},
                                                                                                              {'title': 'b', 'artist': 'b', 'album': 'b'}]}]},
          {'version': '1.0', 'date': '2020-09-03', 'library': [{'name': 'a', 'tracks': [{'title': 'a', 'artist': 'a', 'album': 'a'},
                                                                                        {'title': 'b', 'artist': 'b', 'album': 'b'},
                                                                                        {'title': 'c', 'artist': 'c', 'album': 'c'}]}]},
          {'version': '1.0', 'date': '2020-09-03', 'library': [{'name': 'a', 'tracks': [{'title': 'a', 'artist': 'a', 'album': 'a'},
                                                                                        {'title': 'b', 'artist': 'b', 'album': 'b'}]}]},
          {'version': '1.0', 'date': str(datetime.date(datetime.now())), 'library': [{'name': 'a', 'tracks': [{'title': 'a', 'artist': 'a', 'album': 'a'},
                                                                                                              {'title': 'b', 'artist': 'b', 'album': 'b'},
                                                                                                              {'title': 'i', 'artist': 'i', 'album': 'i'}]}]},
          {'version': '1.0', 'date': str(datetime.date(datetime.now())), 'library': [{'name': 'a', 'tracks': [{'title': 'a', 'artist': 'a', 'album': 'a'},
                                                                                                              {'title': 'b', 'artist': 'b', 'album': 'b'},
                                                                                                              {'title': 'c', 'artist': 'c', 'album': 'c'}]},
                                                                                     {'name': 'b', 'tracks': [{'title': 'd', 'artist': 'd', 'album': 'd'},
                                                                                                              {'title': 'e', 'artist': 'e', 'album': 'e'},
                                                                                                              {'title': 'f', 'artist': 'f', 'album': 'f'}]}]},
          {'version': '1.0', 'date': '2020-09-03', 'library': []}
          ]
new = [{'version': '1.0', 'date': str(datetime.date(datetime.now())), 'library': [{'name': 'a', 'tracks': [{'title': 'a', 'artist': 'a', 'album': 'a'},
                                                                                                           {'title': 'b', 'artist': 'b', 'album': 'b'},
                                                                                                           {'title': 'c', 'artist': 'c', 'album': 'c'}]}]}]
previous = []
original = [{'version': '1.0', 'date': '2020-09-03', 'library': [{'name': 'a', 'tracks': [{'title': 'a', 'artist': 'a', 'album': 'a'},
                                                                                          {'title': 'b', 'artist': 'b', 'album': 'b'},
                                                                                          {'title': 'c', 'artist': 'c', 'album': 'c'}]},
                                                                 {'name': 'b', 'tracks': [{'title': 'd', 'artist': 'd', 'album': 'd'},
                                                                                          {'title': 'e', 'artist': 'e', 'album': 'e'},
                                                                                          {'title': 'f', 'artist': 'f', 'album': 'f'}]}]}
            ]
change = [{'version': '1.0', 'changes': [{'date': str(datetime.date(datetime.now())),
                                          'added_playlists': [{'name': 'c', 'added_songs': [{'title': 'g', 'artist': 'g', 'album': 'g'},
                                                                                            {'title': 'h', 'artist': 'h', 'album': 'h'},
                                                                                            {'title': 'i', 'artist': 'i', 'album': 'i'}]}],
                                          'removed_playlists': [{'name': 'a', 'removed_songs': [{'title': 'a', 'artist': 'a', 'album': 'a'},
                                                                                                {'title': 'b', 'artist': 'b', 'album': 'b'},
                                                                                                {'title': 'c', 'artist': 'c', 'album': 'c'}]}],
                                          'modified_playlists': [{'name': 'b',
                                                                  'added_songs': [{'title': 'j', 'artist': 'j', 'album': 'j'}],
                                                                  'removed_songs': [{'title': 'd', 'artist': 'd', 'album': 'd'}]}]}]},
          {'version': '1.0', 'changes': []},
          {'version': '1.0', 'changes': [{'date': '2020-09-04',
                                          'added_playlists': [{'name': 'c', 'added_songs': [{'title': 'g', 'artist': 'g', 'album': 'g'},
                                                                                            {'title': 'h', 'artist': 'h', 'album': 'h'},
                                                                                            {'title': 'i', 'artist': 'i', 'album': 'i'}]}],
                                          'removed_playlists': [{'name': 'a', 'removed_songs': [{'title': 'a', 'artist': 'a', 'album': 'a'},
                                                                                                {'title': 'b', 'artist': 'b', 'album': 'b'},
                                                                                                {'title': 'c', 'artist': 'c', 'album': 'c'}]}],
                                          'modified_playlists': [{'name': 'b',
                                                                  'added_songs': [{'title': 'j', 'artist': 'j', 'album': 'j'}],
                                                                  'removed_songs': [{'title': 'd', 'artist': 'd', 'album': 'd'}]}]}]}
          ]


class TestLibraryCompare(unittest.TestCase):
    def test_no_files(self):
        case = wg.file_save_case_picker(latest[0], new[0], datetime.date(datetime.now()))
        self.assertEqual(case, wg.FIRST_TIME_SAVING, "Should return first time saving")

    def test_same_date(self):
        case = wg.file_save_case_picker(latest[1], new[0], datetime.date(datetime.now()))
        self.assertEqual(case, wg.LATEST_SAVE_WAS_TODAY, "Should return latest save was today")

    def test_no_changes(self):
        case = wg.file_save_case_picker(latest[2], new[0], datetime.date(datetime.now()))
        self.assertEqual(case, wg.NO_CHANGE_SINCE_LAST_SAVE, "Should return no change since last save")

    def test_changes(self):
        case = wg.file_save_case_picker(latest[3], new[0], datetime.date(datetime.now()))
        self.assertEqual(case, wg.CHANGE_SINCE_LAST_SAVE, "Should return change since last save")

    def test_latest_is_empty(self):
        case = wg.file_save_case_picker(latest[6], new[0], datetime.date(datetime.now()))
        self.assertEqual(case, wg.CHANGE_SINCE_LAST_SAVE, "Should return change since last save")

    def test_generate_library_from_changes(self):
        pre_previous = wg.generate_library_from_change_history(original[0], change[0])
        expected_library = {'version': '1.0', 'date': str(datetime.date(datetime.now())), 'library': [{'name': 'b', 'tracks': [{'title': 'e', 'artist': 'e', 'album': 'e'},
                                                                                                                               {'title': 'f', 'artist': 'f', 'album': 'f'},
                                                                                                                               {'title': 'j', 'artist': 'j', 'album': 'j'}]},
                                                                                                      {'name': 'c', 'tracks': [{'title': 'g', 'artist': 'g', 'album': 'g'},
                                                                                                                               {'title': 'h', 'artist': 'h', 'album': 'h'},
                                                                                                                               {'title': 'i', 'artist': 'i', 'album': 'i'}]}]}
        self.assertEqual(pre_previous, expected_library, "Should generate a new library from change history")

    def test_generate_library_from_changes_no_changes(self):
        pre_previous = wg.generate_library_from_change_history(original[0], change[1])
        expected_library = {'version': '1.0', 'date': '2020-09-03', 'library': [{'name': 'a', 'tracks': [{'title': 'a', 'artist': 'a', 'album': 'a'},
                                                                                                         {'title': 'b', 'artist': 'b', 'album': 'b'},
                                                                                                         {'title': 'c', 'artist': 'c', 'album': 'c'}]},
                                                                                {'name': 'b', 'tracks': [{'title': 'd', 'artist': 'd', 'album': 'd'},
                                                                                                         {'title': 'e', 'artist': 'e', 'album': 'e'},
                                                                                                         {'title': 'f', 'artist': 'f', 'album': 'f'}]}]}
        self.assertEqual(pre_previous, expected_library, "Should generate a new library from change history")

    def test_add_to_change_history_empty(self):
        new_change_hist = wg.add_to_change_history(original[0], latest[4], change[1])
        expected_changes = {'version': '1.0', 'changes': [{'date': str(datetime.date(datetime.now())),
                                                           'added_playlists': [],
                                                           'removed_playlists': [{'name': 'b', 'removed_songs': [{'title': 'd', 'artist': 'd', 'album': 'd'},
                                                                                                                 {'title': 'e', 'artist': 'e', 'album': 'e'},
                                                                                                                 {'title': 'f', 'artist': 'f', 'album': 'f'}]}],
                                                           'modified_playlists': [{'name': 'a',
                                                                                   'added_songs': [{'title': 'i', 'artist': 'i', 'album': 'i'}],
                                                                                   'removed_songs': [{'title': 'c', 'artist': 'c', 'album': 'c'}]}]}]}
        self.assertEqual(new_change_hist, expected_changes, "Should add changes to the empty change history")

    def test_add_to_change_history_no_changes(self):
        new_change_hist = wg.add_to_change_history(original[0], latest[5], change[0])
        expected_changes = {'version': '1.0', 'changes': [{'date': str(datetime.date(datetime.now())),
                                                           'added_playlists': [{'name': 'c', 'added_songs': [{'title': 'g', 'artist': 'g', 'album': 'g'},
                                                                                                             {'title': 'h', 'artist': 'h', 'album': 'h'},
                                                                                                             {'title': 'i', 'artist': 'i', 'album': 'i'}]}],
                                                           'removed_playlists': [{'name': 'a', 'removed_songs': [{'title': 'a', 'artist': 'a', 'album': 'a'},
                                                                                                                 {'title': 'b', 'artist': 'b', 'album': 'b'},
                                                                                                                 {'title': 'c', 'artist': 'c', 'album': 'c'}]}],
                                                           'modified_playlists': [{'name': 'b',
                                                                                   'added_songs': [{'title': 'j', 'artist': 'j', 'album': 'j'}],
                                                                                   'removed_songs': [{'title': 'd', 'artist': 'd', 'album': 'd'}]}]}]}
        self.assertEqual(new_change_hist, expected_changes, "Should do nothing to the existing change history, because no changes have occurred")
