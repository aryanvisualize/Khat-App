# 💬 Khat - Full Stack Real-Time Chat Application

A modern, production-ready real-time chat application built with the MERN stack, featuring secure authentication, instant messaging, online presence, media sharing, customizable themes, and a beautiful responsive UI.

---

## ✨ Features

- 💬 Real-Time One-to-One Messaging
- ⚡ Instant Communication with Socket.io
- 🔐 Secure Authentication with Clerk
- 👤 User Management & Profile Sync
- 🟢 Online User Presence Indicator
- 📩 Recent Conversations Sidebar
- 🔍 Search Users Instantly
- 🖼️ Image Sharing Support
- 🎥 Video Sharing Support
- ☁️ Image & Video Uploads with ImageKit
- 🌙 Light & Dark Mode
- 🎨 11 Beautiful Color Themes
- 🖼️ 13 Custom Chat Wallpapers
- 🔊 Optional Keyboard Sound Effects
- 📱 Fully Responsive Design
- ⚛️ Global State Management with Zustand
- 📦 REST API built with Express.js
- 🗄️ MongoDB Database Integration
- 🔒 Protected Routes & Authentication Middleware
- 🔄 Real-Time Socket Connection Management
- 📁 File Upload Handling with Multer
- 📡 Clerk Webhooks for Automatic User Sync
- 🚀 Production Ready Deployment
- 📂 Clean & Scalable Folder Structure

---

# 🛠️ Tech Stack

## Frontend

- React
- Vite
- Tailwind CSS
- HeroUI
- Zustand
- Axios
- Socket.io Client
- React Router DOM
- React Hot Toast / React Toastify
- Lucide React

---

## Backend

- Node.js
- Express.js
- MongoDB
- Mongoose
- Socket.io
- Clerk Authentication
- ImageKit
- Multer
- dotenv

---

## Database

- MongoDB Atlas

---

## Authentication

- Clerk

---

## Media Storage

- ImageKit

---

# 📁 Project Structure

```text
khat-app/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── src/
│   │   ├── controllers/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── lib/
│   │   ├── seeds/
│   │   └── server.js
│   │
│   └── package.json
│
└── README.md
```

---

# ⚙️ Environment Variables

## Backend (`backend/.env`)

```env
PORT=5001

NODE_ENV=development

MONGO_URI=your_mongodb_connection_string

FRONTEND_URL=http://localhost:5173

CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
CLERK_WEBHOOK_SIGNING_SECRET=your_webhook_secret

IMAGEKIT_PUBLIC_KEY=your_imagekit_public_key
IMAGEKIT_PRIVATE_KEY=your_imagekit_private_key
IMAGEKIT_URL_ENDPOINT=your_imagekit_url_endpoint
```

---

## Frontend (`frontend/.env`)

```env
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
VITE_API_URL=http://localhost:5001
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/khat-app.git

cd khat-app
```

---

## 2. Install Dependencies

### Backend

```bash
cd backend

npm install
```

### Frontend

```bash
cd frontend

npm install
```

---

## 3. Configure Environment Variables

Create `.env` files inside both the **frontend** and **backend** directories using the examples above.

---

## 4. Seed the Database

```bash
cd backend

npm run db:seed
```

---

## 5. Run the Backend

```bash
npm run dev
```

---

## 6. Run the Frontend

```bash
cd frontend

npm run dev
```

---

## 🌐 Live Demo

**Render:** https://khat-app.onrender.com

---


# 🔥 Core Functionalities

### Authentication

- Clerk Authentication
- Protected Routes
- Automatic User Sync via Webhooks

### Messaging

- Real-Time Chat
- Instant Delivery
- Conversation History
- Recent Chats

### Media

- Image Upload
- Video Upload
- ImageKit CDN Integration

### User Experience

- Online Presence
- Search Users
- Responsive Design
- Theme Switching
- Wallpaper Customization
- Keyboard Sound Effects

---

# 📦 API Features

- User Authentication
- Fetch Users
- Fetch Conversations
- Get Messages
- Send Messages
- Upload Media
- Socket.io Events
- Online Users Tracking

---

# 🚀 Deployment

This project can be deployed using:

- Render
- Docker
- MongoDB Atlas
- ImageKit CDN
- Clerk Authentication


---


# 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Aryan Rastogi**

If you enjoyed this project, don't forget to ⭐ the repository!