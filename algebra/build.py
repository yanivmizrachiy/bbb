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

def fig(svg, cap="", w=None):
    c = f'<div class="cap">{cap}</div>' if cap else ""
    style = f' style="max-width:{w}%;margin-inline:auto"' if w else ""
    return f'<div class="figure"{style}>{svg}{c}</div>'

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

_HSEQ = "אבגדהוזחטיכלמנסעפצקרשת"
def SECTION(letter, title, subtitle, color):
    _qcount[0] = 0
    CARDS.append(f'<section id="sec-{_HSEQ.index(letter)+1}" class="topic" style="--c:{color}"><div class="sectionbar"><div class="secletter">{letter}</div><div><div class="sectitle">{title}</div><div class="secsub">{subtitle}</div></div></div>')

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
  + fig(C.seq_a3(), w=58)
  + parts([("א.", "כמה סימנים יש בכל אחד מהאיברים המוצגים?", 1),
           ("ב.", "הציעו המשך לסדרה: כתבו שלושה איברים עוקבים.", 1),
           ("ג.", "בהנחה שהאיברים הם " + L("3, 5, 7, 9, 11, 13") + ", מהו האיבר ה־" + L("9") + " בסדרה?", 1),
           ("ד.", "מהו האיבר ה־" + L("58") + "? מהו האיבר ה־" + L("1000") + "?", 1),
           ("ה.", "כמה סימנים יש במקום ה־" + L("n") + "? (כתבו ביטוי אלגברי)", 1)]))

Q(4, "קופסה מכילה כדורים לבנים, סגולים ושחורים בלבד. מספר הכדורים הלבנים גדול פי " + L("4") + " ממספר הסגולים, "
  "ו־" + L("3") + " כדורים פחות ממספר השחורים. מספר הכדורים הסגולים מסומן ב־" + L("x") + "."
  + parts([("א.", "רשמו ביטוי אלגברי למספר הכדורים השחורים, וביטוי למספר הכדורים בקופסה כולה.", 2)]))

Q(5, "הגובה של מגדל הבנוי מ־" + L("4") + " כוסות הוא " + L("20") + " ס\"מ, והגובה של מגדל מ־" + L("6") + " כוסות הוא " + L("26") + " ס\"מ."
  + fig(C.cups_two(), w=52)
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

Q(14, "התאימו לכל <b>תיאור מילולי</b> את הביטוי האלגברי המתאים (רשמו את האות המתאימה ליד כל מספר):"
  + parts([("1.", "הוסיפו " + L("2") + " ל־" + L("a"), 0),
           ("2.", "חסרו " + L("2") + " מ־" + L("a"), 0),
           ("3.", "כפלו את " + L("a") + " ב־" + L("2"), 0),
           ("4.", "חלקו את " + L("a") + " ב־" + L("2"), 0),
           ("5.", "כפלו את " + L("a") + " בעצמו", 0)])
  + "<p>הביטויים: א. " + L("a + 2") + " · ב. " + L("a − 2") + " · ג. " + L("2a") + " · ד. " + L("a/2") + " · ה. " + L("a²") + " · ו. " + L("2 − a") + " · ז. " + L("2/a") + "</p>" + lines(1))

Q(15, "לפניכם סדרת המספרים " + L("2, 5, 11, 23, …") + " (האיבר הראשון הוא " + L("2") + "). איזו מההוראות הבאות יוצרת כל איבר מהאיבר הקודם לו?"
  + mc([("א.", "הוסיפו " + L("1") + " לאיבר הקודם, ואז כפלו ב־" + L("2")),
        ("ב.", "כפלו את האיבר הקודם ב־" + L("2") + ", ואז הוסיפו " + L("1")),
        ("ג.", "כפלו את האיבר הקודם ב־" + L("3") + ", ואז החסירו " + L("1")),
        ("ד.", "החסירו " + L("1") + " מהאיבר הקודם, ואז כפלו ב־" + L("3"))]))

Q(16, "לפניכם שלושה זוגות סדורים: " + L("(3, 6)") + " · " + L("(6, 15)") + " · " + L("(8, 21)") + ". איזה משפט מתאר כיצד מקבלים את המספר השני מהמספר הראשון בכל זוג? (לדוגמה, בזוג " + L("(3, 6)") + " המספר הראשון הוא " + L("3") + " והשני הוא " + L("6") + ".)"
  + mc([("א.", "להוסיף " + L("3")),
        ("ב.", "להחסיר " + L("3")),
        ("ג.", "לכפול ב־" + L("2")),
        ("ד.", "לכפול ב־" + L("2") + " ואז להוסיף " + L("3")),
        ("ה.", "לכפול ב־" + L("3") + " ואז להחסיר " + L("3"))]))

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
  + fig(C.polygon_perim(), w=42) + lines(1))

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
  + fig(C.dotpattern(), w=66)
  + parts([("א.", "מי הציג ביטוי אלגברי שמתאר נכון את מספר הנקודות בכל תמונה?", 1),
           ("ב.", "האם אותה הצבה בשלושת הביטויים נותנת תמיד אותה תוצאה מספרית?", 1)]))

