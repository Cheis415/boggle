from unittest import TestCase
from app import app, games, uuid4, BoggleGame

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            # test that you're getting a template
            
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<table class="board">', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            # write a test for this route
            response = client.get('/api/new-game')
            gameDict = response.get_json()
            self.assertNotEqual(len(gameDict["gameId"]), 0)

            self.assertEqual(len(gameDict["board"]), 5)

    
    def test_api_score_word(self):
        """Test if words are valid."""

        with self.client as client:
            # write a test for this route

            # response = client.get('/api/new-game')
            # gameDict = response.get_json()
            # game_id = gameDict["gameId"]
            game_id = str(uuid4())
            test_var = [['w','a','D','O','G'],
                        ['w','a','D','O','G'],
                        ['w','a','D','O','G'],
                        ['w','a','d','o','g'],
                        ['w','a','d','o','g']]
            
            game = BoggleGame()
            game.board = test_var
            games[game_id] = game

            resp = client.post("/", json={"word": "DOG", "game_id": game_id})
            result = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            #print("OBJECTTTTTT",games[game_id].board)
            self.assertEqual(result["result"], "ok")
