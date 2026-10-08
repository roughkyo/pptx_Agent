---
deck_id: supabase
kind: deck
category: brand
summary: Supabase 기반 개발자 플랫폼 덱 — 흰 캔버스, 절제된 에메랄드, 편집 가능한 제품 UI 패널
keywords: [supabase, developer, emerald, product-ui, saas]
primary_color: "#3ECF8E"
canvas_format: ppt169
canvas_width: 1280
canvas_height: 720
canvas_viewbox: "0 0 1280 720"
source_canvas_width: 1280
source_canvas_height: 720
source_viewbox: "0 0 1280 720"
replication_mode: standard
native_structure_mode: structured
page_count: 7
placeholders:
  01_cover: ["{{TITLE}}", "{{SUBTITLE}}", "{{DATE}}", "{{AUTHOR}}"]
  02_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}", "{{CHAPTER_DESC}}"]
  02_toc: ["{{PAGE_TITLE}}", "{{TOC_ITEM_1_TITLE}}", "{{TOC_ITEM_1_DESC}}", "{{TOC_ITEM_2_TITLE}}", "{{TOC_ITEM_2_DESC}}", "{{TOC_ITEM_3_TITLE}}", "{{TOC_ITEM_3_DESC}}", "{{TOC_ITEM_4_TITLE}}", "{{TOC_ITEM_4_DESC}}"]
  03_content: ["{{PAGE_TITLE}}", "{{CONTENT_AREA}}", "{{PAGE_NUM}}"]
  03a_content_product_ui: ["{{PAGE_TITLE}}", "{{KEY_MESSAGE}}", "{{CONTENT_AREA}}", "{{PAGE_NUM}}"]
  03b_content_code_data: ["{{PAGE_TITLE}}", "{{CONTENT_AREA}}", "{{CODE_SAMPLE}}", "{{PAGE_NUM}}"]
  04_ending: ["{{THANK_YOU}}", "{{ENDING_SUBTITLE}}", "{{CONTACT_INFO}}"]
defaults:
  mode: briefing
  visual_style: swiss-minimal
  delivery_purpose: balanced
---

# Supabase Developer Platform — Design Specification

## I. Template Overview

- **Use cases**: 개발자 플랫폼·SaaS 소개, 기술 강의, 제품 업데이트, 프로젝트 발표
- **Design tone**: 명료하고 절제된 개발자 중심 미니멀리즘
- **Theme mode**: 흰색 중심의 light. 짙은 패널은 코드와 제품 UI 영역에서만 제한적으로 사용
- **Visual identity**: 넓은 흰 여백 위에 에메랄드 한 색을 희소하게 배치하고, 얇은 회색 헤어라인과 편집 가능한 대시보드·SQL 패널을 핵심 시각물로 사용한다.

## II. Color Scheme

| Role | HEX | Application |
| --- | --- | --- |
| Primary emerald | `#3ECF8E` | 핵심 CTA, 상태 점, 한두 개의 강조 수치 |
| Primary deep | `#24B47E` | 선 그래프와 활성 상태 |
| Canvas | `#FFFFFF` | 모든 기본 페이지 배경 |
| Canvas soft | `#FAFAFA` | 보조 패널과 표 헤더 |
| Canvas night | `#1C1C1C` | 코드 블록과 개발자 콘솔 |
| Ink | `#171717` | 제목과 본문 |
| Ink mute | `#707070` | 설명, 캡션, 보조 정보 |
| Hairline | `#DFDFDF` | 1px 경계선과 구분선 |
| Hairline cool | `#EDEDED` | 제품 UI의 내부 격자 |

에메랄드는 한 화면의 작은 핵심 지점에만 사용한다. 그라디언트, 사진 배경, 에메랄드 대면적 배경은 사용하지 않는다. 어두운 면은 코드·콘솔·마무리 페이지에만 제한한다.

## III. Typography

- 모든 텍스트는 번들 글꼴인 `Pretendard`를 사용한다.
- 제목은 Medium 또는 500, 본문은 400을 사용하며 굵기 600 이상을 장식적으로 남용하지 않는다.
- 큰 제목은 약한 음수 자간으로 조밀하게 구성하고, 코드 표본은 `Consolas, Pretendard, monospace`를 사용한다.
- 기본 본문 기준은 20px이며, 짧은 설명은 16–18px 범위로 낮춘다.

## IV. Signature Design Elements

- 좌상단의 작은 `supabase` 워드마크와 에메랄드 상태 점을 모든 페이지의 Master에 고정한다.
- 1px 회색 헤어라인, 6–12px 모서리, 평면 카드로 구조를 만든다.
- 제품 UI는 툴바·사이드바·테이블·SQL 편집기를 단순 SVG 도형으로 구성해 PowerPoint에서 편집 가능하게 유지한다.
- 제품 패널은 페이지 오른쪽 또는 하단 55–65% 영역에 배치하고, 텍스트는 넓은 여백을 가진 왼쪽 열에 둔다.
- 그림자 대신 경계선과 겹친 패널 위치로 깊이를 표현한다.

## V. Page Roster

| File | Role | Layout key / picker name | Visual character and intended content |
| --- | --- | --- | --- |
| `01_cover.svg` | cover | `supabase-cover` / Supabase Cover | 좌측 제목·부제, 우측에 대시보드와 SQL 패널이 겹친 제품 중심 표지 |
| `02_chapter.svg` | chapter | `supabase-chapter` / Supabase Chapter | 큰 챕터 번호와 제목, 하단의 어두운 콘솔 패널로 전환감 부여 |
| `02_toc.svg` | toc | `supabase-toc` / Supabase Contents | 네 개 항목을 얇은 구분선과 번호로 정렬한 여백 중심 목차 |
| `03_content.svg` | content | `supabase-content` / Supabase Content | 제목과 넓은 본문 영역, 우측 에메랄드 상태 레일을 가진 범용 본문 |
| `03a_content_product_ui.svg` | content | `supabase-product-ui` / Supabase Product UI | 왼쪽 핵심 메시지와 설명, 오른쪽 편집 가능한 제품 UI 패널 |
| `03b_content_code_data.svg` | content | `supabase-code-data` / Supabase Code and Data | 왼쪽 설명과 지표, 오른쪽 어두운 코드 블록 및 데이터 행 |
| `04_ending.svg` | ending | `supabase-ending` / Supabase Closing | 짙은 콘솔형 배경 위 에메랄드 점과 간결한 마무리 메시지 |

모든 페이지는 `supabase-master` / `Supabase Master`를 공유한다. 콘텐츠 페이지 변형은 고정 패널과 슬롯 구조가 달라 각각 독립된 Layout으로 정의한다.
