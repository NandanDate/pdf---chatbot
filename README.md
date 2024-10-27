# 📄 PDF Chat-BOT

[![GitHub](https://img.shields.io/badge/GitHub-Repo-blue?logo=github)](https://github.com/NandanDatta/pdf-chatbot)  
A powerful solution to extract structured insights from PDFs containing text, tables, and images, combined with mechanisms for asking clarifying questions, linking text to images, and handling tabular data for a complete understanding of documents.

---

## 🚀 Overview
This project aims to develop a **PDF-based chatbot** that enables users to engage interactively with the content of PDFs. By extracting text, images, and tables, the chatbot offers enhanced insights through:
- Clarifying questions  
- **Text-to-image linking** for better context  
- **Table processing** for structured data extraction  

The bot helps users extract **accurate, efficient** insights from documents and handle complex information by breaking it into manageable parts. 

---

## 🎯 Objectives
- **Contextual Understanding**:  
  Ask clarifying questions to gain a full understanding of the PDF content.
  
- **Efficient Table Processing**:  
  Extract and structure tabular data efficiently for user queries.

- **Image-Text Linking**:  
  Seamlessly connect images with corresponding text to provide a holistic understanding of the document.

---

## 🛠️ System Workflow
1. **Input Processing**:  
   - The user uploads a PDF document, and the content is split into **text, tables, and images**.

2. **Text Preprocessing & Chunking**:  
   - The text is divided into **manageable parts** for easier processing.

3. **Vector Embedding**:  
   - Embed the processed text chunks into **vectors** for efficient retrieval.

4. **Storage**:  
   - Store the **vector embeddings** in Pinecone (a vector database) for quick search.

5. **UI Development**:  
   - Provide an **intuitive user interface** that allows users to upload PDFs and ask questions interactively.

6. **Query and Response**:  
   - Retrieve relevant information from the vector database to answer user questions accurately.

---

## 🧩 Features
- **Interactive Question & Answer Interface**:  
  Users can upload PDFs and ask **questions** about their content in real time.

- **Seamless Image-Text Linking**:  
  Connect images to their corresponding text sections for enhanced understanding.

- **Efficient Handling of Tables**:  
  Extract and interpret **tabular data** for easy comprehension and query processing.

---

## 💻 Tech Stack
- **Python** 🐍: For backend development and logic processing  
- **Pinecone**: Vector database for storing text embeddings  
- **UI Interface**: User-friendly web-based interface  
- **Vector Embeddings**: For document content storage and quick access

---


