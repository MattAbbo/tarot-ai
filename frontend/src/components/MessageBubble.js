import React from 'react';

const MessageBubble = ({ message }) => {
  return (
    <div className="max-w-2xl mx-auto my-8 p-6 bg-gray-800 rounded-lg shadow-lg border border-purple-500">
      <p className="text-gray-200 leading-relaxed whitespace-pre-wrap">{message}</p>
    </div>
  );
};

export default MessageBubble;
