import unittest
from playlist import playlist_compare

_OLD_PLAYLISTS = [
    [{'title': 'a', 'artist': 'a', 'album': 'a'},
     {'title': 'b', 'artist': 'b', 'album': 'b'},
     {'title': 'c', 'artist': 'c', 'album': 'c'}],
    [{'title': 'a', 'artist': 'a', 'album': 'a'},
     {'title': 'b', 'artist': 'b', 'album': 'b'}],
    [],
    None
]

_NEW_PLAYLISTS = [
    [{'title': 'a', 'artist': 'a', 'album': 'a'},
     {'title': 'b', 'artist': 'b', 'album': 'b'},
     {'title': 'c', 'artist': 'c', 'album': 'c'}],
    [{'title': 'a', 'artist': 'a', 'album': 'a'},
     {'title': 'b', 'artist': 'b', 'album': 'b'}],
    [{'title': 'a', 'artist': 'a', 'album': 'a'},
     {'title': 'b', 'artist': 'b', 'album': 'b'},
     {'title': 'd', 'artist': 'd', 'album': 'd'}],
    [],
    None,
    [{'title': 'b', 'artist': 'b', 'album': 'b'},
     {'title': 'c', 'artist': 'c', 'album': 'c'},
     {'title': 'a', 'artist': 'a', 'album': 'a'}],
    [{'title': 'a', 'artist': 'x', 'album': 'a'},
     {'title': 'x', 'artist': 'y', 'album': 'b'},
     {'title': 'x', 'artist': 'c', 'album': 'y'}]
]


class TestPlaylistCompare(unittest.TestCase):
    def test_adding_one_song(self):
        changes = playlist_compare.compare_playlist_versions(_OLD_PLAYLISTS[1], _NEW_PLAYLISTS[0])
        expected_result = {'added_songs': [{'title': 'c', 'artist': 'c', 'album': 'c'}], 'removed_songs': []}
        self.assertTrue(changes == expected_result, 'Should add one song')

    def test_removing_one_song(self):
        changes = playlist_compare.compare_playlist_versions(_OLD_PLAYLISTS[0], _NEW_PLAYLISTS[1])
        expected_result = {'added_songs': [], 'removed_songs': [{'title': 'c', 'artist': 'c', 'album': 'c'}]}
        self.assertTrue(changes == expected_result, 'Should remove one song')

    def test_remove_one_add_one(self):
        changes = playlist_compare.compare_playlist_versions(_OLD_PLAYLISTS[0], _NEW_PLAYLISTS[2])
        expected_result = {'added_songs': [{'title': 'd', 'artist': 'd', 'album': 'd'}], 'removed_songs': [{'title': 'c', 'artist': 'c', 'album': 'c'}]}
        self.assertTrue(changes == expected_result, 'Should remove one song and add a different one')

    def test_removing_all_songs(self):
        changes = playlist_compare.compare_playlist_versions(_OLD_PLAYLISTS[0], _NEW_PLAYLISTS[3])
        expected_result = {'added_songs': [], 'removed_songs': [{'title': 'a', 'artist': 'a', 'album': 'a'},
                                                                {'title': 'b', 'artist': 'b', 'album': 'b'},
                                                                {'title': 'c', 'artist': 'c', 'album': 'c'}]}
        self.assertTrue(changes == expected_result, 'Should remove all three songs')

    def test_adding_all_songs(self):
        changes = playlist_compare.compare_playlist_versions(_OLD_PLAYLISTS[2], _NEW_PLAYLISTS[0])
        expected_result = {'added_songs': [{'title': 'a', 'artist': 'a', 'album': 'a'},
                                           {'title': 'b', 'artist': 'b', 'album': 'b'},
                                           {'title': 'c', 'artist': 'c', 'album': 'c'}],
                           'removed_songs': []}
        self.assertTrue(changes == expected_result, 'Should add all three songs')

    def test_empty_to_empty(self):
        changes = playlist_compare.compare_playlist_versions(_OLD_PLAYLISTS[2], _NEW_PLAYLISTS[3])
        expected_result = {'added_songs': [], 'removed_songs': []}
        self.assertTrue(changes == expected_result, 'Both playlists are empty, nothing should happen')

    def test_identical(self):
        changes = playlist_compare.compare_playlist_versions(_OLD_PLAYLISTS[0], _NEW_PLAYLISTS[0])
        expected_result = {'added_songs': [], 'removed_songs': []}
        self.assertTrue(changes == expected_result, 'Both playlists are non-empty and identical, nothing should happen')

    def test_old_is_none(self):
        with self.assertRaises(TypeError):
            playlist_compare.compare_playlist_versions(_OLD_PLAYLISTS[3], _NEW_PLAYLISTS[0])
            print('Old playlist is type None, this message should never print')

    def test_new_is_none(self):
        with self.assertRaises(TypeError):
            playlist_compare.compare_playlist_versions(_OLD_PLAYLISTS[0], _NEW_PLAYLISTS[4])
            print('New playlist is type None, this message should never print')

    def test_both_are_none(self):
        with self.assertRaises(TypeError):
            playlist_compare.compare_playlist_versions(_OLD_PLAYLISTS[3], _NEW_PLAYLISTS[4])
            print('Both playlists are type None, this message should never print')

    def test_different_order(self):
        changes = playlist_compare.compare_playlist_versions(_OLD_PLAYLISTS[0], _NEW_PLAYLISTS[5])
        expected_result = {'added_songs': [], 'removed_songs': []}
        self.assertTrue(changes == expected_result, 'Both playlists are non-empty and identical but ordered differently, nothing should happen')

    def test_partial_matches(self):
        changes = playlist_compare.compare_playlist_versions(_OLD_PLAYLISTS[0], _NEW_PLAYLISTS[6])
        expected_result = {'added_songs': [{'title': 'a', 'artist': 'x', 'album': 'a'},
                                           {'title': 'x', 'artist': 'y', 'album': 'b'},
                                           {'title': 'x', 'artist': 'c', 'album': 'y'}],
                           'removed_songs': [{'title': 'a', 'artist': 'a', 'album': 'a'},
                                             {'title': 'b', 'artist': 'b', 'album': 'b'},
                                             {'title': 'c', 'artist': 'c', 'album': 'c'}]}
        self.assertTrue(changes == expected_result, 'Partial matches should be counted as different songs')
