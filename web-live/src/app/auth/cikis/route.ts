import { sunucuIstemcisi } from "@/lib/supabase/sunucu";

export async function POST(): Promise<Response> {
  const istemci = await sunucuIstemcisi();
  await istemci.auth.signOut();

  // 303: POST sonrası GET ile yönlendir. Göreli Location, host'u bozmaz.
  return new Response(null, { status: 303, headers: { Location: "/login" } });
}