Q(2, "בסרטוט חלקת אדמה מלבנית ובתוכה בית מלבני; מסביב גדל דשא. אורך הבית הוא חצי מאורך החלקה, ורוחבו חצי מרוחב החלקה."
  + fig(C.landhouse(), w=54)
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
  + fig(C.rect_two(), w=50)
  + parts([("א.", "יוסי: " + L("2x + 3x = (x+x) + (x+x+x) = 5x"), 1),
           ("ב.", "דני: " + L("2x + 3x = (2+3)x = 5x"), 1)]))

Q(2, "סרגל עולה " + L("k") + " שקלים ועט עולה " + L("m") + " שקלים. התאימו לכל תיאור מילולי את הביטוי האלגברי המתאים (רשמו את האות ליד המספר):"
  + parts([("1.", "המחיר של " + L("5") + " עטים", 0),
           ("2.", "המחיר של " + L("5") + " סרגלים ו־" + L("5") + " עטים", 0),
           ("3.", "ההפרש בין מחיר " + L("5") + " עטים לבין מחיר " + L("5") + " סרגלים", 0),
           ("4.", "העודף מ־" + L("50") + " שקלים ששולמו עבור " + L("5") + " עטים", 0)])
  + "<p>הביטויים: א. " + L("5m") + " · ב. " + L("5(k + m)") + " · ג. " + L("5m − 5k") + " · ד. " + L("50 − 5m") + " · ה. " + L("5k") + " · ו. " + L("5k − 5m") + "</p>" + lines(1))

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

Q(2, "מה צריך לכתוב במשבצת במשוואה " + L("x³ + x = □") + " כדי שפתרון המשוואה יהיה " + L("1") + "?" + lines(1))

Q(3, "סמנו את המשוואה שפתרונה הוא " + L("x = 10") + ":"
  + mc([("•", L("40x = 5x + 100")), ("•", L("2x − 2 = x + 8")), ("•", L("3x + 12 = 100")), ("•", L("4x − 4 = 30x + 1"))]))

Q(4, "סמנו את שתי המשוואות שפתרונן הוא " + L("x = 0.5") + ":"
  + mc([("•", L("2x + 5 = 6x + 3")), ("•", L("x = 1 + x")), ("•", L("10x + 6 = 8x + 7")), ("•", L("3 + 3x = 6"))]))

