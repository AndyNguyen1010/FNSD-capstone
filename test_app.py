import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie
from dotenv import load_dotenv,find_dotenv
env_file = find_dotenv('.env.test')
load_dotenv(env_file)
database_path = os.environ.get('DATABASE_URL')
MANAGER_TOKEN = os.environ.get('MANAGER_TOKEN')
BARISTA_TOKEN = os.environ.get('BARISTA_TOKEN')
class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

    def tearDown(self):
        pass

    def test_get_actors_manager_role(self):
        res = self.client().get('/actors',
                                headers={'Authorization':
                                             'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_get_actors_barista(self):
        res = self.client().get('/actors',
                                headers={'Authorization':
                                             'Bearer ' + BARISTA_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_post_new_actor_manager(self):
        res = self.client().post('/actors',
                                 json={
                                     'name': "George",
                                     'age': 28,
                                     'gender': 'MALE'
                                 },
                                 headers={'Authorization':
                                              'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['actor'])

    def test_post_new_actor(self):
        res = self.client().post('/actors',
                                 json={
                                     'name': "George",
                                     'age': 28,
                                     'gender': 'MALE'
                                 },
                                 headers={'Authorization':
                                              'Bearer ' + BARISTA_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_post_new_actor_name_missing(self):
        res = self.client().post('/actors',
                                 json={
                                     'age': 28,
                                     'gender': 'MALE'
                                 },
                                 headers={'Authorization':
                                              'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_post_new_actor_gender_missing(self):
        res = self.client().post('/actors',
                                 json={
                                     'name': "George",
                                     'age': 28,
                                 },
                                 headers={'Authorization':
                                              'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_delete_actor(self):
        res = self.client().post('/actors',  json={
                                     'name': "George",
                                     'age': 28,
                                     'gender': 'MALE'
                                 },
                                 headers={'Authorization':
                                              'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        actor_id = data['actor']['id']

        res = self.client().delete('/actors/{}'.format(actor_id),
                                   headers={'Authorization':
                                                'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['id'], actor_id)

    def test_delete_actor_not_found(self):
        res = self.client().delete('/actors/999',
                                   headers={'Authorization':
                                                'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_patch_actor(self):
        res = self.client().patch('/actors/2',
                                  json={
                                      'name': "George",
                                      'age': 28,
                                      'gender': 'MALE'
                                  },
                                  headers={'Authorization':
                                               'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['id'], 2)

    # PATCH Negative case - Update age for non-existent actor
    # - Director Role
    def test_patch_actor_not_found(self):
        res = self.client().patch('/actors/999',
                                  json={
                                      'name': "George",
                                      'age': 28,
                                      'gender': 'MALE'
                                  },
                                  headers={'Authorization':
                                               'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_get_movies_barista(self):
        res = self.client().get('/movies?page=1',
                                headers={'Authorization':
                                             'Bearer ' + BARISTA_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_get_movies_manager(self):
        res = self.client().get('/movies',
                                headers={'Authorization':
                                             'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_post_new_movie(self):
        res = self.client().post('/movies',
                                 json={'title': "TOM NGUYEN",
                                       'release': "2023-10-10"},
                                 headers={'Authorization':
                                              'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)
        id = data.get('movie').get('id')

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['movie'])

    def test_post_new_movie_title_missing(self):
        res = self.client().post('/movies',
                                 json={
                                     'release': "2023-10-10"},
                                 headers={'Authorization':
                                              'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_post_new_movie_reldate_missing(self):
        res = self.client().post('/movies',
                                 json={'title': "TOM NGUYEN"},
                                 headers={'Authorization':
                                              'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_delete_movie(self):
        res = self.client().post('/movies',
                                 json={'title': "TOMNGUYEN",
                                       'release': "2023-10-10"},
                                 headers={'Authorization':
                                              'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)

        movie_id = data['movie']['id']

        res = self.client().delete('/movies/{}'.format(movie_id),
                                   headers={'Authorization':
                                                'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['id'], movie_id)

    def test_delete_movie_not_found(self):
        res = self.client().delete('/movies/999',
                                   headers={'Authorization':
                                                'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_patch_movie(self):
        res = self.client().patch('/movies/2',
                                  json={'title': "TOMNGUYEN",
                                        'release': "2023-10-10"},
                                  headers={'Authorization':
                                               'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data.get('movie')['id'], 2)

    def test_patch_movie_not_found(self):
        res = self.client().patch('/movies/99',
                                  json={'title': "TOMNGUYEN",
                                        'release': "2023-10-10"},
                                  headers={'Authorization':
                                               'Bearer ' + MANAGER_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_no_auth(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],
                         'Authorization header is expected.')

    def test_no_permission(self):
        res = self.client().post('/movies', json={'title': "TOMNGUYEN",
                                                  'release': "2023-10-10"},
                                 headers={'Authorization':
                                              'Bearer ' + BARISTA_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission Not found')


if __name__ == "__main__":
    unittest.main()
