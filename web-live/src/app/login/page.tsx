import GirisFormu from "./giris-formu";

export const metadata = {
  title: "Giriş — Job Tracker",
};

// Açık yönlendirme koruması: yalnızca kendi sitemizdeki mutlak yollar.
function guvenliYol(aday: string | string[] | undefined): string {
  const tek = Array.isArray(aday) ? aday[0] : aday;
  if (!tek || !tek.startsWith("/") || tek.startsWith("//")) return "/";
  return tek;
}

function tekDeger(deger: string | string[] | undefined): string | null {
  const tek = Array.isArray(deger) ? deger[0] : deger;
  return tek ?? null;
}

export default async function GirisSayfasi({
  searchParams,
}: PageProps<"/login">) {
  const parametreler = await searchParams;

  return (
    <main className="flex min-h-dvh items-center justify-center px-4 py-12">
      <div className="w-full max-w-sm">
        <h1 className="text-2xl font-semibold">Job Tracker</h1>
        <p className="mt-2 text-sm opacity-70">
          Başvurularını tek yerde topla, CV&apos;nle eşleştir.
        </p>

        <GirisFormu
          devam={guvenliYol(parametreler.devam)}
          girisHatasi={tekDeger(parametreler.hata)}
        />
      </div>
    </main>
  );
}
