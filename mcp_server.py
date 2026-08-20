import os
import json
import requests
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from fastmcp import FastMCP
# pyrefly: ignore [missing-import]
from pymongo import MongoClient
# pyrefly: ignore [missing-import]
from bson import ObjectId

# Load environment variables (.env in root or backend/.env)
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "backend", ".env"))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/khat-app_db")
BACKEND_URL = os.getenv("BACKEND_URL", os.getenv("VITE_API_URL", "http://localhost:3000")).rstrip("/")
MCP_API_KEY = os.getenv("MCP_API_KEY")

# Initialize FastMCP Server
mcp = FastMCP("Khat-App MCP Server")

def mcp_headers():
    if not MCP_API_KEY:
        raise RuntimeError("MCP_API_KEY is not configured")

    return {
        "X-MCP-API-Key": MCP_API_KEY
    }

def get_db():
    client = MongoClient(MONGO_URI)
    # Parse DB name from MONGO_URI if present, else fallback to khat-app_db
    try:
        db = client.get_database()
    except Exception:
        db = client["khat-app_db"]
    return db

def _resolve_user_id(db, identifier: str) -> Optional[ObjectId]:
    if not identifier:
        return None
    identifier = str(identifier).strip()
    if ObjectId.is_valid(identifier):
        user = db.users.find_one({"_id": ObjectId(identifier)})
        if user:
            return user["_id"]

    user = db.users.find_one({"email": identifier.lower()})
    if user:
        return user["_id"]

    user = db.users.find_one({"clerkId": identifier})
    if user:
        return user["_id"]

    # Regex search as fallback
    user = db.users.find_one({"$or": [
        {"email": {"$regex": identifier, "$options": "i"}},
        {"fullName": {"$regex": identifier, "$options": "i"}}
    ]})
    if user:
        return user["_id"]

    return None

def _format_user(user: dict) -> dict:
    if not user:
        return {}
    return {
        "id": str(user.get("_id")),
        "email": user.get("email", ""),
        "fullName": user.get("fullName", ""),
        "profilePic": user.get("profilePic", ""),
        "createdAt": str(user.get("createdAt", "")) if user.get("createdAt") else None
    }

@mcp.tool()
def list_users() -> str:
    """Returns list of registered users in Khat-App."""
    try:
        res = requests.get(
            f"{BACKEND_URL}/api/mcp/users",
            headers=mcp_headers(),
            timeout=3
        )
        if res.status_code == 200:
            return json.dumps(res.json(), indent=2)
    except Exception:
        pass

    try:
        db = get_db()
        users = list(db.users.find({}, {"clerkId": 0}))
        formatted = [_format_user(u) for u in users]
        return json.dumps({"success": True, "count": len(formatted), "users": formatted}, indent=2)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@mcp.tool()
def search_users(query: str) -> str:
    """Search users in Khat-App by name or email query."""
    try:
        res = requests.get(
            f"{BACKEND_URL}/api/mcp/users",
            params={"q": query},
            headers=mcp_headers(),
            timeout=3
        )
        if res.status_code == 200:
            return json.dumps(res.json(), indent=2)
    except Exception:
        pass

    try:
        db = get_db()
        users = list(db.users.find({
            "$or": [
                {"fullName": {"$regex": query, "$options": "i"}},
                {"email": {"$regex": query, "$options": "i"}}
            ]
        }, {"clerkId": 0}))
        formatted = [_format_user(u) for u in users]
        return json.dumps({"success": True, "count": len(formatted), "users": formatted}, indent=2)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@mcp.tool()
def get_conversations(user_email_or_id: str) -> str:
    """Retrieve recent chat conversations for a given user (by email, ObjectId, or clerkId)."""
    try:
        res = requests.get(
            f"{BACKEND_URL}/api/mcp/conversations",
            params={"user": user_email_or_id},
            headers=mcp_headers(),
            timeout=3
        )
        if res.status_code == 200:
            return json.dumps(res.json(), indent=2)
    except Exception:
        pass

    try:
        db = get_db()
        user_id = _resolve_user_id(db, user_email_or_id)
        if not user_id:
            return json.dumps({"success": False, "error": f"User '{user_email_or_id}' not found"})

        pipeline = [
            {"$match": {"$or": [{"senderId": user_id}, {"receiverId": user_id}]}},
            {"$group": {
                "_id": {"$cond": [{"$eq": ["$senderId", user_id]}, "$receiverId", "$senderId"]},
                "lastMessageAt": {"$max": "$createdAt"},
                "lastMessageText": {"$last": "$text"}
            }},
            {"$sort": {"lastMessageAt": -1}},
            {"$lookup": {"from": "users", "localField": "_id", "foreignField": "_id", "as": "user"}},
            {"$unwind": "$user"}
        ]
        results = list(db.messages.aggregate(pipeline))
        conversations = []
        for r in results:
            u = r.get("user", {})
            conversations.append({
                "id": str(u.get("_id")),
                "email": u.get("email", ""),
                "fullName": u.get("fullName", ""),
                "profilePic": u.get("profilePic", ""),
                "lastMessageAt": str(r.get("lastMessageAt", "")),
                "lastMessageText": r.get("lastMessageText", "")
            })
        return json.dumps({"success": True, "count": len(conversations), "conversations": conversations}, indent=2)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@mcp.tool()
