import type { SupabaseClient } from "@supabase/supabase-js";

import type { Veritabani } from "@/lib/tipler";

// Faz 4-5'in ölçümü bu akışa dayanıyor. Ad listesi kapalı tutuluyor ki
// aynı olay iki farklı yazımla iki ayrı olay gibi görünmesin.
export type OlayAdi =
  | "signup"
  | "cv_uploaded"
  | "application_created"
  | "status_changed";

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
 * geçtiği için tekrarı burada engellemek gerekiyor.
 */
export async function ilkGirisiIsaretle(
  istemci: Istemci,
  kullaniciId: string,
): Promise<void> {
  const { count, error } = await istemci
    .from("events")
    .select("id", { count: "exact", head: true })
    .eq("user_id", kullaniciId)
    .eq("event_name", "signup");

  if (error) {
    console.error("signup olayı kontrol edilemedi", error.message);
    return;
  }

  if ((count ?? 0) === 0) {
    await olayYaz(istemci, "signup");
  }
}
