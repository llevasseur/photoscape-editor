const electron = require('electron')
const path = require('path')
const app = electron.app
const BrowserWindow = electron.BrowserWindow

const isPackaged = require('electron-is-packaged').isPackaged
const fs = require('fs')
const os = require('os')
const { exec, execFile, spawn } = require('child_process')

let name = 'nt-brew'
let version = '0.1.0'

let mainWindow
let devOpts = false

function createWindow() {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    icon: 'favicon-16x16.png',
    title: `${name} v${version}`,
    webPreferences: { nodeIntegration: true, contextIsolation: false },
  })
  // and load the index.html of the app.
  mainWindow.loadFile(path.join(__dirname, '/build/index.html'))

  if (devOpts) {
    mainWindow.webContents.openDevTools()
  }
}

// Set App Name
app.setName(name)

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Backend

// Logging
function logToFile(logFilePath, message) {
  const timestamp = new Date().toISOString()
  const logMessage = `${timestamp}: ${message}\n`

  fs.appendFileSync(logFilePath, logMessage)
}

// Log File Path
const logDirectory = path.join(app.getPath('documents'), 'NT', 'logs')
const logFilePath = path.join(logDirectory, 'electron.log')

// Create the log directory if it doesn't exist
if (!fs.existsSync(logDirectory)) {
  fs.mkdirSync(logDirectory, { recursive: true })
}

// Start Flask Server
let backendPath = isPackaged
  ? os.platform() === 'win32'
    ? path.join(
        __dirname,
        'Resources',
        'app',
        'backend',
        'dist',
        'app',
        'app.exe'
      )
    : path.join(__dirname, 'Resources', 'app', 'backend', 'dist', 'app', 'app')
  : os.platform() === 'win32'
  ? path.join(__dirname, 'backend', 'dist', 'app', 'app.exe')
  : path.join(__dirname, 'backend', 'dist', 'app', 'app')

logToFile(logFilePath, `__dirname: ${__dirname}`)
logToFile(logFilePath, `backend path: ${backendPath}`)

let flaskProcess = execFile(backendPath)

// Log Flask server output
flaskProcess.stdout.on('data', (data) => {
  const message = `Flask server output: ${data}`
  //logToFile(logFilePath, message)
})

// Log any errors that occur
flaskProcess.stderr.on('data', (data) => {
  const errorMessage = `Error message: ${data}`
  logToFile(logFilePath, errorMessage)
})

// Handle Cleanup
app.on('before-quit', () => {
  flaskProcess.kill()
})
