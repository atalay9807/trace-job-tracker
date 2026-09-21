import { redirect } from "next/navigation";

import { sunucuIstemcisi } from "@/lib/supabase/sunucu";

export default async function AnaSayfa() {
  const istemci = await sunucuIstemcisi();
  const {
    data: { user },
  } = await istemci.auth.getUser();

  // Middleware zaten yönlendiriyor; bu ikinci kontrol doğrudan erişime karşı.
  if (!user) redirect("/login");

  return (
    <main className="mx-auto w-full max-w-2xl px-4 py-12">
      <h1 className="text-2xl font-semibold">Job Tracker</h1>
      <p className="mt-2 text-sm opacity-70">
        Giriş yapıldı: <span className="font-mono">{user.email}</span>
      </p>

      <div className="mt-8 rounded-lg border border-current/15 p-4 text-sm">
        <p className="font-medium">Faz 1 — Adım 1 kuruldu</p>
        <p className="mt-1 opacity-70">
          Giriş, oturum ve veri katmanı hazır. Başvuru sayfaları
          (/applications, /applications/new, /onboarding) sonraki adımlarda
          geliyor.
        </p>
      </div>

      <form action="/auth/cikis" method="post" className="mt-6">
        <button
          type="submit"
          className="rounded-lg border border-current/20 px-3 py-2 text-sm font-medium"
        >
          Çıkış yap
        </button>
      </form>
    </main>
  );
}
