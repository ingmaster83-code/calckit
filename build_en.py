"""
CalcKit 영어 버전 자동 생성 스크립트
실행: python build_en.py
결과: en/ 폴더에 영어 버전 HTML 파일 생성
"""

import os, re, shutil, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
EN_DIR = os.path.join(BASE, 'en')
os.makedirs(EN_DIR, exist_ok=True)

SITE_URL = 'https://calckit.wooahouse.com'
SITE_NAME = 'WooaCalc'

# ── 1. 페이지별 메타 번역 ──────────────────────────────────────────────────────
PAGE_META = {
    'index.html': {
        'title':    'Free Online Calculators — Loan, BMI, Date & Unit Tools | WooaCalc',
        'desc':     '25+ free online calculators: loan interest, BMI, salary, D-Day, date, temperature, unit converters and more. No sign-up. Use in browser instantly.',
        'kw':       'free online calculator, loan calculator, BMI calculator, salary calculator, D-Day, date calculator, unit converter, WooaCalc',
        'og_title': 'Free Online Calculators | WooaCalc',
        'og_desc':  '25+ free calculators: loan, BMI, salary, date, unit conversion and more.',
        'h1':       'All Calculations, Free, in One Place',
        'app_name': 'WooaCalc',
    },
    'age.html': {
        'title':    'Age Calculator — International Age, Korean Age & Birthday | WooaCalc',
        'desc':     'Enter your birth date to calculate exact age (international & Korean), days until next birthday, and total days since birth. Free age calculator.',
        'kw':       'age calculator, international age, Korean age, birthday calculator, days since birth, WooaCalc',
        'og_title': 'Age Calculator Free Online | WooaCalc',
        'og_desc':  'Calculate exact age (international & Korean), days to next birthday, and total days since birth.',
        'app_name': 'Age Calculator',
    },
    'apartment-score.html': {
        'title':    'Korean Housing Subscription Score Calculator | WooaCalc',
        'desc':     'Calculate your Korean housing subscription (청약) priority score. Housing-free period (max 32pts), dependents (max 35pts), subscription period (max 17pts). Max 84 points.',
        'kw':       'Korean housing subscription, cheongak score, apartment lottery score, housing priority calculator, WooaCalc',
        'og_title': 'Korean Housing Subscription Score | WooaCalc',
        'og_desc':  'Calculate Korean housing subscription priority score — housing-free period, dependents, subscription period. Max 84 points.',
        'app_name': 'Housing Subscription Score Calculator',
    },
    'area.html': {
        'title':    'Area Unit Converter — m², Pyeong, Hectare, Acre | WooaCalc',
        'desc':     'Convert area units in real time: mm², cm², m², km², pyeong (평), hectare, acre, and more. Free online area unit converter.',
        'kw':       'area converter, m2 to pyeong, hectare, acre, square meter, area unit conversion, WooaCalc',
        'og_title': 'Area Unit Converter Free Online | WooaCalc',
        'og_desc':  'Convert area units in real time: mm², cm², m², km², pyeong, hectare, acre.',
        'app_name': 'Area Unit Converter',
    },
    'bmi.html': {
        'title':    'BMI Calculator — Body Mass Index & Ideal Weight | WooaCalc',
        'desc':     'Enter height and weight to calculate BMI, obesity level, and ideal weight. Visual BMI scale included. Based on WHO and Korean obesity society standards.',
        'kw':       'BMI calculator, body mass index, obesity level, ideal weight, BMI scale, WooaCalc',
        'og_title': 'BMI Calculator Free Online | WooaCalc',
        'og_desc':  'Calculate BMI, obesity level, and ideal weight instantly. Visual BMI scale included.',
        'app_name': 'BMI Calculator',
    },
    'bmr.html': {
        'title':    'BMR Calculator — Basal Metabolic Rate & TDEE | WooaCalc',
        'desc':     'Calculate basal metabolic rate (BMR) and total daily energy expenditure (TDEE) using the Mifflin-St Jeor formula. Supports activity level multipliers.',
        'kw':       'BMR calculator, basal metabolic rate, TDEE, calorie calculator, Mifflin-St Jeor, WooaCalc',
        'og_title': 'BMR & TDEE Calculator Free Online | WooaCalc',
        'og_desc':  'Calculate BMR and TDEE using the Mifflin-St Jeor formula with activity level multipliers.',
        'app_name': 'BMR Calculator',
    },
    'brokerage.html': {
        'title':    'Korean Real Estate Brokerage Fee Calculator | WooaCalc',
        'desc':     'Calculate the maximum legal real estate brokerage fee in Korea for buying, jeonse (전세), and monthly rent. Based on 2021 revised rates. Free calculator.',
        'kw':       'Korean brokerage fee, real estate commission Korea, jeonse fee, brokerage calculator, WooaCalc',
        'og_title': 'Korean Brokerage Fee Calculator | WooaCalc',
        'og_desc':  'Calculate Korean real estate brokerage fees for buying, jeonse, and monthly rent. 2021 revised rates.',
        'app_name': 'Real Estate Brokerage Fee Calculator',
    },
    'calorie.html': {
        'title':    'Calorie Burn Calculator — Calories Burned by Exercise | WooaCalc',
        'desc':     'Calculate calories burned by exercise type, body weight, and duration using MET values. Supports walking, running, cycling, swimming and more. Free.',
        'kw':       'calorie burn calculator, calories burned exercise, MET calculator, exercise calories, WooaCalc',
        'og_title': 'Calorie Burn Calculator Free Online | WooaCalc',
        'og_desc':  'Calculate calories burned by exercise using MET values — walking, running, cycling, swimming and more.',
        'app_name': 'Calorie Burn Calculator',
    },
    'compound-interest.html': {
        'title':    'Compound Interest Calculator — Annual, Monthly & Quarterly | WooaCalc',
        'desc':     'Enter principal, annual interest rate, and investment period to see compound interest results in a yearly table. Supports monthly, quarterly, and annual compounding.',
        'kw':       'compound interest calculator, compound interest table, investment calculator, annual compounding, WooaCalc',
        'og_title': 'Compound Interest Calculator Free | WooaCalc',
        'og_desc':  'Calculate compound interest with yearly table. Supports monthly, quarterly, and annual compounding.',
        'app_name': 'Compound Interest Calculator',
    },
    'data-size.html': {
        'title':    'Data Size Converter — Bit, Byte, KB, MB, GB, TB, PB | WooaCalc',
        'desc':     'Convert data storage units instantly: bit, byte, KB, MB, GB, TB, PB, and more. Real-time conversion as you type. Free online data size converter.',
        'kw':       'data size converter, bit byte KB MB GB TB PB, storage unit converter, WooaCalc',
        'og_title': 'Data Size Converter Free Online | WooaCalc',
        'og_desc':  'Convert data units in real time: bit, byte, KB, MB, GB, TB, PB and more.',
        'app_name': 'Data Size Converter',
    },
    'date-calc.html': {
        'title':    'Date Calculator — Days Between Dates & Add/Subtract Days | WooaCalc',
        'desc':     'Calculate the exact duration between two dates in years, months, and days. Also add or subtract days from any date. Free online date calculator.',
        'kw':       'date calculator, days between dates, add days to date, subtract days, date difference, WooaCalc',
        'og_title': 'Date Calculator Free Online | WooaCalc',
        'og_desc':  'Calculate duration between two dates or add/subtract days from any date.',
        'app_name': 'Date Calculator',
    },
    'dday.html': {
        'title':    'D-Day Calculator — Countdown & Multiple D-Day Tracker | WooaCalc',
        'desc':     'Calculate days remaining until any target date. Save and manage multiple D-Day countdowns locally. Free D-Day calculator with persistent storage.',
        'kw':       'D-Day calculator, countdown calculator, days until, D-Day tracker, WooaCalc',
        'og_title': 'D-Day Calculator Free Online | WooaCalc',
        'og_desc':  'Calculate days remaining until any date. Save and manage multiple D-Day countdowns.',
        'app_name': 'D-Day Calculator',
    },
    'electricity.html': {
        'title':    'Korean Electricity Bill Calculator 2026 — KEPCO Rate | WooaCalc',
        'desc':     'Calculate Korean electricity bill (KEPCO progressive rate) by entering monthly kWh usage. Shows base charge, usage fee, VAT, fund, and total bill. Free.',
        'kw':       'Korean electricity bill calculator, KEPCO rate, kWh calculator, electricity cost Korea, WooaCalc',
        'og_title': 'Korean Electricity Bill Calculator | WooaCalc',
        'og_desc':  'Calculate Korean electricity bill using KEPCO progressive rate — base charge, usage fee, VAT, and total.',
        'app_name': 'Electricity Bill Calculator',
    },
    'exchange-rate.html': {
        'title':    'Currency Converter — KRW, USD, EUR, JPY, CNY, GBP | WooaCalc',
        'desc':     'Convert between Korean Won, US Dollar, Euro, Japanese Yen, Chinese Yuan, and British Pound all at once. Enter any amount in any currency. Free converter.',
        'kw':       'currency converter, KRW USD EUR JPY CNY GBP, exchange rate calculator, won to dollar, WooaCalc',
        'og_title': 'Currency Converter Free Online | WooaCalc',
        'og_desc':  'Convert KRW, USD, EUR, JPY, CNY, and GBP all at once in real time.',
        'app_name': 'Currency Converter',
    },
    'fuel-economy.html': {
        'title':    'Fuel Economy Calculator — km/L, L/100km & Fuel Cost | WooaCalc',
        'desc':     'Calculate fuel economy from distance and fuel used, or estimate fuel costs from efficiency, fuel price, and distance. Supports km/L and L/100km. Free.',
        'kw':       'fuel economy calculator, km/L, L/100km, fuel cost calculator, gas mileage, WooaCalc',
        'og_title': 'Fuel Economy Calculator Free Online | WooaCalc',
        'og_desc':  'Calculate fuel economy (km/L, L/100km) and fuel cost. Free online fuel calculator.',
        'app_name': 'Fuel Economy Calculator',
    },
    'health-insurance.html': {
        'title':    'Korean Health Insurance Calculator 2025 | WooaCalc',
        'desc':     'Calculate Korean national health insurance and long-term care insurance premiums for 2025. Covers employee (salary-based) and regional subscriber methods.',
        'kw':       'Korean health insurance calculator, NHIS premium, health insurance Korea, long-term care insurance, WooaCalc',
        'og_title': 'Korean Health Insurance Calculator 2025 | WooaCalc',
        'og_desc':  'Calculate Korean health insurance and long-term care premiums for employee and regional subscribers. 2025 rates.',
        'app_name': 'Health Insurance Calculator',
    },
    'length.html': {
        'title':    'Length Unit Converter — mm, cm, m, km, inch, ft, mile | WooaCalc',
        'desc':     'Convert length units in real time: mm, cm, m, km, inch, foot, yard, mile, and more. Simple and fast free online length converter.',
        'kw':       'length converter, mm cm m km inch foot mile, length unit conversion, WooaCalc',
        'og_title': 'Length Unit Converter Free Online | WooaCalc',
        'og_desc':  'Convert length units in real time: mm, cm, m, km, inch, foot, yard, mile.',
        'app_name': 'Length Unit Converter',
    },
    'loan-interest.html': {
        'title':    'Loan Calculator — Equal Payment & Equal Principal Method | WooaCalc',
        'desc':     'Calculate monthly payment, total interest, and repayment schedule for loans using equal payment or equal principal methods. Enter loan amount, rate, and term.',
        'kw':       'loan calculator, mortgage calculator, monthly payment, equal payment, equal principal, repayment schedule, WooaCalc',
        'og_title': 'Loan Interest Calculator Free | WooaCalc',
        'og_desc':  'Calculate monthly loan payment and total interest. Equal payment or equal principal method.',
        'app_name': 'Loan Calculator',
    },
    'percentage.html': {
        'title':    'Percentage Calculator — X% of Y, Ratio & Change Rate | WooaCalc',
        'desc':     'Three calculators in one: find X% of Y, find what percent X is of Y, and calculate percentage change between two values. Free online percentage calculator.',
        'kw':       'percentage calculator, percent of, percentage change, ratio calculator, WooaCalc',
        'og_title': 'Percentage Calculator Free Online | WooaCalc',
        'og_desc':  'Find X% of Y, calculate ratios, and percentage change — three calculators in one.',
        'app_name': 'Percentage Calculator',
    },
    'salary.html': {
        'title':    'Korean Salary Calculator 2026 — Take-Home Pay | WooaCalc',
        'desc':     'Calculate monthly take-home pay from annual salary in Korea for 2026, after deducting national pension, health insurance, employment insurance, and income tax.',
        'kw':       'Korean salary calculator, take-home pay, net salary Korea, social insurance deduction, income tax Korea, WooaCalc',
        'og_title': 'Korean Salary Calculator 2026 | WooaCalc',
        'og_desc':  'Calculate monthly take-home pay from annual salary after all Korean deductions. 2026 rates.',
        'app_name': 'Salary Calculator',
    },
    'savings.html': {
        'title':    'Savings Calculator — Maturity Amount & After-Tax Interest | WooaCalc',
        'desc':     'Calculate savings maturity amount and interest (before and after tax) by entering monthly deposit, annual rate, and term. Supports simple and compound interest.',
        'kw':       'savings calculator, maturity amount, after-tax interest, compound savings, monthly deposit calculator, WooaCalc',
        'og_title': 'Savings Calculator Free Online | WooaCalc',
        'og_desc':  'Calculate savings maturity amount and after-tax interest. Simple and compound interest modes.',
        'app_name': 'Savings Calculator',
    },
    'severance.html': {
        'title':    'Korean Severance Pay Calculator — Tenure & Average Wage | WooaCalc',
        'desc':     'Calculate Korean statutory severance pay by entering employment start date, end date, and last 3 months\' salary. Based on daily average wage formula.',
        'kw':       'Korean severance pay calculator, retirement pay Korea, severance calculation, average wage, WooaCalc',
        'og_title': 'Korean Severance Pay Calculator | WooaCalc',
        'og_desc':  'Calculate Korean severance pay from employment dates and last 3 months salary.',
        'app_name': 'Severance Pay Calculator',
    },
    'temperature.html': {
        'title':    'Temperature Converter — Celsius, Fahrenheit & Kelvin | WooaCalc',
        'desc':     'Convert temperatures in real time between Celsius (°C), Fahrenheit (°F), and Kelvin (K). Instant conversion as you type. Free online temperature converter.',
        'kw':       'temperature converter, Celsius Fahrenheit Kelvin, °C to °F, temperature conversion, WooaCalc',
        'og_title': 'Temperature Converter Free Online | WooaCalc',
        'og_desc':  'Convert temperatures between Celsius, Fahrenheit, and Kelvin in real time.',
        'app_name': 'Temperature Converter',
    },
    'vat.html': {
        'title':    'VAT Calculator — Supply Price, 10% Tax & Total | WooaCalc',
        'desc':     'Auto-calculate VAT (10%) and total from supply price, or reverse-calculate supply price and VAT from total amount. Free Korean VAT calculator.',
        'kw':       'VAT calculator, value added tax, supply price, tax calculation Korea, reverse VAT, WooaCalc',
        'og_title': 'VAT Calculator Free Online | WooaCalc',
        'og_desc':  'Calculate VAT (10%) and total from supply price, or reverse-calculate from total. Free.',
        'app_name': 'VAT Calculator',
    },
    'weight.html': {
        'title':    'Weight Unit Converter — mg, g, kg, Ton, Ounce, Pound | WooaCalc',
        'desc':     'Convert weight units in real time: mg, g, kg, metric ton, ounce (oz), pound (lb), and more. Free online weight unit converter.',
        'kw':       'weight converter, mg g kg ton ounce pound, weight unit conversion, WooaCalc',
        'og_title': 'Weight Unit Converter Free Online | WooaCalc',
        'og_desc':  'Convert weight units in real time: mg, g, kg, ton, ounce (oz), pound (lb).',
        'app_name': 'Weight Unit Converter',
    },
}

