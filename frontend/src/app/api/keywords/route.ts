import { NextResponse } from "next/server";

export async function GET() {
  try {
    const response = await fetch('https://herewegopt-919615563b34.herokuapp.com//api/keywords');
    
    if (!response.ok) {
      return NextResponse.json({ error: "Failed to fetch keywords" }, { status: 500 });
    }

    const keywords = await response.json();

    return NextResponse.json({ keywords });
  } catch (error) {
    return NextResponse.json({ error: `Error fetching data: ${error}` }, { status: 500 });
  }
}
