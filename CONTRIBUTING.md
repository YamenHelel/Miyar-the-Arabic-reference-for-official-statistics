# المساهمة في مِعيار · Contributing to Miʿyar

## بالعربية
مِعيار مرجع يبنيه إحصائيون عرب. أسهل طرق المساهمة:

1. **أبلغ عن خطأ أو عن إصدار أحدث لوثيقة.** افتح بلاغاً من نوع «تصحيح» في GitHub (Issues ← New issue ← تصحيح)، أو راسلنا على yamen.hlel@gmail.com. اذكر الصفحة، وما الخطأ، ورابط الوثيقة الرسمية.
2. **راجع ما يخص بلدك.** إن كنت تعمل أو عملت في جهاز إحصائي، يمكنك أن تتحقق من التعاريف الوطنية لبلدك. يُذكر اسم المراجع مع موافقته.
3. **اقترح مؤشراً أو مفهوماً** يحتاجه عملك اليومي.

قواعد لا تتغير:
- لا تعريف بلا مصدر.
- النص الرسمي يُنسخ حرفياً بلغته الأصلية.
- شرح الذكاء الاصطناعي يبقى موسوماً.
- لا بيانات شخصية ولا بيانات جزئية سرية.

## In English
Miʿyar is built by Arab statisticians. The easiest ways to help:

1. **Report an error or a newer edition of a document.** Open a "Correction" issue, or write to yamen.hlel@gmail.com, with the page, the problem and the link to the official document.
2. **Review your country.** If you work, or worked, in a national statistical office, help verify its definitions. Reviewers are credited with their consent.
3. **Suggest an indicator or concept** you need in your daily work.

Technical contributors: read [CLAUDE.md](CLAUDE.md) (it applies to humans too) and [docs/STATUS.md](docs/STATUS.md). Then:
- Run `python tools/validate.py` before any pull request.
- Run `python tools/build_site.py && python tools/check_seo.py --skip-images` for changes to the site.

Content is CC BY 4.0, code is MIT.
