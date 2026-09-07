# Token maliyeti karşılaştırması — transkript

**Video:** Claude Code / Codex / Gemini token maliyeti karşılaştırması
**Kanal:** Burhan Kocabıyık (`kaynak-claude-code-kursu.md` ile aynı kanal)
**Bağlantı:** kullanıcı tarafından paylaşıldı, URL kaydedilmedi

> Otomatik üretilmiş Türkçe altyazıdan alınmıştır. Tanıma hataları var:
> *Cloud Code / cloud kode / clarcod* = **Claude Code**, *Cemini / Cemine /
> Ceminay* = **Gemini**, *Solet / Sonet* = **Sonnet**, *Opus 4* = Claude Opus 4,
> *Operayin kodexi* = **OpenAI Codex**, *Leflow* = Webflow(?), *Protipal /
> Prototipal* = konuşmacının kendi ürünü, *DOA / Doğu topluluğu* = kendi
> topluluğu, *Gravity* = Google Antigravity.

> **Videodaki rakamların hiçbiri bizim ölçümümüz değil.** Hepsi konuşmacının
> iddiası; doğrulanmadı. Ayrıca video kendini "Nisan 2026" diye tarihliyor
> ama Opus 4, Sonnet 3.7 ve Gemini 2.5'ten bahsediyor — model kuşağı
> güncel değil, fiyatlar da öyle. Çıkarım bölümü en sonda, ayrı tutuldu.

---

## Bölümler

- Giriş ve özet tablo
- Model fiyat karşılaştırması: Opus, Codex ve Gemini
- Örnek 1: 1.78 dolara kurumsal web sitesi yapımı
- Örnek 2: 2.40 dolara YouTube otomasyon sistemi kurulumu
- Örnek 3: Karmaşık uygulama geliştirme ve 12 dolarlık maliyet
- Abonelik paketleri: Pro, Max ve Max 20X farkları
- Token maliyetine takılmak neden yanlış? Çıkarılan değer odaklılık
- Adil karşılaştırma: mimari zeka ve kod kalitesi analizi
- DOA topluluğu ve teknik bilgi olmadan satış yapmak

---

## Giriş ve özet tablo

Şu anda çok popüler bir konu var. Cloud Code çok fazla token mi harcıyor? Yapay zeka modelleri çok mu pahalı? Bu videonun içerisinde hem Codex'i hem Cloud kodu hem de Cemina'yı test ettim ve farklı farklı aslında versiyonlarını ve token kullanımlarını karşılaştırdım. Ve bu videonun sonunda aslında üç farklı benim örneğim için ne kadar token harcadığımı, sonucun ne olduğunu ve buna karşılık da o tokenin karşısındaki miktarı göreceksiniz.

Burada aslında özetle şöyle bir şey gösterebilirim. Cloud Opus en pahalı model, 1 milyon token için 33 dolar. Burada tabii ki API tarafına baktım. Abonelikle alakalı kısmı ayrı göstereceğim, çünkü kendi aboneliğinizi kullandığınızda aslında bu kadar harcamıyorsunuz. Bunu söyleyeyim. Ancak karşılaştırmayı API'a göre koydum ki aslında çok net bir şekilde görünsün. Ancak siz Claude kodu düzgün kullandığınızda 11 dolar oluyor. OpenAI'ın Codex'i yaklaşık 3 dolar oluyor. Cemini 4 dolar oluyor. Sonnet 3.7'yi kullanırsanız da 6 dolar oluyor. Ancak bunların detaylarına bakacağız.

Şimdi token nedir? Neden önemli? Her kelime aslında ayrı bir maliyet gibi düşünebilirsiniz. Ve örneğin 750 kelime eşittir 1000 token gibi düşünebilirsiniz. Ve burada da hem yazdığınız token prompt olarak karşılanabilir hem de bütün aslında birçok şey bunların etrafında kural olarak da alınabilir.

## Model fiyat karşılaştırması: Opus, Codex ve Gemini

Şimdi model fiyat karşılaştırmasında zaten Cemini'yi görüyorsunuz, Codex'i görüyorsunuz. Bir de Opus 4'ü kullanıyorsunuz. Opus 4 zaten açık ara çok daha pahalı bir model. Ancak siz Opus ve Sonnet'i birleştirdiğinizde — ki bunu da aslında `model` yazarak değiştirebilirsiniz Claude kodunuzun içerisinde — bu sayede kullanım olarak 11 dolara kadar indirebilirsiniz. Sadece Opus'u kullandığınızda 33 dolarlık bir maliyetiniz oluyor 1 milyon token için. Bu tabii ki yüksek bir miktar.

