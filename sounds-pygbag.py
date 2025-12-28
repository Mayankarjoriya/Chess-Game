import pygame
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize pygame mixer
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Load actual sound files
sound_dir = "Sound"

# Use chess.com move sound
chess_com_move = resource_path(os.path.join(sound_dir, "chess_com_move.ogg"))

try:
    if os.path.exists(chess_com_move):
        # Use chess.com professional move sound
        MOVE_SOUND = pygame.mixer.Sound(chess_com_move)
        MOVE_SOUND.set_volume(0.5)
        print("✓ Using chess.com move sound")
    else:
        # Fallback to trimmed sound
        trimmed_move = resource_path(os.path.join(sound_dir, "trimmed", "move_click.ogg"))
        if os.path.exists(trimmed_move):
            MOVE_SOUND = pygame.mixer.Sound(trimmed_move)
            MOVE_SOUND.set_volume(0.5)
            print("✓ Using trimmed chess pieces sound")
        else:
            MOVE_SOUND = pygame.mixer.Sound(buffer=b'\x00' * 1000)
except:
    print("Warning: Could not load move sound, using fallback")
    MOVE_SOUND = pygame.mixer.Sound(buffer=b'\x00' * 1000)

try:
    # Load capture sound (ripping paper)
    CAPTURE_SOUND = pygame.mixer.Sound(resource_path(os.path.join(sound_dir, "Capture", "ripping-a-piece-of-paper-103913.ogg")))
    CAPTURE_SOUND.set_volume(0.35)
except:
    print("Warning: Could not load capture sound, using fallback")
    CAPTURE_SOUND = pygame.mixer.Sound(buffer=b'\x00' * 1000)

try:
    # Load check sound (checkmate)
    CHECK_SOUND = pygame.mixer.Sound(resource_path(os.path.join(sound_dir, "checkmate", "ficha-de-ajedrez-34722.ogg")))
    CHECK_SOUND.set_volume(0.4)
except:
    print("Warning: Could not load check sound, using fallback")
    CHECK_SOUND = pygame.mixer.Sound(buffer=b'\x00' * 1000)

try:
    # Load checkmate/victory sound
    CHECKMATE_SOUND = pygame.mixer.Sound(resource_path(os.path.join(sound_dir, "Winning Moment", "11l-victory_beat-1749704511321-358765(1).ogg")))
    CHECKMATE_SOUND.set_volume(0.5)
except:
    print("Warning: Could not load checkmate sound, using fallback")
    CHECKMATE_SOUND = pygame.mixer.Sound(buffer=b'\x00' * 1000)

print("✅ Sound files loaded successfully!")
print(f"  - Move: chess.com move sound (volume 0.5)")
print(f"  - Capture: ripping-paper (volume 0.35)")
print(f"  - Check: ficha-de-ajedrez (volume 0.4)")
print(f"  - Checkmate: victory_beat (volume 0.5)")



