from app import app

def test1():
    response = app.test_client().get('/books')
   
    assert response.status_code == 200