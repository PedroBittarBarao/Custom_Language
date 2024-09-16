import pytest
import os
import subprocess

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
COMPILER_DIR = os.path.join(CURRENT_DIR, "..")
EXAMPLES_DIR = os.path.join(CURRENT_DIR, "..", "Arquivos_de_teste")
COMPILER_PATH = os.path.join(COMPILER_DIR, "main.py")
PYTHON_NAME = "python" if os.name == "nt" else "python3"

def run_program(file_path):
    out = subprocess.check_output([PYTHON_NAME, COMPILER_PATH, file_path])
    return out.decode("utf-8")

def test_ex1():
    # If windows change \n to \r\n
    sep = "\n"
    if os.name == "nt":
        sep = "\r\n"
    
    out = run_program(os.path.join(EXAMPLES_DIR, "teste1.bar"))
    out_list = out.split(sep)
    assert out_list[0] == "x=21"
    assert out_list[1] == "fish"

def test_ex2():
    with pytest.raises(subprocess.CalledProcessError):
        _ = subprocess.check_call([PYTHON_NAME, COMPILER_PATH, os.path.join(EXAMPLES_DIR, "teste2.bar")])


def test_ex3():
    with pytest.raises(subprocess.CalledProcessError):
        _ = subprocess.check_call([PYTHON_NAME, COMPILER_PATH, os.path.join(EXAMPLES_DIR, "teste3.bar")])
