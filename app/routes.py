from flask import Blueprint, request, jsonify, abort
from app import db
from app.models import Drawing, Shape, Annotation

main_bp = Blueprint('main', __name__)
bp = Blueprint('api', __name__)

@main_bp.route('/')
def home():
    return "Welcome to the Building Planner API. Use '/api' prefix for endpoints."

# Drawing Endpoints
@bp.route('/drawings', methods=['POST'])
def create_drawing():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Invalid input")
    
    drawing = Drawing(name=data['name'], description=data.get('description'))
    db.session.add(drawing)
    db.session.commit()
    
    return jsonify({
        'id': drawing.id,
        'name': drawing.name,
        'description': drawing.description,
        'created_at': drawing.created_at.isoformat()
    }), 201

@bp.route('/drawings/<int:id>', methods=['GET'])
def get_drawing(id):
    drawing = Drawing.query.get_or_404(id)
    return jsonify({
        'id': drawing.id,
        'name': drawing.name,
        'description': drawing.description,
        'created_at': drawing.created_at.isoformat(),        
        'shapes': [{'id': shape.id, 'type': shape.type, 'coordinates': shape.coordinates} for shape in drawing.shapes]
    })

@bp.route('/drawings/<int:id>', methods=['PUT'])
def update_drawing(id):
    drawing = Drawing.query.get_or_404(id)
    data = request.get_json()
    
    drawing.name = data.get('name', drawing.name)
    drawing.description = data.get('description', drawing.description)
    db.session.commit()
    
    return jsonify({
        'id': drawing.id,
        'name': drawing.name,
        'description': drawing.description,
        'created_at': drawing.created_at.isoformat()        
    })

@bp.route('/drawings/<int:id>', methods=['DELETE'])
def delete_drawing(id):
    drawing = Drawing.query.get_or_404(id)

    # Delete associated shapes and annotations
    shapes = Shape.query.filter_by(drawing_id=id).all()
    for shape in shapes:
        # Delete associated annotations
        annotations = Annotation.query.filter_by(shape_id=shape.id).all()
        for annotation in annotations:
            db.session.delete(annotation)
        db.session.delete(shape)

    # Finally delete the drawing
    db.session.delete(drawing)
    db.session.commit()

    return '', 204

# Shape Endpoints
@bp.route('/shapes', methods=['POST'])
def create_shape():
    data = request.get_json()
    if not data or 'drawing_id' not in data or 'type' not in data or 'coordinates' not in data:
        abort(400, description="Invalid input")
    
    shape = Shape(
        drawing_id=data['drawing_id'],
        type=data['type'],
        coordinates=data['coordinates']
    )
    db.session.add(shape)
    db.session.commit()
    
    return jsonify({
        'id': shape.id,
        'drawing_id': shape.drawing_id,
        'type': shape.type,
        'coordinates': shape.coordinates
    }), 201

@bp.route('/shapes/<int:id>', methods=['GET'])
def get_shape(id):
    shape = Shape.query.get_or_404(id)
    return jsonify({
        'id': shape.id,
        'drawing_id': shape.drawing_id,
        'type': shape.type,
        'coordinates': shape.coordinates,
        'annotations': [{'id': annotation.id, 'text': annotation.text, 'position': annotation.position} for annotation in shape.annotations]
    })

@bp.route('/shapes/<int:id>', methods=['PUT'])
def update_shape(id):
    shape = Shape.query.get_or_404(id)
    data = request.get_json()
    
    shape.type = data.get('type', shape.type)
    shape.coordinates = data.get('coordinates', shape.coordinates)
    db.session.commit()
    
    return jsonify({
        'id': shape.id,
        'drawing_id': shape.drawing_id,
        'type': shape.type,
        'coordinates': shape.coordinates
    })

@bp.route('/shapes/<int:id>', methods=['DELETE'])
def delete_shape(id):
    shape = Shape.query.get_or_404(id)

    # Delete associated annotations
    annotations = Annotation.query.filter_by(shape_id=id).all()
    for annotation in annotations:
        db.session.delete(annotation)

    # Delete the shape
    db.session.delete(shape)
    db.session.commit()

    return '', 204

# Annotation Endpoints
@bp.route('/annotations', methods=['POST'])
def create_annotation():
    data = request.get_json()
    if not data or 'shape_id' not in data or 'text' not in data or 'position' not in data:
        abort(400, description="Invalid input")
    
    annotation = Annotation(
        shape_id=data['shape_id'],
        text=data['text'],
        position=data['position']
    )
    db.session.add(annotation)
    db.session.commit()
    
    return jsonify({
        'id': annotation.id,
        'shape_id': annotation.shape_id,
        'text': annotation.text,
        'position': annotation.position
    }), 201

@bp.route('/annotations/<int:id>', methods=['GET'])
def get_annotation(id):
    annotation = Annotation.query.get_or_404(id)
    return jsonify({
        'id': annotation.id,
        'shape_id': annotation.shape_id,
        'text': annotation.text,
        'position': annotation.position
    })

@bp.route('/annotations/<int:id>', methods=['PUT'])
def update_annotation(id):
    annotation = Annotation.query.get_or_404(id)
    data = request.get_json()
    
    annotation.text = data.get('text', annotation.text)
    annotation.position = data.get('position', annotation.position)
    db.session.commit()
    
    return jsonify({
        'id': annotation.id,
        'shape_id': annotation.shape_id,
        'text': annotation.text,
        'position': annotation.position
    })

@bp.route('/annotations/<int:id>', methods=['DELETE'])
def delete_annotation(id):
    annotation = Annotation.query.get_or_404(id)
    db.session.delete(annotation)
    db.session.commit()
    return '', 204
