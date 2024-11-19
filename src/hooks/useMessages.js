const useMessages = () => {
    const [messages, setMessages] = useState([
      {
        id: '1',
        content: 'Welcome to Tarot AI!',
        type: 'ai',
      },
    ]);
  
    const addMessage = (content, type, card = null) => {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          content,
          type,
          card,
        },
      ]);
    };
  
    const removeMessage = (messageContent) => {
      setMessages((prev) => prev.filter((m) => m.content !== messageContent));
    };
  
    return { messages, addMessage, removeMessage };
  };
  
  export default useMessages;