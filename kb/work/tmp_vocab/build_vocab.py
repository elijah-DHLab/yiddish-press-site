import json, re, sys

OUT = sys.argv[1]

# (id, he, en, broader, scope, related)
C = []
def c(id, he, en, broader, scope, related=()):
    C.append({"id": id, "he": he, "en": en, "broader": broader, "scope": scope, "related": list(related)})

# ---------------- 1. Persecution ----------------
c("top:jewish-persecution", "רדיפות יהודים, פוגרומים והגבלות", "Persecution of Jews, pogroms and restrictions", None,
  "רדיפת יהודים, אלימות נגדם, עלילות, גזירות והגבלות חוקיות, ואנטישמיות פוליטית בכל הארצות.", ["pl:russian-empire", "pl:romania"])
c("top:pogroms", "פוגרומים ופרעות ביהודים", "Pogroms and anti-Jewish violence", "top:jewish-persecution",
  "פוגרומים, פרעות, חשש מפוגרום, משפטי פורעים, פיצויים וסיוע לנפגעים – בעיקר באימפריה הרוסית ובאירופה (פגיעות ביהודי מרוקו – תחת יהודי מרוקו).",
  ["pl:russian-empire", "top:moroccan-jews", "top:jewish-philanthropy-relief"])
c("top:blood-libels", "עלילות דם", "Blood libels", "top:jewish-persecution",
  "עלילות דם ופרשיותיהן: פרשת בייליס ורצח יושצינסקי, עלילת דמשק (1840), פרשת הילזנר ועלילות במזרח.", ["pl:kiev", "pl:damascus", "top:trials"])
c("top:anti-jewish-restrictions-russia", "הגבלות על יהודים ברוסיה", "Anti-Jewish restrictions in Russia", "top:jewish-persecution",
  "תחום המושב, הגבלות מגורים, מסחר, מקצועות, קניין והשתתפות בבחירות, ומדיניות הממשל הרוסי כלפי היהודים.", ["pl:russian-empire", "pl:kiev"])
c("top:numerus-clausus", "מכסות יהודים בחינוך (הנורמה האחוזית)", "Numerus clausus for Jews", "top:anti-jewish-restrictions-russia",
  "מכסות אחוזים ליהודים בגימנסיות ובאוניברסיטאות, הדרת סטודנטים ותלמידים יהודים ומאבקים בעניין.", ["pl:russian-empire", "top:students-universities"])
c("top:expulsions-of-jews", "גירושי יהודים", "Expulsions of Jews", "top:jewish-persecution",
  "גירוש יהודים מערים ומאזורים (קייב, מוסקבה, פרוסיה, רומניה, סלוניקי ועוד) וגירוש נתינים יהודים זרים.", ["pl:russian-empire", "pl:germany", "pl:romania"])
c("top:antisemitism-politics-press", "אנטישמיות פוליטית ותעמולה אנטישמית", "Political antisemitism and antisemitic propaganda", "top:jewish-persecution",
  "מפלגות ותנועות אנטישמיות, תעמולה ועיתונות אנטישמית, חרם כלכלי על יהודים ואפליה – בגרמניה, אוסטריה, הונגריה, צרפת, יוון, רוסיה ועוד.",
  ["pl:germany", "pl:austria-hungary", "pl:russian-empire", "top:press-opinion-polemics"])
c("top:jewish-rights-emancipation", "המאבק לשוויון זכויות ליהודים", "Jewish civil rights and emancipation", "top:jewish-persecution",
  "מאבקים לשוויון זכויות אזרחיות ופוליטיות ליהודים, שאלת היהודים ברומניה וברוסיה, וסכסוך הדרכונים בין רוסיה לארה\"ב.",
  ["pl:romania", "pl:russian-empire", "pl:united-states"])

# ---------------- 2. Jewish communities ----------------
c("top:jewish-communities", "קהילות יהודיות בעולם", "Jewish communities worldwide", None,
  "חיי הקהילות היהודיות, מוסדותיהן, הנהגתן ומצבן החברתי, הכלכלי והפוליטי ברחבי העולם.", [])
c("top:sephardi-mizrahi-jewry", "יהדות ספרד וארצות האסלאם", "Sephardi and Mizrahi Jewry", "top:jewish-communities",
  "קהילות ספרדיות ויהודי ארצות האסלאם בכלל (פרס, תימן, מצרים, צפון אפריקה מחוץ למרוקו), המורשת הספרדית ויחס ספרד ליהודים ספרדים.",
  ["pl:persia", "pl:egypt", "pl:spain", "top:moroccan-jews", "top:salonica-jewry"])
c("top:moroccan-jews", "יהודי מרוקו", "Moroccan Jews", "top:jewish-communities",
  "מצבם של יהודי מרוקו: חיי המלאח, פרעות ופגיעות ביהודים (קזבלנקה 1907, פאס 1912 ועוד), בתי ספר של אליאנס, מנהגים, זכויות, הגירה וסיוע.",
  ["pl:morocco", "pl:fez", "pl:casablanca", "top:morocco-question", "top:pogroms", "top:alliance-israelite-schools"])
c("top:salonica-jewry", "יהודי סלוניקי", "Jews of Salonica", "top:jewish-communities",
  "קהילת סלוניקי: מוסדותיה, כלכלתה, עיתונותה ורבניה, יחסה לטורקים הצעירים, וגורלה תחת השלטון היווני אחרי מלחמות הבלקן.",
  ["pl:thessaloniki", "top:balkan-wars", "top:young-turk-revolution"])
c("top:ottoman-jewry", "יהודי האימפריה העות'מאנית", "Ottoman Jewry", "top:jewish-communities",
  "יהודי האימפריה העות'מאנית וקושטא: מעמדם, יחסם לשלטון ולמהפכת הטורקים הצעירים, צירים ופקידים יהודים וגיוס יהודים לצבא העות'מאני.",
  ["pl:ottoman-empire", "pl:istanbul", "top:ottoman-politics"])
c("top:syrian-jewry", "יהודי סוריה ודמשק", "Jews of Syria and Damascus", "top:jewish-communities",
  "קהילות דמשק, ביירות ושאר סוריה העות'מאנית: מצבן, התבוללותן ויחסיהן עם השכנים (עלילת דמשק – תחת עלילות דם).",
  ["pl:damascus", "pl:syria", "top:blood-libels"])
c("top:chief-rabbinate", "החכם באשי והרבנות הראשית", "Hakham Bashi and chief rabbinates", "top:jewish-communities",
  "מינוי חכמים באשי ורבנים ראשיים (ירושלים, סלוניקי, קושטא, צרפת), בחירות רבנים ומחלוקות על הרבנות.",
  ["pl:istanbul", "pl:thessaloniki", "pl:ottoman-palestine"])
c("top:russian-polish-jewry", "חיי הקהילה ביהדות רוסיה ופולין", "Jewish community life in Russia and Poland", "top:jewish-communities",
  "חיי הקהילה היהודית באודסה, ורשה ושאר רוסיה ופולין: מוסדות, מסים, בחירות קהילתיות, עוני ופרנסה וחיי היומיום.",
  ["pl:russian-empire", "pl:warsaw"])
c("top:western-jewry", "יהדות מערב ומרכז אירופה", "Jews of Western and Central Europe", "top:jewish-communities",
  "קהילות גרמניה, אוסטריה-הונגריה וגליציה, אנגליה, צרפת, איטליה, הולנד ופורטוגל – מצבן, מוסדותיהן וחייהן.",
  ["pl:germany", "pl:austria-hungary", "pl:united-kingdom", "pl:france", "pl:italy"])
c("top:jewish-politics-advocacy", "פוליטיקה ולאומיות יהודית ושתדלנות", "Jewish politics, nationalism and advocacy", "top:jewish-communities",
  "ארגון פוליטי יהודי, לאומיות יהודית בגולה, שתדלנות ודיפלומטיה יהודית, סולידריות יהודית בינלאומית ויהודים בתפקידים ציבוריים.",
  ["top:zionist-movement", "top:jewish-rights-emancipation"])
c("top:jewish-philanthropy-relief", "צדקה, סעד ופילנתרופיה יהודית", "Jewish philanthropy and relief", "top:jewish-communities",
  "מוסדות צדקה וסעד, ארגוני עזרה בינלאומיים (הילפספראיין, אליאנס, בני ברית), איסוף תרומות וסיוע לנפגעי פוגרומים, שריפות ומלחמה.",
  ["top:pogroms", "top:wwi-jews"])
c("top:jewish-economic-life", "כלכלה ופרנסה של יהודים", "Jewish economic life", "top:jewish-communities",
  "סוחרים, בעלי מלאכה ובנקאים יהודים, מצבם הכלכלי והמקצועי של היהודים, עוני, תחרות כלכלית ויחסי הון ועבודה בקרב יהודים.",
  ["top:trade-tariffs", "top:antisemitism-politics-press"])
c("top:jews-in-military", "יהודים בצבא ובשירות הצבאי", "Jews in military service", "top:jewish-communities",
  "גיוס יהודים לצבאות רוסיה, טורקיה ואחרים, גבורת חיילים יהודים, ומוסדות לחיילים יהודים (מלחמת העולם – תחת היהודים במלחמה).",
  ["top:militarism-conscription", "top:ottoman-military", "top:wwi-jews"])

# ---------------- 3. Zionism ----------------
c("top:zionism-eretz-israel", "ציונות וארץ ישראל", "Zionism and the Land of Israel", None,
  "התנועה הציונית ויריבותיה, היישוב היהודי בארץ ישראל וענייני ארץ ישראל תחת השלטון העות'מאני.", ["pl:ottoman-palestine"])
c("top:zionist-movement", "התנועה הציונית ומוסדותיה", "Zionist movement", "top:zionism-eretz-israel",
  "קונגרסים ואסיפות ציוניות, הקרן הקיימת וגיוס כספים, הנהגה ופולמוסים, ציונות מול התבוללות, וציונות בטורקיה ובארצות שונות.",
  ["top:jewish-politics-advocacy"])
c("top:territorialism", "טריטוריאליזם", "Jewish territorialism", "top:zionism-eretz-israel",
  "התנועה הטריטוריאליסטית ותוכניות למקלט יהודי מחוץ לארץ ישראל (אנגולה, מושבה בפורטוגל ועוד).",
  ["top:jewish-agricultural-colonization"])
c("top:yishuv-settlement", "היישוב וההתיישבות בארץ ישראל", "Jewish settlement in the Land of Israel", "top:zionism-eretz-israel",
  "המושבות, רכישת קרקעות, עבודה ושמירה עברית, פועלים ומתיישבים (כולל יהודי תימן), היישוב הישן והחלוקה, וחינוך ומוסדות בארץ.",
  ["pl:ottoman-palestine"])
c("top:ottoman-palestine", "ארץ ישראל תחת השלטון העות'מאני", "Ottoman Palestine", "top:zionism-eretz-israel",
  "ענייני ארץ ישראל וירושלים: מדיניות השלטון העות'מאני כלפי העלייה והציונים, כלכלה, מסחר ותשתיות, מקומות קדושים ונסיעות לארץ.",
  ["pl:ottoman-palestine", "top:ottoman-politics"])
c("top:jewish-arab-relations", "יחסי יהודים וערבים", "Jewish–Arab relations", "top:zionism-eretz-israel",
  "יחסי יהודים וערבים בארץ ישראל ובמזרח, יחס העיתונות הערבית ליהודים ולציונות.", ["pl:ottoman-palestine", "top:arab-egyptian-nationalism"])

# ---------------- 4. Migration ----------------
c("top:migration", "הגירה ופליטים", "Migration and refugees", None,
  "הגירת יהודים ואחרים, מדיניות הגירה, התיישבות מחוץ לארץ ישראל ופליטים.", ["pl:united-states"])
c("top:jewish-emigration-americas", "הגירה יהודית לאמריקה ויהדות העולם החדש", "Jewish emigration to the Americas", "top:migration",
  "הגירה יהודית לארצות הברית, קנדה ודרום אמריקה (כולל תוכנית גלווסטון), מצוקת מהגרים בדרך, וחיי היהודים באמריקה.",
  ["pl:united-states"])
c("top:jewish-agricultural-colonization", "התיישבות יהודית מחוץ לארץ ישראל", "Jewish agricultural colonization outside Palestine", "top:migration",
  "התיישבות חקלאית יהודית בארגנטינה, באפריקה ובמקומות אחרים, ופעילות יק\"א.", ["top:territorialism"])
c("top:immigration-restrictions", "מדיניות הגירה והגבלות הגירה", "Immigration policy and restrictions", "top:migration",
  "חוקי הגירה והגבלות כניסה (חוק הזרים באנגליה, הגבלות באמריקה ובארץ ישראל), הגירת יפנים ועמים אחרים.",
  ["pl:united-kingdom", "pl:united-states"])
c("top:refugees", "פליטים", "Refugees", "top:migration",
  "פליטי מלחמה ופרעות: פליטים יהודים מטורקיה, מסלוניקי, מקזבלנקה ומרוסיה, ופליטים מוסלמים ויוונים מהבלקן.",
  ["top:balkan-wars", "top:wwi-home-front"])

# ---------------- 5. Jewish religion & culture ----------------
c("top:jewish-religion-culture", "דת, תרבות וחינוך יהודיים", "Jewish religion, culture and education", None,
  "החיים הדתיים, החינוך, השפות, ההיסטוריה והזהות התרבותית של היהודים.", [])
