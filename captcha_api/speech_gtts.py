import os
import time
from io import BytesIO
from tempfile import mkstemp

from sqlalchemy import true

from gtts import gTTS


def text_to_speech(text, lang):
    """Converts a piece of text to an mp3 document."""

    _, filename = mkstemp(suffix="-captcha.mp3")

    tts = gTTS(text, lang=lang, tld='fr', slow=True)
    tts.save(filename)

    # Required because of a weird FS error
    time.sleep(0.3)

    with open(filename, "rb") as fh:
        buf = BytesIO(fh.read())
    buf.seek(0)
    # Cleanup
    if os.path.exists(filename):
        os.remove(filename)
    return buf