Ancak 1 milyon tokenle ne yapabilirsiniz? Bu bence çok önemli. Ve aynı zamanda Claude kodu siz düşündüğünüzde %20'sini Opus 4, %80'ini Sonnet kullandığınızda aslında buradaki geliştirmeniz 33 dolardan 11 dolara iniyor. Hatta token optimizasyonlarını kullanırsanız — ki bununla alakalı da videom var — o zaman aslında bunu da %80 indirebilirsiniz.

## Örnek 1: 1.78 dolara kurumsal web sitesi yapımı

Kurumsal bir web sitesi yaptığımızda nasıl bir miktarı olacak? Bunun nasıl bir masrafı olacak? Şimdi burada ben yaklaşık 150.000 token harcadım ve çok profesyonel bir web sitesi çıktı. Webflow'un kendi web sitesi ve burada da kurumsal bir ajans web sitesi var. İçerisinde blog sayfaların hepsi mevcut. Çok detaylı bütün her taraftaki sayfalar yapıldı. Use case'ler var. Görselleri oluşturdu, videoları oluşturdu. Bunların hepsi içerisinde baştan sona bir web sitesi yaklaşık 150.000 token harcadı.

150.000 tokenin maliyeti ise 1.78 dolar, Claude kod kullandığımda. Gemini kullansaydım 50 cent olacaktı. Codex kullansaydım 40 cent olacaktı. Yani aslında siz profesyonel web sitesi yaptığınızda yaklaşık 2 dolarlık bir miktarla aslında bunu bitirebiliyorsunuz eğer Claude kodu kullanırsanız. O yüzden aslında zaten "Claude Code çok fazla token yakıyormuş" demek yerine siz bu tokende neler yapabilirsiniz, ona bakmanız lazım.

## Örnek 2: 2.40 dolara YouTube otomasyon sistemi kurulumu

YouTube otomasyon sistemi kurdum. Baştan sona, içerisinde hatta stüdyo bile var. Stüdyoları otomatik oluşturabiliyor, promptlamayı yapabiliyor ve bunun uygulamasını kurdum. Claude Code'da çalışan bir uygulama. 200.000 token harcadım yaklaşık. Bunun da masrafı 2.40 dolardı. Bunu aynı zamanda Codex'le yapsaydım 57 cent, Gemini ile yapsaydım 80 cent ödeyecektik.

Yani burada aslında düşündüğünüzde bir yazılımcının günlerce uğraştığı karmaşık bir video render ve API entegrasyonu sadece 2.40 dolara mal oldu. Bir kahve parasından daha ucuza. Bu projenin kapsamından da bahsedeyim: tam otomatik YouTube videosu üretebiliyor. Metinden görsele, sesten videoya uçtan uca bir pipeline oluşturduk. Zorluysa farklı API'ların entegrasyonunu yaptık. Video render ayarlarını yapabilirsiniz. Karmaşık dosya yönetimlerini yapabilirsiniz. Ve sıfırdan mimari bir tasarım yaptım. Hata ayıklama, test süreçleri hepsi bunun içerisinde. 200.000 token.

## Örnek 3: Karmaşık uygulama geliştirme ve 12 dolarlık maliyet

Prototipal'ın UGC factory ve sinematik tarafını — tamamını değil — oluşturmak için yaklaşık 1 milyon token harcadım ki başlı başına bir uygulama, çok da kompleks, ve bunun içinse aslında 12 dolarlık bir harcamam oldu. Bunu Gemini ile yapsaydım 4 dolar olacaktı. OpenAI ile yapsaydım 3 dolar olacaktı.

Şimdi size şu soruyu sormam lazım bu noktada. Evet, Claude Code daha pahalı mı? 4 kat daha pahalı, 5 kat daha pahalı. Doğru. Ama ben bu miktara, 12 dolara çok harika bir arayüz oluşturabiliyorsam, bir uygulama oluşturabiliyorsam ve bu uygulama hem UGC video oluşturup hem sinematik videolar oluşturabiliyorsa, hem frontend'ini hem backend'ini yapabiliyorsam, hem de güvenlik açıklarını kontrol ettirebiliyorsam arkadaşlar bu inanılmaz ucuz.