c("top:jewish-education", "חינוך יהודי", "Jewish education", "top:jewish-religion-culture",
  "חדרים ומלמדים, בתי ספר וגימנסיות עבריים, טכניון, גני ילדים, ספריות וחברות השכלה, ושאלת שפת ההוראה.",
  ["top:jewish-languages"])
c("top:alliance-israelite-schools", "אליאנס (כל ישראל חברים) ובתי הספר שלה", "Alliance Israélite Universelle and its schools", "top:jewish-education",
  "פעילות כל ישראל חברים: רשת בתי הספר במרוקו, בסלוניקי ובמזרח, הסיוע שהגישה, מצבה הכספי ודוחותיה.",
  ["top:moroccan-jews", "top:salonica-jewry", "pl:morocco"])
c("top:jewish-religious-life", "חיים דתיים, הלכה ומנהגים", "Jewish religious life and customs", "top:jewish-religion-culture",
  "שבת וחגים, כשרות ושחיטה, סחר האתרוגים, עלייה לרגל לקברי צדיקים, מחלוקות רבניות ושאלות הלכה, ומנהגי עדות.",
  ["top:chief-rabbinate"])
c("top:jewish-languages", "שפות יהודיות: עברית, יידיש ולדינו", "Jewish languages", "top:jewish-religion-culture",
  "תחיית העברית והפצתה, מעמד היידיש (כולל במפקדים ובמשפט), הלדינו, ומלחמת השפות.", ["top:jewish-press"])
c("top:jewish-history-memory", "היסטוריה וזיכרון יהודיים", "Jewish history and memory", "top:jewish-religion-culture",
  "תקופת בית שני והחשמונאים, גירוש ספרד והאינקוויזיציה, אנוסים, דמויות עבר (מונטיפיורי) ומרטירולוגיה יהודית.", [])
c("top:assimilation-conversion", "התבוללות והמרת דת", "Assimilation and conversion", "top:jewish-religion-culture",
  "התבוללות יהודים בסביבה האירופית והערבית, המרות דת (כולל של ילדים), נישואי תערובת וניתוק מהדת.", [])

# ---------------- 6. Morocco ----------------
c("top:morocco-question", "שאלת מרוקו והמשברים המרוקאיים", "Moroccan question", None,
  "המאבק הבינלאומי על מרוקו 1905–1912 והשתלטות צרפת וספרד עליה, על היבטיו הצבאיים, המדיניים, הכלכליים והפנימיים.",
  ["pl:morocco", "pl:france", "pl:germany", "pl:spain"])
c("top:french-intervention-morocco", "ההתערבות הצבאית הצרפתית במרוקו", "French military intervention in Morocco", "top:morocco-question",
  "פעולות צבאיות צרפתיות וכיבוש מרוקו: כיבוש אוג'דה, הפגזת קזבלנקה ומסע השאוויה, קרבות בגבול אלג'יריה, מסע פאס 1911 והקרבות שאחריו.",
  ["pl:france", "pl:morocco", "pl:casablanca", "pl:fez", "pl:algeria", "top:french-colonial-empire"])
c("top:french-protectorate-morocco", "הפרוטקטורט הצרפתי במרוקו", "French protectorate in Morocco", "top:morocco-question",
  "הסכם פאס והשלטון הצרפתי במרוקו מ-1912: ארגון הפרוטקטורט, ליוטה, המהומות בפאס והמרד נגד הצרפתים, ורפורמות צרפתיות.",
  ["pl:france", "pl:morocco", "pl:fez", "top:french-colonial-empire"])
c("top:franco-german-rivalry-morocco", "היריבות הצרפתית-גרמנית על מרוקו", "Franco-German rivalry over Morocco", "top:morocco-question",
  "המשבר המרוקאי הראשון והשני, ביקור הקייזר בטנג'יר, משבר אגאדיר, סכנת המלחמה והמשא ומתן וההסכמים הצרפתיים-גרמניים בעניין מרוקו וקונגו.",
  ["pl:france", "pl:germany", "pl:agadir", "pl:tangier", "top:franco-german-relations"])
c("top:spanish-intervention-morocco", "ההתערבות הספרדית והיריבות הצרפתית-ספרדית במרוקו", "Spanish intervention and Franco-Spanish rivalry in Morocco", "top:morocco-question",
  "מלחמת מלייה והרי הריף, הכיבוש הספרדי בלאראש ובאלקסאר, הסכסוך וההסכמים בין צרפת לספרד על מרוקו, וההתנגדות בספרד למלחמה.",
  ["pl:spain", "pl:france", "pl:morocco", "top:iberian-politics"])
c("top:morocco-international-diplomacy", "ועידות, הסכמים ורפורמות בינלאומיות במרוקו", "International conferences and reforms in Morocco", "top:morocco-question",
  "ועידת אלחסיראס והסכמיה, רפורמת המשטרה, הבנק הממלכתי ועקרון הדלת הפתוחה, ומעורבות בריטניה, רוסיה, איטליה וארה\"ב בשאלת מרוקו.",
  ["pl:spain", "pl:united-kingdom", "pl:russian-empire", "top:alliances-ententes"])
c("top:moroccan-internal-politics", "השלטון במרוקו ומאבקי הסולטנות", "Moroccan government and succession struggles", "top:morocco-question",
  "הסולטאנים עבד אל-עזיז, עבד אל-חפיט ויוסף, החפיטיה ומאבקי הירושה, החצר והמִחזן, התפטרות הסולטאן והשלטון המרוקאי.",
  ["pl:morocco", "pl:fez", "pl:marrakesh"])
c("top:moroccan-tribal-revolts", "מרידות שבטים וג'יהאד במרוקו", "Tribal revolts and jihad in Morocco", "top:morocco-question",
  "מרידות שבטים נגד הסולטאן ונגד האירופים, מצור המורדים על פאס, רייסולי, קריאות לג'יהאד, מרד חיילים ואי-שקט ואנרכיה במרוקו.",
  ["pl:morocco", "pl:fez", "top:pan-islamism"])
c("top:european-economic-interests-morocco", "אינטרסים כלכליים אירופיים במרוקו", "European economic interests in Morocco", "top:morocco-question",
  "הלוואות וחובות מרוקו לבנקאים אירופיים, סחר חוץ, זיכיונות, סחר נשק, נמלים והתחרות הכלכלית בין המעצמות במרוקו.",
  ["pl:france", "pl:germany", "top:finance-banking"])

# ---------------- 7. Ottoman ----------------
c("top:ottoman-empire", "האימפריה העות'מאנית והטורקים הצעירים", "Ottoman Empire and the Young Turks", None,
  "הפוליטיקה הפנימית, החברה, הצבא והפרובינציות של האימפריה העות'מאנית ויחסיה עם המעצמות.", ["pl:ottoman-empire", "pl:istanbul"])
c("top:young-turk-revolution", "מהפכת הטורקים הצעירים והמשטר החוקתי", "Young Turk Revolution and constitutional regime", "top:ottoman-empire",
  "מהפכת 1908 והשבת החוקה, ועד 'איחוד וקידמה', ההפיכה הנגדית של 1909, צבא הפעולה והדחת עבדול חמיד, ורפורמות הטורקים הצעירים.",
  ["pl:thessaloniki", "pl:istanbul", "top:salonica-jewry"])
c("top:ottoman-politics", "הפוליטיקה העות'מאנית: פרלמנט, ממשלה וסולטנות", "Ottoman politics: parliament, government and sultanate", "top:ottoman-empire",
  "הפרלמנט והבחירות לו, משברי ממשלה, מפלגות ואופוזיציה, הסולטאנים עבדול חמיד ומחמד החמישי, הפיכת 1913 וחקיקה עות'מאנית.",
  ["pl:istanbul"])
c("top:ottoman-military", "הצבא העות'מאני והגיוס", "Ottoman military and conscription", "top:ottoman-empire",
  "ארגון הצבא והצי העות'מאני, גיוס (כולל של לא-מוסלמים), משמעת ותבוסות, ההשפעה הצבאית הגרמנית ותפקיד הצבא בפוליטיקה.",
  ["top:jews-in-military"])
c("top:albanian-question", "המרידות האלבניות והשאלה האלבנית", "Albanian revolts and the Albanian question", "top:ottoman-empire",
  "מרידות האלבנים בשלטון העות'מאני (1910–1912), דיכוין ותוצאותיהן, עצמאות אלבניה, וחוסר היציבות באלבניה אחריה.",
  ["pl:albania", "pl:montenegro", "top:balkan-wars"])
c("top:arab-provinces-revolts", "מרידות ואי-שקט בפרובינציות הערביות", "Revolts in the Arab provinces", "top:ottoman-empire",
  "המרד בתימן ובעסיר, מרד הדרוזים בחוראן, אי-שקט בסוריה, בעיראק ובחצי האי ערב, ויחס השלטון העות'מאני לערבים.",
  ["pl:syria", "pl:damascus", "top:arab-egyptian-nationalism"])
c("top:armenian-question", "השאלה הארמנית ואלימות נגד נוצרים", "Armenian question and anti-Christian violence", "top:ottoman-empire",
  "טבח אדנה, מתיחות ואלימות בין מוסלמים, כורדים וארמנים, ואלימות נגד נוצרים ויוונים באסיה הקטנה.", [])
c("top:ottoman-nationalities", "יחסי לאומים ודתות באימפריה העות'מאנית", "Nationalities and religions in the Ottoman Empire", "top:ottoman-empire",
  "רעיון העות'מאניות ואחוות העמים, זכויות לאומיות, יוונים ובולגרים באימפריה, ולאומיות טורקית מול דת.",
  ["top:interreligious-relations-orient"])
c("top:ottoman-foreign-relations", "יחסי החוץ של האימפריה העות'מאנית והתערבות המעצמות", "Ottoman foreign relations and great-power intervention", "top:ottoman-empire",
  "יחסי טורקיה עם המעצמות ועם שכנותיה (פרס, יוון, רוסיה, בולגריה), הקפיטולציות, השקעות זרות, סכסוכי גבול וחרמות כלכליים.",
  ["pl:persia", "pl:greece", "pl:russian-empire", "top:great-power-diplomacy"])

# ---------------- 8. Balkans ----------------
c("top:balkans-eastern-question", "הבלקן והשאלה המזרחית", "The Balkans and the Eastern question", None,
  "המאבק על השטחים האירופיים של האימפריה העות'מאנית, מדינות הבלקן, מלחמות הבלקן ושאלת המיצרים.", ["pl:balkans"])
c("top:macedonian-question", "השאלה המקדונית", "Macedonian question", "top:balkans-eastern-question",
  "מקדוניה: רפורמות, אוטונומיה, כנופיות וטרור, סכסוכים לאומיים בין בולגרים, יוונים וסרבים ואי-שקט צבאי.",
  ["pl:macedonia", "pl:thessaloniki", "pl:bulgaria", "pl:greece", "pl:serbia"])
c("top:cretan-question", "שאלת כרתים", "Cretan question", "top:balkans-eastern-question",
  "מעמד כרתים, תנועת האיחוד עם יוון, משבר שבועת הצירים והסכסוך הטורקי-יווני על האי.", ["pl:crete", "pl:greece"])
c("top:straits-question", "שאלת המיצרים והדרדנלים", "Straits question", "top:balkans-eastern-question",
  "מעמד הבוספורוס והדרדנלים, סגירתם ופתיחתם והשפעתם על הסחר והספנות, ותביעות רוסיה במיצרים.",
  ["pl:istanbul", "pl:russian-empire", "top:railways-shipping"])
c("top:austria-hungary-balkans", "מדיניות אוסטרו-הונגריה בבלקן ומשבר בוסניה", "Austro-Hungarian Balkan policy and the Bosnian crisis", "top:balkans-eastern-question",
  "סיפוח בוסניה-הרצגובינה והחרם העות'מאני על אוסטריה, המתיחות האוסטרית-סרבית, והיריבות האוסטרית-רוסית בבלקן.",
  ["pl:austria-hungary", "pl:serbia", "pl:russian-empire"])
c("top:balkan-wars", "מלחמות הבלקן", "Balkan Wars", "top:balkans-eastern-question",
  "הברית הבלקנית, מלחמת הבלקן הראשונה והשנייה, המצורים, משא ומתן השלום וחלוקת השטחים, וגורל סלוניקי ואלבניה.",
  ["pl:bulgaria", "pl:serbia", "pl:greece", "pl:montenegro", "pl:thessaloniki", "top:salonica-jewry"])
c("top:balkan-states-politics", "פוליטיקה ויחסים בין מדינות הבלקן", "Politics of the Balkan states", "top:balkans-eastern-question",
  "הפוליטיקה הפנימית של יוון, בולגריה, סרביה, רומניה ומונטנגרו, עצמאות בולגריה, רצח המלך גאורגיוס והמתיחות בין מדינות הבלקן.",
  ["pl:greece", "pl:bulgaria", "pl:serbia", "pl:romania", "pl:montenegro"])

