from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://adarshthakare:test1234@cluster0.cpyxkfa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URI)
db = client["AIBase"]
