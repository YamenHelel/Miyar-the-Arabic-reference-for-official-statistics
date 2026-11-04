# الترجيح والتقدير والخطأ المعياري — Weighting, estimation and standard errors / Pondération, estimation et erreurs-types

Miʿyar id: `ds-lfs-weighting-estimation` · LFS guide section · status: draft

## Summary — AI-ASSISTED

يحصل كل فرد في العينة على وزن يساوي عدد الأشخاص الذين يمثلهم. يُبنى الوزن على ثلاث خطوات: وزن التصميم (مقلوب احتمال السحب)، ثم تصحيح عدم الاستجابة، ثم المعايرة على تقديرات السكان حسب السن والجنس والمنطقة. وتُحسب المعدلات على أنها نسبة مجموعين مرجحين، ولكل معدل خطأ معياري يجب نشره.

## Official text: الأوزان في دليل منظمة العمل الدولية لمعالجة البيانات الجزئية

**Source:** ILOSTAT Microdata Processing Quick Guide — principles and methods for processing anonymized household survey microdata — ILO Department of Statistics  
**URL:** https://www.ilo.org/publications/ilostat-microdata-processing-quick-guide-principles-and-methods-underlying  
**Locator:** ILOSTAT Microdata Processing Quick Guide — the paragraph on survey weights (how ILO uses the national weights when deriving indicators)  
**Status:** NOT YET AVAILABLE — do not quote; say the official text is pending in Miʿyar.

## خطوات الترجيح — AI-ASSISTED

- وزن التصميم يساوي 1 ÷ احتمال سحب المسكن.
- تصحيح عدم الاستجابة يوزّع وزن الأسر التي لم تُجب على الأسر المشابهة لها التي أجابت.
- المعايرة تجعل مجموع الأوزان يطابق تقديرات السكان الرسمية. لذلك تتغير الأرقام المنشورة عند تحديث تقديرات السكان بعد تعداد.

## التقدير والخطأ المعياري — AI-ASSISTED

- معدل البطالة يساوي مجموع أوزان المتعطلين ÷ مجموع أوزان القوة العاملة. هو نسبة تقديرين، فيُحسب خطؤه المعياري بطريقة التقريب الخطي (Taylor) أو بالأوزان المكررة.
- تجاهل التصميم (الطبقات والعناقيد) يجعل الخطأ المعياري أصغر من حقيقته.
- مكتبة الشيفرة في مِعيار تطبق هذا بلغات Python وR وStata.

## Further reading (Miʿyar registry)

- ILOSTAT Microdata Processing Quick Guide — principles and methods for processing anonymized household survey microdata — ILO Department of Statistics — https://www.ilo.org/publications/ilostat-microdata-processing-quick-guide-principles-and-methods-underlying (status: link-ok)
- ILO guidelines and tools for aligning national LFS with latest ICLS standards and best practices (English page) — ILO Department of Statistics — https://ilostat.ilo.org/resources/ilo-guidelines-and-tools-for-aligning-national-labour-force-surveys-with-latest-icls-standards-and-best-practices/ (status: collected)