# ---------------- 9. Italo-Turkish war ----------------
c("top:italo-turkish-war", "המלחמה האיטלקית-טורקית", "Italo-Turkish War", None,
  "מלחמת איטליה והאימפריה העות'מאנית על טריפוליטניה וקירנאיקה (1911–1912), על חזיתותיה, השלכותיה והדיפלומטיה שסביבה.",
  ["pl:italy", "pl:ottoman-empire", "pl:libya", "pl:tripolitania"])
c("top:libya-campaign", "הלחימה בטריפולי ובקירנאיקה", "Fighting in Tripolitania and Cyrenaica", "top:italo-turkish-war",
  "הנחיתה האיטלקית, הקרבות והאלימות נגד האוכלוסייה בלוב, וסיפוח טריפולי וקירנאיקה.", ["pl:libya", "pl:tripolitania"])
c("top:italo-turkish-naval-war", "המלחמה הימית בים האגאי ובדרדנלים", "Naval war in the Aegean and the Dardanelles", "top:italo-turkish-war",
  "פעולות הצי האיטלקי: הפגזת בירות ונמלים, הדרדנלים, חיוס ואיי הדודקאנס.", ["top:straits-question"])
c("top:italo-turkish-war-diplomacy", "הדיפלומטיה של המלחמה האיטלקית-טורקית", "Diplomacy of the Italo-Turkish War", "top:italo-turkish-war",
  "עמדות המעצמות, החרם הטורקי על איטליה, משא ומתן השלום והסכם אושי.", ["top:great-power-diplomacy"])

# ---------------- 10. Russia ----------------
c("top:russian-politics", "פוליטיקה רוסית ומהפכה", "Russian politics and revolution", None,
  "הפוליטיקה הפנימית של האימפריה הרוסית: מהפכה, דומה, ממשל, דיכוי ושאלת הלאומים.", ["pl:russian-empire", "pl:saint-petersburg"])
c("top:russian-revolution-1905", "מהפכת 1905", "Russian Revolution of 1905", "top:russian-politics",
  "יום ראשון העקוב מדם, השביתות וההפגנות, מרידות (פוטיומקין, מוסקבה, סבסטופול), מניפסט אוקטובר והאלימות המהפכנית של 1905–1907.",
  ["pl:saint-petersburg"])
c("top:state-duma", "הדומה הממלכתית והבחירות לה", "State Duma and elections", "top:russian-politics",
  "הבחירות לדומה, מפלגות (קדטים, ימין), דיוני הדומה, פיזורה, צירים יהודים ושאלת היהודים בדומה.", ["top:jewish-rights-emancipation"])
c("top:russian-reaction-repression", "ריאקציה ודיכוי פוליטי ברוסיה", "Reaction and political repression in Russia", "top:russian-politics",
  "הריאקציה אחרי 1905: מעצרים פוליטיים, בתי דין צבאיים, אוחרנה ופרובוקציה, רדיפת מהפכנים ואסירים פוליטיים, ושרירות הממשל המקומי.",
  ["top:death-penalty-punishment", "top:press-censorship"])
c("top:russian-government", "הממשל, המינהל והכספים ברוסיה", "Russian government, administration and finances", "top:russian-politics",
  "הצאר והחצר, ממשלות ושרים (סטוליפין, ויטה), מינויים, תקציב וכספים, מדיניות חינוך ומדיניות פנים.", ["top:finance-banking"])
c("top:russian-nationalities", "שאלת הלאומים באימפריה הרוסית", "Nationalities question in the Russian Empire", "top:russian-politics",
  "רוסיפיקציה ודיכוי פינלנד, שאלת פולין והשלטון העצמי בה, הקווקז ומיעוטים לאומיים אחרים.", ["pl:warsaw"])
c("top:russian-revolution-1917", "מהפכות 1917", "Russian Revolutions of 1917", "top:russian-politics",
  "מהפכת פברואר, הממשלה הזמנית, הבחירות לאסיפה המכוננת, מהפכת אוקטובר ותגובת בעלות הברית לשלטון הבולשביקי.", ["top:wwi"])
c("top:russian-foreign-policy", "מדיניות החוץ של רוסיה", "Russian foreign policy", "top:russian-politics",
  "מדיניות החוץ הרוסית באסיה, במזרח התיכון ובאירופה, יחסי רוסיה עם סין, טורקיה וארה\"ב ומשלחות דיפלומטיות.",
  ["top:great-power-diplomacy", "top:foreign-intervention-persia"])

# ---------------- 11. WWI ----------------
c("top:wwi", "מלחמת העולם הראשונה", "World War I", None,
  "מלחמת העולם הראשונה 1914–1918: פרוצה, החזיתות, הדיפלומטיה, העורף והשלכותיה על היהודים; סקירות מלחמה כלליות.", [])
c("top:wwi-outbreak-diplomacy", "פרוץ המלחמה, דיפלומטיה ונייטרליות", "Outbreak, diplomacy and neutrality in WWI", "top:wwi",
  "משבר יולי ופרוץ המלחמה, נייטרליות והצטרפות מדינות (טורקיה, בולגריה, רומניה, יוון, ארה\"ב), שיחות שלום ושלום נפרד.",
  ["pl:bulgaria", "pl:romania", "pl:greece", "top:great-power-diplomacy"])
c("top:wwi-eastern-front", "החזית המזרחית", "Eastern Front", "top:wwi",
  "הקרבות בין רוסיה לגרמניה ואוסטרו-הונגריה בפולין, גליציה ובוקובינה, כולל כיבוש לודז' וצ'רנוביץ.", ["pl:russian-empire", "pl:germany", "pl:austria-hungary"])
c("top:wwi-balkan-fronts", "חזיתות הבלקן, סלוניקי ורומניה", "Balkan, Salonica and Romanian fronts", "top:wwi",
  "החזית הסרבית, חזית סלוניקי (המקדונית), החזית הרומנית, והפילוג הלאומי ביוון.", ["pl:thessaloniki", "pl:serbia", "pl:romania", "pl:greece"])
c("top:wwi-ottoman-fronts", "החזיתות העות'מאניות", "Ottoman fronts of WWI", "top:wwi",
  "החזית הקווקזית, מערכת גליפולי והדרדנלים, ההתקפה על תעלת סואץ ומצרים, וארץ ישראל וסוריה במלחמה.",
  ["pl:ottoman-empire", "pl:egypt", "pl:ottoman-palestine"])
c("top:wwi-western-italian-fronts", "החזית המערבית והחזית האיטלקית", "Western and Italian fronts", "top:wwi",
  "הקרבות בצרפת ובבלגיה ובחזית האיטלקית-אוסטרית.", ["pl:france", "pl:italy"])
c("top:wwi-naval-air-war", "המלחמה בים ובאוויר", "Naval and air war in WWI", "top:wwi",
  "מלחמת הצוללות, ההסגר הימי, המוקשים, קרבות ימיים והתקפות אוויריות.", ["pl:united-kingdom", "pl:germany"])
c("top:wwi-home-front", "העורף, השבויים והסיוע במלחמה", "Home front, prisoners and war relief", "top:wwi",
  "החיים בעורף (כולל אודסה), כלכלה ומחסור, גיוס, פצועים ושבויי מלחמה, וסיוע לחיילים ולמשפחותיהם.", ["top:refugees"])
c("top:wwi-jews", "היהודים במלחמת העולם הראשונה", "Jews in World War I", "top:wwi",
  "השפעת המלחמה על היהודים: פליטים ומגורשים, חיילים יהודים והגדוד העברי, רדיפת היישוב בארץ ישראל, ויחס המדינות הלוחמות ליהודים.",
  ["top:jewish-philanthropy-relief", "top:yishuv-settlement"])

# ---------------- 12. Diplomacy ----------------
c("top:great-power-diplomacy", "דיפלומטיה של המעצמות ובריתות", "Great-power diplomacy and alliances", None,
  "היחסים בין המעצמות האירופיות, בריתות, יריבויות, משברים בינלאומיים ומאמצי שלום (לפני 1914).", [])
c("top:alliances-ententes", "בריתות והסכמים בין המעצמות", "Alliances and ententes", "top:great-power-diplomacy",
  "הברית המשולשת וההסכמה המשולשת, ההסכמה הלבבית, הברית הצרפתית-רוסית, ההסכם האנגלו-רוסי, הברית האנגלו-יפנית ומאזן הכוחות.",
  ["pl:france", "pl:united-kingdom", "pl:russian-empire", "pl:germany"])
c("top:franco-german-relations", "יחסי צרפת וגרמניה", "Franco-German relations", "top:great-power-diplomacy",
  "היחסים והמתיחות בין צרפת לגרמניה מעבר לשאלת מרוקו: אלזס-לורין, זיכרון מלחמת 1870, פטריוטיזם וסכנת מלחמה ביניהן.",
  ["pl:france", "pl:germany", "top:franco-german-rivalry-morocco"])
c("top:anglo-german-rivalry", "היריבות האנגלו-גרמנית ומירוץ החימוש הימי", "Anglo-German rivalry and naval race", "top:great-power-diplomacy",
  "היחסים בין בריטניה לגרמניה, מירוץ החימוש הימי, כוח ימי מול כוח יבשתי.", ["pl:united-kingdom", "pl:germany"])
c("top:war-scares", "סכנת מלחמה ומשברים בינלאומיים", "War scares and international crises", "top:great-power-diplomacy",
  "חשש ממלחמה אירופית כללית, שמועות מלחמה, פאניקה בבורסות ומתיחות בינלאומית כללית.", ["top:finance-banking"])
c("top:royal-visits-summits", "ביקורי מלכים ופגישות פסגה", "Royal visits and summits", "top:great-power-diplomacy",
  "ביקורי מלכים, קיסרים ונשיאים זה אצל זה, פגישות פסגה ומשמעותן המדינית.", [])
c("top:peace-movement-arbitration", "תנועת השלום, ועידות האג ובוררות", "Peace movement and arbitration", "top:great-power-diplomacy",
  "ועידות השלום בהאג, הגבלת חימוש, הסכמי בוררות, תנועת השלום ופרס נובל לשלום.", ["top:socialism"])

# ---------------- 13. Persia & Asia ----------------
c("top:persia-asia", "פרס, אסיה והמזרח הרחוק", "Persia, Asia and the Far East", None,
  "אירועים ומדיניות בפרס, בסין, ביפן ובקוריאה, כולל המלחמה הרוסית-יפנית.", ["pl:persia", "pl:china", "pl:japan"])
c("top:russo-japanese-war", "המלחמה הרוסית-יפנית", "Russo-Japanese War", "top:persia-asia",
  "המלחמה בין רוסיה ליפן 1904–1905: הקרבות, תנועות הצי הרוסי, מימון המלחמה, שיחות השלום בפורטסמות והשלכותיה.",
  ["pl:russian-empire", "pl:japan"])
c("top:persian-revolution", "המהפכה החוקתית בפרס", "Persian Constitutional Revolution", "top:persia-asia",
  "המהפכה החוקתית, המאבק בשאה מוחמד עלי, המצור על תבריז, משברי ממשל ואי-שקט, ומצב יהודי פרס בעקבותיה.", ["pl:persia"])
c("top:foreign-intervention-persia", "התערבות המעצמות בפרס", "Great-power intervention in Persia", "top:persia-asia",
  "ההתערבות הרוסית והבריטית בפרס, ההסכם האנגלו-רוסי ואזורי ההשפעה, ההסכם הרוסי-גרמני, הלוואות וסכסוכי הגבול הטורקי-פרסי.",
  ["pl:persia", "pl:russian-empire", "pl:united-kingdom", "top:ottoman-foreign-relations"])
c("top:china", "סין והמהפכה הסינית", "China and the Chinese Revolution", "top:persia-asia",
  "המהפכה הסינית והרפובליקה, אי-שקט בסין, התערבות המעצמות, הלוואות, והסכסוכים עם רוסיה ויפן.", ["pl:china"])
c("top:japan-korea", "יפן, קוריאה והתפשטות יפן", "Japan, Korea and Japanese expansion", "top:persia-asia",
  "כיבוש קוריאה וסיפוחה, יחסי יפן עם ארה\"ב וסין, והפוליטיקה היפנית.", ["pl:japan", "pl:united-states"])

# ---------------- 14. Domestic politics ----------------
c("top:domestic-politics", "פוליטיקה פנימית במדינות אירופה ואמריקה", "Domestic politics of European and American states", None,
  "הפוליטיקה הפנימית של המדינות (פרלמנטים, ממשלות, בחירות, חוקות, חצרות מלוכה); רוסיה, האימפריה העות'מאנית ומדינות הבלקן – תחת נושאיהן.", [])
c("top:french-domestic-politics", "פוליטיקה פנימית בצרפת", "French domestic politics", "top:domestic-politics",
  "ממשלות ומשברי ממשלה בצרפת, הפרלמנט והבחירות, רפורמת הבחירות, הצבא והפוליטיקה, שערוריות ודעת הקהל הצרפתית (כולל ויכוחי מרוקו בפרלמנט).",
  ["pl:france", "top:morocco-question"])
c("top:church-state-france", "הפרדת הדת והמדינה בצרפת", "Separation of church and state in France", "top:french-domestic-politics",
  "חוק ההפרדה של 1905, הסכסוך עם הוותיקן, הקתולים בצרפת ופנסיות לאנשי דת.", ["pl:france"])