Q(5, "הקיפו את השאלה שאפשר לייצג בעזרת המשוואה " + L("3x = 270") + ":"
  + parts([("א.", "החשבון היה " + L("270") + " ₪ וכולל " + L("30") + " ₪ תשר. מה מחיר הארוחה (" + L("x") + ") ללא התשר?", 0),
           ("ב.", "מנה עיקרית וקינוח עלו " + L("270") + " ₪. המנה העיקרית פי " + L("3") + " מהקינוח. מה מחיר הקינוח (" + L("x") + ")?", 0),
           ("ג.", "שלושה חברים, כל אחד שילם " + L("270") + " ₪. מה המחיר הכולל (" + L("x") + ")?", 0),
           ("ד.", "שלושה חברים שילמו יחד " + L("270") + " ₪ בחלוקה שווה. כמה שילם כל אחד (" + L("x") + ")?", 0)]))

Q(6, "בית ספר קנה " + L("18") + " כדורים שמחירם זהה. אילו התייקר כל כדור ב־" + L("6") + " ש\"ח, היה אפשר לקנות באותו סכום רק " + L("15") + " כדורים. סמנו ב־" + L("x") + " את מחיר הכדור המקורי (לפני ההתייקרות), בנו משוואה, פתרו אותה, והסבירו את דרך הפתרון." + lines(3))

Q(7, "אילנה קנתה " + L("5") + " חטיפי תמרים, " + L("4") + " חפיסות מסטיק ו־" + L("7") + " חטיפי אגוזים. מחיר חפיסת מסטיק זול ב־" + L("0.5") + " ש\"ח ממחיר חטיף תמרים, ומחיר חטיף אגוזים יקר ב־" + L("3") + " ש\"ח ממחיר חטיף תמרים. אילנה שילמה בסך הכול " + L("75") + " ש\"ח. סמנו ב־" + L("x") + " ₪ את מחיר חטיף התמרים, בנו משוואה, ובחרו את הפתרון הנכון ונמקו."
  + mc([("(1)", "5 ש\"ח"), ("(2)", "−4 ש\"ח"), ("(3)", "3.5 ש\"ח"), ("(4)", "0.2 ש\"ח")]))

Q(8, "רוכב אופניים עלה מעפולה אל פסגת הר תבור במהירות קבועה של " + L("12") + " קמ\"ש. בדרך חזרה — מהפסגה אל עפולה, באותה הדרך — רכב במהירות קבועה של " + L("36") + " קמ\"ש. בסך הכול, הלוך וחזור, נמשכה הרכיבה " + L("2") + " שעות. סמנו ב־" + L("t") + " את זמן העלייה לפסגה (בשעות), בנו משוואה ופתרו, ובחרו את הפתרון הנכון ונמקו."
  + mc([("(1)", L("t = 0.5")), ("(2)", L("t = −2")), ("(3)", L("t = 3")), ("(4)", L("t = 1.5"))]))

Q(9, "לדני היו פי שניים בולים מאשר לרינה. לאחר שנתן לרינה " + L("7") + " בולים, היה להם מספר שווה. כמה בולים יש להם יחד? "
  "התאימו לכל בחירת משתנה את המשוואה המתאימה:"
  + parts([("•", L("x") + " = הבולים שהיו לדני בתחילה", 0),
           ("•", L("x") + " = הבולים שהיו לרינה בתחילה  →  " + L("2x − 7 = x + 7"), 0),
           ("•", L("x") + " = הבולים של שניהם יחד  →  " + L("x/2 − 7 = x/2 + 7"), 0)], ))

Q(10, "בסרטוט משולש שווה־צלעות ומחומש משוכלל. צלע המשולש " + L("10") + " ס\"מ וצלע המחומש " + L("d") + " ס\"מ. "
  "היקף המחומש גדול ב־" + L("5") + " ס\"מ מהיקף המשולש. בנו משוואה עם הנעלם " + L("d") + "."
  + fig(C.tri_pent(), w=52) + lines(1))

Q(11, "על פי הסרטוט, כתבו משוואה למציאת " + L("x") + "."
  + fig(C.eq_fig(), w=40) + lines(1))

