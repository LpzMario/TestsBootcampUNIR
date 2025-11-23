from flask import Flask, request, jsonify

app = Flask(__name__)

# Variable global para almacenar el valor
value = None


@app.route('/value', methods=['GET'])
def get_value():
    """
    GET /value - Devuelve el valor de la variable
    """
    if value is None:
        return jsonify({
            "error": "No se ha establecido ningún valor"
        }), 404
    
    return jsonify({
        "value": value
    }), 200


@app.route('/value', methods=['POST'])
def create_value():
    """
    POST /value - Crea un nuevo valor para la variable
    """
    global value
    
    # Validar que ya no exista un valor
    if value is not None:
        return jsonify({
            "error": "El valor ya ha sido establecido. Use PUT para actualizarlo."
        }), 400
    
    # Obtener los datos del cuerpo de la solicitud
    data = request.get_json()
    
    # Validar que exista el campo 'value'
    if not data or 'value' not in data:
        return jsonify({
            "error": "El campo 'value' es requerido"
        }), 400
    
    # Validar que el valor no esté vacío y sea un string
    new_value = data['value']
    if not isinstance(new_value, str):
        return jsonify({
            "error": "El valor debe ser un string"
        }), 400
    
    if not new_value.strip():
        return jsonify({
            "error": "El valor no puede estar vacío"
        }), 400
    
    # Crear el valor
    value = new_value
    
    return jsonify({
        "message": "Valor creado exitosamente",
        "value": value
    }), 201


@app.route('/value', methods=['PUT'])
def update_value():
    """
    PUT /value - Actualiza el valor de la variable existente
    """
    global value
    
    # Validar que exista un valor para actualizar
    if value is None:
        return jsonify({
            "error": "No existe ningún valor para actualizar. Use POST para crear uno."
        }), 404
    
    # Obtener los datos del cuerpo de la solicitud
    data = request.get_json()
    
    # Validar que exista el campo 'value'
    if not data or 'value' not in data:
        return jsonify({
            "error": "El campo 'value' es requerido"
        }), 400
    
    # Validar que el valor no esté vacío y sea un string
    new_value = data['value']
    if not isinstance(new_value, str):
        return jsonify({
            "error": "El valor debe ser un string"
        }), 400
    
    if not new_value.strip():
        return jsonify({
            "error": "El valor no puede estar vacío"
        }), 400
    
    # Actualizar el valor
    value = new_value
    
    return jsonify({
        "message": "Valor actualizado exitosamente",
        "value": value
    }), 200


@app.route('/value', methods=['DELETE'])
def delete_value():
    """
    DELETE /value - Elimina el valor de la variable
    """
    global value
    
    # Validar que exista un valor para eliminar
    if value is None:
        return jsonify({
            "error": "No existe ningún valor para eliminar"
        }), 404
    
    # Eliminar el valor
    value = None
    
    return jsonify({
        "message": "Valor eliminado exitosamente"
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)