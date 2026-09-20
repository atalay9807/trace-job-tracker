// Veritabanı şemasının TypeScript karşılığı. Kaynak doğruluk
// supabase/migrations altındaki SQL'dir — şema değişirse burası da değişir.

export type BasvuruStatusu =
  | "saved"
  | "applied"
  | "interview"
  | "offer"
  | "rejected";

export type RedNedeni =
  | "skill_gap"
  | "experience"
  | "position_closed"
  | "unknown";

// Kanban kolon sırası ve arayüz etiketleri tek yerden okunur.
export const STATU_SIRASI: readonly BasvuruStatusu[] = [
  "saved",
  "applied",
  "interview",
  "offer",
  "rejected",
] as const;

export const STATU_ETIKETLERI: Record<BasvuruStatusu, string> = {
  saved: "Kaydedildi",
  applied: "Başvuruldu",
  interview: "Mülakat",
  offer: "Teklif",
  rejected: "Red",
};

export const RED_NEDENI_ETIKETLERI: Record<RedNedeni, string> = {
  skill_gap: "Eksik yetkinlik",
  experience: "Deneyim yetersiz",
  position_closed: "Pozisyon kapandı",
  unknown: "Bilinmiyor",
};

type Cv = {
  id: string;
  user_id: string;
  file_url: string;
  uploaded_at: string;
};

type Basvuru = {
  id: string;
  user_id: string;
  company: string;
  position: string;
  job_url: string | null;
  job_description: string | null;
  status: BasvuruStatusu;
  rejection_reason: RedNedeni | null;
  rejection_note: string | null;
  created_at: string;
  updated_at: string;
};

type Olay = {
  id: string;
  user_id: string;
  event_name: string;
  properties: Record<string, unknown>;
  created_at: string;
};

export type Veritabani = {
  public: {
    Tables: {
      cvs: {
        Row: Cv;
        Insert: Omit<Cv, "id" | "uploaded_at"> & {
          id?: string;
          uploaded_at?: string;
        };
        Update: Partial<Cv>;
        Relationships: [];
      };
      applications: {
        Row: Basvuru;
        Insert: Omit<Basvuru, "id" | "created_at" | "updated_at"> & {
          id?: string;
          created_at?: string;
          updated_at?: string;
        };
        Update: Partial<Basvuru>;
        Relationships: [];
      };
      events: {
        Row: Olay;
        Insert: Omit<Olay, "id" | "created_at"> & {
          id?: string;
          created_at?: string;
        };
        Update: Partial<Olay>;
        Relationships: [];
      };
    };
    Views: Record<never, never>;
    Functions: Record<never, never>;
    Enums: {
      application_status: BasvuruStatusu;
      rejection_reason: RedNedeni;
    };
    CompositeTypes: Record<never, never>;
  };
};
