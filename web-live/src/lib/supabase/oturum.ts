import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

import { supabaseAnonAnahtari, supabaseUrl } from "@/lib/ortam";
import type { Veritabani } from "@/lib/tipler";

// Giriş gerektirmeyen yollar. Bunların dışındaki her şey oturum ister.
const ACIK_YOLLAR = ["/login", "/auth"];

function acikYolMu(yol: string): boolean {
  return ACIK_YOLLAR.some((acik) => yol === acik || yol.startsWith(`${acik}/`));
}

// Her istekte oturum çerezini tazeler ve gerekiyorsa /login'e yönlendirir.
export async function oturumuTazele(istek: NextRequest) {
  let yanit = NextResponse.next({ request: istek });

  const istemci = createServerClient<Veritabani>(
    supabaseUrl(),
    supabaseAnonAnahtari(),
    {
      cookies: {
        getAll() {
          return istek.cookies.getAll();
        },
        setAll(yazilacaklar) {
          for (const { name, value } of yazilacaklar) {
            istek.cookies.set(name, value);
          }
          yanit = NextResponse.next({ request: istek });
          for (const { name, value, options } of yazilacaklar) {
            yanit.cookies.set(name, value, options);
          }
        },
      },
    },
  );

  // getUser() çağrısı çerezi tazeler; arada başka kod çalıştırma.
  const {
    data: { user },
  } = await istemci.auth.getUser();

  if (!user && !acikYolMu(istek.nextUrl.pathname)) {
    const girisAdresi = istek.nextUrl.clone();
    girisAdresi.pathname = "/login";
    girisAdresi.searchParams.set("devam", istek.nextUrl.pathname);
    return NextResponse.redirect(girisAdresi);
  }

  return yanit;
}
