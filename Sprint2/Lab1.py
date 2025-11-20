# 1. IMPORTACIÓN DE LIBRERÍAS NECESARIAS
import requests    # 1.1 Para realizar peticiones HTTP a servicios web
import argparse    # 1.2 Para procesar argumentos de línea de comandos
import sys         # 1.3 Para funciones del sistema como salir del programa

# 2. DEFINICIÓN DE LA CLASE PRINCIPAL TaskManager
class TaskManager:
    # 2.1 MÉTODO INICIALIZADOR - Se ejecuta al crear el objeto
    def __init__(self):
        # 2.1.1 Inicializar lista vacía para almacenar las tareas
        self.tasks = []
        # 2.1.2 Definir la URL del servicio de autenticación
        self.base_url = "https://httpbin.org"
    
    # 2.2 MÉTODO DE AUTENTICACIÓN CON SERVICIO EXTERNO
    def authenticate(self, username, password, max_attempts=3):
        """Autentica al usuario usando httpbin.org"""
        # 2.2.1 Contador para llevar registro de intentos fallidos
        attempts = 0
        
        # 2.2.2 Bucle que permite hasta 3 intentos de autenticación
        while attempts < max_attempts:
            try:
                # 2.2.3 Realizar petición HTTP GET al servicio de autenticación
                response = requests.get(
                    # 2.2.4 Construir URL con usuario y contraseña como parámetros
                    f"{self.base_url}/basic-auth/{username}/{password}",
                    # 2.2.5 Incluir credenciales en cabecera de autenticación básica
                    auth=(username, password),
                    # 2.2.6 Establecer tiempo máximo de espera de 10 segundos
                    timeout=10
                )
                
                # 2.2.7 Verificar si la autenticación fue exitosa (código 200)
                if response.status_code == 200:
                    print("Autenticación exitosa.\n")
                    return True  # 2.2.8 Retornar True para indicar éxito
                else:
                    # 2.2.9 Incrementar contador de intentos fallidos
                    attempts += 1
                    # 2.2.10 Calcular cuántos intentos quedan disponibles
                    remaining_attempts = max_attempts - attempts
                    # 2.2.11 Informar al usuario sobre intentos restantes
                    if remaining_attempts > 0:
                        print(f"Credenciales incorrectas. Intentos restantes: {remaining_attempts}")
                    else:
                        # 2.2.12 Bloquear acceso después del tercer intento fallido
                        print("Demasiados intentos fallidos. Acceso denegado.")
                        return False
                        
            # 2.2.13 Manejar errores de conexión o de red
            except requests.exceptions.RequestException as e:
                attempts += 1
                print(f"Error de conexión: {e}")
                remaining_attempts = max_attempts - attempts
                if remaining_attempts > 0:
                    print(f"Intentos restantes: {remaining_attempts}")
                else:
                    print("Demasiados intentos fallidos. Acceso denegado.")
                    return False
        
        return False
    
    # 2.3 MÉTODO PARA AGREGAR NUEVAS TAREAS
    def add_task(self):
        """Agrega una nueva tarea"""
        # 2.3.1 Solicitar al usuario el título de la tarea
        title = input("Ingrese el título de la tarea: ").strip()
        
        # 2.3.2 Validar que el título no esté vacío
        if not title:
            print("Error: El título no puede estar vacío.")
            return
        
        # 2.3.3 Verificar si ya existe una tarea con el mismo título
        for task in self.tasks:
            if task['title'].lower() == title.lower():
                print("Error: Ya existe una tarea con ese título.")
                return
        
        # 2.3.4 Crear diccionario con los datos de la nueva tarea
        new_task = {
            'title': title,           # 2.3.5 Almacenar el título proporcionado
            'status': 'pendiente'     # 2.3.6 Estado inicial siempre "pendiente"
        }
        # 2.3.7 Agregar la nueva tarea al final de la lista
        self.tasks.append(new_task)
        print(f"Tarea '{title}' agregada.")
    
    # 2.4 MÉTODO PARA MOSTRAR TODAS LAS TAREAS
    def list_tasks(self):
        """Lista todas las tareas"""
        # 2.4.1 Verificar si hay tareas en la lista
        if not self.tasks:
            print("No hay tareas registradas.")
            return
        
        # 2.4.2 Mostrar encabezado decorativo de la lista
        print("\n-----------------------")
        print("\n--- Lista de Tareas ---")
        print("\n-----------------------")
        # 2.4.3 Recorrer todas las tareas con numeración automática
        for i, task in enumerate(self.tasks, 1):
            # 2.4.4 Mostrar cada tarea con su número, título y estado
            print(f"{i}. {task['title']} [{task['status']}]")
        print("-------------------------\n")
    
    # 2.5 MÉTODO PARA ELIMINAR TAREAS EXISTENTES
    def delete_task(self):
        """Elimina una tarea por título"""
        # 2.5.1 Verificar que existan tareas para eliminar
        if not self.tasks:
            print("No hay tareas para eliminar.")
            return
        
        # 2.5.2 Mostrar la lista actual de tareas al usuario
        self.list_tasks()
        # 2.5.3 Solicitar el título de la tarea a eliminar
        title = input("Ingrese el título de la tarea a eliminar: ").strip()
        
        # 2.5.4 Validar que se haya ingresado un título
        if not title:
            print("Error: El título no puede estar vacío.")
            return
        
        # 2.5.5 Buscar la tarea en la lista (búsqueda case-insensitive)
        for i, task in enumerate(self.tasks):
            if task['title'].lower() == title.lower():
                # 2.5.6 Eliminar la tarea encontrada de la lista
                deleted_task = self.tasks.pop(i)
                print(f"Tarea '{deleted_task['title']}' eliminada.")
                return  # 2.5.7 Salir del método después de eliminar
        
        # 2.5.8 Mostrar error si no se encuentra la tarea
        print("Error: No se encontró una tarea con ese título.")
    
    # 2.6 MÉTODO PARA MOSTRAR EL MENÚ DE OPCIONES
    def show_menu(self):
        """Muestra el menú principal"""
        print("\n---------------------------------")
        print("--- Menú de Gestión de Tareas ---")
        print("1. Agregar tarea")    # 2.6.1 Opción para crear nueva tarea
        print("2. Listar tareas")    # 2.6.2 Opción para ver todas las tareas
        print("3. Eliminar tarea")   # 2.6.3 Opción para eliminar tarea existente
        print("4. Salir")            # 2.6.4 Opción para terminar el programa
        print("---------------------------------")
    
    # 2.7 MÉTODO PRINCIPAL DE INTERACCIÓN CON EL USUARIO
    def run_interactive_mode(self):
        """Ejecuta el modo interactivo después de la autenticación"""
        # 2.7.1 Bucle infinito que mantiene el programa ejecutándose
        while True:
            # 2.7.2 Mostrar el menú de opciones al usuario
            self.show_menu()
            # 2.7.3 Solicitar al usuario que elija una opción
            choice = input("Elija una opción (1-4): ").strip()
            
            # 2.7.4 Ejecutar la acción correspondiente a la opción seleccionada
            if choice == '1':
                self.add_task()       # 2.7.5 Llamar método para agregar tarea
            elif choice == '2':
                self.list_tasks()     # 2.7.6 Llamar método para listar tareas
            elif choice == '3':
                self.delete_task()    # 2.7.7 Llamar método para eliminar tarea
            elif choice == '4':
                # 2.7.8 Mensaje de despedida y salir del bucle
                print("Saliendo del programa.")
                break
            else:
                # 2.7.9 Manejar selección de opción no válida
                print("Error: Opción no válida. Por favor, elija una opción entre 1 y 4.")

