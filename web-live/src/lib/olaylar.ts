import type { SupabaseClient } from "@supabase/supabase-js";

import type { OlayAdi, Veritabani } from "@/lib/tipler";

export type { OlayAdi };

type Istemci = SupabaseClient<Veritabani>;

/**
 * Olayı events tablosuna yazar. Ölçüm kaydı kullanıcı akışını bozmamalı:
 * hata fırlatmaz, yalnızca loglar ve false döner.
 */
export async function olayYaz(
  istemci: Istemci,
  ad: OlayAdi,
  ozellikler: Record<string, unknown> = {},
): Promise<boolean> {
  const {
    data: { user },
  } = await istemci.auth.getUser();

  if (!user) {
    console.warn(`olay yazılamadı (oturum yok): ${ad}`);
    return false;
  }

  const { error } = await istemci.from("events").insert({
    user_id: user.id,
    event_name: ad,
    properties: ozellikler,
  });

  if (error) {
    console.error(`olay yazılamadı: ${ad}`, error.message);
    return false;
  }

  return true;
}

/**
 * signup olayını yalnızca bir kez yazar. Giriş her seferinde callback'ten
 * geçiyor; tekilliği veritabanındaki events_signup_tek indeksi garanti eder,
 * bu yüzden önce sayıp sonra eklemek yerine doğrudan eklenir.
 */
export async function ilkGirisiIsaretle(
  istemci: Istemci,
  kullaniciId: string,
): Promise<void> {
  const { error } = await istemci.from("events").insert({
    user_id: kullaniciId,
    event_name: "signup",
    properties: {},
  });

  // 23505: tekillik ihlali — signup daha önce yazılmış, beklenen durum.
  if (error && error.code !== "23505") {
    console.error("signup olayı yazılamadı", error.message);
  }
}
