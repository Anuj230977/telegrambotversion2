# Import the regular expressions module for pattern matching
import re
import pyjokes
from simpleeval import simple_eval

# Dynamic categories that use custom logic

# List of templates to generate different ways a user might say a keyword
# For example, "hello", "hello!", "hello 😊", etc.
templates = [
    "{synonym}",
    "{synonym}!",
    "{synonym} 😊",
    "{synonym} please",
    "{synonym}?"
]
 # Dictionary of categories, each with a list of synonyms/phrases users might use
 # This helps the bot recognize many ways to say the same thing (like greetings, thanks, etc.)
synonym_lists = {
    "greetings": [
        "hello", "hi", "hey", "greetings", "good morning", "good afternoon",
        "good evening", "hiya", "what's up", "yo", "hey there", "hello there",
        "hiya", "sup", "howdy", "hello!", "hi!", "hey!", "greetings!", "salutations"
    ],
    "farewells": [
        "bye", "goodbye", "see you", "see ya", "later", "farewell",
        "take care", "catch you later", "bye-bye", "ciao", "adios", "peace out",
        "toodle-oo", "cheerio", "bye!", "goodbye!", "see you!", "later!",
        "take care!", "farewell!"
    ],
    "thanks": [
        "thank you", "thanks", "thx", "thank you so much", "thanks a lot",
        "much appreciated", "thanks!", "thank you!", "ty", "cheers",
        "gratitude", "I appreciate it", "I owe you one", "thanks buddy",
        "thanks pal", "thanks friend", "thanks that helps", "thanks very much",
        "thanks 😊", "thanks 🙂"
    ],
    "apologies": [
        "sorry", "my apologies", "I apologize", "pardon me", "excuse me",
        "oops", "whoops", "mea culpa", "sorry!", "my bad", "forgive me",
        "apologies", "I messed up", "that was my mistake", "I didn't mean that",
        "so sorry", "I'm sorry", "sorry about that", "sorry everyone", "sry"
    ],
    "wellbeing": [
        "how are you", "how's it going", "how do you do", "how have you been",
        "what's up", "what's new", "how are things", "how do you feel",
        "how are you doing", "how r you", "are you okay", "how's life",
        "how r u", "how are you?", "how's it going?", "how do you do?",
        "how have you been?", "what's up?", "what's new?", "are you well"
    ],
    "name_queries": [
        "what's your name", "who are you", "what are you called", "your name?",
        "name?", "who you are", "may I know your name", "tell me your name",
        "who am I talking to", "what should I call you", "your name",
        "who you", "I want your name", "your identity", "introduce yourself",
        "what do I call you", "you are", "you're", "your new name", "who is this"
    ],
    "origin_queries": [
        "where are you from", "origin", "where do you live", "where do you come from",
        "your origin", "born where", "from where", "location", "residence",
        "your hometown", "where u from", "where are you", "domain", "source",
        "where do you stay", "geolocation", "in what country", "in what city",
        "earth location", "virtual home"
    ],
    "joke_requests": [
        "tell me a joke", "joke", "make me laugh", "funny", "say something funny",
        "humor me", "one-liner", "pun", "knock knock", "got any jokes",
        "joke please", "a joke", "funny joke", "tell joke", "tell me something funny",
        "jokes", "comedian mode", "I'm bored", "cheer me up", "lighten the mood"
    ],
    "help_requests": [
        "help", "assist me", "I need help", "can you help me", "support",
        "help please", "aid me", "I need assistance", "guide me", "help!",
        "assist", "help me out", "give me assistance", "lend me a hand",
        "I need a hand", "how to", "instruction", "tutorial", "guide",
        "walk me through"
    ],
    "weather_queries": [
        "what's the weather", "weather", "current weather", "forecast",
        "how's the weather", "weather please", "weather today", "rain or shine",
        "temperature", "is it raining", "is it sunny", "weather update",
        "weather report", "weather now", "will it rain", "what's the forecast",
        "weather?", "weather??", "tell weather", "weather info"
    ],
    "compliments": [
        "you're smart", "you're funny", "nice bot", "cool", "great job", "well done",
        "you rock", "you're awesome", "impressive", "brilliant", "you're helpful", "good bot",
        "smart bot", "friendly bot", "you're kind", "so intelligent", "amazing bot", "i like you",
        "good assistant", "you nailed it"
    ],
    "food_talk": [
        "i'm hungry", "what to eat", "food suggestions", "give me a recipe", "suggest a dish",
        "best food", "i want food", "what's cooking", "favorite snack", "tasty", "yum", "what's for dinner",
        "what's for lunch", "hungry", "thirsty", "drink ideas", "healthy food", "junk food", "make me food",
        "cook something"
    ],
    "fun_requests": [
        "make me smile", "something fun", "fun please", "bored", "entertain me", "tell a fun fact",
        "surprise me", "interesting stuff", "impress me", "amuse me", "give me trivia", "make it exciting",
        "spin a story", "curious stuff", "cool stuff", "funny fact", "exciting", "wow me", "show talent",
        "fun time"
    ],
    "emotion_check": [
        "i'm sad", "feeling down", "not okay", "cheer me up", "bad day", "tough time", "need support",
        "feeling low", "depressed", "frustrated", "lonely", "upset", "help emotionally", "talk to me",
        "make me feel better", "listen to me", "i need a friend", "comfort me", "uplift me", "dark mood"
    ],
    "tech_queries": [
        "what is ai", "what is chatbot", "tech news", "technology updates", "explain machine learning",
        "how do bots work", "tell me about neural networks", "what is python", "what's programming",
        "help with code", "explain algorithms", "what's github", "learn tech", "teach me tech",
        "what is computing", "what is cloud", "digital world", "ai facts", "learn python", "what is coding"
    ],
    "motivation": [
        "motivate me", "encourage me", "give me advice", "pep talk", "life advice", "i need inspiration",
        "say something inspiring", "uplift me", "power quote", "mental boost", "positive words",
        "tell me something good", "self belief", "dream big", "confidence boost", "fire me up",
        "help me focus", "goal setting", "get productive", "help me move forward"
    ],
    "weather_fun": [
        "sunny day", "rainy mood", "cloud talk", "thunder vibes", "weather jokes", "what's outside",
        "humidity", "cold", "hot", "mild weather", "extreme weather", "snow talk", "storm",
        "weather emotion", "fog", "chilly", "heatwave", "monsoon", "climate chat", "season talk"
    ],
    "random_queries": [
        "random", "give me anything", "surprise me", "any fact", "random thought", "drop something",
        "hit me with a topic", "freestyle", "tell me anything", "pick a theme", "share a story",
        "what's next", "think for me", "what's trending", "what's cool", "no idea", "anything works",
        "show talent", "your choice", "go wild"
    ],
    "language_talk": [
        "teach me hindi", "teach me english", "translate", "language tip", "talk in spanish",
        "say hello in french", "help with grammar", "word meaning", "language joke", "common phrases",
        "language facts", "how to greet", "international greeting", "easy phrases", "cool words",
        "simple sentences", "word game", "teach language", "learn language", "how to say it"
    ],
    "math_queries": [
        "solve math", "calculate", "math help", "addition", "subtraction", "multiply", "divide",
        "math tip", "math joke", "solve equation", "help with numbers", "math trivia",
        "how to calculate", "simple math", "complex math", "what is algebra", "math trick", "number facts",
        "math hacks", "math logic"
    ],
    "study_tips": [
        "study tips", "how to study", "study advice", "help me study", "study smarter",
        "study hack", "study tricks", "study routine", "study plan", "study help"
    ],
    "motivation_quotes": [
        "motivation quote", "inspire me", "give me a quote", "quote of the day", "inspirational quote",
        "motivational saying", "uplifting quote", "positive quote", "life quote", "success quote"
    ],
    "programming_help": [
        "help with python", "coding help", "programming question", "debug my code", "fix my code",
        "explain this code", "code error", "coding advice", "programming tips", "how to code"
    ],
    "funny_memes": [
        "send a meme", "funny meme", "make me laugh more", "show me a meme", "meme please",
        "give me a meme", "share a meme", "random meme", "meme time", "meme bot"
    ],
    "book_recommendations": [
        "book suggestion", "recommend a book", "good books", "what to read", "book to read",
        "reading list", "book advice", "book ideas", "suggest a novel", "book rec"
    ]
}
 # Predefined responses for each category
 # When a user's message matches a category, the bot replies with the corresponding response
