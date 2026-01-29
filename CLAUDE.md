# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CNN 기반 손글씨 숫자 인식 애플리케이션 (MNIST 데이터셋 사용). 데스크톱(Tkinter)과 웹(Flask) 버전이 분리되어 있다.

## Commands

```bash
# 환경 설정 (최초 1회)
./setup_venv.sh desktop

# 데스크톱 실행
source .venv/bin/activate
python desktop_version/handwritten_digit_recognizer.py

# 웹 실행
# ./setup_venv.sh web
# source .venv/bin/activate
# python web_version/app.py
```

## Architecture

데스크톱 버전 (`desktop_version/handwritten_digit_recognizer.py`):

- **ModelBundle**: 학습된 모델을 담는 dataclass
- **build_model()**: CNN 모델 구성 (Conv2D → BatchNorm → MaxPool → Dense)
- **load_or_train_model()**: `mnist_model.h5` 파일이 있으면 로드, 없으면 학습 후 저장
- **RoundedButton**: 둥근 모서리 버튼 커스텀 위젯 (tkinter Canvas 기반)
- **DigitCanvas**: 메인 애플리케이션 클래스 - 28x28 그리드에 그림을 그리고 예측 수행

## Code Conventions

- 모든 새 파일 생성 시 파일 상단에 날짜와 시간을 주석으로 표시
  - Python: `# Created: YYYY-MM-DD HH:MM`
  - JavaScript/TypeScript: `// Created: YYYY-MM-DD HH:MM`
  - HTML/Markdown: `<!-- Created: YYYY-MM-DD HH:MM -->`

## Key Details

- 캔버스 크기: 392x392 픽셀 (28x28 그리드, 셀당 14픽셀)
- 브러시: 3x3 크기로 그려짐
- 모델: 10 epochs 학습, Adam optimizer, sparse categorical crossentropy
- 저장 경로: `desktop_version/mnist_model.h5`
