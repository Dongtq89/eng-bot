#!/usr/bin/env python3
"""
🎓 Cambridge Young Learners English Bot
Levels: Starters → Movers → Flyers (Cambridge YLE Standard)
Features: Vocabulary, Quiz, Grammar, Flashcards — all level-adaptive
"""

import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BOT_TOKEN = "8699626749:AAGHmi4cs1NuMXFKc0WNtqXlZGhxxIzZaB4"   # 👈 Thay token của bạn vào đây

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ─── LEVEL METADATA ───────────────────────────────────────────────────────────
LEVELS = {
    "starters": {
        "emoji": "🌟",
        "name": "Starters",
        "desc": "Cấp độ khởi đầu (A1) — Dành cho trẻ em 6-8 tuổi",
        "color": "🟢",
    },
    "movers": {
        "emoji": "🚀",
        "name": "Movers",
        "desc": "Cấp độ trung cấp (A1-A2) — Dành cho trẻ em 8-10 tuổi",
        "color": "🟡",
    },
    "flyers": {
        "emoji": "🦅",
        "name": "Flyers",
        "desc": "Cấp độ nâng cao (A2-B1) — Dành cho trẻ em 10-12 tuổi",
        "color": "🔴",
    },
}

# ─── VOCABULARY DATA ──────────────────────────────────────────────────────────
VOCABULARY = {
    "starters": [
        {"word": "apple",      "meaning": "quả táo",          "example": "I eat an apple every day.",      "topic": "Food"},
        {"word": "cat",        "meaning": "con mèo",          "example": "My cat is black.",               "topic": "Animals"},
        {"word": "red",        "meaning": "màu đỏ",           "example": "The ball is red.",               "topic": "Colours"},
        {"word": "happy",      "meaning": "vui vẻ, hạnh phúc","example": "I am happy today.",             "topic": "Feelings"},
        {"word": "school",     "meaning": "trường học",        "example": "I go to school by bus.",        "topic": "Places"},
        {"word": "dog",        "meaning": "con chó",          "example": "The dog is big.",                "topic": "Animals"},
        {"word": "book",       "meaning": "quyển sách",       "example": "This is my book.",              "topic": "Classroom"},
        {"word": "water",      "meaning": "nước",             "example": "Please drink water.",           "topic": "Food"},
        {"word": "house",      "meaning": "ngôi nhà",         "example": "My house is blue.",             "topic": "Places"},
        {"word": "run",        "meaning": "chạy",             "example": "I can run fast.",               "topic": "Actions"},
        {"word": "big",        "meaning": "to, lớn",          "example": "An elephant is big.",           "topic": "Describing"},
        {"word": "mum",        "meaning": "mẹ",               "example": "My mum is kind.",               "topic": "Family"},
        {"word": "dad",        "meaning": "bố",               "example": "My dad can cook.",              "topic": "Family"},
        {"word": "ball",       "meaning": "quả bóng",         "example": "Kick the ball!",                "topic": "Sports"},
        {"word": "chair",      "meaning": "cái ghế",          "example": "Sit on the chair.",            "topic": "Classroom"},
    ],
    "movers": [
        {"word": "adventure",  "meaning": "cuộc phiêu lưu",   "example": "We had a great adventure.",    "topic": "Stories"},
        {"word": "museum",     "meaning": "bảo tàng",         "example": "We visited the museum.",       "topic": "Places"},
        {"word": "vegetables", "meaning": "rau củ",           "example": "Eat your vegetables!",         "topic": "Food"},
        {"word": "enormous",   "meaning": "rất to lớn",       "example": "The elephant is enormous.",    "topic": "Describing"},
        {"word": "clever",     "meaning": "thông minh",       "example": "She is very clever.",          "topic": "Character"},
        {"word": "frightened", "meaning": "sợ hãi",           "example": "The child was frightened.",    "topic": "Feelings"},
        {"word": "bicycle",    "meaning": "xe đạp",           "example": "He rides his bicycle to school.","topic": "Transport"},
        {"word": "library",    "meaning": "thư viện",         "example": "I borrow books from the library.","topic": "Places"},
        {"word": "terrible",   "meaning": "khủng khiếp, tệ",  "example": "The weather was terrible.",    "topic": "Weather"},
        {"word": "favourite",  "meaning": "yêu thích nhất",   "example": "What is your favourite sport?","topic": "General"},
        {"word": "collect",    "meaning": "sưu tầm, thu thập","example": "I collect stamps.",            "topic": "Hobbies"},
        {"word": "hospital",   "meaning": "bệnh viện",        "example": "The nurse works at the hospital.","topic": "Places"},
        {"word": "bored",      "meaning": "chán nản",         "example": "I am bored at home.",          "topic": "Feelings"},
        {"word": "planet",     "meaning": "hành tinh",        "example": "Earth is a planet.",           "topic": "Science"},
        {"word": "village",    "meaning": "làng",             "example": "My grandparents live in a village.","topic": "Places"},
    ],
    "flyers": [
        {"word": "ancient",    "meaning": "cổ đại, xưa cũ",  "example": "The ancient ruins are beautiful.","topic": "History"},
        {"word": "investigate", "meaning": "điều tra, nghiên cứu","example": "Scientists investigate new diseases.","topic": "Science"},
        {"word": "exhausted",  "meaning": "kiệt sức",         "example": "After the race, I was exhausted.","topic": "Feelings"},
        {"word": "opportunity","meaning": "cơ hội",           "example": "This is a great opportunity.",  "topic": "General"},
        {"word": "environment","meaning": "môi trường",       "example": "We must protect our environment.","topic": "Nature"},
        {"word": "volunteer",  "meaning": "tình nguyện viên", "example": "She volunteers at the shelter.","topic": "Community"},
        {"word": "anxious",    "meaning": "lo lắng, bồn chồn","example": "I felt anxious before the exam.","topic": "Feelings"},
        {"word": "pollution",  "meaning": "ô nhiễm",          "example": "Air pollution is a big problem.","topic": "Environment"},
        {"word": "tournament", "meaning": "giải đấu",         "example": "He won the chess tournament.", "topic": "Sports"},
        {"word": "architect",  "meaning": "kiến trúc sư",     "example": "She wants to be an architect.", "topic": "Jobs"},
        {"word": "destination","meaning": "điểm đến",         "example": "Paris is a wonderful destination.","topic": "Travel"},
        {"word": "recommend",  "meaning": "gợi ý, giới thiệu","example": "I recommend this book to you.", "topic": "General"},
        {"word": "disappear",  "meaning": "biến mất",         "example": "The coins disappeared from the box.","topic": "Actions"},
        {"word": "persuade",   "meaning": "thuyết phục",      "example": "He persuaded me to join the team.","topic": "Communication"},
        {"word": "challenge",  "meaning": "thách thức",       "example": "Learning English is a great challenge.","topic": "General"},
    ],
}

