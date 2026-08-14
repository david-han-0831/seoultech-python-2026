/*
  자바스크립트 - 08. 콜백과 동기/비동기

  자바스크립트를 배울 때 가장 많이 막히는 부분입니다.
  하지만 이걸 넘기면 "자바스크립트를 안다"고 말할 수 있습니다.

  실행: node 08_콜백과_비동기.js

  ⚠️ 먼저 읽으세요 — 실행하면 당황합니다.

  "========== 3. Promise ==========" 같은 제목만 주르륵 찍히고
  그 아래가 텅 비어 보일 겁니다. 고장난 게 아닙니다.

    제목 출력(console.log)은 동기라서 → 전부 먼저 실행되고,
    Promise·setTimeout 결과는 비동기라서 → 맨 뒤에 몰려서 나옵니다.

  즉 "코드를 쓴 순서"와 "실행되는 순서"가 다릅니다.
  이 어긋남을 눈으로 확인하는 것이 이 파일의 목적입니다.
  실행 결과를 위에서 아래로 읽지 말고, 아래 각 항목의 설명과 맞춰 보세요.
*/

console.log("========== 1. 콜백 함수 ==========");

// ---------------------------------------------------------------
// 1. 콜백(callback)이란
// ---------------------------------------------------------------

// 06번 파일에서 봤듯이, 자바스크립트에서 함수는 "값"입니다.
// 그래서 함수를 다른 함수에 인자로 넘길 수 있습니다.
//
//   콜백 함수 = 남에게 넘겨주는 함수. "나중에 대신 불러줘(call back)" 라는 뜻.

function greet(name) {
  console.log(`안녕하세요, ${name}님`);
}

function processUser(name, callback) {
  console.log("사용자 정보를 처리합니다...");
  callback(name);          // 넘겨받은 함수를 여기서 실행
}

processUser("홍길동", greet);
//   사용자 정보를 처리합니다...
//   안녕하세요, 홍길동님

// 보통은 이름을 따로 안 붙이고 그 자리에서 만들어 넘깁니다.
processUser("김철수", (name) => {
  console.log(`${name}님, 반갑습니다`);
});


// ---------------------------------------------------------------
// 2. 사실 우리는 이미 콜백을 써 왔습니다
// ---------------------------------------------------------------

const numbers = [1, 2, 3];

numbers.forEach((n) => console.log(`forEach: ${n}`));
//              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 이게 콜백입니다.
//              배열이 요소 개수만큼 이 함수를 "대신 불러줍니다"

const doubled = numbers.map((n) => n * 2);   // 이것도 콜백
console.log(doubled);

// DOM 이벤트도 마찬가지입니다.
//   button.addEventListener("click", () => { ... });
//                                    ^^^^^^^^^^^^ 콜백
//   "클릭이 일어나면 이 함수를 대신 불러줘"

// [왜 콜백을 쓰나]
//   "언제 실행할지"를 내가 정할 수 없는 일이 있기 때문입니다.
//   - 사용자가 언제 클릭할지 모른다
//   - 서버 응답이 언제 올지 모른다
//   그래서 "그 일이 생기면 이걸 실행해" 라고 함수를 맡겨두는 것입니다.


console.log("\n========== 2. 동기와 비동기 ==========");

// ---------------------------------------------------------------
// 3. 동기(synchronous) vs 비동기(asynchronous)
// ---------------------------------------------------------------

// [동기] 한 줄이 끝나야 다음 줄이 실행된다. 지금까지 짠 코드 전부.
//        비유: 은행 창구. 앞사람 업무가 끝나야 내 차례가 온다.
//
// [비동기] 오래 걸리는 일을 맡겨두고 다음 줄로 먼저 넘어간다.
//          일이 끝나면 맡겨둔 콜백이 나중에 실행된다.
//          비유: 카페 진동벨. 주문하고 자리에 앉아 다른 일을 하다가,
//                벨이 울리면 그때 커피를 받으러 간다.

// 왜 비동기가 필요한가?
//   자바스크립트는 "일하는 사람이 한 명"입니다. (싱글 스레드)
//   서버 응답을 3초 기다리는 동안 동기로 멈춰 있으면,
//   그 3초 동안 화면이 통째로 얼어붙습니다. 스크롤도 클릭도 안 됩니다.
//   그래서 오래 걸리는 일은 전부 비동기로 처리합니다.


// ---------------------------------------------------------------
// 4. setTimeout 으로 비동기 체험하기
// ---------------------------------------------------------------

// setTimeout(함수, 밀리초) : "몇 ms 뒤에 이 함수를 실행해줘"
// 파이썬의 time.sleep() 과는 완전히 다릅니다.
//   time.sleep(2)  → 진짜로 2초 멈춤 (동기)
//   setTimeout(fn, 2000) → 안 멈춤. 그냥 예약만 하고 다음 줄로 감 (비동기)

console.log("① 첫 번째");

setTimeout(() => {
  console.log("② 두 번째 (0초 뒤로 예약했는데도 마지막에 나옴)");
}, 0);

console.log("③ 세 번째");

