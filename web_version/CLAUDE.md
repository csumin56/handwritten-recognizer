<!-- Created: 2026-01-29 -->
<!-- Updated: 2026-01-29 18:30 -->

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

손글씨 숫자 인식 프로그램 - 웹 버전. 브라우저에서 캔버스에 숫자를 그리고 CNN 모델로 예측.

## Tech Stack

- Frontend: HTML, CSS, JavaScript (Canvas API)
- Backend: Python Flask
- ML: TensorFlow/Keras (MNIST CNN 모델)
- Image Processing: Pillow

## Commands

```bash
# 가상환경 활성화
source ../.venv/bin/activate

# 의존성 설치 (최초 1회)
pip install -r requirements.txt

# 서버 실행
python app.py

# 브라우저에서 접속
# http://127.0.0.1:5000
```

## Architecture

```
web_version/
├── app.py              # Flask 서버 + 모델 로드/학습
├── mnist_model.h5      # 학습된 모델 (자동 생성)
├── templates/
│   └── index.html      # 메인 페이지
└── static/
    ├── style.css       # 스타일시트
    └── script.js       # 캔버스 드로잉 + API 호출
```

### 주요 컴포넌트

- **app.py**: Flask 서버. `/` 라우트로 메인 페이지, `/predict` POST 라우트로 이미지 예측
- **index.html**: 392x392 캔버스, Predict/Clear 버튼
- **script.js**: Canvas API로 28x28 그리드 드로잉 (3x3 브러시), base64 이미지를 서버로 전송
- **style.css**: 다크 테마 UI (데스크톱 버전과 동일한 컬러 팔레트)

### 모델 로딩 우선순위

1. `web_version/mnist_model.h5` (로컬)
2. `desktop_version/mnist_model.h5` (공유 모델)
3. 없으면 새로 학습 후 저장

## Code Conventions

- 모든 새 파일 생성 시 파일 상단에 날짜와 시간을 주석으로 표시
  - Python: `# Created: YYYY-MM-DD HH:MM`
  - JavaScript: `// Created: YYYY-MM-DD HH:MM`
  - HTML: `<!-- Created: YYYY-MM-DD HH:MM -->`
