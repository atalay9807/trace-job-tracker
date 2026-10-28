import type { NextRequest } from "next/server";

import { oturumuTazele } from "@/lib/supabase/oturum";

// Next 16'da eski "middleware" dosya kuralının yerini "proxy" aldı.
export async function proxy(istek: NextRequest) {
  return await oturumuTazele(istek);
}

export const config = {
  // Statik dosyalar ve görseller dışındaki her istek oturumdan geçer.
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
