import os
import sys

import youtube_dl
import transcribe

GEN_SUBS_ALWAYS = True
main_opts = {'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }], "outtmpl": "%(id)s.%(ext)s", "keepvideo": True, "writesubtitles": True}


def dl_and_transcribe(urls):
    with youtube_dl.YoutubeDL(main_opts) as ydl:
        for url in urls:
            meta = ydl.extract_info(url, download=False)
            out_filename = meta["id"] + ".wav"
            ydl.download([url])
            transcribe.transcribe_to_srt(out_filename)
            os.remove(out_filename)


if __name__ == "__main__":
    print(sys.argv[1:])
    dl_and_transcribe(sys.argv[1:])
