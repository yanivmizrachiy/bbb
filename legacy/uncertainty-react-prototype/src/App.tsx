import React, { useState } from 'react';
import { Printer, FileText, Check, Palette, Edit2, Award, Copy, AlertCircle } from 'lucide-react';
import html2canvas from 'html2canvas';

interface Theme {
  id: string;
  name: string;
  primary: string;
  accent: string;
  text: string;
  border: string;
  divider: string;
  canvasBg: string;
  cardBg: string;
  cardBgHex: string;
  fontFamily: string;
}

const themes: Theme[] = [
  {
    id: 'hybrid-blue-academic',
    name: 'היברידי כחול-אקדמי דלוקס',
    primary: '#112b4c',
    accent: '#274266',
    text: '#112b4c',
    border: '#112b4c',
    divider: '#cbd5e1',
    canvasBg: 'bg-[#eef2f7]',
    cardBg: 'bg-[#fafaf9]',
    cardBgHex: '#fafaf9',
    fontFamily: 'system-ui, -apple-system, sans-serif'
  },
  {
    id: 'noble-slate',
    name: 'כחול אצילי מינימליסטי',
    primary: '#112b4c',
    accent: '#274266',
    text: '#112b4c',
    border: '#112b4c',
    divider: '#d4dde8',
    canvasBg: 'bg-[#eef2f7]',
    cardBg: 'bg-white',
    cardBgHex: '#ffffff',
    fontFamily: 'system-ui, -apple-system, sans-serif'
  },
  {
    id: 'oxford-academic',
    name: 'אקדמי שנהב יוקרתי',
    primary: '#1e293b',
    accent: '#475569',
    text: '#0f172a',
    border: '#475569',
    divider: '#cbd5e1',
    canvasBg: 'bg-[#f1f5f9]',
    cardBg: 'bg-[#fafaf9]',
    cardBgHex: '#fafaf9',
    fontFamily: 'system-ui, -apple-system, sans-serif'
  }
];

interface Question {
  id: number;
  number: string;
  title: string;
  correctChoice: string;
  solutionExplanation: string;
  renderVisual: (color: string) => React.ReactNode;
  choices: { letter: string; text: string }[];
}

const renderMathOptionText = (text: string) => {
  const parts = text.split(/(\d+\/\d+)/g);
  return (
    <span className="inline-flex flex-wrap items-center gap-0.5">
      {parts.map((part, index) => {
        const match = part.match(/^(\d+)\/(\d+)$/);
        if (match) {
          const [, num, den] = match;
          return (
            <span 
              key={index} 
              className="inline-flex flex-col items-center justify-center text-center font-serif font-semibold leading-none mx-1 text-[1.1em] select-none" 
              style={{ direction: 'ltr', verticalAlign: 'middle' }}
            >
              <span className="border-b border-slate-700 pb-0.5 leading-none px-0.5" style={{ minWidth: '1em' }}>{num}</span>
              <span className="pt-0.5 leading-none px-0.5" style={{ minWidth: '1em' }}>{den}</span>
            </span>
          );
        }
        return <span key={index} className="leading-relaxed">{part}</span>;
      })}
    </span>
  );
};

