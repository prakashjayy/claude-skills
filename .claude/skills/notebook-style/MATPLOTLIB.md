# Matplotlib Sub-skill

## Defaults

```python
import matplotlib.pyplot as plt
plt.style.use("bmh")  # in imports cell, once
```

## Template

```python
fig, ax = plt.subplots(figsize=(...))
ax.plot(x, y, label='...')
ax.set(xlabel='...', ylabel='...', title='...')
ax.legend()
plt.tight_layout()
plt.show()
```

Always `fig, ax = plt.subplots()`. Never bare `plt.plot()`.

## Sizing

Size to the data — interpretability over consistency, concise over impressive.
- Time series / spectra: wide and short
- Distributions: roughly square
- Image grids: match image aspect ratio
- Start small; go larger only if the data demands it

## Colors & Annotations

- Trust the bmh color cycle; only override hex when color has semantic meaning
- Skip legend on single-series plots
- `axvline`/`axhline` for reference lines; `annotate` only when the value is non-obvious

## Other Libraries

Stick to matplotlib. Switch only if **both**: matplotlib can't do it cleanly **and** the alternative meaningfully reduces code.
- Interactive (hover/zoom) → `plotly`
- Complex stat plots (pair grids, violin+swarm) → `seaborn`
- Maps → `cartopy` / `folium`
