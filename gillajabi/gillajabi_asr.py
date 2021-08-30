import streamlit as st
from espnet2.bin.asr_inference import Speech2Text

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def init_model():
    #asr_config = "./exp/asr_train_asr_transformer5.aihub_raw_bpe/config_61.yaml"
    #asr_path = "./exp/asr_train_asr_transformer5.aihub_raw_bpe/valid.acc.best_61.pth"

    asr_config = "./exp/asr_train_asr_transformer5.aihub_raw_bpe/config_final.yaml"
    asr_path = "./exp/asr_train_asr_transformer5.aihub_raw_bpe/valid.acc.best_final.pth"

    speech2text = Speech2Text(
        asr_config,
        asr_path,
        None,
        None,
        ctc_weight=0.3,
        lm_weight=0.0,
        beam_size=3,
        nbest=5,  # 1,
        device="cpu", # "cuda",
    )

    return speech2text