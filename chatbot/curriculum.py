"""
Language Teaching Curriculum
Covers English (Basic, Intermediate, Advanced) and Samoan (Level 1) modules.
Each level contains topics with explanations, examples, and exercises.
"""

CURRICULUM = {
    "English": {
        "basic": {
        "description": "Perfect for beginners. We'll cover the absolute fundamentals of English.",
        "topics": {
            "alphabet": {
                "title": "The English Alphabet",
                "explanation": (
                    "The English alphabet has 26 letters:\n"
                    "  Vowels (5):   A  E  I  O  U\n"
                    "  Consonants (21): B C D F G H J K L M N P Q R S T V W X Y Z\n\n"
                    "Vowels are special — every syllable in English needs at least one vowel."
                ),
                "examples": [
                    "A as in Apple",
                    "B as in Ball",
                    "C as in Cat",
                    "D as in Dog",
                    "E as in Elephant",
                ],
                "quiz": [
                    {
                        "question": "How many letters are in the English alphabet?",
                        "choices": ["A) 24", "B) 25", "C) 26", "D) 28"],
                        "answer": "C",
                        "explanation": "There are 26 letters in the English alphabet.",
                    },
                    {
                        "question": "Which of the following is a VOWEL?",
                        "choices": ["A) B", "B) C", "C) O", "D) T"],
                        "answer": "C",
                        "explanation": "The vowels are A, E, I, O, U. 'O' is the vowel here.",
                    },
                ],
            },
            "greetings": {
                "title": "Greetings & Introductions",
                "explanation": (
                    "Greetings are how we say hello in English.\n\n"
                    "Formal greetings (used with strangers or in professional settings):\n"
                    "  • Good morning  (used before 12:00 PM)\n"
                    "  • Good afternoon (used 12:00 PM – 6:00 PM)\n"
                    "  • Good evening  (used after 6:00 PM)\n"
                    "  • How do you do? / How are you?\n\n"
                    "Informal greetings (used with friends and family):\n"
                    "  • Hi / Hey\n"
                    "  • What's up?\n"
                    "  • How's it going?\n\n"
                    "Introductions:\n"
                    "  • My name is [name].\n"
                    "  • I am [name]. / I'm [name].\n"
                    "  • Nice to meet you!\n"
                    "  • Pleased to meet you."
                ),
                "examples": [
                    "A: Good morning! My name is Sarah. Nice to meet you.",
                    "B: Good morning, Sarah! I'm John. Pleased to meet you too.",
                    "---",
                    "A: Hey! What's up?",
                    "B: Not much, just relaxing. How about you?",
                ],
                "quiz": [
                    {
                        "question": "Which greeting is appropriate at 9:00 AM?",
                        "choices": [
                            "A) Good evening",
                            "B) Good afternoon",
                            "C) Good morning",
                            "D) Good night",
                        ],
                        "answer": "C",
                        "explanation": "'Good morning' is used before 12:00 PM.",
                    },
                    {
                        "question": "Which phrase introduces yourself formally?",
                        "choices": [
                            "A) What's up?",
                            "B) Hey dude!",
                            "C) My name is Anna.",
                            "D) Yo!",
                        ],
                        "answer": "C",
                        "explanation": "'My name is [name]' is the standard formal self-introduction.",
                    },
                ],
            },
            "numbers": {
                "title": "Numbers (1–100)",
                "explanation": (
                    "Cardinal numbers (counting):\n"
                    "  1=one  2=two  3=three  4=four  5=five\n"
                    "  6=six  7=seven  8=eight  9=nine  10=ten\n"
                    "  11=eleven  12=twelve  13=thirteen  14=fourteen  15=fifteen\n"
                    "  16=sixteen  17=seventeen  18=eighteen  19=nineteen  20=twenty\n"
                    "  21=twenty-one  22=twenty-two … 30=thirty … 40=forty\n"
                    "  50=fifty  60=sixty  70=seventy  80=eighty  90=ninety  100=one hundred\n\n"
                    "Ordinal numbers (position/order):\n"
                    "  1st=first  2nd=second  3rd=third  4th=fourth  5th=fifth\n"
                    "  6th=sixth  7th=seventh  8th=eighth  9th=ninth  10th=tenth"
                ),
                "examples": [
                    "There are 7 days in a week.",
                    "She finished in 1st place.",
                    "I have 25 books on my shelf.",
                    "The 21st century began in the year 2001.",
                ],
                "quiz": [
                    {
                        "question": "How do you write '32' in words?",
                        "choices": [
                            "A) Thirty two",
                            "B) Thirty-two",
                            "C) Three-two",
                            "D) Twentythree",
                        ],
                        "answer": "B",
                        "explanation": "32 is written 'thirty-two' (with a hyphen for 21–99).",
                    },
                    {
                        "question": "What is the ordinal form of 3?",
                        "choices": ["A) Threeth", "B) Third", "C) Thirth", "D) Three"],
                        "answer": "B",
                        "explanation": "The ordinal of 3 is 'third' (irregular form).",
                    },
                ],
            },
            "basic_vocabulary": {
                "title": "Everyday Vocabulary",
                "explanation": (
                    "Here are important everyday English words grouped by category:\n\n"
                    "Colors: red, blue, green, yellow, orange, purple, pink, white, black, brown, grey\n\n"
                    "Days of the week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n\n"
                    "Months: January, February, March, April, May, June,\n"
                    "        July, August, September, October, November, December\n\n"
                    "Common nouns: house, car, book, table, chair, food, water, person, family, friend\n\n"
                    "Common verbs: be, have, do, say, go, get, make, know, think, see, come, want, look, use"
                ),
                "examples": [
                    "The sky is blue.",
                    "Today is Monday.",
                    "My birthday is in July.",
                    "I want to go to the library.",
                    "She has a red car.",
                ],
                "quiz": [
                    {
                        "question": "Which month comes after March?",
                        "choices": ["A) February", "B) May", "C) April", "D) June"],
                        "answer": "C",
                        "explanation": "The order is: … February, March, APRIL, May …",
                    },
                    {
                        "question": "What day comes after Wednesday?",
                        "choices": [
                            "A) Tuesday",
                            "B) Thursday",
                            "C) Friday",
                            "D) Monday",
                        ],
                        "answer": "B",
                        "explanation": "The week order: Mon, Tue, WED, THURSDAY, Fri, Sat, Sun.",
                    },
                ],
            },
            "basic_sentences": {
                "title": "Basic Sentence Structure",
                "explanation": (
                    "The most basic English sentence follows the pattern:\n"
                    "  Subject + Verb + Object  (SVO)\n\n"
                    "  Subject:  who or what does the action\n"
                    "  Verb:     the action or state of being\n"
                    "  Object:   who or what receives the action\n\n"
                    "Common sentence types:\n"
                    "  Statement:  I eat apples.\n"
                    "  Question:   Do you eat apples?\n"
                    "  Negative:   I do not (don't) eat apples.\n"
                    "  Command:    Eat your apples!\n\n"
                    "Important: English sentences always need a subject.\n"
                    "  ✓ It is raining.   ✗ Is raining. (missing subject)"
                ),
                "examples": [
                    "She reads books. (Subject=She, Verb=reads, Object=books)",
                    "The dog chases the cat. (Subject=dog, Verb=chases, Object=cat)",
                    "Do you speak English? (Question form)",
                    "I don't like cold weather. (Negative form)",
                ],
                "quiz": [
                    {
                        "question": "Identify the verb: 'The children play football.'",
                        "choices": [
                            "A) children",
                            "B) play",
                            "C) football",
                            "D) The",
                        ],
                        "answer": "B",
                        "explanation": "'Play' is the action (verb) in this sentence.",
                    },
                    {
                        "question": "Which is the correct negative form?",
                        "choices": [
                            "A) I not like pizza.",
                            "B) I doesn't like pizza.",
                            "C) I don't like pizza.",
                            "D) I no like pizza.",
                        ],
                        "answer": "C",
                        "explanation": "Use 'don't' (do + not) for 'I' in the simple present negative.",
                    },
                ],
            },
        },
    },
    "intermediate": {
        "description": "For learners who know the basics. We'll explore grammar tenses, richer vocabulary, and reading comprehension.",
        "topics": {
            "present_tenses": {
                "title": "Present Tenses",
                "explanation": (
                    "English has four present tenses:\n\n"
                    "1. Simple Present  – habits, facts, general truths\n"
                    "   Formula: Subject + base verb (+ -s/-es for he/she/it)\n"
                    "   Example: She works every day.\n\n"
                    "2. Present Continuous  – actions happening RIGHT NOW or temporary situations\n"
                    "   Formula: Subject + am/is/are + verb-ing\n"
                    "   Example: He is studying at the moment.\n\n"
                    "3. Present Perfect  – past actions with present relevance, life experience\n"
                    "   Formula: Subject + have/has + past participle\n"
                    "   Example: I have visited Paris.\n\n"
                    "4. Present Perfect Continuous – actions that started in past and continue now\n"
                    "   Formula: Subject + have/has + been + verb-ing\n"
                    "   Example: She has been waiting for two hours."
                ),
                "examples": [
                    "Simple:              The Earth orbits the Sun.",
                    "Continuous:          I am reading a novel right now.",
                    "Perfect:             They have already eaten lunch.",
                    "Perfect Continuous:  He has been working here since 2018.",
                ],
                "quiz": [
                    {
                        "question": "Choose the correct tense: 'I _____ English for five years.' (ongoing action)",
                        "choices": [
                            "A) study",
                            "B) am studying",
                            "C) have studied",
                            "D) have been studying",
                        ],
                        "answer": "D",
                        "explanation": "Present Perfect Continuous (have been + -ing) shows an action that started in the past and continues now.",
                    },
                    {
                        "question": "Which sentence uses the Simple Present correctly?",
                        "choices": [
                            "A) She is going to school every day.",
                            "B) She goes to school every day.",
                            "C) She has gone to school every day.",
                            "D) She gone to school every day.",
                        ],
                        "answer": "B",
                        "explanation": "Simple Present uses the base verb (+ s for she/he/it) for habits/routines.",
                    },
                ],
            },
            "past_tenses": {
                "title": "Past Tenses",
                "explanation": (
                    "English has four past tenses:\n\n"
                    "1. Simple Past  – completed action at a specific past time\n"
                    "   Formula: Subject + past verb (regular: +ed; irregular: learn the form)\n"
                    "   Example: She watched a movie last night.\n\n"
                    "2. Past Continuous  – action in progress at a specific past time\n"
                    "   Formula: Subject + was/were + verb-ing\n"
                    "   Example: I was sleeping when the phone rang.\n\n"
                    "3. Past Perfect  – action completed BEFORE another past action\n"
                    "   Formula: Subject + had + past participle\n"
                    "   Example: They had already left when I arrived.\n\n"
                    "4. Past Perfect Continuous – action in progress before another past point\n"
                    "   Formula: Subject + had been + verb-ing\n"
                    "   Example: He had been running for an hour before it started raining."
                ),
                "examples": [
                    "Simple:              We visited Rome in 2019.",
                    "Continuous:          She was cooking dinner at 7 PM.",
                    "Perfect:             By noon, he had finished all his work.",
                    "Perfect Continuous:  They had been waiting for 30 minutes.",
                ],
                "quiz": [
                    {
                        "question": "Which sentence uses the Past Perfect correctly?",
                        "choices": [
                            "A) She has eaten before we arrived.",
                            "B) She had eaten before we arrived.",
                            "C) She ate before we will arrive.",
                            "D) She was eating before we arrived.",
                        ],
                        "answer": "B",
                        "explanation": "Past Perfect (had + past participle) shows one past action happened before another.",
                    },
                    {
                        "question": "'When I called, she ___ a bath.' Which tense fits?",
                        "choices": [
                            "A) took",
                            "B) has taken",
                            "C) was taking",
                            "D) had taken",
                        ],
                        "answer": "C",
                        "explanation": "Past Continuous (was/were + -ing) shows an action in progress when another event occurred.",
                    },
                ],
            },
            "future_tenses": {
                "title": "Future Tenses",
                "explanation": (
                    "Ways to express the future in English:\n\n"
                    "1. will + base verb  – predictions, spontaneous decisions, promises\n"
                    "   Example: It will rain tomorrow.\n\n"
                    "2. going to + base verb  – planned intentions, predictions based on evidence\n"
                    "   Example: I'm going to visit my parents this weekend.\n\n"
                    "3. Present Continuous  – fixed future arrangements\n"
                    "   Example: We are meeting at 6 PM.\n\n"
                    "4. Simple Present  – scheduled/timetabled events\n"
                    "   Example: The train leaves at 8 AM.\n\n"
                    "5. Future Perfect  – action completed before a future point\n"
                    "   Formula: will + have + past participle\n"
                    "   Example: By Friday, I will have finished the report."
                ),
                "examples": [
                    "will:                I'll help you with that. (spontaneous decision)",
                    "going to:            She's going to study medicine. (plan)",
                    "Present Continuous:  They are flying to Tokyo next Monday. (arrangement)",
                    "Future Perfect:      By 2030, she will have graduated.",
                ],
                "quiz": [
                    {
                        "question": "Someone spills coffee. You say: 'Don't worry, I ___ get some paper towels.' Which is best?",
                        "choices": [
                            "A) am going to",
                            "B) will",
                            "C) am",
                            "D) have",
                        ],
                        "answer": "B",
                        "explanation": "'will' is used for spontaneous decisions made at the moment of speaking.",
                    },
                    {
                        "question": "Which shows a future plan decided in advance?",
                        "choices": [
                            "A) I will maybe go to the gym.",
                            "B) I go to the gym tomorrow.",
                            "C) I am going to start a gym membership next month.",
                            "D) I am the gym.",
                        ],
                        "answer": "C",
                        "explanation": "'going to' expresses a pre-decided intention or plan.",
                    },
                ],
            },
            "prepositions": {
                "title": "Prepositions",
                "explanation": (
                    "Prepositions show relationships between words — time, place, direction, etc.\n\n"
                    "Prepositions of TIME:\n"
                    "  at  – specific times:    at 5 PM, at midnight, at noon\n"
                    "  on  – days/dates:         on Monday, on March 3rd, on my birthday\n"
                    "  in  – longer periods:     in 2024, in July, in the morning, in the 21st century\n\n"
                    "Prepositions of PLACE:\n"
                    "  at  – specific point:    at the bus stop, at school\n"
                    "  on  – surface:           on the table, on the wall\n"
                    "  in  – enclosed space:    in the box, in the city, in a car\n\n"
                    "Other common prepositions:\n"
                    "  above, below, between, beside, under, over, through, along, across, towards"
                ),
                "examples": [
                    "I wake up at 7 AM.",
                    "The meeting is on Thursday.",
                    "She was born in 1995.",
                    "The keys are on the table.",
                    "The cat is hiding under the bed.",
                ],
                "quiz": [
                    {
                        "question": "Choose the correct preposition: 'I'll see you ___ Monday.'",
                        "choices": ["A) at", "B) in", "C) on", "D) for"],
                        "answer": "C",
                        "explanation": "Use 'on' with specific days of the week.",
                    },
                    {
                        "question": "Choose the correct preposition: 'She was born ___ 1998.'",
                        "choices": ["A) at", "B) in", "C) on", "D) by"],
                        "answer": "B",
                        "explanation": "Use 'in' with years, months, and longer time periods.",
                    },
                ],
            },
            "vocabulary_intermediate": {
                "title": "Intermediate Vocabulary",
                "explanation": (
                    "Building a rich vocabulary improves your communication. Study these word sets:\n\n"
                    "ADJECTIVES (describing words):\n"
                    "  ambitious, confident, creative, determined, enthusiastic,\n"
                    "  generous, honest, patient, reliable, thoughtful\n\n"
                    "ADVERBS (modify verbs/adjectives):\n"
                    "  accurately, briefly, carefully, clearly, directly,\n"
                    "  efficiently, immediately, obviously, probably, rapidly\n\n"
                    "WORD FAMILIES (knowing related forms helps you use vocabulary flexibly):\n"
                    "  decide → decision → decisive → decisively\n"
                    "  create → creation → creative → creatively\n"
                    "  vary → variation → various → variably\n\n"
                    "Tip: When you learn a new word, also learn its noun, verb, adjective, and adverb forms."
                ),
                "examples": [
                    "She is an ambitious student who aims for top grades.",
                    "He responded immediately when he heard the news.",
                    "The team made a decisive victory in the finals.",
                    "Various options are available for the project.",
                ],
                "quiz": [
                    {
                        "question": "What is the noun form of 'decide'?",
                        "choices": [
                            "A) Decided",
                            "B) Decisive",
                            "C) Decision",
                            "D) Decidedly",
                        ],
                        "answer": "C",
                        "explanation": "decide (verb) → decision (noun) → decisive (adj) → decisively (adverb).",
                    },
                    {
                        "question": "Which word means 'willing to give and share'?",
                        "choices": [
                            "A) Ambitious",
                            "B) Generous",
                            "C) Patient",
                            "D) Reliable",
                        ],
                        "answer": "B",
                        "explanation": "'Generous' means willing to give or share freely.",
                    },
                ],
            },
        },
    },
    "advanced": {
        "description": "For proficient learners. Master complex grammar, academic writing, idioms, and sophisticated vocabulary.",
        "topics": {
            "conditionals": {
                "title": "Conditional Sentences",
                "explanation": (
                    "Conditional sentences talk about possible or hypothetical situations.\n\n"
                    "Zero Conditional – general truths, scientific facts\n"
                    "  If + present simple, present simple\n"
                    "  Example: If you heat water to 100°C, it boils.\n\n"
                    "First Conditional – real / likely future situations\n"
                    "  If + present simple, will + base verb\n"
                    "  Example: If it rains, we will stay inside.\n\n"
                    "Second Conditional – unreal / hypothetical present/future\n"
                    "  If + past simple, would + base verb\n"
                    "  Example: If I were a bird, I would fly everywhere.\n\n"
                    "Third Conditional – unreal / impossible past situations\n"
                    "  If + past perfect, would have + past participle\n"
                    "  Example: If she had studied harder, she would have passed.\n\n"
                    "Mixed Conditional – mixing time frames\n"
                    "  If + past perfect, would + base verb\n"
                    "  Example: If he had listened to me, he would be happy now."
                ),
                "examples": [
                    "Zero:   If you drop an egg, it breaks.",
                    "First:  If she calls, I will answer.",
                    "Second: If I had more time, I would travel the world.",
                    "Third:  If they had left earlier, they would have caught the train.",
                    "Mixed:  If I had taken that job, I would be living abroad now.",
                ],
                "quiz": [
                    {
                        "question": "Which conditional is: 'If I won the lottery, I would buy a house'?",
                        "choices": [
                            "A) Zero conditional",
                            "B) First conditional",
                            "C) Second conditional",
                            "D) Third conditional",
                        ],
                        "answer": "C",
                        "explanation": "Second conditional (If + past simple, would + base) expresses hypothetical/unlikely situations.",
                    },
                    {
                        "question": "Complete: 'If they had arrived on time, they _____ the opening speech.'",
                        "choices": [
                            "A) would hear",
                            "B) would have heard",
                            "C) had heard",
                            "D) will hear",
                        ],
                        "answer": "B",
                        "explanation": "Third conditional uses 'would have + past participle' in the result clause.",
                    },
                ],
            },
            "passive_voice": {
                "title": "Passive Voice",
                "explanation": (
                    "In active voice, the subject performs the action.\n"
                    "In passive voice, the subject receives the action.\n\n"
                    "Formation: be (correct tense) + past participle\n"
                    "Agent (doer) can be added with 'by': 'The cake was baked BY Maria.'\n\n"
                    "Tense changes in passive:\n"
                    "  Active                     → Passive\n"
                    "  She writes reports.        → Reports are written (by her).\n"
                    "  He is writing a letter.    → A letter is being written (by him).\n"
                    "  They built the bridge.     → The bridge was built (by them).\n"
                    "  We had finished the work.  → The work had been finished.\n"
                    "  She will send the email.   → The email will be sent.\n\n"
                    "When to use passive:\n"
                    "  • The doer is unknown: 'My bike was stolen.'\n"
                    "  • The doer is obvious: 'The suspect was arrested.'\n"
                    "  • To emphasize the action, not the doer (common in formal/academic writing)"
                ),
                "examples": [
                    "Active:  Shakespeare wrote 'Hamlet'.",
                    "Passive: 'Hamlet' was written by Shakespeare.",
                    "Active:  They are building a new hospital.",
                    "Passive: A new hospital is being built.",
                    "Academic: The results were analyzed using statistical methods.",
                ],
                "quiz": [
                    {
                        "question": "Convert to passive: 'The chef cooked the meal.'",
                        "choices": [
                            "A) The meal cooked by the chef.",
                            "B) The meal was cooked by the chef.",
                            "C) The meal is cooked by the chef.",
                            "D) The chef was cooked the meal.",
                        ],
                        "answer": "B",
                        "explanation": "Simple past passive: was/were + past participle. 'The meal was cooked by the chef.'",
                    },
                    {
                        "question": "Which sentence is in the passive voice?",
                        "choices": [
                            "A) The artist painted a mural.",
                            "B) She has been painting for years.",
                            "C) The mural is being painted.",
                            "D) He paints portraits.",
                        ],
                        "answer": "C",
                        "explanation": "'is being painted' = present continuous passive (is/are + being + past participle).",
                    },
                ],
            },
            "reported_speech": {
                "title": "Reported (Indirect) Speech",
                "explanation": (
                    "Reported speech tells us what someone said without quoting them exactly.\n\n"
                    "Tense backshift (when the reporting verb is past):\n"
                    "  Direct                     → Reported\n"
                    "  'I am happy.'              → She said she WAS happy.\n"
                    "  'I like coffee.'           → He said he LIKED coffee.\n"
                    "  'I am working.'            → She said she WAS WORKING.\n"
                    "  'I have finished.'         → He said he HAD FINISHED.\n"
                    "  'I will call you.'         → She said she WOULD call me.\n"
                    "  'I can swim.'              → He said he COULD swim.\n\n"
                    "Pronoun and time/place changes:\n"
                    "  I/we → he/she/they\n"
                    "  here → there   |   now → then\n"
                    "  today → that day   |   tomorrow → the next day\n"
                    "  yesterday → the day before\n\n"
                    "Reporting questions:\n"
                    "  'Do you like it?' → She asked if/whether I liked it.\n"
                    "  'Where do you live?' → He asked where I lived."
                ),
                "examples": [
                    "'I love music.' → She said she loved music.",
                    "'I'll be there tomorrow.' → He said he would be there the next day.",
                    "'Are you coming?' → She asked if I was coming.",
                    "'What time does it start?' → He asked what time it started.",
                ],
                "quiz": [
                    {
                        "question": "Report this: He said, 'I am studying for the exam.'",
                        "choices": [
                            "A) He said he studied for the exam.",
                            "B) He said he is studying for the exam.",
                            "C) He said he was studying for the exam.",
                            "D) He said he has studied for the exam.",
                        ],
                        "answer": "C",
                        "explanation": "Present continuous (am studying) → Past continuous (was studying) in reported speech.",
                    },
                    {
                        "question": "Report this: She asked, 'Do you want some tea?'",
                        "choices": [
                            "A) She asked did I want some tea.",
                            "B) She asked if I wanted some tea.",
                            "C) She asked that I want some tea.",
                            "D) She asked whether do I want some tea.",
                        ],
                        "answer": "B",
                        "explanation": "Yes/No questions use 'if' or 'whether' + subject + backshifted verb.",
                    },
                ],
            },
            "idioms": {
                "title": "Idioms & Phrasal Verbs",
                "explanation": (
                    "Idioms are phrases whose meaning cannot be deduced from the individual words.\n\n"
                    "Common English Idioms:\n"
                    "  • Break a leg           – Good luck!\n"
                    "  • Hit the nail on the head – To say something exactly right\n"
                    "  • Bite the bullet       – Endure a painful/difficult situation\n"
                    "  • Under the weather     – Feeling sick or unwell\n"
                    "  • Cost an arm and a leg – Very expensive\n"
                    "  • Beat around the bush  – Avoid the main topic\n"
                    "  • Burn bridges          – Destroy a relationship permanently\n"
                    "  • The ball is in your court – It's your turn to take action\n\n"
                    "Phrasal Verbs (verb + particle = new meaning):\n"
                    "  • give up       – stop trying / quit\n"
                    "  • put off       – postpone\n"
                    "  • run into      – meet unexpectedly\n"
                    "  • look up to    – admire and respect\n"
                    "  • come across   – find something by chance\n"
                    "  • carry out     – perform or complete a task\n"
                    "  • get over      – recover from something\n"
                    "  • turn down     – reject an offer"
                ),
                "examples": [
                    "'You hit the nail on the head – that's exactly the problem.'",
                    "'I'm under the weather today, so I'll work from home.'",
                    "'Don't give up! You're almost there.'",
                    "'She looked up to her mentor throughout her career.'",
                    "'They had to put off the meeting until next week.'",
                ],
                "quiz": [
                    {
                        "question": "What does 'break a leg' mean?",
                        "choices": [
                            "A) Get injured",
                            "B) Good luck",
                            "C) Take a break",
                            "D) Be careful",
                        ],
                        "answer": "B",
                        "explanation": "'Break a leg' is a theatrical idiom meaning 'Good luck!'",
                    },
                    {
                        "question": "What does 'put off' mean as a phrasal verb?",
                        "choices": [
                            "A) Remove clothing",
                            "B) Dislike someone",
                            "C) Postpone",
                            "D) Turn off a device",
                        ],
                        "answer": "C",
                        "explanation": "'Put off' means to delay or postpone something.",
                    },
                ],
            },
            "academic_writing": {
                "title": "Academic & Advanced Writing",
                "explanation": (
                    "Academic writing requires clarity, precision, and formal tone.\n\n"
                    "ESSAY STRUCTURE:\n"
                    "  Introduction:\n"
                    "    • Hook (attention-grabbing sentence)\n"
                    "    • Background information\n"
                    "    • Thesis statement (your main argument)\n"
                    "  Body paragraphs (PEEL structure):\n"
                    "    • Point: state the main idea of the paragraph\n"
                    "    • Evidence: provide supporting details, facts, examples\n"
                    "    • Explanation: explain how the evidence supports your point\n"
                    "    • Link: connect back to the thesis or to the next paragraph\n"
                    "  Conclusion:\n"
                    "    • Restate thesis (in different words)\n"
                    "    • Summarize key points\n"
                    "    • Final thought / call to action\n\n"
                    "FORMAL LANGUAGE TIPS:\n"
                    "  • Avoid contractions: use 'do not' not 'don't'\n"
                    "  • Avoid informal words: use 'significant' not 'big'\n"
                    "  • Use linking words: Furthermore, Moreover, However, Nevertheless,\n"
                    "    Consequently, In contrast, In addition, Therefore\n"
                    "  • Use hedging language: 'It appears that…', 'Research suggests…'"
                ),
                "examples": [
                    "Weak:   People use phones a lot. It's a big problem.",
                    "Strong: Excessive smartphone usage has become a significant societal concern,\n"
                    "        as research suggests it negatively impacts mental health and productivity.",
                    "---",
                    "Linking: Furthermore, the data demonstrates a correlation between sleep\n"
                    "         deprivation and cognitive decline. Nevertheless, further research\n"
                    "         is required to establish causation.",
                ],
                "quiz": [
                    {
                        "question": "Which is more appropriate in formal academic writing?",
                        "choices": [
                            "A) The results were really good.",
                            "B) The results were quite impressive.",
                            "C) The results were significantly positive.",
                            "D) The results blew everyone away.",
                        ],
                        "answer": "C",
                        "explanation": "Academic writing requires formal, precise language. 'Significantly positive' is the most appropriate choice.",
                    },
                    {
                        "question": "Which linking word shows CONTRAST?",
                        "choices": [
                            "A) Furthermore",
                            "B) In addition",
                            "C) Therefore",
                            "D) Nevertheless",
                        ],
                        "answer": "D",
                        "explanation": "'Nevertheless' (and 'However', 'In contrast') shows contrast. 'Furthermore' and 'In addition' show addition; 'Therefore' shows result.",
                    },
                ],
            },
        },
    },
    },  # end "English"
    "Samoan": {
        "Level 1": {
            "basics": {
                "explanation": (
                    "Welcome to Samoan basics. Samoan uses a Verb-Subject-Object (VSO) structure,\n"
                    "which is different from English's Subject-Verb-Object (SVO) order.\n\n"
                    "Example:\n"
                    "  English (SVO): The dog  bites  the man.\n"
                    "  Samoan  (VSO): Ua 'ai  e le maile  le tagata.\n"
                    "                 (Bites the dog    the man.)\n\n"
                    "Common greetings:\n"
                    "  • Talofa       – Hello\n"
                    "  • Fa'afetai    – Thank you\n"
                    "  • Tofa         – Goodbye"
                ),
                "quiz": [
                    {
                        "question": "What word order does Samoan use?",
                        "choices": [
                            "A) Subject-Verb-Object (SVO)",
                            "B) Verb-Subject-Object (VSO)",
                            "C) Object-Subject-Verb (OSV)",
                            "D) Verb-Object-Subject (VOS)",
                        ],
                        "answer": "B",
                        "explanation": "Samoan follows Verb-Subject-Object (VSO) order, unlike English which is SVO.",
                    },
                ],
            },
        },
    },
}

