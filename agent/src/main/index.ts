import os from 'os'
import { join } from 'path'
import { app, BrowserWindow, protocol, session,ipcMain ,globalShortcut } from 'electron'
import windowStateKeeper from 'electron-window-state'
import remoteMain from '@electron/remote/main'


import './initConfig'
import initTray from './tray'
import { createWindow, winPagePathMap } from './window'

const foo = "https://www.baidu.com";


remoteMain.initialize()

const isWin7 = os.release().startsWith('6.1')
if (isWin7) app.disableHardwareAcceleration()

if (app.isPackaged) {
  if (!app.requestSingleInstanceLock()) {
    app.quit()
    process.exit(0)
  }
  if (process.platform === 'darwin') {
    app.dock.hide()
  }
}

app.commandLine.appendSwitch('disable-renderer-backgrounding')
app.commandLine.appendSwitch('disable-background-timer-throttling')
app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required')
app.commandLine.appendSwitch('enable-features', 'WebSpeechAPI')


let win: BrowserWindow | undefined
let mainWindowState: windowStateKeeper.State

app
  .whenReady()
  .then(() => {
    // Register a 'CommandOrControl+X' shortcut listener.
    const ret = globalShortcut.register('Alt+A', () => {
      win?.focus()

      const script =`
        document.getElementById("chatbox").style.opacity="1";
        document.getElementById("input").focus();
      `
      win?.webContents.executeJavaScript(script)
      console.log('Alt+A is pressed')
    })

    if (!ret) {
      console.log('registration failed')
    }

    // Check whether a shortcut is registered.
    console.log(globalShortcut.isRegistered('Alt+A'))


    protocol.registerFileProtocol('file', (request, callback) => {
      const url = request.url.replace('file://', '')
      const decodedUrl = decodeURI(url)
      try {
        return callback(decodedUrl)
      } catch (error) {
        console.error('Could not get file path:', error)
        return callback('404')
      }
    })
  })
  .then(() => {
    mainWindowState = windowStateKeeper({
      defaultHeight: 600,
      defaultWidth: 350,
    })
  })
  .then(async () => {
    const options = {
      title: 'Ailive',
      alwaysOnTop: true,
      autoHideMenuBar: true,
      acceptFirstMouse: true,
      hasShadow: false,
      transparent: true,
      frame: false,
      x: mainWindowState.x,
      y: mainWindowState.y,
      width: mainWindowState.width,
      height: mainWindowState.height,
      skipTaskbar: true,
      minimizable: false,
      maximizable: false,
      resizable: false,
      // titleBarStyle: 'hidden',
      webPreferences: {
        preload: join(__dirname, '../preload/index.cjs'),
        webSecurity: false,
        backgroundThrottling: false,
        nodeIntegration: true,
      },
    }

    win = await createWindow(options)


    if (win) {
      mainWindowState.manage(win)
      initTray(win)
      win.on('focus', () => {
        // 窗口获得焦点时的处理逻辑
        win?.webContents.executeJavaScript('document.getElementById("input").focus();')
      });
    
    }
  })

app.on('window-all-closed', () => {
  winPagePathMap.clear()
  app.quit()
})

app.on('browser-window-created', (ev, win) => {
  remoteMain.enable(win.webContents)
})

app.on('second-instance', () => {
  const win = BrowserWindow.getAllWindows()[0]
  if (win) {
    // Someone tried to run a second instance, we should focus our window.
    if (win.isMinimized()) win.restore()
    win.focus()
  }
})

app.on('activate', () => {
  const allWindows = BrowserWindow.getAllWindows()
  if (allWindows.length) {
    allWindows[0].focus()
  }
})

app.on('will-quit', () => {
  // Unregister a shortcut.
  globalShortcut.unregister('Alt+A')

  // Unregister all shortcuts.
  globalShortcut.unregisterAll()
})


ipcMain.on('set-ignore-mouse-events', (event, ignore, options) => {
  const win = BrowserWindow.fromWebContents(event.sender)
  win?.setIgnoreMouseEvents(ignore, options)
})

