from unittest import TestCase
from app import app, update_guess_list, review_word_to_guess_list, update_score, update_high_score
from flask import session
from boggle import Boggle

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class RootTest(TestCase):

    # def setUp(self):
    #     """Stuff to do before every test."""

    #     self.client = app.test_client()
    #     app.config['TESTING'] = True


    def test_guess_submit_CHATGPT(self):
        with app.test_request_context():
            with app.test_client() as client:
                with client.session_transaction() as session:
                    session['board'] = [["C", "A", "T", "T", "T"], 
                                        ["C", "A", "T", "T", "T"], 
                                        ["C", "A", "T", "T", "T"], 
                                        ["C", "A", "T", "T", "T"], 
                                        ["C", "A", "T", "T", "T"]]

                resp = client.post('/guess', json={'guess': 'blue'})
                self.assertIn("not-on-board", resp.data.decode())

                resp = client.post('/guess', json={'guess': 'cat'})
                self.assertIn("ok", resp.data.decode())

    def test_guess_submit_ORIGINAL(self):
        with app.test_request_context():
            with app.test_client() as client:
                with client.session_transaction() as session:        
                    session['board'] = [["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"]]
                    
                    #INDENTATION ERROR!! Original code continued here. It needed to be back one tab. 
                resp = client.post('/guess', json = {'guess' : 'blue'})
                self.assertIn('not-on-board', resp.data.decode())

    def test_home_root(self):
        with app.test_client() as client:
            #make requests to flask via client
            resp = client.get('/')
            html = resp.get_data(as_text = True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Boggle Game</h1>', html)
   
    def test_update_guess_list(self):
        with app.test_request_context():
            with app.test_client() as client:

                word = 'hello'
                update_guess_list(word)

                guess_list = session['guess_list']
                self.assertIn(word.upper(), guess_list)

    def test_review_word(self):
        with app.test_request_context():
            with app.test_client() as client:

                word = 'hello'
                response = 'ok'
                testResp = review_word_to_guess_list(word, response)

                self.assertEqual(testResp, 'ok')

    def test_update_score(self):
        with app.test_request_context():
            with app.test_client() as client:

                update_score('jkasdfljnwcerlkuwnc')
                
                self.assertEqual(session['current_score'], 11)

    def test_update_high_score(self):
        with app.test_request_context():
            with app.test_client() as client:
                with client.session_transaction() as session:        
                    session['high_score'] = 22
                                        
                update_high_score(20)
                
                self.assertEqual(session['high_score'], 22)

    def test_start_game(self):
        with app.test_request_context():
            with app.test_client() as client:        
                resp = client.get('/game')
            
                self.assertEqual(session['current_score'], 0)

