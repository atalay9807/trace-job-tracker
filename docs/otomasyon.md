# Otomasyonun İşleyişi

## Günlük Routine

Bu belge yetkilendirilmiş Claude oturumu/Routine için tasarlanan akışı anlatır.
Bu depoyu klonlamak veya Python komutlarını çalıştırmak zamanlanmış görev
kurmaz, Gmail taramaz, e-posta göndermez. Güncel Routine kimliği ve çalışma
geçmişi bağlı hizmetten doğrulanır; buradaki eski oturum kimliği kaldırılmıştır.

Planlanan saat: `0 6 * * *` UTC = 09:00 Europe/Istanbul.
`docs/ORTAK_CALISMA.md` içindeki veri kaynağı ve tek yazıcı kuralları geçerlidir.

Her sabah şu adımları izler:

1. **Tara** — Gmail'de son 24 saatin iş temalı e-postalarını arar
   (`config/rules.yaml` → `scan.daily_query`).
2. **Sınıflandır** — her e-postayı `status_rules` sırasına göre etiketler:
   red → teklif → mülakat daveti → aksiyon gerekli → incelemede;
   yalnızca son mesajın yeni metni değerlendirilir, çelişkili işaret incelemeye bırakılır.
   `noise_senders` listesindekiler yalnızca sayılır.
3. **Güncelle** — seçilmiş `TRACE_DATA/applications.json` içindeki ilgili kaydın `stage`,
   `status`, `last_contact`, `deadline` ve `next_step` alanlarını tazeler;
   yeni başvuru varsa kayıt ekler.
4. **Raporla** — ayrıca gönderim yetkisi varsa doğrulanmış kullanıcı adresine özet gönderir.
   Demo adresine mail gönderilmez; yalnızca okuma izni gönderim yetkisi değildir.
   Konu: `📋 Günlük İş Takip Raporu — <tarih>`.
5. **Hatırlat** — deadline'ı yaklaşan/geçen ve sessizleşen süreçler için
   `reminders` kurallarını uygular.

Kritik bir gelişme yoksa e-posta bunu açıkça söyler ve açık aksiyonları
tekrar hatırlatır — sessiz kalmaz.

## Haftalık geri bildirim

Pazartesi günleri rapor `--weekly` bölümünü içerir: dört soru sorulur ve
yanıtlar bir sonraki taramada `fit` puanlarına yansıtılır. Bu, sistemin tek
yönlü bir bildirim akışı değil, karşılıklı bir döngü olmasını sağlar.

## Bakım

**Yeni başvuru elle eklemek:** güncel şema `docs/TEKNIK.md` ve
`src/veri.py` içindedir. Yazdıktan sonra `python3 src/veri.py` ile denetle.
İlan metni yoksa match null kalır. İlk gerçek yanıt tarihi biliniyorsa
`first_response` kaydedilir; sonraki mesajlar yalnızca `last_contact` değerini ilerletir.

**Puanlamayı değiştirmek:** `config/rules.yaml` → `scoring` bölümü referans
dokümandır; gerçek aşama ağırlıkları `src/veri.py`,
aciliyet eşikleri `src/pipeline.py` içindedir. İkisini birlikte güncelle.

**Routine'i düzenlemek:** prompt'u değiştirmek için `update_trigger` kullan —
sil ve yeniden oluşturma, çalışma geçmişi kaybolur.

**Tam yeniden inşa:** `config/rules.yaml` → `scan.backfill_queries` içindeki
dört sorgu son 30 günü sıfırdan tarar. Ayda bir çalıştırmak, kaçan
başvuruları yakalar.

## Bilinen sınırlar

- LinkedIn "Easy Apply" başvuruları çoğu zaman yalnızca şirketin ATS'inden
  onay maili üretir; LinkedIn'in kendi başvuru kaydı e-postaya düşmez.
  Bu yüzden `applied` tarihi bazen ATS onay tarihidir, gerçek başvuru
  tarihinden 0–2 gün sonrasıdır.
- `fit` puanı otomatik hesaplanmaz; elle atanır ve haftalık geri bildirimle
  güncellenir.
- Gmail araması İngilizce ve Türkçe anahtar kelimelere dayanır; başka dilde
  gelen e-postalar gürültüye düşebilir.
