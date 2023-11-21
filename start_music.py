from pydub import AudioSegment
from pydub.playback import play
import io


def start_music(file_data):
    song = AudioSegment.from_file(io.BytesIO(file_data), format="wav")
    play(song)