# ─── GRAMMAR DATA ─────────────────────────────────────────────────────────────
GRAMMAR = {
    "starters": [
        {
            "title": "To BE: am / is / are",
            "explanation": (
                "✅ Dùng *am / is / are* để nói về bản thân và mọi người:\n\n"
                "• I *am* happy. (Tôi vui)\n"
                "• She *is* my friend. (Cô ấy là bạn tôi)\n"
                "• They *are* cats. (Chúng là mèo)\n\n"
                "📌 *Quy tắc:*\n"
                "I → am | He/She/It → is | You/We/They → are"
            ),
            "tip": "💡 Nhớ: I AM, không phải I IS hay I ARE!"
        },
        {
            "title": "CAN — Diễn tả khả năng",
            "explanation": (
                "✅ Dùng *can* để nói bạn có thể làm gì:\n\n"
                "• I *can* swim. (Tôi có thể bơi)\n"
                "• She *can* sing. (Cô ấy có thể hát)\n"
                "• He *can't* fly. (Anh ấy không thể bay)\n\n"
                "📌 *Cấu trúc:*\n"
                "Can + động từ nguyên mẫu (không có 'to')\n"
                "✔ I can *run* | ✖ I can *to run*"
            ),
            "tip": "💡 CAN giống nhau cho tất cả ngôi: I/You/He/She/We/They can"
        },
        {
            "title": "This / That / These / Those",
            "explanation": (
                "✅ Dùng để chỉ vật gần hay xa:\n\n"
                "• *This* is my pen. (Cái bút này — gần)\n"
                "• *That* is a bird. (Con chim kia — xa)\n"
                "• *These* are books. (Những quyển sách này — nhiều, gần)\n"
                "• *Those* are dogs. (Những con chó kia — nhiều, xa)"
            ),
            "tip": "💡 This/That = 1 vật | These/Those = nhiều vật"
        },
        {
            "title": "Câu hỏi với HAVE GOT",
            "explanation": (
                "✅ Dùng *have got* để nói về sở hữu:\n\n"
                "• I *have got* a dog. (Tôi có một con chó)\n"
                "• She *has got* blue eyes. (Cô ấy có đôi mắt xanh)\n\n"
                "📌 *Hỏi & Đáp:*\n"
                "Have you got a pet? → Yes, I have. / No, I haven't.\n"
                "Has she got a bike? → Yes, she has. / No, she hasn't."
            ),
            "tip": "💡 I/You/We/They → HAVE GOT | He/She/It → HAS GOT"
        },
    ],
    "movers": [
        {
            "title": "Past Simple — Quá khứ đơn",
            "explanation": (
                "✅ Dùng để kể về việc đã xảy ra trong quá khứ:\n\n"
                "📌 *Động từ có quy tắc (+ ed):*\n"
                "• walk → walk*ed* | play → play*ed*\n"
                "• I *walked* to school yesterday.\n\n"
                "📌 *Động từ bất quy tắc:*\n"
                "• go → *went* | see → *saw* | eat → *ate*\n"
                "• She *went* to the zoo last Sunday."
            ),
            "tip": "💡 Từ khoá: yesterday, last week, ago, in 2020"
        },
        {
            "title": "Comparative Adjectives — So sánh hơn",
            "explanation": (
                "✅ Dùng để so sánh 2 người/vật:\n\n"
                "📌 *Tính từ ngắn (+ er):*\n"
                "• tall → tall*er* | fast → fast*er*\n"
                "• Jack is tall*er* than Tom.\n\n"
                "📌 *Tính từ dài (more + adj):*\n"
                "• interesting → *more* interesting\n"
                "• English is *more* interesting than maths.\n\n"
                "📌 *Đặc biệt:*\n"
                "• good → *better* | bad → *worse*"
            ),
            "tip": "💡 Luôn dùng THAN sau tính từ so sánh hơn"
        },
        {
            "title": "Present Continuous — Hiện tại tiếp diễn",
            "explanation": (
                "✅ Dùng khi nói về hành động đang xảy ra ngay lúc này:\n\n"
                "📌 *Cấu trúc:* am/is/are + V-ing\n\n"
                "• I *am reading* a book now.\n"
                "• She *is playing* in the garden.\n"
                "• They *are not watching* TV.\n\n"
                "📌 *Hỏi:* Are you eating? → Yes, I am."
            ),
            "tip": "💡 Từ khoá: now, at the moment, look!, listen!"
        },
        {
            "title": "Going to — Kế hoạch tương lai",
            "explanation": (
                "✅ Dùng để nói về kế hoạch hoặc dự định:\n\n"
                "📌 *Cấu trúc:* am/is/are + going to + V\n\n"
                "• I *am going to* visit my grandma tomorrow.\n"
                "• She *is going to* study English tonight.\n"
                "• We *are not going to* play football — it's raining."
            ),
            "tip": "💡 'Going to' = đã có kế hoạch, 'will' = quyết định tức thì"
        },
    ],
    "flyers": [
        {
            "title": "Present Perfect — Hiện tại hoàn thành",
            "explanation": (
                "✅ Dùng khi hành động trong quá khứ còn liên quan đến hiện tại:\n\n"
                "📌 *Cấu trúc:* have/has + V3\n\n"
                "• I *have visited* Paris three times.\n"
                "• She *has just finished* her homework.\n"
                "• Have you *ever eaten* sushi? → Yes, I have.\n\n"
                "📌 *Phân biệt với Past Simple:*\n"
                "• I *have lost* my key. (Vẫn đang mất)\n"
                "• I *lost* my key yesterday. (Xong rồi)"
            ),
            "tip": "💡 Từ khoá: just, already, yet, ever, never, since, for"
        },
        {
            "title": "Passive Voice — Câu bị động",
            "explanation": (
                "✅ Dùng khi muốn nhấn mạnh hành động, không phải người làm:\n\n"
                "📌 *Cấu trúc:* be + V3 (past participle)\n\n"
                "• The book *was written* by J.K. Rowling.\n"
                "• English *is spoken* in many countries.\n"
                "• The windows *are cleaned* every week.\n\n"
                "📌 *Các thì thông dụng:*\n"
                "• Present: is/are + V3\n"
                "• Past: was/were + V3\n"
                "• Future: will be + V3"
            ),
            "tip": "💡 Dùng Passive khi không biết hoặc không cần nêu chủ thể"
        },
        {
            "title": "Conditional Type 1 & 2",
            "explanation": (
                "✅ *Type 1* — Điều kiện có thể xảy ra ở hiện tại/tương lai:\n"
                "If + Present Simple → will + V\n"
                "• If it *rains*, I *will* stay home.\n\n"
                "✅ *Type 2* — Điều kiện không thực tế ở hiện tại:\n"
                "If + Past Simple → would + V\n"
                "• If I *had* wings, I *would* fly to school.\n\n"
                "📌 *Lưu ý:* Type 2 dùng 'were' cho tất cả ngôi:\n"
                "• If I *were* a bird... | If she *were* here..."
            ),
            "tip": "💡 Type 1 = thực tế có thể | Type 2 = mơ ước, không thực"
        },
        {
            "title": "Reported Speech — Lời nói gián tiếp",
            "explanation": (
                "✅ Dùng khi kể lại lời ai đó nói:\n\n"
                "📌 *Câu khẳng định:* said (that)...\n"
                "• Direct: \"I like pizza.\"\n"
                "• Reported: He said (that) he *liked* pizza.\n\n"
                "📌 *Câu hỏi:* asked + if/whether...\n"
                "• Direct: \"Do you speak English?\"\n"
                "• Reported: She asked if I *spoke* English.\n\n"
                "📌 *Thì lùi một bậc:* am/is → was | can → could | will → would"
            ),
            "tip": "💡 Thì lùi 1 bậc khi động từ tường thuật là quá khứ (said, asked)"
        },
    ],
}

