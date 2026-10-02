// Supabase ortam değişkenleri. Eksikse sessizce geçmek yerine anlaşılır hata
// veriyoruz — "undefined" bir URL ile kurulan istemci çok daha geç patlıyor.

function zorunlu(ad: string, deger: string | undefined): string {
  if (!deger) {
    throw new Error(
      `${ad} tanımlı değil. .env.local.example dosyasını .env.local olarak kopyala ve Supabase değerlerini gir.`,
    );
  }
  return deger;
}

export function supabaseUrl(): string {
  return zorunlu("NEXT_PUBLIC_SUPABASE_URL", process.env.NEXT_PUBLIC_SUPABASE_URL);
}

export function supabaseAnonAnahtari(): string {
  return zorunlu(
    "NEXT_PUBLIC_SUPABASE_ANON_KEY",
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
  );
}
