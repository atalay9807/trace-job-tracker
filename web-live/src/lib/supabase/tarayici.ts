"use client";

import { createBrowserClient } from "@supabase/ssr";

import { supabaseAnonAnahtari, supabaseUrl } from "@/lib/ortam";
import type { Veritabani } from "@/lib/tipler";

// Tarayıcı tarafı istemci. Oturum çerezleri @supabase/ssr tarafından yönetilir.
export function tarayiciIstemcisi() {
  return createBrowserClient<Veritabani>(supabaseUrl(), supabaseAnonAnahtari());
}
