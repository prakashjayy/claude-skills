# Dataset Subskill

Interactively selects a compute-appropriate dataset for the paper and downloads it via a spawned agent.

---

## Phase 1 — Extract dataset mentions from paper

Scan the paper analysis for:
- Named datasets in abstract, experiments, and implementation sections
- Dataset sizes if mentioned (e.g. "1.2M images", "50K training samples")
- Preprocessing or resolution details (e.g. "224×224", "normalized with ImageNet stats")
- Train / val / test split sizes

Record this as the **paper's dataset list** (may be multiple: one for pre-training, one for evaluation).

---

## Phase 2 — Collect compute context

If `--gpus`, `--vram`, and `--storage` were all passed as CLI flags, use those values and skip asking.

Otherwise, ask the user:

```
To suggest compute-appropriate datasets, I need to know your setup:

1. How many GPUs do you have? (e.g. 1, 2, 4)
2. How much VRAM per GPU? (e.g. 8GB, 16GB, 24GB, 80GB)
3. How much disk storage can you allocate? (e.g. 20GB, 100GB, 500GB)

You can also type "skip" to see all options without filtering.
```

Assign a **compute tier** from the answers:

| Tier | Condition |
|---|---|
| `tiny` | ≤ 8GB VRAM OR ≤ 20GB storage |
| `medium` | 9–24GB VRAM AND 21–150GB storage |
| `large` | > 24GB VRAM AND > 150GB storage (or multi-GPU) |

---

## Phase 3 — Build the options table

Construct a table with four sections, clearly separated:

### Section A: Paper's original dataset(s)
Show each dataset mentioned in the paper with a compute-tier badge.

### Section B: Compute-matched alternatives
Select from the dataset catalog below. Show only those matching the user's tier.

### Section C: Related datasets the paper didn't use
Show 2–3 domain-relevant datasets the user may not know about, regardless of tier.

### Section D: Custom / other
Always include an "Other — I'll specify a URL or HuggingFace dataset ID" row.

---

## Dataset catalog

Use this catalog to populate Section B and C. Always compute-tier-filter Section B.

### Tiny tier (≤ 8GB VRAM, ≤ 20GB storage)

| Dataset | Images | Storage | Source | Best for |
|---|---|---|---|---|
| CIFAR-10 | 60K (32×32) | 170MB | torchvision | baseline classification |
| CIFAR-100 | 60K (32×32) | 170MB | torchvision | fine-grained classification |
| Oxford Flowers 102 | 8K (variable) | 330MB | torchvision | few-shot / transfer |
| Oxford-IIIT Pets | 7K (variable) | 800MB | torchvision | transfer / fine-grained |
| STL-10 | 13K labeled + 100K unlabeled (96×96) | 2.5GB | torchvision | SSL pre-training at small scale |
| ImageNette | 13K (variable) | 1.5GB | direct URL | ImageNet proxy (10 easy classes) |
| Tiny ImageNet | 100K (64×64) | 236MB | direct URL | ImageNet proxy (200 classes) |
| FashionMNIST | 70K (28×28) | 30MB | torchvision | baseline / quick iteration |
| Food-101 (mini 10%) | ~10K | ~500MB | HF Hub | visual recognition transfer |

### Medium tier (9–24GB VRAM, 21–150GB storage)

| Dataset | Images | Storage | Source | Best for |
|---|---|---|---|---|
| ImageNette (full) | 13K (variable) | 1.5GB | direct URL | ImageNet proxy |
| CelebA | 200K (variable) | 1.3GB | torchvision | face attributes / generation |
| Food-101 | 101K | 5GB | HF Hub | fine-grained recognition |
| iNaturalist 2021 (mini) | 500K | ~40GB | HF Hub | long-tail recognition |
| COCO 2017 (images only) | 118K train + 5K val | 20GB | direct URL | detection / segmentation |
| ImageNet-1k (10% subset) | 120K | ~15GB | HF Hub | ImageNet proxy at medium scale |
| Places365-Standard | 1.8M | ~30GB | direct URL | scene recognition |

### Large tier (> 24GB VRAM, > 150GB storage)

| Dataset | Images | Storage | Source | Best for |
|---|---|---|---|---|
| ImageNet-1k (ILSVRC2012) | 1.2M train + 50K val | ~150GB | HF Hub (gated) | paper-exact replication |
| COCO 2017 (full) | 118K train + 5K val + annotations | 25GB | direct URL | detection / segmentation |
| ADE20K | 25K | 3.5GB | direct URL | semantic segmentation |
| CC3M | 3M image-text | ~120GB | HF Hub | vision-language |
| Google Landmarks v2 clean | 1.2M | ~120GB | Kaggle | retrieval / recognition |

---

## Phase 4 — Present options and ask

Format the table and present it. Example output:

```
Based on the paper (uses ImageNet-1k) and your setup (1× 16GB GPU, 50GB storage):

  COMPUTE TIER: medium

  ┌─ A: Paper's dataset ──────────────────────────────────────────────┐
  │  1. ImageNet-1k    1.2M images   ~150GB   HF Hub   ❌ exceeds storage
  └────────────────────────────────────────────────────────────────────┘

  ┌─ B: Compute-matched alternatives ─────────────────────────────────┐
  │  2. ImageNette     13K images    1.5GB    direct   ✅ tiny proxy
  │  3. Food-101       101K images   5GB      HF Hub   ✅ medium scale
  │  4. COCO 2017      118K images   20GB     direct   ✅ fits storage
  │  5. ImageNet-1k 10% subset
  │                    120K images   ~15GB    HF Hub   ✅ good proxy
  └────────────────────────────────────────────────────────────────────┘

  ┌─ C: Related datasets you might not know ──────────────────────────┐
  │  6. iNaturalist 2021 Mini — long-tail, 500K images, 40GB
  │  7. STL-10 — 100K unlabeled for SSL pre-training, 2.5GB
  └────────────────────────────────────────────────────────────────────┘

  ┌─ D: Custom ────────────────────────────────────────────────────────┐
  │  8. Other — enter a HuggingFace dataset ID or direct URL
  └────────────────────────────────────────────────────────────────────┘

Which dataset should I download? Enter a number (1–8) or type a name/ID:
```

Wait for user response before continuing.

---

## Phase 5 — Resolve the chosen dataset

Map the user's choice to a download descriptor:

```python
# descriptor format
{
  "name": "imagenette",
  "display": "ImageNette",
  "source": "direct",           # one of: torchvision | hf_hub | direct | kaggle
  "url_or_id": "https://s3.amazonaws.com/fast-ai-imageclas/imagenette2.tgz",
  "target_dir": "data/imagenette",
  "expected_size_gb": 1.5,
  "split_info": {"train": 9469, "val": 3925},
  "image_size": "variable (min ~160px)",
  "num_classes": 10
}
```

If user chose "Other", ask for the HuggingFace ID or URL and construct the descriptor.

---

## Phase 6 — Spawn download agent

Spawn an Agent with the following prompt (substitute values from the descriptor):

```
Download the <display> dataset for a ML training project.

Target directory: <target_dir> (relative to current working directory)
Source: <source>
URL or ID: <url_or_id>
Expected size: ~<expected_size_gb>GB

Instructions:
1. Check available disk space: `df -h .`
   If free space < expected_size_gb × 1.5, report and stop.
2. Create the target directory: `mkdir -p <target_dir>`
3. Download using the method below.
4. Verify the download (file count or size check).
5. Print a final summary: path, total images found, train/val split if discoverable.

## Download method by source type

### source = torchvision
```python
# uv run python -c "
import torchvision.datasets as D
import torchvision.transforms as T
t = T.ToTensor()
D.<ClassName>(root='<target_dir>', split='train', download=True, transform=t)
D.<ClassName>(root='<target_dir>', split='val',   download=True, transform=t)
print('Done')
# "
```

### source = hf_hub
```bash
uv run python -c "
from datasets import load_dataset
ds = load_dataset('<url_or_id>', cache_dir='<target_dir>')
print(ds)
"
```

### source = direct (URL ending in .tgz, .tar.gz, .zip)
```bash
curl -L "<url_or_id>" -o /tmp/dataset_download.tgz
mkdir -p <target_dir>
tar -xzf /tmp/dataset_download.tgz -C <target_dir> --strip-components=1
rm /tmp/dataset_download.tgz
```

### source = kaggle
```bash
# Requires KAGGLE_USERNAME and KAGGLE_KEY env vars to be set
uv run pip install kaggle -q
kaggle datasets download -d <url_or_id> -p <target_dir> --unzip
```

After downloading, count images:
```bash
find <target_dir> -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.JPEG" \) | wc -l
```

Report back: total file count, directory structure (2 levels deep with `ls -la`), and any errors.
```

**Wait for the agent to complete before continuing.** Do not proceed to the next workflow step until download is confirmed.

---

## Phase 7 — Verify and record

After the agent reports back:
1. Confirm image count is plausible (> 100 files found)
2. Detect the directory layout (ImageFolder-style, HF Arrow, flat, etc.)
3. Write a short dataset section to `configs/default.yaml`:

```yaml
dataset:
  name: imagenette
  root: data/imagenette
  num_classes: 10
  image_size: 224        # resize target for training
  mean: [0.485, 0.456, 0.406]   # ImageNet stats unless dataset-specific
  std:  [0.229, 0.224, 0.225]
  train_split: train
  val_split: val
```

Report: `✓ Dataset: data/<name>/ (<N> images downloaded)`

---

## Special cases

### ImageNet-1k (gated on HuggingFace)
HuggingFace requires account authentication for ImageNet-1k. Tell the user:
```
ImageNet-1k requires a HuggingFace account and access approval.
Run: huggingface-cli login
Then accept the terms at: https://huggingface.co/datasets/imagenet-1k
```
Then proceed with `load_dataset("imagenet-1k")`.

### Dataset already exists
If `<target_dir>` already exists and contains images:
```
data/<name>/ already exists with <N> images.
Use existing download? [y/n]
```
If yes, skip download and go straight to Phase 7.

### Download fails
If the agent reports an error:
1. Print the error clearly
2. Suggest the next-best alternative from the options table
3. Ask: "Should I try <alternative> instead?"
