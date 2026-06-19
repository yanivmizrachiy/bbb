# -*- coding: utf-8 -*-
import os, charts as C

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

# ---------- helpers (same engine as the uncertainty booklet) ----------
def L(x):
    return f'<span dir="ltr">{x}</span>'

def lines(n):
    return '<div class="lines">' + '<div class="ln"></div>' * n + '</div>'

def parts(items):
    out = ['<ol class="parts">']
    for it in items:
        lab, body = it[0], it[1]
        nl = it[2] if len(it) > 2 else 0
        out.append(f'<li><span class="plab">{lab}</span><div class="ptext">{body}{lines(nl) if nl else ""}</div></li>')
    out.append('</ol>')
    return "".join(out)

def mc(options):
    out = ['<div class="mc">']
    for lab, txt in options:
        out.append(f'<div class="opt"><span class="ol">{lab}</span><span class="ot">{txt}</span></div>')
    out.append('</div>')
    return "".join(out)

def table(headers, rows, cls="tbl"):
    out = [f'<table class="{cls}"><thead><tr>']
    for h in headers:
        out.append(f'<th>{h}</th>')
    out.append('</tr></thead><tbody>')
    for r in rows:
        out.append('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>')
    out.append('</tbody></table>')
    return "".join(out)

def fig(svg, cap=""):
    c = f'<div class="cap">{cap}</div>' if cap else ""
    return f'<div class="figure">{svg}{c}</div>'

def img(name, w=66, cap=""):
    c = f'<div class="cap">{cap}</div>' if cap else ""
    return f'<div class="figure"><img class="embed" src="assets/{name}.png" style="max-width:{w}%" alt="{name}">{c}</div>'

CARDS = []
_qcount = [0]
def Q(num, body, src="", grade=""):
    if isinstance(num, int):
        _qcount[0] += 1
        label = str(_qcount[0])
    else:
        label = num
    pill = f'<span class="pill">{src}</span>' if src else ""
    gp = f'<span class="pill grade">{grade}</span>' if grade else ""
    CARDS.append(f'<div class="q"><div class="qhead"><span class="qnum">{label}</span><div class="qtags">{src and pill}{gp}</div></div><div class="qbody">{body}</div></div>')

def SECTION(letter, title, subtitle, color):
    _qcount[0] = 0
    CARDS.append(f'<section class="topic" style="--c:{color}"><div class="sectionbar"><div class="secletter">{letter}</div><div><div class="sectitle">{title}</div><div class="secsub">{subtitle}</div></div></div>')

def ENDSEC():
    CARDS.append('</section>')

def note(html):
    CARDS.append(f'<div class="note">{html}</div>')

# =====================================================================
# SECTION A — משתנים וביטויים אלגבריים
# =====================================================================
SECTION("א", "משתנים וביטויים אלגבריים", "אלגברה · כיתה ז' · משתנה, ביטוי אלגברי והצבה", "#4f46e5")

Q(1, "קישוריות עם גאומטריה — היקף משולש שווה־צלעות:"
  + parts([("א.", "מהו היקפו של משולש שווה־צלעות שאורך צלעו " + L("5") + " ס\"מ? ושל אחד שאורך צלעו " + L("7") + " ס\"מ?", 1),
           ("ב.", "מהו היקפו של משולש שווה־צלעות שאורך צלעו " + L("m") + " ס\"מ? (כתבו ביטוי אלגברי)", 1)]))

Q(2, "מחיר ליטר דלק הוא " + L("7") + " שקלים."
  + parts([("א.", "מהי העלות של " + L("20") + " ליטרים? של " + L("30") + " ליטרים? של " + L("b") + " ליטרים? ומהי העלות כאשר " + L("b=40") + "?", 2),
           ("ב.", "בלילה (בין " + L("21:00") + " ל־" + L("06:00") + ") יש עמלה קבועה של " + L("2") + " שקלים לכל מילוי. רשמו ביטוי לעלות של " + L("b") + " ליטרים בלילה, וחשבו עבור " + L("b=40") + ".", 2)]))

Q(3, "לפניכם שלושת האיברים הראשונים (משמאל לימין) בסדרה של קבוצות סימנים:"
  + img("seq_a3", 60)
  + parts([("א.", "כמה סימנים יש בכל אחד מהאיברים המוצגים?", 1),
           ("ב.", "הציעו המשך לסדרה: כתבו שלושה איברים עוקבים.", 1),
           ("ג.", "בהנחה שהאיברים הם " + L("3, 5, 7, 9, 11, 13") + ", מהו האיבר ה־" + L("9") + " בסדרה?", 1),
           ("ד.", "מהו האיבר ה־" + L("58") + "? מהו האיבר ה־" + L("1000") + "?", 1),
           ("ה.", "כמה סימנים יש במקום ה־" + L("n") + "? (כתבו ביטוי אלגברי)", 1)]))

Q(4, "קופסה מכילה כדורים לבנים, סגולים ושחורים בלבד. מספר הכדורים הלבנים גדול פי " + L("4") + " ממספר הסגולים, "
  "ו־" + L("3") + " כדורים פחות ממספר השחורים. מספר הכדורים הסגולים מסומן ב־" + L("x") + "."
  + parts([("א.", "רשמו ביטוי אלגברי למספר הכדורים השחורים, וביטוי למספר הכדורים בקופסה כולה.", 2)]))

Q(5, "הגובה של מגדל הבנוי מ־" + L("4") + " כוסות הוא " + L("20") + " ס\"מ, והגובה של מגדל מ־" + L("6") + " כוסות הוא " + L("26") + " ס\"מ."
  + img("cups", 56)
  + parts([("א.", "בכמה ס\"מ גדל גובה המגדל כאשר מוסיפים כוס אחת?", 1),
           ("ב.", "רשמו ביטוי אלגברי לגובה (בס\"מ) של מגדל מ־" + L("n") + " כוסות.", 1)]))

