# 04. GitHub 연동 — push · clone · pull

앞에서 만든 기록은 **아직 내 컴퓨터에만** 있습니다.
컴퓨터가 고장 나면 끝입니다. 이제 GitHub에 올립니다.

---

## 1. GitHub에 빈 저장소 만들기

1. https://github.com 로그인
2. 우측 상단 **`+`** → **New repository**
3. 입력:
   - **Repository name**: `git-practice`
   - **Description**: (선택) `Git 연습용 저장소`
   - **Public** 선택 — 포트폴리오로 쓰려면 반드시 Public이어야 남들이 봅니다.
   - ⚠️ **`Add a README file` 체크하지 마세요.** 아래 3개 다 체크 해제입니다.
     이미 내 컴퓨터에 파일이 있어서, 여기서 만들면 충돌이 납니다.
4. **Create repository**

만들면 이런 안내 화면이 나옵니다. 우리가 쓸 건 아래쪽입니다.

```
…or push an existing repository from the command line
```

---

## 2. `git remote add` — 주소 연결

내 로컬 저장소에게 "GitHub 주소는 여기야" 라고 알려줍니다.

```bash
git remote add origin https://github.com/내아이디/git-practice.git
```

- **`origin`** 은 그 주소에 붙인 **별명**입니다. 관례적으로 origin을 씁니다.
  매번 긴 URL을 치지 않으려고 붙이는 이름입니다.
- 주소는 GitHub 저장소 화면의 초록색 **Code** 버튼 → HTTPS 탭에서 복사하면 됩니다.

### 연결 확인

```bash
git remote -v
```

```
origin  https://github.com/내아이디/git-practice.git (fetch)
origin  https://github.com/내아이디/git-practice.git (push)
```

### 주소를 잘못 넣었다면

```bash
git remote set-url origin https://github.com/올바른아이디/git-practice.git
```

---

## 3. `git push` — 올리기

```bash
git push -u origin main
```

- `origin` : 어디로 (GitHub)
- `main` : 어느 브랜치를
- `-u` : "앞으로 기본값으로 기억해" 라는 뜻. **처음 한 번만** 붙입니다.

처음 실행하면 브라우저 창이 뜨고 GitHub 로그인을 요구합니다.
(안 뜨면 02번 문서의 **PAT** 방식으로 로그인하세요.)

성공하면:

```
Enumerating objects: 6, done.
...
To https://github.com/내아이디/git-practice.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

### 확인

GitHub 저장소 페이지를 **새로고침**하세요. 파일이 올라와 있어야 합니다.

### 두 번째부터는 짧게

`-u` 를 한 번 붙였으므로 이제부터는 이것만 치면 됩니다.

```bash
git push
```

---

## 4. 앞으로의 작업 사이클

이제 여러분이 매일 반복할 4줄입니다.

```bash
git status                    # 1. 뭐가 바뀌었나 확인
git add .                     # 2. 담고
git commit -m "메시지"         # 3. 저장하고
git push                      # 4. 올린다
```

> **커밋은 자주, 푸시는 하루 끝에.** 정도로 생각하면 무난합니다.

---

## 5. `git clone` — 남의(또는 내) 저장소 받아오기

다른 사람 코드를 받거나, 집 컴퓨터에서 이어 작업할 때 씁니다.

```bash
git clone https://github.com/david-han-0831/seoultech-python-2026.git
```

- 실행한 위치에 **저장소 이름의 폴더가 새로 생깁니다.**
  그 안에 `.git` 까지 통째로 딸려옵니다. 따로 `git init` 할 필요 없습니다.
- 이미 그 이름의 폴더가 있으면 에러가 납니다. 다른 위치에서 실행하세요.

```bash
cd seoultech-python-2026
```

```bash
git log --oneline
```

받아온 저장소의 모든 기록이 그대로 보입니다.

> **`clone` vs `init`**
> - 새로 시작 → `git init`
> - 이미 있는 걸 받아옴 → `git clone`
> 둘 다 하면 안 됩니다.

---

## 6. `git pull` — 최신 내용 가져오기

학교 컴퓨터에서 push 하고, 집에 와서 이어서 하려면 먼저 받아와야 합니다.

```bash
git pull
```

- GitHub의 최신 커밋을 내 컴퓨터로 가져와 합칩니다.
- **작업 시작 전에 `git pull` 부터** 하는 습관을 들이세요. 충돌이 확 줄어듭니다.

### 자주 만나는 에러

```
! [rejected]        main -> main (fetch first)
error: failed to push some refs
```

> **원인**: GitHub 쪽에 내가 모르는 커밋이 있다.
> (웹에서 직접 파일을 수정했거나, 다른 컴퓨터에서 push 했거나)
> **해결**: `git pull` 로 먼저 받아온 뒤 다시 `git push`

---

## 7. README.md 잘 쓰기

GitHub 저장소를 열면 **README.md 가 첫 화면에 자동으로 렌더링**됩니다.
채용 담당자가 제일 먼저 보는 문서입니다. 이게 곧 표지입니다.

Markdown 문법은 이 정도면 충분합니다.

```markdown
# 제목 (가장 큼)
## 소제목
### 더 작은 제목

일반 문단입니다.

**굵게** *기울임* `코드`

- 목록 1
- 목록 2

1. 번호 목록
2. 두 번째

[링크 이름](https://example.com)

![이미지 설명](스크린샷.png)

​```python
print("코드 블록. 언어 이름을 적으면 색이 입혀집니다.")
​```

| 표 | 만들기 |
|---|---|
| 값1 | 값2 |
```

### 포트폴리오 README에 꼭 들어갈 것

```markdown
# 프로젝트 이름

한 줄 소개.

## 무엇을 만들었나
어떤 문제를 풀려고 만들었는지 2~3문장.

## 사용 기술
- Python 3.12
- requests, BeautifulSoup

## 실행 방법
​```bash
pip install -r requirements.txt
python main.py
​```

## 화면
(스크린샷 이미지)

## 배운 점
막혔던 부분과 어떻게 해결했는지.
```

마지막 **"배운 점"** 이 의외로 면접에서 이야깃거리가 됩니다.

---

## 8. 프로필 꾸미기 (보너스)

GitHub 아이디와 **똑같은 이름의 저장소**를 만들면
그 저장소의 README가 내 프로필 첫 화면에 뜹니다.

- 아이디가 `gildong-hong` 이면 → 저장소 이름도 `gildong-hong`
- Public + `Add a README file` 체크해서 생성
- 거기에 자기소개를 쓰면 프로필이 됩니다.

---

## 연습 문제

1. `git-practice` 를 GitHub에 push 하고, 웹 브라우저에서 파일이 보이는지 확인하세요.
2. **GitHub 웹사이트에서** README.md 를 직접 수정하고 커밋한 뒤,
   내 컴퓨터에서 `git pull` 로 받아오세요.
3. 강사 저장소 `seoultech-python-2026` 을 clone 하고 `git log` 를 확인하세요.
4. 위 README 템플릿을 참고해 내 저장소 README를 다시 쓰세요.
   (제목 / 소개 / 사용 기술 / 실행 방법 이 4개는 필수)