c("top:german-domestic-politics", "פוליטיקה פנימית בגרמניה", "German domestic politics", "top:domestic-politics",
  "הקייזר והחצר, הרייכסטאג והבחירות לו, זכות הבחירה בפרוסיה, אלזס-לורין, מדיניות כלפי הפולנים והדיכוי המשטרתי.", ["pl:germany"])
c("top:british-domestic-politics", "פוליטיקה פנימית בבריטניה", "British domestic politics", "top:domestic-politics",
  "הממשלה והפרלמנט הבריטיים, הבחירות, משבר התקציב ובית הלורדים, אירלנד ורפורמת הבחירות.", ["pl:united-kingdom"])
c("top:austro-hungarian-domestic-politics", "פוליטיקה פנימית באוסטרו-הונגריה", "Austro-Hungarian domestic politics", "top:domestic-politics",
  "הפרלמנט האוסטרי והבחירות, זכות הבחירה הכללית, המשבר ההונגרי, משברי שרים ומתיחות בין הלאומים בקיסרות.", ["pl:austria-hungary"])
c("top:italian-domestic-politics", "פוליטיקה פנימית באיטליה", "Italian domestic politics", "top:domestic-politics",
  "ממשלות ומשברים באיטליה, תסיסה אנטי-קלריקלית ומהומות.", ["pl:italy"])
c("top:iberian-politics", "פוליטיקה בספרד ובפורטוגל", "Spanish and Portuguese politics", "top:domestic-politics",
  "משברי ממשלה ומהומות בספרד, רצח מלך פורטוגל, המהפכה הפורטוגלית והרפובליקה וקשרים מלוכניים נגדה.", ["pl:spain"])
c("top:smaller-european-states", "פוליטיקה במדינות אירופה הקטנות", "Politics of smaller European states", "top:domestic-politics",
  "פירוק האיחוד בין נורווגיה לשוודיה, הפוליטיקה בשוודיה, בהולנד, בבלגיה, בדנמרק ובשווייץ.", [])
c("top:americas-politics", "פוליטיקה ביבשת אמריקה", "Politics in the Americas", "top:domestic-politics",
  "הפוליטיקה בארצות הברית (בחירות, מדיניות אנטי-טראסט), המהפכה במקסיקו ואירועים באמריקה הלטינית.", ["pl:united-states"])
c("top:catholic-church-papacy", "האפיפיורות והכנסייה הקתולית", "Papacy and the Catholic Church", "top:domestic-politics",
  "האפיפיור והוותיקן, הישועים והכנסייה הקתולית ויחסיהן עם המדינות.", ["pl:italy", "top:church-state-france"])

# ---------------- 15. Colonialism ----------------
c("top:colonialism", "קולוניאליזם ואימפריאליזם", "Colonialism and imperialism", None,
  "ההתפשטות הקולוניאלית של המעצמות, התחרות ביניהן, השלטון במושבות והביקורת עליו (מרוקו – תחת שאלת מרוקו).", [])
c("top:colonial-rivalry", "התחרות הקולוניאלית בין המעצמות", "Colonial rivalry among the powers", "top:colonialism",
  "חלוקת אפריקה והעולם בין המעצמות, פיצויים קולוניאליים (קונגו), חלוקת 'ירושת' העולם המוסלמי והתפשטות על חשבון האימפריה העות'מאנית.",
  ["top:morocco-question", "top:great-power-diplomacy"])
c("top:french-colonial-empire", "האימפריה הקולוניאלית הצרפתית", "French colonial empire", "top:colonialism",
  "השלטון הצרפתי באלג'יריה, תוניסיה, הודו-סין, מדגסקר ואפריקה, המדיניות הצרפתית בצפון אפריקה ומרידות נגד צרפת מחוץ למרוקו.",
  ["pl:france", "pl:algeria", "top:french-intervention-morocco"])
c("top:british-empire", "האימפריה הבריטית: הודו, מצרים ותעלת סואץ", "British Empire: India, Egypt and Suez", "top:colonialism",
  "השלטון הבריטי בהודו ובמצרים, התסיסה נגדו, תעלת סואץ והמדיניות הבריטית בעדן ובערב.", ["pl:united-kingdom", "pl:egypt"])
c("top:other-colonial-empires", "מושבות גרמניה, בלגיה, פורטוגל ואחרות", "German, Belgian, Portuguese and other colonies", "top:colonialism",
  "המושבות הגרמניות באפריקה, קונגו הבלגית, מושבות פורטוגל ואיטליה ומושבות נוספות.", ["pl:germany"])
c("top:anti-colonial-critique", "ביקורת הקולוניאליזם והצדקותיו", "Critique and justifications of colonialism", "top:colonialism",
  "'המשימה התרבותית', ניצול ודיכוי עמים במושבות, ביקורת על הציוויליזציה האירופית והפגנות סוציאליסטיות נגד קולוניאליזם.",
  ["top:socialism"])

# ---------------- 16. Economy ----------------
c("top:economy", "כלכלה, מסחר ותחבורה", "Economy, trade and transport", None,
  "מסחר, כספים, תעשייה, תחבורה ויוקר המחיה.", [])
c("top:trade-tariffs", "מסחר, מכסים וחרמות כלכליים", "Trade, tariffs and boycotts", "top:economy",
  "סחר בינלאומי ומקומי, הסכמי סחר ומכסים, מונופולים, מחירי שוק וחרמות כלכליים בין מדינות.", [])
c("top:finance-banking", "בנקאות, הלוואות ובורסה", "Finance, banking and loans", "top:economy",
  "הלוואות ממלכתיות (למשל הלוואות צרפת לרוסיה), בנקים, בית רוטשילד, בורסות ופאניקות פיננסיות.", ["pl:france", "pl:russian-empire"])
c("top:railways-shipping", "מסילות ברזל, ספנות ותעלות", "Railways, shipping and canals", "top:economy",
  "מסילת בגדאד ומסילות בארץ ישראל ובאימפריה, ספנות בים השחור ובבלקן, תעלת פנמה ונמלים.", ["top:straits-question"])
c("top:cost-of-living", "יוקר המחיה ומשברים כלכליים", "Cost of living and economic crises", "top:economy",
  "התייקרות מזון ומחירים, הפגנות נגד יוקר המחיה, מחסור, משברים כלכליים ואבטלה.", ["top:labour-strikes"])
c("top:industry-concessions", "תעשייה, משאבים וזיכיונות", "Industry, resources and concessions", "top:economy",
  "פיתוח כלכלי ותעשייה, תעשיות שונות, משאבי טבע וזיכיונות לחברות זרות.", [])

# ---------------- 17. Disasters & health ----------------
c("top:disasters-health", "אסונות, מגפות ובריאות", "Disasters, epidemics and health", None,
  "אסונות טבע ואסונות מעשה ידי אדם, מגפות ובריאות הציבור.", [])
c("top:epidemics", "מגפות", "Epidemics", "top:disasters-health",
  "כולרה, דבר, אבעבועות ומחלות מדבקות אחרות, הסגר ובידוד בנמלים.", [])
c("top:natural-disasters", "אסונות טבע ורעב", "Natural disasters and famine", "top:disasters-health",
  "רעידות אדמה, שיטפונות, סערות, גלי חום ורעב.", [])
c("top:fires", "שריפות", "Fires", "top:disasters-health",
  "שריפות בערים, ברובעים יהודיים, בבתי כנסת ובבתי קולנוע, וסיוע לנפגעיהן.", ["top:jewish-philanthropy-relief"])
c("top:accidents", "תאונות ואסונות תחבורה", "Accidents and transport disasters", "top:disasters-health",
  "אסונות ימיים (טיטניק), תאונות רכבת, תעופה וצפלינים, ואסונות מכרות.", ["top:aviation"])
c("top:medicine-public-health", "רפואה ובריאות הציבור", "Medicine and public health", "top:disasters-health",
  "חידושים ברפואה (תרופת 606), שחפת, חיסונים, תברואה ובריאות בקהילות.", [])

# ---------------- 18. Press, culture, science ----------------
c("top:press-culture-science", "עיתונות, תרבות ומדע", "Press, culture and science", None,
  "העיתונות ומדוריה, ספרות, תיאטרון, בידור, הנצחה, מדע וטכנולוגיה.", [])
c("top:press-censorship", "חופש העיתונות וצנזורה", "Press freedom and censorship", "top:press-culture-science",
  "צנזורה, עיקולים, קנסות ומשפטים נגד עיתונים ועיתונאים, וחוקי עיתונות.", ["top:russian-reaction-repression"])
c("top:jewish-press", "העיתונות היהודית", "Jewish press", "top:press-culture-science",
  "עיתונות ביידיש, בעברית ובלדינו, העיתונות היהודית בטורקיה ובסלוניקי, ומסעות ומשלחות של העיתון.", ["top:jewish-languages"])
c("top:press-opinion-polemics", "דעת קהל, תגובות העיתונות ופולמוסים", "Public opinion, press reactions and polemics", "top:press-culture-science",
  "תגובות העיתונות האירופית והרוסית, פולמוסים עיתונאיים, הכחשות רשמיות, עיתונות ודיפלומטיה ועיתונות לאומנית.", [])
c("top:news-digests", "מדורי מברקים וידיעות קצרות", "Telegram columns and news digests", "top:press-culture-science",
  "מדורי מברקים, כותרות וידיעות קצרות מעורבות שאין להם נושא מרכזי אחד.", [])
c("top:literature-serials", "ספרות, רומנים בהמשכים וביקורת", "Literature, serialized novels and criticism", "top:press-culture-science",
  "רומנים היסטוריים בהמשכים, סיפורת מתורגמת, יצירות סופרים (שלום עליכם), ביקורת ספרות ודרמה.", [])
c("top:satire-humour", "סאטירה והומור", "Satire and humour", "top:press-culture-science",
  "סאטירה פוליטית וחברתית, פרודיות, הומור ומברקים הומוריסטיים.", [])
c("top:arts-entertainment", "תיאטרון, בידור, ספורט ותערוכות", "Theatre, entertainment, sport and exhibitions", "top:press-culture-science",
  "תיאטרון (כולל יידי), שחמט וספורט, אופנה, תערוכות עולמיות וחיי חברה גבוהה.", [])
c("top:ads-notices", "מודעות ופרסומות", "Advertisements and notices", "top:press-culture-science",
  "פרסומות מסחריות, מודעות מנוי, הגרלות וקופוני טיול לארץ ישראל, מודעות אבל וברכה.", [])
c("top:commemorations", "יובלות, הנצחה והספדים", "Jubilees, commemorations and obituaries", "top:press-culture-science",
  "חגיגות יובל, הנצחת אישים ואירועים, הספדים ופטירת אישים.", [])
c("top:aviation", "תעופה", "Aviation", "top:press-culture-science",
  "טיסות ותחרויות טיסה, התפתחות התעופה וצפלינים (אסונות אוויר – גם תחת תאונות).", ["top:accidents"])
c("top:science-archaeology", "מדע, ארכאולוגיה וטכנולוגיה", "Science, archaeology and technology", "top:press-culture-science",
  "תגליות ותופעות מדעיות (שביט האלי), חפירות ארכאולוגיות, תחזיות טכנולוגיות והמצאות.", [])

# ---------------- 19. Society ----------------
c("top:society-labour", "חברה, עבודה וסוציאליזם", "Society, labour and socialism", None,
  "תנועת הפועלים והסוציאליזם, שביתות, מעמד האישה, סטודנטים, מיליטריזם, לאומיות וחיי חברה.", [])
c("top:labour-strikes", "שביתות ותנאי עבודה", "Strikes and working conditions", "top:society-labour",
  "שביתות והפגנות פועלים, שביתות כלליות, סכסוכי עבודה, תנאי שכר ואבטלה.", [])
c("top:socialism", "סוציאליזם ותנועת הפועלים", "Socialism and the labour movement", "top:society-labour",
  "מפלגות סוציאליסטיות וסוציאל-דמוקרטיות, האינטרנציונל וקונגרסיו, סולידריות פועלים, אנטי-מיליטריזם סוציאליסטי ואנרכיזם.",
  ["top:peace-movement-arbitration"])
c("top:women-family", "נשים, משפחה ונישואין", "Women, family and marriage", "top:society-labour",
  "זכות הבחירה לנשים וזכויות נשים, השכלת נשים, לבוש ומעמד האישה, שידוכים, נישואין ושערוריות משפחתיות.", [])
c("top:prostitution-trafficking", "זנות וסחר בנשים", "Prostitution and trafficking in women", "top:society-labour",
  "סחר בנשים ('העבדות הלבנה'), זנות ובתי בושת והמאבק בהם.", [])
c("top:students-universities", "סטודנטים, אוניברסיטאות וחופש אקדמי", "Students and universities", "top:society-labour",
  "תסיסת סטודנטים, חופש אקדמי, רפורמות באוניברסיטאות ופיקוח עליהן.", ["top:numerus-clausus"])
c("top:militarism-conscription", "מיליטריזם, צבא וגיוס", "Militarism, armies and conscription", "top:society-labour",
  "מיליטריזם ופטריוטיזם, גיוס ושירות צבאי, הכנות ותמרונים צבאיים, אסטרטגיה וחימוש (צבא עות'מאני ויהודים בצבא – בנפרד).", [])