Q(12, "ההיקף של משולש שווה־שוקיים הוא " + L("62") + " ס\"מ, ואורך השוק שלו גדול ב־" + L("13") + " ס\"מ מאורך הבסיס."
  + fig(C.iso_tri(), w=40)
  + parts([("א.", "סמנו ב־" + L("x") + " את אורך הבסיס ובנו משוואה למציאת " + L("x") + ".", 1),
           ("ב.", "סמנו ב־" + L("x") + " את אורך השוק ובנו משוואה למציאת " + L("x") + ".", 1)]))
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

Q(6, "<b>שיח מתמטי.</b> ארבעה תלמידים פתרו את המשוואה " + L("7x + 4(3x − 2) = 5x − 8") + ". התייחסו לפתרון של כל אחד — האם הוא נכון או שגוי? נמקו."
  + table(["ירון", "שירה", "מיכל", "אלון"],
          [[L("7x + 4(3x−2) = 5x−8") + "<br>" + L("19x − 8 = 5x − 8") + "<br>" + L("19x = 5x   / : x") + "<br>" + L("19 = 5") + "<br><b>אין פתרון!</b>",
            L("7x + 4(3x−2) = 5x−8") + "<br>" + L("19x − 8 = 5x − 8") + "<br>" + L("19x = 5x   / − 5x") + "<br>" + L("14x = 0") + "<br><b>x = 0</b>",
            "ברור שאין פתרון, כי לא ייתכן ש־" + L("5x") + " יהיה שווה ל־" + L("19x") + ".",
            "ירון ושירה קיבלו אותו דבר, כי \"אין פתרון\" זה כמו אפס!"]])
  + lines(3))

Q(7, "נתונות שתי משקולות. האחת כבדה פי " + L("2") + " מהאחרת, ומשקלן הכולל " + L("13.5") + " ק\"ג. מה משקל המשקולת הקלה?" + lines(2))

Q(8, "במשולש ישר־זווית, זווית חדה אחת קטנה ב־" + L("20°") + " מהזווית החדה האחרת. מצאו את גודל הזוויות." + lines(2))

Q(9, "דן גדול מיואב ב־" + L("6") + " שנים. לפני " + L("4") + " שנים היה גילו של דן פי " + L("2") + " מגילו של יואב. בני כמה דן ויואב כיום?" + lines(2))

Q(10, "בתחנת דלק א' מחיר הדלק " + L("6.45") + " ₪ לליטר ועמלת הלילה " + L("4") + " ₪; בתחנה ב' המחיר " + L("6.55") + " ₪ לליטר ועמלת הלילה " + L("2") + " ₪. "
  "לאיזו כמות דלק עלות התדלוק בלילה בשתי התחנות שווה?" + lines(2))

Q(11, "אנה ודן יוצאים באותו הזמן משני מקומות שהמרחק ביניהם " + L("14") + " ק\"מ, וצועדים זה לקראת זה. אנה צועדת במהירות קבועה של " + L("4") + " קמ\"ש, ודן במהירות " + L("6") + " קמ\"ש. בנו משוואה ומצאו כעבור כמה זמן הם ייפגשו."
  + fig(C.seg_walk(), w=56) + lines(2))

