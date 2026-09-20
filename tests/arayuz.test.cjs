// Gerçek şablonun JavaScript'i ağ erişimi kapalı bir DOM içinde çalıştırılır.
// Bu testler görsel/tarayıcı testinin yerine geçtiğini iddia etmez.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {JSDOM, VirtualConsole} = require('jsdom');
const source = fs.readFileSync(path.join(__dirname, '../site/app.html'), 'utf8');

function sayfa(mutator = () => {}, setup = () => {}) {
  const errors = [];
  const html = source.replace(/^const D = (.+);$/m, (_, json) => {
    const data = JSON.parse(json);
    mutator(data);
    return 'const D = ' + JSON.stringify(data).replace(/</g, '\\u003c') + ';';
  });
  const virtualConsole = new VirtualConsole();
  virtualConsole.on('jsdomError', e => errors.push(e.message));
  const dom = new JSDOM(html, {
    url: 'https://trace.example/app.html', runScripts: 'dangerously', virtualConsole,
    beforeParse(window) {
      window.matchMedia = () => ({matches: false});
      window.scrollTo = () => {};
      setup(window);
    }
  });
  return {dom, window: dom.window, document: dom.window.document, errors};
}

function bos(data) {
  data.applications = [];
  data.profile = null;
  data.stats = {total:0, active:0, interviews:0, interview_rate:0, stale:0};
  data.insights.learning_plan = [];
  data.insights.skill_gaps.rows = [];
  data.insights.trend = [];
  data.insights.track_success = [];
  data.insights.channel_success = [];
  data.insights.funnel.steps.forEach(s => {s.value=0; s.conv_from_prev=null;});
  data.insights.engagement = {tracking_started:null, days_tracked:0, reports_sent:0, current_streak:0,
    longest_streak:0, coverage:0, calendar:[], feedback_replies:0};
  data.insights.missed = {strong_missed:[], all_open:[], expired:[], not_applied:0, saved_total:0};
  data.insights.response_speed = {responded:0, measured:0, silent:0, median_days:null, buckets:[], basis:'Ölçüm yok.'};
  data.role_targets = {meta:{}, hedefler:[]};
}

function rota(window, name) {
  window.location.hash = '#/' + name;
  window.dispatchEvent(new window.HashChangeEvent('hashchange'));
}

const cv = {name:'ornek.txt', size:200, text:async () => 'Örnek adayın deneyim ve yetkinlik metni. '.repeat(5)};

test('Demo altı sayfada açılır; desteklenmeyen CV seçimi kapalıdır', t => {
  // Beklenen satır sayısı veriden okunur, sabit kodlanmaz: demo veri gerçek
  // veriden yeniden üretiliyor ve kayıt sayısı her üretimde değişiyor.
  let beklenen = 0;
  const {dom, window, document, errors} = sayfa(d => { beklenen = d.applications.length; });
  t.after(() => dom.window.close());
  for(const page of ['ana','basvurular','raporlar','egitim','profil','baglan']) {
    rota(window,page);
    assert.equal(document.querySelector('.page.on').id, 'p-'+page);
  }
  assert.equal(document.getElementById('cvFile').disabled, true);
  assert.equal(document.getElementById('demoNote').hidden, false);
  assert.ok(beklenen > 0, 'demo veri boş olmamalı');
  assert.equal(document.querySelectorAll('#tbody tr').length, beklenen);
  assert.deepEqual(errors,[]);
});

test('Boş veri ve eksik profil tüm sayfalarda hata vermeden gösterilir', t => {
  const {dom, window, document, errors} = sayfa(bos); t.after(() => dom.window.close());
  for(const name of ['ana','basvurular','raporlar','egitim','profil','baglan']) rota(window,name);
  assert.match(document.getElementById('eduSub').textContent,/Henüz eğitim önerisi/);
  assert.equal(document.querySelectorAll('#tbody tr').length,0);
  assert.doesNotMatch(document.querySelector(".wrap").textContent,/NaN|undefined|Infinity/);
  assert.deepEqual(errors,[]);
});

test('Puanı ve son temas tarihi bilinmeyen kaydın detayında null görünmez', t => {
  const {dom, window, document, errors} = sayfa(d => {
    Object.assign(d.applications[0],{match_score:null, match_segment_key:null, match_rationale:null,
      match_breakdown:[], last_contact:null, days_silent:null});
  }); t.after(() => dom.window.close());
  const id = document.querySelector('#tbody tr').dataset.id;
  rota(window,'basvurular/'+id);
  assert.match(document.getElementById('dBody').textContent,/Puanlanmadı/);
  assert.doesNotMatch(document.getElementById('dBody').textContent,/null|undefined/);
  assert.deepEqual(errors,[]);
});

