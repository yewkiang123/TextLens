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
