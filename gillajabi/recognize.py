import soundfile
import time
import jamotools
from pororo import Pororo
from CER import CER


def recognize(audio_path, speech2text, idolvoice):
    g2p = Pororo(task="g2p", lang="ko")

    audio, rate = soundfile.read(audio_path)
    dur = len(audio) / rate
    print("audio : {:d} {:.2f}".format(len(audio), dur))

    start = time.time()
    ret = speech2text(audio)
    end = time.time()

    hyp_sents = []

    for idx_hyp in range(len(ret)):
        hyp_sent, _, _, hyp = ret[idx_hyp]
        hyp_sents.append(hyp_sent)
        # print(hyp)
        print("[{}] ({}), {:.4f}".format(idx_hyp + 1, hyp_sent, hyp.score.item()))

    elapsed_time = end - start
    print("time : {:.8f} (sec.)".format(elapsed_time))
    rtf = elapsed_time / dur
    print("RTF: {:.2f}".format(rtf))

    users = hyp_sents[0]
    ground_truth = jamotools.split_syllables(g2p(idolvoice))
    CER(ground_truth, users)


    return hyp_sents, elapsed_time, dur
