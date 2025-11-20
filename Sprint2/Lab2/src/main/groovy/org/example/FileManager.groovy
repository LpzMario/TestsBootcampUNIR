package org.example

class FileManager {
    private Logger logger

    FileManager() {
        this.logger = new Logger()
    }

    def processFile(String fileName) {
        try {
            logger.logInfo("Iniciando procesamiento del archivo: $fileName")

            // Verificar que el archivo existe
            File inputFile = new File("src/main/resources/input/$fileName")
            if (!inputFile.exists()) {
                logger.logError("El archivo $fileName no existe en la carpeta src/main/resources/input/")
                return
            }

            // Leer el contenido del archivo
            logger.logInfo("Leyendo contenido del archivo...")
            List<String> lines = inputFile.readLines()
            logger.logSuccess("Archivo leído correctamente. Total de líneas: ${lines.size()}")

            // Transformación funcional del contenido
            logger.logInfo("Aplicando transformaciones funcionales...")

            // 1. Filtrar líneas que contienen "Groovy" (usando findAll)
            def linesWithGroovy = lines.findAll { line ->
                line.toLowerCase().contains('groovy')
            }
            logger.logInfo("Líneas que contienen 'Groovy': ${linesWithGroovy.size()}")

            // 2. Transformar cada línea (usando collect)
            def transformedLines = lines.collect { line ->
                ">>> ${line.toUpperCase()} [Procesada]"
            }

            // 3. Agregar numeración y longitud (usando collect con índice)
            def numberedLines = lines.withIndex().collect { line, idx ->
                "Línea ${idx + 1} (${line.length()} caracteres): $line"
            }

            // 4. Contar total de caracteres (usando inject)
            def totalChars = lines.inject(0) { sum, line ->
                sum + line.length()
            }
            logger.logInfo("Total de caracteres procesados: $totalChars")

            // 5. Crear resumen estadístico
            def summary = createSummary(lines)

            // Escribir archivo transformado
            String outputFileName = "src/main/resources/input/copy_$fileName"
            logger.logInfo("Escribiendo archivo transformado: $outputFileName")

            new File(outputFileName).withWriter { writer ->
                writer.println("=" * 60)
                writer.println("ARCHIVO PROCESADO FUNCIONALMENTE")
                writer.println("=" * 60)
                writer.println()

                writer.println("--- CONTENIDO ORIGINAL ---")
                lines.each { line ->
                    writer.println(line)
                }
                writer.println()

                writer.println("--- LÍNEAS TRANSFORMADAS (MAYÚSCULAS) ---")
                transformedLines.each { line ->
                    writer.println(line)
                }
                writer.println()

                writer.println("--- LÍNEAS NUMERADAS CON LONGITUD ---")
                numberedLines.each { line ->
                    writer.println(line)
                }
                writer.println()

                writer.println("--- LÍNEAS QUE CONTIENEN 'GROOVY' ---")
                linesWithGroovy.each { line ->
                    writer.println("* $line")
                }
                writer.println()

                writer.println("--- RESUMEN ESTADÍSTICO ---")
                writer.println(summary)
                writer.println()

                writer.println("=" * 60)
                writer.println("Procesado el: ${new Date()}")
                writer.println("=" * 60)
            }

            logger.logSuccess("Archivo procesado y guardado exitosamente: $outputFileName")
            logger.logInfo("Proceso completado")

        } catch (Exception e) {
            logger.logError("Error al procesar el archivo: ${e.message}")
            e.printStackTrace()
        }
    }

    private String createSummary(List<String> lines) {
        def totalLines = lines.size()
        def totalChars = lines.inject(0) { sum, line -> sum + line.length() }
        def avgCharsPerLine = totalLines > 0 ? totalChars / totalLines : 0
        def longestLine = lines.max { it.length() }
        def shortestLine = lines.min { it.length() }

        return """
Total de líneas: $totalLines
Total de caracteres: $totalChars
Promedio de caracteres por línea: ${avgCharsPerLine.round(2)}
Línea más larga: ${longestLine?.length() ?: 0} caracteres
Línea más corta: ${shortestLine?.length() ?: 0} caracteres
Palabras totales: ${lines.sum { it.split(/\s+/).size() }}
        """.trim()
    }
}

