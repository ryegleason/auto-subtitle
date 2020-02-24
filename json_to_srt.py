from pysrt import SubRipFile, SubRipItem


def json_to_srt(deepspeech_json, max_word_time=10, min_sub_time=1.5, max_sub_time=3):
    index = 0
    subtitle = ""
    start_time = 0
    end_time = 0
    subtitles = SubRipFile()

    for word in deepspeech_json["words"]:
        word["end_time"] = word["start_time"] + word["duration"]
        if word["duration"] < max_word_time:
            if start_time + max_sub_time >= word["end_time"] and subtitle:
                subtitle += " "
                subtitle += word["word"]
                end_time = max(word["end_time"], start_time + min_sub_time)
            elif subtitle:
                # Convert to milliseconds
                subtitles.append(
                    SubRipItem(index=++index, start=int(start_time*1000), end=int(end_time*1000), text=subtitle))
                subtitle = ""

            if not subtitle:
                start_time = word["start_time"]
                subtitle += word["word"]
                end_time = max(word["end_time"], start_time + min_sub_time)

    if subtitle:
        subtitles.append(SubRipItem(index=++index, start=int(start_time*1000), end=int(end_time*1000), text=subtitle))
    return subtitles
