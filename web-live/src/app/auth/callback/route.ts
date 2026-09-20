import type { EmailOtpType } from "@supabase/supabase-js";
import type { NextRequest } from "next/server";

import { ilkGirisiIsaretle } from "@/lib/olaylar";
import { sunucuIstemcisi } from "@/lib/supabase/sunucu";

// Açık yönlendirme koruması: yalnızca kendi sitemizdeki mutlak yollar.
function guvenliYol(aday: string | null): string {
  if (!aday || !aday.startsWith("/") || aday.startsWith("//")) return "/";
  return aday;
}

/**
 * Göreli Location ile yönlendirir. Mutlak URL kurmuyoruz: route handler
 * içinde istek.url sunucunun kendi adresini veriyor, arkasında proxy olan
 * bir dağıtımda kullanıcıyı yanlış hosta göndermesi riskli.
 */
function yonlendir(yol: string, durum = 307): Response {
  return new Response(null, { status: durum, headers: { Location: yol } });
}

function girisegeriDon(mesaj: string): Response {
  return yonlendir(`/login?hata=${encodeURIComponent(mesaj)}`);
}

export async function GET(istek: NextRequest) {
  const parametreler = istek.nextUrl.searchParams;
  const kod = parametreler.get("code");
  const tokenHash = parametreler.get("token_hash");
  const tur = parametreler.get("type") as EmailOtpType | null;
  const devam = guvenliYol(parametreler.get("devam"));

  const istemci = await sunucuIstemcisi();

  // Magic link iki biçimde dönebiliyor: PKCE kodu ya da token_hash.
  let hataMesaji: string | null = null;

  if (kod) {
    const { error } = await istemci.auth.exchangeCodeForSession(kod);
    hataMesaji = error?.message ?? null;
  } else if (tokenHash && tur) {
    const { error } = await istemci.auth.verifyOtp({
      type: tur,
      token_hash: tokenHash,
    });
    hataMesaji = error?.message ?? null;
  } else {
    hataMesaji = "Giriş bağlantısı eksik ya da bozuk. Yeni bir bağlantı iste.";
  }

  if (hataMesaji) {
    return girisegeriDon(hataMesaji);
  }

  const {
    data: { user },
  } = await istemci.auth.getUser();

  if (!user) {
    return girisegeriDon("Oturum açılamadı. Yeni bir bağlantı iste.");
  }

  await ilkGirisiIsaretle(istemci, user.id);

  return yonlendir(devam);
}