# ─── QUIZ DATA ────────────────────────────────────────────────────────────────
QUIZZES = {
    "starters": [
        {
            "question": "What colour is the sun?",
            "options": ["Blue", "Red", "Yellow", "Green"],
            "answer": 2,
            "explanation": "✅ The sun is *yellow*! ☀️"
        },
        {
            "question": "Complete: 'I ___ a student.'",
            "options": ["is", "are", "am", "be"],
            "answer": 2,
            "explanation": "✅ I + *am* → I am a student."
        },
        {
            "question": "Which animal can fly?",
            "options": ["Dog", "Cat", "Fish", "Bird"],
            "answer": 3,
            "explanation": "✅ A *bird* can fly! 🐦"
        },
        {
            "question": "Complete: 'She ___ got a cat.'",
            "options": ["have", "has", "am", "is"],
            "answer": 1,
            "explanation": "✅ She/He/It + *has* got → She has got a cat."
        },
        {
            "question": "What is this? 📚",
            "options": ["A pen", "A book", "A bag", "A chair"],
            "answer": 1,
            "explanation": "✅ 📚 is a *book*!"
        },
        {
            "question": "Complete: '___ can swim. Dogs can't.'",
            "options": ["Cats", "Fish", "Birds", "Rabbits"],
            "answer": 1,
            "explanation": "✅ *Fish* can swim! 🐟"
        },
        {
            "question": "Complete: 'Those ___ my friends.'",
            "options": ["am", "is", "be", "are"],
            "answer": 3,
            "explanation": "✅ Those (plural) + *are* → Those are my friends."
        },
        {
            "question": "'Big' is the opposite of:",
            "options": ["Fast", "Small", "Tall", "Long"],
            "answer": 1,
            "explanation": "✅ Big ↔ *Small*! 🐘🐭"
        },
    ],
    "movers": [
        {
            "question": "Choose the correct past tense: 'Yesterday, she ___ to the park.'",
            "options": ["go", "goes", "went", "going"],
            "answer": 2,
            "explanation": "✅ Go → *went* (bất quy tắc). Yesterday → Past Simple!"
        },
        {
            "question": "Choose the comparative: 'An elephant is ___ than a mouse.'",
            "options": ["more big", "bigger", "most big", "biggest"],
            "answer": 1,
            "explanation": "✅ Big → *bigger* (tính từ ngắn + er than)"
        },
        {
            "question": "Complete: 'Look! The children ___ playing football.'",
            "options": ["is", "are", "am", "were"],
            "answer": 1,
            "explanation": "✅ They/The children + *are* + V-ing (Present Continuous)"
        },
        {
            "question": "'Museum' means:",
            "options": ["Siêu thị", "Bảo tàng", "Bệnh viện", "Thư viện"],
            "answer": 1,
            "explanation": "✅ Museum = *Bảo tàng* 🏛️"
        },
        {
            "question": "Complete: 'I ___ going to visit my grandma tomorrow.'",
            "options": ["am", "is", "are", "be"],
            "answer": 0,
            "explanation": "✅ I + *am* going to + V (kế hoạch tương lai)"
        },
        {
            "question": "Which word means 'very big'?",
            "options": ["Tiny", "Small", "Enormous", "Short"],
            "answer": 2,
            "explanation": "✅ *Enormous* = rất to lớn 🐘"
        },
        {
            "question": "Choose the correct form: 'He ___ TV when I called.'",
            "options": ["watch", "watches", "watched", "watching"],
            "answer": 2,
            "explanation": "✅ Past Simple: *watched*. 'When I called' signals past!"
        },
        {
            "question": "Complete: 'She is ___ intelligent ___ her brother.'",
            "options": ["more / than", "most / than", "more / then", "most / then"],
            "answer": 0,
            "explanation": "✅ *more* + long adjective + *than* = so sánh hơn"
        },
    ],
    "flyers": [
        {
            "question": "Choose the correct form: 'She ___ to Paris three times.'",
            "options": ["went", "has gone", "has been", "goes"],
            "answer": 2,
            "explanation": "✅ *Has been* = đã từng đến và trở về (Present Perfect kinh nghiệm)"
        },
        {
            "question": "The book ___ by Roald Dahl.",
            "options": ["wrote", "is writing", "was written", "has written"],
            "answer": 2,
            "explanation": "✅ Passive Voice Past Simple: *was written* (be + V3)"
        },
        {
            "question": "'If I ___ you, I would apologise immediately.'",
            "options": ["am", "was", "were", "will be"],
            "answer": 2,
            "explanation": "✅ Conditional Type 2 → If + *were* (dùng 'were' cho mọi ngôi)"
        },
        {
            "question": "'Pollution' means:",
            "options": ["Giải pháp", "Ô nhiễm", "Môi trường", "Thiên nhiên"],
            "answer": 1,
            "explanation": "✅ Pollution = *Ô nhiễm* 🌫️"
        },
        {
            "question": "Choose: 'He told me he ___ tired.'",
            "options": ["is", "are", "was", "will be"],
            "answer": 2,
            "explanation": "✅ Reported Speech: is → *was* (thì lùi 1 bậc)"
        },
        {
            "question": "'Exhausted' is closest in meaning to:",
            "options": ["Excited", "Very tired", "Bored", "Surprised"],
            "answer": 1,
            "explanation": "✅ Exhausted = *very tired* (kiệt sức hoàn toàn) 😴"
        },
        {
            "question": "Complete: 'If it rains tomorrow, we ___ stay inside.'",
            "options": ["would", "will", "can", "should"],
            "answer": 1,
            "explanation": "✅ Conditional Type 1: If + Present → *will* + V"
        },
        {
            "question": "Which is correct?",
            "options": [
                "English is spoke here.",
                "English is speaking here.",
                "English is spoken here.",
                "English spoken here."
            ],
            "answer": 2,
            "explanation": "✅ Passive Present Simple: is + *spoken* (V3)"
        },
    ],
}