c("top:nationalism", "לאומיות ותנועות לאומיות", "Nationalism and national movements", "top:society-labour",
  "לאומיות ולאומנות כתופעה כללית, תנועות לאומיות באירופה ומתיחויות לאומיות (גרמנים וסלאבים, לגיונות פולניים).", [])
c("top:daily-life-leisure", "חיי יומיום, פנאי ונופש", "Daily life, leisure and travel", "top:society-labour",
  "נופש בבתי מרפא, טיולים ונסיעות, רכילות חברתית ותיאורי חיי יומיום.", [])

# ---------------- 20. Crime & law ----------------
c("top:crime-law", "פשיעה, משפט וענישה", "Crime, law and punishment", None,
  "פשיעה, משפטים, אלימות פוליטית, ענישה, ריגול ושחיתות.", [])
c("top:crime-robbery", "פשיעה ושוד", "Crime and robbery", "top:crime-law",
  "שוד, רצח, הונאות, גניבות, כנופיות ושוד מזוין (בעיקר ברוסיה ובפולין).", ["pl:russian-empire", "pl:warsaw"])
c("top:trials", "משפטים ופרשות משפטיות", "Trials and court cases", "top:crime-law",
  "משפטים פליליים, פוליטיים וצבאיים ופרשות משפטיות בולטות, ומערכת המשפט.", ["top:blood-libels"])
c("top:political-violence", "אלימות פוליטית, טרור והתנקשויות", "Political violence, terrorism and assassinations", "top:crime-law",
  "התנקשויות ברשמים ובמלכים, פיגועי פצצות, טרור מהפכני ואנרכיסטי ורציחות פוליטיות.", [])
c("top:death-penalty-punishment", "עונש מוות, ענישה ובתי כלא", "Death penalty, punishment and prisons", "top:crime-law",
  "עונש המוות והוצאות להורג, ביטולו, עונשי גוף, בתי כלא ובריחת אסירים, חנינות.", [])
c("top:espionage", "ריגול", "Espionage", "top:crime-law",
  "פרשיות ריגול ופעילות חתרנית.", [])
c("top:corruption-scandals", "שחיתות ושערוריות ציבוריות", "Corruption and public scandals", "top:crime-law",
  "שוחד ושחיתות בממשל ובצבא, שערוריות ציבוריות (פרשת מרקוני) ושרירות פקידים.", [])

# ---------------- 21. Islam ----------------
c("top:islam-middle-east", "האסלאם והעולם המוסלמי", "Islam and the Muslim world", None,
  "דת, חברה, תרבות ותנועות פוליטיות בעולם המוסלמי והערבי, ויחסים בין דתות במזרח.", [])
c("top:pan-islamism", "פאן-אסלאמיזם והתעוררות העולם המוסלמי", "Pan-Islamism and Muslim awakening", "top:islam-middle-east",
  "פאן-אסלאמיזם וסולידריות מוסלמית, התעוררות העולם המוסלמי, ח'ליפות, רפורמות חוקתיות במדינות מוסלמיות ורגשות אנטי-אירופיים.",
  ["top:moroccan-tribal-revolts"])
c("top:muslim-religious-life", "דת ופולחן מוסלמיים", "Muslim religious life", "top:islam-middle-east",
  "עלייה לרגל למכה, חגים, אמונות עממיות ופולחן קדושים, אנשי דת מוסלמים ומקומות קדושים.", [])
c("top:arab-egyptian-nationalism", "לאומיות ערבית ומצרית", "Arab and Egyptian nationalism", "top:islam-middle-east",
  "התנועה הלאומית הערבית, הלאומיות המצרית והעיתונות הערבית.", ["pl:egypt", "pl:syria", "top:arab-provinces-revolts"])
c("top:ethnography-orient", "תיאורים אתנוגרפיים של המזרח", "Ethnographic depictions of the Orient", "top:islam-middle-east",
  "תיאורי חיי בדואים, דרוזים, כורדים ושבטי מרוקו, תרבות מרוקאית וערבית, נוף וחיי יומיום במזרח ודימויים של עמי המזרח.",
  ["pl:morocco", "pl:syria"])
c("top:interreligious-relations-orient", "יחסים בין-דתיים במזרח", "Interreligious relations in the Orient", "top:islam-middle-east",
  "יחסי מוסלמים, נוצרים, דרוזים ויהודים, מתיחות בין-דתית וחשש ממלחמת קודש.", ["top:ottoman-nationalities"])

# =============== EVENTS ===============
E = []
def e(id, he, en, date, end, broader, place, participants, desc, en_alt=()):
    E.append({"id": id, "he": he, "en": en, "en_alt": list(en_alt), "date": date, "end": end,
              "broader": broader, "place": place, "participants": list(participants), "desc": desc})

# Morocco
e("ev:first-moroccan-crisis", "המשבר המרוקאי הראשון", "First Moroccan Crisis", "1905-03-31", "1906-04-07",
  "top:franco-german-rivalry-morocco", "pl:morocco", ["pl:germany", "pl:france", "pl:morocco"],
  "Franco-German crisis over Morocco triggered by the Kaiser's Tangier visit", ["Tangier Crisis"])
e("ev:kaiser-visit-tangier", "ביקור הקייזר בטנג'יר", "Kaiser Wilhelm II's visit to Tangier", "1905-03-31", None,
  "top:franco-german-rivalry-morocco", "pl:tangier", ["pl:germany", "pl:morocco"],
  "Wilhelm II landed at Tangier and declared support for Moroccan independence", ["Tangier Crisis"])
e("ev:delcasse-resignation", "התפטרות דלקאסה", "Resignation of Théophile Delcassé", "1905-06-06", None,
  "top:franco-german-rivalry-morocco", "pl:france", ["pl:france", "pl:germany"],
  "French foreign minister Delcassé forced to resign under German pressure over Morocco", ["Théophile Delcassé"])
e("ev:algeciras-conference", "ועידת אלחסיראס", "Algeciras Conference", "1906-01-16", "1906-04-07",
  "top:morocco-international-diplomacy", "pl:spain", ["pl:france", "pl:germany", "pl:spain", "pl:united-kingdom", "pl:russian-empire", "pl:italy", "pl:austria-hungary", "pl:united-states", "pl:morocco"],
  "international conference on Morocco; Act of Algeciras on police, state bank and open door", ["Act of Algeciras", "Algeciras Act"])
e("ev:mauchamp-murder", "רצח הרופא מושאן במרקש", "Murder of Émile Mauchamp", "1907-03-19", None,
  "top:french-intervention-morocco", "pl:marrakesh", ["pl:france", "pl:morocco"],
  "murder of French doctor Émile Mauchamp in Marrakesh, pretext for occupation of Oujda", ["Émile Mauchamp"])
e("ev:occupation-of-oujda", "כיבוש אוג'דה", "French occupation of Oujda", "1907-03-29", None,
  "top:french-intervention-morocco", "pl:morocco", ["pl:france", "pl:morocco"],
  "French troops from Algeria occupied Oujda", ["Occupation of Oujda (1907)"])
e("ev:maclean-kidnapping", "חטיפת קאיד מקלין בידי רייסולי", "Kidnapping of Kaid Maclean", "1907-07-03", "1908-02",
  "top:moroccan-tribal-revolts", "pl:morocco", ["pl:morocco", "pl:united-kingdom"],
  "Raisuli kidnapped the Sultan's British military adviser Kaid Harry Maclean", ["Harry Maclean", "Mulai Ahmed er Raisuni"])
e("ev:casablanca-riots-1907", "המהומות בקזבלנקה 1907", "1907 Casablanca riots", "1907-07-30", None,
  "top:moroccan-tribal-revolts", "pl:casablanca", ["pl:morocco", "pl:france"],
  "killing of European workers at the Casablanca port works, prelude to the French bombardment", ["Bombardment of Casablanca (1907)"])
e("ev:bombardment-of-casablanca", "הפגזת קזבלנקה", "Bombardment of Casablanca", "1907-08-05", "1907-08-07",
  "top:french-intervention-morocco", "pl:casablanca", ["pl:france", "pl:spain", "pl:morocco"],
  "French naval bombardment and landing at Casablanca", ["Bombardment of Casablanca (1907)"])
e("ev:casablanca-mellah-pogrom-1907", "פרעות במלאח של קזבלנקה", "Casablanca mellah pogrom (1907)", "1907-08-05", "1907-08-07",
  "top:moroccan-jews", "pl:casablanca", ["pl:morocco"],
  "looting and killing in the Jewish quarter of Casablanca during the bombardment")
e("ev:chaouia-campaign", "מסע השאוויה", "Chaouia campaign", "1907-08", "1908-05",
  "top:french-intervention-morocco", "pl:casablanca", ["pl:france", "pl:morocco"],
  "French military campaign in the Chaouia hinterland of Casablanca", ["French conquest of Morocco"])
e("ev:hafidiya", "החפיטיה (מלחמת האחים על הסולטנות)", "Hafidiya", "1907-08-16", "1908-08-23",
  "top:moroccan-internal-politics", "pl:marrakesh", ["pl:morocco"],
  "civil war in which Abd al-Hafid overthrew his brother Sultan Abd al-Aziz", ["Hafidiya revolution"])
e("ev:franco-german-accord-1909", "ההסכם הצרפתי-גרמני על מרוקו 1909", "Franco-German Agreement on Morocco (1909)", "1909-02-09", None,
  "top:franco-german-rivalry-morocco", None, ["pl:france", "pl:germany"],
  "accord recognizing French political interests in Morocco in return for German economic equality")
e("ev:melilla-war-1909", "מלחמת מלייה 1909", "Second Melillan campaign", "1909-07-09", "1910-01-27",
  "top:spanish-intervention-morocco", "pl:morocco", ["pl:spain", "pl:morocco"],
  "Spanish war against Rif tribes around Melilla", ["Melilla War", "Rif War of 1909"])
e("ev:tragic-week", "השבוע הטרגי בברצלונה", "Tragic Week (Spain)", "1909-07-26", "1909-08-02",
  "top:spanish-intervention-morocco", "pl:spain", ["pl:spain"],
  "riots in Barcelona against call-up of reservists for the Melilla war", ["Setmana Tràgica"])
e("ev:siege-of-fez-1911", "מצור המורדים על פאס 1911", "Siege of Fez (1911)", "1911-03", "1911-05-21",
  "top:moroccan-tribal-revolts", "pl:fez", ["pl:morocco"],
  "rebel tribes besieged Sultan Abd al-Hafid in Fez")
e("ev:fez-expedition-1911", "מסע פאס הצרפתי", "French expedition to Fez (1911)", "1911-04", "1911-06",
  "top:french-intervention-morocco", "pl:fez", ["pl:france", "pl:morocco"],
  "French relief column under Moinier entered Fez on 21 May 1911", ["Fez expedition"])
e("ev:spanish-landing-larache", "הנחיתה הספרדית בלאראש", "Spanish occupation of Larache", "1911-06-08", None,
  "top:spanish-intervention-morocco", "pl:morocco", ["pl:spain", "pl:morocco"],
  "Spain occupied Larache and Ksar el-Kebir in response to the French Fez expedition", ["Larache"])
e("ev:agadir-crisis", "משבר אגאדיר", "Agadir Crisis", "1911-07-01", "1911-11-04",
  "top:franco-german-rivalry-morocco", "pl:agadir", ["pl:germany", "pl:france", "pl:united-kingdom"],
  "German gunboat Panther sent to Agadir; Second Moroccan Crisis", ["Second Moroccan Crisis", "Panthersprung nach Agadir"])
e("ev:kert-campaign", "מסע הקרט", "Kert campaign", "1911-08-24", "1912-05-15",
  "top:spanish-intervention-morocco", "pl:morocco", ["pl:spain", "pl:morocco"],
  "Spanish campaign against Rif tribes along the Kert river")
e("ev:morocco-congo-treaty", "ההסכם הצרפתי-גרמני (מרוקו-קונגו) 1911", "Morocco–Congo Treaty", "1911-11-04", None,
  "top:franco-german-rivalry-morocco", None, ["pl:france", "pl:germany"],
  "Germany accepted French protectorate over Morocco in exchange for part of French Congo", ["Franco-German Treaty of 1911", "Treaty of Berlin (1911)"])
e("ev:treaty-of-fez", "הסכם פאס", "Treaty of Fes", "1912-03-30", None,
  "top:french-protectorate-morocco", "pl:fez", ["pl:france", "pl:morocco"],
  "treaty making Morocco a French protectorate", ["Treaty of Fez"])
e("ev:fez-riots-1912", "מהומות פאס 1912 (טְרִיטֶל)", "1912 Fez riots", "1912-04-17", "1912-04-19",
  "top:french-protectorate-morocco", "pl:fez", ["pl:france", "pl:morocco"],
  "mutiny of Moroccan troops and riots in Fez against the protectorate, including sack of the mellah", ["Tritel", "Fez mutiny"])
e("ev:abdication-abd-al-hafid", "התפטרות הסולטאן עבד אל-חפיט", "Abdication of Abd al-Hafid", "1912-08-12", None,
  "top:moroccan-internal-politics", "pl:morocco", ["pl:morocco", "pl:france"],
  "abdication of Sultan Abd al-Hafid and accession of Yusuf", ["Abd al-Hafid of Morocco"])