Normalde böyle bir şey için bundan 2 yıl öncesi olsaydı binlerce euro para verirdiniz — ki ben verdim zamanında. Biz 2,5 yıl içerisinde 50.000 euroluk development masrafı harcadık, yazılım masrafı harcadık, ve şu anda aynı şeyleri ben 12 dolarla yapabiliyorsam ben bu 100 dolar olsa da okeyim. Ben bu bakış açısıyla bakıyorum.

Şimdi siz diyorsanız "ama Claude Code çok pahalı, 5 kat daha pahalı" — doğru, ama aynı sonucu alabilecek misin Codex'le? Hayır. Claude Code yazılımda en iyi mi? Evet. Gemini'den çok daha iyi mi? Evet. O yüzden sen bu sonucu alabiliyorsan — ki bu çok kompleks bir proje — yine okey aslında.

Şimdi birazcık tam maliyet karşılaştırma tablosuna bakalım. Eğer milyonlarca token harcamayacaksanız Claude kodu kullanmanız lazım. Eğer 20 milyon, 30 milyon, 50 milyon token harcayacaksanız — ki 50 milyon token eşittir 50 tane uygulama demek — o zaman başka modelleri kullanmanız lazım, daha kompleks bir sistem kurmanız lazım.

Ama şimdi modellere bakalım. OpenAI'ın Codex'i en ucuzu. Web sitesini oluştursaydım masraflar bu şekilde olacaktı. Sadece Opus'u kullansaydım — mix'ten bahsetmiyorum, sadece Opus, en pahalı model, her şey için en pahalı modeli kullanıyorum test etmek için — o zaman 5 dolar olacaktı web sitesi için. Profesyonel web sitesi. YouTube botum için 6 dolar olacaktı. Uygulama için, az önce gösterdiğim uygulama, yine Prototipal'ın tamamı değil tabii ki ama sinematik sistemi ve UGC oluşturma sistemi, bu da 33 dolara denk gelecekti.

Şimdi o yüzden en ucuz seçeneğiniz aslında sizin OpenAI'ın Codex'i, Gemini 2.5'i — ve bunlar aslında rutin görevler için çok ideal. O yüzden siz aslında test yapıyorken örneğin Gemini'yi kullanabilirsiniz. Gemini test olayında gayet güzel. Codex de gayet güzel. Ve bir uygulamanın içerisindeki testleri yapıyorken — ki bu sayfaların doğru çalışıp çalışmadığını anlamak için olabilir — Codex'i veya Gemini'yi kullanabilirsiniz. Bu da sizin token kullanımınızı yarı yarıya etkileyebilir.

Aynı zamanda siz Opus'u ve Claude kodun içerisinde Sonnet'i kullanıyorken token kullanımınızı optimize etmeniz lazım. Eğer siz token kullanımınızı optimize etmeyi bilmiyorsanız bununla alakalı bir videom da var. Tokenlerinizi %80 kısabilirsiniz. Bu kısılmış versiyonlarla aslında çok kompleks bir uygulamayı bile çok az tokenle yapabilirsiniz.

## Abonelik paketleri: Pro, Max ve Max 20X farkları

Şimdi tabii ki bunlar API masrafları. Yani normalde API'dan kullansaydınız masrafı bu olacaktı. Ancak aboneliğinizi kullanıyorken nasıl olacak? Abonelik paketleri karşılaştırması: burada ChatGPT Plus var, Pro var, Cloud Pro var, Max var, Max 20X var. Bir de Gemini'nin Pro'su var. Ben bunların hepsini çıkarttım sizin için ve bunu yapay zekaya yaptırdım. Hata yoktur diye düşünüyorum ama belki hatalar varsa içerisinde de yine yorumlara yazabilirsiniz. Ama çok doğru göründü bana açıkçası, çünkü güncel dataya göre bunu aldı direkt web sitesinden ve Nisan 2026'ya göre aldım bunu.

Şimdi ChatGPT'nin Plus'ıyla 256.000 token context'iniz var — bu context penceresi — ve burada da aslında 160 mesaj, 3 saat boyunca devam ettirebiliyorsunuz, ve Claude Code erişiminiz zaten yok. Kod yazma gücü ise orta. ChatGPT'nin Pro'sunu kullanabilirsiniz, GPT-5 + O3'ü kullanabilirsiniz, kod yazma gücü yüksek, fena değil.

