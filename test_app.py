from app import app

def test_home():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200

def test_tailor_resume():
    tester = app.test_client()
    response = tester.post('/tailor-resume', data={
        'job_description': 'Data Scientist',
        'resume': 'Proficient in Python'
    })
    assert response.status_code == 200
    assert b'Tailored for Data Scientist' in response.data
