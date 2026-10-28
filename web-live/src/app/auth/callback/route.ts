import type { EmailOtpType } from "@supabase/supabase-js";
import type { NextRequest } from "next/server";

import type { GirisHataKodu } from "@/lib/giris-hatalari";
import { guvenliYol } from "@/lib/guvenli-yol";
import { ilkGirisiIsaretle } from "@/lib/olaylar";
import { sunucuIstemcisi } from "@/lib/supabase/sunucu";

/**
 * Göreli Location ile yönlendirir. Mutlak URL kurmuyoruz: route handler
 * içinde istek.url sunucunun kendi adresini veriyor, arkasında proxy olan
 * bir dağıtımda kullanıcıyı yanlış hosta göndermesi riskli.
 */
function yonlendir(yol: string, durum = 307): Response {
  return new Response(null, { status: durum, headers: { Location: yol } });
}

function girisegeriDon(kod: GirisHataKodu): Response {
  return yonlendir(`/login?hata=${kod}`);
}

export async function GET(istek: NextRequest) {
  const parametreler = istek.nextUrl.searchParams;
  const kod = parametreler.get("code");
  const tokenHash = parametreler.get("token_hash");
  const tur = parametreler.get("type") as EmailOtpType | null;
  const devam = guvenliYol(parametreler.get("devam"));

  const istemci = await sunucuIstemcisi();

  // Magic link iki biçimde dönebiliyor: PKCE kodu ya da token_hash.
  // Supabase'in ham hata metni kullanıcıya gitmez, yalnızca loglanır.
  if (kod) {
    const { error } = await istemci.auth.exchangeCodeForSession(kod);
    if (error) {
      console.error("giriş kodu doğrulanamadı", error.message);
      return girisegeriDon("baglanti_gecersiz");
    }
  } else if (tokenHash && tur) {
    const { error } = await istemci.auth.verifyOtp({
      type: tur,
      token_hash: tokenHash,
    });
    if (error) {
      console.error("giriş bağlantısı doğrulanamadı", error.message);
      return girisegeriDon("baglanti_gecersiz");
    }
  } else {
    return girisegeriDon("baglanti_eksik");
  }

  const {
    data: { user },
  } = await istemci.auth.getUser();

  if (!user) {
    return girisegeriDon("oturum_acilamadi");
  }

  await ilkGirisiIsaretle(istemci, user.id);

  return yonlendir(devam);
}