Q(6, "ליובל יש פי שניים ספרים מאשר לעמית. לדוד יש שישה ספרים יותר מאשר לעמית. כמה ספרים יש לשלושתם יחד, אם לעמית יש:"
  + parts([("א.", L("5") + " ספרים", 1), ("ב.", L("10") + " ספרים", 1),
           ("ג.", L("50") + " ספרים", 1), ("ד.", L("x") + " ספרים (ביטוי אלגברי)", 1)]))

Q(7, "צלע אחת של מלבן ארוכה פי " + L("3") + " מהצלע השנייה."
  + parts([("א.", "מהו היקף המלבן כאשר אורך הצלע הקצרה הוא: " + L("5") + " ס\"מ · " + L("20") + " ס\"מ · " + L("35") + " ס\"מ · " + L("a") + " ס\"מ?", 2),
           ("ב.", "כתבו ביטוי אלגברי לשטח המלבן כאשר אורך הצלע הקצרה הוא " + L("a") + " ס\"מ.", 1)]))

Q(8, "צלע אחת של מלבן ארוכה ב־" + L("3") + " ס\"מ מהצלע השנייה."
  + parts([("א.", "כתבו ביטוי אלגברי המתאר את היקף המלבן.", 1),
           ("ב.", "כתבו ביטוי אלגברי המתאר את שטח המלבן.", 1)]))

Q(9, "מספר החולצות של הילה גדול ב־" + L("3") + " ממספר החולצות של חנה. " + L("n") + " מציין את מספר החולצות של הילה. "
  "רשמו ביטוי אלגברי למספר החולצות של חנה באמצעות " + L("n") + "." + lines(1))

Q(10, "אם " + L("t") + " הוא מספר בין " + L("6") + " ל־" + L("9") + ", אז " + L("t + 5") + " הוא מספר:"
  + mc([("א.", "בין " + L("1") + " ל־" + L("4")), ("ב.", "בין " + L("10") + " ל־" + L("13")),
        ("ג.", "בין " + L("11") + " ל־" + L("14")), ("ד.", "בין " + L("30") + " ל־" + L("45"))]))

Q(11, "מהם חמשת האיברים הראשונים של הסדרה שבמקום ה־" + L("n") + " שלה נמצא המספר " + L("3·n − 1") + "?" + lines(1))

Q(12, "הציבו בביטוי " + L("21 − 3a") + " את הערכים " + L("3, 4, 5") + " במקום המשתנה " + L("a") + ", וחשבו את ערכו המספרי בכל מקרה." + lines(2))

Q(13, "הציבו את המספרים " + L("1, 2, 3") + " במקום המשתנה " + L("t") + " בביטוי " + L("4t + 2 − 3t + 1") + "." + lines(2))

Q(14, "מִתחו קו בין ביטויים השווים זה לזה:"
  + img("match_expr", 60))

Q(15, "התאימו: הסבירו את סדר הפעולות שיש לבצע בכל ביטוי לאחר הצבת מספר במקום " + L("t") + ", "
  "והתאימו כל ביטוי לתיאור המילולי המתאים."
  + img("fig17", 72))

Q(16, "התבוננו בסדרת התמונות / הביטויים והשלימו לפי הנדרש:"
  + img("fig18", 78))

Q(17, "התאימו כל ביטוי לתיאור המילולי:"
  + parts([("i.", "הציון של נבו במבחן גבוה מהציון של חן ב־" + L("20") + " נקודות.", 0),
           ("ii.", "הלכנו " + L("10") + " ק\"מ, ואז המשכנו באופנוע במהירות " + L("20") + " קמ\"ש במשך זמן מה.", 0),
           ("iii.", "מחיר העגבניות התייקר ב־" + L("3") + " ₪ לק\"ג, וקניתי " + L("2") + " ק\"ג.", 0)])
  + "<p>הביטויים: " + L("t − 20") + " · " + L("20 + 10t") + " · " + L("2(t + 3)") + "</p>" + lines(1))

Q(18, "מחיר ק\"ג עגבניות בחנות הוא " + L("a") + " שקלים ומחיר ק\"ג מלפפונים הוא " + L("b") + " שקלים. "
  "כתבו ביטוי אלגברי לעלות הכוללת של " + L("3") + " ק\"ג עגבניות ו־" + L("2") + " ק\"ג מלפפונים." + lines(1))

Q(19, "מחיר ק\"ג עגבניות בשוק נמוך ב־" + L("2") + " שקלים ממחירו בחנות, ומחיר ק\"ג מלפפונים בשוק הוא " + L("3/4") + " ממחירו בחנות. "
  "כתבו ביטוי אלגברי לעלות הכוללת של " + L("3") + " ק\"ג עגבניות ו־" + L("2") + " ק\"ג מלפפונים בשוק." + lines(1))

Q(20, "ידוע כי " + L("a + b = 5") + ". חשבו:"
  + parts([("א.", L("(a + b)·2"), 1), ("ב.", L("2a + 2b − 4"), 1),
           ("ג.", L("a + b + 5"), 1), ("ד.", L("(a + b)(a + b)"), 1)]))

Q(21, "נתון ביטוי אלגברי " + L("5b − 1.5c") + ". מהו ערכו עבור:"
  + parts([("א.", L("b = 5, c = 1.5"), 1), ("ב.", L("b = 2, c = −3"), 1),
           ("ג.", L("b = −4, c = 3.75"), 1), ("ד.", L("b = 0, c = −9"), 1)]))

Q(22, "נתון ביטוי אלגברי " + L("h³ + 4k² − 4") + ". מהו ערכו עבור:"
  + parts([("א.", L("h = 2, k = 1.5"), 1), ("ב.", L("h = −2, k = 3"), 1),
           ("ג.", L("h = −1, k = 2"), 1), ("ד.", L("k = 0, h = 4"), 1)]))

Q(23, "מהו הביטוי המייצג את היקף המצולע שבסרטוט? נתון: " + L("b = 11") + " ו־" + L("c = 16") + " — חשבו את ההיקף."
  + img("polygon", 30) + lines(1))

note("<b>שאלות מסכמות</b> — לפרק משתנים וביטויים אלגבריים")

