# 🌾 Farmer.Chat: Agentic AI for Digital Agriculture Extension

**Farmer.Chat** adalah platform **Agentic AI** yang dirancang untuk mendemokrasi akses informasi bagi petani kecil. Proyek ini mentransformasi AI dari sekadar chatbot pasif menjadi "Penyuluh Pertanian Digital" yang proaktif, multimodal, dan sangat kontekstual.

---

## 🚀 Fitur Utama

* **Multimodal Interaction:** Mendukung input suara (dialek lokal) dan foto tanaman untuk mengatasi hambatan literasi digital.
* **Computer Vision Diagnosis:** Identifikasi penyakit dan hama secara instan melalui analisis gambar kamera ponsel.
* **Contextual Reasoning:** Integrasi otomatis dengan data GPS, cuaca real-time, dan histori lahan untuk saran yang akurat secara geografis.
* **Proactive Engagement:** Agen secara otonom mengirimkan peringatan dini cuaca dan tindak lanjut (*follow-up*) kondisi tanaman tanpa harus ditanya kembali.
* **Market Intelligence:** Menyediakan informasi harga pasar terkini untuk melindungi petani dari permainan harga tengkulak.

## 🏗️ Tech Stack

| Komponen | Teknologi |
| :--- | :--- |
| **LLM Backbone** | Llama 3 / GPT-4o |
| **Orchestration** | LangChain / CrewAI |
| **Knowledge Base** | RAG (Pinecone / Milvus) dengan dokumen riset pertanian |
| **Computer Vision** | TensorFlow / PyTorch (PlantVillage Dataset) |
| **Speech Engine** | OpenAI Whisper (STT) & Azure/ElevenLabs (TTS) |
| **Deployment** | WhatsApp Business API / Telegram Bot |

## 🧠 Mengapa "Agentic"?

Tidak seperti chatbot tradisional, Farmer.Chat memiliki **otonomi**. Jika petani mengeluhkan daun layu, agen secara mandiri memutuskan untuk mengecek data curah hujan seminggu terakhir sebelum memberikan diagnosis. 

Agen bekerja secara **iteratif**—mengevaluasi keberhasilan saran sebelumnya melalui foto susulan dan menyesuaikan rekomendasi secara proaktif jika kondisi lapangan berubah (misal: prediksi hujan mendadak yang membatalkan jadwal pemupukan).

## 🛠️ Kontribusi

Kami menyambut kontribusi dari pengembang AI, agronomis, dan pegiat teknologi pertanian untuk:
1. Pengembangan model dialek lokal (Regional STT/TTS).
2. Optimasi dataset visi komputer untuk tanaman tropis.
3. Integrasi sensor IoT pertanian dan data satelit.

---
*Inspired by Digital Green's vision to empower smallholder farmers through technology.*
