import { NextResponse } from "next/server";
import { exec } from "child_process";
import path from "path";

export async function GET() {
  return new Promise((resolve) => {
    const scriptPath = path.join(process.cwd(), "../backend/keywords.py");

    exec(`python ${scriptPath}`, (error, stdout, stderr) => {
      if (error) {
        resolve(NextResponse.json({ error: stderr }, { status: 500 }));
      } else {
        const keywords = JSON.parse(stdout);
        resolve(NextResponse.json({ keywords }));
      }
    });
  });
}
