# Sense.py — Sensitivity Analysis of Transport Systems

## English

This script performs a **one-at-a-time (OAT) sensitivity analysis** of the M_b transport efficiency index across five transport modes: road, river, railway, aviation, and airships. It is part of a scientific study on transport system evaluation for the Republic of Sakha (Yakutia).

**How it works:**

For each of 21 input parameters (load capacity, speed, route distance, working hours, fuel consumption, fuel price, crew salary, infrastructure costs, revenue per ton-km, tax rate, vehicle cost, efficiency rate, risk components, constraint scores, wagon count, wagon cost), the script varies the parameter from −20% to +20% of its baseline value in 21 steps while keeping all other parameters fixed. For each step it computes M_b using the formula:

```
M_b = (Pr × Re) / (L × R × I)
```

It then calculates the **elasticity** of M_b with respect to each parameter using a central finite difference:

```
elasticity = (ΔM_b / M_b) / (Δparam / param)
```

**Output:** for every parameter, the script generates an HTML report with an interactive sensitivity curve chart (logarithmic scale), an elasticity ranking table, and a full M_b value table. All reports are linked in a single `index.html` navigation page saved to the `отчёты_по_параметрам/` folder.

**Interpretation:** elasticity > 0.5 indicates a highly sensitive parameter; 0.1–0.5 moderate; < 0.1 low sensitivity.

**Best used for:** identifying which input parameters most strongly drive transport system efficiency, supporting variable selection for Monte Carlo simulation (see SAKHA_case.py), and preparing sensitivity tables for scientific publication appendices.

**Requirements:** Python 3.8+, numpy, pandas, matplotlib.

---

## Русский

Скрипт выполняет **однофакторный анализ чувствительности (OAT)** показателя эффективности транспортной системы M_b по пяти видам транспорта: автомобильный, речной, железнодорожный, авиационный, дирижабли. Является частью научного исследования по оценке транспортных систем Республики Саха (Якутия).

**Принцип работы:**

Для каждого из 21 входного параметра (грузоподъёмность, скорость, дальность маршрута, рабочие часы, расход топлива, цена топлива, зарплата экипажа, стоимость инфраструктуры, тариф за тонно-км, ставка налога, стоимость транспортного средства, норматив эффективности, составляющие рисков, ограничения, количество вагонов, стоимость вагона) скрипт изменяет параметр от −20% до +20% от базового значения в 21 шаге, фиксируя остальные параметры. В каждой точке вычисляется M_b:

```
M_b = (Pr × Re) / (L × R × I)
```

Затем рассчитывается **эластичность** M_b по каждому параметру через центральную разность:

```
эластичность = (ΔM_b / M_b) / (Δпараметр / параметр)
```

**Результат:** для каждого параметра формируется HTML-отчёт с графиком кривой чувствительности (логарифмическая шкала), таблицей ранжирования по эластичности и полной таблицей значений M_b. Все отчёты объединены в навигационной странице `index.html` в папке `отчёты_по_параметрам/`.

**Интерпретация:** эластичность > 0.5 — высокочувствительный параметр; 0.1–0.5 — умеренная чувствительность; < 0.1 — низкая.

**Область применения:** выявление параметров, наиболее сильно влияющих на эффективность транспортной системы; обоснование выбора переменных для симуляции Монте-Карло (см. SAKHA_case.py); подготовка таблиц чувствительности для приложений к научным публикациям.

**Зависимости:** Python 3.8+, numpy, pandas, matplotlib.

---

## Монгол

Энэ скрипт нь таван төрлийн тээврийн хэрэгслэл (авто, голын, төмөр зам, нисэх онгоц, дирижабль) дахь M_b үр ашгийн үзүүлэлтийн **нэг хүчин зүйлийн мэдрэмжийн шинжилгээ (OAT)**-г гүйцэтгэдэг. Саха (Якут) Бүгд Найрамдах Улсын тээврийн систем үнэлэх шинжлэх ухааны судалгааны нэг хэсэг юм.

**Ажиллах зарчим:**

21 оролтын параметр (ачааны даац, хурд, маршрутын зай, ажлын цаг, түлшний зарцуулалт, түлшний үнэ, багийн цалин, дэд бүтцийн зардал, тонн-км тариф, татварын хувь, тээврийн хэрэгслийн өртөг, үр ашгийн норматив, эрсдэлийн бүрэлдэхүүн хэсгүүд, хязгаарлалтын оноо, вагоны тоо, вагоны өртөг) тус бүрийн хувьд бусад параметрүүдийг тогтмол барин, уг параметрийг суурь утгаасаа −20%-аас +20% хүртэл 21 алхамаар өөрчилнө. Тус бүр дэх M_b-г тооцно:

```
M_b = (Pr × Re) / (L × R × I)
```

Дараа нь төвийн ялгаврын аргаар **уян хатан чанар (эластичность)**-ийг тооцдог:

```
эластичность = (ΔM_b / M_b) / (Δпараметр / параметр)
```

**Гаралт:** Тус бүр параметрт мэдрэмжийн муруйн график (логарифм масштаб), эластичностийн жагсаалт, M_b-ийн бүрэн хүснэгт бүхий HTML тайлан үүсгэнэ. Бүх тайлан `отчёты_по_параметрам/` хавтсанд `index.html` навигацийн хуудсаар нэгтгэгдэнэ.

**Тайлбар:** эластичность > 0.5 — өндөр мэдрэмжтэй параметр; 0.1–0.5 — дунд зэрэг; < 0.1 — бага мэдрэмж.

**Хэрэглэх хамгийн тохиромжтой газар:** тээврийн системийн үр ашигт хамгийн их нөлөөлдөг параметрүүдийг тодорхойлох; Монте-Карло симуляцийн хувьсагчийн сонголтыг үндэслэх (SAKHA_case.py-г үзнэ үү); шинжлэх ухааны нийтлэлийн хавсралтад мэдрэмжийн хүснэгт бэлтгэх.

**Шаардлага:** Python 3.8+, numpy, pandas, matplotlib.
