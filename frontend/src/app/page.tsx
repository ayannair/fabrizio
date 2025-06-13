'use client';
import { useState, useEffect } from 'react';

export default function Home() {
  const [input, setInput] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [keywords, setKeywords] = useState<string[]>([]);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [timeline, setTimeline] = useState<{ date: string; summary: string }[]>([]);

  useEffect(() => {
    const fetchKeywords = async () => {
      const res = await fetch('https://herewegopt-919615563b34.herokuapp.com//api/keywords');
      const data = await res.json();
      const keywords = data;
      setKeywords(keywords);
    };
    fetchKeywords();
  }, []);

  useEffect(() => {
    if (input.length < 2) {
      setSuggestions([]);
      return;
    }

    const filtered = keywords.filter((kw) => {
      const cleaned = kw.replace(/[\[\]"]+/g, '').trim();
      return cleaned.toLowerCase().includes(input.toLowerCase());
    });

    setSuggestions(filtered.slice(0, 5));
  }, [input, keywords]);


  const handleSearch = async () => {
    setLoading(true);
    const res = await fetch('/api/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: input }),
    });
    const data = await res.json();
    const summary = data.summary ? data.summary.replace(/^\s*-\s*/gm, '')  : 'No summary found.';
    setSummary(summary);
    setTimeline(data.timeline || []);
    setLoading(false);
    console.log(data)
  };

  const handleSelectSuggestion = (suggestion: string) => {
    setInput(suggestion);
    setSuggestions([]);
  };

  const sortedTimeline = [...timeline].sort((a, b) => {
    const dateA = new Date(a.date);
    const dateB = new Date(b.date);
    return dateB.getTime() - dateA.getTime(); // descending: newest first
  });

  return (
  <main className="p-8 max-w-xl mx-auto">
  <h1 className="text-2xl font-bold mb-4">HereWeGo!PT</h1>

  <div className="mb-2">
    <input
      type="text"
      value={input}
      onChange={(e) => setInput(e.target.value)}
      placeholder="Enter player, club, or manager"
      className="border p-2 w-full"
    />
    {suggestions.length > 0 && input.length >= 2 && (
      <ul className="bg-white border w-full shadow max-h-40 overflow-y-auto text-black mt-1 rounded">
        {suggestions.map((s, idx) => (
        <li
          key={idx}
          onClick={() => handleSelectSuggestion(s)}
          className="p-2 hover:bg-blue-100 cursor-pointer"
        >
          {s.replace(/[\[\]"]+/g, '').trim()}
        </li>
      ))}
      </ul>
    )}
  </div>

  <div className="mt-4">
    <button
      onClick={handleSearch}
      className="bg-blue-600 text-white px-4 py-2 rounded w-full"
      disabled={loading}
    >
      {loading ? 'Loading...' : 'Search'}
    </button>
  </div>

  {summary && (
    <div className="mt-6 whitespace-pre-line border p-4 rounded bg-black-50 text-white">
      <h2 className="font-semibold mb-2">Summary</h2>
      <ul className="pl-5">
        {summary
          .split("\n")
          .filter(line => line.trim())
          .map((line, index) => (
            <li key={index} className="list-disc">{line.trim()}</li>
          ))}
      </ul>
    </div>
  )}


  {sortedTimeline.length > 0 && (
    <div className="mt-6 border p-4 rounded bg-black shadow">
      <h2 className="font-semibold text-lg mb-3 text-white">Timeline</h2>
      <ul className="space-y-2">
        {sortedTimeline.map((item, idx) => (
          <li key={idx} className="border-l-4 border-blue-600 pl-3 mb-6">
            <p className="text-sm font-semibold text-white">{item.date}</p>
            <p className="text-white">{item.summary}</p>
          </li>
        ))}
      </ul>
    </div>
  )}
</main>
);
}