# ─── FLASHCARDS ───────────────────────────────────────────────────────────────
FLASHCARDS = {
    "starters": [
        {"front": "🔤 What is this? 🍎", "back": "Apple = *Quả táo*\n\n📝 _'I eat an apple.'_"},
        {"front": "🔤 What is this? 🐕", "back": "Dog = *Con chó*\n\n📝 _'The dog is big.'_"},
        {"front": "🔤 What colour is 🌊?", "back": "Blue = *Màu xanh dương*\n\n📝 _'The sea is blue.'_"},
        {"front": "🔤 CAN or CAN'T? 🐟 + swim?", "back": "A fish *can* swim! ✅\n\n📝 _'Fish can swim in water.'_"},
        {"front": "🔤 am / is / are?\n'She ___ my friend.'", "back": "She *is* my friend.\n\n📌 He/She/It → IS"},
        {"front": "🔤 What is this? 📖", "back": "Book = *Quyển sách*\n\n📝 _'I read a book.'_"},
        {"front": "🔤 Opposite of BIG?", "back": "Small = *Nhỏ bé*\n\n📝 _'A mouse is small.'_"},
        {"front": "🔤 HAVE or HAS?\n'They ___ got a dog.'", "back": "They *have* got a dog.\n\n📌 I/You/We/They → HAVE"},
    ],
    "movers": [
        {"front": "🔤 Past tense of GO?", "back": "Go → *Went* (bất quy tắc!)\n\n📝 _'We went to the zoo.'_"},
        {"front": "🔤 What does ENORMOUS mean?", "back": "Enormous = *Rất to lớn*\n\n📝 _'The whale is enormous.'_"},
        {"front": "🔤 Comparative of GOOD?", "back": "Good → *Better*\n\n📝 _'This book is better than that one.'_"},
        {"front": "🔤 What tense?\n'She is eating lunch now.'", "back": "Present Continuous ✅\n(am/is/are + V-ing)\n\n*Now* = đang xảy ra"},
        {"front": "🔤 What does FRIGHTENED mean?", "back": "Frightened = *Sợ hãi*\n\n📝 _'The child was frightened.'_"},
        {"front": "🔤 Comparative of BAD?", "back": "Bad → *Worse*\n\n📝 _'Today's weather is worse than yesterday.'_"},
        {"front": "🔤 GOING TO or WILL?\n'Look at those clouds! It ___ rain.'", "back": "*Going to* rain! 🌧️\n\n📌 Nhìn thấy bằng chứng → going to"},
        {"front": "🔤 Past tense of SEE?", "back": "See → *Saw* (bất quy tắc!)\n\n📝 _'I saw a rainbow yesterday.'_"},
    ],
    "flyers": [
        {"front": "🔤 Present Perfect:\n'She ___ just ___ her homework.'", "back": "She *has just finished* her homework.\n\n📌 have/has + V3"},
        {"front": "🔤 What does PERSUADE mean?", "back": "Persuade = *Thuyết phục*\n\n📝 _'He persuaded me to join.'_"},
        {"front": "🔤 Passive:\n'The letter ___ yesterday.'", "back": "The letter *was written* yesterday.\n\n📌 Past Passive: was/were + V3"},
        {"front": "🔤 What does VOLUNTEER mean?", "back": "Volunteer = *Tình nguyện viên*\n\n📝 _'She volunteers at the hospital.'_"},
        {"front": "🔤 Reported Speech:\n'I love English.' → He said...", "back": "He said (that) he *loved* English.\n\n📌 love → loved (lùi 1 bậc)"},
        {"front": "🔤 What does ANXIOUS mean?", "back": "Anxious = *Lo lắng, bồn chồn*\n\n📝 _'I felt anxious before the exam.'_"},
        {"front": "🔤 Conditional Type 2:\n'If I ___ wings, I would fly.'", "back": "If I *had* wings...\n\n📌 Type 2: If + Past Simple → would"},
        {"front": "🔤 What does DESTINATION mean?", "back": "Destination = *Điểm đến*\n\n📝 _'Paris is my dream destination.'_"},
    ],
}

