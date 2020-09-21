import os
import time
from io import BytesIO
from tempfile import mkstemp

import pyttsx3


def text_to_speech(text):
    """Converts a piece of text to an mp3 document."""

    engine = pyttsx3.init()
    engine.setProperty("rate", 60)
    _, filename = mkstemp(suffix="-captcha.mp3")
    engine.save_to_file(text, filename)
    engine.runAndWait()
    engine.stop()
    # Required because of a weird FS error
    time.sleep(0.3)

    with open(filename, "rb") as fh:
        buf = BytesIO(fh.read())
    buf.seek(0)
    # Cleanup
    if os.path.exists(filename):
        os.remove(filename)
    return buf
