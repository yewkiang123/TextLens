"""
Objective 1 — OCR detection and recognition accuracy.

Tests that the OCR engine correctly detects and recognizes scene text
from the generated test images by measuring:
  - Detection rate  : whether any text was detected at all (recall proxy)
  - Character Error Rate (CER) : recognised text vs. ground truth
  - Per-language accuracy breakdown

Dependencies:
    pip install pillow pytesseract
    (Tesseract binary: https://github.com/UB-Mannheim/tesseract/wiki)

Run:
    cd ocr_test
    pytest test_ocr_accuracy.py -v
"""

import os
import sys
import math
import pytest

sys.path.insert(0, os.path.dirname(__file__))
from generate_ocr_images import TEXTS

# ---------------------------------------------------------------------------
# Tesseract availability check
# ---------------------------------------------------------------------------
try:
    import pytesseract
    from PIL import Image

    pytesseract.get_tesseract_version()
    TESSERACT_AVAILABLE = True
except Exception:
    TESSERACT_AVAILABLE = False

pytesseract_skip = pytest.mark.skipif(
    not TESSERACT_AVAILABLE,
    reason="pytesseract / Tesseract binary not installed",
)

# ---------------------------------------------------------------------------
# OCR language codes (Tesseract)
# ---------------------------------------------------------------------------
LANG_MAP = {
    "english": "eng",
    "chinese": "chi_sim",
    "korean":  "kor",
    "japanese": "jpn",
}

IMAGE_DIR = os.path.join(os.path.dirname(__file__), "ocr_test_images")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def levenshtein(s1: str, s2: str) -> int:
    """Compute Levenshtein edit distance between two strings."""
    m, n = len(s1), len(s2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, n + 1):
            temp = dp[j]
            dp[j] = prev if s1[i - 1] == s2[j - 1] else 1 + min(prev, dp[j], dp[j - 1])
            prev = temp
    return dp[n]


def cer(hypothesis: str, reference: str) -> float:
    """Character Error Rate: edit_distance / len(reference)."""
    ref = reference.strip()
    hyp = hypothesis.strip()
    if not ref:
        return 0.0 if not hyp else 1.0
    return levenshtein(hyp, ref) / len(ref)


def run_ocr(image_path: str, lang_code: str) -> str:
    """Run Tesseract OCR and return the recognised string."""
    img = Image.open(image_path)
    config = f"--oem 3 --psm 7 -l {lang_code}"
    return pytesseract.image_to_string(img, config=config)


def image_path(lang: str, index: int) -> str:
    return os.path.join(IMAGE_DIR, lang, f"{index:03d}.png")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def image_dir_exists():
    assert os.path.isdir(IMAGE_DIR), (
        f"Test image directory not found: {IMAGE_DIR}\n"
        "Run  python generate_ocr_images.py  first."
    )


# ---------------------------------------------------------------------------
# Test 1-A  Detection rate — were images generated for each language?
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("lang", list(LANG_MAP.keys()))
def test_images_exist_for_language(lang, image_dir_exists):
    """Each language folder must contain exactly 100 test images."""
    lang_dir = os.path.join(IMAGE_DIR, lang)
    assert os.path.isdir(lang_dir), f"Missing language folder: {lang_dir}"
    pngs = [f for f in os.listdir(lang_dir) if f.endswith(".png")]
    assert len(pngs) == 100, (
        f"Expected 100 images for '{lang}', found {len(pngs)}"
    )


# ---------------------------------------------------------------------------
# Test 1-B  OCR detects non-empty text in every image
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("lang", list(LANG_MAP.keys()))
@pytesseract_skip
def test_detection_rate(lang, image_dir_exists):
    """
    OCR must return non-empty output for at least 90 % of images.
    A blank result means the text region was not detected at all.
    """
    lang_code = LANG_MAP[lang]
    total = min(20, len(TEXTS[lang]))   # sample first 20 images per language
    detected = 0

    for i in range(1, total + 1):
        path = image_path(lang, i)
        if not os.path.exists(path):
            continue
        result = run_ocr(path, lang_code).strip()
        if result:
            detected += 1

    detection_rate = detected / total
    assert detection_rate >= 0.90, (
        f"[{lang}] detection rate {detection_rate:.0%} < 90 % threshold"
    )


# ---------------------------------------------------------------------------
# Test 1-C  CER per language (sample of 10 images each)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("lang,cer_threshold", [
    ("english", 0.15),
    ("chinese", 0.25),
    ("korean",  0.25),
    ("japanese", 0.25),
])
@pytesseract_skip
def test_cer_per_language(lang, cer_threshold, image_dir_exists):
    """
    Average CER for each language must be below the per-language threshold.
    English has the tightest threshold; CJK scripts are allowed more error
    because Tesseract models vary in quality across languages.
    """
    lang_code = LANG_MAP[lang]
    ground_truths = TEXTS[lang]
    sample = min(10, len(ground_truths))
    total_cer = 0.0

    for i in range(sample):
        path = image_path(lang, i + 1)
        if not os.path.exists(path):
            continue
        reference = ground_truths[i].strip()
        hypothesis = run_ocr(path, lang_code).strip()
        total_cer += cer(hypothesis, reference)

    avg_cer = total_cer / sample
    assert avg_cer <= cer_threshold, (
        f"[{lang}] avg CER {avg_cer:.3f} exceeds threshold {cer_threshold}"
    )


# ---------------------------------------------------------------------------
# Test 1-D  CER helper unit tests (no external dependency needed)
# ---------------------------------------------------------------------------

def test_cer_identical_strings():
    assert cer("hello", "hello") == 0.0


def test_cer_completely_wrong():
    """CER of a completely different string equals 1 or more."""
    result = cer("xxxx", "hello")
    assert result >= 1.0


def test_cer_empty_reference_nonempty_hypothesis():
    assert cer("something", "") == 1.0


def test_cer_empty_both():
    assert cer("", "") == 0.0


def test_cer_single_substitution():
    result = cer("hXllo", "hello")
    assert math.isclose(result, 1 / 5, rel_tol=1e-9)


def test_cer_insertion():
    result = cer("hellXo", "hello")
    assert math.isclose(result, 1 / 5, rel_tol=1e-9)


def test_cer_deletion():
    result = cer("hell", "hello")
    assert math.isclose(result, 1 / 5, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# Test 1-E  Ground-truth texts sanity check
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("lang", list(LANG_MAP.keys()))
def test_ground_truth_count(lang):
    """
    Each language must have at least 50 ground-truth strings.
    The image generator cycles through the list to fill 100 images, so
    the list does not need to be exactly 100 entries long.
    """
    count = len(TEXTS[lang])
    assert count >= 50, (
        f"[{lang}] expected at least 50 texts, got {count}"
    )


@pytest.mark.parametrize("lang", list(LANG_MAP.keys()))
def test_ground_truth_non_empty(lang):
    """No ground-truth string should be empty."""
    for i, text in enumerate(TEXTS[lang]):
        assert text.strip(), f"[{lang}] text at index {i} is empty"