# ─── USER STORE ───────────────────────────────────────────────────────────────
users = {}

def get_user(uid):
    if uid not in users:
        users[uid] = {
            "level": None,
            "quiz_index": 0,
            "quiz_score": 0,
            "flashcard_index": 0,
            "vocab_seen": [],
            "grammar_seen": [],
        }
    return users[uid]

# ─── KEYBOARDS ────────────────────────────────────────────────────────────────

def level_select_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌟 Starters (A1)", callback_data="level_starters")],
        [InlineKeyboardButton("🚀 Movers (A1-A2)", callback_data="level_movers")],
        [InlineKeyboardButton("🦅 Flyers (A2-B1)", callback_data="level_flyers")],
    ])

def main_menu_keyboard(level):
    lvl = LEVELS[level]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 Từ vựng", callback_data="vocab"),
         InlineKeyboardButton("🧠 Quiz", callback_data="quiz_start")],
        [InlineKeyboardButton("📚 Ngữ pháp", callback_data="grammar"),
         InlineKeyboardButton("🃏 Flashcard", callback_data="flashcard")],
        [InlineKeyboardButton("🔄 Đổi cấp độ", callback_data="change_level")],
    ])

def back_to_menu_btn():
    return InlineKeyboardButton("🏠 Menu", callback_data="menu")