test('Son 7 gün filtresi geleceği ve yedinci gün sınırını dışarıda bırakır', t => {
  const {dom, window, document} = sayfa(d => {
    d.meta.last_scan='2026-09-17';
    const app=d.applications[0];
    d.applications=['2026-09-18','2026-09-17','2026-09-11','2026-09-10'].map((applied,i)=>({...app,id:'gun-'+i,applied}));
  }); t.after(() => dom.window.close());
  const select = document.getElementById('dateRange');
  select.value='son7'; select.dispatchEvent(new window.Event('change'));
  assert.equal(document.querySelectorAll('#tbody tr').length,2);
});

test('Türkçe arama ve boş sonuç durumu çalışır', t => {
  const {dom, window, document} = sayfa(d => {d.applications[0].company='İLERİ TEKNOLOJİ';}); t.after(() => dom.window.close());
  const search = document.getElementById('search');
  search.value='ileri'; search.dispatchEvent(new window.Event('input'));
  assert.equal(document.querySelectorAll('#tbody tr').length,1);
  search.value='kesinlikle-bulunmayan'; search.dispatchEvent(new window.Event('input'));
  assert.equal(document.getElementById('empty').hidden,false);
});

test('Gmail hakkında düğmesi sahte bağlantı başlatmaz', t => {
  const {dom, document} = sayfa(); t.after(() => dom.window.close());
  document.getElementById('gmailBtn').click();
  assert.match(document.getElementById('gmErr').textContent,/bağlantısı kurulmaz/);
  assert.match(document.getElementById('gmStat').textContent,/Bağlı değil/);
  assert.equal(document.getElementById('gmailBtn').disabled,false);
});

test('URL protokolü ve HTML metni çalıştırılabilir içeriğe dönüşmez', t => {
  const {dom, window, document, errors} = sayfa(d => {
    d.applications[0].company='<img src=x onerror="alert(1)">';
    d.applications[0].links_actions=[{url:'javascript:alert(1)', label:'Bağlantı', kind:'ext'}];
  }); t.after(() => dom.window.close());
  assert.equal(document.querySelector('#tbody img'),null);
  assert.equal(document.querySelector('a[href^="javascript:"]'),null);
  assert.equal(window.safeURL('https://user:pass@example.com'),'#');
  assert.deepEqual(errors,[]);
});

test('Tema ve tanıtım turu açılıp kapanır', t => {
  const {dom, document} = sayfa(); t.after(() => dom.window.close());
  document.getElementById('themeBtn').click();
  assert.equal(document.documentElement.dataset.theme,'dark');
  document.getElementById('tourBtn').focus();
  document.getElementById('tourBtn').click();
  assert.equal(document.getElementById('tourWrap').classList.contains('on'),true);
  assert.equal(document.activeElement.id,'tourSkip');
  document.getElementById('tourSkip').click();
  assert.equal(document.getElementById('tourWrap').classList.contains('on'),false);
  assert.equal(document.activeElement.id,'tourBtn');
});

test('CV analizi desteklenmediğinde sağlayıcıya hiç gidilmez', async t => {
  let calls=0;
  const {dom, window, document} = sayfa(()=>{}, w => {w.claude={use:async()=>{calls++;}};});
  t.after(() => dom.window.close());
  await window.handleCV(cv);
  assert.equal(calls,0);
  assert.match(document.getElementById('cvErr').textContent,/kullanılamıyor/);
});

test('Destekli ortamda CV paylaşım onayı olmadan analiz başlamaz', async t => {
  let calls=0;
  const {dom, window, document} = sayfa(d=>{d.demo=false;}, w=>{w.claude={use:async()=>{calls++;}};});
  t.after(() => dom.window.close());
  await window.handleCV(cv);
  assert.equal(calls,0);
  assert.match(document.getElementById('cvErr').textContent,/onay/);
});

test('Sağlayıcı izin hatası yakalanır ve sonraki deneme mümkün kalır', async t => {
  const {dom, window, document} = sayfa(d=>{d.demo=false;}, w=>{w.claude={use:async()=>{throw Error('not_granted');}};});
  t.after(() => dom.window.close());
  document.getElementById('cvConsent').checked=true;
  await window.handleCV(cv);
  assert.match(document.getElementById('cvErr').textContent,/başlatılamadı/);
  assert.equal(document.getElementById('cvFile').disabled,false);
});

