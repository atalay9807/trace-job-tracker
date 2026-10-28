import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

import { supabaseAnonAnahtari, supabaseUrl } from "@/lib/ortam";
import type { Veritabani } from "@/lib/tipler";

// Sunucu tarafı istemci (Server Component, Route Handler, Server Action).
export async function sunucuIstemcisi() {
  const cerezler = await cookies();

  return createServerClient<Veritabani>(supabaseUrl(), supabaseAnonAnahtari(), {
    cookies: {
      getAll() {
        return cerezler.getAll();
      },
      setAll(yazilacaklar) {
        try {
          for (const { name, value, options } of yazilacaklar) {
            cerezler.set(name, value, options);
          }
        } catch {
          // Server Component içinden çerez yazılamaz; oturum tazelemeyi
          // middleware yaptığı için bu durum güvenle yutulabilir.
        }
      },
    },
  });
}
