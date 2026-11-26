# part 2 (exec'd after build.py)
E('alexei-polivanov', 'אלכסיי פוליבנוב', 'Alexei Polivanov', 'Russian general, deputy war minister, war minister 1915–1916', 'general', RU, [206])
E('joseph-pulitzer', "ג'וזף פוליצר", 'Joseph Pulitzer', 'American newspaper publisher, endowed the Columbia School of Journalism', 'publisher', 'pl:united-states', [209])
E('yehiel-michel-pines', 'יחיאל מיכל פינס', 'Yehiel Michel Pines', 'Jerusalem rabbi, writer and Hovevei Zion activist (died 1913)', 'rabbi', 'pl:ottoman-palestine', [252])
E('nikolay-karabchevsky', "ניקולאי קרבצ'בסקי", 'Nikolay Karabchevsky', 'Prominent Russian defence lawyer', 'lawyer', RU, [513])
E('raphael-aaron-ben-simon', 'רפאל אהרן בן שמעון', 'Raphael Aaron ben Simon', 'Chief Rabbi (Hakham Bashi) of Cairo 1891–1921', 'rabbi', 'pl:egypt', [756])
E('akiba-rubinstein', 'עקיבא רובינשטיין', 'Akiba Rubinstein', 'Polish-Jewish chess grandmaster', 'chess player', 'pl:poland', [])
E('rudolf-spielmann', 'רודולף שפילמן', 'Rudolf Spielmann', 'Austrian-Jewish chess master', 'chess player', AT, [764])
E('carl-schlechter', 'קרל שלכטר', 'Carl Schlechter', 'Austrian chess master', 'chess player', AT, [750])

PAP = {'hyt': 'Haynt', 'dfr': 'Der Fraynd', 'unzerleben': 'Unzer Leben'}
def where(k):
    a = ART[K[k]][0]
    p = next((v for kk, v in PAP.items() if a.startswith(kk)), '?')
    return p, DATE[a][:7]
def O(k, slug, en, ctx, kind='person', country=None, more=(), he=None):
    p, d = where(k)
    E(slug, he or rows[k-1][1], en, f'{ctx} (mentioned in {p}, {d})', kind, country, [k] + list(more))