test('Geçerli CV yanıtı gösterilir; eşzamanlı ikinci istek engellenir', async t => {
  let calls=0;
  const {dom, window, document} = sayfa(d=>{d.demo=false;}, w=>{w.claude={use:async()=>({json:async()=>{calls++; return {ad:'Örnek Aday',beceriler:[],aciklar:[]};}})};});
  t.after(() => dom.window.close());
  document.getElementById('cvConsent').checked=true;
  await Promise.all([window.handleCV(cv),window.handleCV(cv)]);
  assert.equal(calls,1);
  assert.match(document.getElementById('cvOut').textContent,/Örnek Aday/);
  assert.equal(document.getElementById('cvFile').disabled,false);
});

test('Modelin şema dışı yanıtı kullanıcıya anlaşılır hata verir', async t => {
  const {dom, window, document} = sayfa(d=>{d.demo=false;}, w=>{w.claude={use:async()=>({json:async()=>({beceriler:'hatalı'})})};});
  t.after(() => dom.window.close());
  document.getElementById('cvConsent').checked=true;
  await window.handleCV(cv);
  assert.match(document.getElementById('cvErr').textContent,/beklenen biçimde değil/);
  assert.equal(document.getElementById('cvFile').disabled,false);
});

function listeOrnegi(data) {
  const temel = data.applications[0];
  data.meta.last_scan = '2026-09-20';
  data.applications = [
    {id:'isik', company:'Işık', score:35, band:'low', match_score:50, match_segment_key:'fair',
      applied:'2026-09-10', deadline:'2026-09-22', closed:false},
    {id:'ileri', company:'İleri', score:80, band:'high', match_score:0, match_segment_key:'weak',
      applied:'2026-09-14', deadline:'2026-09-20', closed:false},
    {id:'cinar', company:'Çınar', score:80, band:'high', match_score:null, match_segment_key:null,
      applied:null, deadline:null, closed:false},
    {id:'anka', company:'Anka', score:0, band:'archive', match_score:90, match_segment_key:'strong',
      applied:'2026-09-18', deadline:'2026-09-01', closed:true, stage:'closed'}
  ].map(a => ({...temel, stage:'under_review', status:'in_progress', role:'Uzman',
    last_contact:'2026-09-19', links_actions:[], gap_skills:[], ...a}));
}

function sec(window, document, id, value) {
  const element = document.getElementById(id);
  element.value = value;
  element.dispatchEvent(new window.Event(element.tagName === 'INPUT' ? 'input' : 'change'));
}

function satirKimlikleri(document) {
  return [...document.querySelectorAll('#tbody tr')].map(row => row.dataset.id);
}

test('Altı sıralama çalışır; eksik değerler ve kapalı süreçler doğru yerde kalır', t => {
  const {dom, window, document, errors} = sayfa(listeOrnegi);
  t.after(() => dom.window.close());
  const once = window.eval('JSON.stringify(D.applications)');
  const beklenen = {
    aciliyet:['cinar','ileri','isik','anka'],
    'eslesme-azalan':['anka','isik','ileri','cinar'],
    'eslesme-artan':['ileri','isik','anka','cinar'],
    'basvuru-yeni':['anka','ileri','isik','cinar'],
    'deadline-yakin':['ileri','isik','cinar','anka'],
    sirket:['anka','cinar','isik','ileri']
  };
  for (const [siralama, ids] of Object.entries(beklenen)) {
    sec(window, document, 'sortOrder', siralama);
    assert.deepEqual(satirKimlikleri(document), ids, siralama);
  }
  assert.equal(window.eval('JSON.stringify(D.applications)'), once);
  assert.deepEqual(errors, []);
});

test('Puanlanmamış kayıt ayrı bulunur; sıfır puan bilinmeyen sayılmaz', t => {
  const {dom, document} = sayfa(listeOrnegi); t.after(() => dom.window.close());
  document.querySelector('[data-s="unscored"]').click();
  assert.deepEqual(satirKimlikleri(document), ['cinar']);
  assert.match(document.getElementById('tbody').textContent, /Puanlanmadı/);
  document.querySelector('[data-s="weak"]').click();
  assert.deepEqual(satirKimlikleri(document), ['ileri']);
  assert.match(document.getElementById('tbody').textContent, /0/);
});

