/*
  자바스크립트 - 05. 객체 (Object)

  파이썬의 딕셔너리에 해당합니다.
  자바스크립트에서는 이게 정말 자주 나옵니다. API 응답도 전부 객체입니다.

  실행: node 05_객체.js
*/

// ---------------------------------------------------------------
// 1. 객체 만들기
// ---------------------------------------------------------------

// 파이썬:  {"name": "홍길동", "age": 20}
// 자바스크립트는 키에 따옴표를 안 붙여도 됩니다.

const student = {
  name: "홍길동",
  age: 20,
  major: "ITM",
  isEnrolled: true,
};

console.log(student);


// ---------------------------------------------------------------
// 2. 값 꺼내기 - 점 표기법이 기본
// ---------------------------------------------------------------

console.log(student.name);       // 홍길동   ← 이게 기본
console.log(student["name"]);    // 홍길동   ← 파이썬 방식도 됨

// 언제 대괄호를 쓰나?
//   (1) 키가 변수에 들어있을 때
const key = "age";
console.log(student[key]);       // 20
// console.log(student.key);     // undefined  ← "key" 라는 키를 찾음

//   (2) 키에 띄어쓰기나 하이픈이 있을 때
const config = { "api-key": "abc123" };
console.log(config["api-key"]);

// 없는 키는 에러가 아니라 undefined 입니다. (파이썬은 KeyError)
console.log(student.phone);      // undefined


// ---------------------------------------------------------------
// 3. 값 추가 / 수정 / 삭제
// ---------------------------------------------------------------

student.email = "hong@example.com";   // 없으면 추가
student.age = 21;                      // 있으면 수정
delete student.isEnrolled;             // 삭제 (파이썬 del)

console.log(student);


// ---------------------------------------------------------------
// 4. 키/값 목록 얻기
// ---------------------------------------------------------------

console.log(Object.keys(student));     // [ 'name', 'age', 'major', 'email' ]
console.log(Object.values(student));   // [ '홍길동', 21, 'ITM', 'hong@...' ]
console.log(Object.entries(student));  // [ ['name','홍길동'], ... ]

// 반복하기
for (const [k, v] of Object.entries(student)) {
  console.log(`${k}: ${v}`);
}

// 키가 있는지 확인 (파이썬 "name" in student)
console.log("name" in student);        // true
console.log(student.phone === undefined);  // true


// ---------------------------------------------------------------
// 5. 중첩 구조 - 실무 데이터는 대부분 이 모양입니다
// ---------------------------------------------------------------

// 5일차에 배운 API 응답이 정확히 이 형태로 옵니다.

const classInfo = {
  title: "Python 특강",
  location: {
    building: "프론티어관",
    room: 501,
  },
  students: [
    { name: "홍길동", scores: [90, 85] },
    { name: "김철수", scores: [70, 95] },
  ],
};

console.log(classInfo.location.room);              // 501
console.log(classInfo.students[0].name);           // 홍길동
console.log(classInfo.students[1].scores[1]);      // 95

// 깊이 들어갈 때는 ?. 를 쓰면 안전합니다.
console.log(classInfo.teacher?.name);              // undefined (에러 안 남)
// console.log(classInfo.teacher.name);            // TypeError!


// 학생 이름만 뽑기
const names = classInfo.students.map((s) => s.name);
console.log(names);   // [ '홍길동', '김철수' ]


// ---------------------------------------------------------------
// 6. 구조 분해 할당 (destructuring) - 매우 자주 씁니다
// ---------------------------------------------------------------

// 객체에서 필요한 값만 골라 변수로 꺼내는 문법입니다.

const { name, age } = student;
console.log(name, age);       // 홍길동 21

// 위 한 줄은 아래 두 줄과 같습니다.
//   const name = student.name;
//   const age = student.age;

// 이름을 바꿔서 받기
const { major: mj } = student;
console.log(mj);              // ITM

// 없을 때 기본값
const { phone = "없음" } = student;
console.log(phone);           // 없음

// 배열도 됩니다.
const [first, second] = ["첫째", "둘째"];
console.log(first, second);   // 첫째 둘째


// ---------------------------------------------------------------
// 7. 복사 - 얕은 복사 주의
// ---------------------------------------------------------------

const a = { x: 1 };
const b = a;         // 복사가 아니라 "같은 것을 가리킴"
b.x = 999;
console.log(a.x);    // 999  ← a도 바뀝니다!

// 복사하려면 스프레드 문법을 씁니다.
const c = { ...a };
c.x = 1;
console.log(a.x, c.x);   // 999 1

// 합치기에도 씁니다. 뒤에 오는 것이 이깁니다.
const defaults = { theme: "light", size: 10 };
const userSetting = { size: 14 };
console.log({ ...defaults, ...userSetting });   // { theme: 'light', size: 14 }


// ---------------------------------------------------------------
// 8. JSON - 파이썬에서 배운 그것과 같습니다
// ---------------------------------------------------------------

// 객체 → 문자열
const jsonText = JSON.stringify(student);       // 파이썬 json.dumps()
console.log(jsonText);

// 보기 좋게 (들여쓰기 2칸)
console.log(JSON.stringify(student, null, 2));

// 문자열 → 객체
const parsed = JSON.parse('{"name":"이영희","age":22}');   // json.loads()
console.log(parsed.name);    // 이영희

// API에서 받은 데이터를 다룰 때 이 두 함수를 계속 쓰게 됩니다.


// ---------------------------------------------------------------
// 연습 문제
// ---------------------------------------------------------------

const book = {
  title: "코딩 자율학습",
  author: { name: "김철수", email: "kim@example.com" },
  price: 25000,
  tags: ["프로그래밍", "입문"],
};

// 1. 저자 이름을 출력하세요.

// 2. 첫 번째 태그를 출력하세요.

// 3. 구조 분해 할당으로 title 과 price 를 변수로 꺼내
//    "코딩 자율학습 - 25000원" 형태로 출력하세요.

// 4. book 에 publisher: "골든래빗" 을 추가하세요.

// 5. Object.entries 로 book 의 키와 값을 전부 한 줄씩 출력하세요.

// 6. book 을 보기 좋은 JSON 문자열로 출력하세요.

// 7. 아래 배열에서 가격이 20000원 이상인 책의 제목만 뽑아 배열로 만드세요.
const books = [
  { title: "A", price: 15000 },
  { title: "B", price: 30000 },
  { title: "C", price: 22000 },
];
