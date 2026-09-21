"use client";

import { useState } from "react";

import { tarayiciIstemcisi } from "@/lib/supabase/tarayici";

type Durum = "bos" | "gonderiliyor" | "gonderildi" | "hata";

type Ozellikler = {
  /** Giriş sonrası dönülecek yol; proxy tarafından eklenir. */
  devam: string;
  /** auth/callback bir hatayla geri gönderdiyse gösterilecek mesaj. */
  girisHatasi: string | null;
};

export default function GirisFormu({ devam, girisHatasi }: Ozellikler) {
  const [eposta, setEposta] = useState("");
  const [durum, setDurum] = useState<Durum>("bos");
  const [hata, setHata] = useState("");

  async function gonder(olay: React.FormEvent<HTMLFormElement>) {
    olay.preventDefault();
    setDurum("gonderiliyor");
    setHata("");

    const hedef = `${window.location.origin}/auth/callback?devam=${encodeURIComponent(devam)}`;

    const { error } = await tarayiciIstemcisi().auth.signInWithOtp({
      email: eposta,
      options: { emailRedirectTo: hedef },
    });

    if (error) {
      setDurum("hata");
      setHata(error.message);
      return;
    }

    setDurum("gonderildi");
  }

  if (durum === "gonderildi") {
    return (
      <div className="mt-8 rounded-lg border border-current/15 p-4 text-sm">
        <p className="font-medium">Bağlantı gönderildi.</p>
        <p className="mt-1 opacity-70">
          {eposta} adresine gelen giriş bağlantısına tıkla. Bağlantı tek
          kullanımlık ve kısa ömürlü.
        </p>
        <button
          type="button"
          onClick={() => setDurum("bos")}
          className="mt-3 text-sm underline underline-offset-4"
        >
          Başka bir adres kullan
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={gonder} className="mt-8 flex flex-col gap-3">
      <label htmlFor="eposta" className="text-sm font-medium">
        E-posta adresin
      </label>
      <input
        id="eposta"
        name="eposta"
        type="email"
        required
        autoComplete="email"
        inputMode="email"
        value={eposta}
        onChange={(olay) => setEposta(olay.target.value)}
        placeholder="ornek@eposta.com"
        className="w-full rounded-lg border border-current/20 bg-transparent px-3 py-2 text-base outline-none focus:border-current/50"
      />

      <button
        type="submit"
        disabled={durum === "gonderiliyor"}
        className="w-full rounded-lg bg-foreground px-3 py-2 text-base font-medium text-background disabled:opacity-50"
      >
        {durum === "gonderiliyor" ? "Gönderiliyor…" : "Giriş bağlantısı gönder"}
      </button>

      <p className="text-xs opacity-60">
        Parola yok. Adresine tek kullanımlık bir bağlantı gönderiyoruz.
      </p>

      {hata && (
        <p role="alert" className="text-sm text-red-600 dark:text-red-400">
          Bağlantı gönderilemedi: {hata}
        </p>
      )}
      {girisHatasi && !hata && (
        <p role="alert" className="text-sm text-red-600 dark:text-red-400">
          {girisHatasi}
        </p>
      )}
    </form>
  );
}