e("ev:battle-of-sidi-bou-othman", "קרב סידי בו עות'מאן", "Battle of Sidi Bou Othman", "1912-09-06", None,
  "top:french-intervention-morocco", "pl:marrakesh", ["pl:france", "pl:morocco"],
  "French defeat of Ahmed al-Hiba's uprising and entry into Marrakesh", ["El Hiba uprising"])
e("ev:franco-spanish-treaty-1912", "ההסכם הצרפתי-ספרדי על מרוקו 1912", "Treaty Between France and Spain Regarding Morocco", "1912-11-27", None,
  "top:spanish-intervention-morocco", "pl:spain", ["pl:france", "pl:spain", "pl:morocco"],
  "treaty establishing the Spanish protectorate zone in northern Morocco", ["Franco-Spanish Treaty (1912)"])
e("ev:entente-cordiale", "ההסכמה הלבבית", "Entente Cordiale", "1904-04-08", None,
  "top:alliances-ententes", None, ["pl:france", "pl:united-kingdom"],
  "Anglo-French agreements incl. free hand for France in Morocco")
e("ev:franco-italian-agreement-1902", "ההסכם הצרפתי-איטלקי על טריפולי ומרוקו", "Prinetti–Barrère Accord", "1902-11-01", None,
  "top:alliances-ententes", None, ["pl:france", "pl:italy"],
  "secret Franco-Italian accord: Italian free hand in Tripoli, French in Morocco", ["Franco-Italian Agreement (1902)"])

# Ottoman
e("ev:young-turk-revolution", "מהפכת הטורקים הצעירים", "Young Turk Revolution", "1908-07-03", "1908-07-24",
  "top:young-turk-revolution", "pl:thessaloniki", ["pl:ottoman-empire"],
  "constitutional revolution restoring the 1876 Ottoman constitution")
e("ev:ottoman-election-1908", "הבחירות לפרלמנט העות'מאני 1908", "1908 Ottoman general election", "1908-11", "1908-12",
  "top:ottoman-politics", "pl:ottoman-empire", ["pl:ottoman-empire"],
  "first elections after the revolution; parliament opened 17 Dec 1908")
e("ev:31-march-incident", "ההפיכה הנגדית (אירוע 31 במרץ)", "31 March incident", "1909-04-13", "1909-04-24",
  "top:young-turk-revolution", "pl:istanbul", ["pl:ottoman-empire"],
  "counter-revolutionary uprising in Istanbul suppressed by the Action Army", ["Action Army"])
e("ev:deposition-abdul-hamid", "הדחת הסולטאן עבדול חמיד השני", "Deposition of Abdul Hamid II", "1909-04-27", None,
  "top:young-turk-revolution", "pl:istanbul", ["pl:ottoman-empire"],
  "deposition of Abdul Hamid II, exile to Salonica and accession of Mehmed V", ["Abdul Hamid II"])
e("ev:adana-massacre", "טבח אדנה", "Adana massacre", "1909-04", None,
  "top:armenian-question", None, ["pl:ottoman-empire"], "massacre of Armenians in Adana province")
e("ev:hauran-druze-rebellion", "מרד הדרוזים בחוראן", "Hauran Druze Rebellion", "1909-05", "1910-11",
  "top:arab-provinces-revolts", "pl:syria", ["pl:ottoman-empire"],
  "Druze revolt in the Hauran suppressed by Sami Pasha al-Farouqi; executions in Damascus")
e("ev:albanian-revolt-1910", "המרד האלבני 1910", "Albanian revolt of 1910", "1910-04", "1910-06",
  "top:albanian-question", "pl:albania", ["pl:ottoman-empire", "pl:albania"], "Albanian uprising in Kosovo vilayet")
e("ev:albanian-revolt-1911", "המרד האלבני 1911", "Malissori uprising", "1911-03", "1911-08",
  "top:albanian-question", "pl:albania", ["pl:ottoman-empire", "pl:albania", "pl:montenegro"], "Malësori uprising in northern Albania", ["Albanian revolt of 1911"])
e("ev:albanian-revolt-1912", "המרד האלבני 1912", "Albanian revolt of 1912", "1912-01", "1912-08",
  "top:albanian-question", "pl:albania", ["pl:ottoman-empire", "pl:albania"], "last Albanian revolt against Ottoman rule")
e("ev:albanian-independence", "הכרזת העצמאות של אלבניה", "Albanian Declaration of Independence", "1912-11-28", None,
  "top:albanian-question", "pl:albania", ["pl:albania"], "Albanian independence proclaimed at Vlorë")
e("ev:yemen-revolt-1911", "המרד בתימן 1911", "Treaty of Daan", "1911", "1911-10",
  "top:arab-provinces-revolts", None, ["pl:ottoman-empire"],
  "Zaydi revolt under Imam Yahya ended by the Treaty of Daan", ["Yemeni revolt 1904–1911"])
e("ev:raid-on-sublime-porte", "הפשיטה על הפורטה הנשגבה (הפיכת 1913)", "1913 Ottoman coup d'état", "1913-01-23", None,
  "top:ottoman-politics", "pl:istanbul", ["pl:ottoman-empire"],
  "CUP coup bringing the Three Pashas to power", ["Raid on the Sublime Porte"])

# Balkans
e("ev:bulgarian-independence", "הכרזת העצמאות של בולגריה", "Bulgarian Declaration of Independence", "1908-10-05", None,
  "top:balkan-states-politics", "pl:bulgaria", ["pl:bulgaria", "pl:ottoman-empire"], "Ferdinand proclaimed Bulgarian independence")
e("ev:bosnian-crisis", "משבר בוסניה", "Bosnian Crisis", "1908-10-06", "1909-03-31",
  "top:austria-hungary-balkans", "pl:balkans", ["pl:austria-hungary", "pl:serbia", "pl:russian-empire", "pl:ottoman-empire"],
  "Austro-Hungarian annexation of Bosnia-Herzegovina and the ensuing crisis", ["Annexation crisis"])
e("ev:ottoman-boycott-austria-1908", "החרם העות'מאני על סחורות אוסטריות", "1908 Ottoman boycott of Austria-Hungary", "1908-10", "1909-02",
  "top:austria-hungary-balkans", "pl:ottoman-empire", ["pl:ottoman-empire", "pl:austria-hungary"], "boycott of Austrian goods after annexation of Bosnia")
e("ev:cretan-union-1908", "הכרזת איחוד כרתים עם יוון", "Cretan State", "1908-10-07", None,
  "top:cretan-question", "pl:crete", ["pl:greece", "pl:crete", "pl:ottoman-empire"],
  "Cretan assembly declared union with Greece", ["Union of Crete with Greece"])
e("ev:goudi-coup", "הפיכת גודי", "Goudi coup", "1909-08-28", None,
  "top:balkan-states-politics", "pl:greece", ["pl:greece"], "Greek military coup leading to Venizelos' rise")
e("ev:balkan-league", "הקמת הברית הבלקנית", "Balkan League", "1912-03-13", "1912-10",
  "top:balkan-wars", "pl:balkans", ["pl:serbia", "pl:bulgaria", "pl:greece", "pl:montenegro"], "alliance of Balkan states against the Ottoman Empire")
e("ev:first-balkan-war", "מלחמת הבלקן הראשונה", "First Balkan War", "1912-10-08", "1913-05-30",
  "top:balkan-wars", "pl:balkans", ["pl:bulgaria", "pl:serbia", "pl:greece", "pl:montenegro", "pl:ottoman-empire"], "Balkan League war against the Ottoman Empire")
e("ev:capture-of-thessaloniki-1912", "כיבוש סלוניקי בידי יוון", "Greek capture of Thessaloniki", "1912-11-08", None,
  "top:balkan-wars", "pl:thessaloniki", ["pl:greece", "pl:ottoman-empire", "pl:bulgaria"],
  "surrender of Salonica to the Greek army", ["Battle of Yenidje", "Liberation of Thessaloniki"])
e("ev:siege-of-scutari", "המצור על סקוטרי", "Siege of Scutari (1912–1913)", "1912-10-28", "1913-04-23",
  "top:balkan-wars", "pl:albania", ["pl:montenegro", "pl:serbia", "pl:ottoman-empire"], "Montenegrin siege of Shkodër; Scutari crisis with the powers", ["Scutari crisis"])
e("ev:siege-of-adrianople", "המצור על אדריאנופול", "Siege of Adrianople (1912–1913)", "1912-11-03", "1913-03-26",
  "top:balkan-wars", None, ["pl:bulgaria", "pl:serbia", "pl:ottoman-empire"], "Bulgarian-Serbian siege and capture of Edirne")
e("ev:london-conference-1912", "ועידת לונדון (השלום והשגרירים) 1912–1913", "London Conference of 1912–1913", "1912-12-16", "1913-08-11",
  "top:balkan-wars", "pl:united-kingdom", ["pl:united-kingdom", "pl:ottoman-empire", "pl:bulgaria", "pl:serbia", "pl:greece", "pl:montenegro"],
  "peace talks and ambassadors' conference on the Balkan settlement and Albania", ["Treaty of London (1913)"])
e("ev:second-balkan-war", "מלחמת הבלקן השנייה", "Second Balkan War", "1913-06-29", "1913-08-10",
  "top:balkan-wars", "pl:macedonia", ["pl:bulgaria", "pl:serbia", "pl:greece", "pl:romania", "pl:ottoman-empire", "pl:montenegro"], "war of Bulgaria against its former allies")
e("ev:treaty-of-bucharest-1913", "הסכם בוקרשט 1913", "Treaty of Bucharest (1913)", "1913-08-10", None,
  "top:balkan-wars", None, ["pl:bulgaria", "pl:serbia", "pl:greece", "pl:romania", "pl:montenegro"], "peace treaty ending the Second Balkan War")
e("ev:assassination-george-i", "רצח המלך גאורגיוס הראשון", "Assassination of George I of Greece", "1913-03-18", None,
  "top:balkan-states-politics", "pl:thessaloniki", ["pl:greece"],
  "assassination of King George I of Greece in Salonica", ["George I of Greece"])

# Italo-Turkish
e("ev:italo-turkish-war", "המלחמה האיטלקית-טורקית", "Italo-Turkish War", "1911-09-29", "1912-10-18",
  "top:italo-turkish-war", "pl:libya", ["pl:italy", "pl:ottoman-empire"], "Italian war to seize Tripolitania and Cyrenaica", ["Turco-Italian War", "Tripolitanian War"])
e("ev:battle-of-tripoli-1911", "כיבוש טריפולי", "Battle of Tripoli (1911)", "1911-10-03", "1911-10-10",
  "top:libya-campaign", "pl:tripolitania", ["pl:italy", "pl:ottoman-empire"], "Italian bombardment and landing at Tripoli")
e("ev:battle-of-shar-al-shatt", "קרב שארע א-שט והטבח בטריפולי", "Battle of Shar al-Shatt", "1911-10-23", "1911-10-26",
  "top:libya-campaign", "pl:tripolitania", ["pl:italy", "pl:ottoman-empire"], "Ottoman-Arab attack near Tripoli followed by Italian reprisals")
e("ev:annexation-of-libya", "סיפוח טריפולי וקירנאיקה לאיטליה", "Italian Libya", "1911-11-05", None,
  "top:libya-campaign", "pl:libya", ["pl:italy"], "royal decree annexing Tripolitania and Cyrenaica")
e("ev:battle-of-beirut-1912", "הפגזת בירות", "Battle of Beirut (1912)", "1912-02-24", None,
  "top:italo-turkish-naval-war", None, ["pl:italy", "pl:ottoman-empire"], "Italian cruisers sank Ottoman ships at Beirut")
e("ev:dardanelles-1912", "ההתקפה האיטלקית על הדרדנלים וסגירתם", "Italian attack on the Dardanelles (1912)", "1912-04-18", "1912-05",
  "top:italo-turkish-naval-war", None, ["pl:italy", "pl:ottoman-empire"], "Italian naval attack and Ottoman closure of the Straits")
e("ev:dodecanese-occupation", "כיבוש איי הדודקאנס", "Italian occupation of the Dodecanese", "1912-04", "1912-05",
  "top:italo-turkish-naval-war", None, ["pl:italy", "pl:ottoman-empire"], "Italy occupied Rhodes and the Dodecanese")
e("ev:treaty-of-ouchy", "הסכם אושי (לוזאן 1912)", "Treaty of Ouchy", "1912-10-18", None,
  "top:italo-turkish-war-diplomacy", None, ["pl:italy", "pl:ottoman-empire"], "peace treaty ending the Italo-Turkish War", ["First Treaty of Lausanne"])

# Russia
e("ev:russo-japanese-war", "המלחמה הרוסית-יפנית", "Russo-Japanese War", "1904-02-08", "1905-09-05",
  "top:russo-japanese-war", None, ["pl:russian-empire", "pl:japan"], "war between Russia and Japan over Manchuria and Korea")
e("ev:siege-of-port-arthur", "נפילת פורט ארתור", "Siege of Port Arthur", "1904-08-01", "1905-01-02",
  "top:russo-japanese-war", "pl:china", ["pl:russian-empire", "pl:japan"], "Japanese siege and capture of Port Arthur")
e("ev:battle-of-mukden", "קרב מוקדן", "Battle of Mukden", "1905-02-20", "1905-03-10",
  "top:russo-japanese-war", "pl:china", ["pl:russian-empire", "pl:japan"], "major land battle of the war")