# ─── ESCAPE MARKDOWN V2 ───────────────────────────────────────────────────────
def esc(text):
    """Escape special chars for MarkdownV2, preserving * and _ for formatting."""
    special = r'\[]()~`>#+-=|{}.!'
    return ''.join(f'\\{c}' if c in special else c for c in text)

# ─── HANDLERS ─────────────────────────────────────────────────────────────────

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    ud = get_user(uid)
    ud["level"] = None
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 Xin chào *{name}*\\!\n\n"
        "🎓 Chào mừng đến với *Cambridge English Bot*\\!\n\n"
        "Bot hỗ trợ 3 cấp độ theo chuẩn Cambridge YLE:\n"
        "🌟 *Starters* \\— Khởi đầu \\(A1\\)\n"
        "🚀 *Movers* \\— Trung cấp \\(A1\\-A2\\)\n"
        "🦅 *Flyers* \\— Nâng cao \\(A2\\-B1\\)\n\n"
        "👇 *Chọn cấp độ của bạn:*",
        parse_mode="MarkdownV2",
        reply_markup=level_select_keyboard()
    )

async def select_level(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = update.effective_user.id
    ud = get_user(uid)
    level = query.data.replace("level_", "")
    ud["level"] = level
    ud["quiz_index"] = 0
    ud["quiz_score"] = 0
    ud["flashcard_index"] = 0
    ud["vocab_seen"] = []
    lvl = LEVELS[level]
    await query.answer(f"✅ Đã chọn {lvl['name']}!")
    await query.edit_message_text(
        f"{lvl['emoji']} *Cấp độ: {esc(lvl['name'])}*\n"
        f"_{esc(lvl['desc'])}_\n\n"
        "Bạn muốn học gì hôm nay\\?",
        parse_mode="MarkdownV2",
        reply_markup=main_menu_keyboard(level)
    )

async def menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = update.effective_user.id
    ud = get_user(uid)
    await query.answer()
    if not ud["level"]:
        await query.edit_message_text(
            "👇 Chọn cấp độ của bạn:", reply_markup=level_select_keyboard()
        )
        return
    level = ud["level"]
    lvl = LEVELS[level]
    await query.edit_message_text(
        f"{lvl['emoji']} *{esc(lvl['name'])}* \\| Bạn muốn học gì\\?",
        parse_mode="MarkdownV2",
        reply_markup=main_menu_keyboard(level)
    )

async def change_level(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🔄 *Chọn cấp độ mới:*",
        parse_mode="MarkdownV2",
        reply_markup=level_select_keyboard()
    )

# ── VOCABULARY ────────────────────────────────────────────────────────────────

async def send_vocab(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = update.effective_user.id
    ud = get_user(uid)
    if not ud["level"]:
        await query.answer("Chọn cấp độ trước nhé!")
        await query.edit_message_text("👇 Chọn cấp độ:", reply_markup=level_select_keyboard())
        return

    level = ud["level"]
    vocab_list = VOCABULARY[level]
    remaining = [v for v in vocab_list if v["word"] not in ud["vocab_seen"]]
    if not remaining:
        ud["vocab_seen"] = []
        remaining = vocab_list

    v = random.choice(remaining)
    ud["vocab_seen"].append(v["word"])
    lvl = LEVELS[level]

    text = (
        f"{lvl['emoji']} *\\[{esc(lvl['name'])}\\] Từ vựng mới*\n\n"
        f"🔤 *{esc(v['word'].upper())}*\n"
        f"🏷️ Chủ đề: _{esc(v['topic'])}_\n"
        f"🇻🇳 Nghĩa: *{esc(v['meaning'])}*\n\n"
        f"💬 Ví dụ: _{esc(v['example'])}_"
    )
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔄 Từ tiếp theo", callback_data="vocab"),
        back_to_menu_btn()
    ]])
    await query.answer()
    await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)