Q("מסכמת 1", "אריאל הפיל כדור מראש צוק, והכדור הגיע לקרקע " + L("3") + " שניות לאחר מכן. הגובה (במטרים) מקורב בנוסחה "
  + L("h = 5t²") + ", כאשר " + L("t") + " הוא מספר השניות עד הנחיתה."
  + parts([("(1)", "מהו בערך הגובה של הצוק?" + mc([("א.", "15 מטר"), ("ב.", "30 מטר"), ("ג.", "45 מטר"), ("ד.", "225 מטר")]), 0),
           ("(2)", "אריאל הפיל כדור זהה מראש צוק אחר, והכדור הגיע לקרקע לאחר " + L("2") + " שניות. איזה צוק גבוה יותר? ומהו הפרש הגבהים?", 2)]))

Q("מסכמת 2", "מגזין רכב מדרג חמש מכוניות לפי ארבעה מאפיינים — בטיחות " + L("(S)") + ", יעילות דלק " + L("(F)")
  + ", מראה חיצוני " + L("(E)") + ", אבזור פנימי " + L("(T)") + " (דירוג: " + L("3") + "=מצוין, " + L("2") + "=טוב, " + L("1") + "=סביר):"
  + table(['T', 'E', 'F', 'S', 'מכונית'],
          [['3','2','1','3','Ca'],['2','2','2','2','M'],['2','3','1','3','Sp'],['3','3','1','1','N'],['2','3','2','3','KK']])
  + parts([("א.", "הציון הכולל מחושב לפי " + L("3·S + F + E + T") + ". חשבו את הציון הכולל של \"Ca\".", 1),
           ("ב.", "כתבו כלל (עם ארבעה מקדמים חיוביים) " + L("__·S + __·F + __·E + __·T") + " שלפיו \"Ca\" תנצח, ונמקו.", 2)]),
  src="אוריינות")
ENDSEC()

# =====================================================================
# SECTION B — שוויון בין ביטויים אלגבריים
# =====================================================================
SECTION("ב", "שוויון בין ביטויים אלגבריים", "אלגברה · כיתה ז' · זהות בין ביטויים", "#0d9488")

Q(1, "בסרטוט ארבע התמונות הראשונות בסדרה. דוד, שרית ואוסנת הציעו דרכים שונות להכליל את מספר הנקודות "
  "(" + L("n") + " = מספר סידורי של תמונה): דוד — " + L("4(n−1)+1") + "; שרית — " + L("2n−1+2(n−1)") + "; אוסנת — " + L("2(2n−1)−1") + "."
  + img("dotpattern", 70)
  + parts([("א.", "מי הציג ביטוי אלגברי שמתאר נכון את מספר הנקודות בכל תמונה?", 1),
           ("ב.", "האם אותה הצבה בשלושת הביטויים נותנת תמיד אותה תוצאה מספרית?", 1)]))

Q(2, "בסרטוט חלקת אדמה מלבנית ובתוכה בית מלבני; מסביב גדל דשא. אורך הבית הוא חצי מאורך החלקה, ורוחבו חצי מרוחב החלקה."
  + img("landhouse", 50)
  + parts([("א.", "נבו: \"אחסר את שטח הבית משטח החלקה\". מהו הביטוי שאליו הגיע? האם צדק?", 1),
           ("ב.", "אלה: \"שטח הבית הוא רבע מהחלקה, לכן אכפול את שטח החלקה ב־" + L("0.75") + "\". מהו הביטוי שלה? האם צדקה?", 1),
           ("ג.", "האם לכל ערך של " + L("a") + " שני הביטויים שווים?", 1)]))

Q(3, "במבצע ירד מחיר המנגו ב־" + L("2") + " ₪ לק\"ג. הדס ואלה קונות " + L("5") + " ק\"ג כל אחת. נסמן ב־" + L("m") + " את המחיר המקורי לק\"ג. "
  "הדס: התשלום הוא " + L("5(m−2)") + ". אלה: ההוזלה היא " + L("10") + " ₪, לכן " + L("5m−10") + ". מי צודקת? הסבירו." + lines(2))

Q(4, "האם הביטויים " + L("a·a") + " ו־" + L("a²") + " הם ביטויים שווים? הסבירו." + lines(1))
ENDSEC()

# =====================================================================
# SECTION C — כינוס איברים דומים
# =====================================================================
SECTION("ג", "כינוס איברים דומים", "אלגברה · כיתה ז' · פישוט ביטויים וחוק הפילוג", "#7c3aed")

Q(1, "לפניכם מלבן המורכב משני חלקים. דני ויוסי מצאו את שטחו בדרכים שונות — מי צודק? אולי שניהם?"
  + img("rect_two", 56)
  + parts([("א.", "יוסי: " + L("2x + 3x = (x+x) + (x+x+x) = 5x"), 1),
           ("ב.", "דני: " + L("2x + 3x = (2+3)x = 5x"), 1)]))

Q(2, "סרגל עולה " + L("k") + " שקלים ועט עולה " + L("m") + " שקלים. חברו בקו בין התיאור המילולי לייצוג האלגברי:"
  + img("ruler_pen", 72))

Q(3, "חברו בין הביטויים בטור א' לביטויים השווים להם בטור ב':"
  + table(['טור ב\'', 'טור א\''],
          [[L("8a + 5"), L("2a + 5")], [L("a/2"), L("3a − a")], [L("4a + 4"), L("4(a + 1)")],
           [L("15a"), L("6a + 2a + 5")], [L("5 + 2a"), L("5 · 3a")], [L("2a"), L("a/2 · ... ")]]))
ENDSEC()

# =====================================================================
# SECTION D — משוואות וזיהוי פתרונן
# =====================================================================
SECTION("ד", "משוואות וזיהוי פתרונן", "אלגברה · כיתה ז' · משוואה ומשמעות הפתרון", "#e11d48")

