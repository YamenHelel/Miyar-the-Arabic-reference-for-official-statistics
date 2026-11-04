# مكتبة شيفرة مِعيار · Miʿyar code library

## بالعربية
شيفرة جاهزة لحساب مؤشرات سوق العمل من البيانات الجزئية لمسح القوى العاملة، وفق قرار المؤتمر الدولي التاسع عشر لخبراء إحصاءات العمل (2013، المعدَّل في 2023)، مع الأوزان والأخطاء المعيارية.

**المؤشرات:**
- معدل المشاركة، ونسبة العمالة إلى السكان
- معدل البطالة (LU1) والمقاييس LU2 وLU3 وLU4
- بطالة الشباب، ونسبة الشباب خارج التعليم والعمل والتدريب (NEET)

لكل مؤشر: الخطأ المعياري، ومعامل الاختلاف، ومجال الثقة 95%، وأثر التصميم التقريبي.

**الإصدارات:**

| اللغة | الملف | الحالة |
|---|---|---|
| Python | `python/miyar_lfs.py` | مُختبَر (`tools/test_code.py`) |
| R | `r/miyar_lfs.R` (حزمة survey) | يُشغَّل في CI ويطابق نتائج Python |
| Stata | `stata/miyar_lfs.do` | **لم يُشغَّل**؛ كُتب ليطابق النسختين الأخريين |

**قواعد كل بلد:** الحد الأدنى للسن، ومدة البحث، ومدة الإتاحة تأتي من `presets/countries.json`. يبنيه مِعيار **فقط** من النصوص الرسمية المتحقق منها، وما لم يرد في النص يأخذ القيمة الافتراضية لمنظمة العمل الدولية، ويُعلن البرنامج ذلك عند التشغيل.

**البيانات التجريبية:** الملف `data/synthetic_lfs.csv` بيانات **مصطنعة** للاختبار والتدريب فقط، لا تمثل أي بلد.

## In English
**Quick start**
```bash
python code/python/miyar_lfs.py code/data/synthetic_lfs.csv --country jor --by sex
```

**Use it on your own LFS file.** Rename your variables to these names, or add a mapping step:

| variable | meaning |
|---|---|
| `stratum`, `psu`, `weight` | sample design: stratum, primary sampling unit, final weight |
| `age`, `sex`, `nationality` | demographics (any codes; used for disaggregation) |
| `in_education`, `in_training` | 1 if in formal education / training (for NEET) |
| `worked_1h` | 1 if worked at least one hour for pay or profit in the reference week |
| `temp_absent` | 1 if has a job but was temporarily absent |
| `searched_days` | days since the last active job-search step (empty if no search) |
| `available_days` | could start within N days after the reference week (0 = during it; empty if not available) |
| `future_starter` | 1 if has found a job that starts later |
| `wants_work` | 1 if would like to work |
| `hours_usual`, `wants_more_hours`, `available_more_hours` | for time-related underemployment |

Most national files store search and availability as categories, not days. Convert them, e.g. "within the next two weeks" → `14`. The conversion is where national rules matter; document it.

**Method and limitations**
- Standard errors use Taylor linearisation for ratios, with PSUs treated as sampled with replacement. This is the same as R `survey` with `svydesign(ids=~psu, strata=~stratum, weights=~weight)`. It ignores finite-population corrections and the variance effect of calibrating the weights. Replicate-weight methods are on the backlog.
- The design effect is approximate: design variance over p(1−p)/n with unweighted n.
- The hours threshold for time-related underemployment is a national choice. 35 is a placeholder until a country's text states its threshold.

**Tests:** `python tools/test_code.py` checks:
- identities (LF = E + U, LU1 ≤ LU2, LU3 ≤ LU4)
- the SE against the simple-random-sampling formula
- that country rules move the numbers in the right direction
- that every preset traces to a quotation

CI (`.github/workflows/code.yml`) also runs the R version and compares it with Python.

Licence: MIT (code). Cite: Miʿyar code library, https://github.com/YamenHelel/Miyar-the-Arabic-reference-for-official-statistics, accessed <date>.