# ── QUIZ ──────────────────────────────────────────────────────────────────────

async def quiz_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = update.effective_user.id
    ud = get_user(uid)
    if not ud["level"]:
        await query.answer("Chọn cấp độ trước!")
        await query.edit_message_text("👇 Chọn cấp độ:", reply_markup=level_select_keyboard())
        return
    ud["quiz_index"] = 0
    ud["quiz_score"] = 0
    await query.answer()
    await _send_quiz_q(query, uid)

async def _send_quiz_q(query, uid):
    ud = get_user(uid)
    level = ud["level"]
    lvl = LEVELS[level]
    questions = QUIZZES[level]
    idx = ud["quiz_index"]

    if idx >= len(questions):
        score = ud["quiz_score"]
        total = len(questions)
        pct = score / total
        if pct == 1.0:   star = "🏆 Xuất sắc! Hoàn hảo!"
        elif pct >= 0.75: star = "🎉 Rất tốt! Cố gắng thêm nhé!"
        elif pct >= 0.5:  star = "📚 Khá tốt! Ôn thêm một chút nha!"
        else:             star = "💪 Cần cố gắng thêm! Bạn làm được!"
        text = (
            f"{lvl['emoji']} *Quiz {esc(lvl['name'])} hoàn thành\\!*\n\n"
            f"🎯 Điểm số: *{score}/{total}*\n"
            f"{esc(star)}"
        )
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("🔄 Làm lại", callback_data="quiz_start"),
            back_to_menu_btn()
        ]])
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)
        return

    q = questions[idx]
    text = (
        f"{lvl['emoji']} *\\[{esc(lvl['name'])}\\] Câu {idx+1}/{len(questions)}*\n\n"
        f"{esc(q['question'])}"
    )
    labels = ["🅰️", "🅱️", "🅲️", "🅳️"]
    buttons = [
        [InlineKeyboardButton(f"{labels[i]} {opt}", callback_data=f"qans_{i}")]
        for i, opt in enumerate(q["options"])
    ]
    await query.edit_message_text(text, parse_mode="MarkdownV2",
                                   reply_markup=InlineKeyboardMarkup(buttons))