Q(1, "בדקו בעזרת הצבה מי מהערכים הוא פתרון של המשוואה ומי איננו:"
  + parts([("א.", L("x − 10 = 5") + " — האם " + L("x = 5") + "?", 1),
           ("ב.", L("4x − 2 = 2x + 2") + " — האם " + L("x = 1") + "?", 1),
           ("ג.", L("4x − 2 = 10 − x") + " — האם " + L("x = 2") + "?", 1),
           ("ד.", L("2x + 6 = 5x") + " — האם " + L("x = 2") + "? האם " + L("x = 3") + "?", 1),
           ("ה.", L("3x − 6 = 7x") + " — האם " + L("x = 3") + "?", 1),
           ("ו.", L("7x − 6 = 3x") + " — האם " + L("x = 2") + "? האם " + L("x = 1") + "?", 1)]))

Q(2, "מה צריך לכתוב במשבצת כדי שפתרון המשוואה יהיה " + L("1") + "?"
  + img("box_eq", 26) + lines(1))

Q(3, "סמנו את המשוואה שפתרונה הוא " + L("x = 10") + ":"
  + mc([("•", L("40x = 5x + 100")), ("•", L("2x − 2 = x + 8")), ("•", L("3x + 12 = 100")), ("•", L("4x − 4 = 30x + 1"))]))

Q(4, "סמנו את שתי המשוואות שפתרונן הוא " + L("x = 0.5") + ":"
  + mc([("•", L("2x + 5 = 6x + 3")), ("•", L("x = 1 + x")), ("•", L("10x + 6 = 8x + 7")), ("•", L("3 + 3x = 6"))]))

Q(5, "הקיפו את השאלה שאפשר לייצג בעזרת המשוואה " + L("3x = 270") + ":"
  + parts([("א.", "החשבון היה " + L("270") + " ₪ וכולל " + L("30") + " ₪ תשר. מה מחיר הארוחה (" + L("x") + ") ללא התשר?", 0),
           ("ב.", "מנה עיקרית וקינוח עלו " + L("270") + " ₪. המנה העיקרית פי " + L("3") + " מהקינוח. מה מחיר הקינוח (" + L("x") + ")?", 0),
           ("ג.", "שלושה חברים, כל אחד שילם " + L("270") + " ₪. מה המחיר הכולל (" + L("x") + ")?", 0),
           ("ד.", "שלושה חברים שילמו יחד " + L("270") + " ₪ בחלוקה שווה. כמה שילם כל אחד (" + L("x") + ")?", 0)]))

Q(6, "מחיר כדור התייקר. סמנו ב־" + L("x") + " את המחיר המקורי, בנו משוואה והסבירו את דרך הפתרון."
  + img("ball", 80)
  + table(['ביטוי', 'תיאור'],
          [[L("x"), 'מחיר כל כדור (ש\"ח)'], [L("18x"), 'תשלום כולל (ש\"ח)'], [L("x+6"), 'מחיר חדש לכל כדור'],
           [L("15(x+6)"), 'תשלום כולל חדש'], [L("15(x+6) = 18x"), 'תשלום כולל = תשלום חדש']]))

Q(7, "סמנו ב־" + L("x") + " ₪ את מחיר חטיף תמרים. בנו משוואה לפי הנתון, ובחרו את הפתרון הנכון ונמקו."
  + img("snack", 78)
  + mc([("(1)", "5 ש\"ח"), ("(2)", "−4 ש\"ח"), ("(3)", "3.5 ש\"ח"), ("(4)", "0.2 ש\"ח")]))

Q(8, "סמנו ב־" + L("t") + " את זמן העלייה מעפולה לפסגת הר תבור (בשעות). בנו משוואה לפי הנתונים, ובחרו את הפתרון ונמקו."
  + img("tabor", 80)
  + mc([("(1)", L("t = 0.5")), ("(2)", L("t = −2")), ("(3)", L("t = 3")), ("(4)", L("t = 1.5"))]))

Q(9, "לדני היו פי שניים בולים מאשר לרינה. לאחר שנתן לרינה " + L("7") + " בולים, היה להם מספר שווה. כמה בולים יש להם יחד? "
  "התאימו לכל בחירת משתנה את המשוואה המתאימה:"
  + parts([("•", L("x") + " = הבולים שהיו לדני בתחילה", 0),
           ("•", L("x") + " = הבולים שהיו לרינה בתחילה  →  " + L("2x − 7 = x + 7"), 0),
           ("•", L("x") + " = הבולים של שניהם יחד  →  " + L("x/2 − 7 = x/2 + 7"), 0)], ))

Q(10, "בסרטוט משולש שווה־צלעות ומחומש משוכלל. צלע המשולש " + L("10") + " ס\"מ וצלע המחומש " + L("d") + " ס\"מ. "
  "היקף המחומש גדול ב־" + L("5") + " ס\"מ מהיקף המשולש. בנו משוואה עם הנעלם " + L("d") + "."
  + img("tri_pent", 44) + lines(1))

Q(11, "על פי הסרטוט, כתבו משוואה למציאת " + L("x") + "."
  + img("eq_fig", 34) + lines(1))

Q(12, "לפניכם משולש. " + parts([("א.", "סמנו ב־" + L("x") + " את אורך הבסיס ובנו משוואה למציאת " + L("x") + ".", 1),
                                ("ב.", "סמנו ב־" + L("x") + " את אורך השוק ובנו משוואה למציאת " + L("x") + ".", 1)])
  + img("tri_base", 66))
ENDSEC()

# =====================================================================
# SECTION E — פתירת משוואות ממעלה ראשונה
# =====================================================================
SECTION("ה", "פתירת משוואות ממעלה ראשונה", "אלגברה · כיתה ז' · מעבר בין משוואות שקולות", "#d97706")

Q(1, "פתרו בעל פה, בעזרת שיקול דעת חישובי:"
  + parts([("א.", L("3a = 11 + 4"), 1), ("ב.", L("b − 1 = 7 + 3"), 1), ("ג.", L("2(c − 5) = 18"), 1)]))

Q(2, "כתבו משוואה שהפתרון שלה הוא " + L("1") + "." + lines(1))

