import toast from "react-hot-toast"

function ChatPage() {
  return (
    <div>
      Chatpage
      <button onClick={()=> toast.success("You clicked")}>Click me</button>
    </div>
  )
}

export default ChatPage
