TextLens

TextLens is an offline Android mobile application that performs real-time scene text translation. It uses the device camera to detect text in the environment, recognize the text, translate it into a selected target language, and render the translated text back onto the scene. The system is designed to work directly on-device without requiring continuous internet access.

Resources:
- TextLens Implementation: https://github.com/yewkiang123/TranslatorApp/tree/main
- APK Link: https://drive.google.com/file/d/1la37nps5yGOoBrKYuGCF-pRSXzhEINot/view?usp=sharing
  
Features:
- Real-time camera-based text detection and recognition
- On-device translation without constant internet connection
- Scene text replacement instead of simple text overlay
- Support for multiple languages, including Latin, Chinese, Japanese, and Korean
- Freeze-frame mode for easier viewing
- Image saving support for processed results

Tech Stack

- Kotlin for Android app development
- Android Studio as the development environment
- CameraX for live camera frame capture
- Google ML Kit OCR for on-device text recognition
- Google ML Kit Translation for on-device translation
- OpenCV for image processing, inpainting, and scene text replacement
- Kotlin Coroutines and Flow for asynchronous processing

How It Works

1. The app captures frames from the camera using CameraX.
2. OCR detects and recognizes text from stable frames.
3. The recognized text is translated using on-device translation models.
4. The original scene text is removed using image inpainting.
5. The translated text is rendered back into the image in the correct position.
6. A tracking mechanism helps keep translated text aligned across frames without running OCR on every frame.

Offline Capability

TextLens is designed to work offline once the required language models are downloaded. OCR runs fully on-device, and translation also works locally after model installation. This improves privacy, reduces latency, and allows the application to function in low-connectivity environments.

Project Goal

The goal of TextLens is to provide a practical mobile solution for multilingual scene text translation by combining computer vision, OCR, translation, tracking, and scene text editing into a single Android application.

---

Testing

The ocr_test/ folder contains automated Python test suites and supporting scripts that verify three core objectives of the TextLens system.

Test Image Set

The ocr_test/ folder contains 400 PNG test images (100 per language):

- ocr_test/ocr_test_images/english/   — 001.png to 100.png
- ocr_test/ocr_test_images/chinese/   — 001.png to 100.png
- ocr_test/ocr_test_images/korean/    — 001.png to 100.png
- ocr_test/ocr_test_images/japanese/  — 001.png to 100.png

Each image contains a single line of text rendered on a varied background (solid, gradient, noisy, lined paper, blueprint, etc.) using native system fonts. The images are designed to test OCR under realistic and challenging visual conditions.

Automated Test Suites

Three pytest test files cover the main system objectives:

  File                          Objective tested
  ----------------------------  -----------------------------------------------
  test_ocr_accuracy.py          Objective 1 — OCR detection and recognition
  test_overlay_rendering.py     Objective 3 — Overlay rendered in correct location
  test_responsiveness.py        Objective 4 — Real-time responsiveness

Prerequisites

  pip install pillow numpy pytest

The OCR live-detection tests (test_detection_rate, test_cer_per_language) additionally require:
- pytesseract Python package:   pip install pytesseract
- Tesseract binary: https://github.com/UB-Mannheim/tesseract/wiki
  After installing, make sure the tesseract executable is on your PATH.

All other tests run without Tesseract and will not be skipped.

Running the Tests

Run all three suites at once from the repository root:

  cd ocr_test
  pytest test_ocr_accuracy.py test_overlay_rendering.py test_responsiveness.py -v

Run a single suite:

  pytest test_ocr_accuracy.py -v
  pytest test_overlay_rendering.py -v
  pytest test_responsiveness.py -v

What Each Suite Tests

Objective 1 — test_ocr_accuracy.py
  Verifies that the OCR engine correctly detects and recognises scene text.
  - Checks that 100 test images exist for each language.
  - Measures detection rate: at least 90% of images must return non-empty OCR output.
  - Measures Character Error Rate (CER) per language:
      English ≤ 0.15, Chinese / Korean / Japanese ≤ 0.25.
  - Unit-tests the CER helper function independently of any OCR engine.
  - Verifies the integrity of the ground-truth text list.
  The detection rate and CER tests are skipped automatically when Tesseract is not
  installed; all other tests run without it.

Objective 3 — test_overlay_rendering.py
  Verifies that translated text is rendered in the correct location on the scene.
  - Overlay pixels must lie within the target bounding box (±2 px tolerance).
  - Inpainting must erase the original text region without touching surrounding pixels.
  - Rendered text must meet a minimum luminance contrast ratio of 3.0.
  - Two adjacent text regions must not bleed into each other.
  - Output image dimensions must be unchanged after processing.
  - Rotated text regions must still receive a rendered overlay.

Objective 4 — test_responsiveness.py
  Verifies that the image-processing pipeline meets real-time performance targets.
  - Full end-to-end pipeline (OCR + translation + rendering) must complete in < 1500 ms.
  - Rendering stage alone must complete in < 150 ms per frame.
  - Lightweight tracking path must sustain ≥ 24 fps over 60 consecutive frames.
  - Latency must remain stable across 10 repeated runs (coefficient of variation < 50%).
  - Processing 60 frames must not increase heap allocation by more than 20 MB.
  - Concurrent frame processing must not corrupt output (thread-safety smoke test).
  - CJK scripts must meet the same rendering latency target as Latin.

Manual Device Testing

To test the full app on an Android device:

Step 1 — Install the TextLens app
  Download and install the APK from the link above. On first launch, download the
  translation models for the languages you want to test.

Step 2 — Transfer the test images to your device
  Copy the ocr_test/ocr_test_images/ folder to your Android device via USB,
  Google Drive, or adb:

    adb push ocr_test/ocr_test_images /sdcard/Pictures/ocr_test_images

Step 3 — Open an image in TextLens
  In the TextLens app, open one of the test images, or display it on a monitor
  and point the device camera at it.

Step 4 — Observe OCR and translation output
  - The app will detect the text in the image.
  - It will then translate the detected text into your selected target language.
  - Compare the detected text with the original text to assess OCR accuracy.
  - Compare the translated output with an expected translation to assess quality.

What to Check

- Detection rate: Was any text detected at all?
- OCR accuracy: Does the recognised text match the original? Look for substituted characters, missing words, or garbled output.
- Translation accuracy: Is the translated text semantically correct?
- Language coverage: Test each language folder to see which languages perform best.
- Background robustness: Images with noise, dark backgrounds, or gradients are more challenging — check if accuracy drops on those variants.

Regenerating the Test Images

If you want to produce a fresh set of images (e.g., with different fonts or text content):

  pip install pillow
  cd ocr_test
  python generate_ocr_images.py

This will regenerate all 400 images under ocr_test/ocr_test_images/.
