import type { NextApiRequest, NextApiResponse } from 'next';
import { exec } from 'child_process';
import path from 'path';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { query } = req.body;

  if (!query) {
    return res.status(400).json({ error: 'No query provided' });
  }

  const scriptPath = path.resolve(process.cwd(), '../backend/chain.py');

  const child = exec(`python ${scriptPath} "${query}"`, (error, stdout, stderr) => {
    if (error) {
      console.error('Error:', error);
      return res.status(500).json({ error: 'Internal Server Error' });
    }
    if (stderr) {
      console.error('Stderr:', stderr);
    }

    try {
      const parsed = JSON.parse(stdout.trim());
      res.status(200).json(parsed);
    } catch (e) {
      console.error("Failed to parse JSON from Python:", stdout);
      res.status(500).json({ error: 'Invalid response from backend' });
    }
  });
}
