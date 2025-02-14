from pycaw.pycaw import AudioUtilities
import keyboard

def get_currently_playing_sessions():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.State == 1:
            print(f"Process: {session.Process.name()}, Volume: {session.SimpleAudioVolume.GetMasterVolume()}")

def control_media():
    keyboard.add_hotkey('ctrl+alt+p', lambda: keyboard.send('play/pause'))
    keyboard.add_hotkey('ctrl+alt+n', lambda: keyboard.send('next track'))
    keyboard.add_hotkey('ctrl+alt+b', lambda: keyboard.send('previous track'))

    print("Press Ctrl+Alt+P to play/pause, Ctrl+Alt+N for next track, Ctrl+Alt+B for previous track.")
    keyboard.wait('esc')  # Wait until 'esc' is pressed to exit


