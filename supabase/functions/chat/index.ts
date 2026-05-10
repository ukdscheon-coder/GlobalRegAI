import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // CORS Preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { messages, activeModule } = await req.json()

    // Get the OpenAI API key securely from Supabase Secrets
    const openAiKey = Deno.env.get('OPENAI_API_KEY')
    if (!openAiKey) {
      throw new Error("OpenAI API key not configured in Edge Function secrets.")
    }

    const systemPrompt = `You are GlobalRegAI, a world-class regulatory affairs consultant for medical devices, pharmaceuticals, cosmetics, and food. 
    The user is using the '${activeModule}' module.
    Answer the user's regulatory query in Korean.
    Benchmark Google's AI Overview: Use a highly structured, analytical markdown format with numbered bullet points.
    Search for all global contexts (FDA, EMA, MFDS, PMDA, NMPA, ISO, GMP).
    At the end, provide 1-2 realistic URLs as [출처: 기관명](url) for verification.`;

    const openAiResponse = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${openAiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-4o-mini',
        messages: [
          { role: 'system', content: systemPrompt },
          ...messages
        ],
      }),
    })

    const data = await openAiResponse.json()
    const aiContent = data.choices[0].message.content

    return new Response(
      JSON.stringify({ response: aiContent }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )

  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
    )
  }
})
