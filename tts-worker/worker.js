export default {
  async fetch(request, env) {
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Max-Age': '86400',
        },
      });
    }

    if (request.method !== 'POST') {
      return new Response(JSON.stringify({ error: 'Method not allowed' }), {
        status: 405,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }

    try {
      const { text } = await request.json();

      if (!text || typeof text !== 'string' || text.trim().length === 0) {
        return new Response(JSON.stringify({ error: 'Text is required' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        });
      }

      // Cap text length to avoid excessive API costs
      const trimmedText = text.slice(0, 5000);

      const ttsResponse = await fetch(
        `https://api.elevenlabs.io/v1/text-to-speech/${env.VOICE_ID}/stream`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'xi-api-key': env.ELEVENLABS_API_KEY,
          },
          body: JSON.stringify({
            text: trimmedText,
            model_id: 'eleven_flash_v2_5',
            voice_settings: {
              stability: 0.5,
              similarity_boost: 0.75,
              style: 0.0,
              use_speaker_boost: true,
            },
          }),
        }
      );

      if (!ttsResponse.ok) {
        const errText = await ttsResponse.text();
        return new Response(JSON.stringify({ error: 'TTS API error', details: errText }), {
          status: ttsResponse.status,
          headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        });
      }

      return new Response(ttsResponse.body, {
        status: 200,
        headers: {
          'Content-Type': 'audio/mpeg',
          'Access-Control-Allow-Origin': '*',
          'Cache-Control': 'public, max-age=3600',
        },
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: 'Internal error', message: err.message }), {
        status: 500,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }
  },
};
