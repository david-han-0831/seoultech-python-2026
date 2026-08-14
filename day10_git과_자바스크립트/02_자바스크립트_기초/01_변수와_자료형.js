/*
  자바스크립트 - 01. 변수와 자료형

  파이썬을 아는 상태에서 봅니다. 다른 점 위주로 정리했습니다.
  실행: node 01_변수와_자료형.js
*/

// ---------------------------------------------------------------
// 1. 변수 선언 - let 과 const
// ---------------------------------------------------------------

// 파이썬은 그냥 name = "홍길동" 이라고 씁니다.
// 자바스크립트는 앞에 let 또는 const 를 붙여야 합니다.

let name = "홍길동";       // 나중에 값을 바꿀 수 있음
const BIRTH_YEAR = 2005;   // 바꿀 수 없음 (상수)

console.log(name);         // 홍길동
console.log(BIRTH_YEAR);   // 2005

name = "김철수";           // let 이라서 가능
console.log(name);         // 김철수

// BIRTH_YEAR = 2006;      // 에러! TypeError: Assignment to constant variable.


// [실무 규칙]
// 일단 전부 const 로 쓰고, 값을 바꿔야 할 때만 let 으로 바꾸세요.
// 그러면 "이 값은 안 바뀐다"는 게 코드에 드러나서 읽기 쉬워집니다.

// [주의] var 라는 옛날 키워드도 있습니다. 인터넷 예제에서 많이 보이지만
//        문제가 많아 요즘은 쓰지 않습니다. let / const 만 쓰세요.


// ---------------------------------------------------------------
// 2. 변수 이름 규칙
// ---------------------------------------------------------------

// 파이썬은 snake_case (밑줄), 자바스크립트는 camelCase (낙타 등) 를 씁니다.

const studentName = "이영희";   // O  자바스크립트 스타일
const student_name2 = "박민수"; // △  동작은 하지만 JS답지 않음

console.log(studentName);

// 대소문자를 구분합니다. name 과 Name 은 다른 변수입니다.


// ---------------------------------------------------------------
// 3. 자료형 (typeof 로 확인)
// ---------------------------------------------------------------

const age = 20;                 // number
const height = 175.5;           // number  ← 파이썬과 달리 int/float 구분이 없습니다
const nickname = "길동이";       // string
const isStudent = true;         // boolean ← 파이썬은 True, JS는 소문자 true
const nothing = null;           // null    ← 파이썬의 None
let notAssigned;                // undefined ← 값을 안 넣은 상태

console.log(typeof age);        // number
console.log(typeof nickname);   // string
console.log(typeof isStudent);  // boolean
console.log(typeof notAssigned);// undefined


// [파이썬과의 대응표]
//   Python          JavaScript
//   int, float  →   number   (하나로 통일)
//   str         →   string
//   bool        →   boolean  (True/False → true/false)
//   None        →   null
//   (없음)      →   undefined


// ---------------------------------------------------------------
// 4. null 과 undefined 의 차이
// ---------------------------------------------------------------

// undefined : 값을 아직 안 넣었다 (자바스크립트가 자동으로 붙임)
// null      : 값이 없다고 개발자가 명시적으로 지정했다

let box;              // undefined - 상자를 만들었지만 아직 아무것도 안 넣음
let emptyBox = null;  // null      - "비어있음"을 일부러 넣음

console.log(box);       // undefined
console.log(emptyBox);  // null

// 실무에서는 대부분 null 을 씁니다. undefined 는 주로 "빠졌다"는 신호입니다.


// ---------------------------------------------------------------
// 5. 문자열 다루기
// ---------------------------------------------------------------

const first = "홍";
const last = "길동";

// (1) + 로 이어붙이기
console.log(first + last);            // 홍길동

// (2) 템플릿 리터럴 - 파이썬의 f-string 에 해당합니다. 제일 많이 씁니다.
//     작은따옴표(')가 아니라 백틱(`) 입니다. 키보드 숫자 1 왼쪽에 있습니다.
const fullName = `${first}${last}`;
console.log(`제 이름은 ${fullName}이고, 나이는 ${age}살입니다.`);

// 계산식도 넣을 수 있습니다.
console.log(`내년이면 ${age + 1}살입니다.`);

// 여러 줄도 그대로 됩니다.
const message = `안녕하세요.
줄바꿈이 그대로 유지됩니다.`;
console.log(message);


// (3) 자주 쓰는 문자열 메서드 - 파이썬과 이름이 비슷합니다
const text = "  Hello JavaScript  ";

console.log(text.length);              // 21     (파이썬 len(text))
console.log(text.trim());              // 앞뒤 공백 제거 (파이썬 strip())
console.log(text.toUpperCase());       // 대문자 (파이썬 upper())
console.log(text.toLowerCase());       // 소문자 (파이썬 lower())
console.log(text.includes("Java"));    // true   (파이썬 "Java" in text)
console.log(text.replace("Hello", "Hi"));
console.log("a,b,c".split(","));       // [ 'a', 'b', 'c' ]  (파이썬과 동일)

// [주의] length 는 함수가 아니라 속성입니다. length() 가 아니라 length 입니다.


// ---------------------------------------------------------------
// 6. 형 변환
// ---------------------------------------------------------------

const numStr = "10";

console.log(Number(numStr) + 5);       // 15  (파이썬 int("10"))
console.log(parseInt("10살"));          // 10  숫자 부분만 뽑음
console.log(parseFloat("3.14가지"));    // 3.14
console.log(String(100) + "점");        // "100점" (파이썬 str())

// [함정] + 는 문자열이 하나라도 있으면 이어붙이기가 됩니다.
console.log("10" + 5);   // "105"   ← 조심!
console.log("10" - 5);   //  5      ← -, *, / 는 숫자로 바꿔서 계산

// 그래서 사용자 입력값(항상 문자열)은 반드시 Number() 로 바꿔서 씁니다.


// ---------------------------------------------------------------
// 연습 문제
// ---------------------------------------------------------------

// 1. 자기 이름, 나이, 전공을 const 변수로 만들고
//    템플릿 리터럴을 이용해 "OOO는 20살이고 ITM 전공입니다." 를 출력하세요.

// 2. const 로 선언한 변수에 새 값을 넣어 보고 어떤 에러가 나는지 확인하세요.

// 3. "  SeoulTech  " 라는 문자열에서 공백을 지우고 모두 소문자로 바꿔 출력하세요.

// 4. "3" 과 4 를 더했을 때 7 이 나오도록 코드를 작성하세요.

// 5. 다음 코드의 출력 결과를 예측한 뒤 실행해서 확인하세요.
//      console.log(typeof "10");
//      console.log(typeof (10 + 5));
//      console.log(typeof true);
//      console.log("10" + 5 + 5);
//      console.log(5 + 5 + "10");
