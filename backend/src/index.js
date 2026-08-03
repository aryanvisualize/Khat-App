import express from "express";
import "dotenv/config";

import fs from "fs";
import path from "path";

import job from "./cronjob.js";
import clerkWebhook from "./webhooks/clerk.webhook.js";

import User from "./models/user.model.js";
import { connectDB } from "./lib/db.js";

import { clerkMiddleware } from "@clerk/express";
import cors from "cors";

const app = express();
const PORT = process.env.PORT || 3000;
const FRONTEND_URL = process.env.FRONTEND_URL;

const publicDir = path.join(process.cwd(), "public");

app.use('api/webhooks/clerk',express.raw({type:"application/json"}) ,clerkWebhook)

app.use(express.json());
app.use(clerkMiddleware());
app.use(cors({ origin: FRONTEND_URL, credentials: true }));

app.get("/health", (req, res) => {
  res.status(200).json({ status: "ok" });
});

if(fs.existsSync(publicDir)){
  app.use(express.static(publicDir));
  app.get("/{*any}",(req, res, next)=>{
    res.sendFile(path.join(publicDir, "index.html"), (err)=> next(err));
  });
}

app.listen(PORT, () => {
  connectDB();
  console.log(`Server is running on http://localhost:${PORT}`);
  if(process.env.NODE_ENV === "production") {
    job.start();
  }
});
