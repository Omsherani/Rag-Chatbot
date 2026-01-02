"use client";

import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, User, Bot } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { askQuestion } from '@/lib/api';

interface Message {
    role: 'user' | 'model';
    content: string;
}

export default function ChatInterface() {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            const data = await askQuestion(userMessage);
            const answer = data.answer || "Sorry, I couldn't get an answer.";
            setMessages(prev => [...prev, { role: 'model', content: answer }]);
        } catch (error) {
            setMessages(prev => [...prev, { role: 'model', content: "Error: Failed to connect to server." }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen max-w-4xl mx-auto bg-gray-900 text-gray-100 shadow-2xl overflow-hidden glass-panel">
            {/* Header */}
            <header className="p-4 border-b border-gray-800 bg-gray-950/50 backdrop-blur-md flex items-center justify-between sticky top-0 z-10">
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                    RAG Chatbot
                </h1>
                <div className="text-xs text-gray-500">Gemini Pro • Pinecone</div>
            </header>

            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-6 scrollbar-thin scrollbar-thumb-gray-700">
                {messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-full text-gray-500 space-y-4">
                        <Bot size={48} className="opacity-20" />
                        <p>Ready to answer your questions.</p>
                    </div>
                )}

                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        {msg.role === 'model' && (
                            <div className="w-8 h-8 rounded-full bg-blue-600/20 flex items-center justify-center border border-blue-500/30 flex-shrink-0">
                                <Bot size={16} className="text-blue-400" />
                            </div>
                        )}

                        <div className={`max-w-[80%] rounded-2xl p-4 ${msg.role === 'user'
                                ? 'bg-blue-600 text-white rounded-br-sm'
                                : 'bg-gray-800/80 border border-gray-700/50 rounded-bl-sm'
                            }`}>
                            {msg.role === 'model' ? (
                                <div className="prose prose-invert prose-sm">
                                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                                </div>
                            ) : (
                                <p className="whitespace-pre-wrap">{msg.content}</p>
                            )}
                        </div>

                        {msg.role === 'user' && (
                            <div className="w-8 h-8 rounded-full bg-purple-600/20 flex items-center justify-center border border-purple-500/30 flex-shrink-0">
                                <User size={16} className="text-purple-400" />
                            </div>
                        )}
                    </div>
                ))}

                {isLoading && (
                    <div className="flex gap-4">
                        <div className="w-8 h-8 rounded-full bg-blue-600/20 flex items-center justify-center border border-blue-500/30">
                            <Bot size={16} className="text-blue-400" />
                        </div>
                        <div className="bg-gray-800/80 border border-gray-700/50 rounded-2xl p-4 flex items-center gap-2">
                            <Loader2 size={16} className="animate-spin text-gray-400" />
                            <span className="text-sm text-gray-400">Thinking...</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-gray-950/50 border-t border-gray-800 backdrop-blur-md">
                <form onSubmit={handleSubmit} className="flex gap-2 relative">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask me anything..."
                        className="flex-1 bg-gray-900 border border-gray-700/50 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all placeholder:text-gray-600"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl px-4 transition-colors flex items-center justify-center"
                    >
                        <Send size={20} />
                    </button>
                </form>
                <div className="text-center mt-2 text-xs text-gray-600">
                    AI can make mistakes. Check important info.
                </div>
            </div>
        </div>
    );
}