# ── 2. 공통 문자열 번역 ────────────────────────────────────────────────────────
COMMON = [
    # ── nav & aria ──
    ('aria-label="메뉴"', 'aria-label="Menu"'),

    # ── nav links ──
    ('>💰 금융</a>', '>💰 Finance</a>'),
    ('>🏥 건강</a>', '>🏥 Health</a>'),
    ('>📅 날짜</a>', '>📅 Date</a>'),
    ('>📐 단위변환</a>', '>📐 Unit Converter</a>'),
    ('>🏠 생활</a>', '>🏠 Life</a>'),

    # ── index hero ──
    ('<h1>모든 계산, 한 곳에서 무료로</h1>', '<h1>All Calculations, Free, in One Place</h1>'),
    ('대출이자·연봉·BMI·단위변환·날짜 계산까지 20가지 계산기 100% 무료. 회원가입 없이 브라우저에서 바로 사용', '25+ free calculators: loan interest, salary, BMI, unit conversion, dates, and more. No sign-up. Use instantly in your browser.'),
    ('✅ 100% 무료', '✅ 100% Free'),
    ('🔒 데이터 수집 없음', '🔒 No Data Collected'),
    ('📱 모바일 최적화', '📱 Mobile Optimized'),
    ('⚡ 즉시 계산', '⚡ Instant Calculation'),

    # ── index category headings ──
    ('💰 금융 계산기', '💰 Finance Calculators'),
    ('🏥 건강 계산기', '🏥 Health Calculators'),
    ('📅 날짜 계산기', '📅 Date Calculators'),
    ('📐 단위 변환', '📐 Unit Converters'),
    ('🏠 생활 계산기', '🏠 Life Calculators'),

    # ── index tool card text ──
    ('<h3>대출이자 계산기</h3>', '<h3>Loan Interest Calculator</h3>'),
    ('<p>원리금균등·원금균등 상환 방식, 월납입금·총이자 계산</p>', '<p>Equal payment & equal principal methods, monthly payment & total interest</p>'),
    ('<h3>적금이자 계산기</h3>', '<h3>Savings Calculator</h3>'),
    ('<p>단리·복리, 만기수령액·세후이자 계산</p>', '<p>Simple & compound interest, maturity amount & after-tax interest</p>'),
    ('<h3>연봉 실수령액 계산기</h3>', '<h3>Salary Take-Home Calculator</h3>'),
    ('<p>4대보험·소득세 공제 후 월 실수령액</p>', '<p>Monthly take-home after insurance & income tax deductions</p>'),
    ('<h3>퇴직금 계산기</h3>', '<h3>Severance Pay Calculator</h3>'),
    ('<p>근속연수·평균임금 기반 퇴직금 산출</p>', '<p>Statutory severance based on tenure and average wage</p>'),
    ('<h3>부가세 계산기</h3>', '<h3>VAT Calculator</h3>'),
    ('<p>공급가액·부가세·합계 자동 계산, 역산 지원</p>', '<p>Auto-calculate supply price, VAT (10%), and total; reverse calculation supported</p>'),
    ('<h3>환율 계산기</h3>', '<h3>Currency Converter</h3>'),
    ('<p>KRW·USD·EUR·JPY·CNY·GBP 환율 계산</p>', '<p>Convert KRW, USD, EUR, JPY, CNY, GBP all at once</p>'),
    ('<h3>건강보험료 계산기</h3>', '<h3>Health Insurance Calculator</h3>'),
    ('<p>2025년 기준 직장·지역 건강보험료 본인부담금 계산</p>', '<p>2025 employee & regional health insurance premium calculation</p>'),
    ('<h3>복리 계산기</h3>', '<h3>Compound Interest Calculator</h3>'),
    ('<p>원금·연이율·기간 복리 이자, 연도별 원리금 표</p>', '<p>Principal, annual rate, period; compound interest with yearly table</p>'),
    ('<h3>BMI 계산기</h3>', '<h3>BMI Calculator</h3>'),
    ('<p>체질량지수, 비만도 판정, 표준체중</p>', '<p>Body mass index, obesity level, ideal weight</p>'),
    ('<h3>기초대사량 계산기</h3>', '<h3>BMR Calculator</h3>'),
    ('<p>Harris-Benedict 공식, 활동계수 TDEE</p>', '<p>Mifflin-St Jeor formula, activity-level TDEE</p>'),
    ('<h3>칼로리 소모 계산기</h3>', '<h3>Calorie Burn Calculator</h3>'),
    ('<p>운동종류별 MET 값 기반 소모 칼로리</p>', '<p>Calories burned by exercise type using MET values</p>'),
    ('<h3>D-Day 계산기</h3>', '<h3>D-Day Calculator</h3>'),
    ('<p>특정 날짜까지 남은 일수, 지난 일수</p>', '<p>Days remaining or elapsed until a target date</p>'),
    ('<h3>날짜 계산기</h3>', '<h3>Date Calculator</h3>'),
    ('<p>두 날짜 사이 기간(년/월/일), 특정일 +N일 계산</p>', '<p>Duration between dates (years/months/days), add N days to a date</p>'),
    ('<h3>나이 계산기</h3>', '<h3>Age Calculator</h3>'),
    ('<p>만나이·한국식나이, 다음 생일까지 일수</p>', '<p>International age, Korean age, days to next birthday</p>'),
    ('<h3>길이 변환</h3>', '<h3>Length Converter</h3>'),
    ('<p>mm·cm·m·km·inch·ft·yard·mile</p>', '<p>mm, cm, m, km, inch, ft, yard, mile</p>'),
    ('<h3>무게 변환</h3>', '<h3>Weight Converter</h3>'),
    ('<p>mg·g·kg·ton·oz·lb</p>', '<p>mg, g, kg, ton, oz, lb</p>'),
    ('<h3>온도 변환</h3>', '<h3>Temperature Converter</h3>'),
    ('<p>°C·°F·K 실시간 변환</p>', '<p>Real-time °C, °F, K conversion</p>'),
    ('<h3>넓이 변환</h3>', '<h3>Area Converter</h3>'),
    ('<p>mm²·cm²·m²·km²·평·헥타르</p>', '<p>mm², cm², m², km², pyeong, hectare</p>'),
    ('<h3>데이터 용량 변환</h3>', '<h3>Data Size Converter</h3>'),
    ('<p>bit·byte·KB·MB·GB·TB·PB</p>', '<p>bit, byte, KB, MB, GB, TB, PB</p>'),
    ('<h3>백분율 계산기</h3>', '<h3>Percentage Calculator</h3>'),
    ('<p>X의 Y%, X가 Y의 몇%, 증감률</p>', '<p>X% of Y, what % is X of Y, percentage change</p>'),
    ('<h3>연비 계산기</h3>', '<h3>Fuel Economy Calculator</h3>'),
    ('<p>km/L, L/100km, 주유비 계산</p>', '<p>km/L, L/100km, and fuel cost calculation</p>'),
    ('<h3>전기요금 계산기</h3>', '<h3>Electricity Bill Calculator</h3>'),
    ('<p>월사용량(kWh) 기반 한국전력 누진요금 계산</p>', '<p>Monthly kWh-based KEPCO progressive rate calculation</p>'),
    ('<h3>중개수수료 계산기</h3>', '<h3>Brokerage Fee Calculator</h3>'),
    ('<p>매매·전세·월세 유형별 법정 최대 수수료</p>', '<p>Maximum legal brokerage fee by transaction type (buy/jeonse/rent)</p>'),
    ('<h3>청약 가점 계산기</h3>', '<h3>Housing Subscription Score</h3>'),
    ('<p>무주택기간·부양가족·청약통장 가입기간 가점 합산</p>', '<p>Housing-free period, dependents, subscription period score sum</p>'),

    # ── index features section ──
    ('<h3>100% 무료</h3>', '<h3>100% Free</h3>'),
    ('<p>모든 계산기를 무료로 제한 없이 사용하세요</p>', '<p>Use all calculators for free with no restrictions</p>'),
    ('<h3>개인정보 안전</h3>', '<h3>Privacy Safe</h3>'),
    ('<p>입력한 데이터는 브라우저에서만 처리, 서버 전송 없음</p>', '<p>All data processed locally in your browser — never sent to any server</p>'),
    ('<h3>모바일 최적화</h3>', '<h3>Mobile Optimized</h3>'),
    ('<p>스마트폰·태블릿에서도 편리하게 사용</p>', '<p>Works great on smartphones and tablets</p>'),
    ('<h3>즉시 계산</h3>', '<h3>Instant Results</h3>'),
    ('<p>회원가입·설치 없이 브라우저에서 바로 계산</p>', '<p>No sign-up or installation needed — calculate right in your browser</p>'),

    # ── index footer col heading ──
    ('<h4>계산기</h4>', '<h4>Calculators</h4>'),

    # ── common tool page elements ──
    ('>계산하기<', '>Calculate<'),
    ('>초기화<', '>Reset<'),
    ('>복사<', '>Copy<'),

    # ── breadcrumb home ──
    ('>홈<', '>Home<'),

    # ── free badge ──
    ('>무료<', '>Free<'),

    # ── gender ──
    ('> 남성<', '> Male<'),
    ('> 여성<', '> Female<'),
    ('<label>성별</label>', '<label>Gender</label>'),

    # ── BMI page ──
    ('<label for="height">키 (cm)</label>', '<label for="height">Height (cm)</label>'),
    ('<label for="weight">몸무게 (kg)</label>', '<label for="weight">Weight (kg)</label>'),
    ('placeholder="예: 175"', 'placeholder="e.g. 175"'),
    ('placeholder="예: 70"', 'placeholder="e.g. 70"'),
    ('<h1>BMI 계산기</h1>', '<h1>BMI Calculator</h1>'),
    ('<p>체질량지수(BMI) 계산, 비만도 판정, 표준체중 확인</p>', '<p>Calculate BMI, obesity level, and ideal weight</p>'),
    ('>건강 계산기<', '>Health Calculators<'),
    ('>BMI 계산기<', '>BMI Calculator<'),
    ('<span class="label">표준체중 (Broca)</span>', '<span class="label">Ideal Weight (Broca)</span>'),
    ('<span class="label">비만도</span>', '<span class="label">Obesity Level</span>'),
    ('<span class="label">정상 체중 범위</span>', '<span class="label">Normal Weight Range</span>'),
    # ── BMI classification (longer strings FIRST to avoid partial replacement) ──
    ('<h3>💡 BMI 판정 기준 (대한비만학회)</h3>', '<h3>💡 BMI Classification (Korean Obesity Society)</h3>'),
    ('<li>18.5 미만: 저체중</li>', '<li>Under 18.5: Underweight</li>'),
    ('<li>18.5 ~ 22.9: 정상</li>', '<li>18.5 – 22.9: Normal</li>'),
    ('<li>23.0 ~ 24.9: 과체중</li>', '<li>23.0 – 24.9: Overweight</li>'),
    ('<li>25.0 ~ 29.9: 비만</li>', '<li>25.0 – 29.9: Obese</li>'),
    ('<li>30.0 이상: 고도비만</li>', '<li>30.0 and above: Severely Obese</li>'),
    ('<span>고도비만</span>', '<span>Severely Obese</span>'),
    ('<span>비만</span>', '<span>Obese</span>'),
    ('<span>저체중</span>', '<span>Underweight</span>'),
    ('<span>정상</span>', '<span>Normal</span>'),
    ('<span>과체중</span>', '<span>Overweight</span>'),
    ('고도비만', 'Severely Obese'),
    ('저체중', 'Underweight'),
    ('과체중', 'Overweight'),
    ('비만', 'Obese'),
    # NOTE: '정상' bare word is not added — it would corrupt "BMI 정상 범위" etc.
    # '정상' → 'Normal' is handled by context-specific entries above.
    ("alert('키와 몸무게를 입력해주세요.');", "alert('Please enter your height and weight.');"),

    # ── BMR page ──
    ('<h1>기초대사량 계산기</h1>', '<h1>BMR Calculator</h1>'),
    ('<p>BMR(기초대사량)과 TDEE(총 에너지 소비량)를 계산합니다</p>', '<p>Calculate BMR (Basal Metabolic Rate) and TDEE (Total Daily Energy Expenditure)</p>'),
    ('>기초대사량 계산기<', '>BMR Calculator<'),
    ('<label for="age">나이 (세)</label>', '<label for="age">Age (years)</label>'),
    ('placeholder="예: 30"', 'placeholder="e.g. 30"'),
    ('<label for="activity">활동 수준</label>', '<label for="activity">Activity Level</label>'),
    ('>비활동적 (운동 안 함)<', '>Sedentary (little or no exercise)<'),
    ('>가벼운 활동 (주 1~3회)<', '>Light activity (1–3 days/week)<'),
    ('>보통 활동 (주 3~5회)<', '>Moderate activity (3–5 days/week)<'),
    ('>활발한 활동 (주 6~7회)<', '>Active (6–7 days/week)<'),
    ('>매우 활발 (육체노동/운동선수)<', '>Very active (physical labor / athlete)<'),
    ('<div class="result-label">기초대사량 (BMR)</div>', '<div class="result-label">Basal Metabolic Rate (BMR)</div>'),
    ('<span class="label">TDEE (총 에너지 소비량)</span>', '<span class="label">TDEE (Total Daily Energy Expenditure)</span>'),
    ('<span class="label">체중 감량 (-500kcal)</span>', '<span class="label">Weight Loss (-500 kcal/day)</span>'),
    ('<span class="label">체중 유지</span>', '<span class="label">Maintenance</span>'),
    ('<span class="label">체중 증가 (+500kcal)</span>', '<span class="label">Weight Gain (+500 kcal/day)</span>'),
    ('<h3>💡 기초대사량 참고사항</h3>', '<h3>💡 BMR Notes</h3>'),
    ('<li><strong>BMR:</strong> 아무것도 하지 않아도 생명 유지에 필요한 최소 칼로리</li>', '<li><strong>BMR:</strong> Minimum calories needed to sustain life at complete rest</li>'),
    ('<li><strong>TDEE:</strong> BMR × 활동계수, 실제 하루에 소비하는 총 칼로리</li>', '<li><strong>TDEE:</strong> BMR × activity factor — total calories burned per day</li>'),
    ('<li>체중 감량은 하루 500kcal 적게 섭취 시 주당 약 0.5kg 감량 효과</li>', '<li>Eating 500 kcal less per day results in ~0.5 kg weight loss per week</li>'),
    ('<li>Mifflin-St Jeor 공식 사용 (가장 정확하다고 알려진 공식)</li>', '<li>Uses Mifflin-St Jeor formula (widely considered the most accurate)</li>'),
    ("alert('모든 값을 입력해주세요.');", "alert('Please fill in all fields.');"),

    # ── Calorie page ──
    ('<h1>칼로리 소모 계산기</h1>', '<h1>Calorie Burn Calculator</h1>'),
    ('<p>운동 종류별 MET 값 기반 소모 칼로리를 계산합니다</p>', '<p>Calculate calories burned by exercise using MET values</p>'),
    ('>칼로리 소모 계산기<', '>Calorie Burn Calculator<'),
    ('<label for="exercise">운동 종류</label>', '<label for="exercise">Exercise Type</label>'),
    ('<label for="duration">운동 시간 (분)</label>', '<label for="duration">Duration (minutes)</label>'),
    ('placeholder="예: 60"', 'placeholder="e.g. 60"'),
    ('>걷기 (보통 속도) - MET 3.5<', '>Walking (moderate pace) — MET 3.5<'),
    ('>빠르게 걷기 - MET 5.0<', '>Brisk Walking — MET 5.0<'),
    ('>가볍게 달리기 - MET 7.0<', '>Light Running — MET 7.0<'),
    ('>달리기 - MET 10.0<', '>Running — MET 10.0<'),
    ('>자전거 (보통) - MET 6.0<', '>Cycling (moderate) — MET 6.0<'),
    ('>수영 - MET 7.0<', '>Swimming — MET 7.0<'),
    ('>등산 - MET 7.5<', '>Hiking — MET 7.5<'),
    ('>줄넘기 - MET 11.0<', '>Jump Rope — MET 11.0<'),
    ('>헬스 (웨이트) - MET 5.0<', '>Weight Training — MET 5.0<'),
    ('>요가 - MET 3.0<', '>Yoga — MET 3.0<'),
    ('>농구 - MET 8.0<', '>Basketball — MET 8.0<'),
    ('>축구 - MET 10.0<', '>Soccer — MET 10.0<'),
    ('<div class="result-label">소모 칼로리</div>', '<div class="result-label">Calories Burned</div>'),
    ('<span class="label">MET 값</span>', '<span class="label">MET Value</span>'),
    ('<span class="label">운동 시간</span>', '<span class="label">Exercise Duration</span>'),
    ('<span class="label">시간당 소모</span>', '<span class="label">Calories per Hour</span>'),
    ('<h3>💡 칼로리 소모 참고</h3>', '<h3>💡 Calorie Burn Notes</h3>'),
    ('<li><strong>MET (Metabolic Equivalent of Task):</strong> 안정 시 대사율 대비 운동 강도 배수</li>', '<li><strong>MET (Metabolic Equivalent of Task):</strong> Ratio of exercise energy use to resting metabolic rate</li>'),
    ('<li>계산 공식: 소모 칼로리 = MET x 체중(kg) x 시간(h)</li>', '<li>Formula: Calories burned = MET × weight (kg) × time (h)</li>'),
    ('<li>실제 소모 칼로리는 운동 강도, 체력, 환경에 따라 다를 수 있습니다</li>', '<li>Actual calories burned may vary by exercise intensity, fitness level, and environment</li>'),
    ("alert('몸무게와 운동 시간을 입력해주세요.');", "alert('Please enter weight and exercise duration.');"),

    # ── Loan page ──
    ('<h1>대출이자 계산기</h1>', '<h1>Loan Interest Calculator</h1>'),
    ('<p>원리금균등·원금균등 상환 방식별 월납입금과 총이자를 계산합니다</p>', '<p>Calculate monthly payment and total interest by repayment method</p>'),
    ('>대출이자 계산기<', '>Loan Interest Calculator<'),
    ('>금융 계산기<', '>Finance Calculators<'),
    ('<label for="loanAmount">대출금액 (만원)</label>', '<label for="loanAmount">Loan Amount (10,000 KRW units)</label>'),
    ('placeholder="예: 10000"', 'placeholder="e.g. 10000"'),
    ('<label for="rate">연이율 (%)</label>', '<label for="rate">Annual Interest Rate (%)</label>'),
    ('placeholder="예: 4.5"', 'placeholder="e.g. 4.5"'),
    ('<label for="months">대출기간 (개월)</label>', '<label for="months">Loan Term (months)</label>'),
    ('placeholder="예: 360"', 'placeholder="e.g. 360"'),
    ('<label>상환방식</label>', '<label>Repayment Method</label>'),
    ('> 원리금균등<', '> Equal Payment<'),
    ('> 원금균등<', '> Equal Principal<'),
    ("document.getElementById('resMonthlyLabel').textContent='월 납입금 (매월 동일)';", "document.getElementById('resMonthlyLabel').textContent='Monthly Payment (fixed)';"),
    ("document.getElementById('resMonthlyLabel').textContent='월 납입금 (첫 달)';", "document.getElementById('resMonthlyLabel').textContent='Monthly Payment (first month)';"),
    ('<div class="result-label" id="resMonthlyLabel">월 납입금 (첫 달)</div>', '<div class="result-label" id="resMonthlyLabel">Monthly Payment (first month)</div>'),
    ('<span class="label">총 납입금액</span>', '<span class="label">Total Amount Paid</span>'),
    ('<span class="label">총 이자금액</span>', '<span class="label">Total Interest</span>'),
    ('<span class="label">이자 비율</span>', '<span class="label">Interest Ratio</span>'),
    ('<h3>상환 스케줄</h3>', '<h3>Repayment Schedule</h3>'),
    ('<th>회차</th>', '<th>Month</th>'),
    ('<th>납입금</th>', '<th>Payment</th>'),
    ('<th>원금</th>', '<th>Principal</th>'),
    ('<th>이자</th>', '<th>Interest</th>'),
    ('<th>잔액</th>', '<th>Balance</th>'),
    ('<h3>💡 대출이자 계산 팁</h3>', '<h3>💡 Loan Calculation Tips</h3>'),
    ('<li><strong>원리금균등:</strong> 매월 같은 금액을 납입. 초기 이자 비중이 높고 점차 원금 비중 증가</li>', '<li><strong>Equal Payment:</strong> Same amount every month. Higher interest portion early, increasing principal over time</li>'),
    ('<li><strong>원금균등:</strong> 매월 같은 원금 + 줄어드는 이자. 초기 납입금이 크지만 총이자는 적음</li>', '<li><strong>Equal Principal:</strong> Fixed principal + decreasing interest. Higher initial payment but less total interest</li>'),
    ('<li>같은 조건이라면 원금균등이 총이자가 더 적습니다</li>', '<li>Under the same conditions, equal principal results in less total interest</li>'),
    ("alert('모든 값을 입력해주세요.');", "alert('Please fill in all fields.');"),

    # ── Age page ──
    ('<h1>나이 계산기 2026</h1>', '<h1>Age Calculator</h1>'),
    ('<p>만나이, 한국식 나이, 다음 생일까지 남은 일수를 계산합니다</p>', '<p>Calculate international age, Korean age, and days to next birthday</p>'),
    ('>나이 계산기<', '>Age Calculator<'),
    ('>날짜 계산기<', '>Date Calculators<'),
    ('<label for="birth">생년월일</label>', '<label for="birth">Date of Birth</label>'),
    ('<label for="baseDate">기준일</label>', '<label for="baseDate">Reference Date</label>'),
    ('<div class="result-label">만 나이</div>', '<div class="result-label">International Age</div>'),
    ('<span class="label">한국식 나이</span>', '<span class="label">Korean Age</span>'),
    ('<span class="label">태어난 지</span>', '<span class="label">Days Since Birth</span>'),
    ('<span class="label">다음 생일까지</span>', '<span class="label">Days to Next Birthday</span>'),
    ('<span class="label">띠</span>', '<span class="label">Zodiac Animal</span>'),
    ("alert('생년월일을 선택해주세요.');", "alert('Please select your date of birth.');"),
    ("'만 '+age+'세'", "'Age: '+age"),
    ("korAge+'세'", "korAge+' years (Korean)'"),
    ("totalDays.toLocaleString('ko-KR')+'일'", "totalDays.toLocaleString()+ ' days'"),
    ("daysToNext+'일 남음'", "daysToNext+' days remaining'"),
    ("zodiac+'띠'", "zodiac+' year'"),

    # ── Date calc page ──
    ('>날짜 계산기<', '>Date Calculators<'),
    ('<h1>날짜 계산기</h1>', '<h1>Date Calculator</h1>'),

    # ── D-Day page ──
    ('<h1>D-Day 계산기</h1>', '<h1>D-Day Calculator</h1>'),
    ('>D-Day 계산기<', '>D-Day Calculator<'),

    # ── Savings page ──
    ('<h1>적금이자 계산기</h1>', '<h1>Savings Calculator</h1>'),
    ('>적금이자 계산기<', '>Savings Calculator<'),
    ('<label for="deposit">월 납입액 (만원)</label>', '<label for="deposit">Monthly Deposit (10,000 KRW units)</label>'),
    ('<label for="period">기간 (개월)</label>', '<label for="period">Term (months)</label>'),
    ('<label>이자 유형</label>', '<label>Interest Type</label>'),
    ('> 단리<', '> Simple Interest<'),
    ('> 복리<', '> Compound Interest<'),
    ('<div class="result-label">만기 수령액</div>', '<div class="result-label">Maturity Amount</div>'),
    ('<span class="label">원금 합계</span>', '<span class="label">Total Principal</span>'),
    ('<span class="label">세전 이자</span>', '<span class="label">Pre-tax Interest</span>'),
    ('<span class="label">이자 소득세 (15.4%)</span>', '<span class="label">Interest Tax (15.4%)</span>'),
    ('<span class="label">세후 이자</span>', '<span class="label">After-tax Interest</span>'),
    ('<span class="label">세후 수령액</span>', '<span class="label">After-tax Maturity Amount</span>'),

    # ── Salary page ──
    ('<h1>연봉 실수령액 계산기 2026</h1>', '<h1>Salary Take-Home Calculator 2026</h1>'),
    ('<p>4대보험·소득세 공제 후 실제 월급을 계산합니다</p>', '<p>Calculate actual monthly take-home pay after all Korean deductions</p>'),
    ('>연봉 실수령액 계산기<', '>Salary Calculator<'),
    ('<label for="salary">연봉 (만원)</label>', '<label for="salary">Annual Salary (10,000 KRW units)</label>'),
    ('placeholder="예: 5000"', 'placeholder="e.g. 5000"'),
    ('<label for="dependents">부양가족 수 (본인 포함)</label>', '<label for="dependents">Dependents (including self)</label>'),
    ('<label for="taxfree">비과세액 (만원/월)</label>', '<label for="taxfree">Non-taxable Amount (10,000 KRW/mo)</label>'),
    ('>1명<', '>1 person<'),
    ('>2명<', '>2 persons<'),
    ('>3명<', '>3 persons<'),
    ('>4명<', '>4 persons<'),
    ('>5명<', '>5 persons<'),
    ('>6명<', '>6 persons<'),
    ('>7명<', '>7 persons<'),
    ('>8명<', '>8 persons<'),
    ('>9명<', '>9 persons<'),
    ('>10명<', '>10 persons<'),
    ('<div class="result-label">월 실수령액</div>', '<div class="result-label">Monthly Take-Home Pay</div>'),
    ('<span class="label">월 급여 (세전)</span>', '<span class="label">Monthly Gross Salary</span>'),
    ('<span class="label">국민연금 (4.5%)</span>', '<span class="label">National Pension (4.5%)</span>'),
    ('<span class="label">건강보험 (3.545%)</span>', '<span class="label">Health Insurance (3.545%)</span>'),
    ('<span class="label">장기요양 (건강×12.95%)</span>', '<span class="label">Long-term Care (Health×12.95%)</span>'),
    ('<span class="label">고용보험 (0.9%)</span>', '<span class="label">Employment Insurance (0.9%)</span>'),
    ('<span class="label">소득세</span>', '<span class="label">Income Tax</span>'),
    ('<span class="label">지방소득세 (소득세×10%)</span>', '<span class="label">Local Income Tax (Income Tax×10%)</span>'),
    ('<span class="label">공제 합계</span>', '<span class="label">Total Deductions</span>'),
    ('<h3>💡 연봉 실수령액 팁</h3>', '<h3>💡 Salary Tips</h3>'),
    ('<li>비과세액(식대)은 2026년 기준 월 20만원까지 비과세 적용</li>', '<li>Non-taxable allowance (meal): up to KRW 200,000/month as of 2026</li>'),
    ('<li>국민연금은 월 소득 590만원 상한 적용 (2026년 기준 근사치)</li>', '<li>National pension capped at KRW 5.9M monthly income (approx. 2026)</li>'),
    ('<li>소득세는 간이세액표 근사치로 실제와 다소 차이가 있을 수 있습니다</li>', '<li>Income tax is approximated from the simplified withholding table; actual amounts may differ</li>'),
    ('<li>정확한 세액은 국세청 간이세액표를 참고하세요</li>', '<li>For exact figures, refer to the NTS simplified withholding tax table</li>'),
    ("alert('연봉을 입력해주세요.');", "alert('Please enter your annual salary.');"),

    # ── Severance page ──
    ('<h1>퇴직금 계산기</h1>', '<h1>Severance Pay Calculator</h1>'),
    ('>퇴직금 계산기<', '>Severance Pay Calculator<'),
    ('<label for="startDate">입사일</label>', '<label for="startDate">Employment Start Date</label>'),
    ('<label for="endDate">퇴사일</label>', '<label for="endDate">Employment End Date</label>'),
    ('<label for="m1">최근 3개월 급여 합계 (원)</label>', '<label for="m1">Total Salary Last 3 Months (KRW)</label>'),
    ('<div class="result-label">예상 퇴직금</div>', '<div class="result-label">Estimated Severance Pay</div>'),
    ('<span class="label">근속 기간</span>', '<span class="label">Tenure</span>'),
    ('<span class="label">1일 평균임금</span>', '<span class="label">Daily Average Wage</span>'),
    ('<span class="label">계산 기준</span>', '<span class="label">Formula Basis</span>'),
    ("alert('입사일과 퇴사일을 선택하고 급여를 입력해주세요.');", "alert('Please select employment dates and enter salary.');"),

    # ── VAT page ──
    ('<h1>부가세 계산기</h1>', '<h1>VAT Calculator</h1>'),
    ('>부가세 계산기<', '>VAT Calculator<'),
    ('<label for="supply">공급가액 (원)</label>', '<label for="supply">Supply Price (KRW)</label>'),
    ('<label for="total">합계금액 (원)</label>', '<label for="total">Total Amount (KRW)</label>'),
    ('<div class="result-label">부가세 (10%)</div>', '<div class="result-label">VAT (10%)</div>'),
    ('<span class="label">공급가액</span>', '<span class="label">Supply Price</span>'),
    ('<span class="label">부가세</span>', '<span class="label">VAT</span>'),
    ('<span class="label">합계금액</span>', '<span class="label">Total Amount</span>'),
    ('>공급가액 → 부가세·합계<', '>Supply Price → VAT & Total<'),
    ('>합계 → 공급가액·부가세<', '>Total → Supply Price & VAT<'),

    # ── Exchange rate page ──
    ('<h1>환율 계산기</h1>', '<h1>Currency Converter</h1>'),
    ('>환율 계산기<', '>Currency Converter<'),
    ('<p>금액을 입력하면 주요 통화로 실시간 환율 변환합니다</p>', '<p>Enter any amount to convert between major currencies in real time</p>'),
    ('환율 기준', 'Exchange Rate Basis'),

    # ── Health insurance page ──
    ('<h1>건강보험료 계산기 2025</h1>', '<h1>Health Insurance Calculator 2025</h1>'),
    ('<p>2025년 기준 건강보험료와 장기요양보험료 본인부담금을 계산합니다</p>', '<p>Calculate 2025 health insurance and long-term care insurance premiums</p>'),
    ('>건강보험료 계산기<', '>Health Insurance Calculator<'),
    ('<label>가입자 유형</label>', '<label>Subscriber Type</label>'),
    ('> 직장가입자', '> Employee Subscriber'),
    ('> 지역가입자', '> Regional Subscriber'),
    ('<label for="monthlyPay">월 보수월액 (원)</label>', '<label for="monthlyPay">Monthly Salary (KRW)</label>'),
    ('placeholder="예: 3000000"', 'placeholder="e.g. 3000000"'),
    ('직장가입자: 보수월액 / 지역가입자: 소득월액 기준', 'Employee: monthly salary / Regional: monthly income basis'),
    ('<span class="label">건강보험료 전체 (7.09%)</span>', '<span class="label">Total Health Insurance (7.09%)</span>'),
    ('<span class="label">본인부담 건강보험료 (3.545%)</span>', '<span class="label">Employee Share of Health Insurance (3.545%)</span>'),
    ('<span class="label">장기요양보험료 전체 (건강보험×12.95%)</span>', '<span class="label">Total Long-term Care (Health×12.95%)</span>'),
    ('<span class="label">본인부담 장기요양보험료</span>', '<span class="label">Employee Share of Long-term Care</span>'),
    ('<span class="label">본인부담 합계</span>', '<span class="label">Total Employee Share</span>'),
    ('⚠️ 2025년 기준 요율이며, 변경될 수 있습니다. 정확한 보험료는 국민건강보험공단을 통해 확인하세요.', '⚠️ Based on 2025 rates; subject to change. For exact figures, contact the National Health Insurance Service (NHIS).'),
    ('<h3>💡 건강보험료 계산 안내 (2025년 기준)</h3>', '<h3>💡 Health Insurance Guide (2025 Rates)</h3>'),
    ('<li><strong>직장가입자 건강보험료:</strong> 보수월액 × 7.09% (노사 각 50% 부담)</li>', '<li><strong>Employee health insurance:</strong> Monthly salary × 7.09% (employer and employee each pay 50%)</li>'),
    ('<li><strong>본인부담:</strong> 보수월액 × 3.545%</li>', '<li><strong>Employee share:</strong> Monthly salary × 3.545%</li>'),
    ('<li><strong>장기요양보험료:</strong> 건강보험료 × 12.95% (노사 각 50% 부담)</li>', '<li><strong>Long-term care:</strong> Health insurance premium × 12.95% (employer and employee each pay 50%)</li>'),
    ('<li>지역가입자는 소득·재산·자동차를 종합한 점수제가 적용되나, 이 계산기는 소득 기준으로 간략 계산합니다</li>', '<li>Regional subscribers use an income/property/vehicle point system; this calculator uses income basis only for simplicity</li>'),

    # ── Compound interest page ──
    ('<h1>복리 계산기</h1>', '<h1>Compound Interest Calculator</h1>'),
    ('>복리 계산기<', '>Compound Interest Calculator<'),
    ('<label for="principal">원금 (만원)</label>', '<label for="principal">Principal (10,000 KRW units)</label>'),
    ('<label for="annualRate">연이율 (%)</label>', '<label for="annualRate">Annual Interest Rate (%)</label>'),
    ('<label for="years">기간 (년)</label>', '<label for="years">Period (years)</label>'),
    ('<label>복리 주기</label>', '<label>Compounding Frequency</label>'),
    ('>매년<', '>Annual<'),
    ('>매분기<', '>Quarterly<'),
    ('>매월<', '>Monthly<'),
    ('<div class="result-label">최종 금액</div>', '<div class="result-label">Final Amount</div>'),
    ('<span class="label">복리 이자</span>', '<span class="label">Compound Interest</span>'),
    ('<h3>연도별 복리 계산 표</h3>', '<h3>Yearly Compound Interest Table</h3>'),
    ('<th>년도</th>', '<th>Year</th>'),
    ('<th>원리금</th>', '<th>Principal + Interest</th>'),
    ('<th>이자 합계</th>', '<th>Total Interest</th>'),
    # compound JS table cells
    ("      <td>${fmt(amount)}원</td>", '      <td>${fmt(amount)} KRW</td>'),
    ("      <td>${fmt(cumulativeInterest)}원</td>", '      <td>${fmt(cumulativeInterest)} KRW</td>'),
    ("      <td>${fmt(yearlyInterest)}원</td>", '      <td>${fmt(yearlyInterest)} KRW</td>'),
    ('placeholder="예: 5"', 'placeholder="e.g. 5"'),

    # ── Data size page ──
    ('<h1>데이터 용량 변환기</h1>', '<h1>Data Size Converter</h1>'),
    ('>데이터 용량<', '>Data Size<'),
    ('데이터 용량 변환', 'Data Size Conversion'),

    # ── Date-calc page ──
    ('<h1>날짜 계산기</h1>', '<h1>Date Calculator</h1>'),
    ('<label for="date1">시작일</label>', '<label for="date1">Start Date</label>'),
    ('<label for="date2">종료일</label>', '<label for="date2">End Date</label>'),
    ('<label for="baseDay">기준 날짜</label>', '<label for="baseDay">Base Date</label>'),
    ('<label for="addDays">더하거나 뺄 일수</label>', '<label for="addDays">Days to Add / Subtract</label>'),
    ('>날짜 간격 계산<', '>Date Difference<'),
    ('>날짜 더하기/빼기<', '>Add/Subtract Days<'),
    ('<span class="label">년</span>', '<span class="label">Years</span>'),
    ('<span class="label">월</span>', '<span class="label">Months</span>'),
    ('<span class="label">일</span>', '<span class="label">Days</span>'),
    ('<span class="label">총 일수</span>', '<span class="label">Total Days</span>'),
    ('<span class="label">결과 날짜</span>', '<span class="label">Result Date</span>'),

    # ── D-Day page ──
    ('<label for="ddayName">D-Day 이름</label>', '<label for="ddayName">D-Day Name</label>'),
    ('<label for="ddayDate">목표 날짜</label>', '<label for="ddayDate">Target Date</label>'),
    ('>D-Day 추가<', '>Add D-Day<'),
    ('저장된 D-Day', 'Saved D-Days'),

    # ── Electricity page ──
    ('<h1>전기요금 계산기 2026</h1>', '<h1>Electricity Bill Calculator 2026</h1>'),
    ('<p>월 사용량(kWh)으로 한국전력 누진요금을 계산합니다</p>', '<p>Calculate KEPCO electricity bill using monthly kWh usage</p>'),
    ('>전기요금 계산기<', '>Electricity Bill Calculator<'),
    ('<label for="kwh">월 사용량 (kWh)</label>', '<label for="kwh">Monthly Usage (kWh)</label>'),
    ('placeholder="예: 350"', 'placeholder="e.g. 350"'),
    ('<label>계절</label>', '<label>Season</label>'),
    ('> 기타 계절 (1~6월, 9~12월)', '> Other Seasons (Jan–Jun, Sep–Dec)'),
    ('> 하계 (7~8월)', '> Summer (Jul–Aug)'),
    ('<div class="result-label">총 청구금액 (원)</div>', '<div class="result-label">Total Bill (KRW)</div>'),
    ('<span class="label">구간</span>', '<span class="label">Tier</span>'),
    ('<span class="label">기본요금</span>', '<span class="label">Base Charge</span>'),
    ('<span class="label">전력량요금</span>', '<span class="label">Usage Charge</span>'),
    ('<span class="label">부가세 (10%)</span>', '<span class="label">VAT (10%)</span>'),
    ('<span class="label">전력산업기반기금 (3.7%)</span>', '<span class="label">Industry Fund (3.7%)</span>'),
    ('<h3>💡 전기요금 누진 구간 (기타계절 기준)</h3>', '<h3>💡 KEPCO Progressive Rate Tiers (non-summer)</h3>'),
    ('<li><strong>1구간 (0~200kWh):</strong> 기본요금 910원, 전력량 93.3원/kWh</li>', '<li><strong>Tier 1 (0–200 kWh):</strong> Base 910 KRW, Usage 93.3 KRW/kWh</li>'),
    ('<li><strong>2구간 (201~400kWh):</strong> 기본요금 1,600원, 전력량 187.9원/kWh</li>', '<li><strong>Tier 2 (201–400 kWh):</strong> Base 1,600 KRW, Usage 187.9 KRW/kWh</li>'),
    ('<li><strong>3구간 (400kWh 초과):</strong> 기본요금 7,300원, 전력량 280.6원/kWh</li>', '<li><strong>Tier 3 (over 400 kWh):</strong> Base 7,300 KRW, Usage 280.6 KRW/kWh</li>'),
    ('<li>부가가치세 10%와 전력산업기반기금 3.7%가 추가됩니다</li>', '<li>VAT (10%) and industry development fund (3.7%) are added to the subtotal</li>'),
    ("alert('사용량을 입력해주세요.');", "alert('Please enter your kWh usage.');"),
    ("'1구간'", "'Tier 1'"),
    ("'2구간'", "'Tier 2'"),
    ("'3구간'", "'Tier 3'"),

    # ── Brokerage page ──
    ('<h1>부동산 중개수수료 계산기</h1>', '<h1>Real Estate Brokerage Fee Calculator</h1>'),
    ('<p>매매·전세·월세 거래유형별 법정 최대 중개수수료를 계산합니다</p>', '<p>Calculate maximum legal brokerage fee by transaction type</p>'),
    ('>중개수수료 계산기<', '>Brokerage Fee Calculator<'),
    ('>생활 계산기<', '>Life Calculators<'),
    ('<label>거래 유형</label>', '<label>Transaction Type</label>'),
    ('> 매매', '> Purchase/Sale'),
    ('> 전세', '> Jeonse (Lump-sum Lease)'),
    ('> 월세', '> Monthly Rent'),
    ('<label for="price">거래금액 (만원)</label>', '<label for="price">Transaction Amount (10,000 KRW units)</label>'),
    ('placeholder="예: 50000"', 'placeholder="e.g. 50000"'),
    ('<span class="form-hint">매매가 / 전세보증금 / 월세보증금</span>', '<span class="form-hint">Sale price / Jeonse deposit / Monthly rent deposit</span>'),
    ('<label for="rent">월세 금액 (만원)</label>', '<label for="rent">Monthly Rent Amount (10,000 KRW units)</label>'),
    ('placeholder="예: 80"', 'placeholder="e.g. 80"'),
    ('<div class="result-label">최대 중개수수료 (VAT 별도)</div>', '<div class="result-label">Max Brokerage Fee (excl. VAT)</div>'),
    ('<span class="label">적용 요율</span>', '<span class="label">Applied Rate</span>'),
    ('<span class="label">거래금액</span>', '<span class="label">Transaction Amount</span>'),
    ('<span class="label">VAT 포함 (10%)</span>', '<span class="label">Incl. VAT (10%)</span>'),
    ('<h3>💡 중개수수료 참고 (2021년 개정 기준)</h3>', '<h3>💡 Brokerage Fee Reference (2021 Revised Rates)</h3>'),
    ('<li>중개수수료는 법정 <strong>최대</strong> 요율이며, 협의로 낮출 수 있습니다</li>', '<li>The brokerage fee shown is the <strong>maximum</strong> legal rate; it can be negotiated lower</li>'),
    ('<li>부가가치세(VAT 10%)는 중개사가 일반과세자인 경우 별도</li>', '<li>VAT (10%) is added separately if the agent is a general taxable business</li>'),
    ('<li>월세의 경우 환산금액 = 보증금 + (월세 x 100)으로 구간 판단</li>', '<li>For monthly rent: equivalent amount = deposit + (monthly rent × 100) for tier calculation</li>'),

    # ── Apartment score page ──
    ('<h1>청약 가점 계산기</h1>', '<h1>Housing Subscription Score Calculator</h1>'),
    ('<p>무주택기간·부양가족·청약통장 가입기간 가점을 합산합니다 (최대 84점)</p>', '<p>Sum housing-free period, dependents, and subscription period scores (max 84 points)</p>'),
    ('>청약 가점 계산기<', '>Housing Subscription Score<'),
    ('1. 무주택기간', '1. Housing-Free Period'),
    ('(최대 32점)', '(max 32 pts)'),
    ('>1년 미만 — 2점<', '>Under 1 year — 2 pts<'),
    ('>1년 이상 2년 미만 — 4점<', '>1–2 years — 4 pts<'),
    ('>2년 이상 3년 미만 — 6점<', '>2–3 years — 6 pts<'),
    ('>3년 이상 4년 미만 — 8점<', '>3–4 years — 8 pts<'),
    ('>4년 이상 5년 미만 — 10점<', '>4–5 years — 10 pts<'),
    ('>5년 이상 6년 미만 — 12점<', '>5–6 years — 12 pts<'),
    ('>6년 이상 7년 미만 — 14점<', '>6–7 years — 14 pts<'),
    ('>7년 이상 8년 미만 — 16점<', '>7–8 years — 16 pts<'),
    ('>8년 이상 9년 미만 — 18점<', '>8–9 years — 18 pts<'),
    ('>9년 이상 10년 미만 — 20점<', '>9–10 years — 20 pts<'),
    ('>10년 이상 11년 미만 — 22점<', '>10–11 years — 22 pts<'),
    ('>11년 이상 12년 미만 — 24점<', '>11–12 years — 24 pts<'),
    ('>12년 이상 13년 미만 — 26점<', '>12–13 years — 26 pts<'),
    ('>13년 이상 14년 미만 — 28점<', '>13–14 years — 28 pts<'),
    ('>14년 이상 15년 미만 — 30점<', '>14–15 years — 30 pts<'),
    ('>15년 이상 — 32점<', '>15+ years — 32 pts<'),
    ('만 30세 미만 미혼은 성년 이후 기간 적용', 'For unmarried persons under 30, period counted from age of majority'),
    ('2. 부양가족 수', '2. Number of Dependents'),
    ('(최대 35점, 본인 제외)', '(max 35 pts, excluding self)'),
    ('>0명 — 5점<', '>0 dependents — 5 pts<'),
    ('>1명 — 10점<', '>1 dependent — 10 pts<'),
    ('>2명 — 15점<', '>2 dependents — 15 pts<'),
    ('>3명 — 20점<', '>3 dependents — 20 pts<'),
    ('>4명 — 25점<', '>4 dependents — 25 pts<'),
    ('>5명 — 30점<', '>5 dependents — 30 pts<'),
    ('>6명 이상 — 35점<', '>6+ dependents — 35 pts<'),
    ('직계존속(부모 등) 3년 이상 동일 주민등록 시 인정', 'Direct ascendants (parents, etc.) recognized with 3+ years of shared residence registration'),
    ('3. 청약통장 가입기간', '3. Subscription Account Period'),
    ('(최대 17점)', '(max 17 pts)'),
    ('>6개월 미만 — 1점<', '>Under 6 months — 1 pt<'),
    ('>6개월 이상 1년 미만 — 2점<', '>6–12 months — 2 pts<'),
    ('>1년 이상 2년 미만 — 3점<', '>1–2 years — 3 pts<'),
    ('>2년 이상 3년 미만 — 4점<', '>2–3 years — 4 pts<'),
    ('>3년 이상 4년 미만 — 5점<', '>3–4 years — 5 pts<'),
    ('>4년 이상 5년 미만 — 6점<', '>4–5 years — 6 pts<'),
    ('>5년 이상 6년 미만 — 7점<', '>5–6 years — 7 pts<'),
    ('>6년 이상 7년 미만 — 8점<', '>6–7 years — 8 pts<'),
    ('>7년 이상 8년 미만 — 9점<', '>7–8 years — 9 pts<'),
    ('>8년 이상 9년 미만 — 10점<', '>8–9 years — 10 pts<'),
    ('>9년 이상 10년 미만 — 11점<', '>9–10 years — 11 pts<'),
    ('>10년 이상 11년 미만 — 12점<', '>10–11 years — 12 pts<'),
    ('>11년 이상 12년 미만 — 13점<', '>11–12 years — 13 pts<'),
    ('>12년 이상 13년 미만 — 14점<', '>12–13 years — 14 pts<'),
    ('>13년 이상 14년 미만 — 15점<', '>13–14 years — 15 pts<'),
    ('>14년 이상 15년 미만 — 16점<', '>14–15 years — 16 pts<'),
    ('>15년 이상 — 17점<', '>15+ years — 17 pts<'),
    ('/ 84점 (최대)', '/ 84 points (max)'),
    ('>무주택기간<', '>Housing-Free Period<'),
    ('>부양가족<', '>Dependents<'),
    ('>청약통장 가입기간<', '>Subscription Period<'),
    ('💡 점수가 높을수록 인기 단지 당첨 확률이 높습니다. 단지별 커트라인은 청약홈(applyhome.co.kr)에서 확인하세요.', '💡 A higher score increases your chances for popular housing units. Check cutoff scores per project at applyhome.co.kr.'),
    ('<h3>💡 청약 가점제 안내</h3>', '<h3>💡 Korean Housing Subscription Priority System</h3>'),
    ('<li>가점제는 무주택 기간(32점) + 부양가족 수(35점) + 청약통장 가입기간(17점) = 최대 84점</li>', '<li>Score = Housing-free period (32 pts) + Dependents (35 pts) + Subscription period (17 pts) = max 84 pts</li>'),
    ('<li>투기과열지구·조정대상지역 85㎡ 이하는 가점제 100% 적용</li>', '<li>Speculative/regulated areas: 100% priority system applies for units 85㎡ and under</li>'),
    ('<li>무주택기간: 세대 구성원 전원이 주택을 소유하지 않은 기간</li>', '<li>Housing-free period: period during which all household members have owned no housing</li>'),
    ('<li>부양가족: 주민등록표상 동일 세대원 (직계존속은 3년 이상 동거 요건)</li>', '<li>Dependents: same household members on resident registration (direct ascendants need 3+ years co-residence)</li>'),
    ("'최상위권 — 인기 단지도 도전해볼 만합니다'", "'Top tier — competitive for popular housing projects'"),
    ("'상위권 — 일반 분양 단지에서 경쟁력이 있습니다'", "'Upper tier — competitive for standard housing projects'"),
    ("'중위권 — 외곽지역 또는 비인기 단지 청약을 고려하세요'", "'Middle tier — consider outer areas or less popular projects'"),
    ("'하위권 — 가점 누적 후 재도전하거나 추첨제 청약을 활용하세요'", "'Lower tier — accumulate more points or apply via lottery allocation'"),

    # ── Area page ──
    ('<h1>넓이 단위 변환기</h1>', '<h1>Area Unit Converter</h1>'),
    ('<p>값을 입력하면 모든 넓이 단위가 실시간으로 변환됩니다</p>', '<p>Enter a value to convert all area units in real time</p>'),
    ('>단위 변환<', '>Unit Converters<'),
    ('>넓이 변환<', '>Area Converter<'),
    ('<h2>넓이 단위 변환</h2>', '<h2>Area Unit Conversion</h2>'),
    ('<h3>💡 넓이 단위 참고</h3>', '<h3>💡 Area Unit Reference</h3>'),
    ('<li>1평 = 3.30579 m² (약 3.3 m²)</li>', '<li>1 pyeong = 3.30579 m² (approx. 3.3 m²)</li>'),
    ('<li>1헥타르 = 10,000 m² (100m x 100m)</li>', '<li>1 hectare = 10,000 m² (100m × 100m)</li>'),
    ('<li>1에이커 = 4,046.86 m²</li>', '<li>1 acre = 4,046.86 m²</li>'),
    ('<li>아파트 33평 = 약 109 m²</li>', '<li>33 pyeong apartment ≈ 109 m²</li>'),

    # ── Length page ──
    ('<h1>길이 단위 변환기</h1>', '<h1>Length Unit Converter</h1>'),
    ('<p>값을 입력하면 모든 길이 단위가 실시간으로 변환됩니다</p>', '<p>Enter a value to convert all length units in real time</p>'),
    ('>길이 변환<', '>Length Converter<'),
    ('<h2>길이 단위 변환</h2>', '<h2>Length Unit Conversion</h2>'),

    # ── Weight page ──
    ('<h1>무게 단위 변환기</h1>', '<h1>Weight Unit Converter</h1>'),
    ('<p>값을 입력하면 모든 무게 단위가 실시간으로 변환됩니다</p>', '<p>Enter a value to convert all weight units in real time</p>'),
    ('>무게 변환<', '>Weight Converter<'),
    ('<h2>무게 단위 변환</h2>', '<h2>Weight Unit Conversion</h2>'),

    # ── Temperature page ──
    ('<h1>온도 변환기</h1>', '<h1>Temperature Converter</h1>'),
    ('<p>값을 입력하면 섭씨·화씨·켈빈이 실시간으로 변환됩니다</p>', '<p>Enter a value to convert between Celsius, Fahrenheit, and Kelvin in real time</p>'),
    ('>온도 변환<', '>Temperature Converter<'),
    ('<h2>온도 변환</h2>', '<h2>Temperature Conversion</h2>'),

    # ── Percentage page ──
    ('<h1>백분율 계산기</h1>', '<h1>Percentage Calculator</h1>'),
    ('>백분율 계산기<', '>Percentage Calculator<'),
    ('X의 Y%', 'Y% of X'),
    ('X가 Y의 몇%', 'What % is X of Y'),
    ('증감률', 'Percentage Change'),
    ('<label for="val1">값 (X)</label>', '<label for="val1">Value (X)</label>'),
    ('<label for="pct">퍼센트 (Y%)</label>', '<label for="pct">Percent (Y%)</label>'),
    ('<label for="partVal">부분 (X)</label>', '<label for="partVal">Part (X)</label>'),
    ('<label for="wholeVal">전체 (Y)</label>', '<label for="wholeVal">Whole (Y)</label>'),
    ('<label for="oldVal">이전 값</label>', '<label for="oldVal">Original Value</label>'),
    ('<label for="newVal">새 값</label>', '<label for="newVal">New Value</label>'),
    ('>결과:<', '>Result:<'),

    # ── Fuel economy page ──
    ('<h1>연비 계산기</h1>', '<h1>Fuel Economy Calculator</h1>'),
    ('>연비 계산기<', '>Fuel Economy Calculator<'),
    ('<label for="distance">주행 거리 (km)</label>', '<label for="distance">Distance (km)</label>'),
    ('<label for="fuel">연료 사용량 (L)</label>', '<label for="fuel">Fuel Used (L)</label>'),
    ('<label for="efficiency">연비 (km/L)</label>', '<label for="efficiency">Fuel Economy (km/L)</label>'),
    ('<label for="fuelPrice">연료 단가 (원/L)</label>', '<label for="fuelPrice">Fuel Price (KRW/L)</label>'),
    ('<label for="travelDist">주행 거리 (km)</label>', '<label for="travelDist">Travel Distance (km)</label>'),
    ('<div class="result-label">연비</div>', '<div class="result-label">Fuel Economy</div>'),
    ('<span class="label">주유 비용</span>', '<span class="label">Fuel Cost</span>'),

    # ── FAQ heading (all pages — inline style version) ──
    ('>자주 묻는 질문</', '>Frequently Asked Questions</'),

    # ── Footer common ──
    ('대출이자·연봉·BMI·단위변환·날짜 계산까지 20가지 무료 온라인 계산기 모음', '25+ free online calculators: loan, salary, BMI, unit conversion, dates and more'),
    ('20가지 무료 온라인 계산기 모음', '25+ free online calculators'),
    ('<h4>WooaHouse Services</h4>', '<h4>WooaHouse Services</h4>'),
    ('<h4>정보</h4>', '<h4>Info</h4>'),
    ('>서비스 소개<', '>About<'),
    ('>개인정보처리방침<', '>Privacy Policy<'),
    ('>대출이자 계산기<', '>Loan Calculator<'),
    ('>적금이자 계산기<', '>Savings Calculator<'),
    ('>연봉 실수령액<', '>Salary Calculator<'),
    ('>퇴직금 계산기<', '>Severance Pay<'),
    ('>BMI 계산기<', '>BMI Calculator<'),
    ('>기초대사량 계산기<', '>BMR Calculator<'),
    ('>칼로리 소모 계산기<', '>Calorie Burn<'),
    ('>D-Day 계산기<', '>D-Day Calculator<'),
    ('>날짜 계산기<', '>Date Calculator<'),
    ('>나이 계산기<', '>Age Calculator<'),
    ('>길이 변환<', '>Length Converter<'),
    ('>무게 변환<', '>Weight Converter<'),
    ('>온도 변환<', '>Temperature Converter<'),
    ('>넓이 변환<', '>Area Converter<'),
    ('>데이터 용량<', '>Data Size<'),
    ('>백분율 계산기<', '>Percentage Calculator<'),
    ('>연비 계산기<', '>Fuel Economy<'),
    ('>전기요금 계산기<', '>Electricity Bill<'),
    ('>중개수수료 계산기<', '>Brokerage Fee<'),
    ('>청약 가점 계산기<', '>Housing Score<'),
    ('>환율 계산기<', '>Currency Converter<'),
    ('>건강보험료 계산기<', '>Health Insurance<'),
    ('>복리 계산기<', '>Compound Interest<'),
    ('>부가세 계산기<', '>VAT Calculator<'),
    ('이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.', 'This post is part of the Coupang Partners program, and we may receive a commission.'),

    # ── apartment score initial values ──
    ('>2점 / 32점<', '>2 pts / 32<'),
    ('>5점 / 35점<', '>5 pts / 35<'),
    ('>1점 / 17점<', '>1 pt / 17<'),

    # ── HTML comment strings ──
    ('<!-- 금융 계산기 -->', '<!-- Finance Calculators -->'),
    ('<!-- 건강 계산기 -->', '<!-- Health Calculators -->'),
    ('<!-- 날짜 계산기 -->', '<!-- Date Calculators -->'),
    ('<!-- 단위 변환 -->', '<!-- Unit Converters -->'),
    ('<!-- 생활 계산기 -->', '<!-- Life Calculators -->'),
    ('<!-- 무주택기간 -->', '<!-- Housing-Free Period -->'),
    ('<!-- 부양가족 수 -->', '<!-- Number of Dependents -->'),
    ('<!-- 청약통장 가입기간 -->', '<!-- Subscription Account Period -->'),

    # ── Compound interest page ──
    ('<p>원금과 연이율로 복리 효과를 연도별로 계산합니다</p>', '<p>Enter principal and annual rate to see compound interest by year</p>'),
    ('<label for="principal">원금 (원)</label>', '<label for="principal">Principal (KRW)</label>'),
    ('placeholder="예: 10000000"', 'placeholder="e.g. 10000000"'),
    ('<label for="years">투자기간 (년)</label>', '<label for="years">Investment Period (years)</label>'),
    ('placeholder="예: 10"', 'placeholder="e.g. 10"'),
    ('<label for="compoundFreq">이자 복리 방식</label>', '<label for="compoundFreq">Compounding Frequency</label>'),
    ('>월복리 (월 1회)<', '>Monthly compounding<'),
    ('>분기복리 (분기 1회)<', '>Quarterly compounding<'),
    ('>반기복리 (반기 1회)<', '>Semi-annual compounding<'),
    ('>연복리 (연 1회)<', '>Annual compounding<'),
    ('<div class="result-label">최종 원리금 합계</div>', '<div class="result-label">Final Amount (Principal + Interest)</div>'),
    ('<span class="label">원금</span>', '<span class="label">Principal</span>'),
    ('<span class="label">총 이자</span>', '<span class="label">Total Interest</span>'),
    ('<span class="label">수익률</span>', '<span class="label">Return Rate</span>'),
    ('<h3 style="font-size:.95rem;font-weight:700;color:#e2e8f0;margin-bottom:8px">연도별 원리금 현황</h3>', '<h3 style="font-size:.95rem;font-weight:700;color:#e2e8f0;margin-bottom:8px">Year-by-Year Summary</h3>'),
    ('<th>연도</th>', '<th>Year</th>'),
    ('<th>원리금 합계</th>', '<th>Total (P+I)</th>'),
    ('<th>누적 이자</th>', '<th>Cumulative Interest</th>'),
    ('<th>연간 이자</th>', '<th>Annual Interest</th>'),
    ('<h3>💡 복리 계산 팁</h3>', '<h3>💡 Compound Interest Tips</h3>'),
    ('<li><strong>복리 공식:</strong> A = P × (1 + r/n)^(n×t) — P: 원금, r: 연이율, n: 연간 복리 횟수, t: 기간(년)</li>', '<li><strong>Formula:</strong> A = P × (1 + r/n)^(n×t) — P: principal, r: annual rate, n: compounding periods/year, t: years</li>'),
    ('<li>월복리는 연복리보다 실효 수익이 더 높습니다</li>', '<li>Monthly compounding yields slightly higher returns than annual compounding</li>'),
    ('<li>이자에 이자가 붙는 복리 효과는 장기 투자일수록 극대화됩니다</li>', '<li>The power of compounding grows dramatically over long time horizons</li>'),
    ('<li>세금(이자소득세 15.4%)은 이 계산기에서 제외됩니다</li>', '<li>This calculator excludes tax (15.4% interest income tax)</li>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">복리와 단리의 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between compound and simple interest?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">단리는 원금에만 이자가 붙지만, 복리는 이자에도 이자가 붙습니다. 기간이 길수록 복리 효과가 극적으로 커집니다. 예를 들어 연 5% 복리로 30년 투자 시 원금이 약 4.3배가 됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Simple interest applies only to the principal, while compound interest applies to both principal and accumulated interest. The longer the period, the more dramatic the difference — e.g., 5% annual compound rate over 30 years turns 1x into ~4.3x.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">월복리가 연복리보다 항상 유리한가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Is monthly compounding always better than annual?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">같은 명목 이율이라면 복리 횟수가 많을수록 실효 수익이 약간 높아집니다. 단, 차이는 크지 않으며 상품별 명목 이율과 조건을 먼저 비교하는 것이 중요합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">For the same nominal rate, more frequent compounding yields slightly higher effective returns. However, the difference is small — focus on comparing the nominal rate and terms of each product first.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">72의 법칙이란?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the Rule of 72?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">원금이 2배가 되는 기간 = 72 ÷ 연이율(%)로 근사 계산하는 법칙입니다. 예: 연 6% 복리라면 72÷6=12년 후 원금이 약 2배가 됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Years to double = 72 ÷ annual rate (%). Example: at 6% annual compound rate, 72÷6=12 years to double your money.</p>'),
    ("alert('최대 50년까지 계산 가능합니다.');", "alert('Maximum investment period is 50 years.');"),
    ('`\n      <td>${y}년</td>', '`\n      <td>${y}</td>'),

    # ── VAT page ──
    ('<p>공급가액과 부가세(10%), 합계금액을 자동으로 계산합니다</p>', '<p>Automatically calculate VAT (10%) and total from supply price, or reverse</p>'),
    ('<label>계산 방식</label>', '<label>Calculation Mode</label>'),
    ('> 공급가액으로 계산', '> From Supply Price'),
    ('> 합계금액에서 역산', '> Reverse from Total'),
    ('<label for="supplyAmt">공급가액 (원)</label>', '<label for="supplyAmt">Supply Price (KRW)</label>'),
    ('placeholder="예: 1000000"', 'placeholder="e.g. 1000000"'),
    ('<label for="totalAmt">합계금액 (부가세 포함, 원)</label>', '<label for="totalAmt">Total Amount (incl. VAT, KRW)</label>'),
    ('placeholder="예: 1100000"', 'placeholder="e.g. 1100000"'),
    ('<h3>💡 부가세 계산 팁</h3>', '<h3>💡 VAT Calculation Tips</h3>'),
    ('<li>부가세(VAT)는 공급가액의 10%입니다</li>', '<li>VAT is 10% of the supply price</li>'),
    ('<li>합계금액 = 공급가액 × 1.1</li>', '<li>Total = Supply Price × 1.1</li>'),
    ('<li>역산: 공급가액 = 합계금액 ÷ 1.1, 부가세 = 합계금액 ÷ 11</li>', '<li>Reverse: Supply Price = Total ÷ 1.1; VAT = Total ÷ 11</li>'),
    ('<li>세금계산서 발행 시 공급가액과 부가세를 별도로 기재합니다</li>', '<li>Tax invoices list supply price and VAT separately</li>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">부가세란 무엇인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is VAT?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">부가가치세(VAT)는 재화 또는 용역의 공급에 부과되는 세금으로, 현재 한국 표준세율은 10%입니다. 소비자가 부담하고 사업자가 대신 납부합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">VAT (Value Added Tax) is a tax levied on goods and services. The standard rate in Korea is 10%. Consumers bear the cost and businesses remit it to the government.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">공급가액과 합계금액의 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between supply price and total amount?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">공급가액은 부가세를 제외한 순수 상품·서비스 금액이고, 합계금액(공급대가)은 공급가액에 부가세 10%를 더한 실제 결제 금액입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Supply price is the pre-tax price of the goods/service. Total amount (payable) is supply price plus 10% VAT — the actual amount paid by the customer.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">부가세 면제 대상은?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What goods and services are VAT-exempt?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">기초생활용품(쌀·채소·과일 등), 의료용역, 교육용역, 금융보험 등은 부가세가 면제됩니다. 면세 거래는 세금계산서 대신 계산서를 발행합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Basic necessities (rice, vegetables, fruit, etc.), medical services, educational services, and financial/insurance products are VAT-exempt. Tax-exempt transactions use a regular invoice instead of a tax invoice.</p>'),

    # ── Severance page ──
    ('<p>입사일·퇴사일·최근 3개월 급여로 퇴직금을 산출합니다</p>', '<p>Calculate severance pay from employment dates and last 3 months salary</p>'),
    ('<label for="salary3m">최근 3개월 총 급여 (만원)</label>', '<label for="salary3m">Total Salary Last 3 Months (10,000 KRW units)</label>'),
    ('<span class="form-hint">상여금, 연차수당 등 포함 총액</span>', '<span class="form-hint">Include bonuses, annual leave pay, etc.</span>'),
    ('<span class="label">근속일수</span>', '<span class="label">Days Employed</span>'),
    ('<span class="label">근속연수</span>', '<span class="label">Years of Service</span>'),
    ('<div class="result-label">예상 퇴직금</div>', '<div class="result-label">Estimated Severance Pay</div>'),
    ('<h3>💡 퇴직금 계산 팁</h3>', '<h3>💡 Severance Pay Tips</h3>'),
    ('<li>퇴직금 = 1일 평균임금 × 30일 × (근속일수 / 365)</li>', '<li>Severance = Daily Average Wage × 30 × (Days Employed / 365)</li>'),
    ('<li>1일 평균임금 = 최근 3개월 급여 총액 / 91일</li>', '<li>Daily Average Wage = Total salary last 3 months / 91 days</li>'),
    ('<li>1년 미만 근무 시에도 비례하여 퇴직금이 발생합니다 (단, 계속근로기간 1년 이상 시 법적 의무)</li>', '<li>Severance is prorated even for under 1 year (legally required only for 1+ year continuous employment)</li>'),
    ('<li>상여금, 연차수당은 3개월분으로 환산하여 포함</li>', '<li>Bonuses and annual leave pay are converted to a 3-month basis and included</li>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">퇴직금을 받으려면 얼마나 일해야 하나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How long must I work to receive severance pay?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1주 소정근로시간 15시간 이상으로 계속 근로 기간이 1년 이상이어야 합니다. 아르바이트도 해당 조건을 충족하면 퇴직금을 받을 수 있습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">You must have worked at least 15 hours per week continuously for 1 or more years. Part-time workers who meet these conditions are also entitled to severance pay.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">평균임금이란 무엇인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the daily average wage?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">퇴직 전 3개월간 지급된 임금 총액을 해당 기간의 총 일수로 나눈 금액입니다. 상여금·연차수당도 일부 포함될 수 있습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Total wages paid in the 3 months before resignation divided by the total calendar days in that period. Bonuses and annual leave pay may be partially included.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">퇴직금은 언제까지 지급해야 하나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">By when must severance pay be paid?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">퇴직일로부터 14일 이내에 지급해야 합니다. 당사자 합의 시 기간을 연장할 수 있으나, 미지급 시 근로기준법 위반에 해당합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Payment must be made within 14 days of the last working day. It can be extended by mutual agreement, but failure to pay violates the Labor Standards Act.</p>'),
    ("alert('퇴사일이 입사일보다 빠릅니다.');", "alert('End date must be after start date.');"),

    # ── Savings page ──
    ('<p>월 납입금과 이율을 입력하면 만기수령액과 세후이자를 계산합니다</p>', '<p>Enter monthly deposit and interest rate to calculate maturity amount and after-tax interest</p>'),
    ('<label for="monthly">월 납입금액 (만원)</label>', '<label for="monthly">Monthly Deposit (10,000 KRW units)</label>'),
    ('placeholder="예: 50"', 'placeholder="e.g. 50"'),
    ('<label for="months">적금기간 (개월)</label>', '<label for="months">Savings Term (months)</label>'),
    ('placeholder="예: 12"', 'placeholder="e.g. 12"'),
    ('<label class="checkbox-label"><input type="checkbox" id="taxApply" checked> 이자소득세 15.4% 공제 적용</label>', '<label class="checkbox-label"><input type="checkbox" id="taxApply" checked> Apply 15.4% interest income tax</label>'),
    ('<div class="result-label">만기수령액</div>', '<div class="result-label">Maturity Amount</div>'),
    ('<span class="label">세금 (15.4%)</span>', '<span class="label">Tax (15.4%)</span>'),
    ('<h3>💡 적금이자 계산 팁</h3>', '<h3>💡 Savings Calculator Tips</h3>'),
    ('<li><strong>단리 공식:</strong> 이자 = 월납입금 × 기간 × (기간+1) / 2 × (연이율/12/100)</li>', '<li><strong>Simple interest formula:</strong> Interest = Monthly deposit × term × (term+1) / 2 × (annual rate / 12 / 100)</li>'),
    ('<li>이자소득세 15.4% = 소득세 14% + 지방소득세 1.4%</li>', '<li>Interest income tax 15.4% = income tax 14% + local income tax 1.4%</li>'),
    ('<li>비과세 적금(청년희망적금 등)이면 세금 공제를 해제하세요</li>', '<li>Uncheck tax if your savings account is tax-exempt (e.g., Youth Hope Savings)</li>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">단리와 복리의 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between simple and compound interest?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">단리는 원금에만 이자가 붙고, 복리는 이자에도 이자가 붙어 장기적으로 수익이 커집니다. 적금은 대부분 단리 방식으로 계산합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Simple interest applies only to the principal; compound interest applies to both principal and accumulated interest. Most Korean savings accounts use simple interest.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">이자소득세는 얼마나 공제되나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How much interest income tax is withheld?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">일반 이자소득에는 15.4%(이자소득세 14% + 지방소득세 1.4%)가 원천징수됩니다. 비과세 저축상품은 세금이 면제됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">General interest income is subject to 15.4% withholding tax (14% income tax + 1.4% local income tax). Tax-exempt savings products are not subject to this tax.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">만기 전 해지하면 이자는 어떻게 되나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What happens to interest if I withdraw early?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">중도해지 시 약정 금리보다 낮은 중도해지 이율이 적용되어 이자가 크게 줄어듭니다. 금융기관별로 다르니 사전에 확인하세요.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Early withdrawal applies a lower early termination rate, significantly reducing your interest. Rates vary by institution — check beforehand.</p>'),

    # ── Exchange rate page ──
    ('<h1>환율 계산기</h1>', '<h1>Currency Converter</h1>'),
    ('<p>금액을 입력하면 주요 통화로 실시간 환율 변환합니다</p>', '<p>Enter an amount in any currency to convert all others in real time</p>'),
    ('<h3>💡 환율 계산기 안내</h3>', '<h3>💡 Currency Converter Notes</h3>'),
    ('<li>기준 환율은 고정값으로, 실시간 환율과 다를 수 있습니다</li>', '<li>Exchange rates are fixed reference values and may differ from real-time market rates</li>'),
    ('<li>실제 환전 시에는 은행 또는 환전소의 고시 환율을 확인하세요</li>', '<li>For actual currency exchange, check the posted rates at banks or exchange offices</li>'),
    ('<li>금액 입력 후 자동으로 모든 통화가 변환됩니다</li>', '<li>All currencies are converted automatically as you type</li>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">환율은 실시간인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Are the exchange rates real-time?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">아니요. 이 계산기는 참고용 고정 환율을 사용합니다. 실시간 환율은 은행, 네이버 금융, 구글 검색 등을 참고하세요.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">No. This calculator uses fixed reference rates for estimation only. For real-time rates, check your bank, Naver Finance, or Google.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">환율 계산기는 어떤 통화를 지원하나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Which currencies are supported?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">현재 KRW(원), USD(달러), EUR(유로), JPY(엔), CNY(위안), GBP(파운드) 6개 통화를 지원합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Currently supported: KRW (Korean Won), USD (US Dollar), EUR (Euro), JPY (Japanese Yen), CNY (Chinese Yuan), GBP (British Pound).</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">환율 스프레드란 무엇인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is an exchange rate spread?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">은행이 외화를 사고파는 가격 차이입니다. 통상 매매기준율보다 살 때 더 비싸고, 팔 때 더 쌉니다. 환전 수수료를 낮추려면 은행 앱 환전 우대를 활용하세요.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">The spread is the difference between the buy and sell rates at a bank. To minimize fees, use bank app exchange discounts or currency exchange platforms.</p>'),

    # ── D-Day page ──
    ('<p>목표 날짜까지 남은 일수를 계산하고 여러 D-Day를 저장 관리합니다</p>', '<p>Calculate days until your target date and manage multiple D-Day countdowns</p>'),
    ('<label for="ddayName">D-Day 이름</label>', '<label for="ddayName">D-Day Name</label>'),
    ('<label for="ddayDate">목표 날짜</label>', '<label for="ddayDate">Target Date</label>'),
    ('<button class="btn btn-primary" onclick="addDday()">D-Day 추가</button>', '<button class="btn btn-primary" onclick="addDday()">Add D-Day</button>'),
    ('저장된 D-Day 목록', 'Saved D-Days'),
    ('<p style="color:#64748b;text-align:center;padding:20px">저장된 D-Day가 없습니다.</p>', '<p style="color:#64748b;text-align:center;padding:20px">No saved D-Days.</p>'),
    ("alert('D-Day 이름을 입력해주세요.');", "alert('Please enter a D-Day name.');"),
    ("alert('날짜를 선택해주세요.');", "alert('Please select a date.');"),
    ("'D+' + Math.abs(diff) + '일'", "'D+' + Math.abs(diff) + ' days'"),
    ("'D-' + diff + '일'", "'D-' + diff + ' days'"),
    ("'오늘'", "'Today'"),
    ('일 남음', ' days remaining'),
    ('일 지남', ' days ago'),
    ('<h3>💡 D-Day 계산기 안내</h3>', '<h3>💡 D-Day Calculator Notes</h3>'),
    ('<li>D-Day는 브라우저 로컬 스토리지에 저장되어 페이지를 닫아도 유지됩니다</li>', '<li>D-Days are stored in browser local storage and persist after closing the page</li>'),
    ('<li>목표 날짜가 오늘이면 D-Day, 이후면 D-N(남은 일수), 이전이면 D+N(지난 일수)</li>', '<li>Today = D-Day; future date = D-N (days remaining); past date = D+N (days elapsed)</li>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">D-Day가 초기화되는 경우는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">When are D-Days reset?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">브라우저 캐시/쿠키 삭제, 시크릿 모드 사용, 또는 다른 기기에서 접속할 경우 저장된 D-Day가 사라집니다. 중요한 날짜는 별도로 기록해 두세요.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Saved D-Days are cleared when you clear browser cache/cookies, use incognito mode, or access from another device. Keep a separate record of important dates.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">여러 개의 D-Day를 등록할 수 있나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Can I save multiple D-Days?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 여러 개의 D-Day를 추가하면 목록으로 저장되고 각각 삭제할 수 있습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. You can add multiple D-Days. They appear as a list and can be deleted individually.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">D-Day 계산은 몇 시 기준인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What time does the D-Day calculation use?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">날짜 기준(자정)으로 계산합니다. 예를 들어 오늘 2024년 1월 1일이고 목표일이 1월 3일이면 D-2가 표시됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Calculation is based on date (midnight). For example, if today is Jan 1 and your target is Jan 3, it shows D-2.</p>'),
    ('삭제', 'Delete'),

    # ── Date-calc page ──
    ('<p>두 날짜 사이의 기간과 특정 날짜에 일수를 더하거나 뺄 수 있습니다</p>', '<p>Calculate duration between two dates or add/subtract days from any date</p>'),
    ('<h3>💡 날짜 계산 팁</h3>', '<h3>💡 Date Calculation Tips</h3>'),
    ('<li>기간 계산: 시작일과 종료일을 선택하면 년·월·일로 기간을 계산합니다</li>', '<li>Duration: select start and end dates to get the difference in years, months, and days</li>'),
    ('<li>날짜 더하기: 기준 날짜에 양수·음수 일수를 더해 결과 날짜를 계산합니다</li>', '<li>Add/subtract: enter a base date and positive or negative number of days to find the result date</li>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">기간 계산에서 시작일을 포함하나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Is the start date included in the duration calculation?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">시작일을 포함하지 않고 종료일을 포함합니다. 예를 들어 1월 1일~1월 3일은 2일입니다. 시작일 포함이 필요하면 1일을 더해서 계산하세요.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">The start date is excluded and the end date is included. For example, Jan 1 to Jan 3 = 2 days. Add 1 if you need to include the start date.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">음수 일수를 입력하면 날짜가 어떻게 되나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What happens if I enter a negative number of days?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">음수를 입력하면 날짜가 이전으로 계산됩니다. 예를 들어 기준일 2024년 3월 1일에 -30을 입력하면 1월 31일이 됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">A negative number moves the date backward. For example, entering -30 from March 1, 2024 gives January 31.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">윤년 계산도 정확한가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Is leap year handling accurate?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. JavaScript Date 객체를 사용해 윤년(2월 29일)을 자동으로 처리합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. The calculator uses the JavaScript Date object to handle leap years (Feb 29) automatically.</p>'),
    ("alert('시작일과 종료일을 선택해주세요.');", "alert('Please select start and end dates.');"),
    ("alert('기준 날짜를 선택해주세요.');", "alert('Please select a base date.');"),

    # ── Age page ──
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">만 나이와 한국식 나이의 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between international and Korean age?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">만 나이는 생일이 지나야 한 살을 더하는 국제 기준입니다. 한국식 나이는 태어나자마자 1살로 시작해 1월 1일마다 한 살씩 추가됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">International age adds one year only after each birthday. Korean age starts at 1 at birth and increases by one on every January 1.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">2023년부터 만 나이로 통일됐나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Did Korea officially switch to international age in 2023?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 2023년 6월 28일부터 법적·행정적으로 만 나이가 공식 기준이 됐습니다. 일상 대화에서는 여전히 한국식 나이를 쓰기도 합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. Since June 28, 2023, international age is the official legal and administrative standard in Korea. Korean age is still used in everyday conversation.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">윤년생(2월 29일생)은 어떻게 계산하나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How is age calculated for people born on Feb 29 (leap day)?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">윤년이 아닌 해에는 2월 28일 또는 3월 1일을 생일로 인정합니다. 법적으로는 2월 28일 기준으로 처리하는 경우가 많습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">In non-leap years, either Feb 28 or Mar 1 is recognized as the birthday. Legally, Feb 28 is typically used.</p>'),

    # ── Fuel economy page ──
    ('<h1>연비 계산기</h1>', '<h1>Fuel Economy Calculator</h1>'),
    ('<p>주행 거리와 연료 사용량으로 연비를 계산하고, 주유비를 예상합니다</p>', '<p>Calculate fuel economy from distance and fuel used, or estimate fuel cost</p>'),
    ('<h3>💡 연비 계산 팁</h3>', '<h3>💡 Fuel Economy Tips</h3>'),
    ('<li>연비(km/L) = 주행거리(km) ÷ 연료사용량(L)</li>', '<li>Fuel economy (km/L) = Distance (km) ÷ Fuel used (L)</li>'),
    ('<li>L/100km = 100 ÷ km/L</li>', '<li>L/100km = 100 ÷ km/L</li>'),
    ('<li>주유비 = 주행거리 ÷ 연비 × 연료단가</li>', '<li>Fuel cost = Distance ÷ Economy × Fuel price</li>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">km/L와 L/100km의 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between km/L and L/100km?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">km/L는 1리터로 갈 수 있는 거리, L/100km는 100km를 가는 데 필요한 연료량입니다. 유럽에서는 L/100km를 주로 사용합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">km/L measures how far you travel per liter; L/100km measures how much fuel you use per 100 km. Europe typically uses L/100km.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">mpg(마일/갤런)는 어떻게 변환하나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How do I convert mpg (miles per gallon)?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 mpg ≈ 0.4251 km/L입니다. 미국 갤런(3.785L) 기준입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 mpg ≈ 0.4251 km/L (based on US gallon = 3.785 L).</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">연비를 높이는 방법은?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How can I improve fuel economy?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">급가속·급제동 자제, 적정 타이어 공기압 유지, 에어컨 과다 사용 줄이기, 불필요한 공회전 방지 등이 연비 향상에 효과적입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Avoid rapid acceleration and hard braking, maintain proper tire pressure, reduce excessive AC use, and avoid unnecessary idling.</p>'),

    # ── Length/Weight/Temperature pages ──
    ('<h3>💡 길이 단위 참고</h3>', '<h3>💡 Length Unit Reference</h3>'),
    ('<li>1인치 = 2.54cm</li>', '<li>1 inch = 2.54 cm</li>'),
    ('<li>1피트 = 30.48cm (12인치)</li>', '<li>1 foot = 30.48 cm (12 inches)</li>'),
    ('<li>1야드 = 91.44cm (3피트)</li>', '<li>1 yard = 91.44 cm (3 feet)</li>'),
    ('<li>1마일 = 1.60934km</li>', '<li>1 mile = 1.60934 km</li>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">1피트는 몇 cm인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How many cm is 1 foot?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1피트(ft) = 30.48cm, 1인치(in) = 2.54cm입니다. 6피트는 약 183cm입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 foot (ft) = 30.48 cm; 1 inch (in) = 2.54 cm. 6 feet ≈ 183 cm.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">1마일은 몇 km인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How many km is 1 mile?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1마일 = 1.60934km입니다. 마라톤 42.195km는 약 26.22마일입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 mile = 1.60934 km. A marathon (42.195 km) is about 26.22 miles.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">해리(nautical mile)란?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is a nautical mile?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1해리(nm) = 1,852m = 1.852km입니다. 항공·해상 거리 단위로 사용됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 nautical mile (nm) = 1,852 m = 1.852 km. Used in aviation and maritime navigation.</p>'),
    ('<h3>💡 무게 단위 참고</h3>', '<h3>💡 Weight Unit Reference</h3>'),
    ('<li>1파운드 = 453.592g (0.4536kg)</li>', '<li>1 pound = 453.592 g (0.4536 kg)</li>'),
    ('<li>1온스 = 28.3495g</li>', '<li>1 ounce = 28.3495 g</li>'),
    ('<li>1근 = 600g (한국식 고기 단위)</li>', '<li>1 geun = 600 g (Korean meat unit)</li>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">파운드와 킬로그램 환산은?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How do I convert pounds to kilograms?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1파운드(lb) = 약 0.4536kg입니다. 예를 들어 체중 150lb는 약 68kg입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 pound (lb) ≈ 0.4536 kg. For example, 150 lb ≈ 68 kg.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">온스와 그램 환산은?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How do I convert ounces to grams?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1온스(oz) = 28.3495g입니다. 금 1트로이온스 = 31.1035g으로 일반 온스와 다릅니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 ounce (oz) = 28.3495 g. Note: 1 troy ounce (for gold) = 31.1035 g, different from the standard ounce.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">미국 톤(short ton)과 미터 톤의 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between a short ton and a metric ton?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">미국식 단톤(short ton) = 907.185kg, 미터 톤(metric ton) = 1,000kg, 영국식 장톤(long ton) = 1,016.05kg입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Short ton (US) = 907.185 kg; metric ton = 1,000 kg; long ton (UK) = 1,016.05 kg.</p>'),
    ('<h3>💡 온도 변환 참고</h3>', '<h3>💡 Temperature Conversion Reference</h3>'),
    ('<li>물의 어는점: 0°C = 32°F = 273.15K</li>', '<li>Water freezing point: 0°C = 32°F = 273.15 K</li>'),
    ('<li>물의 끓는점: 100°C = 212°F = 373.15K</li>', '<li>Water boiling point: 100°C = 212°F = 373.15 K</li>'),
    ('<li>사람 체온: 약 36.5°C = 97.7°F</li>', '<li>Human body temperature: ~36.5°C = 97.7°F</li>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">섭씨와 화씨 변환 공식은?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the formula for Celsius ↔ Fahrenheit?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">°F = °C × 9/5 + 32, °C = (°F − 32) × 5/9입니다. 예를 들어 체온 36.5°C = 97.7°F입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">°F = °C × 9/5 + 32; °C = (°F − 32) × 5/9. Example: body temperature 36.5°C = 97.7°F.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">켈빈이란 무엇인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the Kelvin scale?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">켈빈(K)은 절대온도 단위로, 0K는 이론적으로 가능한 최저 온도(-273.15°C)입니다. 과학에서 주로 사용합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Kelvin (K) is the absolute temperature scale. 0 K is the theoretical minimum temperature (−273.15°C). Primarily used in science.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">체감온도와 실제 온도의 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between apparent and actual temperature?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">체감온도는 바람, 습도, 일사량 등 환경 요인을 반영한 온도입니다. 바람이 강할수록 체감온도는 낮아집니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Apparent temperature (feels-like) reflects wind, humidity, and sun. Stronger wind makes it feel colder; high humidity makes heat feel more intense.</p>'),

    # ── Data size page ──
    ('<h1>데이터 용량 변환기</h1>', '<h1>Data Size Converter</h1>'),
    ('<p>값을 입력하면 모든 데이터 용량 단위가 실시간으로 변환됩니다</p>', '<p>Enter a value to convert all data size units in real time</p>'),
    ('<h2>데이터 용량 변환</h2>', '<h2>Data Size Conversion</h2>'),
    ('<h3>💡 데이터 용량 참고</h3>', '<h3>💡 Data Size Reference</h3>'),
    ('<li>1 Byte = 8 bit</li>', '<li>1 Byte = 8 bits</li>'),
    ('<li>1 KB = 1,024 Byte</li>', '<li>1 KB = 1,024 Bytes</li>'),
    ('<li>1 MB = 1,024 KB</li>', '<li>1 MB = 1,024 KB</li>'),
    ('<li>1 GB = 1,024 MB</li>', '<li>1 GB = 1,024 MB</li>'),
    ('<li>HD 영화 1편 ≈ 4~8 GB</li>', '<li>1 HD movie ≈ 4–8 GB</li>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">1TB는 몇 GB인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How many GB is 1 TB?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1TB = 1,024GB입니다. 하드디스크 제조사는 1TB = 1,000GB로 표기해 실제보다 조금 크게 보이는 경우가 있습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 TB = 1,024 GB. Hard drive manufacturers often use 1 TB = 1,000 GB, making drives appear slightly larger than they are in practice.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">KiB와 KB의 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between KiB and KB?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">KiB(키비바이트)는 1,024Byte, KB(킬로바이트)는 1,000Byte를 의미하는 경우가 있습니다. 이 계산기는 1KB=1,024Byte(이진 기준)를 사용합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">KiB (kibibyte) = 1,024 bytes; KB (kilobyte) can mean 1,000 bytes in some contexts. This calculator uses the binary standard: 1 KB = 1,024 bytes.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">인터넷 속도 Mbps와 MB의 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between Mbps and MB?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Mbps(Megabit per second)는 초당 전송 비트 수입니다. 100Mbps 인터넷으로 1MB 파일을 다운받으면 약 0.08초가 걸립니다(100Mbps÷8=12.5MBps).</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Mbps = megabits per second (network speed). To download a 1 MB file on a 100 Mbps connection takes about 0.08 seconds (100 Mbps ÷ 8 = 12.5 MB/s).</p>'),

    # ── Percentage page ──
    ('<h1>백분율 계산기</h1>', '<h1>Percentage Calculator</h1>'),
    ('<p>세 가지 방식의 백분율 계산을 모두 지원합니다</p>', '<p>Supports three types of percentage calculations in one place</p>'),
    ('<h3>X의 Y%</h3>', '<h3>Y% of X</h3>'),
    ('<h3>X가 Y의 몇%인가?</h3>', '<h3>What % is X of Y?</h3>'),
    ('<h3>증감률</h3>', '<h3>Percentage Change</h3>'),
    ('<h3>💡 백분율 계산 팁</h3>', '<h3>💡 Percentage Calculation Tips</h3>'),
    ('<li>X의 Y% = X × Y ÷ 100</li>', '<li>Y% of X = X × Y ÷ 100</li>'),
    ('<li>X가 Y의 몇% = X ÷ Y × 100</li>', '<li>What % is X of Y = X ÷ Y × 100</li>'),
    ('<li>증감률 = (새값 - 이전값) ÷ |이전값| × 100</li>', '<li>Percentage change = (new - old) ÷ |old| × 100</li>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">할인율 계산은 어떻게 하나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How do I calculate a discount?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">원가 × (1 - 할인율/100)으로 계산합니다. 예를 들어 10만원 상품을 30% 할인하면 70,000원입니다. \'X의 Y%\' 계산기에서 X=100000, Y=30으로 할인금액을 구한 후 원가에서 빼세요.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Discounted price = original × (1 − discount% / 100). E.g., 30% off ₩100,000 = ₩70,000. Use the \'Y% of X\' calculator with X=100000, Y=30 to get the discount amount, then subtract from original.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">퍼센트 포인트(pp)와 퍼센트(%) 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between percentage points (pp) and percent (%)?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">5%에서 10%로 변화 시 5%p(퍼센트 포인트) 상승이지만 증가율은 100% 증가입니다. 퍼센트 포인트는 절대 차이, 퍼센트는 상대 변화율입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Going from 5% to 10% is a 5 percentage point (pp) increase but a 100% relative increase. Percentage points measure absolute difference; percent measures relative change.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">세후 수령액 계산은?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How do I calculate after-tax income?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">세전금액 × (1 - 세율/100) = 세후금액입니다. 예를 들어 이자 100만원에 15.4% 세금이라면 100만원 × 0.846 = 846,000원입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">After-tax amount = pre-tax amount × (1 − rate / 100). E.g., ₩1,000,000 interest at 15.4% tax: ₩1,000,000 × 0.846 = ₩846,000.</p>'),

    # ── Salary page FAQs ──
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">비과세액이란 무엇인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is a non-taxable allowance?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">식대 등 실비 보전 성격의 급여로, 2026년 기준 월 20만 원까지 소득세·4대보험 산정 기준에서 제외됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Expense reimbursement-type pay such as meal allowances. As of 2026, up to KRW 200,000 per month is excluded from income tax and insurance premium calculations.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">국민연금에 상한액이 있나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Is there a cap on national pension contributions?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 국민연금은 월 소득 590만 원(2026년 기준 근사치)을 상한으로 적용합니다. 그 이상 소득이 있어도 납부액은 동일합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. National pension contributions are capped at a monthly income of approximately KRW 5.9 million (2026 estimate). Higher earners pay the same maximum amount.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">부양가족 수가 실수령액에 영향을 주나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Do dependents affect my take-home pay?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">부양가족 1인당 연 150만 원의 인적공제가 적용되어 소득세가 줄어들고, 결과적으로 실수령액이 높아집니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Each dependent gives you a KRW 1.5 million annual personal deduction, which reduces your income tax and increases take-home pay.</p>'),

    # ── Loan interest page FAQs ──
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">원리금균등상환과 원금균등상환의 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between equal payment and equal principal repayment?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">원리금균등상환은 매달 내는 금액이 동일하며, 원금균등상환은 원금을 균등하게 나누어 납부해 초기 납부액이 크고 총 이자가 적습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Equal payment keeps the monthly amount fixed. Equal principal splits the principal evenly, resulting in a higher initial payment but less total interest.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">계산 결과가 실제 대출 이자와 다를 수 있나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Can the result differ from my actual loan interest?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 금융기관별로 이자 산정 방식, 연체이자, 중도상환수수료 등이 달라 실제 금액과 차이가 날 수 있습니다. 참고용으로만 사용하세요.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. Interest calculation methods, late fees, and prepayment penalties vary by lender. Use this as a reference only.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">DSR이란 무엇인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is DSR (Debt Service Ratio)?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">총부채원리금상환비율(DSR)은 연소득 대비 모든 부채의 연간 원리금 상환액 비율입니다. 현재 40% 규제가 적용됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">DSR (Debt Service Ratio) measures annual debt repayments as a percentage of annual income. Korea currently enforces a 40% DSR cap.</p>'),

    # ── Brokerage FAQs ──
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">중개수수료를 협의로 낮출 수 있나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Can the brokerage fee be negotiated lower?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 법정 요율은 최대 한도이며, 중개인과 협의해 낮은 요율로 계약할 수 있습니다. 중개 서비스 품질을 고려해 합리적인 금액을 협의하세요.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. The legal rate is the maximum — you can negotiate a lower rate with the agent. Consider the service quality when agreeing on a fee.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">월세의 환산금액이란?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the equivalent amount for monthly rent?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">월세의 경우 수수료 구간 판단을 위해 \'보증금 + (월세 × 100)\'으로 환산합니다. 예를 들어 보증금 1,000만원, 월세 50만원이면 환산금액은 6,000만원입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">For monthly rent, the equivalent amount = deposit + (monthly rent × 100). E.g., deposit KRW 10M + rent KRW 500K → equivalent = KRW 60M.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">전세와 월세 수수료 요율이 다른가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Are jeonse and monthly rent brokerage rates different?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 거래 유형(매매·전세·월세)과 거래금액 구간에 따라 적용 요율이 다릅니다. 2021년 개정 기준으로 상한 요율이 조정되었습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. Rates differ by transaction type (purchase, jeonse, monthly rent) and transaction amount tier. Caps were revised in the 2021 reform.</p>'),

    # ── Health insurance FAQs ──
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">건강보험료 부과 기준 소득은 무엇인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What income is used as the health insurance premium base?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">직장가입자의 경우 보수월액(급여 총액 - 비과세 소득)을 기준으로 합니다. 비과세 식대(월 20만원 한도)는 제외됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">For employee subscribers, the base is the monthly remuneration (total salary minus non-taxable income). Non-taxable meal allowances (up to KRW 200,000/month) are excluded.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">장기요양보험료는 별도인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Is long-term care insurance separate?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 장기요양보험료는 건강보험료 × 12.95%로, 건강보험료와 별도로 부과됩니다. 노인 장기요양 서비스 재원으로 사용됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. Long-term care insurance = health insurance premium × 12.95%, billed separately. It funds elderly long-term care services.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">건강보험료 상한과 하한이 있나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Are there upper and lower limits on health insurance premiums?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 상한과 하한 금액이 매년 설정됩니다. 2025년 기준 상한 보수월액은 약 1억 2,000만원이며, 하한은 최저 보험료가 적용됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. Upper and lower limits are set annually. For 2025, the maximum monthly remuneration base is approx. KRW 120 million, and a minimum premium floor applies.</p>'),

    # ── Apartment score FAQs ──
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">청약 가점제란 무엇인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the Korean housing subscription priority system?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">무주택 기간, 부양가족 수, 청약통장 가입 기간에 따라 점수를 부여하고 높은 점수 순으로 당첨자를 선정하는 방식입니다. 최대 84점입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">A priority system that awards points based on housing-free period, number of dependents, and subscription account tenure. Winners are selected in descending score order. Maximum: 84 points.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">무주택기간은 어떻게 산정하나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How is the housing-free period calculated?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">세대 구성원 전원이 주택을 소유하지 않은 기간을 기준으로 합니다. 만 30세 미만 미혼은 만 30세부터 또는 혼인 신고일부터 산정합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">The period during which all household members have owned no housing. For unmarried persons under 30, the period starts from age 30 or marriage registration, whichever comes first.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">가점이 낮으면 청약을 못 하나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Can I still apply with a low score?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">가점제 물량 외에 추첨제 물량이 있습니다. 85㎡ 초과 중대형이나 민간분양 추첨제 물량은 가점과 무관하게 청약할 수 있습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. Beyond the priority-system allocation, there is a lottery allocation. Units over 85㎡ and private-sector lottery allocations can be applied for regardless of your score.</p>'),

    # ── Area FAQs ──
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">평과 제곱미터 환산은?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How do I convert pyeong to square meters?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1평 = 3.30579m²입니다. 33평 아파트는 약 109m²입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 pyeong = 3.30579 m². A 33-pyeong apartment is about 109 m².</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">에이커는 몇 평인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How many pyeong is 1 acre?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1에이커 ≈ 1,224평(약 4,047m²)입니다. 미국 토지 거래 시 주로 사용합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 acre ≈ 1,224 pyeong (≈ 4,047 m²). Commonly used in US land transactions.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">평방피트와 평방미터 환산은?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How do I convert square feet to square meters?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1평방피트(ft²) = 약 0.0929m²입니다. 100ft²는 약 9.3m²입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 sq ft (ft²) ≈ 0.0929 m². 100 ft² ≈ 9.3 m².</p>'),

    # ── BMI FAQs ──
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">BMI 정상 범위는 얼마인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the normal BMI range?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">WHO 기준 18.5~24.9가 정상, 25 이상은 과체중, 30 이상은 비만으로 분류합니다. 한국은 23 이상을 과체중으로 보는 경우도 있습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">By WHO standards, 18.5–24.9 is normal; 25+ is overweight; 30+ is obese. In Korea, 23+ is sometimes classified as overweight.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">BMI가 높으면 무조건 비만인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Does a high BMI always mean I am obese?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">아닙니다. BMI는 체지방과 근육을 구분하지 못합니다. 근육량이 많은 운동선수도 BMI가 높게 나올 수 있으므로 참고 지표로만 활용하세요.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Not necessarily. BMI cannot distinguish fat from muscle. Athletes with high muscle mass can have a high BMI. Use it as a general reference only.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">표준 체중은 어떻게 계산하나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How is ideal weight calculated?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">표준 체중(kg) = 키(m)² × 22 공식을 주로 사용합니다. 예를 들어 키 170cm이면 1.7² × 22 ≈ 63.6kg이 표준 체중입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Ideal weight (kg) = height (m)² × 22. For example, for 170 cm: 1.7² × 22 ≈ 63.6 kg.</p>'),

    # ── BMR FAQs ──
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">기초대사량(BMR)이란?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is basal metabolic rate (BMR)?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">아무것도 하지 않고 가만히 있어도 생명 유지에 필요한 최소한의 칼로리 소모량입니다. 호흡, 체온 유지, 장기 기능 등에 사용됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">The minimum calories your body burns at complete rest to sustain life — used for breathing, maintaining body temperature, and organ function.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">BMR 계산 공식은?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the BMR formula?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Mifflin-St Jeor 공식이 가장 정확합니다. 남성: 10×체중(kg)+6.25×키(cm)-5×나이+5, 여성: 10×체중+6.25×키-5×나이-161입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">The Mifflin-St Jeor formula is the most accurate. Male: 10×weight(kg)+6.25×height(cm)−5×age+5; Female: 10×weight+6.25×height−5×age−161.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">기초대사량보다 적게 먹으면 살이 빠지나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Will I lose weight if I eat less than my BMR?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">단기적으로는 체중이 줄 수 있지만, 장기적으로 근육 손실과 대사 저하를 유발합니다. 전문가와 상담 후 적절한 칼로리를 설정하세요.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">You may lose weight short-term, but long-term it causes muscle loss and metabolic slowdown. Consult a professional before setting your calorie target.</p>'),

    # ── Calorie FAQs ──
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">MET(대사당량)란 무엇인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is MET (Metabolic Equivalent of Task)?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">안정 시 산소 소모량 대비 특정 활동의 에너지 소모 비율입니다. 걷기는 약 3.5 MET, 달리기는 7~10 MET 수준입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">The ratio of energy expenditure during an activity to the resting metabolic rate. Walking ≈ 3.5 MET; running ≈ 7–10 MET.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">같은 운동도 체중에 따라 칼로리가 다른가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Does body weight affect calories burned during the same exercise?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 칼로리 소모량 = MET × 체중(kg) × 시간(h)으로 계산하므로, 체중이 많을수록 같은 운동에서 더 많은 칼로리를 소모합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. Calories burned = MET × weight (kg) × time (h), so heavier individuals burn more calories doing the same exercise.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">1kg 감량에 필요한 칼로리는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How many calories does it take to lose 1 kg?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">체지방 1kg ≈ 7,700kcal입니다. 하루 500kcal를 추가로 소모하면 약 2주에 1kg 감량이 가능합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 kg of body fat ≈ 7,700 kcal. Burning an extra 500 kcal per day leads to approximately 1 kg of fat loss in 2 weeks.</p>'),

    # ── Electricity FAQs ──
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">전기요금 누진세란 무엇인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is a progressive electricity rate?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">사용량이 많을수록 단가가 올라가는 구조입니다. 주택용 전기는 200kWh 이하, 201~400kWh, 400kWh 초과 3단계로 나뉘어 단가가 달라집니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">A progressive rate means the unit price increases as usage rises. Residential electricity in Korea has 3 tiers: 0–200 kWh, 201–400 kWh, and over 400 kWh.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">여름·겨울 요금이 다른가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Are summer and winter electricity rates different?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 7~8월(하계)과 12~2월(동계)에는 에너지 수요가 높아 계절별 할증이 적용될 수 있습니다. 한국전력 고지서를 기준으로 확인하세요.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. Summer (Jul–Aug) and winter (Dec–Feb) have higher energy demand and may carry seasonal surcharges. Check your KEPCO bill for details.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">실제 청구 금액과 차이가 날 수 있나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Can the calculated amount differ from my actual bill?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 이 계산기는 기본 누진세 구조를 기준으로 하며, 복지 할인, 계절 요금, 연료비 조정액 등은 반영되지 않아 실제 금액과 다를 수 있습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. This calculator uses the basic progressive rate structure. Welfare discounts, seasonal charges, and fuel cost adjustments are not included, so the actual bill may differ.</p>'),

    # ── JS template literals in compound-interest.html ──
    ("'원'", "'KRW'"),
    ("+' kcal/일';", "+' kcal/day';"),
    ("+' kcal/h';", "+' kcal/h';"),
    ("+'일 ('+hours.toFixed(1)+'시간)'", "+'min ('+hours.toFixed(1)+'h)'"),
    ("+'원';", "+'KRW';"),
    ("+'원 ('+years+'년 '+months+'개월 '+days+'일)'", "+'KRW ('+years+'y '+months+'m '+days+'d)'"),

    # ── exchange-rate page (exact strings in source) ──
    ('<p>KRW·USD·EUR·JPY·CNY·GBP 환율을 한 번에 계산합니다</p>', '<p>Convert between KRW, USD, EUR, JPY, CNY, GBP in one place</p>'),
    ('<label for="amount">기준 금액</label>', '<label for="amount">Amount</label>'),
    ('placeholder="예: 1000"', 'placeholder="e.g. 1000"'),
    ('<label for="baseCurrency">기준 통화</label>', '<label for="baseCurrency">Base Currency</label>'),
    ('<option value="KRW">🇰🇷 KRW (원)</option>', '<option value="KRW">🇰🇷 KRW (Korean Won)</option>'),
    ('<option value="USD" selected>🇺🇸 USD (달러)</option>', '<option value="USD" selected>🇺🇸 USD (US Dollar)</option>'),
    ('<option value="EUR">🇪🇺 EUR (유로)</option>', '<option value="EUR">🇪🇺 EUR (Euro)</option>'),
    ('<option value="JPY">🇯🇵 JPY (엔)</option>', '<option value="JPY">🇯🇵 JPY (Japanese Yen)</option>'),
    ('<option value="CNY">🇨🇳 CNY (위안)</option>', '<option value="CNY">🇨🇳 CNY (Chinese Yuan)</option>'),
    ('<option value="GBP">🇬🇧 GBP (파운드)</option>', '<option value="GBP">🇬🇧 GBP (British Pound)</option>'),
    ('⚠️ 참고: 표시된 환율은 참고용이며 실제 환율과 다를 수 있습니다. (2025년 기준 고정 환율 적용)', '⚠️ Note: Exchange rates shown are reference values only and may differ from real-time rates. (Fixed rates as of 2025)'),
    ('<div class="tips-panel"><h3>💡 환율 계산 참고사항</h3><ul>', '<div class="tips-panel"><h3>💡 Currency Converter Notes</h3><ul>'),
    ('<li>이 계산기는 2025년 기준 참고용 고정 환율을 사용합니다</li>', '<li>This calculator uses fixed reference rates as of 2025</li>'),
    ('<li>실제 환율은 매일 변동하므로 정확한 환율은 은행이나 한국은행 사이트를 확인하세요</li>', '<li>Actual exchange rates change daily — check your bank or the Bank of Korea website for precise rates</li>'),
    ('<li>환전 시 은행 수수료가 별도 부과될 수 있습니다</li>', '<li>Bank fees may apply when exchanging currency</li>'),
    ('<li>참고 환율: 1 USD = 1,380 KRW / 1 EUR = 1,500 KRW / 100 JPY = 920 KRW</li>', '<li>Reference rates: 1 USD = 1,380 KRW / 1 EUR = 1,500 KRW / 100 JPY = 920 KRW</li>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">실시간 환율을 사용하나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Are the exchange rates real-time?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">이 계산기는 2025년 기준 고정 환율을 사용합니다. 실시간 환율은 매일 변동하므로 정확한 정보는 한국은행(bok.or.kr) 또는 은행 앱을 이용하세요.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">No. This calculator uses fixed reference rates (2025). For real-time rates, check the Bank of Korea (bok.or.kr) or your bank app.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">환전 수수료는 얼마인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How much is the currency exchange fee?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">환전 수수료는 금융기관마다 다르며 보통 1~3% 수준입니다. 환전 우대 쿠폰이나 인터넷·앱 환전을 이용하면 수수료를 줄일 수 있습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Fees vary by institution, typically 1–3%. Using bank app exchange discounts or online exchange services can reduce fees.</p>'),
    ('// Exchange Rate Basis: KRW 기준 (1 단위당 KRW)', '// Exchange Rate Basis: per 1 unit in KRW'),
    ("  KRW: { flag:'🇰🇷', name:'한국 원', symbol:'₩', code:'KRW', decimals:0 },", "  KRW: { flag:'🇰🇷', name:'Korean Won', symbol:'₩', code:'KRW', decimals:0 },"),
    ("  USD: { flag:'🇺🇸', name:'미국 달러', symbol:'$', code:'USD', decimals:2 },", "  USD: { flag:'🇺🇸', name:'US Dollar', symbol:'$', code:'USD', decimals:2 },"),
    ("  EUR: { flag:'🇪🇺', name:'유로', symbol:'€', code:'EUR', decimals:2 },", "  EUR: { flag:'🇪🇺', name:'Euro', symbol:'€', code:'EUR', decimals:2 },"),
    ("  JPY: { flag:'🇯🇵', name:'일본 엔', symbol:'¥', code:'JPY', decimals:0 },", "  JPY: { flag:'🇯🇵', name:'Japanese Yen', symbol:'¥', code:'JPY', decimals:0 },"),
    ("  CNY: { flag:'🇨🇳', name:'중국 위안', symbol:'¥', code:'CNY', decimals:2 },", "  CNY: { flag:'🇨🇳', name:'Chinese Yuan', symbol:'¥', code:'CNY', decimals:2 },"),
    ("  GBP: { flag:'🇬🇧', name:'영국 파운드', symbol:'£', code:'GBP', decimals:2 }", "  GBP: { flag:'🇬🇧', name:'British Pound', symbol:'£', code:'GBP', decimals:2 }"),
    ('  // KRW로 변환', '  // Convert to KRW'),

    # ── fuel-economy page (exact strings) ──
    ('<p>연비(km/L) 계산과 주유비 계산을 한 번에</p>', '<p>Calculate fuel economy (km/L) and fuel cost in one place</p>'),
    ('  <h2>연비 계산</h2>', '  <h2>Fuel Economy</h2>'),
    ('<label for="dist1">주행거리 (km)</label>', '<label for="dist1">Distance (km)</label>'),
    ('<label for="fuel1">연료량 (L)</label>', '<label for="fuel1">Fuel Used (L)</label>'),
    ('placeholder="예: 500"', 'placeholder="e.g. 500"'),
    ('placeholder="예: 40"', 'placeholder="e.g. 40"'),
    ('>연비 계산</button>', '>Calculate Fuel Economy</button>'),
    ('<div class="result-label">연비 (km/L)</div>', '<div class="result-label">Fuel Economy (km/L)</div>'),
    ('  <h2>주유비 계산</h2>', '  <h2>Fuel Cost</h2>'),
    ('<label for="dist2">주행거리 (km)</label>', '<label for="dist2">Distance (km)</label>'),
    ('<label for="fe2">연비 (km/L)</label>', '<label for="fe2">Fuel Economy (km/L)</label>'),
    ('placeholder="예: 300"', 'placeholder="e.g. 300"'),
    ('<label for="price2">연료 단가 (원/L)</label>', '<label for="price2">Fuel Price (KRW/L)</label>'),
    ('placeholder="예: 1650"', 'placeholder="e.g. 1650"'),
    ('>주유비 계산</button>', '>Calculate Fuel Cost</button>'),
    ('<div class="result-label">예상 주유비</div>', '<div class="result-label">Estimated Fuel Cost</div>'),
    ('<span class="label">필요 연료량</span>', '<span class="label">Fuel Needed</span>'),
    ('<span class="label">km당 비용</span>', '<span class="label">Cost per km</span>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">연비 계산 방법은?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How is fuel economy calculated?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">연비(km/L) = 주행 거리(km) ÷ 사용 연료량(L)으로 계산합니다. 주유 후 주행 거리를 기록해 다음 주유 시 계산하면 됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Fuel economy (km/L) = Distance (km) ÷ Fuel used (L). Record your odometer reading after each refuel and calculate at the next fill-up.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">복합연비와 공인연비의 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between combined and official fuel economy?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">공인연비는 국가 기준 테스트의 측정값이며, 복합연비는 도심(45%)과 고속도로(55%) 연비를 혼합 계산한 값입니다. 실제 주행 연비는 차이가 날 수 있습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Official fuel economy is measured under standardized government tests; combined fuel economy blends city (45%) and highway (55%) figures. Real-world fuel economy may differ.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">주유 비용 계산도 가능한가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Can I also calculate fuel cost?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">주유 비용 = 주행 거리 ÷ 연비 × 유가(원/L)로 계산할 수 있습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Fuel cost = Distance ÷ Fuel economy × Fuel price (KRW/L).</p>'),
    ("  if(!d||!f){alert('값을 입력해주세요.');return;}", "  if(!d||!f){alert('Please enter all values.');return;}"),
    ("  if(!d||!fe||!p){alert('값을 입력해주세요.');return;}", "  if(!d||!fe||!p){alert('Please enter all values.');return;}"),
    ("  document.getElementById('resPerKm').textContent=fmt(cost/d)+'원/km';", "  document.getElementById('resPerKm').textContent=fmt(cost/d)+' KRW/km';"),

    # ── date-calc page (exact strings) ──
    ('<p>두 날짜 사이 기간 계산, 날짜 더하기/빼기</p>', '<p>Calculate duration between two dates, or add/subtract days</p>'),
    ('<button class="tab-btn active" onclick="switchTab(0)">기간 계산</button>', '<button class="tab-btn active" onclick="switchTab(0)">Duration</button>'),
    ('<label for="startDate">시작일</label>', '<label for="startDate">Start Date</label>'),
    ('<label for="endDate">종료일</label>', '<label for="endDate">End Date</label>'),
    ('<div class="result-label">총 일수</div>', '<div class="result-label">Total Days</div>'),
    ('<span class="label">년/월/일</span>', '<span class="label">Y / M / D</span>'),
    ('<span class="label">주</span>', '<span class="label">Weeks</span>'),
    ('<span class="label">시간</span>', '<span class="label">Hours</span>'),
    ('<label for="addVal">값</label>', '<label for="addVal">Value</label>'),
    ('placeholder="예: 100"', 'placeholder="e.g. 100"'),
    ('<label for="addUnit">단위</label>', '<label for="addUnit">Unit</label>'),
    ('<option value="days">일</option><option value="months">개월</option><option value="years">년</option>', '<option value="days">Days</option><option value="months">Months</option><option value="years">Years</option>'),
    ('<label>방향</label>', '<label>Direction</label>'),
    ('> 더하기 (+)</label>', '> Add (+)</label>'),
    ('> 빼기 (-)</label>', '> Subtract (−)</label>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">윤년도 자동으로 반영되나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Are leap years handled automatically?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 자바스크립트 Date 객체를 사용해 윤년(2월 29일)을 포함한 정확한 날짜 계산이 가능합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. The calculator uses the JavaScript Date object to correctly handle leap years (Feb 29).</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">두 날짜 사이의 주 수도 알 수 있나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Can I find the number of weeks between two dates?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">일 수를 7로 나누면 됩니다. 예를 들어 28일 차이면 4주입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Divide the number of days by 7. For example, 28 days apart = 4 weeks.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">날짜에 특정 일수를 더하거나 뺄 수 있나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Can I add or subtract a number of days from a date?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 기준 날짜에 원하는 일수를 더하거나 빼서 미래·과거 날짜를 계산할 수 있습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. Enter a base date and add or subtract any number of days to calculate a future or past date.</p>'),
    ("const DAYS=['일','월','화','수','목','금','토'];", "const DAYS=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];"),
    ("  document.getElementById('resDays0').textContent=days.toLocaleString('ko-KR')+'일';", "  document.getElementById('resDays0').textContent=days.toLocaleString()+' days';"),
    ("  document.getElementById('resYMD').textContent=y+'년 '+m+'개월 '+d+'일';", "  document.getElementById('resYMD').textContent=y+'y '+m+'m '+d+'d';"),
    ("  document.getElementById('resWeeks').textContent=Math.floor(days/7)+'주 '+days%7+'일';", "  document.getElementById('resWeeks').textContent=Math.floor(days/7)+'w '+days%7+'d';"),
    ("  document.getElementById('resHours').textContent=(days*24).toLocaleString('ko-KR')+'시간';", "  document.getElementById('resHours').textContent=(days*24).toLocaleString()+' hours';"),
    ("  if(!document.getElementById('baseDate').value||!val){alert('값을 입력해주세요.');return;}", "  if(!document.getElementById('baseDate').value||!val){alert('Please enter all values.');return;}"),

    # ── dday page (exact strings) ──
    ('<p>특정 날짜까지 남은 일수를 계산하고 저장합니다</p>', '<p>Calculate days remaining to a target date and save multiple D-Days</p>'),
    ('  <h2>D-Day 계산</h2>', '  <h2>D-Day Calculator</h2>'),
    ('<label for="ddayName">이름 (선택)</label>', '<label for="ddayName">Name (optional)</label>'),
    ('placeholder="예: 시험, 여행, 기념일"', 'placeholder="e.g. Exam, Trip, Anniversary"'),
    ('<label for="targetDate">목표 날짜</label>', '<label for="targetDate">Target Date</label>'),
    ('>저장하기</button>', '>Save</button>'),
    ('<span class="label">목표 날짜</span>', '<span class="label">Target Date</span>'),
    ('<span class="label">요일</span>', '<span class="label">Day of Week</span>'),
    ('<span class="label">주 단위</span>', '<span class="label">In Weeks</span>'),
    ('  <h2>Saved D-Days 목록</h2>', '  <h2>Saved D-Days</h2>'),
    ('Saved D-Days가 없습니다. 위에서 추가해보세요.', 'No saved D-Days. Add one above.'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">D-Day와 D+1의 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between D-Day and D+1?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">기준일을 D-0으로 할 때 다음 날은 D+1입니다. 이 계산기는 당일을 포함해 날짜 차이를 계산합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">When the reference day is D-0, the next day is D+1. This calculator counts differences including today.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">과거 날짜도 계산할 수 있나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Can I calculate past dates too?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 목표 날짜가 오늘보다 이전이면 경과한 일수를 계산합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. If the target date is earlier than today, the calculator shows how many days have passed.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">생일, 기념일 D-Day 계산에 활용할 수 있나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Can I use it for birthdays and anniversaries?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 결혼기념일, 수능, 생일 등 특별한 날까지 남은 날을 확인하는 데 활용할 수 있습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. Use it to count down to weddings, exams, birthdays, and any other special occasions.</p>'),
    ("  if(!target){alert('목표 날짜를 선택해주세요.');return;}", "  if(!target){alert('Please select a target date.');return;}"),
    ("  document.getElementById('resInfo').textContent=diff>0?diff+'일 남았습니다':diff===0?'바로 오늘입니다!':Math.abs(diff)+'일 지났습니다';", "  document.getElementById('resInfo').textContent=diff>0?diff+' days remaining':diff===0?'Today!':Math.abs(diff)+' days ago';"),
    ("  document.getElementById('resDow').textContent=DAYS[t.getDay()]+'요일';", "  document.getElementById('resDow').textContent=DAYS[t.getDay()];"),
    ("  document.getElementById('resWeeks').textContent=Math.floor(weeks/7)+'주 '+weeks%7+'일';", "  document.getElementById('resWeeks').textContent=Math.floor(weeks/7)+'w '+weeks%7+'d';"),

    # ── health-insurance FAQs (exact strings in source) ──
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">건강보험료율은 얼마인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the health insurance premium rate?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">2025년 기준 건강보험료율은 보수월액의 7.09%이며, 직장가입자는 사업주와 근로자가 각 50%(3.545%)씩 부담합니다. 장기요양보험료는 건강보험료의 12.95%가 추가됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">As of 2025, the health insurance premium rate is 7.09% of monthly salary. Employers and employees each pay 50% (3.545%). Long-term care insurance adds 12.95% of the health insurance premium.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">장기요양보험료란 무엇인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is long-term care insurance?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">장기요양보험료는 노인 장기요양보험 재원 마련을 위한 보험료로, 건강보험료의 12.95%가 부과됩니다. 건강보험료와 함께 고지됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Long-term care insurance funds elderly care services. It is charged at 12.95% of the health insurance premium and billed together with health insurance.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">지역가입자 건강보험료는 어떻게 계산되나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How is health insurance calculated for regional subscribers?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">지역가입자는 소득, 재산, 자동차를 종합한 점수제로 계산됩니다. 이 계산기는 소득 기준 간략 계산이므로, 정확한 금액은 국민건강보험공단을 통해 확인하세요.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Regional subscribers use an income, property, and vehicle point system. This calculator uses a simplified income-based estimate — contact NHIS for accurate figures.</p>'),
    ('  // 2025년 기준: 건강보험료율 7.09%, 본인부담 3.545%', '  // 2025 rates: Health insurance 7.09%, employee share 3.545%'),
    ('  const LTC_RATE = 0.1295; // 건강보험료 대비 장기요양보험료율', '  const LTC_RATE = 0.1295; // Long-term care rate vs. health insurance'),

    # ── apartment-score JS outputs ──
    ("  document.getElementById('scoreHL').textContent = hl + '점 / 32점';", "  document.getElementById('scoreHL').textContent = hl + ' pts / 32';"),
    ("  document.getElementById('scoreDep').textContent = dep + '점 / 35점';", "  document.getElementById('scoreDep').textContent = dep + ' pts / 35';"),
    ("  document.getElementById('scoreSub').textContent = sub + '점 / 17점';", "  document.getElementById('scoreSub').textContent = sub + ' pts / 17';"),
    ('// 초기 계산', '// Initial calculation'),

    # ── age page JS ──
    ("const ZODIAC=['원숭이','닭','개','돼지','쥐','소','호랑이','토끼','용','뱀','말','양'];",
     "const ZODIAC=['Monkey','Rooster','Dog','Pig','Rat','Ox','Tiger','Rabbit','Dragon','Snake','Horse','Goat'];"),
    ('  // 만나이', '  // International age'),
    ('  // 한국식 나이', '  // Korean age'),
    ('  // 총일수', '  // Total days'),
    ('  // 다음 생일', '  // Next birthday'),
    ('  // 띠', '  // Zodiac'),

    # ── percentage page inline labels ──
    ("<h3>1. Y% of X는 얼마?</h3>", '<h3>1. What is Y% of X?</h3>'),
    ("<h3>2. X는 Y의 몇 %?</h3>", '<h3>2. What % is X of Y?</h3>'),
    ("<h3>3. X에서 Y로 변했을 때 Percentage Change</h3>", '<h3>3. Percentage change from X to Y</h3>'),
    ("      <input type=\"number\" id=\"a1\" step=\"any\" placeholder=\"X\"> 의", '      <input type="number" id="a1" step="any" placeholder="X"> of'),
    ("      <input type=\"number\" id=\"a2\" step=\"any\" placeholder=\"Y\"> %는 =", '      <input type="number" id="a2" step="any" placeholder="Y"> % ='),
    ("      <input type=\"number\" id=\"b1\" step=\"any\" placeholder=\"X\"> 는", '      <input type="number" id="b1" step="any" placeholder="X"> is'),
    ("      <input type=\"number\" id=\"b2\" step=\"any\" placeholder=\"Y\"> 의", '      <input type="number" id="b2" step="any" placeholder="Y"> of'),
    ("      <input type=\"number\" id=\"c1\" step=\"any\" placeholder=\"X (이전)\"> →", '      <input type="number" id="c1" step="any" placeholder="X (old)"> →'),
    ("      <input type=\"number\" id=\"c2\" step=\"any\" placeholder=\"Y (이후)\"> =", '      <input type="number" id="c2" step="any" placeholder="Y (new)"> ='),
    ('>계산</button>', '>Calculate</button>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">백분율과 퍼센트포인트(pp)의 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between percent and percentage points (pp)?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">백분율은 비율 자체를 나타내고, 퍼센트포인트는 두 백분율의 차이를 나타냅니다. 금리가 2%에서 3%로 오르면 1pp 상승이지만, 50% 증가입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Percent expresses a ratio; percentage points measure the absolute difference between two percentages. A rise from 2% to 3% is a 1 pp increase but a 50% relative increase.</p>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">할인율(%) = (원래 가격 - 할인 가격) ÷ 원래 가격 × 100으로 계산합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Discount rate (%) = (original price − discounted price) ÷ original price × 100.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">증가율은 어떻게 계산하나요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How do I calculate a percentage increase?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">증가율(%) = (변화 후 값 - 변화 전 값) ÷ 변화 전 값 × 100으로 계산합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Percentage increase (%) = (new value − old value) ÷ old value × 100.</p>'),

    # ── salary JS comments ──
    ('  // 국민연금: 과세소득의 4.5%, 상한 5,900,000원', '  // National pension: 4.5% of taxable income, capped at 5,900,000 KRW'),
    ('  // 건강보험: 3.545%', '  // Health insurance: 3.545%'),
    ('  // 장기요양: 건강보험의 12.95%', '  // Long-term care: 12.95% of health insurance'),
    ('  // 고용보험: 0.9%', '  // Employment insurance: 0.9%'),
    ('  // 소득세 간이세액표 근사치 (simplified bracket)', '  // Income tax simplified withholding table approximation'),
    ('  // 부양가족 공제 근사 (인적공제 150만×가족수)', '  // Dependent deduction approximation (1.5M KRW × dependents)'),

    # ── date-calc add/subtract button ──
    ('<button class="tab-btn" onclick="switchTab(1)">날짜 더하기/빼기</button>', '<button class="tab-btn" onclick="switchTab(1)">Add / Subtract</button>'),

    # ── breadcrumb date section ──
    ('>날짜 계산기</', '>Date Calculators</'),

    # ── ld+json FAQPage answer text (compact, no HTML) ──
    # bmr
    ('"기초대사량(BMR)이란?"', '"What is basal metabolic rate (BMR)?"'),
    ('"가만히 있어도 생명 유지에 필요한 최소한의 칼로리 소모량입니다."', '"The minimum calories your body needs to sustain life at complete rest."'),
    ('"BMR 계산 공식은?"', '"What is the BMR formula?"'),
    ('"Mifflin-St Jeor 공식: 남성 10×체중+6.25×키-5×나이+5, 여성 10×체중+6.25×키-5×나이-161입니다."', '"Mifflin-St Jeor formula: Male = 10×weight+6.25×height−5×age+5; Female = 10×weight+6.25×height−5×age−161."'),
    ('"기초대사량보다 적게 먹으면?"', '"What happens if I eat less than my BMR?"'),
    ('"단기 체중 감소가 가능하나 장기적으로 근육 손실과 대사 저하를 유발합니다."', '"Short-term weight loss is possible, but long-term it causes muscle loss and metabolic slowdown."'),
    # calorie
    ('"MET란?"', '"What is MET?"'),
    ('"안정 시 대비 특정 활동의 에너지 소모 비율입니다."', '"The ratio of energy expenditure during an activity compared to the resting metabolic rate."'),
    ('"체중에 따라 칼로리가 다른가요?"', '"Does body weight affect calories burned?"'),
    ('"네. 칼로리 소모 = MET × 체중(kg) × 시간으로, 체중이 많을수록 소모가 큽니다."', '"Yes. Calories burned = MET × weight (kg) × time (h), so heavier individuals burn more."'),
    ('"1kg 감량에 필요한 칼로리는?"', '"How many calories does it take to lose 1 kg?"'),
    ('"체지방 1kg ≈ 7,700kcal입니다."', '"1 kg of body fat ≈ 7,700 kcal."'),
    # savings
    ('"단리와 복리의 차이는?"', '"What is the difference between simple and compound interest?"'),
    ('"단리는 원금에만 이자가 붙고, 복리는 이자에도 이자가 붙어 장기적으로 수익이 커집니다."', '"Simple interest applies only to principal; compound interest applies to both, growing more over time."'),
    ('"이자소득세는 얼마나 공제되나요?"', '"How much interest income tax is withheld?"'),
    ('"일반 이자소득에는 15.4%가 원천징수됩니다."', '"General interest income is subject to 15.4% withholding tax."'),
    ('"만기 전 해지 시 이자는?"', '"What happens to interest if I withdraw early?"'),
    ('"중도해지 이율이 적용되어 이자가 크게 줄어듭니다."', '"A lower early termination rate applies, significantly reducing your interest."'),
    # temperature
    ('"섭씨와 화씨 변환은?"', '"How do I convert Celsius to Fahrenheit?"'),
    ('"°F = °C × 9/5 + 32, °C = (°F - 32) × 5/9입니다."', '"°F = °C × 9/5 + 32; °C = (°F − 32) × 5/9."'),
    ('"켈빈(K)이란?"', '"What is the Kelvin scale?"'),
    ('"절대온도 단위로 0K = -273.15°C이며 음수가 없는 온도 척도입니다."', '"Kelvin is the absolute temperature scale. 0 K = −273.15°C; there are no negative Kelvin values."'),
    ('"영하 온도도 변환 가능한가요?"', '"Can I convert below-zero temperatures?"'),
    ('"네. 동일한 공식으로 변환됩니다."', '"Yes. The same formula applies."'),
    # exchange-rate
    ('"실시간 환율을 사용하나요?"', '"Are the exchange rates real-time?"'),
    ('"이 계산기는 2025년 기준 고정 환율을 사용합니다. 정확한 환율은 한국은행이나 은행 앱을 이용하세요."', '"No. This calculator uses fixed reference rates (2025). For real-time rates, check the Bank of Korea or your bank app."'),
    ('"환전 수수료는 얼마인가요?"', '"How much is the currency exchange fee?"'),
    ('"환전 수수료는 금융기관마다 다르며 보통 1~3% 수준입니다."', '"Fees vary by institution, typically 1–3%."'),
    # loan-interest
    ('"원리금균등상환과 원금균등상환의 차이는?"', '"What is the difference between equal payment and equal principal repayment?"'),
    ('"원리금균등상환은 매달 내는 금액이 동일하고, 원금균등상환은 원금을 균등 분할해 초기 납부액이 크고 총 이자가 적습니다."', '"Equal payment keeps the monthly amount fixed. Equal principal splits the principal evenly, resulting in a higher initial payment but less total interest."'),
    ('"계산 결과가 실제 대출 이자와 다를 수 있나요?"', '"Can the calculated result differ from my actual loan interest?"'),
    ('"금융기관별 이자 산정 방식, 수수료 등이 달라 실제 금액과 차이가 날 수 있습니다."', '"Yes. Interest calculation methods and fees vary by lender, so actual amounts may differ."'),
    ('"DSR이란 무엇인가요?"', '"What is DSR (Debt Service Ratio)?"'),
    ('"총부채원리금상환비율로, 연소득 대비 모든 부채의 연간 원리금 상환액 비율입니다."', '"DSR (Debt Service Ratio) is the ratio of annual debt repayments to annual income. Korea currently enforces a 40% DSR cap."'),
    # salary
    ('"비과세액이란 무엇인가요?"', '"What is a non-taxable allowance?"'),
    ('"식대 등 실비 보전 성격의 급여로, 월 20만 원까지 소득세와 4대보험 산정에서 제외됩니다."', '"Expense reimbursement pay such as meal allowances — up to KRW 200,000 per month is excluded from income tax and insurance calculations."'),
    ('"국민연금에 상한액이 있나요?"', '"Is there a cap on national pension contributions?"'),
    ('"월 소득 590만 원을 상한으로 적용하며, 그 이상 소득이어도 납부액은 동일합니다."', '"Contributions are capped at a monthly income of approximately KRW 5.9 million. Higher earners pay the same maximum."'),
    ('"부양가족 수가 실수령액에 영향을 주나요?"', '"Do dependents affect my take-home pay?"'),
    ('"부양가족 1인당 연 150만 원 인적공제가 적용되어 소득세가 줄어들고 실수령액이 높아집니다."', '"Each dependent gives a KRW 1.5 million annual deduction, reducing income tax and increasing take-home pay."'),
    # vat
    ('"부가세란 무엇인가요?"', '"What is VAT?"'),
    ('"부가가치세(VAT)는 재화 또는 용역 공급에 부과되는 세금으로 한국 표준세율은 10%입니다."', '"VAT (Value Added Tax) is a tax levied on goods and services. The standard rate in Korea is 10%."'),
    ('"공급가액과 합계금액의 차이는?"', '"What is the difference between supply price and total amount?"'),
    ('"공급가액은 부가세 제외 금액이고, 합계금액은 공급가액에 부가세 10%를 더한 실제 결제 금액입니다."', '"Supply price is the pre-tax price; total amount is supply price plus 10% VAT — the actual amount paid."'),
    ('"부가세 면제 대상은?"', '"What goods and services are VAT-exempt?"'),
    ('"기초생활용품, 의료용역, 교육용역, 금융보험 등은 부가세가 면제됩니다."', '"Basic necessities, medical services, educational services, and financial/insurance products are VAT-exempt."'),
    # compound interest
    ('"복리와 단리의 차이는?"', '"What is the difference between compound and simple interest?"'),
    ('"단리는 원금에만 이자가 붙지만, 복리는 이자에도 이자가 붙어 기간이 길수록 효과가 극적으로 커집니다."', '"Simple interest applies only to principal; compound interest applies to both principal and accumulated interest, growing dramatically over time."'),
    ('"월복리가 연복리보다 항상 유리한가요?"', '"Is monthly compounding always better than annual?"'),
    ('"같은 명목 이율이라면 복리 횟수가 많을수록 실효 수익이 약간 높아지지만, 차이는 크지 않습니다."', '"For the same nominal rate, more frequent compounding yields slightly higher returns, but the difference is small."'),
    ('"72의 법칙이란?"', '"What is the Rule of 72?"'),
    ('"원금이 2배가 되는 기간 = 72 ÷ 연이율(%)로 근사 계산하는 법칙입니다."', '"Years to double your money ≈ 72 ÷ annual interest rate (%)."'),
    # bmi
    ('"BMI 정상 범위는?"', '"What is the normal BMI range?"'),
    ('"WHO 기준 18.5~24.9가 정상이며, 25 이상은 과체중, 30 이상은 비만입니다."', '"By WHO standards, 18.5–24.9 is normal; 25+ is overweight; 30+ is obese."'),
    ('"BMI가 높으면 무조건 비만인가요?"', '"Does a high BMI always mean obese?"'),
    ('"아닙니다. BMI는 체지방과 근육을 구분하지 못해 근육량이 많은 경우 높게 나올 수 있습니다."', '"Not necessarily. BMI cannot distinguish fat from muscle — athletes with high muscle mass can have a high BMI."'),
    ('"표준 체중 계산 방법은?"', '"How is ideal weight calculated?"'),
    ('"표준 체중(kg) = 키(m)² × 22 공식을 사용합니다."', '"Ideal weight (kg) = height (m)² × 22."'),
    # percentage
    ('"백분율과 퍼센트포인트 차이는?"', '"What is the difference between percent and percentage points?"'),
    ('"백분율은 비율 자체, 퍼센트포인트는 두 백분율의 차이를 나타냅니다."', '"Percent expresses a ratio; percentage points measure the absolute difference between two percentages."'),
    ('"할인율 계산은?"', '"How do I calculate a discount rate?"'),
    ('"(원래 가격 - 할인 가격) ÷ 원래 가격 × 100입니다."', '"(original price − discounted price) ÷ original price × 100."'),
    ('"증가율 계산은?"', '"How do I calculate a percentage increase?"'),
    ('"(변화 후 - 변화 전) ÷ 변화 전 × 100입니다."', '"(new value − old value) ÷ old value × 100."'),
    # fuel-economy
    ('"연비 계산 방법은?"', '"How is fuel economy calculated?"'),
    ('"연비(km/L) = 주행 거리 ÷ 사용 연료량으로 계산합니다."', '"Fuel economy (km/L) = Distance ÷ Fuel used."'),
    ('"복합연비와 공인연비의 차이는?"', '"What is the difference between combined and official fuel economy?"'),
    ('"공인연비는 테스트 측정값이며, 복합연비는 도심·고속도로 연비를 혼합 계산한 값입니다."', '"Official fuel economy is measured under standardized tests; combined fuel economy blends city and highway figures."'),
    ('"주유 비용 계산은?"', '"How do I calculate fuel cost?"'),
    ('"주행 거리 ÷ 연비 × 유가(원/L)로 계산할 수 있습니다."', '"Fuel cost = Distance ÷ Fuel economy × Fuel price (KRW/L)."'),
    # dday
    ('"D-Day와 D+1의 차이는?"', '"What is the difference between D-Day and D+1?"'),
    ('"기준일을 D-0으로 할 때 다음 날이 D+1입니다."', '"When the reference day is D-0, the next day is D+1."'),
    ('"과거 날짜도 계산할 수 있나요?"', '"Can I calculate past dates?"'),
    ('"네. 목표 날짜가 오늘보다 이전이면 경과한 일수를 계산합니다."', '"Yes. If the target date is before today, it shows how many days have passed."'),
    ('"기념일 D-Day 계산에 활용할 수 있나요?"', '"Can I use it for anniversaries and special occasions?"'),
    ('"결혼기념일, 수능 등 특별한 날까지 남은 날을 확인할 수 있습니다."', '"Yes. Use it to count down to weddings, exams, birthdays, and any special occasion."'),
    # date-calc
    ('"윤년도 자동 반영되나요?"', '"Are leap years handled automatically?"'),
    ('"네. 윤년(2월 29일)을 포함한 정확한 날짜 계산이 가능합니다."', '"Yes. The calculator correctly handles leap years including Feb 29."'),
    ('"두 날짜 사이의 주 수도 알 수 있나요?"', '"Can I find the number of weeks between two dates?"'),
    ('"일 수를 7로 나누어 계산할 수 있습니다."', '"Divide the number of days by 7."'),
    ('"날짜에 일수를 더하거나 뺄 수 있나요?"', '"Can I add or subtract days from a date?"'),
    ('"네. 기준 날짜에 원하는 일수를 더하거나 빼서 미래·과거 날짜를 계산할 수 있습니다."', '"Yes. Enter a base date and add or subtract any number of days to get a future or past date."'),
    # age
    ('"만 나이와 한국식 나이의 차이는?"', '"What is the difference between international and Korean age?"'),
    ('"만 나이는 생일이 지나야 한 살을 추가하는 국제 기준이며, 한국식 나이는 태어나자마자 1살로 시작합니다."', '"International age adds one year only after each birthday. Korean age starts at 1 at birth and increases by one on every January 1."'),
    ('"2023년부터 만 나이로 통일됐나요?"', '"Did Korea switch to international age in 2023?"'),
    ('"네. 2023년 6월 28일부터 법적·행정적으로 만 나이가 공식 기준입니다."', '"Yes. Since June 28, 2023, international age is the official legal and administrative standard in Korea."'),
    ('"윤년생은 어떻게 계산하나요?"', '"How is age calculated for leap day birthdays?"'),
    ('"윤년이 아닌 해에는 2월 28일을 생일로 인정하는 경우가 많습니다."', '"In non-leap years, Feb 28 is typically recognized as the birthday."'),
    # health-insurance
    ('"건강보험료율은 얼마인가요?"', '"What is the health insurance premium rate?"'),
    ('"2025년 기준 건강보험료율은 7.09%이며, 직장가입자는 사업주와 근로자가 각 3.545%씩 부담합니다."', '"As of 2025, the health insurance premium rate is 7.09%, split equally between employer and employee (3.545% each)."'),
    ('"장기요양보험료란 무엇인가요?"', '"What is long-term care insurance?"'),
    ('"장기요양보험료는 건강보험료의 12.95%가 부과되며 건강보험료와 함께 고지됩니다."', '"Long-term care insurance is 12.95% of the health insurance premium and is billed together with health insurance."'),
    ('"지역가입자 건강보험료는 어떻게 계산되나요?"', '"How is health insurance calculated for regional subscribers?"'),
    ('"지역가입자는 소득, 재산, 자동차를 종합한 점수제로 계산됩니다. 정확한 금액은 국민건강보험공단에서 확인하세요."', '"Regional subscribers use an income, property, and vehicle point system. Contact NHIS (nhis.or.kr) for accurate figures."'),
    # brokerage
    ('"부동산 중개수수료 상한요율은?"', '"What are the maximum brokerage fee rates?"'),
    ('"매매는 0.4~0.7%, 전·월세는 0.3~0.6%의 상한요율이 적용됩니다."', '"Purchase transactions: max 0.4–0.7%; jeonse/monthly rent: max 0.3–0.6%."'),
    ('"중개수수료는 협의가 가능한가요?"', '"Can the brokerage fee be negotiated?"'),
    ('"상한요율 이하에서 중개인과 협의 가능하며, 상한을 초과하는 것은 불법입니다."', '"Yes, you can negotiate below the maximum rate. Charging above the cap is illegal."'),
    ('"매매와 전세 수수료가 다른가요?"', '"Are purchase and jeonse brokerage fees different?"'),
    ('"네. 매매가 전세보다 상한요율이 높습니다."', '"Yes. Purchase transactions have higher maximum rates than jeonse."'),
    # electricity
    ('"전기요금 누진세란?"', '"What is a progressive electricity rate?"'),
    ('"사용량이 많을수록 단가가 올라가는 구조로, 주택용은 3단계 누진 요금제가 적용됩니다."', '"The unit price increases with usage. Residential electricity in Korea has a 3-tier progressive rate."'),
    ('"여름·겨울 요금이 다른가요?"', '"Are summer and winter rates different?"'),
    ('"네. 하계(7~8월)와 동계(12~2월)에는 계절별 할증이 적용될 수 있습니다."', '"Yes. Summer (Jul–Aug) and winter (Dec–Feb) may carry seasonal surcharges."'),
    ('"실제 청구 금액과 차이가 날 수 있나요?"', '"Can the calculated amount differ from my actual bill?"'),
    ('"복지 할인, 연료비 조정액 등이 반영되지 않아 실제 금액과 다를 수 있습니다."', '"Yes. Welfare discounts, fuel cost adjustments, and other fees are not included."'),
    # area
    ('"평과 m² 환산은?"', '"How do I convert pyeong to m²?"'),
    ('"1평 = 3.30579m²입니다."', '"1 pyeong = 3.30579 m²."'),
    ('"에이커는 몇 평인가요?"', '"How many pyeong is 1 acre?"'),
    ('"1에이커 ≈ 1,224평입니다."', '"1 acre ≈ 1,224 pyeong."'),
    ('"평방피트와 m² 환산은?"', '"How do I convert square feet to m²?"'),
    ('"1ft² ≈ 0.0929m²입니다."', '"1 sq ft ≈ 0.0929 m²."'),
    # apartment-score
    ('"청약 가점제란 무엇인가요?"', '"What is the Korean housing subscription priority system?"'),
    ('"무주택 기간, 부양가족 수, 청약통장 가입 기간에 따라 점수를 부여하고 높은 점수 순으로 당첨자를 선정하는 방식으로 최대 84점입니다."', '"A priority system awarding points for housing-free period, dependents, and subscription tenure. Winners selected by descending score. Max 84 points."'),
    ('"무주택기간은 어떻게 산정하나요?"', '"How is the housing-free period calculated?"'),
    ('"세대 구성원 전원이 주택을 소유하지 않은 기간 기준이며, 만 30세 미만 미혼은 만 30세 또는 혼인신고일부터 산정합니다."', '"Based on the period all household members have owned no housing. For unmarried persons under 30, the period starts from age 30 or marriage registration."'),
    ('"가점이 낮으면 청약을 못 하나요?"', '"Can I still apply with a low score?"'),
    ('"85㎡ 초과 중대형이나 민간분양 추첨제 물량은 가점과 무관하게 청약할 수 있습니다."', '"Units over 85㎡ and private-sector lottery allocations can be applied for regardless of your score."'),

    # ── temperature page exact strings ──
    ('<p>섭씨·화씨·켈빈 온도를 실시간으로 변환합니다</p>', '<p>Convert between Celsius, Fahrenheit, and Kelvin in real time</p>'),
    ('<div class="unit-label">섭씨 (°C)</div>', '<div class="unit-label">Celsius (°C)</div>'),
    ('<div class="unit-label">화씨 (°F)</div>', '<div class="unit-label">Fahrenheit (°F)</div>'),
    ('<div class="unit-label">켈빈 (K)</div>', '<div class="unit-label">Kelvin (K)</div>'),
    ('<div class="tips-panel"><h3>💡 온도 변환 공식</h3><ul>', '<div class="tips-panel"><h3>💡 Temperature Conversion Formulas</h3><ul>'),
    ('<li>체온: 36.5°C = 97.7°F</li>', '<li>Body temperature: 36.5°C = 97.7°F</li>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">°F = °C × 9/5 + 32, °C = (°F - 32) × 5/9입니다. 체온 37°C는 98.6°F입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">°F = °C × 9/5 + 32; °C = (°F − 32) × 5/9. Body temperature 37°C = 98.6°F.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">켈빈(K)이란 무엇인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the Kelvin scale?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">절대온도 단위로, 물리학·화학에서 주로 사용합니다. 0K = -273.15°C이며 음수가 없는 온도 척도입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Kelvin is the absolute temperature scale used in physics and chemistry. 0 K = −273.15°C; there are no negative Kelvin values.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">영하 온도도 변환 가능한가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Can I convert below-zero temperatures?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 영하 온도도 동일한 공식으로 변환됩니다. -40°C는 -40°F로 두 단위가 일치하는 특별한 온도입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. The same formula applies. Notably, −40°C equals −40°F — the one temperature where both scales agree.</p>'),

    # ── length page JS labels ──
    ("  {key:'mm',label:'밀리미터 (mm)',factor:0.001},", "  {key:'mm',label:'Millimeter (mm)',factor:0.001},"),
    ("  {key:'cm',label:'센티미터 (cm)',factor:0.01},", "  {key:'cm',label:'Centimeter (cm)',factor:0.01},"),
    ("  {key:'m',label:'미터 (m)',factor:1},", "  {key:'m',label:'Meter (m)',factor:1},"),
    ("  {key:'km',label:'킬로미터 (km)',factor:1000},", "  {key:'km',label:'Kilometer (km)',factor:1000},"),
    ("  {key:'inch',label:'인치 (inch)',factor:0.0254},", "  {key:'inch',label:'Inch (in)',factor:0.0254},"),
    ("  {key:'ft',label:'피트 (ft)',factor:0.3048},", "  {key:'ft',label:'Foot (ft)',factor:0.3048},"),
    ("  {key:'yard',label:'야드 (yard)',factor:0.9144},", "  {key:'yard',label:'Yard (yd)',factor:0.9144},"),
    ("  {key:'mile',label:'마일 (mile)',factor:1609.344}", "  {key:'mile',label:'Mile (mi)',factor:1609.344}"),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">인치와 센티미터 환산은?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How do I convert inches to centimeters?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1인치 = 2.54cm입니다. 예를 들어 6인치는 15.24cm입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 inch = 2.54 cm. For example, 6 inches = 15.24 cm.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">마일과 킬로미터 환산은?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How do I convert miles to kilometers?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1마일 ≈ 1.60934km입니다. 미국 도로 표지판의 마일을 킬로미터로 바꿀 때 유용합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 mile ≈ 1.60934 km. Useful for converting US road sign distances to kilometers.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">피트와 미터 환산은?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How do I convert feet to meters?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1피트 = 0.3048m입니다. 170cm는 약 5피트 7인치에 해당합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 foot = 0.3048 m. 170 cm ≈ 5 feet 7 inches.</p>'),

    # ── weight page JS labels and FAQs ──
    ("  {key:'mg',label:'밀리그램 (mg)',factor:0.001},", "  {key:'mg',label:'Milligram (mg)',factor:0.001},"),
    ("  {key:'g',label:'그램 (g)',factor:1},", "  {key:'g',label:'Gram (g)',factor:1},"),
    ("  {key:'kg',label:'킬로그램 (kg)',factor:1000},", "  {key:'kg',label:'Kilogram (kg)',factor:1000},"),
    ("  {key:'ton',label:'톤 (ton)',factor:1000000},", "  {key:'ton',label:'Metric Ton (t)',factor:1000000},"),
    ("  {key:'oz',label:'온스 (oz)',factor:28.3495},", "  {key:'oz',label:'Ounce (oz)',factor:28.3495},"),
    ("  {key:'lb',label:'파운드 (lb)',factor:453.592}", "  {key:'lb',label:'Pound (lb)',factor:453.592}"),
    ('<li>1 oz (온스) = 28.3495 g</li>', '<li>1 oz (ounce) = 28.3495 g</li>'),
    ('<li>1 lb (파운드) = 453.592 g = 약 0.4536 kg</li>', '<li>1 lb (pound) = 453.592 g ≈ 0.4536 kg</li>'),
    ('<li>1 ton (톤) = 1,000 kg</li>', '<li>1 ton (metric) = 1,000 kg</li>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1파운드 = 약 0.4536kg입니다. 체중 150파운드는 약 68kg입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 pound ≈ 0.4536 kg. Body weight of 150 lb ≈ 68 kg.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">온스는 몇 그램인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How many grams is an ounce?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1온스(oz) = 약 28.35g입니다. 음식 레시피나 금 무게 표기에 자주 사용됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 ounce (oz) ≈ 28.35 g. Commonly used in food recipes and gold weight measurement.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">돈(貫)과 그램 변환은?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">How do I convert don (Korean gold unit) to grams?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">귀금속에서 사용하는 1돈 = 3.75g입니다. 금 시세 계산 시 자주 활용됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 don (Korean precious metal unit) = 3.75 g. Frequently used when calculating gold prices.</p>'),

    # ── data-size page JS labels and FAQs ──
    ("  {key:'bit',label:'비트 (bit)',factor:1},", "  {key:'bit',label:'Bit (bit)',factor:1},"),
    ("  {key:'byte',label:'바이트 (byte)',factor:8},", "  {key:'byte',label:'Byte (B)',factor:8},"),
    ("  {key:'kb',label:'킬로바이트 (KB)',factor:8*1024},", "  {key:'kb',label:'Kilobyte (KB)',factor:8*1024},"),
    ("  {key:'mb',label:'메가바이트 (MB)',factor:8*1024*1024},", "  {key:'mb',label:'Megabyte (MB)',factor:8*1024*1024},"),
    ("  {key:'gb',label:'기가바이트 (GB)',factor:8*1024*1024*1024},", "  {key:'gb',label:'Gigabyte (GB)',factor:8*1024*1024*1024},"),
    ("  {key:'tb',label:'테라바이트 (TB)',factor:8*1024*1024*1024*1024},", "  {key:'tb',label:'Terabyte (TB)',factor:8*1024*1024*1024*1024},"),
    ("  {key:'pb',label:'페타바이트 (PB)',factor:8*1024*1024*1024*1024*1024}", "  {key:'pb',label:'Petabyte (PB)',factor:8*1024*1024*1024*1024*1024}"),
    ('<li>1 KB = 1,024 byte (이진법 기준)</li>', '<li>1 KB = 1,024 bytes (binary)</li>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">GB와 GiB의 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between GB and GiB?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">GB(기가바이트)는 10³ = 1,000³ 기준(10진수), GiB(기비바이트)는 2³⁰ = 1,073,741,824 기준(2진수)입니다. 하드디스크는 GB(10진수), OS는 GiB(2진수) 기준으로 표기하는 경우가 많습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">GB (gigabyte) uses 10³ = 1,000³ (decimal); GiB (gibibyte) uses 2³⁰ = 1,073,741,824 (binary). Hard drives typically use decimal GB; operating systems often display binary GiB.</p>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1TB = 1,000GB(10진수 기준)입니다. 2진수 기준으로는 약 931GiB입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">1 TB = 1,000 GB (decimal). In binary terms, 1 TB ≈ 931 GiB.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Mbps와 MB/s의 차이는?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the difference between Mbps and MB/s?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Mbps(메가비트/초)는 인터넷 속도, MB/s(메가바이트/초)는 파일 전송 속도에 사용됩니다. 100Mbps = 약 12.5MB/s입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Mbps (megabits/second) measures internet speed; MB/s (megabytes/second) measures file transfer speed. 100 Mbps ≈ 12.5 MB/s.</p>'),

    # ── brokerage exact FAQs ──
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">부동산 중개수수료 상한요율은?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What are the maximum brokerage fee rates?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">2021년 10월부터 개편되어 매매는 거래금액에 따라 0.4~0.7%, 전·월세는 0.3~0.6%의 상한요율이 적용됩니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Revised from October 2021: purchase transactions have max rates of 0.4–0.7% depending on amount; jeonse/monthly rent have max rates of 0.3–0.6%.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">중개수수료는 협의가 가능한가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Can the brokerage fee be negotiated?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 상한요율 이하에서 중개인과 협의해 수수료를 낮출 수 있습니다. 상한요율을 초과하는 것은 불법입니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. You can negotiate below the maximum rate with the agent. Charging above the cap is illegal.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">매매와 전세 수수료가 다른가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Are brokerage fees different for purchase vs. jeonse?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">네. 매매는 전세보다 상한 요율이 높게 설정되어 있으며, 거래 금액 구간별로 상한요율이 달라집니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Yes. Purchase transactions have higher maximum rates than jeonse, and rates vary by transaction amount tier.</p>'),
    ("  if(!priceMan){alert('거래금액을 입력해주세요.');return;}", "  if(!priceMan){alert('Please enter the transaction amount.');return;}"),
    ('    // 매매', '    // Purchase'),
    ('    // 전세', '    // Jeonse'),
    ('    // 월세 (환산금액으로 구간 판단, 수수료는 환산금액 기준)', '    // Monthly rent (tier based on equivalent amount)'),

    # ── percentage page p description ──
    ('<p>퍼센트(%) 계산, 비율, 증감률을 간편하게 계산합니다</p>', '<p>Calculate percentages, ratios, and percentage changes easily</p>'),
    ('<p>퍼센트(%) 계산, 비율, Percentage Change 모두 지원</p>', '<p>All percentage calculations: Y% of X, ratio, and percentage change</p>'),
    ('<p>세 가지 방식의 백분율 계산을 모두 지원합니다</p>', '<p>Supports all three types of percentage calculations in one place</p>'),
    # percentage inline form labels (exact source strings)
    ('<h3>1. X의 Y%는 얼마?</h3>', '<h3>1. What is Y% of X?</h3>'),
    ('<h3>2. X가 Y의 몇%인가?</h3>', '<h3>2. What % is X of Y?</h3>'),
    ('<h3>3. 증감률</h3>', '<h3>3. Percentage Change</h3>'),
    ('placeholder="X (이전)"', 'placeholder="X (old)"'),
    ('placeholder="Y (이후)"', 'placeholder="Y (new)"'),
    # bmi FAQ exact strings (these come BEFORE '정상' bare word replacement)
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">BMI 정상 범위는 얼마인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the normal BMI range?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">WHO 기준 18.5~24.9가 정상, 25 이상은 과체중, 30 이상은 비만으로 분류합니다. 한국은 23 이상을 과체중으로 보는 경우도 있습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">By WHO standards, 18.5–24.9 is normal; 25+ is overweight; 30+ is obese. In Korea, 23+ is sometimes classified as overweight.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">BMI가 높으면 무조건 비만인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Does a high BMI always mean obese?</summary>'),

    # ── health-insurance exact FAQ p texts ──
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">2025년 기준 건강보험료율은 보수월액의 7.09%이며, 직장가입자는 사업주와 근로자가 각 50%(3.545%)씩 부담합니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">As of 2025, the health insurance premium rate is 7.09% of monthly salary, split equally between employer and employee (3.545% each).</p>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">지역가입자는 소득, 재산, 자동차를 종합한 점수제로 계산됩니다. 이 계산기는 소득 기준 간략 계산이므로, 정확한 금액은 국민건강보험공단(nhis.or.kr)에서 확인하세요.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Regional subscribers use an income, property, and vehicle point system. This calculator uses simplified income-based estimation — check nhis.or.kr for accurate figures.</p>'),

    # ── savings page placeholder ──
    ('placeholder="예: 3.5"', 'placeholder="e.g. 3.5"'),
    ("  document.getElementById('resTax').textContent=tax?'-'+fmt(taxAmt)+'KRW':'0원';", "  document.getElementById('resTax').textContent=tax?'-'+fmt(taxAmt)+' KRW':'0 KRW';"),

    # ── calorie JS ──
    ("  document.getElementById('resDur').textContent=dur+'분 ('+hours.toFixed(1)+'시간)';", "  document.getElementById('resDur').textContent=dur+' min ('+hours.toFixed(1)+'h)';"),

    # ── severance JS ──
    ("  document.getElementById('resDays').textContent=fmt(days)+'일';", "  document.getElementById('resDays').textContent=fmt(days)+' days';"),
    ("  document.getElementById('resYears').textContent=years+'년';", "  document.getElementById('resYears').textContent=years+' years';"),
    ('placeholder="예: 9000000"', 'placeholder="e.g. 9000000"'),

    # ── electricity JS comments ──
    ('  // 기타계절 기준', '  // Non-summer season rates'),
    ('  // 하계는 동일 요금 체계 사용 (간소화)', '  // Summer uses same tier system (simplified)'),
    ('  // 기금은 10원 미만 절사', '  // Fund charge rounded down to nearest 10 KRW'),

    # ── bmi JS ──
    ("  else if(bmi<23)status='정상';", "  else if(bmi<23)status='Normal';"),

    # ── data-size FAQ exact text ──
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">GB(기가바이트)는 10³ = 1,000³ 기준(10진수), GiB(기비바이트)는 2³⁰ = 1,073,741,824 기준(2진수)입니다. 하드디스크는 GB(10진수), OS는 GiB(2진수) 기준으로 표기하는 경우가 많습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">GB (gigabyte) uses decimal (1,000³); GiB (gibibyte) uses binary (2³⁰ = 1,073,741,824). Hard drives typically use decimal GB; operating systems often display binary GiB.</p>'),

    # ── BMI FAQ exact texts ──
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">BMI 정상 범위는 얼마인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">What is the normal BMI range?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">WHO 기준 18.5~24.9가 정상, 25 이상은 과체중, 30 이상은 비만으로 분류합니다. 한국은 23 이상을 과체중으로 보는 경우도 있습니다.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">By WHO standards, 18.5–24.9 is normal; 25+ is overweight; 30+ is obese. In Korea, 23+ is sometimes classified as overweight.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">BMI가 높으면 무조건 비만인가요?</summary>', '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Does a high BMI always mean obese?</summary>'),
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">아닙니다. BMI는 체지방과 근육을 구분하지 못합니다. 근육량이 많은 운동선수도 BMI가 높게 나올 수 있으므로 참고 지표로만 활용하세요.</p>', '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Not always. BMI cannot distinguish fat from muscle. Athletes with high muscle mass can have a high BMI — use it as a general reference only.</p>'),
    # BMI JS
    ("  else status='고도비만';", "  else status='Severely Obese';"),

    # ── Post-bare-word BMI FAQ texts (과체중/비만 already replaced) ──
    # These match AFTER '과체중'→'Overweight' and '비만'→'Obese' bare-word replacements
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">WHO 기준 18.5~24.9가 정상, 25 이상은 Overweight, 30 이상은 Obese으로 분류합니다. 한국은 23 이상을 Overweight으로 보는 경우도 있습니다.</p>',
     '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">By WHO standards, 18.5–24.9 is normal; 25+ is overweight; 30+ is obese. In Korea, 23+ is sometimes classified as overweight.</p>'),
    ('<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">BMI가 높으면 무조건 Obese인가요?</summary>',
     '<summary style="cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none">Does a high BMI always mean I am obese?</summary>'),
    # bmi ld+json (after 과체중/비만 replacement)
    ('"WHO 기준 18.5~24.9가 정상이며, 25 이상은 Overweight, 30 이상은 Obese입니다."',
     '"By WHO standards, 18.5–24.9 is normal; 25+ is overweight; 30+ is obese."'),
    ('"아닙니다. BMI는 체지방과 근육을 구분하지 못해 근육량이 많은 경우 높게 나올 수 있습니다."',
     '"Not necessarily. BMI cannot distinguish fat from muscle — athletes with high muscle mass can have a high BMI."'),

    # ── Severance placeholder and ld+json ──
    ('placeholder="예: 1200"', 'placeholder="e.g. 1200"'),
    ('"1주 15시간 이상 근무, 계속 근로 1년 이상이면 퇴직금을 받을 수 있습니다."',
     '"You must work at least 15 hours per week continuously for 1 or more years to be entitled to severance pay."'),
    ('"퇴직 전 3개월 임금 총액을 해당 기간 총 일수로 나눈 금액입니다."',
     '"Total wages paid in the 3 months before resignation divided by the total calendar days in that period."'),
    ('"퇴직일로부터 14일 이내에 지급해야 합니다."',
     '"Severance pay must be made within 14 days of the last working day."'),

    # ── Percentage: p description (after 증감률→Percentage Change bare-word) ──
    ('<p>퍼센트(%) 계산, 비율, Percentage Change을 간편하게 계산합니다</p>',
     '<p>Calculate percentages, ratios, and percentage changes easily</p>'),
    # percentage FAQ p (no comma before 50% in source)
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">백분율은 비율 자체를 나타내고, 퍼센트포인트는 두 백분율의 차이를 나타냅니다. 금리가 2%에서 3%로 오르면 1pp 상승이지만 50% 증가입니다.</p>',
     '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">Percent expresses a ratio; percentage points measure the absolute difference between two percentages. A rise from 2% to 3% is a 1 pp increase but a 50% relative increase.</p>'),

    # ── Data-size exact p text (source: 하드디스크 제조사는 GB를 사용해 실제 용량이 작게 느껴집니다) ──
    ('<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">GB(기가바이트)는 10³ = 1,000³ 기준(10진수), GiB(기비바이트)는 2³⁰ = 1,073,741,824 기준(2진수)입니다. 하드디스크 제조사는 GB를 사용해 실제 용량이 작게 느껴집니다.</p>',
     '<p style="margin:8px 0 0;color:#94a3b8;line-height:1.7">GB (gigabyte) uses decimal (1,000³); GiB (gibibyte) uses binary (2³⁰ = 1,073,741,824). Hard drive manufacturers use decimal GB, so drives appear slightly smaller than advertised.</p>'),
    # data-size ld+json compact answers
    ('"GB는 10진수(1,000³), GiB는 2진수(2³⁰) 기준입니다."',
     '"GB uses decimal (1,000³); GiB uses binary (2³⁰)."'),
    ('"1TB = 1,000GB(10진수 기준)입니다."',
     '"1 TB = 1,000 GB (decimal)."'),
    ('"Mbps는 비트 단위 속도, MB/s는 바이트 단위 속도입니다. 100Mbps ≈ 12.5MB/s입니다."',
     '"Mbps = network speed in bits/s; MB/s = file transfer speed in bytes/s. 100 Mbps ≈ 12.5 MB/s."'),

    # ── Area JS labels ──
    ("{key:'pyeong',label:'평',factor:3.30579},", "{key:'pyeong',label:'Pyeong',factor:3.30579},"),
    ("{key:'hectare',label:'헥타르 (ha)',factor:10000},", "{key:'hectare',label:'Hectare (ha)',factor:10000},"),
    ("{key:'acre',label:'에이커 (ac)',factor:4046.86}", "{key:'acre',label:'Acre (ac)',factor:4046.86}"),

    # ── Weight ld+json compact answers ──
    ('"1파운드 ≈ 0.4536kg입니다."', '"1 pound ≈ 0.4536 kg."'),
    ('"1온스(oz) ≈ 28.35g입니다."', '"1 ounce (oz) ≈ 28.35 g."'),
    ('"1돈 = 3.75g입니다."', '"1 don (Korean precious metal unit) = 3.75 g."'),

    # ── Length ld+json compact answers ──
    ('"1인치 = 2.54cm입니다."', '"1 inch = 2.54 cm."'),
    ('"1마일 ≈ 1.60934km입니다."', '"1 mile ≈ 1.60934 km."'),
    ('"1피트 = 0.3048m입니다."', '"1 foot = 0.3048 m."'),

    # ── Date-calc JS ternary Korean units ──
    ("+(unit==='days'?'일':unit==='months'?'개월':'년')",
     "+(unit==='days'?' days':unit==='months'?' months':' years')"),

    # ── about.html full body translation ──
    ('<h1>WooaCalc WooaCalc 소개</h1>', '<h1>About WooaCalc</h1>'),
    ('<p>생활에 필요한 모든 계산기를 무료로 제공합니다</p>', '<p>All the calculators you need for daily life, completely free</p>'),
    ('<h2>WooaCalc이란?</h2>', '<h2>What is WooaCalc?</h2>'),
    ('<p>WooaCalc(WooaCalc)은 일상생활에서 자주 필요한 계산을 한 곳에서 무료로 할 수 있는 온라인 계산기 모음 서비스입니다. 회원가입이나 프로그램 설치 없이 브라우저에서 바로 사용할 수 있으며, 입력한 데이터는 서버로 전송되지 않아 개인정보가 안전합니다.</p>',
     '<p>WooaCalc is a free collection of online calculators covering everyday calculation needs — all in one place. No sign-up or installation required; everything runs directly in your browser, and no data is ever sent to a server.</p>'),
    ('<h2>제공 계산기 (19종)</h2>', '<h2>Available Calculators (25+)</h2>'),
    ('<li><strong>금융 계산기:</strong> 대출이자 계산기, 적금이자 계산기, 연봉 실수령액 계산기, 퇴직금 계산기</li>',
     '<li><strong>Finance:</strong> Loan Interest, Savings, Salary Take-Home, Severance Pay, Exchange Rate, Compound Interest, VAT, Brokerage Fee, Health Insurance</li>'),
    ('<li><strong>건강 계산기:</strong> BMI 계산기, 기초대사량(BMR/TDEE) 계산기, 칼로리 소모 계산기</li>',
     '<li><strong>Health:</strong> BMI Calculator, BMR/TDEE Calculator, Calorie Burn Calculator</li>'),
    ('<li><strong>날짜 계산기:</strong> D-Day 계산기, 날짜 계산기 (기간/더하기), 나이 계산기</li>',
     '<li><strong>Date:</strong> D-Day Calculator, Date Duration / Add-Subtract Calculator, Age Calculator</li>'),
    ('<li><strong>단위 변환:</strong> 길이, 무게, 온도, 넓이, 데이터 용량 변환기</li>',
     '<li><strong>Unit Converters:</strong> Length, Weight, Temperature, Area, Data Size</li>'),
    ('<li><strong>생활 계산기:</strong> 백분율 계산기, 연비 계산기, 전기요금 계산기, 중개수수료 계산기</li>',
     '<li><strong>Life:</strong> Percentage Calculator, Fuel Economy Calculator, Electricity Bill Calculator, Housing Score Calculator</li>'),
    ('<h2>특징</h2>', '<h2>Features</h2>'),
    ('<li>100% 무료 — 모든 기능을 제한 없이 사용</li>', '<li>100% Free — all features, no restrictions</li>'),
    ('<li>개인정보 안전 — 모든 계산은 브라우저에서 처리, 서버 전송 없음</li>', '<li>Privacy-safe — all calculations happen locally, nothing sent to a server</li>'),
    ('<li>모바일 최적화 — 스마트폰, 태블릿에서도 편리하게 사용</li>', '<li>Mobile-optimized — works great on smartphones and tablets</li>'),
    ('<li>즉시 사용 — 회원가입, 로그인, 설치 불필요</li>', '<li>Instant — no sign-up, no login, no installation needed</li>'),
    ('<h2>WooaHouse Services 패밀리</h2>', '<h2>WooaHouse Services Family</h2>'),
    ('<p>WooaCalc은 WooaHouse Services의 일원입니다. 다양한 무료 웹 도구를 만나보세요:</p>',
     '<p>WooaCalc is part of WooaHouse Services. Discover our other free web tools:</p>'),
    ('<li><a href="https://wooahouse.com/" target="_blank">WooaHouse</a> — 유용한 사이트 링크 큐레이션</li>',
     '<li><a href="https://wooahouse.com/" target="_blank">WooaHouse</a> — Curated links to useful websites</li>'),
    ('<li><a href="https://pdfkit.wooahouse.com/" target="_blank">PDFKit</a> — 브라우저 기반 PDF 도구 모음</li>',
     '<li><a href="https://pdfkit.wooahouse.com/" target="_blank">WooaPDF</a> — Browser-based PDF tools</li>'),
    ('<li><a href="https://imagekit.wooahouse.com/" target="_blank">WooaImage</a> — 이미지 압축·변환·편집 도구</li>',
     '<li><a href="https://imagekit.wooahouse.com/" target="_blank">WooaImage</a> — Image compress, convert & edit tools</li>'),
    ('<li><a href="https://colorkit.wooahouse.com/" target="_blank">WooaColor</a> — 색상 변환·팔레트·그라디언트 도구</li>',
     '<li><a href="https://colorkit.wooahouse.com/" target="_blank">WooaColor</a> — Color conversion, palette & gradient tools</li>'),
    ('<li><a href="https://textkit.wooahouse.com/" target="_blank">WooaText</a> — 텍스트 분석·변환·생성 도구</li>',
     '<li><a href="https://textkit.wooahouse.com/" target="_blank">WooaText</a> — Text analysis, conversion & generation tools</li>'),
    ('<li><a href="https://qrkit.wooahouse.com/" target="_blank">WooaQR</a> — QR코드 생성·읽기 도구</li>',
     '<li><a href="https://qrkit.wooahouse.com/" target="_blank">WooaQR</a> — QR code generator & reader</li>'),
    ('<li> — Steam 실시간 할인·인기 순위</li>', ''),
    ('<li> — Chrome 확장 프로그램 큐레이션</li>', ''),
    ('<li><a href="https://fontkit.wooahouse.com/" target="_blank">WooaFont</a> — 무료 상업용 폰트 큐레이션</li>',
     '<li><a href="https://fontkit.wooahouse.com/" target="_blank">WooaFont</a> — Free commercial font curation</li>'),
    ('<li><a href="https://vskit.wooahouse.com/" target="_blank">WooaVS</a> — VS Code 확장 프로그램 큐레이션</li>',
     '<li><a href="https://vskit.wooahouse.com/" target="_blank">WooaVS</a> — VS Code extension curation</li>'),
    ('<li><a href="https://mactools.wooahouse.com/" target="_blank">WooaMac</a> — Mac 필수 앱 다운로드 허브</li>',
     '<li><a href="https://mactools.wooahouse.com/" target="_blank">WooaMac</a> — Essential Mac app download hub</li>'),
    ('<li><a href="https://pctools.wooahouse.com/" target="_blank">WooaPC</a> — PC 필수 프로그램 다운로드 허브</li>',
     '<li><a href="https://pctools.wooahouse.com/" target="_blank">WooaPC</a> — Essential PC software download hub</li>'),

    # ── privacy.html full body translation ──
    ('<div class="breadcrumb"><a href="/">홈</a><span>›</span>개인정보처리방침</div>',
     '<div class="breadcrumb"><a href="/">Home</a><span>›</span>Privacy Policy</div>'),
    ('<h1 style="font-size:1.5rem;font-weight:800;margin-bottom:24px">개인정보처리방침</h1>',
     '<h1 style="font-size:1.5rem;font-weight:800;margin-bottom:24px">Privacy Policy</h1>'),
    ('<p style="color:#6B7280;margin-bottom:24px">시행일: 2026년 3월 21일</p>',
     '<p style="color:#6B7280;margin-bottom:24px">Effective Date: March 21, 2026</p>'),
    ('<h2 style="font-size:1.1rem;font-weight:700;margin:24px 0 12px">1. 개인정보의 수집 및 이용</h2>',
     '<h2 style="font-size:1.1rem;font-weight:700;margin:24px 0 12px">1. Collection and Use of Personal Information</h2>'),
    ('<p>WooaCalc(WooaCalc, 이하 "서비스")은 별도의 회원가입 절차가 없으며, 이용자의 개인정보를 수집하지 않습니다. 서비스에서 입력하는 모든 데이터(숫자, 날짜 등)는 이용자의 브라우저에서만 처리되며, 서버로 전송되지 않습니다.</p>',
     '<p>WooaCalc (the "Service") does not require account registration and does not collect any personal information. All data you enter (numbers, dates, etc.) is processed solely within your browser and is never transmitted to any server.</p>'),
    ('<h2 style="font-size:1.1rem;font-weight:700;margin:24px 0 12px">2. 쿠키 및 로컬 스토리지</h2>',
     '<h2 style="font-size:1.1rem;font-weight:700;margin:24px 0 12px">2. Cookies and Local Storage</h2>'),
    ('<p>서비스는 D-Day 저장 기능 등 일부 기능에서 브라우저의 로컬 스토리지(localStorage)를 사용합니다. 이 데이터는 이용자의 기기에만 저장되며, 서버로 전송되지 않습니다. 브라우저 설정에서 언제든지 삭제할 수 있습니다.</p>',
     '<p>The Service uses browser localStorage for features such as D-Day storage. This data is stored only on your device and is never sent to a server. You can delete it at any time through your browser settings.</p>'),
    ('<h2 style="font-size:1.1rem;font-weight:700;margin:24px 0 12px">3. 제3자 서비스</h2>',
     '<h2 style="font-size:1.1rem;font-weight:700;margin:24px 0 12px">3. Third-Party Services</h2>'),
    ('<p>서비스는 다음의 제3자 서비스를 이용합니다:</p>', '<p>The Service uses the following third-party services:</p>'),
    ('<li><strong>Google AdSense:</strong> 광고 제공을 위해 쿠키를 사용할 수 있습니다. Google의 광고 쿠키 사용에 대한 자세한 내용은 <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">Google 광고 정책</a>을 참조하세요.</li>',
     '<li><strong>Google AdSense:</strong> May use cookies to serve ads. See <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">Google Advertising Policies</a> for details.</li>'),
    ('<li><strong>Google Fonts:</strong> 웹 폰트 제공을 위해 사용됩니다.</li>',
     '<li><strong>Google Fonts:</strong> Used to serve web fonts.</li>'),
    ('<h2 style="font-size:1.1rem;font-weight:700;margin:24px 0 12px">4. 데이터 보안</h2>',
     '<h2 style="font-size:1.1rem;font-weight:700;margin:24px 0 12px">4. Data Security</h2>'),
    ('<p>모든 계산 로직은 이용자의 브라우저에서 JavaScript로 처리됩니다. 입력한 데이터는 외부 서버로 전송되지 않으므로 데이터 유출의 위험이 없습니다.</p>',
     '<p>All calculation logic runs locally in JavaScript within your browser. No data is transmitted to any external server, eliminating any risk of data leakage.</p>'),
    ('<h2 style="font-size:1.1rem;font-weight:700;margin:24px 0 12px">5. 이용자의 권리</h2>',
     '<h2 style="font-size:1.1rem;font-weight:700;margin:24px 0 12px">5. Your Rights</h2>'),
    ('<p>이용자는 브라우저의 로컬 스토리지를 언제든지 삭제하여 저장된 데이터를 제거할 수 있습니다. 광고 쿠키의 경우 브라우저 쿠키 설정에서 관리할 수 있습니다.</p>',
     '<p>You can delete all locally stored data at any time by clearing your browser\'s local storage. Advertising cookies can be managed through your browser\'s cookie settings.</p>'),
    ('<h2 style="font-size:1.1rem;font-weight:700;margin:24px 0 12px">6. 개인정보처리방침의 변경</h2>',
     '<h2 style="font-size:1.1rem;font-weight:700;margin:24px 0 12px">6. Changes to This Policy</h2>'),
    ('<p>이 개인정보처리방침은 법령이나 서비스 변경에 따라 수정될 수 있으며, 변경 시 이 페이지에 공지합니다.</p>',
     '<p>This Privacy Policy may be updated to reflect changes in law or the Service. Any changes will be announced on this page.</p>'),
    ('<h2 style="font-size:1.1rem;font-weight:700;margin:24px 0 12px">7. 문의</h2>',
     '<h2 style="font-size:1.1rem;font-weight:700;margin:24px 0 12px">7. Contact</h2>'),
    ('<p>개인정보처리방침에 대한 문의는 서비스 내 연락처를 통해 가능합니다.</p>',
     '<p>For questions about this Privacy Policy, please contact us through the contact information provided on the Service.</p>'),

    # ── about.html og 태그 ──
    ('<meta property="og:title" content="서비스 소개 — WooaCalc WooaCalc">',
     '<meta property="og:title" content="About WooaCalc — Free Online Calculators">'),
    ('<meta property="og:description" content="20가지 무료 온라인 계산기를 제공하는 WooaCalc을 소개합니다.">',
     '<meta property="og:description" content="Learn about WooaCalc — 25+ free online calculators for loan, BMI, salary, date and unit conversion.">'),

    # ── privacy.html 순서충돌 수정 (삭제→Delete 후 남은 한글) ──
    ('<p>서비스는 D-Day 저장 기능 등 일부 기능에서 브라우저의 로컬 스토리지(localStorage)를 사용합니다. 이 데이터는 이용자의 기기에만 저장되며, 서버로 전송되지 않습니다. 브라우저 설정에서 언제든지 Delete할 수 있습니다.</p>',
     '<p>Some features, such as D-Day saving, use the browser\'s local storage (localStorage). This data is stored only on your device and is never sent to a server. You can delete it at any time from your browser settings.</p>'),
    ('<p>이용자는 브라우저의 로컬 스토리지를 언제든지 Delete하여 저장된 데이터를 제거할 수 있습니다. 광고 쿠키의 경우 브라우저 쿠키 설정에서 관리할 수 있습니다.</p>',
     '<p>You can delete all locally stored data at any time by clearing your browser\'s local storage. Advertising cookies can be managed through your browser\'s cookie settings.</p>'),

    # ── privacy.html og 태그 ──
    ('<meta property="og:title" content="개인정보처리방침 — WooaCalc WooaCalc">',
     '<meta property="og:title" content="Privacy Policy — WooaCalc">'),

    # ── keywords 한글 제거 ──
    ('청약가점계산기,청약점수,주택청약가점,무주택기간점수,부양가족점수,청약통장가입기간,청약가점제',
     'Korean housing subscription score, apartment lottery calculator, cheongak score, housing priority points, WooaCalc'),
    ('건강보험료계산기,건강보험료,장기요양보험료,직장가입자,본인부담금,2025건강보험',
     'Korean health insurance calculator, NHIS premium, long-term care insurance, employee insurance 2025, WooaCalc'),
    ('연봉계산기,연봉실수령액,월급계산기,4대보험,소득세,실수령액',
     'Korean salary calculator, take-home pay, net salary, income tax Korea, social insurance deduction, WooaCalc'),
    ('퇴직금계산기,퇴직금,평균임금,근속연수,퇴직금산출',
     'Korean severance pay calculator, retirement pay, average wage, tenure, statutory severance, WooaCalc'),
    ('부가세계산기,부가세,공급가액,VAT계산기,부가가치세,역산,합계금액',
     'VAT calculator Korea, value added tax, supply price, reverse VAT calculation, total amount, WooaCalc'),

    # ── about.html 본문 잔여 (순서충돌 폴백 포함) ──
    ('<li><strong>단위 변환:</strong> 길이, 무게, 온도, 넓이, Data Size Conversion기</li>',
     '<li><strong>Unit Converters:</strong> Length, Weight, Temperature, Area, Data Size</li>'),
]

