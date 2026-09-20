---
name: mail-classification
description: "Runs Trace's daily Gmail scan: finds job-related email, strips out the noise, classifies each message into one of five states (offer / interview invitation / action required / rejection / under review) and updates the matching record in data/applications.json. Use it when running the daily scan, when the user says 'scan the mail', 'any new applications', 'check the inbox', when asked which category an email falls into, and when editing the Routine's prompt. Do not write the queries or the noise list from memory — they are here."
---

# Mail sınıflandırma

Veri yolu ve ortak geliştirme kuralları `docs/collaboration.md` içindedir.
`data/...` seçilmiş TRACE_DATA klasörünü ifade eder; özel veri eksikse demo
veriye dönülmez. Diğer ajana aktarılırken mutlak veri yolu açıkça verilir.


Trace'in günlük hattının ilk iki adımı. Amaç, gelen kutusundaki gürültüden
başvuru sürecine dair **durum değişikliklerini** ayıklamak.

Kanonik sorgular ve listeler `config/rules.yaml` içindedir. Oradaki
`daily_query`, `noise_senders`, `ats_senders` ve `status_rules` bu skill'in
uzun halidir; değişiklik gerekiyorsa ikisini birlikte güncelle.

---

## 1. Tara

Günlük tarama son 24 saati kapsar:

```
newer_than:1d (mülakat OR interview OR "case study" OR başvuru OR pozisyon OR
recruiter OR "insan kaynakları" OR application OR görüşme OR assessment OR
candidate OR aday OR hiring OR offer OR teklif)
```

Aylık yeniden inşa gerekiyorsa `config/rules.yaml` → `backfill_queries`
içindeki dört sorgu son 30 günü sıfırdan tarar. Bunu ayda bir çalıştırmak
kaçan başvuruları yakalar.

**Thread'i okumadan sınıflandırma yapma.** Arama sonuçları yalnızca en eski
~5 mesajı gösterir; bir thread'de sonradan gelen red maili görünmez. Önemli
görünen her thread için `get_thread` ile (`PLAIN_TEXT` formatında) tam metni al.

## 2. Gürültüyü ayıkla

Şu göndericiler **yalnızca adet olarak** raporlanır, kayıt açılmaz:

```
jobalerts-noreply@linkedin.com      messaging-digest-noreply@linkedin.com
jobs-noreply@linkedin.com           groups-noreply@linkedin.com
noreply@glassdoor.com               noreply@news.bloomberg.com
subscriptions@message.bloomberg.com noreply@info.getmidas.com
hello@students.udemy.com            updates@mail.quillbot.com
```

**Bir istisna var:** `jobs-noreply@linkedin.com` genelde gürültüdür ama
"kaydedilen iş ilanına başvurun" ve "ilanınızın süresi sona eriyor" konulu
mailleri `data/saved_jobs.json`'ı besler — huninin üst kısmı oradan geliyor.
Bunları atma, ayrı topla.

ATS sağlayıcıları (`myworkday.com`, `hire.lever.co`, `ashbyhq.com`,
`workablemail.com`, `smartrecruiters.com`, `successfactors.com`, `hrpanda.co`,
`peoplise.com`, `recruitee-mailbox.com`, `resreader.com`, `jobgether.com`)
gürültü değildir — başvuru onayı ya da durum değişikliği taşırlar.

## 3. Sınıflandır — ilk eşleşen kazanır

Sıra önemli: bir mail hem "assessment" hem "unfortunately" içeriyorsa red
kazanmalı, çünkü süreç kapanmıştır. Bu yüzden yukarıdan aşağı bakılır.

| Sıra | Durum | Sinyaller |
|---|---|---|
| 1 | **red** | not moving forward, not to proceed, won't be moving forward, uygun bulunmamıştır |
| 2 | **teklif** | offer letter, we are pleased to offer, iş teklifi, teklif mektubu |
| 3 | **mülakat daveti / sonraki aşama** | schedule an interview, interview invitation, görüşme daveti |
| 4 | **aksiyon gerekli** | assessment, complete your application, deadline, testi tamamla |
| 5 | **incelemede** | we received your application, thank you for applying, başvurunuz alındı |

Sinyalleri son mesajın yeni yazılmış kısmında değerlendir; alıntılanmış eski
mesajdaki red/teklif yeni durumu değiştirmez. `not moving forward` içindeki
`moving forward` olumlu davet değildir. Yalnızca `unfortunately`, `test` veya
`availability` gibi genel kelimelerle karar verme; çelişki varsa incelemeye bırak.

Hiçbirine uymuyorsa sınıflandırma yapma — kullanıcıya sor. Zorlama bir
etiket, yanlış bir `stage` değerine ve yanlış hatırlatmaya yol açar.

## 4. Kaydı güncelle

`data/applications.json` içindeki ilgili kaydı bul (yoksa yeni kayıt aç) ve
sınıfa göre şu alanları tazele:

| Sınıf | Güncellenen alanlar |
|---|---|
| teklif | `stage: offer`, `status: action_required`, `next_step` |
| mülakat daveti | `stage: interview_scheduling` veya `next_stage`, `status: action_required`, varsa `deadline` |
| aksiyon gerekli | `stage: assessment` veya `application_incomplete`, `status: action_required`, `deadline` |
| red | `stage: closed`, `status: rejected` |
| incelemede | `stage: under_review`, `status: awaiting_response` |

Her durumda `last_contact` son mesaj tarihine çekilir. Otomatik onay dışındaki
ilk gerçek dönüşün tarihi biliniyorsa `first_response` alanına yaz; sonraki
mesajlarda bu ilk tarihi değiştirme. Eski kayıtta bilinmiyorsa null kalır.
Yanıt kanıtı varsa `response_received: true`, yalnızca otomatik onay varsa false
kullanılabilir; ileri aşama veya red ile false birlikte kullanılamaz.

**Yeni kayıt açarken** ilan metni varsa `match-scoring` skill'ine geç.
Yalnızca başlık/şirket varsa `match: null`, `gap_skills: []` bırak; puan uydurma.
Yazdıktan sonra `python3 src/veri.py` ile denetle.

## Tarih ve deadline çıkarımı

- Tarihler daima `YYYY-MM-DD`. Mail "Monday, 31 August" diyorsa yılı thread'in
  tarihinden al, tahmin etme.
- Deadline yalnızca **mailde açıkça yazıyorsa** girilir. "En kısa sürede" bir
  deadline değildir; `deadline: null` bırak.
- Mülakat saati/platformu `next_step` içine düz metin olarak yazılır
  (ör. "28 Ağu 12:00 Teams görüşmesi"), ayrı alan açılmaz.

## Üçüncü kişilerin bilgisi

Depo herkese açık. İK çalışanlarının adı ve iş e-postası **kayda girmez**;
rol etiketiyle temsil edilir:

```
"contact": "İK Müdürü — ik@sirket.example"
```

`.example` alan adı RFC 2606 gereği hiçbir zaman gerçek olamaz. Bu, mailden
okuduğun gerçek adı silmek anlamına gelir — kasıtlı.

## URL kuralı

`links_actions` içine yalnızca **mailde doğrulanmış** bağlantılar gerçek URL
olarak girer (`kind: "ext"`). Doğrulanmamışsa Gmail arama derin bağlantısı
üretilir:

```
https://mail.google.com/mail/u/0/#search/<şirket adı, url-encoded>
```

Şirketin kariyer portalı adresini tahmin edip yazma — kırık link, link
olmamasından kötüdür.
