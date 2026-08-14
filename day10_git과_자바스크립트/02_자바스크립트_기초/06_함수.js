/*
  자바스크립트 - 06. 함수

  실행: node 06_함수.js
*/

// ---------------------------------------------------------------
// 1. 기본 형태 - function 선언문
// ---------------------------------------------------------------

// 파이썬:
//   def greet(name):
//       return f"안녕하세요, {name}님"

function greet(name) {
  return `안녕하세요, ${name}님`;
}

console.log(greet("홍길동"));

// def → function, 콜론 → 중괄호. 나머지는 같습니다.


// 매개변수 기본값 (파이썬과 동일)
function introduce(name, age = 20) {
  return `${name}, ${age}세`;
}
console.log(introduce("김철수"));       // 김철수, 20세
console.log(introduce("이영희", 22));   // 이영희, 22세

// [파이썬과 다른 점] 인자 개수가 안 맞아도 에러가 나지 않습니다.
console.log(introduce());   // undefined, 20세  ← name 이 undefined


// return 이 없으면 undefined 를 반환합니다. (파이썬의 None)
function noReturn() {
  console.log("아무것도 반환 안 함");
}
console.log(noReturn());    // undefined


// ---------------------------------------------------------------
// 2. 화살표 함수 (arrow function) - 요즘 표준
// ---------------------------------------------------------------

// 같은 함수를 세 가지로 쓸 수 있습니다.

const add1 = function (a, b) {   // 함수 표현식
  return a + b;
};

const add2 = (a, b) => {         // 화살표 함수
  return a + b;
};

const add3 = (a, b) => a + b;    // 한 줄이면 { } 와 return 생략 가능

console.log(add1(1, 2), add2(1, 2), add3(1, 2));   // 3 3 3

// 매개변수가 1개면 소괄호도 생략 가능
const double = (n) => n * 2;
console.log(double(5));   // 10

// 객체를 반환할 때는 소괄호로 감싸야 합니다. (중괄호가 블록으로 해석되므로)
const makeUser = (name) => ({ name: name, level: 1 });
console.log(makeUser("홍길동"));


// [언제 뭘 쓰나]
//   - 배열 메서드(map, filter 등)에 넘기는 짧은 함수 → 화살표 함수
//   - 독립적으로 정의하는 함수 → 둘 다 무방
// 실무 코드는 화살표 함수가 압도적으로 많습니다.


// ---------------------------------------------------------------
// 3. 함수도 값입니다 (일급 함수)
// ---------------------------------------------------------------

// 자바스크립트에서 함수는 숫자나 문자열처럼 "값"입니다.
// 변수에 넣고, 다른 함수에 넘기고, 반환할 수 있습니다.

const sayHi = () => console.log("안녕");
sayHi();                  // 안녕
console.log(typeof sayHi);   // function


// 함수를 인자로 넘기기 (콜백 함수)
function repeat(count, action) {
  for (let i = 1; i <= count; i++) {
    action(i);            // 넘겨받은 함수를 실행
  }
}

repeat(3, (n) => console.log(`${n}번째`));

// map, filter, forEach 가 정확히 이 방식으로 동작합니다.
// 우리가 넘긴 화살표 함수를 배열이 대신 실행해 주는 것입니다.


// ---------------------------------------------------------------
// 4. 스코프 - 변수가 보이는 범위
// ---------------------------------------------------------------

const globalVar = "전역";

function scopeTest() {
  const localVar = "지역";
  console.log(globalVar);   // 전역   ← 밖의 것은 보임
  console.log(localVar);    // 지역
}

scopeTest();
// console.log(localVar);   // 에러! 함수 밖에서는 안 보임


// let/const 는 중괄호 블록 단위로 갇힙니다.
if (true) {
  const inside = "블록 안";
  console.log(inside);
}
// console.log(inside);     // 에러

// [파이썬과 다른 점] 파이썬의 if 블록 안 변수는 밖에서도 보이지만,
//                   자바스크립트의 let/const 는 안 보입니다.


// ---------------------------------------------------------------
// 5. 실전 예제 - 5일차 파이썬 코드와 비교
// ---------------------------------------------------------------

// 학생 목록에서 합격자 명단을 만드는 함수
function getPassedNames(students, cutoff = 60) {
  return students
    .filter((s) => s.score >= cutoff)
    .map((s) => s.name);
}

const students = [
  { name: "홍길동", score: 85 },
  { name: "김철수", score: 45 },
  { name: "이영희", score: 92 },
];

console.log(getPassedNames(students));       // [ '홍길동', '이영희' ]
console.log(getPassedNames(students, 90));   // [ '이영희' ]


// 성적 통계를 객체로 반환
const getStats = (scores) => ({
  count: scores.length,
  total: scores.reduce((a, b) => a + b, 0),
  average: scores.reduce((a, b) => a + b, 0) / scores.length,
  max: Math.max(...scores),
  min: Math.min(...scores),
});

console.log(getStats([85, 45, 92]));


// ---------------------------------------------------------------
// 6. 비동기 함수 맛보기 (async / await)
// ---------------------------------------------------------------

// 5일차에 requests 로 API를 호출했습니다. 자바스크립트는 fetch 를 씁니다.
// 다만 네트워크 응답은 "기다려야" 하므로 async / await 를 붙입니다.

async function getUser() {
  const response = await fetch("https://api.github.com/users/octocat");
  const data = await response.json();
  console.log(data.name, data.public_repos);
}

// 실행해 보려면 아래 주석을 푸세요. (Node 18 이상 또는 브라우저 콘솔)
// getUser();

// 규칙 두 가지만 기억하세요.
//   1. 기다려야 하는 작업 앞에는 await 를 붙인다
//   2. await 를 쓰는 함수 앞에는 async 를 붙인다
//
// 자세한 건 다음 단계에서 배웁니다. 지금은 "이런 게 있다" 정도면 충분합니다.


// ---------------------------------------------------------------
// 연습 문제
// ---------------------------------------------------------------

// 1. 두 수를 받아 큰 값을 반환하는 함수 max2 를 화살표 함수로 작성하세요.

// 2. 이름 배열을 받아 "홍길동님, 김철수님" 형태의 문자열을 반환하는 함수를 작성하세요.

// 3. 점수를 받아 학점(A/B/C/F)을 반환하는 함수 getGrade 를 작성하고,
//    배열 [95, 82, 71, 40] 에 map 으로 적용해 보세요.

// 4. 함수를 인자로 받아 3번 실행하는 함수 runThreeTimes(fn) 을 작성하세요.

// 5. 숫자 배열을 받아 짝수의 합을 반환하는 함수를 filter + reduce 로 작성하세요.

// 6. (도전) getStats 를 참고해, 학생 객체 배열을 받아
//    { 합격자수, 불합격자수, 평균 } 을 반환하는 함수를 작성하세요.
