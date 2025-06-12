import type { NextApiRequest, NextApiResponse } from 'next';
import { exec } from 'child_process';
import path from 'path';

function execShellCommand(cmd: string): Promise<string> {
  console.log("[execShellCommand] Running command:", cmd);  // DEBUG: command start
  return new Promise((resolve, reject) => {
    exec(cmd, (error, stdout, stderr) => {
      if (error) {
        console.error("[execShellCommand] Error:", error);  // DEBUG: error from exec
        reject(error);
      } else if (stderr) {
        console.warn("[execShellCommand] Stderr:", stderr); // DEBUG: stderr output (warnings, etc)
        resolve(stdout);
      } else {
        console.log("[execShellCommand] Success, stdout length:", stdout.length);  // DEBUG: stdout received
        resolve(stdout);
      }
    });
  });
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  console.log("[handler] Request method:", req.method);  // DEBUG: incoming method

  if (req.method !== 'POST') {
    console.warn("[handler] Invalid method, returning 405");
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { query } = req.body;
  console.log("[handler] Received query:", query);  // DEBUG: input query

  if (!query) {
    console.warn("[handler] No query provided, returning 400");
    return res.status(400).json({ error: 'No query provided' });
  }

  try {
    const response = await fetch(`http://127.0.0.1:5000/api/query?entity=${encodeURIComponent(query)}`);
    
    if (!response.ok) {
      return res.status(500).json({ error: "Failed to fetch query results" });
    }

    const data = await response.json();
    
    return res.status(200).json(data);
  } catch (error) {
    console.error("[handler] Caught error:", error);
    return res.status(500).json({ error: `Internal Server Error or Invalid response from backend: ${error}` });
  }
}
