TextLens

TextLens is an offline Android mobile application that performs real-time scene text translation. It uses the device camera to detect text in the environment, recognize the text, translate it into a selected target language, and render the translated text back onto the scene. The system is designed to work directly on-device without requiring continuous internet access.

Resources:
- TextLens Implementation: https://github.com/yewkiang123/TranslatorApp/tree/main
- APK Link: https://drive.google.com/file/d/1w9sgwMR6rbkqU5-o-dmRmoTLvTK4JfTb/view?usp=drive_link

Features

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

OCR Accuracy Testing

This repository includes a set of pre-generated test images and a Python script to evaluate how accurately TextLens detects and translates text across multiple languages.

Test Image Set

The ocr_test/ folder contains 400 PNG test images (100 per language):

- ocr_test/ocr_test_images/english/   — 001.png to 100.png
- ocr_test/ocr_test_images/chinese/   — 001.png to 100.png
- ocr_test/ocr_test_images/korean/    — 001.png to 100.png
- ocr_test/ocr_test_images/japanese/  — 001.png to 100.png

Each image contains a single line of text rendered on a varied background (solid, gradient, noisy, lined paper, blueprint, etc.) using native system fonts. The images are designed to test OCR under realistic and challenging visual conditions.

How to Run the Test

Prerequisites:
- TextLens app installed on an Android device or emulator (see APK link above)
- Language models downloaded inside the app (English, Chinese, Korean, Japanese)

Step 1 — Install the TextLens app
  Download and install the APK from the link above. On first launch, download the translation models for the languages you want to test.

Step 2 — Transfer the test images to your device
  Copy the ocr_test/ocr_test_images/ folder to your Android device (via USB, Google Drive, or adb push).

  Example using adb:
    adb push ocr_test/ocr_test_images /sdcard/Pictures/ocr_test_images

Step 3 — Open an image in TextLens
  In the TextLens app, use the image import or gallery mode (if available) to open one of the test images, or display the image on a monitor/screen and point the device camera at it.

Step 4 — Observe OCR and translation output
  - The app will detect the text in the image.
  - It will then translate the detected text into your selected target language.
  - Compare the detected text with the original text shown in the image to assess OCR accuracy.
  - Compare the translated output with an expected translation to assess translation quality.

What to Check

- Detection rate: Was any text detected at all?
- OCR accuracy: Does the recognized text match the original? Look for substituted characters, missing words, or garbled output.
- Translation accuracy: Is the translated text semantically correct?
- Language coverage: Test each language folder (English, Chinese, Korean, Japanese) to see which languages perform best.
- Background robustness: Images with noise, dark backgrounds, or gradients are more challenging — check if accuracy drops on those variants.

Regenerating the Test Images

If you want to produce a fresh set of images (e.g., with different fonts or text content), run the generator script:

  pip install pillow
  cd ocr_test
  python generate_ocr_images.py

This will regenerate all 400 images under ocr_test/ocr_test_images/.
