package org.example

import java.time.LocalDateTime
    import java.time.format.DateTimeFormatter

    class Logger {
        private static final String LOG_FILE = "application.log"
        private DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")

        def log(String message) {
            String timestamp = LocalDateTime.now().format(formatter)
            String logMessage = "[$timestamp] $message"

            // Escribir en consola
            println logMessage

            // Escribir en archivo de log
            new File(LOG_FILE).withWriterAppend { writer ->
                writer.println(logMessage)
            }
        }

        def logInfo(String message) {
            log("INFO: $message")
        }

        def logError(String message) {
            log("ERROR: $message")
        }

        def logSuccess(String message) {
            log("SUCCESS: $message")
        }
    }

