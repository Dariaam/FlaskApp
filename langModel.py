import ollama, chardet, docx, chromadb
from tkinter.filedialog import askopenfilename as ask
from nltk import sent_tokenize as st
import nltk

client = chromadb.PersistentClient()
nltk.download('punkt_tab')


def new_gettext(file):
    try:
        if file.endswith('.txt'):
            text = open(rf'{file}','rb')
            text_body = text.read()
            enc = chardet.detect(text_body).get("encoding")
            if enc and enc.lower() != "utf-8" and enc.lower() != "windows-1251":
                text_body = text_body.decode(enc)
                text_body = text_body.encode("utf-8")
                text_body = text_body.decode("utf-8")
                return text_body
            elif enc and enc.lower() == "windows-1251":
                text = open(rf'{file}', 'r', encoding = 'windows-1251')
                text_body = text.read()
                text.close()
                return text_body
            else:
                text = open(rf'{file}', 'r', encoding = 'UTF-8')
                text_body = text.read()
                text.close()
                return text_body
        elif file.endswith('.docx'):
            doc = docx.Document(rf'{file}')
            text = (paragraph.text for paragraph in doc.paragraphs)
            text_body = '\n'.join(text)
            return text_body
        else:
            pass
    except:
        pass

def create_db():
    collection = client.create_collection(name="bots")
    file = r"plants_bot.txt"
    text = new_gettext(file)
    sents = st(text)

    for i,d in enumerate(sents):
        print(i)
        try:
            response = ollama.embeddings(model="snowflake-arctic-embed:22m", prompt=d)
            embedding = response["embedding"]
            collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[d])
        except:
            print("OOPS")

def query(userprompt):
    collection = client.get_collection(name="bots")
    reprompt = ollama.generate(
    model = "llama3.1:8b",
    prompt=f"{userprompt}. Ответь на этот вопрос, будь точным, избегай новых деталей."
    )
    curPrompt = reprompt['response']
    response = []

    question = ollama.embeddings(
    prompt=curPrompt,
    model = 'snowflake-arctic-embed:22m'
    )
    results = collection.query(
    query_embeddings=[question["embedding"]],
    n_results=5 #Может, больше результатов брать?
    )
    [response.append(n) for i in results['documents'] for n in i]
    data = ' '.join(response)
    output = ollama.generate(
    model = "llama3.1:8b",
    prompt=f"Using this data: {data}. Respond to this prompt: {userprompt}"
    )
    return output['response']

#Создание Базы Знаний
if __name__ == "__main__":
    create_db()
