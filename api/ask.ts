// api/ask.ts
import type { VercelRequest, VercelResponse } from "@vercel/node";

export default async function handler(req: VercelRequest, res: VercelResponse) {
  try {
    if (req.method !== "POST") return res.status(405).json({ error: "Method Not Allowed" });

    const { question } = req.body || {};
    if (!question || typeof question !== "string") {
      return res.status(400).json({ error: "Missing 'question' string in body" });
    }

    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      // 키가 없을 때도 프론트가 죽지 않게 친절한 메시지 반환
      return res.status(200).json({
        answer:
          "Demo 모드: OPENAI_API_KEY가 설정되지 않아 간단 회신만 합니다.\n\n질문: " +
          question,
      });
    }

    // OpenAI Chat Completions (Responses API로 바꿔도 OK)
    const resp = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: [
          {
            role: "system",
            content:
              "너는 규제·법령을 알기 쉽게 요약하고, 모르면 보수적으로 한계를 밝히는 도우미다. 간결하게 한국어로 답해라.",
          },
          { role: "user", content: question },
        ],
        temperature: 0.2,
      }),
    });

    if (!resp.ok) {
      const text = await resp.text();
      return res.status(500).json({ error: "Upstream error", detail: text });
    }

    const data = await resp.json();
    const answer = data?.choices?.[0]?.message?.content ?? "(no content)";
    return res.status(200).json({ answer });
  } catch (e: any) {
    return res.status(500).json({ error: e?.message || "Server error" });
  }
}
