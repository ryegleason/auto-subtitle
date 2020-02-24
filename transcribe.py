import json
import subprocess
import sys

from json_to_srt import json_to_srt


def transcribe_to_srt(filename):
    process_out = subprocess.run(['deepspeech', '--model', 'deepspeech-0.6.1-models/output_graph.pbmm',
                                  '--lm', 'deepspeech-0.6.1-models/lm.binary', '--trie', 'deepspeech-0.6.1-models/trie',
                                  '--audio', filename, '--json'], capture_output=True)
    # print("Stderr:")
    # print(process_out.stderr.decode(sys.stderr.encoding))
    out = process_out.stdout.decode(sys.stdout.encoding)
    # print("out: " + out)
    out = out.replace("start_time ", "start_time")
    out = json.loads(out)
    subs = json_to_srt(out)
    srt_name = filename[:filename.rfind(".")] + ".en.srt"
    subs.save(srt_name, encoding="utf_8")