e("ev:battle-of-tsushima", "קרב צושימה", "Battle of Tsushima", "1905-05-27", "1905-05-28",
  "top:russo-japanese-war", None, ["pl:russian-empire", "pl:japan"], "destruction of the Russian Baltic Fleet")
e("ev:treaty-of-portsmouth", "הסכם פורטסמות", "Treaty of Portsmouth", "1905-09-05", None,
  "top:russo-japanese-war", "pl:united-states", ["pl:russian-empire", "pl:japan", "pl:united-states"], "peace treaty ending the Russo-Japanese War", ["Portsmouth Peace Conference"])
e("ev:russian-revolution-1905", "המהפכה הרוסית של 1905", "Russian Revolution of 1905", "1905-01-22", "1907-06-16",
  "top:russian-revolution-1905", "pl:russian-empire", ["pl:russian-empire"], "wave of revolutionary unrest in the Russian Empire")
e("ev:bloody-sunday-1905", "יום ראשון העקוב מדם", "Bloody Sunday (1905)", "1905-01-22", None,
  "top:russian-revolution-1905", "pl:saint-petersburg", ["pl:russian-empire"], "troops fired on Gapon's procession of workers")
e("ev:potemkin-mutiny", "מרד המלחים בפוטיומקין", "Russian battleship Potemkin", "1905-06-27", "1905-07-08",
  "top:russian-revolution-1905", None, ["pl:russian-empire"], "mutiny on the battleship Potemkin off Odessa", ["Potemkin mutiny", "Potemkin uprising"])
e("ev:october-manifesto", "מניפסט אוקטובר", "October Manifesto", "1905-10-30", None,
  "top:russian-revolution-1905", "pl:saint-petersburg", ["pl:russian-empire"], "Nicholas II granted civil liberties and an elected Duma")
e("ev:odessa-pogrom-1905", "פוגרום אודסה 1905", "1905 Odessa pogrom", "1905-10-31", "1905-11-03",
  "top:pogroms", None, ["pl:russian-empire"], "anti-Jewish pogrom in Odessa after the October Manifesto", ["Odessa pogroms"])
e("ev:sevastopol-uprising-1905", "מרד סבסטופול ופרשת שמידט", "Sevastopol uprising (1905)", "1905-11-24", "1905-11-28",
  "top:russian-revolution-1905", None, ["pl:russian-empire"], "naval uprising led by Lt. Pyotr Schmidt, executed 1906")
e("ev:moscow-uprising-1905", "מרד דצמבר במוסקבה", "Moscow uprising of 1905", "1905-12-07", "1905-12-18",
  "top:russian-revolution-1905", None, ["pl:russian-empire"], "armed workers' uprising in Moscow", ["December Uprising"])
e("ev:russian-election-1906", "הבחירות לדומה הראשונה", "1906 Russian legislative election", "1906-03", "1906-04",
  "top:state-duma", "pl:russian-empire", ["pl:russian-empire"], "elections to the First Duma")
e("ev:first-duma", "הדומה הראשונה ופיזורה", "1st State Duma of the Russian Empire", "1906-05-10", "1906-07-21",
  "top:state-duma", "pl:saint-petersburg", ["pl:russian-empire"], "first Russian parliament, dissolved after 72 days", ["State Duma (Russian Empire)"])
e("ev:vyborg-manifesto", "מניפסט ויבורג", "Vyborg Manifesto", "1906-07-23", None,
  "top:state-duma", None, ["pl:russian-empire"], "appeal of dissolved Duma deputies; signatories prosecuted")
e("ev:bialystok-pogrom", "פוגרום ביאליסטוק", "Białystok pogrom", "1906-06-14", "1906-06-16",
  "top:pogroms", None, ["pl:russian-empire"], "anti-Jewish pogrom in Białystok")
e("ev:siedlce-pogrom", "פוגרום שדלץ", "Siedlce pogrom", "1906-09-08", "1906-09-10",
  "top:pogroms", None, ["pl:russian-empire"], "army-led pogrom in Siedlce")
e("ev:russian-election-1907-jan", "הבחירות לדומה השנייה", "January 1907 Russian legislative election", "1907-01", "1907-02",
  "top:state-duma", "pl:russian-empire", ["pl:russian-empire"], "elections to the Second Duma")
e("ev:second-duma", "הדומה השנייה", "2nd State Duma of the Russian Empire", "1907-03-05", "1907-06-16",
  "top:state-duma", "pl:saint-petersburg", ["pl:russian-empire"], "second Duma, dissolved by Stolypin", ["State Duma (Russian Empire)"])
e("ev:june-coup-1907", "הפיכת יוני 1907", "Coup of June 1907", "1907-06-16", None,
  "top:state-duma", "pl:saint-petersburg", ["pl:russian-empire"], "dissolution of the Second Duma and new restrictive electoral law", ["Third of June Coup"])
e("ev:russian-election-1907-sep", "הבחירות לדומה השלישית", "September 1907 Russian legislative election", "1907-09", "1907-10",
  "top:state-duma", "pl:russian-empire", ["pl:russian-empire"], "elections to the Third Duma")
e("ev:russian-election-1912", "הבחירות לדומה הרביעית", "1912 Russian legislative election", "1912-09", "1912-10",
  "top:state-duma", "pl:russian-empire", ["pl:russian-empire"], "elections to the Fourth Duma")
e("ev:stolypin-assassination", "רצח סטוליפין", "Assassination of Pyotr Stolypin", "1911-09-14", None,
  "top:political-violence", "pl:kiev", ["pl:russian-empire"], "Stolypin shot by Dmitry Bogrov at the Kiev opera during the Tsar's visit", ["Pyotr Stolypin"])
e("ev:beilis-affair", "פרשת בייליס", "Beilis affair", "1911-03-20", "1913-11-10",
  "top:blood-libels", "pl:kiev", ["pl:russian-empire"], "blood libel after the murder of Andrei Yushchinsky; trial and acquittal of Menahem Mendel Beilis",
  ["Menahem Mendel Beilis", "Beilis trial", "Andrei Yushchinsky"])
e("ev:lena-massacre", "טבח לנה", "Lena massacre", "1912-04-17", None,
  "top:labour-strikes", "pl:russian-empire", ["pl:russian-empire"], "troops shot striking gold miners on the Lena river", ["Lena Goldfields massacre"])
e("ev:february-revolution", "מהפכת פברואר", "February Revolution", "1917-03-08", "1917-03-16",
  "top:russian-revolution-1917", "pl:saint-petersburg", ["pl:russian-empire"], "overthrow of the Tsar and formation of the Provisional Government")
e("ev:october-revolution", "מהפכת אוקטובר", "October Revolution", "1917-11-07", None,
  "top:russian-revolution-1917", "pl:saint-petersburg", ["pl:russian-empire"], "Bolshevik seizure of power", ["Bolshevik Revolution"])
e("ev:kishinev-pogrom", "פוגרום קישינב", "Kishinev pogrom", "1903-04-19", "1903-04-20",
  "top:pogroms", None, ["pl:russian-empire"], "anti-Jewish pogrom in Kishinev (remembered and invoked in the corpus)")
e("ev:damascus-affair", "עלילת דמשק", "Damascus affair", "1840-02-05", None,
  "top:blood-libels", "pl:damascus", ["pl:syria"], "1840 blood libel against the Jews of Damascus")
e("ev:hilsner-affair", "פרשת הילזנר", "Hilsner affair", "1899-04", "1900",
  "top:blood-libels", None, ["pl:austria-hungary"], "blood libel trial of Leopold Hilsner in Bohemia")

# Persia / Asia
e("ev:persian-constitutional-revolution", "המהפכה החוקתית בפרס", "Persian Constitutional Revolution", "1905-12", "1911-12",
  "top:persian-revolution", "pl:persia", ["pl:persia"], "establishment of a parliament and constitution in Persia")
e("ev:siege-of-tabriz", "המצור על תבריז", "Siege of Tabriz", "1908-06", "1909-04",
  "top:persian-revolution", "pl:persia", ["pl:persia", "pl:russian-empire"], "royalist siege of constitutionalist Tabriz, ended by Russian intervention")
e("ev:triumph-of-tehran", "כיבוש טהראן בידי החוקתיים והדחת השאה", "Triumph of Tehran", "1909-07-13", "1909-07-16",
  "top:persian-revolution", "pl:persia", ["pl:persia"], "constitutionalists took Tehran and deposed Mohammad Ali Shah")
e("ev:anglo-russian-convention", "ההסכם האנגלו-רוסי", "Anglo-Russian Convention", "1907-08-31", None,
  "top:foreign-intervention-persia", None, ["pl:united-kingdom", "pl:russian-empire", "pl:persia"], "division of Persia into spheres of influence")
e("ev:potsdam-agreement-1911", "ההסכם הרוסי-גרמני בפוטסדאם", "Potsdam Agreement (1911)", "1911-08-19", None,
  "top:foreign-intervention-persia", None, ["pl:russian-empire", "pl:germany", "pl:persia"], "Russo-German agreement on Persia and the Baghdad railway")
e("ev:russian-ultimatum-persia-1911", "האולטימטום הרוסי לפרס 1911", "Russian ultimatum to Persia (1911)", "1911-11-29", "1911-12-24",
  "top:foreign-intervention-persia", "pl:persia", ["pl:russian-empire", "pl:persia"], "Russian ultimatum forcing Shuster's dismissal and closure of the Majlis", ["William Morgan Shuster"])
e("ev:xinhai-revolution", "המהפכה הסינית (שינהאי)", "1911 Revolution", "1911-10-10", "1912-02-12",
  "top:china", "pl:china", ["pl:china"], "overthrow of the Qing dynasty and founding of the Republic of China", ["Xinhai Revolution", "Chinese Revolution of 1911"])
e("ev:manchurian-plague", "מגפת הדבר במנצ'וריה", "Manchurian plague", "1910-10", "1911-03",
  "top:epidemics", "pl:china", ["pl:china", "pl:russian-empire"], "pneumonic plague epidemic in Manchuria", ["1910–1911 Manchurian plague"])
e("ev:japan-korea-annexation", "סיפוח קוריאה ליפן", "Japan–Korea Treaty of 1910", "1910-08-22", None,
  "top:japan-korea", None, ["pl:japan"], "Japanese annexation of Korea", ["Korea under Japanese rule"])
e("ev:anglo-japanese-alliance-1905", "חידוש הברית האנגלית-יפנית", "Anglo-Japanese Alliance", "1905-08-12", None,
  "top:alliances-ententes", None, ["pl:united-kingdom", "pl:japan"], "renewal and extension of the Anglo-Japanese Alliance")
e("ev:mexican-revolution", "המהפכה המקסיקנית", "Mexican Revolution", "1910-11-20", None,
  "top:americas-politics", None, [], "revolution against Porfirio Díaz")

# Diplomacy
e("ev:treaty-of-bjorko", "הסכם ביורקה", "Treaty of Björkö", "1905-07-24", None,
  "top:alliances-ententes", None, ["pl:germany", "pl:russian-empire"], "abortive Russo-German defensive treaty")
e("ev:russian-loan-1906", "ההלוואה הצרפתית לרוסיה 1906", "Russian loan of 1906", "1906-04", None,
  "top:finance-banking", "pl:france", ["pl:france", "pl:russian-empire"], "large French-led international loan to Russia after Algeciras")
e("ev:hague-conference-1907", "ועידת השלום השנייה בהאג", "Hague Conventions of 1899 and 1907", "1907-06-15", "1907-10-18",
  "top:peace-movement-arbitration", None, [], "Second Hague Peace Conference", ["Second Hague Conference"])
e("ev:swinemunde-meeting-1907", "פגישת הקיסרים בסווינמינדה", "Swinemünde meeting (1907)", "1907-08-03", "1907-08-06",
  "top:royal-visits-summits", "pl:germany", ["pl:germany", "pl:russian-empire"], "meeting of Wilhelm II and Nicholas II at Swinemünde")

# WWI
e("ev:assassination-franz-ferdinand", "רצח פרנץ פרדיננד בסרייבו", "Assassination of Archduke Franz Ferdinand", "1914-06-28", None,
  "top:wwi-outbreak-diplomacy", "pl:austria-hungary", ["pl:austria-hungary", "pl:serbia"], "assassination in Sarajevo triggering the July Crisis")
e("ev:july-crisis", "משבר יולי ופרוץ מלחמת העולם", "July Crisis", "1914-06-28", "1914-08-06",
  "top:wwi-outbreak-diplomacy", None, ["pl:austria-hungary", "pl:serbia", "pl:russian-empire", "pl:germany", "pl:france", "pl:united-kingdom"], "diplomatic crisis leading to the outbreak of WWI", ["Outbreak of World War I"])
e("ev:world-war-i", "מלחמת העולם הראשונה", "World War I", "1914-07-28", "1918-11-11",
  "top:wwi", None, [], "global war 1914–1918", ["First World War", "Great War"])
e("ev:ottoman-entry-wwi", "כניסת האימפריה העות'מאנית למלחמה", "Ottoman entry into World War I", "1914-10-29", "1914-11-14",
  "top:wwi-outbreak-diplomacy", "pl:ottoman-empire", ["pl:ottoman-empire", "pl:russian-empire", "pl:germany"], "Black Sea raid and Ottoman declaration of war", ["Black Sea raid"])
