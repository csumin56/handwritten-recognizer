<!-- Created: 2026-01-29 18:52 -->

# Handwritten Digit Recognizer (MNIST)

MNIST 데이터셋으로 학습한 CNN 모델을 사용해 손글씨 숫자를 예측하는 프로젝트입니다.
데스크톱(Tkinter) 버전과 웹(Flask) 버전이 각각 제공됩니다.

## 구성

```
.
├── desktop_version/                 # 데스크톱 앱 (Tkinter)
│   ├── handwritten_digit_recognizer.py
│   ├── mnist_model.h5               # 학습된 모델 (자동 생성)
│   ├── requirements.txt
│   └── CLAUDE.md
├── web_version/                     # 웹 앱 (Flask)
│   ├── app.py
│   ├── mnist_model.h5               # 학습된 모델 (자동 생성)
│   ├── requirements.txt
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── style.css
│       └── script.js
├── setup_venv.sh                    # 가상환경/의존성 설치 스크립트
└── CLAUDE.md                        # 저장소 가이드
```

## 빠른 시작

### 공통 (최초 1회)

```bash
# 데스크톱 또는 웹 중 하나 선택
./setup_venv.sh desktop
# 또는
./setup_venv.sh web
```

### 데스크톱 버전 실행

```bash
source .venv/bin/activate
python desktop_version/handwritten_digit_recognizer.py
```

### 웹 버전 실행

```bash
source .venv/bin/activate
python web_version/app.py
```

브라우저에서 `http://127.0.0.1:5000` 접속

## 동작 방식

- **모델 학습/로드**: `mnist_model.h5`가 없으면 MNIST를 다운로드해 학습 후 저장합니다.
- **데스크톱 UI**: 28x28 그리드 기반 캔버스(392x392)에서 3x3 브러시로 그림을 입력합니다.
- **웹 UI**: Canvas API로 그림을 그린 뒤 `/predict`로 전송해 예측합니다.
- **웹 모델 우선순위**: `web_version/mnist_model.h5` → `desktop_version/mnist_model.h5` → 새로 학습

## 의존성

- 데스크톱: `numpy`, `tensorflow`
- 웹: `flask`, `numpy`, `pillow`, `tensorflow`

## 참고

- 모델 학습은 첫 실행 시 시간이 걸릴 수 있습니다.
- 가이드 문서는 각 디렉터리의 `CLAUDE.md`에 상세히 정리되어 있습니다.
