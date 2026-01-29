<!-- Created: 2026-01-29 -->

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

손글씨 숫자 인식 프로그램 - 데스크톱 버전. Tkinter GUI로 숫자를 그리고 CNN 모델로 예측.

## Tech Stack

- GUI: Python Tkinter
- ML: TensorFlow/Keras (MNIST CNN 모델)

## Commands

```bash
# 가상환경 활성화
source ../.venv/bin/activate

# 의존성 설치 (최초 1회)
pip install -r requirements.txt

# 실행
python handwritten_digit_recognizer.py
```

## Architecture

단일 파일 구조 (`handwritten_digit_recognizer.py`):

- **ModelBundle**: 학습된 모델을 담는 dataclass
- **build_model()**: CNN 모델 구성 (Conv2D → BatchNorm → MaxPool → Dense)
- **load_or_train_model()**: `mnist_model.h5` 파일이 있으면 로드, 없으면 학습 후 저장
- **RoundedButton**: 둥근 모서리 버튼 커스텀 위젯 (tkinter Canvas 기반)
- **DigitCanvas**: 메인 애플리케이션 클래스 - 28x28 그리드에 그림을 그리고 예측 수행

## Code Conventions

- 모든 새 파일 생성 시 파일 상단에 날짜와 시간을 주석으로 표시
  - Python: `# Created: YYYY-MM-DD HH:MM`
