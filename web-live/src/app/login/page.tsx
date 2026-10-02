import { girisHatasiMetni } from "@/lib/giris-hatalari";
import { guvenliYol } from "@/lib/guvenli-yol";

import GirisFormu from "./giris-formu";

export const metadata = {
  title: "Giriş — Job Tracker",
};

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
          girisHatasi={girisHatasiMetni(parametreler.hata)}
        />
      </div>
    </main>
  );
}
