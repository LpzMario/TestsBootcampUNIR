package org.example

static void main(String[] args) {
    // Verificar que se haya proporcionado el nombre del archivo
    if (args.length == 0) {
        println "Error: Debe proporcionar el nombre del archivo como argumento"
        println "Uso: gradle run --args='<nombre_del_archivo>'"
        println "Ejemplo: gradle run --args='ejemplo.txt'"
        System.exit(1)
    }

    // Obtener el nombre del archivo desde los argumentos
    String fileName = args[0]

    println "=" * 60
    println "PROCESADOR DE ARCHIVOS CON GROOVY"
    println "=" * 60
    println()

    // Crear instancia de FileManager y procesar el archivo
    FileManager fileManager = new FileManager()
    fileManager.processFile(fileName)

    println()
    println "=" * 60
    println "Revisa el archivo application.log para ver el registro completo"
    println "=" * 60
}