test('Aksiyon bekleyen kritik kayıt daha yüksek puanlı normal işlerden önce gelir', t => {
  const {dom, document} = sayfa(d => {
    listeOrnegi(d);
    Object.assign(d.applications[0], {band:'critical', score:20, status:'action_required'});
  }); t.after(() => dom.window.close());
  assert.deepEqual(satirKimlikleri(document), ['isik','cinar','ileri','anka']);
});

test('Düşük aciliyet ve kapanan süreç filtreleri eksiksizdir', t => {
  const {dom, window, document} = sayfa(listeOrnegi); t.after(() => dom.window.close());
  document.querySelector('[data-b="low"]').click();
  assert.deepEqual(satirKimlikleri(document), ['isik']);
  document.querySelector('[data-b="archive"]').click();
  assert.deepEqual(satirKimlikleri(document), ['anka']);
  assert.equal(document.querySelector('[data-b="archive"]').textContent, 'Kapanan');
  document.getElementById('resetFilters').click();
  sec(window, document, 'processState', 'open');
  assert.deepEqual(satirKimlikleri(document), ['cinar','ileri','isik']);
  sec(window, document, 'processState', 'closed');
  assert.deepEqual(satirKimlikleri(document), ['anka']);
});

test('Arama, tarih, aciliyet, eşleşme ve süreç filtreleri birlikte uygulanır', t => {
  const {dom, window, document} = sayfa(listeOrnegi); t.after(() => dom.window.close());
  document.querySelector('[data-b="high"]').click();
  document.querySelector('[data-s="weak"]').click();
  sec(window, document, 'processState', 'open');
  sec(window, document, 'dateRange', 'son7');
  sec(window, document, 'search', 'İLERİ');
  assert.deepEqual(satirKimlikleri(document), ['ileri']);
  assert.equal(document.getElementById('tblCount').textContent, '1 / 4 başvuru');
  sec(window, document, 'dateRange', 'son30');
  sec(window, document, 'search', 'IŞIK');
  assert.deepEqual(satirKimlikleri(document), []);
  assert.equal(document.getElementById('empty').hidden, false);
  assert.equal(document.getElementById('exportCsv').disabled, true);
});

test('Filtreleri temizleme tüm denetimleri ve varsayılan sıralamayı geri getirir', t => {
  const {dom, window, document} = sayfa(listeOrnegi); t.after(() => dom.window.close());
  document.querySelector('[data-b="low"]').click();
  document.querySelector('[data-s="unscored"]').click();
  for (const [id,value] of Object.entries({processState:'closed', dateField:'last_contact',
    dateRange:'son7', search:'aranan', sortOrder:'sirket'})) sec(window, document, id, value);
  assert.equal(document.getElementById('resetFilters').disabled, false);
  document.getElementById('resetFilters').click();
  assert.deepEqual(satirKimlikleri(document), ['cinar','ileri','isik','anka']);
  for (const [id,value] of Object.entries({processState:'all', dateField:'applied',
    dateRange:'all', search:'', sortOrder:'aciliyet'})) assert.equal(document.getElementById(id).value, value);
  assert.equal(document.querySelector('#bandGroup [aria-pressed="true"]').dataset.b, 'all');
  assert.equal(document.querySelector('#segGroup [aria-pressed="true"]').dataset.s, 'all');
  assert.equal(document.querySelectorAll('#dateGroup .on').length, 0);
  assert.equal(document.getElementById('resetFilters').disabled, true);
  assert.equal(document.getElementById('exportCsv').disabled, false);
});

test('CSV yalnızca görünen kayıtları ekran sırasıyla içerir; bilinmeyen puan boş kalır', t => {
  const {dom, window, document} = sayfa(listeOrnegi); t.after(() => dom.window.close());
  sec(window, document, 'processState', 'open');
  sec(window, document, 'sortOrder', 'eslesme-artan');
  const csv = window.gorunenCsvOlustur();
  assert.equal(csv[0], '\uFEFF');
  const satirlar = csv.trimEnd().split('\r\n');
  assert.equal(satirlar.length, 4);
  assert.deepEqual(satirlar.slice(1).map(row => row.split(',')[0]), ['"ileri"','"isik"','"cinar"']);
  assert.match(satirlar[1], /,"0",/);
  assert.equal(satirlar[3].split(',')[11], '""');
  assert.doesNotMatch(csv, /"anka"/);
  assert.match(csv, /"Şirket"/);
});

