from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista para almacenar las tareas (en memoria)
tasks = []

# Contador para generar IDs únicos
next_id = 1


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    GET /tasks - Devuelve la lista de todas las tareas
    """
    return jsonify(tasks), 200


@app.route('/tasks', methods=['POST'])
def create_task():
    """
    POST /tasks - Crea una nueva tarea
    """
    global next_id
    
    # Obtener los datos del cuerpo de la solicitud
    data = request.get_json()
    
    # Validar que exista el campo 'title'
    if not data or 'title' not in data:
        return jsonify({
            "error": "El campo 'title' es requerido"
        }), 400
    
    # Validar que el título no esté vacío
    title = data['title']
    if not isinstance(title, str):
        return jsonify({
            "error": "El título debe ser un string"
        }), 400
    
    if not title.strip():
        return jsonify({
            "error": "El título no puede estar vacío"
        }), 400
    
    # Crear la nueva tarea
    new_task = {
        "id": next_id,
        "title": title.strip(),
        "completed": False
    }
    
    # Agregar la tarea a la lista
    tasks.append(new_task)
    next_id += 1
    
    return jsonify(new_task), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    PUT /tasks/<id> - Actualiza una tarea específica por su ID
    """
    # Buscar la tarea por ID
    task = None
    for t in tasks:
        if t['id'] == task_id:
            task = t
            break
    
    # Si no se encuentra la tarea, devolver 404
    if task is None:
        return jsonify({
            "error": f"Tarea con ID {task_id} no encontrada"
        }), 404
    
    # Obtener los datos del cuerpo de la solicitud
    data = request.get_json()
    
    # Validar que se envíen datos
    if not data:
        return jsonify({
            "error": "No se enviaron datos para actualizar"
        }), 400
    
    # Actualizar el título si se proporciona
    if 'title' in data:
        title = data['title']
        
        # Validar que el título sea un string
        if not isinstance(title, str):
            return jsonify({
                "error": "El título debe ser un string"
            }), 400
        
        # Validar que el título no esté vacío
        if not title.strip():
            return jsonify({
                "error": "El título no puede estar vacío"
            }), 400
        
        task['title'] = title.strip()
    
    # Actualizar el estado de completado si se proporciona
    if 'completed' in data:
        completed = data['completed']
        
        # Validar que completed sea un booleano
        if not isinstance(completed, bool):
            return jsonify({
                "error": "El campo 'completed' debe ser un booleano (true/false)"
            }), 400
        
        task['completed'] = completed
    
    return jsonify(task), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    DELETE /tasks/<id> - Elimina una tarea por su ID
    """
    global tasks
    
    # Buscar la tarea por ID
    task = None
    for t in tasks:
        if t['id'] == task_id:
            task = t
            break
    
    # Si no se encuentra la tarea, devolver 404
    if task is None:
        return jsonify({
            "error": f"Tarea con ID {task_id} no encontrada"
        }), 404
    
    # Eliminar la tarea de la lista
    tasks.remove(task)
    
    return jsonify({
        "message": f"Tarea con ID {task_id} eliminada exitosamente"
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)