def get_messages(user1_identifier: str, user2_identifier: str, limit: int = 20) -> str:
    """Read chat message history between two users (identified by email, ID, or clerkId)."""
    try:
        res = requests.get(
            f"{BACKEND_URL}/api/mcp/messages",
            params={
                "user1": user1_identifier,
                "user2": user2_identifier,
                "limit": limit
            },
            headers=mcp_headers(),
            timeout=3
        )
        if res.status_code == 200:
            return json.dumps(res.json(), indent=2)
    except Exception:
        pass

    try:
        db = get_db()
        u1_id = _resolve_user_id(db, user1_identifier)
        u2_id = _resolve_user_id(db, user2_identifier)

        if not u1_id or not u2_id:
            return json.dumps({"success": False, "error": "One or both users not found"})

        messages = list(db.messages.find({
            "$or": [
                {"senderId": u1_id, "receiverId": u2_id},
                {"senderId": u2_id, "receiverId": u1_id}
            ]
        }).sort("createdAt", -1).limit(limit))

        messages.reverse()
        formatted = []
        for m in messages:
            formatted.append({
                "id": str(m.get("_id")),
                "senderId": str(m.get("senderId")),
                "receiverId": str(m.get("receiverId")),
                "text": m.get("text", ""),
                "image": m.get("image"),
                "video": m.get("video"),
                "createdAt": str(m.get("createdAt", ""))
            })
        return json.dumps({"success": True, "count": len(formatted), "messages": formatted}, indent=2)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

@mcp.tool()
def send_message(sender_identifier: str, receiver_identifier: str, text: str = "", image_url: Optional[str] = None, video_url: Optional[str] = None) -> str:
    """Send a real-time chat message from sender to receiver. Emits Socket.io real-time event to receiver if online."""
    try:
        res = requests.post(
            f"{BACKEND_URL}/api/mcp/send",
            json={
                "sender": sender_identifier,
                "receiver": receiver_identifier,
                "text": text,
                "image": image_url,
                "video": video_url
            },
            headers=mcp_headers(),
            timeout=5
        )
        if res.status_code in [200, 201]:
            return json.dumps(res.json(), indent=2)
        else:
            return json.dumps({"success": False, "error": res.json().get("message", res.text)})
    except Exception as e:
        # Fallback to direct DB write if backend server isn't reachable
        try:
            db = get_db()
            sender_id = _resolve_user_id(db, sender_identifier)
            receiver_id = _resolve_user_id(db, receiver_identifier)

            if not sender_id or not receiver_id:
                return json.dumps({"success": False, "error": "Sender or Receiver not found"})

            import datetime
            doc = {
                "senderId": sender_id,
                "receiverId": receiver_id,
                "text": text or "",
                "image": image_url,
                "video": video_url,
                "createdAt": datetime.datetime.utcnow(),
                "updatedAt": datetime.datetime.utcnow()
            }
            res = db.messages.insert_one(doc)
            return json.dumps({
                "success": True,
                "message": "Message saved to DB (backend offline, real-time socket skip)",
                "insertedId": str(res.inserted_id)
            }, indent=2)
        except Exception as db_err:
            return json.dumps({"success": False, "error": f"Failed to send message: {str(e)} | DB Error: {str(db_err)}"})

@mcp.tool()
def get_online_users() -> str:
    """Retrieve users currently online in Khat-App."""
    try:
        res = requests.get(
            f"{BACKEND_URL}/api/mcp/online",
            headers=mcp_headers(),
            timeout=3
        )
        if res.status_code == 200:
            return json.dumps(res.json(), indent=2)
    except Exception:
        pass
    return json.dumps({
        "success": True,
        "message": "Online status requires running Khat-App backend server",
        "onlineUsers": []
    }, indent=2)

if __name__ == "__main__":
    mcp.run()