Q(3, "נתונה משוואה ודרך הפתרון. הסבירו בכל שורה מה בוצע ומדוע זה מוצדק:<br>"
  + L("10x = 3(x + 7)") + " → " + L("10x = 3x + 21") + " → " + L("7x = 21") + " → " + L("x = 3") + lines(2))

Q(4, "פתרו את המשוואה " + L("15(x + 6) = 18x") + " והסבירו בעל פה כל שלב בפתרון." + lines(3))

Q(5, "פתרו, בעזרת מעבר למשוואות שקולות:"
  + parts([("א.", L("8x − 6 = 3x + 4"), 1), ("ב.", L("3(y − 2) + 1 = y + 5"), 1),
           ("ג.", L("2(z − 3) + 5 = 5(7 − 2z) − 2"), 1), ("ד.", L("6x + 20 = 4(2x + 3)"), 1),
           ("ה.", L("(x − 1)/3 = 7"), 1), ("ו.", L("(x − 1)/3 = x/5"), 1)]))

Q(6, "שאלה לדיון כיתתי (מזמנת שיח מתמטי):"
  + img("balance", 74))

Q(7, "נתונות שתי משקולות. האחת כבדה פי " + L("2") + " מהאחרת, ומשקלן הכולל " + L("13.5") + " ק\"ג. מה משקל המשקולת הקלה?" + lines(2))

Q(8, "במשולש ישר־זווית, זווית חדה אחת קטנה ב־" + L("20°") + " מהזווית החדה האחרת. מצאו את גודל הזוויות." + lines(2))

Q(9, "דן גדול מיואב ב־" + L("6") + " שנים. לפני " + L("4") + " שנים היה גילו של דן פי " + L("2") + " מגילו של יואב. בני כמה דן ויואב כיום?" + lines(2))

Q(10, "בתחנת דלק א' מחיר הדלק " + L("6.45") + " ₪ לליטר ועמלת הלילה " + L("4") + " ₪; בתחנה ב' המחיר " + L("6.55") + " ₪ לליטר ועמלת הלילה " + L("2") + " ₪. "
  "לאיזו כמות דלק עלות התדלוק בלילה בשתי התחנות שווה?" + lines(2))

Q(11, "בנו משוואה ופתרו לפי הסרטוט:"
  + img("fig_e12", 66) + lines(2))

Q(12, "בנו משוואה ופתרו לפי הסרטוט:"
  + img("fig_e13", 66) + lines(2))
ENDSEC()

# =====================================================================
# SECTION F — קריאת תיאור גרפי של נקודות ברביע I
# =====================================================================
SECTION("ו", "קריאת גרף — נקודות ברביע I", "אלגברה · כיתה ז' · קריאה וייצוג גרפי", "#0284c7")

Q(1, "עלות החנייה בחניון היא " + L("10") + " ₪ לשעה הראשונה, ועוד " + L("3.50") + " ₪ לכל רבע שעה נוספת."
  + fig(C.points_plot([(1,10),(1.25,13.5),(1.5,17),(1.75,20.5),(2,24),(3,38)],
                      0,4,0.5, 0,55,5, 'שעות חנייה', 'עלות (₪)', color='#0284c7'),
        "עלות החנייה (הנקודות בין שעתיים ל־3 הושמטו)")
  + parts([("א.", "מהי עלות החנייה לשעתיים מלאות? ול־" + L("3") + " שעות מלאות?", 1),
           ("ב.", "השלימו את הנקודה המתאימה לתשלום עבור " + L("3.5") + " שעות חנייה.", 0),
           ("ג.", "מהו התשלום עבור חנייה של " + L("4") + " שעות?", 1)]))

Q(2, "הגרף מציג את ההישג הממוצע של תלמידי ישראל במבחן בינלאומי (טווח אפשרי " + L("200") + "–" + L("800") + "):"
  + fig(C.points_plot([(2007,463,'463'),(2011,516,'516'),(2015,511,'511'),(2019,519,'519'),(2023,487,'487')],
                      2006,2024,2, 400,600,50, 'שנה', 'הישג ממוצע', color='#0284c7', point_labels=True),
        "ההישג הממוצע של ישראל לפי שנים")
  + parts([("א.", "מה היה ההישג הממוצע בשנת " + L("2011") + "?", 1),
           ("ב.", "באיזו שנה היה ההישג " + L("511") + "?", 1),
           ("ג.", "באיזו שנה היה ההישג הגבוה ביותר?", 1)]))

Q(3, "הגרף מציג את שטח הריבוע בהתאם לאורך הצלע (בס\"מ):"
  + fig(C.points_plot([(1,1),(1.5,2.25),(2,4),(2.5,6.25),(3,9)],
                      0,4,0.5, 0,10,1, 'אורך הצלע (ס\"מ)', 'שטח (סמ\"ר)', color='#0284c7'),
        "שטח הריבוע כתלות באורך הצלע")
  + parts([("א.", "כאשר אורך הצלע " + L("1.5") + " ס\"מ, מהו שטח הריבוע?", 1),
           ("ב.", "מה יכול להיות אורך הצלע אם השטח בין " + L("3") + " ל־" + L("7") + " סמ\"ר? (לפי הנקודות בגרף)", 1),
           ("ג.", "נסמן ב־" + L("x") + " את אורך הצלע וב־" + L("y") + " את השטח. רשמו " + L("y = ……") + ".", 1)]))

