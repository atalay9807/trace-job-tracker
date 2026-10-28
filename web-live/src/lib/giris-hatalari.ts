// Giriş hataları URL'de metin olarak değil kod olarak taşınır. Metin
// taşınsaydı herkes "/login?hata=<istediği cümle>" bağlantısıyla gerçek
// alan adımızda istediği uyarıyı gösterebilirdi. Bilinmeyen kod hiçbir şey
// göstermez; Supabase'in ham İngilizce mesajı yalnızca sunucu logunda kalır.
// Metinler e-posta şablonu ayarından bağımsız doğru kalacak biçimde yazıldı:
// "aynı tarayıcıda aç" her iki bağlantı biçiminde de çalışır (README).

export const GIRIS_HATALARI = {
  baglanti_eksik: "Giriş bağlantısı eksik ya da bozuk. Yeni bir bağlantı iste.",
  baglanti_gecersiz:
    "Giriş bağlantısı açılamadı. Süresi dolmuş ya da daha önce kullanılmış olabilir. Yeni bir bağlantı iste; yine açılmazsa onu girişi başlattığın tarayıcıda aç.",
  oturum_acilamadi: "Oturum açılamadı. Yeni bir bağlantı iste.",
} as const;

export type GirisHataKodu = keyof typeof GIRIS_HATALARI;

export function girisHatasiMetni(
  kod: string | string[] | undefined,
): string | null {
  const tek = Array.isArray(kod) ? kod[0] : kod;
  if (!tek || !Object.hasOwn(GIRIS_HATALARI, tek)) return null;
  return GIRIS_HATALARI[tek as GirisHataKodu];
}
