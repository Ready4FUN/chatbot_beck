from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

# Разрешаем кросс-доменные запросы (если необходимо)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get():
    return HTMLResponse("Chatbot Server Running")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        response = process_message(data)
        await websocket.send_text(response)


# Словарь ключевых слов и ответов
keywords_responses = {
    "привет": "Привет! Как я могу вам помочь?",
    "вода": "Вода будет отключена для профилактических работ с 10:00 до 14:00.",
    "электричество": "Плановое отключение электричества запланировано на 15 июня с 09:00 до 17:00.",
    "отопление": "Отопительный сезон начнётся 1 октября.",
    "газ": "Газовые службы проводят проверки с 8:00 до 18:00 ежедневно.",
    "ремонт": "Ремонтные работы в подъезде будут завершены к концу недели.",
    "подвал": "Плановая проверка подвалов запланирована на следующую неделю.",
    "дворник": "Дворник работает с 6:00 до 14:00 каждый день.",
    "лифты": "Лифты будут проверены на техническое обслуживание в пятницу.",
    "счетчики": "Поверка счетчиков будет проводиться 20 июля.",
    "вывоз мусора": "Вывоз мусора производится ежедневно в 7:00.",
    "управляющая компания": "Контактный телефон управляющей компании: +7 (123) 456-78-90.",
    "жалобы": "Вы можете оставить жалобу на сайте управляющей компании.",
    "освещение": "Освещение во дворе будет восстановлено к концу месяца.",
    "парковка": "Парковочные места для жильцов находятся во дворе.",
    "тарифы": "Актуальные тарифы на коммунальные услуги можно узнать на сайте вашей управляющей компании.",
}

# Компилируем регулярное выражение для всех ключевых слов
keywords_pattern = re.compile("|".join(re.escape(keyword) for keyword in keywords_responses.keys()))

def process_message(message: str) -> str:
    message_lower = message.lower()
    match = keywords_pattern.search(message_lower)
    if match:
        return keywords_responses[match.group(0)]
    return "Я этого не понял. Не могли бы вы перефразировать?"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)