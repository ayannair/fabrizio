'use client';
import { useState } from 'react';

export default function Home() {
  const [input, setInput] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    const res = await fetch('/api/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: input }),
    });
    const data = await res.json();
    setSummary(data.summary || 'No summary found.');
    setLoading(false);
  };

  return (
    <main className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">HereWeGo!PT</h1>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter player, club, or manager"
        className="border p-2 w-full mb-4"
      />
      <button
        onClick={handleSearch}
        className="bg-blue-600 text-white px-4 py-2 rounded"
        disabled={loading}
      >
        {loading ? 'Loading...' : 'Search'}
      </button>
      {summary && (
        <div className="mt-6 whitespace-pre-line border p-4 rounded">
          <h2 className="font-semibold mb-2">Summary</h2>
          <p>{summary}</p>
        </div>
      )}
    </main>
  );
}
