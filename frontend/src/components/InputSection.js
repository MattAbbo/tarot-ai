import React, { useState } from 'react';

const InputSection = () => {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Implement question submission logic
    setQuestion('');
  };

  return (
    <div className="mt-8">
      <form onSubmit={handleSubmit} className="max-w-2xl mx-auto">
        <div className="flex flex-col space-y-4">
          <label htmlFor="question" className="text-lg text-purple-300">
            Ask your question:
          </label>
          <textarea
            id="question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="p-3 rounded-lg bg-gray-800 text-white border border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500"
            rows="3"
            placeholder="What would you like to know?"
          />
          <button
            type="submit"
            className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors"
          >
            Ask
          </button>
        </div>
      </form>
    </div>
  );
};

export default InputSection;
