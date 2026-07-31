# 🎓 AIT AI Assistant – Website RAG Chatbot

An AI-powered chatbot that answers questions about **Atria Institute of Technology (AIT)** using information collected from the official AIT website.

The project uses **Retrieval-Augmented Generation (RAG)**, which allows the chatbot to search relevant college information before generating an answer. This helps provide more relevant, context-based responses and reduces incorrect information.

---

## 📌 Project Overview

Students often need information about:

* College departments
* Courses
* Admissions
* Placements
* Campus facilities
* Faculty
* Contact information
* Events and activities

Searching through many webpages can take time. This project provides a single AI chatbot interface where users can ask questions in natural language.

The chatbot collects publicly available information from the official AIT website, converts the information into vector embeddings, stores it in **ChromaDB**, and retrieves relevant content when a user asks a question.

The retrieved information is then provided to the **Google Gemini AI model**, which generates a clear and easy-to-understand answer.

---

## ✨ Features

* 🌐 Automatically collects information from the official AIT website
* 🤖 AI-powered conversational chatbot
* 🔎 Searches relevant website content using semantic search
* 🧠 Uses Retrieval-Augmented Generation (RAG)
* 📚 Stores website information in ChromaDB
* 💬 Answers questions in natural language
* 🔗 Displays source webpages used for answers
* 🧹 Removes unnecessary webpage content
* 🔄 Supports knowledge-base updates
* 🖥️ Simple and user-friendly Streamlit interface
* 🛡️ Reduces hallucinations by using retrieved website content
* ⚡ Provides quick access to college information

---

## 🧠 What is RAG?

**RAG stands for Retrieval-Augmented Generation.**

RAG combines information retrieval with Generative AI.

Instead of asking the AI model to answer only from its general knowledge, the system first searches the AIT website knowledge base and retrieves relevant information.

The retrieved information is then given to the Gemini model, which generates the final response.

### RAG Process

```text
User Question
      ↓
Convert Question into an Embedding
      ↓
Search ChromaDB
      ↓
Retrieve Relevant AIT Website Content
      ↓
Send Context to Gemini AI
      ↓
Generate Final Answer
      ↓
Display Answer and Sources
```

---

## 🏗️ System Architecture

```text
                 ┌─────────────────────┐
                 │ Official AIT Website │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Python Web Scraper  │
                 │ BeautifulSoup       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Text Cleaning and   │
                 │ Text Chunking       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ SentenceTransformer │
                 │ Embedding Model     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ ChromaDB Vector     │
                 │ Database            │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ User Question       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Semantic Search     │
                 │ and Retrieval       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Google Gemini API   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ AI Answer + Sources │
                 └─────────────────────┘
```

---

## 🛠️ Technologies Used

| Technology            | Purpose                                |
| --------------------- | -------------------------------------- |
| Python                | Main programming language              |
| Streamlit             | Creates the chatbot web interface      |
| BeautifulSoup         | Extracts information from webpages     |
| Requests              | Downloads website pages                |
| Sentence Transformers | Converts text into vector embeddings   |
| ChromaDB              | Stores and searches website embeddings |
| Google Gemini API     | Generates AI responses                 |
| Python-dotenv         | Loads the API key securely             |
| TQDM                  | Displays website crawling progress     |

---

## 📂 Project Structure

```text
AIT_RAG_CHATBOT/
│
├── app.py
├── scraper.py
├── build_knowledge_base.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
└── chroma_db/
```

### File Description

| File                      | Description                                                |
| ------------------------- | ---------------------------------------------------------- |
| `app.py`                  | Main Streamlit chatbot application                         |
| `scraper.py`              | Crawls and extracts information from the AIT website       |
| `build_knowledge_base.py` | Creates embeddings and stores them in ChromaDB             |
| `requirements.txt`        | Contains required Python libraries                         |
| `.env`                    | Stores the Gemini API key                                  |
| `.gitignore`              | Prevents private and unnecessary files from being uploaded |
| `README.md`               | Project documentation                                      |
| `chroma_db/`              | Stores the generated vector database                       |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

Move into the project folder:

```bash
cd AIT_RAG_CHATBOT
```

---