responses = {
    "greetings":       "Hello! How can I assist you today?",
    "farewells":       "Goodbye! Have a great day!",
    "thanks":          "You're welcome!",
    "apologies":       "No worries!",
    "wellbeing":       "I'm a bot, but I'm functioning perfectly!",
    "name_queries":    "I'm Copilot, your friendly assistant!",
    "origin_queries":  "I reside in the cloud 🌩️",
    "help_requests":   "Sure, what do you need help with?",
    "weather_queries": "I don't have real-time weather, but it's always sunny in code!",
    "compliments":      "You're too kind 😊 I'm always here to help!",
    "food_talk":        "Craving something tasty? How about paneer butter masala or a cheesy sandwich?",
    "fun_requests":     "Sure! Did you know octopuses have three hearts? 🐙",
    "emotion_check":    "You’re not alone. I’m here, and I believe in you 🫶",
    "tech_queries":     "AI is like giving a brain to machines—want a deep dive?",
    "motivation":       "Push forward, even when it’s tough. You’ve got this 💪",
    "weather_fun":      "Rain or shine, I’m always online ☀️🌧️",
    "random_queries":   "Here’s something cool: bananas are berries, but strawberries aren’t 🍓🤯",
    "language_talk":    "‘Bonjour’ means hello in French! Want more?",
    "study_tips":      "Break your study sessions into short, focused intervals and take regular breaks. Stay hydrated and review your notes often!",
    "motivation_quotes": "“The only way to do great work is to love what you do.” – Steve Jobs",
    "programming_help": "Describe your programming problem, and I'll do my best to help! If you have an error message, please share it.",
    "funny_memes":     "Why did the computer show up at work late? It had a hard drive! (Sorry, I can't send images, but I can tell jokes!)",
    "book_recommendations": "I recommend 'Atomic Habits' by James Clear for self-improvement, or 'The Alchemist' by Paulo Coelho for inspiration.",
}
# Dynamic categories that use custom logic
dynamic_categories = ["joke_requests", "math_queries"]
# Build regex patterns for static responses only
pattern_response_pairs = {}
for category, synonyms in synonym_lists.items():
    if category in dynamic_categories:
        continue  # Skip dynamic ones
    for synonym in synonyms:
        for tmpl in templates:
            phrase = tmpl.format(synonym=synonym)
            pattern = re.compile(r"\b" + re.escape(phrase.lower()) + r"\b", re.IGNORECASE)
            pattern_response_pairs[pattern] = category

# Response generator with dynamic logic
def generate_response(category, user_input=None):
    if category == "joke_requests":
        return pyjokes.get_joke()
    elif category == "math_queries":
        try:
            math_pattern = r'^[\d\s\+\-\*/\(\)\.]+$'
            if not re.match(math_pattern, user_input.strip()):
                return "Sure! Send me a math expression like '4 + 3 * 2' and I’ll solve it."
            result = simple_eval(user_input)
            return f"The result is: {result}"
        except:
            return "Hmm... I couldn't solve that expression. Try a simpler one like '4 + 3 * 2'."
    else:
        return responses.get(category, "I'm still learning. Try asking about jokes, greetings, or weather!")

# Unified input handler
def handle_response(text: str) -> str:
    if re.match(r'^[\d\s\+\-\*/\(\)\.]+$', text):
        return generate_response("math_queries", text)
    cleaned_text = text.lower().strip()

    for pattern, category in pattern_response_pairs.items():
        if pattern.search(cleaned_text):
            return generate_response(category, cleaned_text)

    for category in dynamic_categories:
        for synonym in synonym_lists[category]:
            if synonym in cleaned_text:
                return generate_response(category, cleaned_text)

    return "I'm still learning. Try asking about jokes, greetings, or weather!"