export default function App() {
  const [currentTheme, setCurrentTheme] = useState<Theme>(themes[0]);
  const [activeQuestionId, setActiveQuestionId] = useState<number>(1);
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [printAllBooklet, setPrintAllBooklet] = useState<boolean>(true);
  const [copyState, setCopyState] = useState<'idle' | 'copying' | 'success' | 'error'>('idle');

  // Editable fields state
  const [editableQuestions, setEditableQuestions] = useState<Record<number, { title: string; choiceTexts: string[] }>>({
    1: {
      title: 'בסיבוב של גלגל המזל שלפניכם, מהי ההסתברות שהמחוג ייעצר על הצבע הכחול?',
      choiceTexts: ['1/2', '1/4', '1/8', '3/4']
    },
    2: {
      title: 'בכד מונחים שלושה כדורים כחולים, חמישה כדורים צהובים ושני כדורים ירוקים. מוציאים באקראי כדור אחד מהכד. מהי ההסתברות שהכדור שהוצא אינו ירוק?',
      choiceTexts: ['3/10', '1/2', '4/5', '7/10']
    },
    3: {
      title: 'לפניכם דיאגרמת עמודות המציגה את התפלגות הציונים במבחן במתמטיקה בכיתה ז׳. מוציאים באקראי תלמיד אחד מהכיתה. מהי ההסתברות שציונו גבוה מ-80?',
      choiceTexts: ['3/7', '2/7', '4/7', '1/2']
    },
    4: {
      title: 'מטילים פעמיים מטבע הוגן. על צד אחד של המטבע רשום \'עץ\' ועל הצד השני רשום \'פלי\'. מהי ההסתברות לקבל בשתי ההטלות את אותו הצד?',
      choiceTexts: ['1/4', '1/2', '3/4', '1/3']
    },
    5: {
      title: 'לפניכם גלגל מסתובב המחולק ל-8 גזרות שוות וזהות, הממוספרות מ-1 עד 8. מסובבים את הגלגל פעם אחת באקראי. מהי ההסתברות שהמחוג ייעצר על מספר ראשוני?',
      choiceTexts: ['1/2', '3/8', '5/8', '1/4']
    },
    6: {
      title: 'בשקית נייר אטומה יש 5 סוכריות בטעם תות ו-3 סוכריות בטעם לימון. דני מוציא סוכרייה אחת מבלי להביט. לפניכם 4 טענות. מצאו את הטענה שהיא נכונה בהכרח ונמקו מדוע:',
      choiceTexts: [
        'ההסתברות להוציא סוכריית תות היא 1.',
        'ההסתברות להוציא סוכריית מנטה היא 0.',
        'ההסתברות להוציא סוכריית תות קטנה מההסתברות להוציא סוכריית לימון.',
        'ההסתברות להוציא סוכרייה שאינה לימון היא 3/8.'
      ]
    },
    7: {
      title: 'לפניכם ציר הסתברות הנע בין מספרים 0 (אירוע בלתי אפשרי) ל-1 (אירוע ודאי). אם הסבירות שירד מחר גשם היא 0.15, היכן ממוקמת הסתברות זו על גבי הציר?',
      choiceTexts: [
        'קרובה מאוד ל-1 (ודאי כמעט לחלוטין).',
        'בדיוק באמצע (סיכוי שווה של חצי-חצי).',
        'קרובה מאוד ל-0 (סבירות נמוכה מאוד אך אפשרית).',
        'בדיוק ב-0 (אירוע בלתי אפשרי לחלוטין).'
      ]
    },
    8: {
      title: 'מטילים בו-זמנית שני מטבעות הוגנים בעלי שני צדדים: "עץ" או "פלי". מהי ההסתברות לקבל לכל היותר פעם אחת "עץ"?',
      choiceTexts: ['1/4', '1/2', '3/4', '1']
    }
  });

  const baseQuestions: Question[] = [
    {
      id: 1,
      number: '1',
      title: editableQuestions[1].title,
      correctChoice: 'ב',
      solutionExplanation: 'הגלגל מחולק ל-4 רבעים שווים. רבע אחד צבוע בכחול כהה (1/4 מהשטח כולו), ולכן ההסתברות שהמחוג ייעצר עליו היא בדיוק 1/4 (25%).',
      choices: [
        { letter: 'א', text: editableQuestions[1].choiceTexts[0] },
        { letter: 'ב', text: editableQuestions[1].choiceTexts[1] },
        { letter: 'ג', text: editableQuestions[1].choiceTexts[2] },
        { letter: 'ד', text: editableQuestions[1].choiceTexts[3] }
      ],
      renderVisual: (color) => (
        <svg width="180" height="180" viewBox="0 0 100 100" className="mx-auto select-none">
          <circle cx="50" cy="50" r="48" fill="#ffffff" stroke="#112b4c" strokeWidth="0.7"/>
          {/* Top-Left: Gray */}
          <path d="M 50 50 L 2 50 A 48 48 0 0 1 50 2 Z" fill="#e2e8f0" stroke="#112b4c" strokeWidth="0.5"/>
          {/* Bottom-Left: Corporate Deep Blue (representing the blue sector) */}
          <path d="M 50 50 L 50 98 A 48 48 0 0 1 2 50 Z" fill="#112b4c" stroke="#112b4c" strokeWidth="0.5"/>
          {/* Bottom-Right: White */}
          <path d="M 50 50 L 98 50 A 48 48 0 0 1 50 98 Z" fill="#ffffff" stroke="#112b4c" strokeWidth="0.5"/>
          {/* Top-Right: Soft Yellowish */}
          <path d="M 50 50 L 50 2 A 48 48 0 0 1 98 50 Z" fill="#fef08a" stroke="#112b4c" strokeWidth="0.5"/>
          <circle cx="50" cy="50" r="2.5" fill="#112b4c"/>
          <polyline points="50,50 50,20" stroke="#112b4c" strokeWidth="1.5" strokeLinecap="round"/>
          <polygon points="50,15 47,22 53,22" fill="#112b4c"/>
        </svg>
      )
    },

    {
      id: 2,
      number: '2',
      title: editableQuestions[2].title,
      correctChoice: 'ג',
      solutionExplanation: 'בכד מונחים 3 כדורים כחולים, 5 כדורים צהובים ו-2 ירוקים, ובסך הכל יש 10 כדורים. מספר הכדורים שאינם ירוקים (כלומר כחולים או צהובים) הוא 3 + 5 = 8 כדורים. לכן ההסתברות להוציא כדור שאינו ירוק היא 8/10, ולאחר צמצום של השבר ב-2 נקבל 4/5 (או 80%).',
      choices: [
        { letter: 'א', text: editableQuestions[2].choiceTexts[0] },
        { letter: 'ב', text: editableQuestions[2].choiceTexts[1] },
        { letter: 'ג', text: editableQuestions[2].choiceTexts[2] },
        { letter: 'ד', text: editableQuestions[2].choiceTexts[3] }
      ],
      renderVisual: (color) => (
        <svg width="180" height="180" viewBox="0 0 100 100" className="mx-auto select-none">
          {/* Transparent jar scale outline */}
          <path d="M 35 15 L 65 15 L 65 25 C 75 35, 78 50, 75 80 C 72 92, 28 92, 25 80 C 22 50, 25 35, 35 25 Z" fill="#ffffff" stroke="#112b4c" strokeWidth="1.5" />
          <line x1="32" y1="18" x2="68" y2="18" stroke="#112b4c" strokeWidth="1" />
          
          {/* Blue marbles (3) */}
          <circle cx="40" cy="78" r="5" fill="#112b4c" stroke="#112b4c" strokeWidth="0.3" />
          <circle cx="50" cy="80" r="5" fill="#112b4c" stroke="#112b4c" strokeWidth="0.3" />
          <circle cx="60" cy="78" r="5" fill="#112b4c" stroke="#112b4c" strokeWidth="0.3" />
          
          {/* Yellow Marbles (5) */}
          <circle cx="45" cy="70" r="5" fill="#facc15" stroke="#112b4c" strokeWidth="0.3" />
          <circle cx="55" cy="72" r="5" fill="#facc15" stroke="#112b4c" strokeWidth="0.3" />
          <circle cx="37" cy="65" r="5" fill="#facc15" stroke="#112b4c" strokeWidth="0.3" />
          <circle cx="50" cy="62" r="5" fill="#facc15" stroke="#112b4c" strokeWidth="0.3" />
          <circle cx="63" cy="67" r="5" fill="#facc15" stroke="#112b4c" strokeWidth="0.3" />
          
          {/* Green Marbles (2) */}
          <circle cx="43" cy="54" r="5" fill="#22c55e" stroke="#112b4c" strokeWidth="0.3" />
          <circle cx="57" cy="52" r="5" fill="#22c55e" stroke="#112b4c" strokeWidth="0.3" />
        </svg>
      )
    },
    {
      id: 3,
      number: '3',
      title: editableQuestions[3].title,
      correctChoice: 'א',
      solutionExplanation: 'סכום כלל התלמידים בכיתה הוא: 6 (ציון 70) + 10 (ציון 80) + 8 (ציון 90) + 4 (ציון 100) = 28 תלמידים. מספר התלמידים שקיבלו ציון גבוה מ-80 (כלומר 90 או 100) הוא: 8 + 4 = 12 תלמידים. ההסתברות שבוחרים באקראי תלמיד שקיבל מעל 80 היא 12/28. לאחר צמצום של השבר ב-4 נקבל 3/7.',
      choices: [
        { letter: 'א', text: editableQuestions[3].choiceTexts[0] },
        { letter: 'ב', text: editableQuestions[3].choiceTexts[1] },
        { letter: 'ג', text: editableQuestions[3].choiceTexts[2] },
        { letter: 'ד', text: editableQuestions[3].choiceTexts[3] }
      ],
      renderVisual: (color) => (
        <svg width="240" height="180" viewBox="0 0 120 80" className="mx-auto select-none">
          <line x1="15" y1="10" x2="15" y2="70" stroke="#112b4c" strokeWidth="0.5" />
          <line x1="15" y1="70" x2="110" y2="70" stroke="#112b4c" strokeWidth="0.5" />
          
          {/* Grid lines */}
          <line x1="15" y1="50" x2="110" y2="50" stroke="#f1f5f9" strokeWidth="0.2" />
          <line x1="15" y1="30" x2="110" y2="30" stroke="#f1f5f9" strokeWidth="0.2" />
          
          {/* Y Axis indicators and labels */}
          <text x="8" y="72" fontSize="3" fill="#112b4c">0</text>
          <text x="8" y="52" fontSize="3" fill="#112b4c">5</text>
          <text x="6" y="32" fontSize="3" fill="#112b4c">10</text>
 
          {/* Bar 1 (Grade: 70, Count: 6) */}
          <rect x="25" y="46" width="12" height="24" fill="#cbd5e1" stroke="#112b4c" strokeWidth="0.3" />
          <text x="31" y="76" fontSize="4.5" fill="#112b4c" textAnchor="middle">70</text>
          <text x="31" y="42" fontSize="3.5" fill="#112b4c" textAnchor="middle">6</text>
 
          {/* Bar 2 (Grade: 80, Count: 10) */}
          <rect x="45" y="30" width="12" height="40" fill="#cbd5e1" stroke="#112b4c" strokeWidth="0.3" />
          <text x="51" y="76" fontSize="4.5" fill="#112b4c" textAnchor="middle">80</text>
          <text x="51" y="26" fontSize="3.5" fill="#112b4c" textAnchor="middle">10</text>
 
          {/* Bar 3 (Grade: 90, Count: 8) */}
          <rect x="65" y="38" width="12" height="32" fill="#112b4c" stroke="#112b4c" strokeWidth="0.3" />
          <text x="71" y="76" fontSize="4.5" fill="#112b4c" textAnchor="middle">90</text>
          <text x="71" y="34" fontSize="3.5" fill="#112b4c" textAnchor="middle">8</text>
 
          {/* Bar 4 (Grade: 100, Count: 4) */}
          <rect x="85" y="54" width="12" height="16" fill="#112b4c" stroke="#112b4c" strokeWidth="0.3" />
          <text x="91" y="76" fontSize="4.5" fill="#112b4c" textAnchor="middle">100</text>
          <text x="91" y="50" fontSize="3.5" fill="#112b4c" textAnchor="middle">4</text>
        </svg>
      )
    },












    {
      id: 4,
      number: '4',
      title: editableQuestions[4].title,
      correctChoice: 'ב',
      solutionExplanation: 'בדיאגרמת העץ יש ארבעה מסלולים אפשריים בעלי סיכוי שווה לקבלת תוצאה: (עץ, עץ), (עץ, פלי), (פלי, עץ), (פלי, פלי). התוצאות שבהן מתקבל אותו הצד בשתי ההטלות הן (עץ, עץ) ו-(פלי, פלי) – סך הכל 2 אפשרויות מתוך 4. לכן ההסתברות המבוקשת היא 2/4, השווה לחצי (1/2, או 50%).',
      choices: [
        { letter: 'א', text: editableQuestions[4].choiceTexts[0] },
        { letter: 'ב', text: editableQuestions[4].choiceTexts[1] },
        { letter: 'ג', text: editableQuestions[4].choiceTexts[2] },
        { letter: 'ד', text: editableQuestions[4].choiceTexts[3] }
      ],
      renderVisual: (color) => (
        <svg width="240" height="180" viewBox="0 0 140 80" className="mx-auto">
          {/* Main node starting point */}
          <circle cx="20" cy="40" r="3" fill={color} />
          <text x="12" y="48" fontSize="4" fontWeight="bold" fill={color}>התחלה</text>
          
          {/* First Branch Leaves */}
          <line x1="23" y1="40" x2="55" y2="20" stroke={color} strokeWidth="0.5" />
          <line x1="23" y1="40" x2="55" y2="60" stroke={color} strokeWidth="0.5" />
          
          <circle cx="55" cy="20" r="2.5" fill={color} />
          <text x="53" y="15" fontSize="4.5" fill={color}>עץ</text>
          <circle cx="55" cy="60" r="2.5" fill={color} />
          <text x="53" y="66" fontSize="4.5" fill={color}>פלי</text>

          {/* Second level branches upper */}
          <line x1="57.5" y1="20" x2="95" y2="10" stroke={color} strokeWidth="0.3" />
          <line x1="57.5" y1="20" x2="95" y2="30" stroke={color} strokeWidth="0.3" />
          
          <circle cx="95" cy="10" r="2" fill={color} />
          <text x="99" y="11.5" fontSize="4" fill={color}>עץ</text>
          <circle cx="95" cy="30" r="2" fill={color} />
          <text x="99" y="31.5" fontSize="4" fill={color}>פלי</text>

          {/* Second level branches lower */}
          <line x1="57.5" y1="60" x2="95" y2="50" stroke={color} strokeWidth="0.3" />
          <line x1="57.5" y1="60" x2="95" y2="70" stroke={color} strokeWidth="0.3" />
          
          <circle cx="95" cy="50" r="2" fill={color} />
          <text x="99" y="51.5" fontSize="4" fill={color}>עץ</text>
          <circle cx="95" cy="70" r="2" fill={color} />
          <text x="99" y="71.5" fontSize="4" fill={color}>פלי</text>
        </svg>
      )
    },
    {
      id: 5,
      number: '5',
      title: editableQuestions[5].title,
      correctChoice: 'א',
      solutionExplanation: 'הגלגל מחולק ל-8 חלקים שווים. המספרים הראשוניים בין 1 ל-8 הם: 2, 3, 5, 7 (סך הכל 4 מספרים). ההסתברות לקבל מספר ראשוני היא 4/8, שהם בדיוק 1/2.',
      choices: [
        { letter: 'א', text: editableQuestions[5].choiceTexts[0] },
        { letter: 'ב', text: editableQuestions[5].choiceTexts[1] },
        { letter: 'ג', text: editableQuestions[5].choiceTexts[2] },
        { letter: 'ד', text: editableQuestions[5].choiceTexts[3] }
      ],
      renderVisual: (color) => (
        <svg width="180" height="180" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="48" fill="#ffffff" stroke={color} strokeWidth="0.7"/>
          <line x1="50" y1="2" x2="50" y2="98" stroke={color} strokeWidth="0.5"/>
          <line x1="2" y1="50" x2="98" y2="50" stroke={color} strokeWidth="0.5"/>
          <line x1="16" y1="16" x2="84" y2="84" stroke={color} strokeWidth="0.5"/>
          <line x1="16" y1="84" x2="84" y2="16" stroke={color} strokeWidth="0.5"/>
          
          <text x="68" y="28" fontSize="6" textAnchor="middle" fill={color}>1</text>
          <text x="80" y="47" fontSize="6" textAnchor="middle" fill={color}>2</text>
          <text x="73" y="69" fontSize="6" textAnchor="middle" fill={color}>3</text>
          <text x="50" y="80" fontSize="6" textAnchor="middle" fill={color}>4</text>
          <text x="27" y="69" fontSize="6" textAnchor="middle" fill={color}>5</text>
          <text x="20" y="47" fontSize="6" textAnchor="middle" fill={color}>6</text>
          <text x="28" y="28" fontSize="6" textAnchor="middle" fill={color}>7</text>
          <text x="50" y="22" fontSize="6" textAnchor="middle" fill={color}>8</text>
          
          <circle cx="50" cy="50" r="3.5" fill={color}/>
          <polyline points="50,50 32,32" stroke={color} strokeWidth="1.2" strokeLinecap="round"/>
          <polygon points="30,30 38,32 32,38" fill={color}/>
        </svg>
      )
    },
    {
      id: 6,
      number: '6',
      title: editableQuestions[6].title,
      correctChoice: 'ב',
      solutionExplanation: 'בשקית יש רק סוכריות בטעמי תות ולימון. מכיוון שאין אף סוכריית מנטה בשקית, האירוע "להוציא סוכריית מנטה" הוא אירוע בלתי אפשרי, וההסתברות שלו היא בדיוק 0.',
      choices: [
        { letter: 'א', text: editableQuestions[6].choiceTexts[0] },
        { letter: 'ב', text: editableQuestions[6].choiceTexts[1] },
        { letter: 'ג', text: editableQuestions[6].choiceTexts[2] },
        { letter: 'ד', text: editableQuestions[6].choiceTexts[3] }
      ],
      renderVisual: (color) => (
        <svg width="180" height="180" viewBox="0 0 100 100">
          <path d="M 30 30 L 35 85 L 65 85 L 70 30 Z" fill="#ffffff" stroke={color} strokeWidth="0.8"/>
          <path d="M 28 30 L 72 30 L 68 23 L 32 23 Z" fill="#f1f5f9" stroke={color} strokeWidth="0.8"/>
          
          <g stroke={color} strokeWidth="0.5">
            {/* Candy 1 */}
            <circle cx="43" cy="74" r="4" fill="#fc8181"/>
            <polygon points="39,74 36,71 36,77" fill="#fc8181"/>
            <polygon points="47,74 50,71 50,77" fill="#fc8181"/>
            
            {/* Candy 2 */}
            <circle cx="57" cy="76" r="4" fill="#fc8181"/>
            <polygon points="53,76 50,73 50,79" fill="#fc8181"/>
            <polygon points="61,76 64,73 64,79" fill="#fc8181"/>
            
            {/* Candy 3 */}
            <circle cx="50" cy="80" r="4" fill="#fc8181"/>
            <polygon points="46,80 43,77 43,83" fill="#fc8181"/>
            <polygon points="54,80 57,77 57,83" fill="#fc8181"/>

            {/* Candy 4 */}
            <circle cx="40" cy="63" r="4" fill="#fc8181"/>
            <polygon points="36,63 33,60 33,66" fill="#fc8181"/>
            <polygon points="44,63 47,60 47,66" fill="#fc8181"/>

            {/* Candy 5 */}
            <circle cx="51" cy="67" r="4" fill="#fc8181"/>
            <polygon points="47,67 44,64 44,70" fill="#fc8181"/>
            <polygon points="55,67 58,64 58,70" fill="#fc8181"/>
          </g>
          <g stroke={color} strokeWidth="0.5">
            {/* Candy 1 */}
            <circle cx="59" cy="61" r="4" fill="#f6e05e"/>
            <polygon points="55,61 52,58 52,64" fill="#f6e05e"/>
            <polygon points="63,61 66,58 66,64" fill="#f6e05e"/>

            {/* Candy 2 */}
            <circle cx="46" cy="55" r="4" fill="#f6e05e"/>
            <polygon points="42,55 39,52 39,58" fill="#f6e05e"/>
            <polygon points="50,55 53,52 53,58" fill="#f6e05e"/>

            {/* Candy 3 */}
            <circle cx="53" cy="49" r="4" fill="#f6e05e"/>
            <polygon points="49,49 46,46 46,52" fill="#f6e05e"/>
            <polygon points="57,49 60,46 60,52" fill="#f6e05e"/>
          </g>
        </svg>
      )
    },
    {
      id: 7,
      number: '7',
      title: editableQuestions[7].title,
      correctChoice: 'ג',
      solutionExplanation: 'ההסתברות 0.15 היא מספר קטן מאוד, קרוב ל-0. אירוע כזה הוא אפשרי (אינו 0) אך בסבירות נמוכה מאוד, ולכן הוא ממוקם קרוב מאוד לקצה השמאלי של ציר ההסתברות.',
      choices: [
        { letter: 'א', text: editableQuestions[7].choiceTexts[0] },
        { letter: 'ב', text: editableQuestions[7].choiceTexts[1] },
        { letter: 'ג', text: editableQuestions[7].choiceTexts[2] },
        { letter: 'ד', text: editableQuestions[7].choiceTexts[3] }
      ],
      renderVisual: (color) => (
        <svg width="240" height="120" viewBox="0 0 120 60">
          <line x1="15" y1="30" x2="105" y2="30" stroke={color} strokeWidth="0.8"/>
          <line x1="15" y1="26" x2="15" y2="34" stroke={color} strokeWidth="0.8"/>
          <text x="15" y="42" fontSize="3.5" textAnchor="middle" fill={color}>0</text>
          <text x="15" y="21" fontSize="3" textAnchor="middle" fill={color}>בלתי אפשרי</text>

          <line x1="37.5" y1="28" x2="37.5" y2="32" stroke={color} strokeWidth="0.5"/>
          <text x="37.5" y="42" fontSize="3" textAnchor="middle" fill="#94a3b8">0.25</text>

          <line x1="60" y1="26" x2="60" y2="34" stroke={color} strokeWidth="0.8"/>
          <text x="60" y="42" fontSize="3.5" textAnchor="middle" fill={color}>0.5</text>
          <text x="60" y="21" fontSize="3" textAnchor="middle" fill={color}>חצי-חצי</text>

          <line x1="82.5" y1="28" x2="82.5" y2="32" stroke={color} strokeWidth="0.5"/>
          <text x="82.5" y="42" fontSize="3" textAnchor="middle" fill="#94a3b8">0.75</text>

          <line x1="105" y1="26" x2="105" y2="34" stroke={color} strokeWidth="0.8"/>
          <text x="105" y="42" fontSize="3.5" textAnchor="middle" fill={color}>1</text>
          <text x="105" y="21" fontSize="3" textAnchor="middle" fill={color}>ודאי בהחלט</text>
        </svg>
      )
    },
    {
      id: 8,
      number: '8',
      title: editableQuestions[8].title,
      correctChoice: 'ג',
      solutionExplanation: 'כשמטילים שני מטבעות יש 4 אפשרויות שוות סיכוי: (עץ, עץ), (עץ, פלי), (פלי, עץ), (פלי, פלי). האירוע "לכל היותר פעם אחת עץ" כולל את האפשרויות עם פעם אחת עץ או אפס פעמים (כלומר, הכל חוץ מהטלת פעמיים עץ). אלו 3 תוצאות מתוך 4, בסבירות של 3/4.',
      choices: [
        { letter: 'א', text: editableQuestions[8].choiceTexts[0] },
        { letter: 'ב', text: editableQuestions[8].choiceTexts[1] },
        { letter: 'ג', text: editableQuestions[8].choiceTexts[2] },
        { letter: 'ד', text: editableQuestions[8].choiceTexts[3] }
      ],
      renderVisual: (color) => (
        <svg width="240" height="120" viewBox="0 0 160 80">
          <g stroke={color} strokeWidth="0.8">
            <circle cx="50" cy="40" r="24" fill="#f8fafc"/>
            <circle cx="50" cy="40" r="21" fill="none" strokeDasharray="2,2"/>
            <path d="M 50 25 L 50 55 M 50 35 L 40 28 M 50 35 L 60 28 M 50 45 L 38 38 M 50 45 L 62 38" fill="none" strokeLinecap="round"/>
            <text x="50" y="52" fontSize="6" textAnchor="middle" fill={color} fontWeight="bold">עץ</text>
          </g>
          <text x="80" y="43" fontSize="10" textAnchor="middle" fill={color}>+</text>
          <g stroke={color} strokeWidth="0.8">
            <circle cx="110" cy="40" r="24" fill="#f8fafc"/>
            <circle cx="110" cy="40" r="21" fill="none" strokeDasharray="2,2"/>
            <path d="M 103 27 L 117 27 M 106 27 L 106 48 C 106 52 114 52 114 48 L 114 27 M 110 27 L 110 49" fill="none" strokeLinecap="round"/>
            <text x="110" y="52" fontSize="6" textAnchor="middle" fill={color} fontWeight="bold">פלי</text>
          </g>
        </svg>
      )
    }
  ];

  const handlePrint = () => {
    window.print();
  };

  const copyQuestionAsImage = async () => {
    setCopyState('copying');
    try {
      const element = document.getElementById('worksheet-preview-container');
      if (!element) {
        throw new Error('Preview container not found');
      }

      // 1. Try with a safe, standard high-resolution scale first (e.g. 1.5 instead of 2.5) to avoid memory crashes on iPad/Mobile
      const canvas = await html2canvas(element, {
        scale: 1.5,
        useCORS: true,
        allowTaint: true, // Prevents throwing errors on third-party elements & custom styles
        backgroundColor: '#fafaf9',
        logging: false,
        onclone: (clonedDoc) => {
          const clonedEl = clonedDoc.getElementById('worksheet-preview-container');
          if (clonedEl) {
            clonedEl.style.borderRadius = '0px';
            clonedEl.style.boxShadow = 'none';
            clonedEl.style.border = 'none';
          }
        }
      });

      const dataUrl = canvas.toDataURL('image/png');

      // 2. Try copying to the clipboard
      let clipboardSuccess = false;
      try {
        if (navigator.clipboard && typeof ClipboardItem !== 'undefined') {
          const res = await fetch(dataUrl);
          const blob = await res.blob();
          await navigator.clipboard.write([
            new ClipboardItem({ 'image/png': blob })
          ]);
          clipboardSuccess = true;
        }
      } catch (clipErr) {
        console.warn('Clipboard write was restricted by sandbox permissions. Continuing with automatic system download...', clipErr);
      }

      // 3. Always trigger an automatic image download as a guaranteed fail-safe so the user receives the image!
      const link = document.createElement('a');
      link.download = `question-0${activeQuestionId}-hq.png`;
      link.href = dataUrl;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      setCopyState('success');
      setTimeout(() => setCopyState('idle'), 3000);

    } catch (err) {
      console.error('High-resolution render failed, attempting ultra-safe scale 1.0 fallback:', err);
      try {
        const element = document.getElementById('worksheet-preview-container');
        if (element) {
          const canvasSafe = await html2canvas(element, {
            scale: 1.0,
            useCORS: true,
            allowTaint: true,
            backgroundColor: '#ffffff',
            logging: false
          });
          const dataUrl = canvasSafe.toDataURL('image/png');
          const link = document.createElement('a');
          link.download = `question-0${activeQuestionId}-standard.png`;
          link.href = dataUrl;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          
          setCopyState('success');
          setTimeout(() => setCopyState('idle'), 3000);
          return;
        }
      } catch (safeErr) {
        console.error('Standard safe fallback also failed:', safeErr);
      }
      setCopyState('error');
      setTimeout(() => setCopyState('idle'), 3000);
    }
  };

  const handleEditChange = (field: 'title' | 'choice', index?: number, value?: string) => {
    setEditableQuestions(prev => {
      const current = { ...prev[activeQuestionId] };
      if (field === 'title' && value !== undefined) {
        current.title = value;
      } else if (field === 'choice' && index !== undefined && value !== undefined) {
        const list = [...current.choiceTexts];
        list[index] = value;
        current.choiceTexts = list;
      }
      return { ...prev, [activeQuestionId]: current };
    });
  };

  const currentQuestionData = baseQuestions.find(q => q.id === activeQuestionId) || baseQuestions[0];

  return (
    <>
      <div className={`min-h-screen ${currentTheme.canvasBg} flex flex-col transition-colors duration-300 print:hidden`} dir="rtl">
      {/* Interactive Top Menu - Hidden on standard print */}
      <header className="print:hidden w-full bg-[#112b4c] text-white py-4.5 px-6 shadow-md border-b border-[#18345a] z-10">
        <div className="max-w-7xl mx-auto flex flex-col lg:flex-row items-center justify-between gap-5">
          
          <div className="flex items-center gap-3">
            <Award className="w-7 h-7 text-amber-400 shrink-0" />
            <div>
              <h1 className="text-xl font-bold tracking-wide">מערכת דפי עבודה מותאמת: אי-ודאות והסתברות לגילאי חטיבה</h1>
              <p className="text-xs text-slate-300">אפשרות להתאמה אישית, הדפסה אסתטית ללא מיתוג ומסכי לימוד אינטראקטיביים</p>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-3">
            {/* Theme / Palette selection */}
            <div className="bg-[#18345a] px-3.5 py-1.5 rounded-lg flex items-center gap-2.5 border border-[#274266]">
              <Palette className="w-4 h-4 text-slate-300" />
              <span className="text-xs font-semibold ml-1">סגנון הדפסה:</span>
              <div className="flex gap-2">
                {themes.map((t) => (
                  <button
                    key={t.id}
                    onClick={() => setCurrentTheme(t)}
                    className={`px-3 py-1 text-xs rounded-md transition-all duration-200 ${
                      currentTheme.id === t.id
                        ? 'bg-white text-[#112b4c] font-semibold'
                        : 'text-slate-200 hover:bg-[#274266]'
                    }`}
                  >
                    {t.name.split(' ')[0]}
                  </button>
                ))}
              </div>
            </div>

            {/* Questions Navigator */}
            <div className="bg-[#18345a] px-3.5 py-1.5 rounded-lg flex items-center gap-2 border border-[#274266]">
              <FileText className="w-4 h-4 text-slate-300" />
              <span className="text-xs font-semibold ml-1">שאלה:</span>
              <div className="flex gap-1">
                {baseQuestions.map((q) => (
                  <button
                    key={q.id}
                    onClick={() => {
                      setActiveQuestionId(q.id);
                    }}
                    className={`w-7.5 h-7.5 flex items-center justify-center text-xs font-bold rounded-full transition-all duration-200 ${
                      activeQuestionId === q.id
                        ? 'bg-white text-[#112b4c] scale-105 shadow-sm'
                        : 'text-slate-200 hover:bg-[#274266]'
                    }`}
                  >
                    {q.number}
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={() => setIsEditing(!isEditing)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all duration-200 cursor-pointer border ${
                isEditing 
                  ? 'bg-emerald-600 hover:bg-emerald-500 text-white border-emerald-700' 
                  : 'bg-[#18345a] hover:bg-[#274266] text-white border-[#274266]'
              }`}
            >
              <Edit2 className="w-3.5 h-3.5" />
              {isEditing ? 'סגור עריכה' : 'תקן טקסט לשאלה'}
            </button>

            {/* Print Scope Selectors */}
            <div className="bg-[#18345a] px-3 py-1.5 rounded-lg flex items-center gap-2 border border-[#274266]">
              <Printer className="w-4 h-4 text-slate-300" />
              <span className="text-xs font-semibold">ייצוא להדפסה:</span>
              <div className="flex gap-1.5">
                <button
                  onClick={() => setPrintAllBooklet(false)}
                  className={`px-2.5 py-1 text-xs rounded-md transition-all duration-200 ${
                    !printAllBooklet
                      ? 'bg-sky-600 text-white font-semibold'
                      : 'text-slate-300 hover:bg-[#274266]'
                  }`}
                  title="הדפסת השאלה שנבחרה בלבד"
                >
                  שאלה נוכחית
                </button>
                <button
                  onClick={() => setPrintAllBooklet(true)}
                  className={`px-2.5 py-1 text-xs rounded-md transition-all duration-200 ${
                    printAllBooklet
                      ? 'bg-sky-600 text-white font-semibold'
                      : 'text-slate-300 hover:bg-[#274266]'
                  }`}
                  title="הדפסה של כל 8 דפי השאלות ברציפות"
                >
                  חוברת עבודה (8 שאלות)
                </button>
              </div>
            </div>

            <button
              onClick={copyQuestionAsImage}
              disabled={copyState === 'copying'}
              className={`px-3.5 py-1.8 rounded-lg text-xs font-bold flex items-center gap-2 shadow-sm transition-all duration-200 cursor-pointer ${
                copyState === 'success'
                  ? 'bg-amber-500 text-white border border-amber-600'
                  : copyState === 'error'
                  ? 'bg-rose-600 text-white border border-rose-700'
                  : 'bg-indigo-600 hover:bg-indigo-505 text-white border border-indigo-700'
              }`}
            >
              {copyState === 'copying' ? (
                <>
                  <span className="animate-spin inline-block w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full" />
                  מצלם ומעתיק...
                </>
              ) : copyState === 'success' ? (
                <>
                  <Check className="w-4 h-4 text-white" />
                  הועתק ללוח / הורד!
                </>
              ) : copyState === 'error' ? (
                <>
                  <AlertCircle className="w-4 h-4" />
                  שגיאה בצילום
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  העתק שאלה כתמונה
                </>
              )}
            </button>

            <button
              onClick={handlePrint}
              className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-1.8 rounded-lg text-xs font-bold flex items-center gap-2 shadow-sm transition-all duration-200 cursor-pointer"
            >
              <Printer className="w-4 h-4" />
              שגר להדפסה
            </button>
          </div>

        </div>
      </header>

      {/* Workspace Area: Left customization control + Center A4 Sheet */}
      <div className="flex-1 max-w-7xl w-full mx-auto grid grid-cols-1 lg:grid-cols-12 gap-6 p-6">
        
        {/* Left Side: Educational control panel / instructions (Hidden on printing) */}
        <div className="print:hidden lg:col-span-4 flex flex-col gap-6">
          
          {/* General Workspace Info */}
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <h3 className="text-sm font-bold text-[#112b4c] mb-3 flex items-center gap-2">
              <FileText className="w-4 h-4 text-sky-600 animate-pulse" />
              דפי עבודה: אי-ודאות והסתברות
            </h3>
            <p className="text-xs text-slate-500 leading-relaxed mb-3">
              מערכת זו מעוצבת להכנה והדפסה של דפי עבודה וחוברות תרגול במתמטיקה ברמת גימור אקדמית ונקייה.
            </p>
            <ul className="text-xs text-slate-600 space-y-2.5 list-disc list-inside">
              <li>בחר שאלות <strong className="text-[#112b4c]">1 עד 8</strong> מהתפריט העליון.</li>
              <li>בחר סגנון הדפסה מבוקש למראה אחיד, מדויק ומקצועי ביותר.</li>
              <li>תוכל לערוך ולשנות את נוסח השאלות או האפשרויות בזמן אמת על-ידי לחיצה על <strong className="text-[#112b4c]">תיקן טקסט לשאלה</strong>.</li>
              <li>סעיף **העתקת תמונה**: יש כפתור <strong className="text-[#112b4c]">העתק שאלה כתמונה</strong> לכל שאלה, המאפשר להעתיק את השאלה כולה ולהדביק ברמה גבוהה מאוד ישירות בתוכנות חיצוניות דוגמת **קנבה (Canva)** או **וורד (Word)**.</li>
              <li>כל שאלה מיוצאת ומודפסת **בעמוד חדש ונפרד** בצורה עצמאית ומקצועית ללא כל גלישה.</li>
            </ul>
          </div>

          {/* Quick Dynamic Editor */}
          {isEditing && (
            <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col gap-4 animate-fade-in">
              <h3 className="text-sm font-bold text-[#112b4c] mb-1">עריכת תוכן השאלה בזמן אמת</h3>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">נוסח השאלה:</label>
                <textarea
                  value={editableQuestions[activeQuestionId].title}
                  onChange={(e) => handleEditChange('title', undefined, e.target.value)}
                  className="w-full text-xs p-2.5 border border-slate-200 rounded-lg focus:outline-none focus:border-[#112b4c] min-h-[80px] leading-relaxed"
                />
              </div>
              <div className="flex flex-col gap-2">
                <label className="block text-xs font-semibold text-slate-700">תשובות מוצעות (א-ד):</label>
                {editableQuestions[activeQuestionId].choiceTexts.map((text, idx) => (
                  <div key={idx} className="flex items-center gap-2">
                    <span className="text-xs font-bold text-[#112b4c]">
                      {idx === 0 ? '(א)' : idx === 1 ? '(ב)' : idx === 2 ? '(ג)' : '(ד)'}
                    </span>
                    <input
                      type="text"
                      value={text}
                      onChange={(e) => handleEditChange('choice', idx, e.target.value)}
                      className="flex-1 text-xs p-2 border border-slate-200 rounded-lg focus:outline-none focus:border-[#112b4c]"
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>

        {/* Center/Right Side: Beautiful A4 PDF Preview */}
        <div className="lg:col-span-8 flex justify-center">
          <div
            id="worksheet-preview-container"
            className="w-[210mm] min-h-[297mm] p-[18mm_20mm_15mm] border border-slate-300 rounded-xl shadow-xl flex flex-col justify-between transition-all duration-300 relative print:m-0 print:border-0 print:shadow-none print:w-full print:h-full"
            style={{ fontFamily: currentTheme.fontFamily, backgroundColor: currentTheme.cardBgHex }}
          >
            {/* Header section */}
            <div 
              className="top-header pb-2 mb-[12mm] flex justify-between items-end"
              style={{ borderBottom: `1px solid ${currentTheme.primary}` }}
            >
              <span className="text-xs text-slate-400 font-light select-none"></span>
              <span 
                className="top-title text-[12pt] font-normal tracking-wide"
                style={{ color: currentTheme.primary }}
              >
                שאלה {currentQuestionData.number}
              </span>
            </div>

            {/* Content & Main Question Area */}
            <div className="flex-grow flex flex-col justify-start">
              <section className="mb-8">
                <h2 
                  className="text-[17pt] leading-relaxed font-normal text-right transition-colors duration-300 whitespace-pre-wrap"
                  style={{ color: currentTheme.text }}
                >
                  {editableQuestions[activeQuestionId].title}
                </h2>
              </section>

              {/* Graphic element reconstructed with exact mathematical vector ratios */}
              <section className="graphic-area my-8 flex justify-center shrink-0">
                <div className="p-3 border border-slate-100 rounded-xl bg-white/40 backdrop-blur-xs">
                  {currentQuestionData.renderVisual(currentTheme.primary)}
                </div>
              </section>

              {/* Choices option boxes */}
              <section className={`grid ${activeQuestionId === 6 || activeQuestionId === 7 ? 'grid-cols-1 gap-3.5' : 'grid-cols-2 gap-5'} mt-8`}>
                {currentQuestionData.choices.map((choice, i) => {
                  return (
                    <div
                      key={i}
                      className="border rounded-lg p-4 flex items-center gap-3 bg-white transition-all duration-200 select-none shadow-xs"
                      style={{ 
                        borderColor: currentTheme.accent,
                        backgroundColor: '#ffffff'
                      }}
                    >
                      <span 
                        className="text-[12pt] font-semibold select-none"
                        style={{ color: currentTheme.primary }}
                      >
                        ({choice.letter})
                      </span>
                      <span 
                        className="text-[14px] font-normal ml-auto text-right text-slate-800"
                      >
                        {renderMathOptionText(editableQuestions[activeQuestionId].choiceTexts[i])}
                      </span>
                    </div>
                  );
                })}
              </section>

              {/* Print lines mock for pencil response */}
              <section className="solution-lines mt-12 grow flex flex-col justify-end mb-8">
                <div className="line h-[11mm]" style={{ borderBottom: `1px solid ${currentTheme.divider}` }}></div>
                <div className="line h-[11mm]" style={{ borderBottom: `1px solid ${currentTheme.divider}` }}></div>
                <div className="line h-[11mm]" style={{ borderBottom: `1px solid ${currentTheme.divider}` }}></div>
              </section>
            </div>

            {/* Footer with exact requirements */}
            <footer className="footer mt-[14mm] text-center shrink-0">
              <div className="w-full h-px mb-[3mm]" style={{ backgroundColor: currentTheme.primary }}></div>
              <div 
                className="footer-text text-[10pt] font-normal tracking-wide" 
                style={{ color: currentTheme.primary, letterSpacing: '0.12em' }}
              >
                תחום וודאות
              </div>
            </footer>
          </div>
        </div>

      </div>
    </div>

    {/* Elegant Print-Only booklet and single-page generator */}
    <div className="hidden print:block bg-white scroll-smooth" dir="rtl" style={{ fontFamily: currentTheme.fontFamily }}>
      <style dangerouslySetInnerHTML={{ __html: `
        @media print {
          @page {
            size: A4 portrait;
            margin: 0;
          }
          body {
            margin: 0;
            padding: 0;
            background: #ffffff !important;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
          }
          .break-page {
            page-break-after: always;
            break-after: page;
          }
        }
      `}} />
      
      {(printAllBooklet ? baseQuestions : [currentQuestionData]).map((q) => {
        const editable = editableQuestions[q.id];
        return (
          <div 
            key={q.id}
            className="w-[210mm] h-[297mm] max-h-[297mm] p-[18mm_20mm_15mm] flex flex-col justify-between bg-white text-black break-page relative mx-auto"
            style={{ boxSizing: 'border-box' }}
          >
            {/* Header section */}
            <div 
              className="pb-2 mb-[12mm] flex justify-between items-end border-b"
              style={{ borderColor: currentTheme.primary }}
            >
              <span className="text-xs text-slate-400 font-light select-none">דף עבודה מתמטיקה: אי-ודאות והסתברות</span>
              <span 
                className="text-[12pt] font-semibold"
                style={{ color: currentTheme.primary }}
              >
                שאלה {q.number}
              </span>
            </div>

            {/* Content & Main Question Area */}
            <div className="flex-grow flex flex-col justify-start">
              <section className="mb-6">
                <h2 
                  className="text-[16pt] leading-relaxed font-normal text-right whitespace-pre-wrap text-[#0f172a]"
                >
                  {editable.title}
                </h2>
              </section>

              {/* Graphic element */}
              <section className="graphic-area my-6 flex justify-center shrink-0">
                <div className="p-2 border border-slate-100 rounded-xl bg-white">
                  {q.renderVisual(currentTheme.primary)}
                </div>
              </section>

              {/* Choices option boxes */}
              <section className={`grid ${q.id === 6 || q.id === 7 ? 'grid-cols-1 gap-3' : 'grid-cols-2 gap-4'} mt-4`}>
                {q.choices.map((choice, i) => {
                  return (
                    <div
                      key={i}
                      className="border border-slate-200 rounded-lg p-3.5 flex items-center gap-3 bg-white"
                    >
                      <span 
                        className="text-[11pt] font-bold"
                        style={{ color: currentTheme.primary }}
                      >
                        ({choice.letter})
                      </span>
                      <span 
                        className="text-[13pt] font-normal ml-auto text-right text-slate-800"
                      >
                        {renderMathOptionText(editable.choiceTexts[i])}
                      </span>
                    </div>
                  );
                })}
              </section>

              {/* Student Response Mock Pencil Lines */}
              <section className="solution-lines mt-10 grow flex flex-col justify-end mb-6">
                <div className="text-xs text-[#64748b] text-right mb-1 select-none">נמקו והסבירו את דרך החישוב:</div>
                <div className="line h-[10mm] border-b border-dashed border-slate-200"></div>
                <div className="line h-[10mm] border-b border-dashed border-slate-200"></div>
                <div className="line h-[10mm] border-b border-dashed border-slate-200"></div>
              </section>
            </div>

            {/* Footer with exact requirements */}
            <footer className="footer mt-[12mm] text-center shrink-0">
              <div className="w-full h-px mb-[3mm]" style={{ backgroundColor: currentTheme.primary }}></div>
              <div 
                className="text-[9pt] font-normal tracking-wider text-slate-500" 
                style={{ letterSpacing: '0.12em' }}
              >
                תחום וודאות
              </div>
            </footer>
          </div>
        );
      })}
    </div>
  </>
  );
}
