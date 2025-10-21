import React, { useState } from "react";

export default function App() {
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<{ role: "user" | "assistant"; text: string }[]>([]);

  async function ask() {
    const question = q.trim();
    if (!question) return;
    setLoading(true);
    setMessages((m) => [...m, { role: "user", text: question }]);
    setQ("");

    try {
      const resp = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await resp.json();
      const answer = data?.answer ?? data?.error ?? "응답 없음";
      setMessages((m) => [...m, { role: "assistant", text: answer }]);
    } catch (e: any) {
      setMessages((m) => [
        ...m,
        { role: "assistant", text: `네트워크 오류: ${e?.message || e}` },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 760, margin: "40px auto", padding: 16, fontFamily: "system-ui" }}>
      <h1>GlobalRegAI 🚀</h1>
      <p>AI 기반 규제·법령 Q&A. 모르면 한계를 밝히고, 확실한 건 간결하게 요약합니다.</p>

      <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && ask()}
          placeholder="예: 미국 FDA 의료기기 510(k) 제출 요건 핵심을 요약해줘"
          style={{ flex: 1, padding: 10, fontSize: 16 }}
        />
        <button disabled={loading} onClick={ask} style={{ padding: "10px 16px", fontSize: 16 }}>
          {loading ? "조회중…" : "질문"}
        </button>
      </div>

      <div style={{ marginTop: 20, display: "grid", gap: 10 }}>
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              whiteSpace: "pre-wrap",
              background: m.role === "user" ? "#f3f4f6" : "#eef6ff",
              border: "1px solid #e5e7eb",
              borderRadius: 8,
              padding: 12,
            }}
          >
            <b>{m.role === "user" ? "질문" : "답변"}</b>
            <div style={{ marginTop: 6 }}>{m.text}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
