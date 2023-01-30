from db import session, User, Message, Chat, ChatMedia, Media, Contact

user = session.query(User).filter(User.user_id).first()
# chat = session.query(Chat).filter(user in chat.users).first()

print(chat)