# 3. FUNCIÓN PRINCIPAL DEL PROGRAMA
def main():
    # 3.1 CONFIGURACIÓN DEL PROCESADOR DE ARGUMENTOS
    # 3.1.1 Crear objeto para manejar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Sistema de Gestión de Tareas TechCorp')
    # 3.1.2 Definir argumento obligatorio para el nombre de usuario
    parser.add_argument('-u', '--username', required=True, help='Nombre de usuario')
    # 3.1.3 Definir argumento obligatorio para la contraseña
    parser.add_argument('-p', '--password', required=True, help='Contraseña')
    
    # 3.2 PROCESAMIENTO DE ARGUMENTOS
    # 3.2.1 Leer y validar los argumentos proporcionados por el usuario
    args = parser.parse_args()
    
    # 3.3 INICIALIZACIÓN DEL GESTOR DE TAREAS
    # 3.3.1 Crear una instancia de la clase TaskManager
    task_manager = TaskManager()
    
    # 3.4 PROCESO DE AUTENTICACIÓN
    # 3.4.1 Intentar autenticar al usuario con las credenciales proporcionadas
    if task_manager.authenticate(args.username, args.password):
        # 3.4.2 Si la autenticación es exitosa, iniciar el modo interactivo
        task_manager.run_interactive_mode()
    else:
        # 3.4.3 Si la autenticación falla, terminar el programa con código de error
        sys.exit(1)

# 4. VERIFICACIÓN DE EJECUCIÓN DIRECTA
if __name__ == "__main__":
    # 4.1 Ejecutar la función main() solo si el script se ejecuta directamente
    main()