LEVEL_ORDER = ["basic", "intermediate", "advanced"]

TOPIC_ORDER = {
    "basic": [
        "alphabet",
        "greetings",
        "numbers",
        "basic_vocabulary",
        "basic_sentences",
    ],
    "intermediate": [
        "present_tenses",
        "past_tenses",
        "future_tenses",
        "prepositions",
        "vocabulary_intermediate",
    ],
    "advanced": [
        "conditionals",
        "passive_voice",
        "reported_speech",
        "idioms",
        "academic_writing",
    ],
}


def get_levels(course="English"):
    if course == "Samoan":
        return ["Level 1"]
    return LEVEL_ORDER[:]


def get_topics(course, level):
    if course == "Samoan" and level == "Level 1":
        return ["basics"]
    return TOPIC_ORDER.get(level, [])


def get_lesson(course, level, topic):
    # Handle slight nesting difference between English and Samoan dictionaries
    if course == "Samoan":
        return CURRICULUM.get(course, {}).get(level, {}).get(topic)
    return CURRICULUM.get(course, {}).get(level, {}).get("topics", {}).get(topic)


def get_level_description(course, level):
    if course == "Samoan":
        return "Samoan Basics"
    return CURRICULUM.get(course, {}).get(level, {}).get("description", "")


def next_topic(course, level, topic):
    topics = get_topics(course, level)
    if topic in topics:
        idx = topics.index(topic)
        if idx + 1 < len(topics):
            return level, topics[idx + 1]
    levels = get_levels(course)
    if level in levels:
        level_idx = levels.index(level)
        if level_idx + 1 < len(levels):
            next_lv = levels[level_idx + 1]
            next_topics = get_topics(course, next_lv)
            if next_topics:
                return next_lv, next_topics[0]
    return None, None
