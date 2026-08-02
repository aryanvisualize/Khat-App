import express from 'express';
import 'dotenv/config';
const app = express();
const PORT = process.env.PORT || 3000;

console.log("DB_URL=",process.env.DB_URL)
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});