Cloud Pro. Şimdi "Pro'yu mu almam lazım, Max'i mi almam lazım?" Genelde bu soru çok geliyor. Ana model olarak aslında siz burada Sonnet ve Opus kullanabilirsiniz. Cloud Pro'da da 5 saatlik aslında yaklaşık çalışma yaptırabilirsiniz ve kod yazma gücü çok yüksek. Aynı zamanda Cloud Max'ta sizin burada token kullanımınız yine çok çok yüksek.

Ama baktığınızda aslında şu alt taraftaki yere dikkat çekmek istiyorum: abonelik planları sabit ücretle sınırlı kullanım sunuyor; API'da ise sınırsız kullanıyorsunuz ama kullandıkça ödüyorsunuz. Şimdi bunun arasındaki farksa aslında kendi yapmak istediğiniz işe göre değişebilir ve ona göre farklı şeyler almanız lazım. Günlük aktif geliştirme için Max paketi çok çok ideal, ve çok yoğun kullanımda Max'ın 20x'ine geçmeniz lazım veya doğrudan API'yi tercih etmeniz lazım.

Ancak az önce zaten neler yapabildiğinizi gördünüz. Ben aslında Cloud Pro paketiyle bile az önce yaptığım şeylerin çoğunu yapabilirdim. API ile 1 milyon token 12 dolarken, örneğin burada Max 20 aboneliği 200 dolar aylık ve 15 milyon token veriyor size. Yani aslında düşündüğünüzde mantık olarak yine abonelik daha avantajlı oluyor API'dan kullanmaktansa. Burada 1 milyon tokenin masrafı 12 dolar civarında oluyor ki 12 dolarla neler yapabildiğinizi zaten göstermiş oldum.

## Token maliyetine takılmak neden yanlış? Çıkarılan değer odaklılık

Peki bu maliyete gerçekten değer mi? Token maliyetlerine takılmak neden yanlış? Ben bu bakış açısının açıkçası oldukça yanlış olduğunu düşünüyorum, çünkü bununla alakalı çok fazla sosyal medyada da içerik görüyorum: "Claude kodu kullanmayın, çok fazla token yakıyor, tek prompt verdim bütün context'im bitti, bütün promptlarım doldu, hiçbir şey yapamıyorum şu an" gibi bir sürü şey görüyorum. Bunlar tamamen aslında yanlış.

Neden yanlış olduğunu iki şekilde anlatayım. Bir: token optimizasyonu yapmazsanız hangi modeli kullanırsanız kullanın tokenleriniz hızlı biter, her şeyden önce. İki: siz Claude kodu kullanıyorken — evet, Codex'ten 5 kat pahalı mı? Pahalı. Ama çıkarttığı sonuca bakmanız lazım. Ve burada da örneğin ben normalde dediğim gibi binlerce dolar harcayacağım bir uygulamayı Claude kod'la iki gün içerisinde bütün her şeyini yapabiliyorsam ve mükemmel şekilde çalışıyorsa, buna değer.

Aynı zamanda ben bunun için 12 dolar veriyorsam, 20 dolar veriyorsam yine çok çok iyi. Normalde 2.500 dolarlık bir proje maliyetiniz olacakken siz bunu 12 dolara indiriyorsunuz. Ve bu gerçek. Bu arada ilk defa hayatta böyle bir şey gerçekleşiyor, ilk defa dünyada böyle bir şey yaşıyoruz. Ama tam anlamıyla bu.

Normalde ben şu prototipte burada gösterdiğim şeyleri yaptırmam 6 hafta alır. 6 hafta. Türkiye'de birisini çalıştırdığınızı düşünün, en ucuz miktarı verdiğinizi düşünün — yine size masrafı yaklaşık 2000-3.000 dolar. Ve 3.000 dolarlık bir proje var bir tarafta, bir tarafta benim sadece promptlayarak yaptığım 12 dolarlık bir şey var.

Şimdi bu şekilde baktığınızda maliyetine gerçekten değiyor mu? Değiyor. Peki ben burada şu an "ya 12 dolar vermek çok fazla, 12 dolar yerine keşke 4 dolar verseydim" demem mantıklı mı? Değil. Neden? Çünkü bana oluşturduğu değer zaten bunun çok yüksek. O yüzden ben bir yerden 1000 dolar kazanacaksam oraya 10 dolar harcamamla 50 dolar harcamam arasında çok büyük bir fark yok, eğer 1.000 doları kazanıyorsam oradan.