// 실제 출력 순서:
//   ① 첫 번째
//   ③ 세 번째
//   ② 두 번째
//
// 0초인데도 마지막입니다. 왜?
//   비동기 작업은 "지금 하는 일이 전부 끝난 뒤"에 처리되기 때문입니다.
//   순서를 담당하는 규칙을 이벤트 루프(event loop)라고 부릅니다.
//   지금은 "비동기는 무조건 나중"이라고만 기억해도 충분합니다.


// ---------------------------------------------------------------
// 5. 초보자가 100% 하는 실수
// ---------------------------------------------------------------

function getDataWrong() {
  let result = "아직 없음";

  setTimeout(() => {
    result = "서버에서 받아온 데이터";   // 1초 뒤에 실행됨
  }, 1000);

  return result;   // 지금 당장 실행됨 → "아직 없음"
}

console.log("잘못된 방식:", getDataWrong());   // 아직 없음

// 결과를 기다리지 않고 먼저 return 해버렸습니다.
// 비동기 작업의 결과는 이렇게 꺼낼 수 없습니다.
// 그래서 콜백 → Promise → async/await 가 필요해진 것입니다.


// ---------------------------------------------------------------
// 6. 콜백으로 해결하기 → 그리고 콜백 지옥
// ---------------------------------------------------------------

function getData(callback) {
  setTimeout(() => {
    callback("서버에서 받아온 데이터");   // 끝나면 콜백을 부른다
  }, 500);
}

getData((data) => {
  console.log("콜백 방식:", data);
});

// 문제는 순서대로 여러 번 해야 할 때입니다.
//
//   getUser(1, (user) => {
//     getPosts(user.id, (posts) => {
//       getComments(posts[0].id, (comments) => {
//         getLikes(comments[0].id, (likes) => {
//           console.log(likes);      ← 오른쪽으로 계속 밀려남
//         });
//       });
//     });
//   });
//
// 이걸 "콜백 지옥(callback hell)" 이라고 부릅니다.
// 읽기도 어렵고 에러 처리는 더 어렵습니다.
// 이 문제를 풀려고 나온 것이 Promise 입니다.


console.log("\n========== 3. Promise ==========");

// ---------------------------------------------------------------
// 7. Promise - "결과를 나중에 주겠다는 약속"
// ---------------------------------------------------------------

// Promise 객체는 세 가지 상태 중 하나입니다.
//   pending   진행 중        (배달 중)
//   fulfilled 성공           (배달 완료)  → .then() 이 받음
//   rejected  실패           (배달 사고)  → .catch() 가 받음

function getDataPromise(shouldFail = false) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (shouldFail) {
        reject(new Error("데이터를 불러오지 못했습니다"));   // 실패 시
      } else {
        resolve("Promise로 받아온 데이터");                  // 성공 시
      }
    }, 300);
  });
}

getDataPromise()
  .then((data) => {
    console.log("then:", data);
    return data.length;          // return 한 값이 다음 then 으로 넘어감
  })
  .then((length) => {
    console.log("then 이어서:", length);
  })
  .catch((error) => {
    console.log("catch:", error.message);
  })
  .finally(() => {
    console.log("finally: 성공하든 실패하든 항상 실행");
  });

// 콜백 지옥이 아래로 쭉 이어지는 형태로 펴집니다.
//
//   getUser(1)
//     .then(user => getPosts(user.id))
//     .then(posts => getComments(posts[0].id))
//     .then(comments => console.log(comments))
//     .catch(err => console.log(err));
//
// 훨씬 낫지만 아직도 .then 이 계속 붙습니다.


console.log("\n========== 4. async / await ==========");

// ---------------------------------------------------------------
// 8. async / await - 비동기를 동기처럼 쓰기 (요즘 표준)
// ---------------------------------------------------------------

// 규칙 딱 두 개입니다.
//   1. 기다려야 하는 것 앞에 await 를 붙인다
//   2. await 를 쓰는 함수 앞에 async 를 붙인다

async function main() {
  console.log("--- main 시작 ---");

  // await 를 붙이면 그 줄에서 결과가 올 때까지 기다렸다가 다음 줄로 갑니다.
  // 겉보기엔 동기 코드처럼 위에서 아래로 읽힙니다.
  const data = await getDataPromise();
  console.log("await:", data);

  // 에러 처리는 파이썬에서 배운 try / except 와 똑같습니다. (except → catch)
  try {
    const bad = await getDataPromise(true);   // 일부러 실패시킴
    console.log(bad);                          // 여기는 실행되지 않음
  } catch (error) {
    console.log("try/catch 로 잡음:", error.message);
  }

  // 순서대로 여러 번 (콜백 지옥이 이렇게 펴집니다)
  const first = await getDataPromise();
  const second = await getDataPromise();
  console.log("두 번 순서대로 완료:", first === second);

  console.log("--- main 끝 ---");
}

main();

// [주의] async 함수는 항상 Promise 를 반환합니다.
//        그래서 async 함수의 결과를 쓰려면 그것도 await 해야 합니다.
//
//   const r = main();          // Promise { <pending> }  ← 값이 아님
//   const r = await main();    // 실제 값