FIC = 'fictional character'
GR, BG, PL, PAL, CN = 'pl:greece', 'pl:bulgaria', 'pl:poland', 'pl:ottoman-palestine', 'pl:china'
TG = 'person in Russian telegram news'
SM = "character in Sholem Aleichem's epistolary novel Marienbad"
TK = 'character in the serialized historical novel "The Tyrant King" (Second Temple period)'
BW = 'character in the serialized Hasmonean novel "The Bloody War"'
WR = 'Warsaw rabbi, signatory of a 1910 kashrut proclamation'
DIP = 'historical Jewish figure named in an article on Jews in diplomatic service'
L = [
 (4, 'saladovkin-1911', 'Saladovkin', TG, 'person', RU), (5, 'slavinsky-1911', 'Slavinsky', TG, 'person', RU),
 (7, 'salazkin-1911', 'Salazkin', TG, 'person', RU), (9, 'slutskin-1913', 'Slutskin', 'person in a Jewish news item'),
 (10, 'kastan-saltyk', 'Kastan Saltyk', 'figure in an 18th-century blood-libel trial at Pavolitch (essay by M. D. Rivkin)', 'person', 'pl:ukraine'),
 (12, 'sheikh-salim-1911', 'Sheikh Salim', 'sheikh in 1911 telegram news'),
 (17, 'george-samuel-diplomat', 'George Samuel', DIP), (20, 'samokhvalov-1906', 'Samokhvalov', TG, 'person', RU),
 (22, 'samoilov-1911', 'Samoilov', TG, 'person', RU), (23, 'general-semashkevich', 'Semashkevich', 'Russian general', 'general', RU),
 (27, 'senshikov-1911', 'Senshikov', 'person in a report on the outbreak of the Italo-Turkish war'),
 (29, 'l-spirin', 'L. Spirin', 'correspondent writing on the Italo-Ottoman war in Tripoli', 'journalist'),
 (32, 'count-spanaki', 'Count Spanaki', 'count involved in the 1910 Ungern-Sternberg espionage affair', 'person', RU),
 (33, 'hanna-spektor', 'Hanna Spektor', 'person named in Haynt headlines'),
 (39, 'scanazzo', 'Scanazzo', DIP), (40, 'skopinsky-1911', 'Skopinsky', TG, 'person', RU),
 (41, 'alexander-skinas', 'Alexander Skinas', 'Greek figure in Salonica after the Greek takeover', 'person', GR),
 (42, 'skiryatin', 'Skiryatin', 'person in Russian Duma news', 'person', RU),
 (47, 'esther-sraker', 'Esther Sraker', SM, FIC), (48, 'chaim-sraker', 'Chaim Sraker', SM, FIC, None, [57]),
 (53, 'sergeyev-1911', 'Sergeyev', TG, 'person', RU), (54, 'sergeyevich-1910', 'Sergeyevich', TG, 'person', RU),
 (55, 'srednitsky-1911', 'Srednitsky', 'person in the Vonlyarlyarsky will trial', 'person', RU),
 (56, 'vice-admiral-sarnovsky', 'Sarnovsky', 'vice-admiral named in telegram news', 'admiral', RU),
 (58, 'mulla-mustafa-asim', 'Mulla Mustafa Asim', 'Muslim cleric in the April 1909 Ottoman counter-revolution', 'cleric', OT),
 (61, 'eblangan', 'Eblangan', 'person named in a historical survey of the Jews of Greece', 'person', GR),
 (62, 'abd-al-sadek-bey', 'Abd al-Sadek Bey', 'figure in 1907 telegram news'),
 (63, 'shlomo-ehrlich-rabbi', 'Shlomo Ehrlich', WR, 'rabbi', PL), (70, 'ettinger-1905', 'Ettinger', 'person in 1905 telegram news'),
 (72, 'hajj-ben-aissa', 'Hajj ben Aissa', 'pasha (governor) of Fez, arrested and tortured by Sultan Abd al-Hafid in 1910', 'pasha', MA, [105]),
 (80, 'elen-fictional', 'Elen', TK, FIC), (82, 'rabbi-amram-1910', 'Rabbi Amram', 'person in short Jewish news items', 'rabbi'),
 (83, 'moshe-ben-yehuda-arabi', 'Moshe ben Yehuda Arabi', DIP),
 (88, 'bishop-pavel-1911', 'Bishop Pavel', 'Russian Orthodox bishop', 'bishop', RU),
 (89, 'captain-faber-mp', 'Captain Faber', 'British MP who revealed "secrets" of the 1911 Morocco crisis', 'politician', GB),
 (90, 'frant-pauliak', 'Frant Pauliak', 'person linked to the Kulyabko affair in Kiev', 'person', RU),
 (91, 'payer-1905', 'Payer', 'person in a French Senate debate on the Russo-Japanese war', 'person', FR),
 (103, 'faneuil-1910', 'Faneuil', 'person in a report on a Jewish agricultural colony for refugees from Russia'),
 (107, 'popovitsky-1911', 'Popovitsky', 'person in the Vonlyarlyarsky will trial', 'person', RU),
 (109, 'parker-1911', 'Parker', 'person in 1911 telegram news'),
 (110, 'ibrahim-pasha-1909', 'Ibrahim Pasha', 'Ottoman pasha in the April 1909 crisis', 'pasha', OT),
 (113, 'ismail-pasha-1908', 'Ismail Pasha', 'Ottoman general close to Sultan Abdul Hamid II', 'general', OT),
 (119, 'dietfurt-pasha', 'Dietfurt Pasha', 'pasha at the first selamlik of Mehmed V, 1909', 'pasha', OT),
 (122, 'hamdi-pasha-1910', 'Hamdi Pasha', 'Ottoman pasha named in news of Jews abroad', 'pasha', OT),
 (133, 'nabi-pasha-1913', 'Nabi Pasha', 'Ottoman official during the 1913 London peace negotiations', 'pasha', OT),
 (135, 'saadun-pasha', 'Saadun Pasha', 'pasha named in Balkan-war telegrams', 'pasha', OT),
 (137, 'abdul-pasha-1911', 'Abdul Pasha', 'pasha named in 1911 telegram news', 'pasha', OT),
 (138, 'ali-saib-pasha', 'Ali Saib Pasha', 'Ottoman pasha mentioned in a comparison of Abdul Hamid and Mehmed V', 'pasha', OT),
 (141, 'fuad-pasha-1908', 'Fuad Pasha', 'Ottoman pasha mentioned after the 1908 Young Turk revolution', 'pasha', OT),
 (145, 'rauf-pasha-1909', 'Rauf Pasha', 'Ottoman pasha in the April 1909 events', 'pasha', OT),
 (146, 'herzog-abba-pasha', 'Herzog Abba Pasha', 'pasha named in 1913 Balkan-war telegrams', 'pasha'),
 (147, 'resid-pasha-1913', 'Reşid Pasha', 'Ottoman delegate at the 1913 London peace talks', 'pasha', OT),
 (155, 'abu-fuad-pasha', 'Abu Fuad Pasha', 'Ottoman pasha in the April 1909 counter-revolution', 'pasha', OT),
 (162, 'zihni-pasha', 'Zihni Pasha', 'Ottoman pasha in the April 1909 counter-revolution', 'pasha', OT),
 (167, 'yusuf-pasha-1909', 'Yusuf Pasha', 'Ottoman official in charge of the deposed Abdul Hamid in Salonica', 'pasha', OT),
 (174, 'osman-pasha-1909', 'Osman Pasha', 'Ottoman pasha in the April 1909 crisis', 'pasha', OT),
 (180, 'rushdi-pasha-1909', 'Rushdi Pasha', 'Ottoman pasha in 1909 telegram news', 'pasha', OT),
 (186, 'shneor-rabbi-of-pavolitch', 'Shneor of Pavolitch', 'rabbi of Pavolitch in an 18th-century blood-libel trial', 'rabbi', 'pl:ukraine'),
 (187, 'pavlov-brothers-1907', 'Pavlov brothers', 'brothers sentenced to death, case raised in the Duma 1907', 'person', RU),
 (188, 'pavlov-1910', 'Pavlov', TG, 'person', RU),
 (191, 'pavlovsky-1914', 'Pavlovsky', "person in a Jewish traveller's report on returning to Russia in 1914"),
 (192, 'pagina-fictional', 'Pagina', BW, FIC), (193, 'podgorodnikov', 'Podgorodnikov', 'person in Duma news', 'person', RU),
 (195, 'cardinal-fusina', 'Cardinal Fusina', 'Catholic cardinal in 1911 telegram news', 'cardinal'),
 (196, 'count-potocki-1911', 'Count Potocki', 'Polish count in 1911 telegram news', 'person', RU),
 (197, 'poyakov', 'Poyakov', 'person in 1907 telegram news'),
 (198, 'moshe-hirsch-fuchs', 'Moshe Hirsch Fuchs', WR, 'rabbi', PL), (199, 'polan-1910', 'Polan', 'person in 1910 telegram news'),
 (200, 'maram-fuld', 'Maram Fuld', 'visitor at Marienbad Zionist gatherings, 1910'),
 (201, 'moshe-poliak-minsk', 'Moshe Poliak', 'Minsk burial-society figure in a 1905 cemetery scandal', 'person', RU),
 (202, 'poliak-1906', 'Poliak', 'person in a report on Jewish emigrants passing through Holland'),
 (203, 'shmuel-poliakov-1911', 'Shmuel Poliakov', TG, 'person', RU),
 (208, 'shmuel-polinkovsky', 'Shmuel Polinkovsky', 'Odessa Jewish resident in local war-time news', 'person', RU),
 (210, 'captain-postnikov', 'Postnikov', 'Russian captain in 1911 telegram news', 'officer', RU, [285, 286]),
 (211, 'pusterin', 'Pusterin', TG, 'person', RU), (212, 'popovic-1913', 'Popović', 'Serbian figure in Balkan-war telegrams', 'person', 'pl:serbia'),
 (213, 'alfred-fox', 'Alfred Fox', 'person in Haynt "four corners of the world" news'),
 (214, 'pokrovsky-duma', 'Pokrovsky', 'Russian Duma figure', 'person', RU),
 (216, 'porchevsky', 'Porchevsky', 'Duma figure in a 1909 debate on religious freedom', 'person', RU),
 (220, 'count-fornek', 'Count Fornek', 'count in 1911 telegram news'), (222, 'pourchot', 'Pourchot', 'person in 1912 French news telegrams', 'person', FR),
 (225, 'ivan-pushkov', 'Ivan Pushkov', 'prisoner named in a history of the Peter and Paul Fortress', 'person', RU),
 (228, 'engineer-petrov-1911', 'Petrov', 'engineer in Haynt latest news', 'engineer', RU), (229, 'petrov-1910', 'Petrov', TG, 'person', RU),
 (231, 'paterno-1912', 'Paterno', 'person in 1912 telegram news'), (233, 'j-petraki', 'J. Petraki', 'person in Odessa local news, 1914', 'person', RU),
 (234, 'feorov', 'Feorov', 'person in short Jewish news items', 'person', RU),
 (240, 'engineer-fioran', 'Fioran', 'engineer in 1909 telegram news', 'engineer'), (242, 'pilos-fictional', 'Pilos', BW, FIC),
 (243, 'admiral-philibert', 'Admiral Philibert', 'French admiral commanding the naval division at Casablanca 1907', 'admiral', FR),
 (244, 'philip-1911', 'Philip', 'person in 1911 telegram news'), (245, 'filippov-1906', 'Filippov', TG, 'person', RU),
 (246, 'philippson-historian', 'Philippson', 'author cited in a historical survey of the Jews of Greece', 'historian'),
 (247, 'zislauer-piletsky', 'Zislauer Piletsky', TG, 'person', RU),
 (248, 'pinald', 'Pinald', 'person in news from Palestine (Anglo-Palestine Bank)', 'person', PAL),
 (249, 'feinberg-1913', 'Feinberg', 'person in 1913 news', 'person', RU), (250, 'pine-1911', 'Pine', 'person in 1911 telegram news'),
 (251, 'finya', 'Finya', 'person in a travel diary of the Jewish colonies in Palestine', 'person', PAL),
 (253, 'n-finkelstein', 'N. Finkelstein', 'person in Haynt Jewish news, 1912'),
 (254, 's-finkelstein', 'S. Finkelstein', 'participant in a 1912 territorialist conference'),
 (255, 'fisterman', 'Fisterman', TG, 'person', RU),
 (258, 'dr-pikholz', 'Dr. Pikholz', 'physician in Palestine at the start of WWI', 'physician', PAL),
 (261, 'pierson-1907', 'Pierson', 'delegate at the 1907 socialist congress'), (265, 'fischel-1911', 'Fischel', TG, 'person', RU),
 (267, 'feldstein-1910', 'Feldstein', 'participant in a Jewish national assembly at Karlsbad, 1910'),
 (269, 'bishop-platon-1907', 'Bishop Platon', 'Russian Orthodox bishop', 'bishop', RU), (270, 'platonov-1912', 'Platonov', TG, 'person', RU),
 (273, 'feliksman', 'Feliksman', TG, 'person', RU), (275, 'dr-planimsky', 'Dr. Planimsky', 'person in 1913 telegram news'),
 (277, 'aharon-feller', 'Aharon Feller', 'Jew named in reports on Turkey after the 1909 counter-revolution', 'person', OT),
 (278, 'l-pameron', 'L. Pameron', 'author of a Paris article on French rule in the Congo', 'journalist'),
 (280, 'dr-fanelstein', 'Dr. Fanelstein', TG, 'person', RU), (281, 'panchenko-1911', 'Panchenko', TG, 'person', RU),
 (282, 'hefner-1917', 'Hefner', 'person in March 1917 news', 'person', RU),
 (293, 'david-frasco', 'David Frasco', 'Ottoman Jew accused of informing under Abdul Hamid', 'person', OT),
 (296, 'ferdin-bey', 'Ferdin Bey', 'figure in WWI telegrams, October 1914'),
 (303, 'frohlich-1911', 'Fröhlich', 'person in 1911 telegram news'), (304, 'prufi-1911', 'Prufi', 'person in 1911 telegram news'),
 (307, 'commander-perron', 'Commander Perron', 'French officer in a 1910 clash on the Moroccan border', 'officer', FR),
 (308, 'prokofiev-1911', 'Prokofiev', TG, 'person', RU), (309, 'leonid-pratiasnikov', 'Leonid Pratiasnikov', TG, 'person', RU),
 (311, 'pariapolsky', 'Pariapolsky', TG, 'person', RU), (312, 'aharon-friedman-1909', 'Aharon Friedman', 'person in 1909 telegram news', 'person', RU),
 (313, 'friedman-1912', 'Friedman', 'person named in Haynt headlines'), (315, 'fereid-1913', 'Fereid', 'person in Balkan-crisis telegrams'),
 (316, 'fraser-1911', 'Fraser', 'person in a 1911 press survey'), (319, 'primavesi', 'Primavesi', 'person in Balkan-crisis telegrams, 1913'),
 (320, 'frisch-1905', 'Frisch', TG, 'person', RU), (325, 'pernikov', 'Pernikov', 'Jewish soldier decorated in WWI', 'soldier', RU),
 (326, 'yitzhak-fernandez', 'Yitzhak Fernandez', 'Ottoman Jew, brother of Shalom Fernandez', 'person', OT),
 (327, 'shalom-fernandez', 'Shalom Fernandez', 'Ottoman Jew, brother of Yitzhak Fernandez', 'person', OT),
 (329, 'maximilian-frankowski', 'Maximilian Frankowski', TG, 'person', RU),
 (330, 'david-frenkel-1911', 'David Frenkel', 'person in Haynt latest news', 'person', RU),
 (342, 'general-chang-1911', 'General Chang', 'Chinese general during the 1911 revolution', 'general', CN),
 (343, 'chava-tshapnik', 'Chava Tshapnik', SM, FIC), (345, 'tsvion-fictional', 'Tsvion', TK, FIC),
 (346, 'tsivarov', 'Tsivarov', 'person in Odessa local news, 1914', 'person', RU),
 (350, 'prince-chen-bei-tsu', 'Prince Chen-bei-tsu', 'Chinese prince in 1911 telegram news', 'prince', CN),
 (351, 'lushan-tsuan', 'Lushan Tsuan', 'person in 1911 telegram news', 'person', CN), (352, 'tsukhavsky', 'Tsukhavsky', TG, 'person', RU),
 (353, 'menachem-zweiback', 'Menachem Zweiback', 'visitor at Marienbad Zionist gatherings, 1910'),
 (355, 'p-zuckerman', 'P. Zuckerman', 'person in 1915 news on Jewish relief committees'),
 (356, 'tsekhanovsky', 'Tsekhanovsky', 'person in March 1917 news', 'person', RU), (357, 'tsizum-fictional', 'Tsizum', BW, FIC),
 (358, 'p-tsizik', 'P. Tsizik', 'person in Haynt news', 'person', RU),
 (361, 'chilingirov', 'Chilingirov', 'Bulgarian figure in Balkan-war telegrams', 'person', BG),
 (362, 'pinchas-zimetbaum', 'Pinchas Zimetbaum', WR, 'rabbi', PL), (363, 'm-zimmerman', 'M. Zimmerman', 'person in Haynt announcements', 'person', PL),
 (365, 'a-tsiklim', 'A. Tsiklim', 'person in Odessa local news, 1914', 'person', RU), (366, 'chelishchev', 'Chelishchev', 'person in Russian news', 'person', RU),
 (369, 'tsiporit-fictional', 'Tsiporit', BW, FIC), (371, 'chkilov', 'Chkilov', TG, 'person', RU),
 (378, 'alphonse-k', 'Alphonse K.', 'person in Haynt news'), (379, 'kadir-1905', 'Kadir', 'person in 1905 telegram news'),
 (380, 'kahn-1912', 'Kahn', 'person in Haynt short news'), (381, 'hugo-kaufmann', 'Hugo Kaufmann', 'Jew of Cologne in news of Jews abroad', 'person', DE),
 (382, 'anna-kaufman', 'Anna Kaufman', 'person in short Jewish news items'), (383, 'friedrich-kaufman', 'Friedrich Kaufman', 'person in short Jewish news items'),
 (385, 'baron-korff-1910', 'Baron Korff', 'Russian baron at a Kremlin ceremony, 1910', 'person', RU),
 (386, 'kozlov-1905', 'Kozlov', TG, 'person', RU), (387, 'ivan-kazimirovich', 'Ivan Kazimirovich', 'character in a serialized travel story', FIC),
 (388, 'kotlov-brothers', 'Kotlov brothers', 'brothers in a Moscow court case, 1906', 'person', RU),
 (389, 'prof-katkov', 'Prof. Katkov', 'Odessa professor in 1914 local news', 'professor', RU),
 (392, 'captain-cagliera', 'Captain Cagliera', 'captain in 1911 telegram news', 'officer'),
 (393, 'shmuel-kalish', 'Shmuel Kalish', TG, 'person', RU), (394, 'kamp-1911', 'Kamp', 'person in Haynt latest news'),
 (395, 'kaneman', 'Kaneman', 'person in 1910 telegram news'),
 (397, 'ben-abia-kasia', 'Ben Abia Kasia', 'Moroccan figure in a 1907 letter of Raisuni', 'person', MA),
 (399, 'abba-kasiri', 'Abba Kasiri', 'rabbi of the Jewish community in Egypt', 'rabbi', 'pl:egypt'),
 (404, 'baron-korff-1906', 'Baron Korff', 'Russian baron in 1906 telegram news', 'person', RU),
 (405, 'jan-marceli-kabushevsky', 'Jan Marceli Kabushevsky', TG, 'person', RU),
 (406, 'p-kabilinsky', 'P. Kabilinsky', 'Russian public figure', 'person', RU, [407]),
 (409, 'costa-cabral-1907', 'Costa Cabral', 'Portuguese politician in 1907 news', 'politician', 'pl:portugal'),
 (410, 'captain-kugel', 'Captain Kugel', 'officer in November 1917 Russian telegrams', 'officer', RU),
 (411, 'kvelch', 'Kvelch', 'delegate at the 1907 Hague Peace Conference'), (412, 'kuzminsky-1906', 'Kuzminsky', 'Russian official in 1906 news', 'person', RU),
 (413, 'kuznetsov-1911', 'Kuznetsov', TG, 'person', RU), (414, 'count-kutaisov', 'Count Kutaisov', 'Russian count in 1911 news', 'person', RU),
 (415, 'kutner', 'Kutner', 'person in Haynt "four corners of the world" news'), (416, 'emilio-frank-coizia', 'Emilio Frank Coizia', 'person in 1910 short news'),
 (420, 'kolchinsky', 'Kolchinsky', TG, 'person', RU), (424, 'kahn-1911', 'Kahn', 'person in Haynt "four corners of the world" news'),
 (433, 'konzaoyo', 'Konzaoyo', 'person in 1911 telegram news'), (434, 'kuperman-1913', 'Kuperman', 'person in 1913 telegram news'),
 (437, 'yona-naftali-kuratov', 'Yona Naftali Kuratov', 'Jewish sage (hakham) in Persia', 'rabbi', PE),
 (443, 'courtney-1911', 'Courtney', 'person in 1911 telegram news'),
 (446, 'kurlander-diary', 'the Kurlander', 'worker nicknamed "the Kurlander" in a travel diary of the Palestine colonies', 'person', PAL),
 (447, 'beltsi-kurlender', 'Beltsi Kurlender', SM, FIC), (448, 'shlomo-kurlender', 'Shlomo Kurlender', SM, FIC, None, [449]),
 (450, 'koranda', 'Koranda', 'person in 1911 telegram news'),
 (451, 'general-kornilov-1905', 'General Kornilov', 'Russian general in 1905 war telegrams', 'general', RU),
 (453, 'archbishop-of-corfu-1911', 'Archbishop of Corfu', 'Greek Orthodox archbishop of Corfu appealed to against antisemitic agitation, 1911', 'archbishop', GR),
 (456, 'z-katlyar', 'Z. Katlyar', 'author of a 1905 report on the Jewish poor of Odessa', 'journalist', RU),
 (457, 'kibe', 'Kibe', 'figure in an essay on an 18th-century blood-libel trial'), (459, 'kyuntsen', 'Kyuntsen', 'person in 1907 short news'),
 (461, 'a-m-kaiser', 'A. M. Kaiser', 'correspondent from Palestine, 1912', 'journalist', PAL),
 (463, 'count-keyserling-1907', 'Count Keyserling', 'count in 1907 telegram news', 'person', RU),
 (464, 'yekaterina-kilkevich', 'Yekaterina Kilkevich', TG, 'person', RU), (465, 'kine-1910', 'Kine', 'person in 1910 telegram news'),
 (466, 'admiral-kinsten', 'Admiral Kinsten', 'admiral in 1911 telegram news', 'admiral'),
 (469, 'kirilov-1909', 'Kirilov', TG, 'person', RU), (470, 'z-kirmind', 'Z. Kirmind', 'person in Haynt news', 'person', RU),
 (471, 'kirnosov', 'Kirnosov', TG, 'person', RU), (472, 'klabov', 'Klabov', 'person in 1913 Balkan telegrams'),
 (473, 'dr-s-a-klauzner', 'Dr. S. A. Klauzner', TG, 'person', RU), (476, 'klein-1911', 'Klein', 'person in 1911 telegram news'),
 (478, 'klimovich-1911', 'Klimovich', TG, 'person', RU), (479, 'kalinkov', 'Kalinkov', 'Bulgarian figure in 1913 telegrams', 'person', BG),
 (483, 'z-klenerman', 'Z. Klenerman', 'person in Haynt news', 'person', RU),
 (496, 'markus-kaminer', 'Markus Kaminer', 'contributor listed in Der Fraynd, 1907'),
 (497, 'kamenshchikov', 'Kamenshchikov', 'person in November 1917 Russian telegrams', 'person', RU),
 (498, 'count-komarovsky', 'Count Komarovsky', 'Russian count in 1912 news', 'person', RU), (500, 'kanan-1910', 'Kanan', 'person in Haynt latest news'),
 (501, 'petronella-kaniovna', 'Petronella Kaniovna', 'person in 1912 telegram news', 'person', RU),
 (503, 'kastin-1911', 'Kastin', 'person in 1911 telegram news'),
 (506, 'david-kesselbrenner', 'David Kesselbrenner', 'Odessa Jewish resident in local war-time news', 'person', RU),
 (509, 'rabbi-kaplan-1911', 'Rabbi Kaplan', 'rabbi in 1911 telegram news', 'rabbi'),
 (510, 'kapman-odessa', 'Kapman', 'person in Odessa local news, 1914', 'person', RU), (512, 'katsko', 'Katsko', TG, 'person', RU),
 (514, 'kraus-1910', 'Kraus', 'person in 1910 telegram news'), (515, 'karatky', 'Karatky', TG, 'person', RU),
 (516, 'karaitsu', 'Karaitsu', 'person in 1912 telegram news'), (517, 'august-kramnis', 'August Kramnis', 'person in Haynt "four corners of the world" news'),
 (519, 'a-l-karavaev', 'A. L. Karavaev', 'member of the First Russian Duma', 'politician', RU), (520, 'krebener', 'Krebener', 'person in 1912 telegram news'),
 (521, 'kravchenko-1907', 'Kravchenko', TG, 'person', RU), (523, 'krumensky', 'Krumensky', TG, 'person', RU),
 (526, 'krupi-1911', 'Krupi', 'person in 1911 telegram news'), (528, 'krautsevich', 'Krautsevich', TG, 'person', RU),
 (533, 'karistovsky', 'Karistovsky', 'person in July 1913 Balkan-war telegrams'), (534, 'christie-1911', 'Christie', 'person in 1911 telegram news'),
 (538, 'carlyle-1909', 'Carlyle', 'person in 1909 telegram news'),
 (540, 'general-kremenstein', 'General Kremenstein', 'Russian general in 1915 news', 'general', RU),
 (541, 'm-kremer', 'M. Kremer', 'person named in a Zionist opinion series from Jaffa, 1911'),
 (544, 'dr-korenfeld', 'Dr. Korenfeld', 'person in 1913 telegram news'),
 (547, 'krasovsky-1911', 'Krasovsky', 'Kiev police detective in the Yushchinsky murder investigation', 'detective', RU),
 (548, 'karastovich', 'Karastovich', 'person in 1911 telegram news'),
 (550, 'yuskevich-kraskovsky', 'Yuskevich-Kraskovsky', 'person in Haynt headlines, 1910', 'person', RU),
 (551, 'karsky-1911', 'Karsky', TG, 'person', RU), (552, 'karachin', 'Karachin', 'person in short news', 'person', RU),
 (553, 'mareaus-rabel', 'Mareaus Rabel', 'person in 1910 telegram news'), (554, 'von-raaben', 'von Raaben', 'person in 1906 foreign news'),
 (555, 'radovic-1906', 'Radovic', 'person in 1906 telegram news'), (559, 'shlomo-radziner', 'Shlomo Radziner', WR, 'rabbi', PL),
 (560, 'senator-radilin', 'Senator Radilin', 'Russian senator', 'senator', RU), (561, 'radin-1905', 'Radin', 'person in 1905 French news telegrams'),
 (562, 'reuben-fictional', 'Reuben', TK, FIC), (563, 'ravenfeld', 'Ravenfeld', 'person in 1911 telegram news'),
 (564, 'prince-radziwill-1911', 'Prince Radziwiłł', 'Polish prince in the Vonlyarlyarsky will trial, 1911', 'prince', RU),
 (567, 'meir-hakohen-rapoport', 'Meir HaKohen Rapoport', WR, 'rabbi', PL),
 (568, 's-i-rapoport', 'S. I. Rapoport', 'Russian-Jewish public figure (S. I. Rapoport)', 'person', RU, [669]),
 (570, 'andre-rachefort', 'André Rachefort', 'person in July 1913 Balkan-war telegrams'), (573, 'revutsky', 'Revutsky', TG, 'person', RU),
 (574, 'rabilant', 'Rabilant', 'person involved with the deposed Abdul Hamid in Salonica, 1909'),
 (575, 'eliezer-simcha-rabinovich', 'Eliezer Simcha Rabinovich', TG, 'person', RU), (576, 'rabinovich-1911', 'Rabinovich', TG, 'person', RU),
 (580, 'prince-wilhelm-radziwill', 'Prince Wilhelm Radziwiłł', 'Polish-German prince in 1911 news', 'prince'),
 (581, 'redzinsky', 'Redzinsky', TG, 'person', RU), (585, 'baron-raden', 'Baron Raden', 'baron in 1911 telegram news'),
 (587, 'general-ruanchikoy', 'General Ruanchikoy', 'general in 1911 telegram news', 'general'),
 (591, 'hrubelevsky', 'Hrubelevsky', TG, 'person', RU), (595, 'rouge-1911', 'Rouge', 'person in 1911 telegram news'),
 (601, 'noach-rosenblum', 'Noach Rosenblum', 'person in 1909 telegram news', 'person', RU), (602, 'rosenwasser', 'Rosenwasser', 'person in Haynt news', 'person', RU),
 (607, 'shmuel-rotani', 'Shmuel Rotani', 'person named in a historical survey of the Jews of Greece', 'person', GR),
 (613, 'madame-rothschild-1911', 'Madame Rothschild', 'member of the Rothschild family mentioned in a 1911 Berlin article'),
 (616, 'royer-1910', 'Royer', 'delegate at the 1910 Copenhagen socialist congress', 'socialist'),
 (620, 'signor-rossaretti', 'Signor Rossaretti', 'figure in a humorous feuilleton on the Italo-Turkish war', FIC),
 (623, 'nissim-russo', 'Nissim Russo', 'Salonica Jewish figure', 'person', OT),
 (624, 'vinogradov-diplomat', 'Vinogradov', 'Russian diplomat in 1907 telegrams', 'diplomat', RU),
 (627, 'rushevsky', 'Rushevsky', 'person in WWI telegrams, 1916', 'person', RU),
 (629, 'valentina-rothschild', 'Valentina Rothschild', 'member of the Rothschild family in 1911 news'),
 (631, 'ali-riza-1909', 'Ali Rıza', 'Ottoman figure in the April 1909 counter-revolution', 'person', OT),
 (632, 'razin-minsk', 'Razin', 'figure in the 1905 Minsk cemetery scandal', 'person', RU), (633, 'reznikov', 'Reznikov', TG, 'person', RU),
 (635, 'lima-rias', 'Lima Rias', 'person in 1913 telegram news'),
 (638, 'm-d-rivkin', 'M. D. Rivkin', 'author of a historical essay on an 18th-century blood libel', 'writer', RU),
 (639, 'rivkin-1911', 'Rivkin', 'person in Haynt news', 'person', RU), (640, 'senator-ridzevsky', 'Senator Ridzevsky', 'Russian senator', 'senator', RU),
 (641, 'riedel-1908', 'Riedel', 'person in 1908 telegram news'),
 (650, 'prince-reuss-1913', 'Prince Reuss', 'German prince of the House of Reuss in 1913 Bulgarian news', 'prince'),
 (653, 'engineer-richter', 'Richter', 'engineer in 1911 telegram news', 'engineer'),
 (654, 'prof-richter-1911', 'Prof. Richter', 'professor in 1911 telegram news', 'professor', None, [655, 656]),
 (660, 'relasi', 'Relasi', 'person in 1911 telegram news'),
 (662, 'baron-ren-1912', 'Baron Ren', "baron in a 1912 report on Wilhelm II's Strasbourg speech"),
 (663, 'vasily-renzaov', 'Vasily Renzaov', 'person in Russian news', 'person', RU), (665, 'm-renalsky', 'M. Renalsky', 'person in a Berlin report, 1912'),
 (667, 'de-resselo', 'de Resselo', 'person in 1912 telegram news'), (668, 'yitzhak-rech', 'Yitzhak Rech', 'person in 1911 telegram news'),
 (670, 'rapoport-1912', 'Rapoport', 'person in 1912 telegram news'), (675, 'herakles-fictional', 'Herakles', BW, FIC),
 (680, 'rashinsky', 'Rashinsky', TG, 'person', RU), (682, 'vincenty-reshkevich', 'Wincenty Reshkevich', 'person in Haynt latest news', 'person', RU),
 (688, 'schiller-shaungridze', 'Schiller Shaungridze', TG, 'person', RU), (689, 'shaivich', 'Shaivich', 'person in a 1906 Russian press survey', 'person', RU),
 (690, 'shalit-1910', 'Shalit', 'person in Haynt latest news'), (691, 'schallert', 'Schallert', 'person in 1911 telegram news'),
 (692, 'shang-1911', 'Shang', 'Chinese figure in 1911 telegrams', 'person', CN),
 (694, 'shapsal', 'Shapsal', 'person in 1908 telegrams on the Persian revolution', 'person', PE),
 (695, 'sharapov-1913', 'Sharapov', 'person in 1913 Balkan telegrams'), (696, 'yaakov-shvodt', 'Yaakov Shvodt', DIP),
 (697, 'v-t-sheviakov', 'V. T. Sheviakov', 'Russian official in 1915 news', 'person', RU),
 (698, 'sheviakov-1913', 'Sheviakov', 'person in 1913 Russian telegrams', 'person', RU), (699, 'shablenko', 'Shablenko', TG, 'person', RU),
 (703, 'israel-shdrovitsky', 'Israel Shdrovitsky', 'person in 1910 news', 'person', RU),
 (704, 'count-shuvalov-1913', 'Count Shuvalov', 'Russian count in 1913 telegrams', 'person', RU),
 (705, 'mahmud-shukri-1909', 'Mahmud Shukri', 'Ottoman figure in the April 1909 events', 'person', OT),
 (707, 'shulgait', 'Shulgait', 'person in 1911 telegram news'), (709, 'wladyslaw-szumanski', 'Władysław Szumański', 'person in 1911 telegram news'),
 (711, 'shukov-1911', 'Shukov', 'person in 1911 telegram news'),
 (712, 'prince-shakhovskoy-1913', 'Prince Shakhovskoy', 'Russian prince in 1913 telegrams', 'prince', RU),
 (713, 'general-stalov', 'General Stalov', 'general in 1911 telegram news', 'general'),
 (714, 'kalman-broyl-shtoyhel', 'Kalman Broyl Shtoyhel', 'character in Sholem Aleichem\'s humorous "telegrams"', FIC),
 (715, 'shetah-fictional', 'Shetah', TK, FIC), (716, 'karl-shtetteyer', 'Karl Shtetteyer', 'person in news of Jews abroad, 1910'),
 (718, 'dr-s-steinberg', 'Dr. S. Steinberg', 'person in Haynt latest news', 'person', RU),
 (719, 'steinberg-1913', 'Steinberg', 'person in a 1913 report on Bulgaria'),
 (720, 'chaim-steinhardt', 'Chaim Steinhardt', 'person in 1915 latest news'), (721, 's-steinhardt', 'S. Steinhardt', 'person in 1915 latest news'),
 (722, 'steinfinkel', 'Steinfinkel', TG, 'person', RU), (723, 'general-shatilov', 'General Shatilov', 'Russian general in 1911 telegrams', 'general', RU),
 (724, 'shtiknagold', 'Shtiknagold', 'person in Haynt news', 'person', RU),
 (733, 'baron-ungern-sternberg-1910', 'Baron Ungern-Sternberg', 'Baltic baron arrested in St Petersburg in 1910 on espionage charges', 'person', RU),
 (734, 'sternberg-1911', 'Sternberg', 'person in 1911 telegram news'),
 (735, 'yitzhak-scheinbleum', 'Yitzhak Scheinbleum', 'person in Haynt announcements', 'person', PL),
 (736, 'n-z-shilnin', 'N. Z. Shilnin', 'former member of the First Duma', 'politician', RU), (738, 'shimaze', 'Shimaze', 'person in 1911 telegram news'),
 (747, 'bernard-schechter', 'Bernard Schechter', 'person in 1911 telegram news'), (748, 'schlossberg-1906', 'Schlossberg', 'person in 1906 telegram news'),
 (749, 'schlichting', 'Schlichting', 'person in 1911 telegram news'), (752, 'shembarsky', 'Shembarsky', 'person in Haynt latest news', 'person', RU),
 (753, 'shmuel-fictional', 'Shmuel', TK, FIC), (754, 'tanner-schmidt', 'Tanner-Schmidt', 'person in 1911 telegram news'),
 (757, 'rabbi-shmelkis', 'Rabbi Shmelkis', 'rabbi in 1911 Jewish news', 'rabbi'), (758, 'shimshon-fictional', 'Shimshon', TK, FIC),
 (760, 'schniederman', 'Schniederman', 'person in news on the Italo-Turkish war, 1911'), (761, 'schneider-1916', 'Schneider', 'person in WWI short news, 1916'),
 (762, 'shenkevich-1911', 'Shenkevich', TG, 'person', RU), (765, 'dr-spindel', 'Dr. Spindel', 'visitor at Marienbad Zionist gatherings, 1910', 'physician'),
 (767, 'dr-spiess', 'Dr. Spiess', 'person in 1911 telegram news'), (768, 'zvi-hirsch-shapira-warsaw', 'Zvi Hirsch Shapira', WR, 'rabbi', PL),
 (769, 'm-spektor', 'M. Spektor', 'person in 1908 telegram news', 'person', RU), (771, 'shchingeliev', 'Shchingeliev', TG, 'person', RU),
 (772, 'shchepkin-duma', 'Shchepkin', 'Russian First Duma deputy quoted in a 1906 press survey', 'politician', RU),
 (774, 'shcherbak', 'Shcherbak', 'person in 1908 telegram news', 'person', RU), (775, 'sheran-1907', 'Sheran', 'person in 1907 telegram news'),
 (776, 'schreiner-1910', 'Schreiner', 'person in 1910 telegram news'), (777, 'abdur-alman-sherin', 'Abdur Alman Sherin', 'person in 1911 telegram news'),
 (778, 'sigmund-schringer', 'Sigmund Schringer', 'person in 1911 telegram news'),
 (781, 'david-moshe-talon', 'David-Moshe', 'pen name of a satirical columnist in Unzer Leben', 'columnist', PL),
]
for t in L:
    k, slug, en, ctx = t[:4]
    kind = t[4] if len(t) > 4 else 'person'
    country = t[5] if len(t) > 5 else None
    more = t[6] if len(t) > 6 else ()
    O(k, slug, en, ctx, kind, country, more)