Q(12, "בסרטוט הקטעים " + L("AB") + " ו־" + L("CD") + " נחתכים בנקודה " + L("O") + ", והזוויות מסומנות כפי שמופיע בסרטוט (" + L("x") + " מייצג את " + L("∠DOB") + " במעלות). בנו משוואה, מצאו את " + L("x") + ", וחשבו את גודל " + L("∠AOD") + " (כתבו יחידות מתאימות)."
  + fig(C.fig_e13_cross(), w=50) + lines(2))
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
.cover .band { text-align:center; padding:0 28px; }
.cover .kick { font-size:10.5pt; letter-spacing:6px; color:#9aa1b3; font-weight:400; margin:0 0 18px; }
.cover h1 { font-size:30pt; font-weight:600; color:#3730a3; letter-spacing:1px; margin:0; }
.cover .rule { width:88px; height:3px; margin:18px auto 0; background:linear-gradient(90deg,#4f46e5,#7c3aed 55%,#0d9488); border-radius:2px; }
.cover .sub { font-size:13pt; color:#5b6573; font-weight:400; margin-top:16px; }
.cover .meta { margin-top:14px; font-size:11pt; opacity:.9; }
.toc { margin:40px 6px 0; }
.toc h2 { color:#1f2a44; font-size:12pt; font-weight:600; letter-spacing:5px; padding-bottom:12px; border-bottom:1.5px solid #1f2a44; margin:0; }
.toc ol { list-style:none; padding:0; margin:0; }
.toc li { border-bottom:0.75px solid #ececf1; }
.toc .tl { display:flex; align-items:center; gap:18px; padding:13px 2px; text-decoration:none; color:inherit; border-radius:8px; }
.toc .tl:hover { background:#f6f7fb; }
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
toc = "".join(f'<li style="--cc:{c}"><a class="tl" href="#sec-{_HSEQ.index(l)+1}"><span class="idx">{l}</span><span class="nm">{t}</span><span class="tick"></span></a></li>' for l,t,c in TOPICS)

cover = f"""<div class="cover">
  <div class="band">
    <div class="kick">מתמטיקה · חטיבת הביניים</div>
    <h1>אלגברה לכיתה ז'</h1>
    <div class="rule"></div>
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
toc_rows = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":703,"height":2000}); pg.goto(url)
    pg.emulate_media(media="print")
    toc_rows = pg.evaluate("""()=>{const c=document.querySelector('.cover');if(!c)return[];
      const cb=c.getBoundingClientRect();
      return [...c.querySelectorAll('.toc .tl')].map(a=>{const r=a.getBoundingClientRect();
        const fx=(r.left-cb.left)/cb.width, fy=(r.top-cb.top)/cb.height, fw=r.width/cb.width, fh=r.height/cb.height;
        return {l:(12+fx*186)/210, t:(16+fy*262)/297, w:fw*186/210, h:fh*262/297};});}""")
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
chap_pg = sorted(l["page"] + 1 for l in _doc[0].get_links() if l.get("page", -1) >= 0)
for i in range(npages): _doc[i].get_pixmap(dpi=120).save(os.path.join(pages_dir, f"p{i+1:03d}.png"))
_doc.close()
ts = int(time.time()); pdf_href = urllib.parse.quote(PDF_NAME)
_hot = "".join(f'<a class="hot" href="#p{pg}" style="left:{r["l"]*100:.3f}%;top:{r["t"]*100:.3f}%;width:{r["w"]*100:.3f}%;height:{r["h"]*100:.3f}%" aria-label="מעבר לפרק"></a>' for r, pg in zip(toc_rows, chap_pg))
def _sheet(i):
    img = f'<img src="assets/pages/p{i+1:03d}.png?v={ts}" loading="lazy" alt="עמוד {i+1}">'
    body = f'<div class="imgwrap">{img}{_hot}</div>' if (i == 0 and toc_rows) else img
    return f'<div class="sheet" id="p{i+1}">{body}<div class="pgn">עמוד {i+1} / {npages}</div></div>'
sheets = "".join(_sheet(i) for i in range(npages))
chapnav = "".join(f'<a class="tc" href="#p{pg}" style="--cc:{c}"><i>{l}</i>{t}</a>' for (l, t, c), pg in zip(TOPICS, chap_pg))
viewer = f"""<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>אלגברה לכיתה ז — תצוגת הדפים</title><style>
 html{{scroll-behavior:smooth}}
 html,body{{margin:0;background:#e9ebf0;font-family:'Segoe UI',Arial,sans-serif}}
 .head{{position:sticky;top:0;z-index:6}}
 .bar{{background:#191c2e;color:#eef;padding:11px 16px;font-size:13.5px;display:flex;gap:16px;align-items:center;justify-content:center}}
 .bar b{{color:#fff}} .bar a{{color:#8ad7ff;text-decoration:none;font-weight:600}}
 .chapters{{background:#21243a;display:flex;gap:8px;overflow-x:auto;padding:9px 12px;border-top:1px solid #2c3050;-webkit-overflow-scrolling:touch}}
 .tc{{flex:0 0 auto;display:inline-flex;align-items:center;gap:7px;background:#2c3050;color:#dfe3f2;text-decoration:none;border-radius:999px;padding:6px 13px 6px 7px;font-size:12px;white-space:nowrap}}
 .tc i{{width:19px;height:19px;border-radius:50%;background:var(--cc);color:#fff;display:flex;align-items:center;justify-content:center;font-style:normal;font-weight:700;font-size:11px;flex:0 0 auto}}
 .tc:hover{{background:#363c63;color:#fff}}
 .wrap{{padding:22px 10px 70px;display:flex;flex-direction:column;align-items:center;gap:22px}}
 .sheet{{width:min(820px,96vw);background:#fff;box-shadow:0 5px 20px rgba(20,25,50,.22);border-radius:3px;overflow:hidden;scroll-margin-top:108px}}
 .sheet img{{display:block;width:100%;height:auto;aspect-ratio:210/297}}
 .imgwrap{{position:relative;line-height:0}}
 .hot{{position:absolute;display:block;border-radius:7px;transition:background .12s}}
 .hot:hover{{background:rgba(79,70,229,.15);box-shadow:0 0 0 2px rgba(79,70,229,.5) inset}}
 .pgn{{text-align:center;color:#7a8194;font-size:11px;padding:6px;background:#fafbfd;border-top:1px solid #eef}}
</style></head><body>
<div class="head"><div class="bar"><a href="index.html">⌂ דף הבית</a> <span>📄 <b>תצוגת הדפים A4</b> · {npages} עמודים</span> <a href="{pdf_href}?v={ts}" download>⬇ הורדה</a></div>
<div class="chapters">{chapnav}</div></div>
<div class="wrap">{sheets}</div></body></html>"""
open(os.path.join(OUT, "viewer.html"), "w", encoding="utf-8").write(viewer)

nq = len([c for c in CARDS if c.startswith('<div class="q"')]); nchap = len(TOPICS)
chips = "".join(f'<span class="chip" style="--cc:{c}"><i>{l}</i>{t}</span>' for l,t,c in TOPICS)
APP = """<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>אלגברה לכיתה ז — אוסף שאלות</title><style>
 *{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
 body{font-family:'Segoe UI','Arial',sans-serif;color:#1f2a44;min-height:100vh;background:radial-gradient(1100px 560px at 85% -12%,#e7ecff 0,transparent 60%),radial-gradient(820px 460px at -5% 2%,#dff5ee 0,transparent 55%),#f4f6fb}
 .wrap{max-width:680px;margin:0 auto;padding:26px 16px 60px}
 .hero{text-align:center;padding:26px 16px 6px}
 .hero .kick{font-size:11px;letter-spacing:5px;color:#9aa1b3;margin-bottom:12px}
 .hero h1{font-size:clamp(24px,6vw,30px);font-weight:600;color:#3730a3;letter-spacing:.5px;margin:0}
 .hero .rule{width:84px;height:3px;margin:14px auto 0;background:linear-gradient(90deg,#4f46e5,#7c3aed 55%,#0d9488);border-radius:2px}
 .hero p{color:#5b6573;font-size:clamp(13px,3.6vw,15px);margin-top:14px}
 .stats{display:flex;gap:10px;justify-content:center;margin:18px auto 0;max-width:420px;position:relative}
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
 <div class="hero"><div class="kick">אוסף שאלות להדפסה</div><h1>אלגברה לכיתה ז'</h1><div class="rule"></div><p>ביטויים אלגבריים · משוואות · גרפים</p></div>
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
