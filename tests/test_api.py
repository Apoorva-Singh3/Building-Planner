import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
from app import create_app, db
from app.models import Drawing, Shape, Annotation

@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

@pytest.fixture(scope='module')
def init_db():
    app = create_app('testing')
    with app.app_context():
        db.create_all()

        # Create sample data
        drawing = Drawing(name='Sample Drawing')
        db.session.add(drawing)
        db.session.commit()

        shape = Shape(drawing_id=drawing.id, type='circle', coordinates=[(0, 0), (1, 1)])
        db.session.add(shape)
        db.session.commit()

        annotation = Annotation(shape_id=shape.id, text='Sample Annotation', position=(1, 1))
        db.session.add(annotation)
        db.session.commit()

        yield db
        db.drop_all()

def test_create_drawing(test_client):
    response = test_client.post('/api/drawings', json={
        'name': 'Test Drawing',
        'description': 'A test drawing'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['name'] == 'Test Drawing'
    assert data['description'] == 'A test drawing'

def test_get_drawing(test_client, init_db):
    drawing = Drawing.query.first()
    response = test_client.get(f'/api/drawings/{drawing.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == drawing.name

def test_update_drawing(test_client, init_db):
    drawing = Drawing.query.first()
    response = test_client.put(f'/api/drawings/{drawing.id}', json={
        'name': 'Updated Drawing',
        'description': 'Updated description'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Updated Drawing'
    assert data['description'] == 'Updated description'

def test_delete_drawing(test_client, init_db):
    drawing_id = Drawing.query.first().id
    response = test_client.delete(f'/api/drawings/{drawing_id}')
    assert response.status_code == 204
    assert init_db.session.get(Drawing, drawing_id) is None

def test_create_shape(test_client, init_db):
    drawing = Drawing.query.first()
    response = test_client.post('/api/shapes', json={
        'drawing_id': drawing.id,
        'type': 'rectangle',
        'coordinates': [(2, 2), (3, 3)]
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['type'] == 'rectangle'

def test_get_shape(test_client, init_db):
    shape = Shape.query.first()
    response = test_client.get(f'/api/shapes/{shape.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == shape.type

def test_update_shape(test_client, init_db):
    shape = Shape.query.first()
    response = test_client.put(f'/api/shapes/{shape.id}', json={
        'type': 'triangle',
        'coordinates': [(4, 4), (5, 5)]
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['type'] == 'triangle'

def test_delete_shape(test_client, init_db):
    shape_id = Shape.query.first().id
    response = test_client.delete(f'/api/shapes/{shape_id}')
    assert response.status_code == 204
    db.session.commit()  # Commit the deletion
    assert db.session.query(Shape).get(shape_id) is None

def test_create_annotation(test_client, init_db):
    shape = Shape.query.first()
    response = test_client.post('/api/annotations', json={
        'shape_id': shape.id,
        'text': 'New Annotation',
        'position': (2, 2)
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['text'] == 'New Annotation'

def test_get_annotation(test_client, init_db):
    annotation = Annotation.query.first()
    response = test_client.get(f'/api/annotations/{annotation.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['text'] == annotation.text

def test_update_annotation(test_client, init_db):
    annotation = Annotation.query.first()
    response = test_client.put(f'/api/annotations/{annotation.id}', json={
        'text': 'Updated Annotation',
        'position': (3, 3)
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['text'] == 'Updated Annotation'

def test_delete_annotation(test_client, init_db):
    annotation_id = Annotation.query.first().id
    response = test_client.delete(f'/api/annotations/{annotation_id}')
    assert response.status_code == 204
    db.session.commit()  # Commit the deletion
    assert db.session.query(Annotation).get(annotation_id) is None
