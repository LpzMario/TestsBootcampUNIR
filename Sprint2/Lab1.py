import requests
import argparse
import sys

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.base_url = "https://httpbin.org"
    
    def authenticate(self, username, password, max_attempts=3):
        """Autentica al usuario usando httpbin.org"""
        attempts = 0
        
        while attempts < max_attempts:
            try:
                # Enviar solicitud de autenticación a httpbin
                response = requests.get(
                    f"{self.base_url}/basic-auth/{username}/{password}",
                    auth=(username, password),
                    timeout=10
                )
                
                if response.status_code == 200:
                    print("Autenticación exitosa.\n")
                    return True
                else:
                    attempts += 1
                    remaining_attempts = max_attempts - attempts
                    if remaining_attempts > 0:
                        print(f"Credenciales incorrectas. Intentos restantes: {remaining_attempts}")
                    else:
                        print("Demasiados intentos fallidos. Acceso denegado.")
                        return False
                        
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
    
    def add_task(self):
        """Agrega una nueva tarea"""
        title = input("Ingrese el título de la tarea: ").strip()
        
        if not title:
            print("Error: El título no puede estar vacío.")
            return
        
        # Verificar si la tarea ya existe
        for task in self.tasks:
            if task['title'].lower() == title.lower():
                print("Error: Ya existe una tarea con ese título.")
                return
        
        # Agregar nueva tarea
        new_task = {
            'title': title,
            'status': 'pendiente'
        }
        self.tasks.append(new_task)
        print(f"Tarea '{title}' agregada.")
    
    def list_tasks(self):
        """Lista todas las tareas"""
        if not self.tasks:
            print("No hay tareas registradas.")
            return
        
        print("\n-----------------------")
        print("\n--- Lista de Tareas ---")
        print("\n-----------------------")
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task['title']} [{task['status']}]")
        print("-------------------------\n")
    
    def delete_task(self):
        """Elimina una tarea por título"""
        if not self.tasks:
            print("No hay tareas para eliminar.")
            return
        
        self.list_tasks()
        title = input("Ingrese el título de la tarea a eliminar: ").strip()
        
        if not title:
            print("Error: El título no puede estar vacío.")
            return
        
        # Buscar y eliminar la tarea
        for i, task in enumerate(self.tasks):
            if task['title'].lower() == title.lower():
                deleted_task = self.tasks.pop(i)
                print(f"Tarea '{deleted_task['title']}' eliminada.")
                return
        
        print("Error: No se encontró una tarea con ese título.")
    
    def show_menu(self):
        """Muestra el menú principal"""
        print("\n---------------------------------")
        print("--- Menú de Gestión de Tareas ---")
        print("1. Agregar tarea")
        print("2. Listar tareas")
        print("3. Eliminar tarea")
        print("4. Salir")
        print("---------------------------------")
    
    def run_interactive_mode(self):
        """Ejecuta el modo interactivo después de la autenticación"""
        while True:
            self.show_menu()
            choice = input("Elija una opción (1-4): ").strip()
            
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.list_tasks()
            elif choice == '3':
                self.delete_task()
            elif choice == '4':
                print("Saliendo del programa.")
                break
            else:
                print("Error: Opción no válida. Por favor, elija una opción entre 1 y 4.")

def main():
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Sistema de Gestión de Tareas TechCorp')
    parser.add_argument('-u', '--username', required=True, help='Nombre de usuario')
    parser.add_argument('-p', '--password', required=True, help='Contraseña')
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Crear instancia del gestor de tareas
    task_manager = TaskManager()
    
    # Autenticar usuario
    if task_manager.authenticate(args.username, args.password):
        # Ejecutar modo interactivo
        task_manager.run_interactive_mode()
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()