async def quiz_answer(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = update.effective_user.id
    ud = get_user(uid)
    await query.answer()
    ans = int(query.data.split("_")[1])
    level = ud["level"]
    q = QUIZZES[level][ud["quiz_index"]]
    correct = q["answer"]
    if ans == correct:
        ud["quiz_score"] += 1
        fb = f"✅ *Chính xác\\!*\n\n{esc(q['explanation'])}"
    else:
        labels = ["A", "B", "C", "D"]
        fb = (
            f"❌ *Sai rồi\\!*\n\n"
            f"Đáp án đúng: *{labels[correct]}\\. {esc(q['options'][correct])}*\n\n"
            f"{esc(q['explanation'])}"
        )
    ud["quiz_index"] += 1
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("▶️ Câu tiếp", callback_data="quiz_next")
    ]])
    await query.edit_message_text(fb, parse_mode="MarkdownV2", reply_markup=kb)

async def quiz_next(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await _send_quiz_q(query, update.effective_user.id)

# ── GRAMMAR ───────────────────────────────────────────────────────────────────

async def send_grammar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = update.effective_user.id
    ud = get_user(uid)
    if not ud["level"]:
        await query.answer("Chọn cấp độ trước!")
        await query.edit_message_text("👇 Chọn cấp độ:", reply_markup=level_select_keyboard())
        return
    level = ud["level"]
    lvl = LEVELS[level]
    lessons = GRAMMAR[level]
    remaining = [l for l in lessons if l["title"] not in ud["grammar_seen"]]
    if not remaining:
        ud["grammar_seen"] = []
        remaining = lessons
    lesson = random.choice(remaining)
    ud["grammar_seen"].append(lesson["title"])

    text = (
        f"{lvl['emoji']} *\\[{esc(lvl['name'])}\\] Ngữ pháp*\n\n"
        f"📌 *{esc(lesson['title'])}*\n\n"
        f"{lesson['explanation']}\n\n"
        f"{esc(lesson['tip'])}"
    )
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔄 Bài khác", callback_data="grammar"),
        back_to_menu_btn()
    ]])
    await query.answer()
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

# ── FLASHCARD ─────────────────────────────────────────────────────────────────

async def send_flashcard(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = update.effective_user.id
    ud = get_user(uid)
    if not ud["level"]:
        await query.answer("Chọn cấp độ trước!")
        await query.edit_message_text("👇 Chọn cấp độ:", reply_markup=level_select_keyboard())
        return
    level = ud["level"]
    lvl = LEVELS[level]
    cards = FLASHCARDS[level]
    idx = ud["flashcard_index"] % len(cards)
    card = cards[idx]
    ud["flashcard_index"] += 1

    text = (
        f"{lvl['emoji']} *\\[{esc(lvl['name'])}\\] Flashcard {idx+1}/{len(cards)}*\n\n"
        f"{esc(card['front'])}"
    )
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("👁 Xem đáp án", callback_data=f"frev_{idx}_{level}")
    ]])
    await query.answer()
    await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)

async def flashcard_reveal(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    _, idx_s, level = query.data.split("_")
    idx = int(idx_s)
    card = FLASHCARDS[level][idx]
    lvl = LEVELS[level]
    text = (
        f"{lvl['emoji']} *\\[{esc(lvl['name'])}\\] Flashcard*\n\n"
        f"{esc(card['front'])}\n\n"
        f"━━━━━━━━━━━━\n\n"
        f"✅ {card['back']}"
    )
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("▶️ Thẻ tiếp", callback_data="flashcard"),
        back_to_menu_btn()
    ]])
    await query.answer()
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

# ── FALLBACK ──────────────────────────────────────────────────────────────────

async def unknown(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    ud = get_user(uid)
    if ud["level"]:
        await update.message.reply_text(
            f"Dùng menu để học nhé! 😊",
            reply_markup=main_menu_keyboard(ud["level"])
        )
    else:
        await update.message.reply_text(
            "Gõ /start để bắt đầu! 🎓",
            reply_markup=level_select_keyboard()
        )

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))

    app.add_handler(CallbackQueryHandler(select_level, pattern="^level_"))
    app.add_handler(CallbackQueryHandler(change_level, pattern="^change_level$"))
    app.add_handler(CallbackQueryHandler(menu, pattern="^menu$"))
    app.add_handler(CallbackQueryHandler(send_vocab, pattern="^vocab$"))
    app.add_handler(CallbackQueryHandler(quiz_start, pattern="^quiz_start$"))
    app.add_handler(CallbackQueryHandler(quiz_answer, pattern="^qans_"))
    app.add_handler(CallbackQueryHandler(quiz_next, pattern="^quiz_next$"))
    app.add_handler(CallbackQueryHandler(send_grammar, pattern="^grammar$"))
    app.add_handler(CallbackQueryHandler(send_flashcard, pattern="^flashcard$"))
    app.add_handler(CallbackQueryHandler(flashcard_reveal, pattern="^frev_"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    print("🎓 Cambridge English Bot đang chạy! Nhấn Ctrl+C để dừng.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
