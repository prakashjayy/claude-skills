# Notebook Style — Annotated Examples

## Cell 1: Intro Markdown

```markdown
## Fourier Transform: From Waves to Frequencies

The Fourier Transform lets us decompose any signal into its constituent sine waves.  
Think of it as a prism for sound — splitting white noise into individual tones.  
We'll build intuition from a single sine wave, work up to composite signals, and end with images.
```

Rule: 3–5 sentences. No equations yet. Set the stage.

---

## Cell 2: Imports

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

plt.style.use("bmh")
```

Rule: imports only. No logic, no comments beyond style config.

---

## Cell 3: Simplest Example

```python
t = np.linspace(0, 1, 1000)
signal = np.sin(2 * np.pi * 5 * t)  # 5 Hz sine wave

plt.plot(t, signal)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Single Sine Wave: 5 Hz')
plt.show()
```

Rule: one concept, minimal code. No functions yet.

---

## Cell 4: Transition Markdown

```markdown
### Why the Frequency Domain?

Time-domain plots show *when* things happen — hard to see *what* frequencies are present.  
The frequency domain tells us *which* sine waves are hiding in the signal.  
Fourier's key insight: any periodic signal is a sum of sines and cosines.
```

---

## Cell 5: Raw Computation (no function yet)

```python
N = len(signal)
yf = fft(signal)
xf = fftfreq(N, 1/1000)

# Only positive frequencies
pos_mask = xf >= 0
plt.plot(xf[pos_mask], 2/N * np.abs(yf[pos_mask]))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.title('Frequency Spectrum')
plt.show()
```

---

## Consolidation Cell (Phase 3)

After building up 5–8 raw cells exploring pieces, collect into a function:

```python
def plot_spectrum(signal, fs=1000, title='Frequency Spectrum'):
    N = len(signal)
    yf = fft(signal)
    xf = fftfreq(N, 1/fs)
    pos = xf >= 0
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax1.plot(np.linspace(0, N/fs, N), signal)
    ax1.set(xlabel='Time (s)', ylabel='Amplitude', title='Time Domain')
    ax2.plot(xf[pos], 2/N * np.abs(yf[pos]))
    ax2.set(xlabel='Frequency (Hz)', ylabel='Amplitude', title=title)
    plt.tight_layout()
    plt.show()
    
    return xf[pos], 2/N * np.abs(yf[pos])
```

Rule: function appears after raw exploration. It wraps what we already proved works.

---

## Demo Cell (Phase 3, after function)

```python
# Composite signal: 3 Hz + 7 Hz + 15 Hz
t = np.linspace(0, 1, 1000)
composite = (
    np.sin(2 * np.pi * 3 * t) +
    0.5 * np.sin(2 * np.pi * 7 * t) +
    0.3 * np.sin(2 * np.pi * 15 * t)
)

freqs, amps = plot_spectrum(composite, title='Composite Signal Spectrum')
```

Rule: the function demo is richer than the raw examples. Shows the payoff.