console.log("\n========== 5. 실전 ==========");

// ---------------------------------------------------------------
// 9. fetch - 5일차 requests 의 자바스크립트 버전
// ---------------------------------------------------------------

// Python:
//   import requests
//   res = requests.get(url)
//   data = res.json()
//
// JavaScript:
//   const res = await fetch(url);
//   const data = await res.json();
//
// await 가 두 번인 이유:
//   ① fetch(url)      → 응답 헤더가 도착할 때까지 기다림
//   ② res.json()      → 본문을 전부 받아 JSON으로 바꿀 때까지 기다림

async function getGithubUser(username) {
  try {
    const res = await fetch(`https://api.github.com/users/${username}`);

    // [중요] fetch 는 404, 500 이어도 에러를 던지지 않습니다!
    //        requests 와 달리 직접 확인해야 합니다.
    if (!res.ok) {
      throw new Error(`요청 실패: ${res.status}`);
    }

    const data = await res.json();
    return { name: data.name, repos: data.public_repos };
  } catch (error) {
    console.log("에러:", error.message);
    return null;
  }
}


// ---------------------------------------------------------------
// 10. 순차 처리 vs 병렬 처리 - 속도가 몇 배 차이납니다
// ---------------------------------------------------------------

async function compare() {
  const users = ["octocat", "torvalds", "gaearon"];

  // (1) 순차 - 하나 끝나야 다음 시작. 3번 기다림.
  console.time("순차");
  const seq = [];
  for (const u of users) {
    seq.push(await getGithubUser(u));
  }
  console.timeEnd("순차");

  // (2) 병렬 - 셋을 동시에 보내고 다 올 때까지 한 번만 기다림.
  //     Promise.all(배열) : 전부 성공하면 결과 배열을 줌. 하나라도 실패하면 catch.
  console.time("병렬");
  const par = await Promise.all(users.map((u) => getGithubUser(u)));
  console.timeEnd("병렬");

  console.log(par);

  // 서로 의존하지 않는 요청은 반드시 Promise.all 로 묶으세요.
  // 하나라도 실패해도 나머지를 살리고 싶으면 Promise.allSettled 를 씁니다.
}

// 인터넷 연결이 필요합니다. 실행하려면 아래 주석을 푸세요.
// compare();


// ---------------------------------------------------------------
// 11. 자주 하는 실수 3가지
// ---------------------------------------------------------------

// (1) await 를 빼먹음
//     const data = fetch(url);       // Promise 객체가 담김
//     const data = await fetch(url); // 실제 응답이 담김

// (2) forEach 안에서 await → 기다리지 않고 그냥 지나감
//     users.forEach(async (u) => { await getUser(u); });   // ❌ 안 기다림
//     for (const u of users) { await getUser(u); }          // ⭕ 순차
//     await Promise.all(users.map(u => getUser(u)));        // ⭕ 병렬

// (3) 최상위에서 await 사용
//     Node의 .js 파일이나 일반 script 태그에서는 함수 밖 await 가 안 됩니다.
//     async 함수로 감싸서 부르세요.
//       async function main() { ... }
//       main();


// ---------------------------------------------------------------
// 정리
// ---------------------------------------------------------------
//
//   콜백    함수를 넘겨두고 "나중에 대신 실행해줘"
//   동기    한 줄씩 순서대로. 오래 걸리면 화면이 멈춤
//   비동기  맡겨두고 먼저 진행. 끝나면 나중에 처리
//
//   콜백 → Promise(.then/.catch) → async/await 순으로 발전했습니다.
//   ⭐ 새로 코드를 짤 때는 async/await 만 쓰면 됩니다.
//      나머지는 남의 코드를 읽기 위해 알아둡니다.


// ---------------------------------------------------------------
// 연습 문제
// ---------------------------------------------------------------

// 1. 아래 코드의 출력 순서를 예측한 뒤 실행해서 확인하세요.
//      console.log("A");
//      setTimeout(() => console.log("B"), 0);
//      console.log("C");

// 2. delay(ms) 함수를 만드세요. ms 밀리초 뒤에 resolve 하는 Promise 를 반환합니다.
//    그리고 async 함수에서 await delay(1000) 을 세 번 호출해
//    1초 간격으로 "1", "2", "3" 이 찍히게 만드세요.

// 3. getGithubUser 를 이용해 본인의 GitHub 아이디 정보를 출력하세요.
//    (오늘 Git 파트에서 만든 계정을 쓰세요)

// 4. 존재하지 않는 아이디(예: "이런계정없음12345")를 넣었을 때
//    에러 메시지가 잘 나오는지 확인하세요.

// 5. 아이디 5개를 순차와 병렬로 각각 가져와 시간 차이를 측정하세요.
//    (console.time / console.timeEnd)

// 6. (도전) 07_DOM_기초.html 을 참고해, 입력창에 GitHub 아이디를 넣으면
//    프로필 사진과 저장소 개수를 화면에 보여주는 페이지를 만드세요.
//    → 09_API_호출_실습.html 에 완성본이 있습니다. 먼저 직접 해 보세요.