### 2. Create a virtual environment

```bash
python -m venv .venv
```

---

### 3. Activate the virtual environment

For Windows:

```bash
.venv\Scripts\activate
```

For macOS or Linux:

```bash
source .venv/bin/activate
```

---

### 4. Install the required libraries

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

---

## 🔑 Gemini API Setup

Create a Gemini API key using Google AI Studio.

Create a file named:

```text
.env
```

Add your API key:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Example:

```env
GEMINI_API_KEY=AQxxxxxxxxxxxxxxxx
```

Do not add spaces around the `=` symbol.

Do not upload the `.env` file to GitHub.

---

## 📚 Build the AIT Knowledge Base

Run:

```bash
python build_knowledge_base.py
```

The program will:

1. Visit the AIT website.
2. Collect publicly available webpage content.
3. Remove unnecessary webpage elements.
4. Clean the extracted text.
5. Divide the text into smaller chunks.
6. Convert the chunks into embeddings.
7. Store the embeddings in ChromaDB.

After successful completion, you may see:

```text
Knowledge base created successfully!

Pages collected: 50
Text chunks stored: 400
```

The exact number of pages and chunks may be different because website content can change.

---

## 🚀 Run the Chatbot

Run:

```bash
streamlit run app.py
```

The application will open in your browser.

If it does not open automatically, visit:

```text
http://localhost:8501
```

---

## 💬 Example Questions

Try asking:

```text
Tell me about Atria Institute of Technology.
```

```text
What departments are available at AIT?
```

```text
What information is available about admissions?
```

```text
Explain the placement activities at AIT.
```

```text
What facilities are available?
```

```text
How can I contact AIT?
```

```text
Tell me about the AIML department.
```

---

## 🔄 Update the Knowledge Base

The AIT website may change over time.

To collect the latest website information and rebuild the vector database, run:

```bash
python build_knowledge_base.py
```

This removes the old knowledge base and creates a new one using the latest available website content.

---

## 🔐 Security

The Gemini API key is private.

Do not:

* Share the API key publicly
* Upload the `.env` file to GitHub
* Add the API key directly to `app.py`
* Share screenshots containing the API key

The `.gitignore` file should contain:

```text
.env
.venv/
__pycache__/
chroma_db/
*.pyc
```

---

## ⚠️ Limitations

* The chatbot can answer only from the information collected from the AIT website.
* Some pages may not be collected because of website restrictions or changes.
* Information such as fees, admission dates, placement statistics, and contact details may change.
* Users should verify important information through official college sources.
* The quality of answers depends on the quality and availability of website content.
* The chatbot may not find information that is not published on the website.

---

## 🔮 Future Improvements

The project can be improved by adding:

* Voice input and voice responses
* Student login system
* Multilingual support
* WhatsApp integration
* PDF document support
* College admission enquiry forms
* Admin dashboard
* Feedback system
* Conversation analytics
* Real-time college announcements
* Firebase or MySQL integration
* Deployment using Streamlit Cloud or Google Cloud
* Better citation and source ranking

---

## 🎯 Project Objective

The main objective of this project is to provide an intelligent and easy-to-use college information assistant.

The chatbot helps students quickly find information without manually searching through multiple webpages.

The project also demonstrates the practical use of:

* Generative AI
* Retrieval-Augmented Generation
* Natural Language Processing
* Web Scraping
* Text Embeddings
* Vector Databases
* Semantic Search
* Conversational AI

---

## 📊 Expected Output

The user enters a question:

> Is hostel accommodation available?

The system:

1. Searches the AIT website knowledge base.
2. Finds relevant hostel information.
3. Sends the retrieved content to Gemini.
4. Generates a clear answer.
5. Displays the source webpage.

If no relevant information is found, the chatbot responds:

> I could not find this information in the current AIT website data. Please verify the information through the official AIT website or contact the college directly.

---

## 👨‍💻 Author

**Shaik Sandhani**

B.Tech – Artificial Intelligence and Machine Learning

Atria Institute of Technology

---

## 📄 License

This project is created for educational and academic purposes.

The AIT website content belongs to its respective owners. The chatbot uses publicly available website information for educational information retrieval.
