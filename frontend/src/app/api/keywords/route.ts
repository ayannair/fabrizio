import { NextResponse } from "next/server";
import { exec } from "child_process";
import path from "path";

export async function GET() {
  const scriptPath = path.join(process.cwd(), "../backend/keywords.py");

  return new Promise<Response>((resolve, reject) => {
    exec(`python ${scriptPath}`, (error, stdout, stderr) => {
      if (error) {
        reject(NextResponse.json({ error: stderr }, { status: 500 }));
      } else {
        try {
          const keywords = JSON.parse(stdout);
          resolve(NextResponse.json({ keywords }));
        } catch (parseError) {
          reject(NextResponse.json({ error: `Failed to parse response from script: ${parseError}` }, { status: 500 }));
        }
      }
    });
  });
}
