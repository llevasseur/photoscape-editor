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
const NTPath = path.join(app.getPath('documents'), 'NT')
const logDirectory = path.join(NTPath, 'logs')
const logFilePath = path.join(logDirectory, 'electron.log')

// Create the log directory if it doesn't exist
if (!fs.existsSync(logDirectory)) {
  fs.mkdirSync(logDirectory, { recursive: true })
}

// assets and json
const assetsSource = isPackaged
  ? path.join(__dirname, 'Resources', 'app', 'public', 'assets')
  : path.join(__dirname, 'public', 'assets')

const jsonSource = isPackaged
  ? path.join(__dirname, 'Resources', 'app', 'public', 'json')
  : path.join(__dirname, 'public', 'json')

const assetDirectory = path.join(NTPath, 'assets')
const jsonDestination = path.join(NTPath, 'json')

function copyFiles(source, destination) {
  // create the destination if it doesn't exist
  if (!fs.existsSync(destination)) {
    fs.mkdirSync(destination, { recursive: true })
  }

  // copy file into destination
  //fs.copyFileSync(source, destination)

  const isDirectory = fs.statSync(source).isDirectory()

  if (isDirectory) {
    // If it's a directory recursively traverse its contents
    fs.readdirSync(source).forEach((item) => {
      const sourcePath = path.join(source, item)
      const destinationPath = path.join(destination, item)

      if (fs.statSync(sourcePath).isDirectory()) {
        // if it's a directory, recursively copy its contents
        copyFiles(sourcePath, destinationPath)
      } else {
        // if its a file, copy it to the destination path
        fs.copyFileSync(sourcePath, destinationPath)
      }
    })
  }
}

copyFiles(assetsSource, assetDirectory)
copyFiles(jsonSource, jsonDestination)

// Start Flask Server
let backendPath = isPackaged
  ? os.platform() === 'win32'
    ? path.join(__dirname, 'Resources', 'app', 'backend', 'dist', 'app.exe')
    : path.join(__dirname, 'Resources', 'app', 'backend', 'dist', 'app')
  : os.platform() === 'win32'
  ? path.join(__dirname, 'backend', 'dist', 'app.exe')
  : path.join(__dirname, 'backend', 'dist', 'app')

logToFile(logFilePath, `__dirname: ${__dirname}`)
logToFile(logFilePath, `backend path: ${backendPath}`)

console.log(`backendPath: ${backendPath} `)

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