O yüzden bakış açınız aslında: evet Codex ve Gemini'den daha pahalı olsa da benim yaptığım işe etki ediyor mu? Ben bunu daha değerli bir şekilde satabiliyor muyum? Ve benim için çıkarttığı şey mükemmel bir şey mi? Buna bakmak lazım. Codex'le saatlerinizi harcayacağınız şeyleri siz Claude koda tek seferde yaptırabiliyorsanız Claude kodu kullanmak yine avantajlıdır. Burada tabii ki ücretsiz modeller de kullanabilirsiniz; ancak ben burada ücretli modelleri karşılaştırdım, en çok kullanılan modelleri karşılaştırdım. Antigravity'i kullanıyorsanız Gemini'yi kullanıyorsunuz, Claude kodu kullanıyorsanız Opus'u kullanıyorsunuz, Codex'i kullanıyorsanız zaten ChatGPT'yi kullanıyorsunuz.

## Adil karşılaştırma: mimari zeka ve kod kalitesi analizi

Şimdi adil bir karşılaştırma özeti yapacak olursak, her şeyi bir kenara bırakıp: diğer modeller Codex ve Gemini — ki bunlar tabii ki sürekli gelişecektir. Bu video Nisan 2026'da çekildi; bu video belki 3 ay sonrasında geçerli olmayabilir. Çok farklı artık modeller ortaya çıkabilir, ücretsiz modeller bile mükemmel olabilir.

Ancak Claude Code şu anda inanılmaz bir fırsat. Mimari zekası tarafında Claude Code inanılmaz iyi. Kodlama söz konusu olduğunda, güvenlik söz konusu olduğunda Claude Code en iyisi şu anda. Ve ucuz modellerle aynı kodu beş kere düzeltmek yerine Claude Code'a iyi bir şekilde anlattığınızda, kural listeniz güzel olduğunda — ki bunları yine sıfırdan başlıyorsanız bu kanalda görebilirsiniz — tek seferde doğru yazar.

Aynı zamanda illa Claude'un Opus 4'ünü kullanmak zorunda değilsiniz. Siz Sonnet'i bazen kullanabilirsiniz, bazen Opus'u kullanabilirsiniz. O yüzden bunları birleştirdiğinizde aslında bütçenizi optimize edebilirsiniz.

Eğer amacınız sadece kod yazdırmak değil, çalışan, ölçeklenebilir ve gelir getiren gerçek ürünler, SaaS ve otomasyon inşa etmekse Claude Code piyasadaki en iyi seçenek. Ve evet, ucuz mu? Değil. Karşılaştırma yaptığınızda yaptığı iş için ucuz mu? İnanılmaz ucuz. Çıkarttığı değer olarak inanılmaz ucuz. Ki ben buna bakıyorum açıkçası, bu bakış açısıyla bakıyorum. Ve ben Claude kodu kullanarak bir insana, bir şirkete web sitesi satabiliyorsam, bu web sitesi için 300 dolar, 500 dolar alabiliyorsam ve çıkan sonuç mükemmelse ve ben bu sonucu 2 saatte alabiliyorsam, ben oraya 10 dolar vermemle 5 dolar vermem arasında fark yok, 25 dolar vermem arasında da fark yok. O yüzden doğru şeylere odaklanmak lazım, mantıklı olan şeylere odaklanmak lazım: 3 dolara 5 dolar yerine ben buradan nasıl 300 dolar kazanabilirim, 500 dolar kazanabilirim'e bakmak lazım. Çünkü bu paraları insanlar kazanıyor.

## DOA topluluğu ve teknik bilgi olmadan satış yapmak

Direkt birazcık reklam gibi olacak olsa da kendi topluluğumun içerisindeki birçok işte ben bunu gördüm. Girişimcilerde bunu görüyorum, yorumlarda görüyorum. Ve insanlar kendi uygulamalarını teknik bilgileri olmadan yapıp satabiliyorlar. Şirketlere web sitesi satıyorlar, uygulama satabiliyorlar, sistemler kurabiliyorlar, ve bunların hepsi de aslında bu tarz sistemlerle olmuş oluyor.

Evet, bu videonun içerisinde baştan sona token maliyetlerini gösterdim. Bu maliyetler aslında sizin için direkt başlayabileceğiniz, görüntüleyebileceğiniz şekilde ve gerçek projelerle birlikte de örneklendirmiş oldum.