# ── 3. 언어 선택기 CSS ────────────────────────────────────────────────────────
LANG_SWITCHER_CSS = """    .lang-switcher { display:flex; align-items:center; gap:4px; }
    .lang-switcher a { color:rgba(255,255,255,0.7); text-decoration:none; font-size:0.8rem; font-weight:600; padding:3px 8px; border-radius:12px; transition:background 0.15s; }
    .lang-switcher a.active { color:white; background:rgba(255,255,255,0.25); }
    .lang-switcher a:hover { color:white; background:rgba(255,255,255,0.18); }
    .lang-switcher span { color:rgba(255,255,255,0.3); font-size:0.75rem; }
"""

def build_page(filename, meta):
    ko_path = os.path.join(BASE, filename)
    en_path = os.path.join(EN_DIR, filename)

    with open(ko_path, encoding='utf-8') as f:
        html = f.read()

    # ── lang 속성 변경 ──
    html = re.sub(r'<html lang="ko">', '<html lang="en">', html)

    # ── 메타 태그 교체 ──
    _t = meta["title"]; html = re.sub(r'<title>[^<]+</title>', lambda m: f'<title>{_t}</title>', html)
    _d = meta["desc"]; html = re.sub(r'<meta name="description" content="[^"]*"', lambda m: f'<meta name="description" content="{_d}"', html)
    if meta.get("kw"):
        _k = meta["kw"]; html = re.sub(r'<meta name="keywords" content="[^"]*"', lambda m: f'<meta name="keywords" content="{_k}"', html)
    _ot = meta["og_title"]; html = re.sub(r'<meta property="og:title" content="[^"]*"', lambda m: f'<meta property="og:title" content="{_ot}"', html)
    _od = meta["og_desc"]; html = re.sub(r'<meta property="og:description" content="[^"]*"', lambda m: f'<meta property="og:description" content="{_od}"', html)
    html = re.sub(r'<meta property="og:url" content="[^"]*"',
                  f'<meta property="og:url" content="{SITE_URL}/en/{filename}"', html)
    html = re.sub(r'<link rel="canonical" href="[^"]*"',
                  f'<link rel="canonical" href="{SITE_URL}/en/{filename}"', html)

    # ── hreflang 추가 ──
    hreflang = (f'\n  <link rel="alternate" hreflang="ko" href="{SITE_URL}/{filename}">'
                f'\n  <link rel="alternate" hreflang="en" href="{SITE_URL}/en/{filename}">'
                f'\n  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/en/{filename}">')
    html = re.sub(r'(<link rel="canonical"[^>]*>)', r'\1' + hreflang, html)

    # ── ld+json 업데이트 ──
    if meta.get('app_name'):
        _an = meta["app_name"]
        html = re.sub(r'"name": "([^"]*[가-힣][^"]*)"',
                      lambda m: f'"name": "{_an}"', html)
        # compact JSON name field too
        html = re.sub(r'"name":"([^"]*[가-힣][^"]*)"',
                      lambda m: f'"name":"{_an}"', html)
    _desc = meta["desc"]
    html = re.sub(r'"description": "([^"]*[가-힣][^"]*)"',
                  lambda m: f'"description": "{_desc}"', html)
    html = re.sub(r'"description":"([^"]*[가-힣][^"]*)"',
                  lambda m: f'"description":"{_desc}"', html)
    html = re.sub(r'"url": "' + re.escape(SITE_URL) + r'/' + re.escape(filename) + '"',
                  f'"url": "{SITE_URL}/en/{filename}"', html)
    html = re.sub(r'"url":"' + re.escape(SITE_URL) + r'/' + re.escape(filename) + '"',
                  f'"url":"{SITE_URL}/en/{filename}"', html)
    html = re.sub(r'"inLanguage": "ko"', '"inLanguage": "en"', html)

    # ── h1 교체 ──
    if meta.get('h1'):
        _h1 = meta["h1"]
        replaced = re.sub(r'<h1 id="toolTitle">[^<]*</h1>',
                          lambda m: f'<h1 id="toolTitle">{_h1}</h1>', html)
        if replaced == html:
            replaced = re.sub(r'<h1>([^<]*)</h1>', lambda m: f'<h1>{_h1}</h1>', html, count=1)
        html = replaced

    # ── 공통 문자열 치환 ──
    for ko, en in COMMON:
        html = html.replace(ko, en)

    # ── 언어 선택기 CSS 삽입 ──
    if 'lang-switcher' not in html:
        if '</style>' in html:
            html = html.replace('</style>', LANG_SWITCHER_CSS + '</style>', 1)
        else:
            html = html.replace('</head>', f'<style>\n{LANG_SWITCHER_CSS}</style>\n</head>', 1)

    # ── 헤더에 언어 선택기 삽입 ──
    _en_hdr = (
        f'\n    <div class="header-right">\n'
        f'      <div class="lang-switcher">\n'
        f'        <a href="../{filename}">KO</a>\n'
        f'        <span>|</span>\n'
        f'        <a href="{filename}" class="active">EN</a>\n'
        f'      </div>\n'
        f'      <a href="../about.html" style="color:rgba(255,255,255,0.85); font-size:0.85rem; text-decoration:none; margin-left:8px;">About</a>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</header>'
    )
    if 'lang-switcher' in html:
        html = re.sub(
            r'\s*<div class="header-right">.*?</header>',
            _en_hdr, html, count=1, flags=re.DOTALL
        )
    else:
        html = re.sub(
            r'(\s*</div>\s*</header>)',
            _en_hdr, html, count=1
        )

    # ── 쿠팡 제거 ──
    html = re.sub(r'\s*<script src="https://ads-partners\.coupang\.com/g\.js"></script>\n?', '', html)
    html = re.sub(r'<script>\s*new PartnersCoupang\.G\([^)]*\);?\s*</script>', '', html)

    # ── og:locale 교체 ──
    html = html.replace('content="ko_KR"', 'content="en_US"')

    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'  OK en/{filename}')


