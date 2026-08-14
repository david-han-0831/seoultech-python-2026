/*
  자바스크립트 - 04. 배열 (Array)

  파이썬의 리스트에 해당합니다. 이름만 다르고 거의 같습니다.
  실행: node 04_배열.js
*/

// ---------------------------------------------------------------
// 1. 배열 만들기와 꺼내기
// ---------------------------------------------------------------

const fruits = ["사과", "바나나", "포도"];

console.log(fruits);          // [ '사과', '바나나', '포도' ]
console.log(fruits[0]);       // 사과   (0번부터 시작 - 파이썬과 동일)
console.log(fruits.length);   // 3      (파이썬 len(fruits))

// [파이썬과 다른 점] 음수 인덱스가 안 됩니다.
// console.log(fruits[-1]);   // undefined
console.log(fruits[fruits.length - 1]);  // 포도  ← 이렇게 씁니다
console.log(fruits.at(-1));              // 포도  ← 최신 문법. 이게 더 편합니다

// 없는 인덱스에 접근하면 에러가 아니라 undefined 가 나옵니다.
console.log(fruits[99]);      // undefined


// [const 인데 왜 바꿀 수 있나?]
// const 는 "변수가 다른 것을 가리키지 못하게" 막는 것이지,
// 배열 안의 내용을 못 바꾸게 하는 게 아닙니다.
fruits[0] = "딸기";           // 가능
console.log(fruits);          // [ '딸기', '바나나', '포도' ]
// fruits = ["다른", "배열"];  // 이건 에러


// ---------------------------------------------------------------
// 2. 추가와 삭제
// ---------------------------------------------------------------

const numbers = [1, 2, 3];

numbers.push(4);          // 맨 뒤에 추가 (파이썬 append)
console.log(numbers);     // [1, 2, 3, 4]

numbers.pop();            // 맨 뒤 삭제 + 그 값 반환
console.log(numbers);     // [1, 2, 3]

numbers.unshift(0);       // 맨 앞에 추가
console.log(numbers);     // [0, 1, 2, 3]

numbers.shift();          // 맨 앞 삭제
console.log(numbers);     // [1, 2, 3]

// 중간 삭제 - splice(시작인덱스, 삭제개수)
const letters = ["a", "b", "c", "d"];
letters.splice(1, 2);     // 1번부터 2개 삭제
console.log(letters);     // [ 'a', 'd' ]


// ---------------------------------------------------------------
// 3. 자르기와 합치기
// ---------------------------------------------------------------

const arr = [1, 2, 3, 4, 5];

console.log(arr.slice(1, 3));   // [2, 3]   (파이썬 arr[1:3] 과 동일)
console.log(arr.slice(2));      // [3, 4, 5]
console.log(arr.slice(-2));     // [4, 5]

console.log(arr.concat([6, 7]));      // [1,2,3,4,5,6,7]
console.log([...arr, 6, 7]);          // 같은 결과 (스프레드 문법, 요즘 스타일)

console.log(arr.join(", "));    // "1, 2, 3, 4, 5"  (파이썬 ", ".join())
console.log(arr.includes(3));   // true             (파이썬 3 in arr)
console.log(arr.indexOf(3));    // 2                (없으면 -1)
console.log(arr.reverse());     // [5,4,3,2,1]      ← 원본을 바꿉니다. 주의


// ---------------------------------------------------------------
// 4. 배열 메서드 3대장 - map / filter / reduce
// ---------------------------------------------------------------

// 자바스크립트에서 가장 중요한 부분입니다.
// 파이썬의 리스트 컴프리헨션 자리를 이 셋이 대신합니다.

const scores = [90, 45, 78, 100, 62];


// (1) map - 각 요소를 변환해서 "새 배열"을 만듦
//     파이썬:  [s + 5 for s in scores]

const bonus = scores.map((score) => score + 5);
console.log(bonus);    // [95, 50, 83, 105, 67]
console.log(scores);   // 원본은 그대로 [90, 45, 78, 100, 62]

// 객체로 변환하기 (화면에 뿌릴 때 자주 씀)
const names = ["홍길동", "김철수"];
const users = names.map((name) => ({ name: name, level: 1 }));
console.log(users);    // [ { name: '홍길동', level: 1 }, { name: '김철수', level: 1 } ]


// (2) filter - 조건에 맞는 것만 골라 "새 배열"을 만듦
//     파이썬:  [s for s in scores if s >= 70]

const passed = scores.filter((score) => score >= 70);
console.log(passed);   // [90, 78, 100]

// filter 는 true/false 를 반환하는 함수를 받습니다.
const evens = [1, 2, 3, 4, 5, 6].filter((n) => n % 2 === 0);
console.log(evens);    // [2, 4, 6]


// (3) reduce - 전체를 하나의 값으로 접음 (합계, 최댓값 등)
//     파이썬:  sum(scores)

const total = scores.reduce((sum, score) => sum + score, 0);
//                          ①누적값  ②현재값              ③시작값
console.log(total);              // 375
console.log(total / scores.length);  // 75  평균

// [자바스크립트에는 sum() 함수가 없습니다.] 합계는 reduce 로 구합니다.


// (4) 이어서 쓰기 (체이닝) - 실무에서 흔한 형태
const result = scores
  .filter((s) => s >= 70)      // 70점 이상만 골라서
  .map((s) => `${s}점`)         // 문자열로 바꾸고
  .join(", ");                 // 하나로 합침
console.log(result);           // "90점, 78점, 100점"


// ---------------------------------------------------------------
// 5. 그 밖에 자주 쓰는 것
// ---------------------------------------------------------------

console.log(scores.find((s) => s >= 80));       // 90    조건에 맞는 "첫 값"
console.log(scores.findIndex((s) => s >= 80));  // 0     그 인덱스
console.log(scores.some((s) => s === 100));     // true  하나라도 만족하나?
console.log(scores.every((s) => s >= 40));      // true  전부 만족하나?

console.log(Math.max(...scores));   // 100  (... 은 배열을 펼치는 문법)
console.log(Math.min(...scores));   // 45


// 정렬 - [주의] 기본 정렬은 "문자열 기준"입니다!
const nums = [10, 9, 100, 1];
console.log([...nums].sort());               // [1, 10, 100, 9]  ← 이상하죠?

// 숫자 정렬은 비교 함수를 넘겨야 합니다.
console.log([...nums].sort((a, b) => a - b));  // [1, 9, 10, 100]  오름차순
console.log([...nums].sort((a, b) => b - a));  // [100, 10, 9, 1]  내림차순

// sort 는 원본을 바꿉니다. 그래서 위처럼 [...nums] 로 복사본을 만들어 정렬합니다.


// ---------------------------------------------------------------
// 연습 문제
// ---------------------------------------------------------------

const students = [
  { name: "홍길동", score: 85 },
  { name: "김철수", score: 92 },
  { name: "이영희", score: 47 },
  { name: "박민수", score: 78 },
];

// 1. 모든 학생의 이름만 뽑아 배열로 만드세요. (map)

// 2. 60점 이상인 학생만 골라내세요. (filter)

// 3. 전체 평균 점수를 구하세요. (reduce)

// 4. 점수가 높은 순으로 정렬하세요. (sort)

// 5. "홍길동: 85점" 형태의 문자열 배열을 만들고, 줄바꿈으로 이어 출력하세요.
//    (map + join("\n"))

// 6. 90점 이상인 학생이 있는지 true/false 로 확인하세요. (some)