# ---------- contextual ----------
ctx = []
sys.path.insert(0, 'kb/scripts')
from kblib import norm_key, split_item
FULL = {}
for l in open('kb/work/articles.jsonl', encoding='utf-8'):
    a = json.loads(l)
    for x in a['ppl']:
        FULL.setdefault(norm_key(split_item(x)[0]), [])
        if a['id'] not in FULL[norm_key(split_item(x)[0])]: FULL[norm_key(split_item(x)[0])].append(a['id'])
def C(k, f):
    key = K[k]; ctx.append({'key': key, 'articles': {a: f(a, DATE[a]) for a in FULL[key]}})
E('puyi', 'פו-יי', 'Puyi', 'Xuantong Emperor, last emperor of China 1908–1912', 'emperor', CN, [])
KAISER = {'dfr19050702-01.2.4': 'ppl:wilhelm-ii-german-emperor', 'hyt19110712-01.2.14': 'ppl:puyi', 'hyt19110712-01.2.5': None, 'hyt19111026-01.2.5': None}
C(194, lambda a, d: 'ppl:armand-fallieres' if d.startswith('1911') else 'ppl:raymond-poincare')
C(467, lambda a, d: KAISER.get(a, 'ppl:nicholas-ii-of-russia'))
C(492, lambda a, d: {'dfr19050501-01.2.11': 'ppl:paul-cambon', 'dfr19070828-01.2.14': None}.get(a, 'ppl:jules-cambon'))
C(685, lambda a, d: 'ppl:mozaffar-ad-din-shah-qajar' if d < '1907' else 'ppl:mohammad-ali-shah-qajar')
C(671, lambda a, d: 'ppl:abraham-harkavy' if a == 'hyt19110404-01.2.5' else 'ppl:theodor-herzl')
C(101, lambda a, d: 'ppl:konstantin-von-der-pahlen' if d < '1906' else None)
C(219, lambda a, d: 'ppl:francois-ernest-fournier' if d < '1910' else 'ppl:louis-dartige-du-fournet')
C(755, lambda a, d: 'ppl:pyotr-schmidt' if d < '1907' else None)
C(717, lambda a, d: None)
C(590, lambda a, d: 'ppl:akiba-rubinstein' if a in ('hyt19110824-01.2.8', 'hyt19120311-01.2.15') else None)
C(314, lambda a, d: None)
drop = [{'key': K[102], 'why': 'Russian military rank "polkovnik" (colonel) without a name'},
        {'key': K[569], 'why': 'unidentifiable fragment ("ראש") in a telegram list'}]

out = {'entities': ents, 'contextual': ctx, 'drop': drop}
json.dump(out, open('kb/work/ent_ppl_3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
import collections
used = [k for e in ents for k in e['keys']] + [c['key'] for c in ctx] + [d['key'] for d in drop]
print('dups:', [k for k, n in collections.Counter(used).items() if n > 1])
print('missing:', [(i, K[i]) for i in K if K[i] not in set(used)])
print('dup ids:', [i for i, n in collections.Counter(e['id'] for e in ents).items() if n > 1])
print(len(ents), len(ctx), len(drop))