def build_simple(filename, en_title, en_desc):
    """about.html / privacy.html 처리"""
    ko_path = os.path.join(BASE, filename)
    en_path = os.path.join(EN_DIR, filename)
    if not os.path.exists(ko_path):
        print(f'  SKIP {filename} not found')
        return

    with open(ko_path, encoding='utf-8') as f:
        html = f.read()

    html = re.sub(r'<html lang="ko">', '<html lang="en">', html)
    html = re.sub(r'<title>[^<]+</title>', f'<title>{en_title}</title>', html)
    html = re.sub(r'<meta name="description" content="[^"]*"',
                  f'<meta name="description" content="{en_desc}"', html)
    html = re.sub(r'<link rel="canonical" href="[^"]*"',
                  f'<link rel="canonical" href="{SITE_URL}/en/{filename}"', html)

    hreflang = (f'\n  <link rel="alternate" hreflang="ko" href="{SITE_URL}/{filename}">'
                f'\n  <link rel="alternate" hreflang="en" href="{SITE_URL}/en/{filename}">'
                f'\n  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/en/{filename}">')
    html = re.sub(r'(<link rel="canonical"[^>]*>)', r'\1' + hreflang, html)

    for ko, en in COMMON:
        html = html.replace(ko, en)

    if 'lang-switcher' not in html:
        if '</style>' in html:
            html = html.replace('</style>', LANG_SWITCHER_CSS + '</style>', 1)
        else:
            html = html.replace('</head>', f'<style>\n{LANG_SWITCHER_CSS}</style>\n</head>', 1)

    _en_hdr_simple = (
        f'\n    <div class="header-right">\n'
        f'      <div class="lang-switcher">\n'
        f'        <a href="../{filename}">KO</a>\n'
        f'        <span>|</span>\n'
        f'        <a href="{filename}" class="active">EN</a>\n'
        f'      </div>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</header>'
    )
    if 'lang-switcher' in html:
        html = re.sub(
            r'\s*<div class="header-right">.*?</header>',
            _en_hdr_simple, html, count=1, flags=re.DOTALL
        )
    else:
        html = re.sub(
            r'(\s*</div>\s*</header>)',
            _en_hdr_simple, html, count=1
        )

    html = re.sub(r'\s*<script src="https://ads-partners\.coupang\.com/g\.js"></script>\n?', '', html)
    html = re.sub(r'<script>\s*new PartnersCoupang\.G\([^)]*\);?\s*</script>', '', html)
    html = html.replace('content="ko_KR"', 'content="en_US"')

    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  OK en/{filename}')


# ── 4. 실행 ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('Building English pages for CalcKit...')

    for filename, meta in PAGE_META.items():
        ko_path = os.path.join(BASE, filename)
        if os.path.exists(ko_path):
            build_page(filename, meta)
        else:
            print(f'  SKIP {filename} not found')

    build_simple(
        'about.html',
        'About WooaCalc — Free Online Calculators',
        'WooaCalc is a free collection of 25+ browser-based calculators: loan interest, BMI, salary, D-Day, date, temperature, unit converters and more. No sign-up required.',
    )
    build_simple(
        'privacy.html',
        'Privacy Policy — WooaCalc',
        'WooaCalc privacy policy. All calculations happen locally in your browser. No personal data is stored or transmitted to any server.',
    )

    print('\nDone! Check en/ folder.')