e("ev:battle-of-lodz-1914", "הקרב על לודז'", "Battle of Łódź (1914)", "1914-11-11", "1914-12-06",
  "top:wwi-eastern-front", None, ["pl:russian-empire", "pl:germany"], "battle on the Eastern Front in Russian Poland")
e("ev:battle-of-sarikamish", "קרב סאריקאמיש", "Battle of Sarikamish", "1914-12-22", "1915-01-17",
  "top:wwi-ottoman-fronts", None, ["pl:russian-empire", "pl:ottoman-empire"], "Ottoman offensive defeated in the Caucasus")
e("ev:raid-on-suez-canal", "ההתקפה העות'מאנית על תעלת סואץ", "Raid on the Suez Canal", "1915-01-26", "1915-02-04",
  "top:wwi-ottoman-fronts", "pl:egypt", ["pl:ottoman-empire", "pl:united-kingdom", "pl:germany"], "first Ottoman offensive against the Suez Canal")
e("ev:gallipoli-campaign", "מערכת גליפולי והדרדנלים", "Gallipoli campaign", "1915-02-19", "1916-01-09",
  "top:wwi-ottoman-fronts", None, ["pl:ottoman-empire", "pl:united-kingdom", "pl:france"], "Allied naval and land campaign at the Dardanelles", ["Dardanelles campaign"])
e("ev:bulgaria-enters-wwi", "כניסת בולגריה למלחמה", "Bulgaria during World War I", "1915-10-14", None,
  "top:wwi-outbreak-diplomacy", "pl:bulgaria", ["pl:bulgaria", "pl:serbia"], "Bulgaria joined the Central Powers")
e("ev:macedonian-front", "חזית סלוניקי", "Macedonian front", "1915-10-05", "1918-09-30",
  "top:wwi-balkan-fronts", "pl:thessaloniki", ["pl:france", "pl:united-kingdom", "pl:serbia", "pl:greece", "pl:bulgaria", "pl:germany"], "Allied front based at Salonica", ["Salonika front"])
e("ev:national-schism", "הפילוג הלאומי ביוון וממשלת סלוניקי", "National Schism", "1916-08", "1917-06",
  "top:wwi-balkan-fronts", "pl:thessaloniki", ["pl:greece"], "split between King Constantine and Venizelos' government in Salonica")
e("ev:romania-enters-wwi", "כניסת רומניה למלחמה והמערכה הרומנית", "Romanian campaign (1916)", "1916-08-27", "1916-12",
  "top:wwi-balkan-fronts", "pl:romania", ["pl:romania", "pl:germany", "pl:austria-hungary", "pl:bulgaria"], "Romania's entry into the war and the Central Powers' counter-offensive", ["Romania in World War I"])
e("ev:unrestricted-submarine-warfare-1917", "מלחמת הצוללות הבלתי מוגבלת", "Unrestricted submarine warfare", "1917-02-01", None,
  "top:wwi-naval-air-war", None, ["pl:germany", "pl:united-kingdom"], "German declaration of unrestricted U-boat warfare", ["U-boat campaign (World War I)"])
e("ev:us-entry-wwi", "כניסת ארה\"ב למלחמה", "American entry into World War I", "1917-04-06", None,
  "top:wwi-outbreak-diplomacy", "pl:united-states", ["pl:united-states", "pl:germany"], "US declaration of war on Germany")
e("ev:jaffa-deportation-1917", "גירוש תל אביב ויפו", "1917 Jaffa deportation", "1917-04-06", None,
  "top:wwi-jews", "pl:ottoman-palestine", ["pl:ottoman-empire"], "Ottoman expulsion of the civilian population of Jaffa and Tel Aviv")
e("ev:jewish-legion", "הגדוד העברי", "Jewish Legion", "1917-08", None,
  "top:wwi-jews", None, ["pl:united-kingdom"], "Jewish battalions of the British army")
e("ev:balfour-declaration", "הצהרת בלפור", "Balfour Declaration", "1917-11-02", None,
  "top:zionist-movement", "pl:united-kingdom", ["pl:united-kingdom"], "British declaration supporting a Jewish national home in Palestine")

# Jewish / Zionist
e("ev:tenth-zionist-congress", "הקונגרס הציוני העשירי", "10th Zionist Congress", "1911-08-09", "1911-08-15",
  "top:zionist-movement", None, [], "Zionist Congress in Basel")
e("ev:galveston-movement", "תוכנית גלווסטון", "Galveston Movement", "1907", "1914",
  "top:jewish-emigration-americas", "pl:united-states", ["pl:united-states"], "scheme diverting Jewish immigrants to Galveston, Texas")
e("ev:aliens-act-1905", "חוק הזרים הבריטי", "Aliens Act 1905", "1905-08-11", None,
  "top:immigration-restrictions", "pl:united-kingdom", ["pl:united-kingdom"], "British law restricting immigration, aimed largely at East European Jews")
e("ev:war-of-the-languages", "מלחמת השפות (פרשת הטכניון)", "War of the Languages", "1913-10", "1914-02",
  "top:jewish-languages", "pl:ottoman-palestine", ["pl:ottoman-palestine"], "conflict over German vs Hebrew as language of instruction at the Technion", ["Language war"])

# European domestic
e("ev:french-separation-law-1905", "חוק הפרדת הדת והמדינה בצרפת", "1905 French law on the Separation of the Churches and the State", "1905-12-09", None,
  "top:church-state-france", "pl:france", ["pl:france"], "law separating church and state in France")
e("ev:norway-sweden-dissolution", "פירוק האיחוד בין נורווגיה לשוודיה", "Dissolution of the union between Norway and Sweden", "1905-06-07", None,
  "top:smaller-european-states", None, [], "Norway's separation from Sweden")
e("ev:hungarian-crisis-1905", "המשבר ההונגרי 1905–1906", "Hungarian crisis of 1905–1906", "1905", "1906-04",
  "top:austro-hungarian-domestic-politics", "pl:austria-hungary", ["pl:austria-hungary"], "constitutional crisis between Hungarian coalition and the Crown; universal suffrage debate")
e("ev:cisleithanian-election-1907", "הבחירות באוסטריה 1907 (זכות בחירה כללית)", "1907 Cisleithanian legislative election", "1907-05-14", None,
  "top:austro-hungarian-domestic-politics", "pl:austria-hungary", ["pl:austria-hungary"], "first Austrian election under universal male suffrage")
e("ev:german-election-1907", "בחירות 'ההוטנטוטים' לרייכסטאג 1907", "1907 German federal election", "1907-01-25", None,
  "top:german-domestic-politics", "pl:germany", ["pl:germany"], "Reichstag election fought over colonial policy")
e("ev:german-election-1912", "הבחירות לרייכסטאג 1912", "1912 German federal election", "1912-01-12", None,
  "top:german-domestic-politics", "pl:germany", ["pl:germany"], "SPD became largest party; antisemitic parties defeated")
e("ev:peoples-budget", "תקציב העם ומשבר בית הלורדים", "People's Budget", "1909-04-29", "1910-04",
  "top:british-domestic-politics", "pl:united-kingdom", ["pl:united-kingdom"], "Lloyd George budget and constitutional crisis")
e("ev:lisbon-regicide", "רצח מלך פורטוגל", "Lisbon Regicide", "1908-02-01", None,
  "top:iberian-politics", None, [], "assassination of King Carlos I of Portugal and his heir")
e("ev:portuguese-revolution-1910", "המהפכה בפורטוגל", "5 October 1910 revolution", "1910-10-05", None,
  "top:iberian-politics", None, [], "overthrow of the Portuguese monarchy and proclamation of the republic")
e("ev:french-railway-strike-1910", "שביתת הרכבות בצרפת", "1910 French railway strike", "1910-10-10", "1910-10-18",
  "top:labour-strikes", "pl:france", ["pl:france"], "railway strike broken by Briand's mobilization of workers")
e("ev:british-railway-strike-1911", "שביתת הרכבות באנגליה 1911", "National railway strike of 1911", "1911-08-17", "1911-08-19",
  "top:labour-strikes", "pl:united-kingdom", ["pl:united-kingdom"], "first national railway strike in Britain amid the Great Unrest", ["Great Unrest"])
e("ev:belfast-strike-1907", "שביתת הנמל והשוטרים בבלפסט", "1907 Belfast Dock strike", "1907-05", "1907-08",
  "top:labour-strikes", "pl:united-kingdom", ["pl:united-kingdom"], "dock strike in Belfast that drew in police mutiny")
e("ev:stuttgart-congress-1907", "הקונגרס הסוציאליסטי הבינלאומי בשטוטגרט", "Stuttgart International Socialist Congress (1907)", "1907-08-18", "1907-08-24",
  "top:socialism", "pl:germany", ["pl:germany"], "Second International congress on militarism and colonialism", ["International Socialist Congress, Stuttgart 1907"])
e("ev:marconi-scandal", "פרשת מרקוני", "Marconi scandal", "1912", "1913",
  "top:corruption-scandals", "pl:united-kingdom", ["pl:united-kingdom"], "insider-trading scandal involving British ministers incl. Herbert Samuel")

# Disasters / science
e("ev:courrieres-mine-disaster", "אסון המכרה בקורייר", "Courrières mine disaster", "1906-03-10", None,
  "top:accidents", "pl:france", ["pl:france"], "Europe's worst mining disaster")
e("ev:messina-earthquake", "רעידת האדמה במסינה", "1908 Messina earthquake", "1908-12-28", None,
  "top:natural-disasters", "pl:italy", ["pl:italy"], "earthquake and tsunami destroying Messina and Reggio")
e("ev:sinking-of-titanic", "טביעת הטיטניק", "Sinking of the Titanic", "1912-04-15", None,
  "top:accidents", None, ["pl:united-kingdom", "pl:united-states"], "sinking of RMS Titanic", ["Titanic"])
e("ev:paris-madrid-air-race", "תחרות הטיסה פריז–מדריד ומות שר המלחמה ברטו", "1911 Paris to Madrid air race", "1911-05-21", "1911-05-26",
  "top:aviation", "pl:france", ["pl:france", "pl:spain"], "air race whose start crash killed French war minister Maurice Berteaux")
e("ev:halleys-comet-1910", "הופעת שביט האלי", "Halley's Comet", "1910-05", None,
  "top:science-archaeology", None, [], "1910 apparition of Halley's Comet")
e("ev:sixth-cholera-pandemic", "מגפת הכולרה (1899–1923)", "1899–1923 cholera pandemic", "1899", "1923",
  "top:epidemics", None, ["pl:russian-empire", "pl:ottoman-empire", "pl:italy"], "sixth cholera pandemic; major outbreaks in Russia 1908–1910 and among Ottoman troops 1911–1913", ["Sixth cholera pandemic"])
e("ev:brussels-exposition-1910", "התערוכה העולמית בבריסל", "Brussels International Exposition (1910)", "1910-04-23", "1910-11-01",
  "top:arts-entertainment", None, [], "world's fair in Brussels")

data = {"concepts": C, "events": E}

# ---- validation ----
ids = [x["id"] for x in C] + [x["id"] for x in E]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
pat = re.compile(r"^(top|ev):[a-z0-9-]+$")
bad = [i for i in ids if not pat.match(i)]
assert not bad, bad
cid = {x["id"]: x for x in C}
for x in C:
    if x["broader"] is not None:
        assert x["broader"] in cid, (x["id"], x["broader"])
    for r in x["related"]:
        assert r.startswith("pl:") or r in cid, (x["id"], r)
    assert x["scope"] and x["he"] and x["en"]
for x in E:
    assert x["broader"] in cid, (x["id"], x["broader"])
    assert re.match(r"^\d{4}(-\d{2}(-\d{2})?)?$", x["date"]), x
    assert x["end"] is None or re.match(r"^\d{4}(-\d{2}(-\d{2})?)?$", x["end"]), x
PL = set("pl:morocco pl:france pl:germany pl:russian-empire pl:ottoman-empire pl:united-kingdom pl:spain pl:italy pl:austria-hungary pl:united-states pl:persia pl:japan pl:china pl:greece pl:bulgaria pl:serbia pl:romania pl:montenegro pl:albania pl:egypt pl:algeria pl:libya pl:ottoman-palestine pl:syria pl:fez pl:casablanca pl:tangier pl:agadir pl:marrakesh pl:thessaloniki pl:damascus pl:istanbul pl:saint-petersburg pl:kiev pl:warsaw pl:macedonia pl:crete pl:tripolitania pl:balkans".split())
for x in C:
    for r in x["related"]:
        if r.startswith("pl:"): assert r in PL, r
for x in E:
    assert x["place"] is None or x["place"] in PL, x["place"]
    for p in x["participants"]: assert p in PL, p
# cycles & depth
def depth(i, seen=()):
    b = cid[i]["broader"]
    assert i not in seen, "cycle " + i
    return 1 if b is None else 1 + depth(b, seen + (i,))
dmax = max(depth(i) for i in cid)
assert dmax <= 3
top = [x for x in C if x["broader"] is None]
print("top-level", len(top), "narrower", len(C) - len(top), "events", len(E), "max depth", dmax)
print("level3:", [i for i in cid if depth(i) == 3])
ens = [x["en"] for x in E]
dup = {n for n in ens if ens.count(n) > 1}
print("duplicate en:", dup)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