Q(4, "בספריית תלפיות יש " + L("1300") + " ספרים ורוכשים " + L("100") + " בשנה; בספריית ארנונה יש " + L("800") + " ורוכשים " + L("150") + " בשנה."
  + fig(C.points_plot([(0,1300),(2,1500),(4,1700),(6,1900),(8,2100),(10,2300)],
                      0,12,2, 800,2400,200, 'שנים', 'מספר ספרים', color='#0284c7',
                      series2=[(0,800),(2,1100),(4,1400),(6,1700),(8,2000),(10,2300)], color2='#e11d48'),
        "תלפיות (כחול) · ארנונה (אדום)")
  + parts([("א.", "התאימו כל סדרת נקודות לספרייה המתאימה.", 1),
           ("ב.", "כמה ספרים היו בארנונה כעבור " + L("3") + " שנים?", 1),
           ("ג.", "כעבור כמה שנים יהיו " + L("1400") + " ספרים בארנונה? ובתלפיות?", 1),
           ("ד.", "סמנו ב־" + L("t") + " את מספר השנים ורשמו ביטוי אלגברי למספר הספרים בכל ספרייה.", 1),
           ("ה.", "כעבור כמה שנים יהיה בשתי הספריות אותו מספר ספרים?", 1),
           ("ו.", "באיזו ספרייה יהיו יותר ספרים כעבור " + L("15") + " שנה?", 1)]))

Q(5, "במשתלה אפשר לקנות פרחים בחנות (" + L("7.5") + " ₪ לפרח) או באתר (" + L("5") + " ₪ לפרח + " + L("50") + " ₪ משלוח)."
  + table([L("30"), L("25"), L("20"), L("15"), L("10"), L("5"), 'מספר פרחים בזר'],
          [['<span class="blank"></span>']*6 + ['קנייה בחנות'],
           ['<span class="blank"></span>']*6 + ['קנייה באתר']])
  + parts([("א.", "מלאו את הטבלה (תשלום בכל דרך).", 0),
           ("ב.", "החל מאיזה מספר פרחים זול יותר לקנות באתר? נמקו.", 2)]))

note("<b>שאלה מסכמת</b> — קיפול נייר: מדדו שטח של דף מלבני, קפלו לשניים שווים בכל פעם, רשמו בטבלה את מספר הקיפולים והשטח המתקבל, וסרטטו את הנקודות במערכת צירים.")
ENDSEC()

# =====================================================================
# Assemble HTML  (same CSS/style as the uncertainty booklet)
# =====================================================================
CSS = """
@page { size: A4; margin: 16mm 12mm 18mm 12mm; }
* { box-sizing: border-box; }
html,body { margin:0; padding:0; }
body { direction: rtl; font-family:'Segoe UI','Arial',sans-serif; color:#1f2a44; font-size:11pt; line-height:1.55; }
p { margin:6px 0; }
.cover { height: 262mm; display:flex; flex-direction:column; justify-content:center; align-items:stretch; page-break-after: always; }
.cover .band { background: linear-gradient(135deg,#4f46e5,#7c3aed 55%,#0d9488); color:#fff; border-radius:22px; padding:46px 40px; text-align:center; box-shadow:0 10px 30px rgba(79,70,229,.18); }
.cover h1 { font-size:40pt; margin:0 0 6px; letter-spacing:.5px; }
.cover .sub { font-size:15pt; opacity:.95; }
.cover .meta { margin-top:14px; font-size:11pt; opacity:.9; }
.toc { margin:40px 6px 0; }
.toc h2 { color:#1f2a44; font-size:12pt; font-weight:600; letter-spacing:5px; padding-bottom:12px; border-bottom:1.5px solid #1f2a44; margin:0; }
.toc ol { list-style:none; padding:0; margin:0; }
.toc li { display:flex; align-items:center; gap:18px; padding:13px 2px; border-bottom:0.75px solid #ececf1; }
.toc li:last-child { border-bottom:none; }
.toc .idx { color:var(--cc,#4f46e5); font-size:11pt; font-weight:600; letter-spacing:1px; min-width:24px; text-align:center; }
.toc .nm { flex:1; font-size:12pt; color:#2a3142; letter-spacing:.2px; }
.toc .tick { width:24px; height:1.5px; background:var(--cc,#4f46e5); opacity:.5; }
.cover .foot { margin-top:auto; text-align:center; color:#b6bbc7; font-size:8pt; letter-spacing:3px; padding-top:18px;}
.sectionbar { display:flex; align-items:center; gap:16px; background:var(--c); color:#fff; border-radius:14px; padding:14px 20px; margin:4px 0 14px; page-break-before: always; page-break-after: avoid; box-shadow:0 4px 14px rgba(0,0,0,.10); }
.secletter { width:46px; height:46px; border-radius:12px; background:rgba(255,255,255,.22); display:flex; align-items:center; justify-content:center; font-size:22pt; font-weight:800; }
.sectitle { font-size:17pt; font-weight:800; }
.secsub { font-size:10.5pt; opacity:.92; }
.q { border:1px solid #e6e8ee; border-radius:12px; padding:12px 16px 14px; margin:11px 0; background:#fff; page-break-inside: avoid; }
.qhead { display:flex; align-items:center; gap:10px; margin-bottom:4px; }
.qnum { background:var(--c,#4f46e5); color:#fff; min-width:30px; height:30px; padding:0 9px; border-radius:16px; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:12.5pt; flex:0 0 auto; }
.qtags { display:flex; gap:6px; }
.pill { background:#eef0fb; color:#4f46e5; border:1px solid #dfe3fb; border-radius:999px; padding:2px 10px; font-size:8.5pt; font-weight:700; }
.qbody { font-size:11pt; }
ol.parts { list-style:none; margin:8px 0 0; padding:0; }
ol.parts > li { display:flex; gap:8px; margin:7px 0; align-items:flex-start; }
.plab { font-weight:800; color:var(--c,#4f46e5); flex:0 0 auto; min-width:30px; }
.ptext { flex:1; }
.mc { margin:8px 0 2px; display:grid; grid-template-columns:1fr 1fr; gap:6px 18px; }
.opt { display:flex; gap:8px; align-items:baseline; }
.ol { width:22px; height:22px; border:1.6px solid #c7ccda; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:9pt; font-weight:700; color:#4b5468; flex:0 0 auto;}
.ot { flex:1; }
.lines { margin:8px 0 2px; }
.ln { border-bottom:1px dotted #c2c8d6; height:21px; }
.figure { margin:10px auto; text-align:center; page-break-inside:avoid; }
svg.chart { display:block; margin:4px auto; max-width:100%; height:auto; }
.cap { color:#5b6573; font-size:9.5pt; margin-top:2px; font-weight:600; }
img.embed { max-width:66%; height:auto; border:1px solid #e6e8ee; border-radius:8px; padding:6px; background:#fff; }
table.tbl { border-collapse:collapse; margin:9px auto; font-size:10.5pt; }
table.tbl th, table.tbl td { border:1px solid #c7ccda; padding:6px 12px; text-align:center; vertical-align:middle; }
table.tbl thead th { background:#f4f5fb; color:#3a4256; font-weight:700; }
.blank { display:inline-block; min-width:46px; border-bottom:1.6px solid #9aa3b8; height:14px; }
.note { background:#f7f8fc; border:1px solid #e6e8ee; border-right:5px solid var(--c,#4f46e5); border-radius:8px; padding:8px 14px; margin:12px 0; font-size:10pt; color:#3a4256; page-break-inside:avoid; }
@media screen { html { background:#e9ebf0; } body { max-width: 880px; margin: 22px auto 60px; padding: 32px 44px; background:#fff; box-shadow:0 4px 24px rgba(20,25,50,.14); border-radius:6px; } .cover { height:auto; min-height:auto; } }
"""

