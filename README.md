# [pptx_Agent]원고를 넣으면 PowerPoint에서 편집되는 PPTX를 만드는 AI 에이전트

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Font](https://img.shields.io/badge/font-Pretendard-0b1f3a)](.claude/skills/ppt-master/assets/fonts/Pretendard/)

Claude Code·Codex 같은 AI 코딩 에이전트 안에서 동작하는 **PPT 제작 스킬 패키지**입니다.
자료(PDF·DOCX·Markdown·주제 한 줄)를 주면 AI가 기획 → 디자인 확인 → 슬라이드 작성 → 품질 검사 → `.pptx` 내보내기까지 진행합니다.
결과물은 그림 한 장짜리 슬라이드가 아니라 **도형·텍스트를 하나하나 고칠 수 있는 네이티브 PowerPoint 파일**입니다.

> 이 저장소는 [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)(MIT) → [byungjunjang/slide-master](https://github.com/byungjunjang/slide-master)를 기반으로 한 학교 업무용 커스터마이즈 버전입니다.

> 원 프로젝트의 상세 설명은 [`README.slide-master.md`](README.slide-master.md)에 그대로 보존했습니다.

### 이 버전에서 바뀐 점

| 항목 | 내용 |
|---|---|
| AI 이미지 기본 모델 | Gemini **Nano Banana 2.1** (`gemini-nano-banana-2.1`) |
| 이미지 수정 요청 처리 | 불만족·변경 요청 시 **Gemini 3.8 Flash**가 피드백을 반영해 프롬프트를 다시 쓰고, Nano Banana 2.1이 다시 그림 ([`image_revise.py`](.claude/skills/ppt-master/scripts/image_revise.py)) |
| Codex 이미지 백엔드 | `CODEX_IMAGE_MODEL` 환경변수로 실행 모델 지정 가능 |
| 브랜드 색 | 양파고 주컬러 프리셋(`yangphago`) 추가 |
| 덱 템플릿 | `supabase` 덱 템플릿 추가 |
| API 키 설정 | `.env.example` 견본 파일 제공 — 복사해서 키만 넣으면 됨 |

---

## 1. 설치법

### 1-1. 준비물

| 준비물 | 비고 |
|---|---|
| Python 3.10 이상 | Windows는 설치 시 **"Add python.exe to PATH" 체크** ([Windows 설치 가이드](docs/windows-installation.md)) |
| AI 에이전트 | [Claude Code](https://claude.ai/code) 권장. Codex CLI / ChatGPT 데스크탑 앱의 Codex도 동작 |
| Git | 저장소 내려받기용 |
| (선택) Node.js | OfficeCLI 검증 도구, Codex CLI 설치용 |

### 1-2. 내려받기와 의존성 설치

```bash
git clone https://github.com/roughkyo/pptx_Agent.git
cd pptx_Agent
pip install -r requirements.txt
python -m playwright install chromium
```

`playwright`는 슬라이드 미리보기 렌더링·시각 검사에 쓰입니다. 없으면 정적 검사만 동작합니다.

### 1-3. 글꼴 (Pretendard)

모든 덱은 **Pretendard** 한 가족으로 만듭니다. 글꼴 파일은 [`.claude/skills/ppt-master/assets/fonts/Pretendard/`](.claude/skills/ppt-master/assets/fonts/Pretendard/)에 들어 있습니다.
이 폴더의 글꼴 파일을 모두 선택해 **설치**하세요. PPTX는 글꼴을 내장하지 않으므로, 완성본을 여는 다른 PC에도 Pretendard가 있어야 모양이 그대로 나옵니다.

### 1-4. AI 이미지 생성 설정 (선택)

표지·마무리 그림 같은 AI 이미지를 쓰려면 API 키를 넣습니다.

```bash
cp .env.example .env
```

(Windows PowerShell: `Copy-Item .env.example .env`)

`.env`를 열어 `GEMINI_API_KEY=` 뒤에 [Google AI Studio](https://aistudio.google.com/apikey)에서 발급한 키를 **직접** 붙여 넣고 저장합니다.
`.env`는 내 PC에만 남는 파일입니다. API 키 없이 Codex CLI 로그인 방식으로 이미지를 만드는 방법은 [`README.slide-master.md`](README.slide-master.md)를 참고하세요.

### 1-5. 설치 확인

```bash
python .claude/skills/ppt-master/scripts/preflight.py
```

오류 없이 끝나면 준비 완료입니다.

### 1-6. (선택) 내보낸 PPTX 검증 도구

```bash
npm install -g @officecli/officecli@1.0.135
```

---

## 2. 사용법

### 2-1. 시작

1. AI 에이전트에서 이 폴더(`pptx_Agent`)를 엽니다. Claude Code라면 폴더에서 `claude` 실행, 데스크탑 앱이라면 폴더 선택.
2. 원고 파일을 `projects/` 아래에 두거나, 채팅에 바로 붙여 넣습니다.
3. 자연어로 요청합니다.

```text
projects/회의자료/원고.md 로 표지 포함 11장 회의용 PPT 만들어줘. 문구는 개조식으로.
```

### 2-2. 진행 순서 (AI가 자동으로 진행)

| 단계 | 내가 할 일 |
|---|---|
| ① 원고 정리·프로젝트 생성 | 없음 |
| ② 전략 확인 페이지 | 브라우저에 열리는 확인 페이지에서 화면 비율·장수·색·이미지 방식을 고르고 **확정** 클릭 |
| ③ 이미지 생성 | 없음 (`.env`에 키가 있으면 Nano Banana 2.1로 생성) |
| ④ 슬라이드 작성 + 라이브 프리뷰 | `http://127.0.0.1:5050` 에서 한 장씩 만들어지는 것을 확인. 고칠 곳은 요소를 클릭해 **주석**을 남김 |
| ⑤ 품질 검사·내보내기 | 없음 |
| ⑥ 결과 확인 | `projects/<프로젝트>/exports/<제목>_ver1.pptx` 를 PowerPoint로 열기 |

### 2-3. 수정하기

- **주석으로 수정**: 라이브 프리뷰에서 주석을 남긴 뒤 채팅에 `진행시켜` 또는 `주석 반영해줘` → 다시 내보내면 `_ver2.pptx`, `_ver3.pptx`…로 쌓입니다.
- **채팅으로 수정**: `4장 글자 크기 키워줘`, `10장 논의 문장 더 크게` 처럼 말하면 됩니다.
- **AI 이미지 변경**: `표지 그림이 별로야, 더 재미있게` 처럼 불만을 말하면 3.8 Flash가 프롬프트를 고치고 Nano Banana 2.1이 다시 그립니다. 직접 실행할 때는:

```bash
python .claude/skills/ppt-master/scripts/image_revise.py projects/<프로젝트>/images/image_prompts.json --file cover.png --feedback "그림이 너무 밋밋해, 더 몰입감 있게"
```

이전 프롬프트는 `image_prompts.json`의 `prompt_history`에 남습니다.

### 2-4. 자주 쓰는 요청

| 상황 | 이렇게 말하기 |
|---|---|
| 자료로 새 덱 | "이 PDF로 10장 내외 보고용 PPT 만들어줘" |
| 기존 PPTX 양식에 내용 채우기 | "이 템플릿 PPTX에 이 내용 채워서 만들어줘" |
| 기존 PPT 레이아웃만 개선 | "문구·순서는 유지하고 레이아웃만 개선해줘" |
| 완성 덱에 발표자 노트·나레이션 | "이 PPTX에 발표자 노트 넣어줘" |
| 내보낸 PPTX 점검 | "내보낸 PPTX 검증해줘" |

자세한 절차는 [Getting Started](docs/getting-started.md), 워크플로우 규칙 원문은 [`SKILL.md`](.claude/skills/ppt-master/SKILL.md)를 보세요.

---

## 3. 유의점

### 3-1. 처음 쓰기 전에 꼭 할 일

1. **`.env` 파일 만들기** — 폴더 안의 `.env.example`을 복사해 이름을 `.env`로 바꿉니다. ([1-4](#1-4-ai-이미지-생성-설정-선택) 참고)
2. **Gemini API 키 입력하기** — `.env`를 메모장으로 열어 `GEMINI_API_KEY=` 바로 뒤에 [Google AI Studio](https://aistudio.google.com/apikey)에서 발급한 키를 붙여 넣고 저장합니다. 띄어쓰기·따옴표 없이 붙여 넣으세요.
   ```text
   GEMINI_API_KEY=여기에_발급받은_키
   ```
   키가 없으면 AI 그림은 만들 수 없고, 도형·아이콘만으로 된 슬라이드로 진행됩니다.
3. **Pretendard 글꼴 설치하기** — 작업하는 PC와 **발표할 PC 모두** 설치해야 합니다. ([1-3](#1-3-글꼴-pretendard) 참고)

### 3-2. API 키 관리

- 키 입력은 **직접** 하세요. AI 에이전트는 보안상 키를 대신 입력하지 않습니다.
- 키를 채팅창, 메신저, 다른 문서에 붙여 넣지 마세요. `.env` 한 곳에만 둡니다.
- 키가 남에게 노출된 것 같으면 Google AI Studio에서 **그 키를 삭제하고 새로 발급**한 뒤 `.env`의 값만 바꾸면 됩니다.
- 그림을 만들 때마다 사용료가 본인 계정에 청구될 수 있습니다. 사용량은 Google AI Studio에서 확인하세요.

### 3-3. 결과물 확인

- 발표할 PC에 Pretendard가 없으면 글꼴이 바뀌어 줄바꿈·위치가 어긋납니다. 설치가 어려우면 PowerPoint에서 **PDF로 저장**해 가져가세요.
- AI 그림은 만들 때마다 결과가 달라집니다. 쓰기 전에 엉뚱한 글자·로고·인물이 들어가지 않았는지 직접 확인하세요.
- 수정할 때마다 `_ver2`, `_ver3`… 파일이 새로 생깁니다. **번호가 가장 큰 파일이 최신본**입니다.
- 원고 내용은 AI 서비스로 전송됩니다. **학생 실명·연락처 등 개인정보는 지우고** 넣으세요.

### 3-4. 문제가 생겼을 때

| 증상 | 해결 |
|---|---|
| 미리보기 주소(`127.0.0.1:5050`)가 안 열림 | 채팅에 "미리보기 다시 열어줘" |
| 그림 생성 단계에서 키 오류 | `.env` 파일 이름(`.env.txt`가 아닌지)과 키 앞뒤 공백 확인 |
| 그림 생성 단계에서 모델 이름 오류 | `.env`에 `GEMINI_MODEL=` 줄을 추가해 계정에서 쓸 수 있는 그림 모델 이름 입력 |
| 설치 확인(1-5)에서 오류 | 오류 메시지를 그대로 AI 에이전트에게 붙여 넣고 해결 요청 |
| 명령 창에서 한글이 깨짐 | PowerShell에서 `$env:PYTHONIOENCODING='utf-8'` 실행 후 다시 시도 |

---

## 폴더 구조

| 경로 | 내용 |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) / [`AGENTS.md`](AGENTS.md) | AI 에이전트 진입점 (Claude Code / Codex) |
| [`.claude/skills/ppt-master/`](.claude/skills/ppt-master/) | 워크플로우 본체 — `SKILL.md`, `references/`, `scripts/`, `workflows/`, `templates/` |
| `projects/` | 내 작업 공간 — 원고·결과물 (내 PC에만 저장) |
| [`docs/`](docs/) | 사용자 문서 |
| [`.env.example`](.env.example) | API 키 설정 견본 |

## 라이선스

[MIT](LICENSE). [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) (Copyright © Hugo He)와 [byungjunjang/slide-master](https://github.com/byungjunjang/slide-master)를 기반으로 하며, 원 프로젝트의 라이선스 전문과 저작권 고지를 유지합니다. 번들 글꼴·아이콘은 각자의 라이선스(SIL OFL 등)를 따릅니다.

© Made By [Yangphago](https://yangphago.oopy.io/)
