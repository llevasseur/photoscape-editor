const fs = require('fs')

class Logger {
  static logToFile(logFilePath, message) {
    const timestamp = new Date().toISOString()
    const logMessage = `${timestamp}: ${message}\n`

    fs.appendFileSync(logFilePath, logMessage)
  }

  static logError(module, errorCode, message, logFilePath) {
    const formattedMessage = `[ERROR][${module}][${errorCode}] ${message}`
    console.error(formattedMessage)
    this.logToFile(logFilePath, formattedMessage)
  }

  static logInfo(module, message, logFilePath) {
    const formattedMessage = `[INFO][${module}] ${message}`
    console.log(formattedMessage)
    this.logToFile(logFilePath, formattedMessage)
  }

  // Log File Path
  static logWarning(module, message, logFilePath) {
    const formattedMessage = `[WARNING][${module}] ${message}`
    this.logToFile(logFilePath, formattedMessage)
  }
  //-----------------------------------------------------------------
}

module.exports = Logger
