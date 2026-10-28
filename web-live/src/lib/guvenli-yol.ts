// Açık yönlendirme koruması: giriş sonrası yalnızca kendi sitemizdeki bir
// yola dönülür. Callback ve giriş sayfası aynı fonksiyonu kullanır ki iki
// kopya zamanla ayrışmasın.
//
// "/" ile başlamak yetmiyor: tarayıcılar "/\evil.example" ve araya sekme
// girmiş "/\t/evil.example" adreslerini başka siteye giden "//" gibi okuyor.
// Bu yüzden ters bölü ve kontrol karakterleri hiç kabul edilmez, kalan aday
// URL olarak ayrıştırılıp kökenin değişmediği doğrulanır.

const SAHTE_KOK = "http://yerel.invalid";

function supheliKarakterVar(metin: string): boolean {
  for (const karakter of metin) {
    const kod = karakter.charCodeAt(0);
    if (karakter === "\\" || kod < 0x20 || kod === 0x7f) return true;
  }
  return false;
}

export function guvenliYol(
  aday: string | string[] | null | undefined,
): string {
  const tek = Array.isArray(aday) ? aday[0] : aday;
  if (!tek || !tek.startsWith("/") || supheliKarakterVar(tek)) return "/";

  let url: URL;
  try {
    url = new URL(tek, SAHTE_KOK);
  } catch {
    return "/";
  }
  if (url.origin !== SAHTE_KOK) return "/";

  return url.pathname + url.search + url.hash;
}
