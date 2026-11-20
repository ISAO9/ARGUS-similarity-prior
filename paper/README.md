# Paper materials

Code, frozen inputs and outputs for

> Kurosawa, I. How Much Do Waveform-Similar Past Earthquakes Improve Early Epicenters?
> Preregistered One-Shot Tests on Japanese Aftershock Sequences (submitted to Seismological Research Letters).

The rest of this repository is a copy of the registration repository (see the README at the top): the records,
the frozen test scripts, the run instructions, and the results, each committed before its test events were opened. Their commit times and the
Zenodo versions (10.5281/zenodo.23905464, 10.5281/zenodo.24190129, 10.5281/zenodo.24239732,
10.5281/zenodo.24247608, 10.5281/zenodo.24317791) time-stamp them. This folder adds what was
made after the tests: the scripts that drew every figure and table of the paper and the
descriptive checks of its supplement.

## Layout

| Path | Content |
|---|---|
| `src/26_01`–`26_06` | Figures 1–9 and Tables S1 (map and waveform, results, schematic and timeline, effect sizes, set-size control, Table S1) |
| `src/26_08`–`26_12` | Descriptive checks of the supplement (inventory, test-period terciles, memory truncation, DPRI catalog and intensity summary with Figure S1, mean removal) |
| `src/26_13` | Builds this folder, scans it, and reruns the scripts below to confirm the numbers |
| `src/26_15` | Figure S2 and Table S9 (full error distributions, descriptive) |
| `src/21_10`, `src/23_01`–`23_03` | Earlier checks used in Text S4 (intensity effect, spatial holdout, DPRI catalog) |
| `data/inputs/models`, `data/inputs/data` | Frozen results of the registered tests: judgment and opening records (JSON), per-event errors (CSV), the frozen learned models |
| `data/`, `models/`, `PDF/` | Outputs of the 26_xx scripts and the figure files |
| `data/paper_gitlog.txt` | Commit times of the registration repository read by Figure 3 |
| `MANIFEST.json`, `SHA256SUMS.txt` | Source, role and SHA-256 of every file here |

## Rerun without waveforms

```
cd paper
uv sync
uv run python src/26_04_paper_effect_sizes.py
uv run python src/26_06_paper_table_s1.py
uv run python src/26_02_paper_result_figures.py
uv run python src/26_03_paper_schematic_timeline.py
```
26_09 and 26_11 read a folder with `models/` and `data/` (as in the author's working folder):
copy `data/inputs/models`, `data/inputs/data` and the `data/26_10_*.json` files into one folder
and pass it with `--root` (26_09) or `--base` (26_11). `src/26_13_release_assemble.py` does this
and compares the outputs with the numbers of the paper.

## Scripts that need waveforms

26_01, 26_05, 26_10, 26_12 and the registered test scripts read caches of picks and waveform
segments built from Hi-net continuous records. Hi-net waveforms cannot be redistributed under the
NIED terms of use, and the West Tottori 2026 records were provided by S. Katoh (University of
Tokyo) and are not public. The caches are therefore not included. They can be rebuilt with a
Hi-net account by following the registration folders (download notebooks and cache scripts);
each judgment JSON gives the SHA-256 of the cache it used, so a rebuilt cache can be checked.

## Data sources

JMA unified hypocenter catalog; Hi-net continuous waveforms (NIED), obtained with HinetPy;
PhaseNet in SeisBench; the DPRI aftershock catalog of the 2016 Central Tottori earthquake
(Iio et al., 2018), https://www.eqhz.dpri.kyoto-u.ac.jp/images/2019/01/ct3_201711.txt
(not redistributed here; the comparison results are in `data/inputs/data/23_02_per_event.csv`
and `23_03_per_event.csv`).

## License

MIT License (see LICENSE at the repository root).
