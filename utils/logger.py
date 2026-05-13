import logging
import os
import streamlit as st

def setup_debug_logger():
    log_path = os.path.join(os.path.dirname(__file__), "../debug.log")
    logger = logging.getLogger("ussr_sim")
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_path, encoding="utf-8")
        ch = logging.StreamHandler()
        fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
        fh.setFormatter(fmt); ch.setFormatter(fmt)
        logger.addHandler(fh); logger.addHandler(ch)
    return logger