TOPICS = [("א","משתנים וביטויים אלגבריים","#4f46e5"),("ב","שוויון בין ביטויים אלגבריים","#0d9488"),
          ("ג","כינוס איברים דומים","#7c3aed"),("ד","משוואות וזיהוי פתרונן","#e11d48"),
          ("ה","פתירת משוואות ממעלה ראשונה","#d97706"),("ו","קריאת גרף — נקודות ברביע I","#0284c7")]
toc = "".join(f'<li style="--cc:{c}"><span class="idx">{l}</span><span class="nm">{t}</span><span class="tick"></span></li>' for l,t,c in TOPICS)

cover = f"""<div class="cover">
  <div class="band">
    <h1>אַלְגֶּבְּרָה לְכִיתָּה ז'</h1>
    <div class="sub">ביטויים, משוואות וגרפים · חטיבת הביניים</div>
  </div>
  <div class="toc">
    <h2>תוכן העניינים</h2>
    <ol>{toc}</ol>
  </div>
  <div class="foot">מתמטיקה · חטיבת הביניים</div>
</div>"""

html = (f'<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8">'
        f'<title>אלגברה לכיתה ז - אוסף שאלות</title><style>{CSS}</style></head><body>'
        + cover + "".join(CARDS) + "</body></html>")

import time, urllib.parse
with open(os.path.join(OUT, "worksheet.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("HTML cards:", len([c for c in CARDS if c.startswith('<div class=\"q\"')]))

from playwright.sync_api import sync_playwright
url = "file:///" + os.path.join(OUT, "worksheet.html").replace("\\", "/")
PDF_NAME = "אלגברה-ז-שאלות.pdf"
pdf_path = os.path.join(OUT, PDF_NAME)
foot = ('<div style="font-family:Segoe UI,Arial; font-size:8px; color:#9aa3b8; width:100%; text-align:center;">'
        'אלגברה לכיתה ז · אוסף שאלות &nbsp;·&nbsp; עמוד <span class="pageNumber"></span> מתוך <span class="totalPages"></span></div>')
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); pg.goto(url)
    pg.pdf(path=pdf_path, format="A4", print_background=True, display_header_footer=True,
           header_template="<div></div>", footer_template=foot,
           margin={"top":"16mm","bottom":"18mm","left":"12mm","right":"12mm"})
    b.close()
print("PDF written OK")

# page images + viewer + simple app
import fitz, glob
pages_dir = os.path.join(OUT, "assets", "pages"); os.makedirs(pages_dir, exist_ok=True)
for old in glob.glob(os.path.join(pages_dir, "*.png")): os.remove(old)
_doc = fitz.open(pdf_path); npages = _doc.page_count
for i in range(npages): _doc[i].get_pixmap(dpi=120).save(os.path.join(pages_dir, f"p{i+1:03d}.png"))
_doc.close()
ts = int(time.time()); pdf_href = urllib.parse.quote(PDF_NAME)
sheets = "".join(f'<div class="sheet"><img src="assets/pages/p{i+1:03d}.png?v={ts}" loading="lazy" alt="עמוד {i+1}"><div class="pgn">עמוד {i+1} / {npages}</div></div>' for i in range(npages))
viewer = f"""<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>אלגברה לכיתה ז — תצוגת הדפים</title><style>
 html,body{{margin:0;background:#e9ebf0;font-family:'Segoe UI',Arial,sans-serif}}
 .bar{{position:sticky;top:0;z-index:5;background:#191c2e;color:#eef;padding:11px 16px;font-size:13.5px;display:flex;gap:16px;align-items:center;justify-content:center}}
 .bar b{{color:#fff}} .bar a{{color:#8ad7ff;text-decoration:none;font-weight:600}}
 .wrap{{padding:22px 10px 70px;display:flex;flex-direction:column;align-items:center;gap:22px}}
 .sheet{{width:min(820px,96vw);background:#fff;box-shadow:0 5px 20px rgba(20,25,50,.22);border-radius:3px;overflow:hidden}}
 .sheet img{{display:block;width:100%;height:auto}}
 .pgn{{text-align:center;color:#7a8194;font-size:11px;padding:6px;background:#fafbfd;border-top:1px solid #eef}}
</style></head><body>
<div class="bar"><a href="index.html">⌂ דף הבית</a> <span>📄 <b>תצוגת הדפים A4</b> · {npages} עמודים</span> <a href="{pdf_href}?v={ts}" download>⬇ הורדה</a></div>
<div class="wrap">{sheets}</div></body></html>"""
open(os.path.join(OUT, "viewer.html"), "w", encoding="utf-8").write(viewer)

nq = len([c for c in CARDS if c.startswith('<div class="q"')]); nchap = len(TOPICS)
chips = "".join(f'<span class="chip" style="--cc:{c}"><i>{l}</i>{t}</span>' for l,t,c in TOPICS)
APP = """<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>אלגברה לכיתה ז — אוסף שאלות</title><style>
 *{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
 body{font-family:'Segoe UI','Arial',sans-serif;color:#1f2a44;min-height:100vh;background:radial-gradient(1100px 560px at 85% -12%,#e7ecff 0,transparent 60%),radial-gradient(820px 460px at -5% 2%,#dff5ee 0,transparent 55%),#f4f6fb}
 .wrap{max-width:680px;margin:0 auto;padding:26px 16px 60px}
 .hero{background:linear-gradient(135deg,#4f46e5 0,#7c3aed 52%,#0d9488 100%);border-radius:24px;padding:38px 24px;color:#fff;text-align:center;box-shadow:0 14px 38px rgba(79,70,229,.26)}
 .hero .kick{font-size:11.5px;letter-spacing:4px;opacity:.9;margin-bottom:10px}
 .hero h1{font-size:clamp(26px,7vw,34px);margin-bottom:8px}
 .hero p{opacity:.94;font-size:clamp(13px,3.6vw,15px)}
 .stats{display:flex;gap:10px;justify-content:center;margin:-24px auto 0;max-width:420px;position:relative}
 .stat{flex:1;background:#fff;border-radius:15px;padding:14px 6px;text-align:center;box-shadow:0 8px 20px rgba(20,25,50,.09)}
 .stat b{display:block;font-size:clamp(20px,6vw,25px);font-weight:800;background:linear-gradient(135deg,#4f46e5,#0d9488);-webkit-background-clip:text;background-clip:text;color:transparent}
 .stat span{font-size:11.5px;color:#5b6573}
 .actions{display:flex;flex-direction:column;gap:11px;margin:26px 0 6px}
 .act{display:flex;align-items:center;gap:13px;padding:14px 15px;background:#fff;border:1px solid #e7e9f2;border-radius:16px;text-decoration:none;color:#1f2a44;box-shadow:0 2px 8px rgba(20,25,50,.04);transition:transform .15s,box-shadow .2s,border-color .2s}
 .act:hover{transform:translateY(-2px);border-color:#d3d8ea;box-shadow:0 10px 22px rgba(20,25,50,.09)}
 .act .ic{width:46px;height:46px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:21px;color:#fff;flex-shrink:0}
 .act .tx{flex:1;min-width:0} .act .tx b{display:block;font-size:16px} .act .tx span{font-size:12.5px;color:#7a8194}
 .act .ar{color:#c4cad8;font-size:24px;font-weight:300}
 .ic-view{background:linear-gradient(135deg,#6366f1,#7c3aed)} .ic-dl{background:linear-gradient(135deg,#0d9488,#10b981)} .ic-print{background:linear-gradient(135deg,#f59e0b,#d97706)}
 .lbl{text-align:center;color:#6b7280;font-size:12.5px;font-weight:700;margin:24px 0 11px;letter-spacing:1px}
 .chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
 .chip{display:flex;align-items:center;gap:8px;background:#fff;border-radius:12px;padding:7px 12px;font-size:12.5px;color:#3a4256;box-shadow:0 3px 12px rgba(20,25,50,.06);border-right:4px solid var(--cc)}
 .chip i{display:flex;align-items:center;justify-content:center;width:21px;height:21px;border-radius:50%;background:var(--cc);color:#fff;font-style:normal;font-weight:800;font-size:11.5px}
 .foot{text-align:center;color:#9aa3b8;font-size:11px;margin-top:28px}
</style></head><body><div class="wrap">
 <div class="hero"><div class="kick">אוסף שאלות להדפסה</div><h1>אלגברה לכיתה ז'</h1><p>ביטויים אלגבריים · משוואות · גרפים</p></div>
 <div class="stats"><div class="stat"><b>__NQ__</b><span>שאלות</span></div><div class="stat"><b>__NCHAP__</b><span>פרקים</span></div><div class="stat"><b>__NPAGES__</b><span>עמודי A4</span></div></div>
 <div class="actions">
   <a class="act" href="viewer.html"><span class="ic ic-view">📖</span><span class="tx"><b>צפייה בדפים</b><span>תצוגת A4 איכותית · גלילה נוחה</span></span><span class="ar">‹</span></a>
   <a class="act" href="__PDF__" download><span class="ic ic-dl">⬇</span><span class="tx"><b>הורדת ה־PDF</b><span>כל הדפים למכשיר · מוכן להדפסה</span></span><span class="ar">‹</span></a>
   <a class="act" href="__PDF__" target="_blank" rel="noopener"><span class="ic ic-print">🖨️</span><span class="tx"><b>הדפסה מהירה</b><span>פתיחת ה־PDF להדפסה ישירה</span></span><span class="ar">‹</span></a>
   <a class="act" href="../index.html"><span class="ic" style="background:linear-gradient(135deg,#64748b,#334155)">⌂</span><span class="tx"><b>חזרה לדף הראשי</b><span>כל הספר — אי-ודאות ואלגברה</span></span><span class="ar">‹</span></a>
 </div>
 <div class="lbl">הפרקים בחוברת</div><div class="chips">__CHIPS__</div>
 <div class="foot">הופק מתוך מסמך "אלגברה לכיתה ז" · גרפיקה וקטורית · __NPAGES__ עמודי A4</div>
</div></body></html>"""
APP = APP.replace("__NQ__",str(nq)).replace("__NCHAP__",str(nchap)).replace("__NPAGES__",str(npages)).replace("__PDF__",pdf_href).replace("__CHIPS__",chips)
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(APP)

import json
json.dump({"key": "algebra", "title": "אלגברה לכיתה ז'", "subtitle": "ביטויים, משוואות וגרפים",
           "questions": nq, "chapters": nchap, "pages": npages, "pdf": PDF_NAME,
           "color": "#0284c7", "icon": "∑"},
          open(os.path.join(OUT, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"App+viewer+meta written. q={nq} chap={nchap} pages={npages}")