test('CSV hücreleri virgül, tırnak, satır sonu ve formül başlangıçlarını korumalı aktarır', t => {
  const {dom, window} = sayfa(listeOrnegi); t.after(() => dom.window.close());
  assert.equal(window.csvHucre('A, "B"\r\nC'), '"A, ""B""\r\nC"');
  assert.equal(window.csvHucre(null), '""');
  assert.equal(window.csvHucre(0), '"0"');
  assert.equal(window.csvHucre(-2), '"-2"');
  for (const metin of ['=1+1', '+1+1', '-1+1', '@SUM(1)', ' \t=1+1', '\r=1+1', '\nmetin', '\u0000=1+1']) {
    assert.ok(window.csvHucre(metin).startsWith('"\''), JSON.stringify(metin));
  }
  const csv = window.gorunenCsvOlustur([{id:'ornek', company:'=1+1', role:'A, "B"',
    notes:'GİZLİ NOT', contact:'gizli@example.com', links_actions:[{url:'https://secret.example'}]}]);
  assert.match(csv, /"'=1\+1"/);
  assert.match(csv, /"A, ""B"""/);
  assert.doesNotMatch(csv, /GİZLİ|gizli@|secret.example/);
});

test('CSV indirme düğmesi dosya oluşturur, indirme bağlantısını ve adresini temizler', async t => {
  let dosya, indirme, iptal, gecikmeliTemizlik;
  const {dom, window, document, errors} = sayfa(listeOrnegi, w => {
    w.URL.createObjectURL = blob => {dosya = blob; return 'blob:trace-test';};
    w.URL.revokeObjectURL = adres => {iptal = adres;};
    w.HTMLAnchorElement.prototype.click = function () {indirme = {ad:this.download, adres:this.href, bagli:this.isConnected};};
    const zamanlayici = w.setTimeout.bind(w);
    w.setTimeout = (callback, delay, ...args) => {
      if (delay === 1000) {gecikmeliTemizlik = callback; return 0;}
      return zamanlayici(callback, delay, ...args);
    };
  }); t.after(() => dom.window.close());
  sec(window, document, 'search', 'İleri');
  document.getElementById('exportCsv').click();
  assert.deepEqual(indirme, {ad:'trace-demo-basvurular-2026-09-20.csv', adres:'blob:trace-test', bagli:true});
  assert.equal(dosya.type, 'text/csv;charset=utf-8');
  const metin = await new Promise((resolve, reject) => {
    const okuyucu = new window.FileReader();
    okuyucu.onload = () => resolve(okuyucu.result);
    okuyucu.onerror = reject;
    okuyucu.readAsText(dosya);
  });
  assert.match(metin, /"İleri"/);
  assert.doesNotMatch(metin, /"Anka"/);
  assert.equal(document.querySelector('a[download]'), null);
  assert.match(document.getElementById('toast').textContent, /1 başvuru/);
  gecikmeliTemizlik();
  assert.equal(iptal, 'blob:trace-test');
  assert.deepEqual(errors, []);
});

test('CSV indirme desteklenmediğinde hata görünür ve tekrar deneme açık kalır', t => {
  const {dom, document, errors} = sayfa(listeOrnegi); t.after(() => dom.window.close());
  document.getElementById('exportCsv').click();
  assert.match(document.getElementById('toast').textContent, /indirilemedi/);
  assert.equal(document.getElementById('exportCsv').disabled, false);
  assert.deepEqual(errors, []);
});

test('Kayıt yoksa boş durum açıklanır ve CSV indirilemez', t => {
  const {dom, document} = sayfa(bos); t.after(() => dom.window.close());
  assert.equal(document.getElementById('empty').textContent, 'Henüz başvuru kaydı yok.');
  assert.equal(document.getElementById('exportCsv').disabled, true);
  assert.equal(document.getElementById('resetFilters').disabled, true);
});

test('Satırdaki bağlantı klavye ile açılırken detay yönlendirmesi araya girmez', t => {
  const {dom, window, document} = sayfa(d => {
    listeOrnegi(d);
    d.applications.forEach(a => {a.links_actions=[{url:'https://example.com', label:'İlan', kind:'ext'}];});
  }); t.after(() => dom.window.close());
  const satir = document.querySelector('#tbody tr');
  const baglanti = satir.querySelector('a');
  const olay = new window.KeyboardEvent('keydown', {key:'Enter', bubbles:true, cancelable:true});
  baglanti.dispatchEvent(olay);
  assert.equal(olay.defaultPrevented, false);
  assert.equal(window.location.hash, '');
  satir.dispatchEvent(new window.KeyboardEvent('keydown', {key:'Enter', bubbles:true, cancelable:true}));
  assert.equal(window.location.hash, '#/basvurular/' + satir.dataset.id);
});
