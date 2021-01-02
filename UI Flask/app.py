from flask import Flask, render_template
import win32api
import win32gui

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def MicMute():
    WM_APPCOMMAND = 0x319
    APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000

    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)
    
@app.route('/joinroom')
def joinroom():
    return render_template('room.html')

if __name__ == "__main__":
    app.run(debug=True)    
    