---

## Videodaki iddialar — tablo

Aşağıdakiler **konuşmacının iddiası**, bizim ölçümümüz değil. API fiyatı
üzerinden, 1 milyon token için:

| Kurulum | İddia edilen maliyet |
|---|---|
| Yalnızca Opus | 33 $ |
| Opus %20 + Sonnet %80 karışım | 11 $ |
| Sonnet 3.7 | 6 $ |
| Gemini | 4 $ |
| OpenAI Codex | 3 $ |

Üç proje örneği:

| Proje | Token | Claude Code | Gemini | Codex |
|---|---|---|---|---|
| Kurumsal web sitesi | ~150 K | 1.78 $ | 0.50 $ | 0.40 $ |
| YouTube otomasyon sistemi | ~200 K | 2.40 $ | 0.80 $ | 0.57 $ |
| UGC + sinematik uygulama | ~1 M | 12 $ | 4 $ | 3 $ |

Abonelik tarafında verdiği tek somut rakam: Max 20x = aylık 200 $, ~15 M token.

## Bizim için çıkarım

**Önce kötü haber: bu videonun sayıları bize doğrudan uygulanamaz.**

1. **Model kuşağı eski.** Video kendini Nisan 2026 diye tarihliyor ama
   Opus 4, Sonnet 3.7 ve Gemini 2.5'ten konuşuyor. Fiyat tablosu o kuşağın.
   Bugünkü fiyatı buradan okuma — Anthropic'in kendi fiyat sayfasına bak.
   (Bu ortamda `WebFetch` kapalı, doğrulayamıyorum; yerele geçince
   doğrulanabilir — `docs/yerel-kurulum.md`.)
2. **"750 kelime = 1000 token" Türkçe için yanlış tarafta.** Bu oran
   İngilizce metin için kaba bir yaklaşım. Türkçe sondan eklemeli ve
   tokenizer'da daha çok parçaya bölünüyor; aynı anlam için daha fazla
   token gider. Trace'in **her şeyi** Türkçe — CLAUDE.md, dokuz ajan, yedi
   skill, arayüz metinleri. Yani bizim token/kelime oranımız videodakinden
   yüksek, tersi değil.
3. **Videonun kıyas ettiği iş bizim işimiz değil.** "150 K token'a kurumsal
   web sitesi" tek seferlik üretim. Trace'in maliyeti her sabah çalışan
   Routine'de — tekrarlayan, küçük ama sürekli. Bunlar farklı maliyet
   profilleri; birinden ötekine oran taşınmaz.

**Geçerli olan tek fikir — ve bizde zaten uygulanmış olanı:**

Videonun asıl doğru saptaması "pahalı modeli her yerde kullanma"; rutin işi
ucuza, yargı gerektiren işi iyi modele ver. Trace bunu modelle değil
**mimariyle** çözmüş durumda: tarama, sınıflandırma, puanlama ve rapor
üretimi `pipeline.py` / `match.py` / `insights.py` içinde — bunlar
**sıfır token** harcıyor. Model yalnızca yargı gerektiren yerde devrede
(dokuz ajan). CLAUDE.md'de yazılı olan "ajan yalnızca yargı gerektiren
yerde kullanılır" kuralı, aynı zamanda projenin token stratejisi.

**Gözden geçirilecek tek somut nokta:** dokuz ajanın hepsi `model: opus`.
Videodaki karışım fikri burada karşılık bulabilir — ama körlemesine değil.
`ilan-cozumleyici` (ilan metnini yapılandırılmış alanlara çevirir) ve
`veri-denetleyici` (şemaya karşı denetler) kurala yakın, mekanik işler;
bunlar daha küçük bir modelde de çalışabilir. Buna karşılık
`kariyer-danismani`, `buyume-stratejisti` ve iki rol önericisi tam da
yargı işi — orada model küçültmek çıktının değerini düşürür.

**Ölçmeden değiştirme.** Şu an hiçbir ajanın token kullanımını ölçmüş
değiliz. Değişiklik yapılacaksa önce ölçüm: aynı girdiyle bir ajanı iki
modelde koşturup çıktı kalitesini karşılaştırmak. Videonun kendi tavsiyesi
de bu yöne çıkıyor zaten — "önce optimize et, sonra model değiştir."
