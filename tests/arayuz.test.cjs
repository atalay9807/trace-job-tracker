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
  const {dom, window, document, errors} = sayfa(); t.after(() => dom.window.close());
  for(const page of ['ana','basvurular','raporlar','egitim','profil','baglan']) {
    rota(window,page);
    assert.equal(document.querySelector('.page.on').id, 'p-'+page);
  }
  assert.equal(document.getElementById('cvFile').disabled, true);
  assert.equal(document.getElementById('demoNote').hidden, false);
  assert.equal(document.querySelectorAll('#tbody tr').length,68);
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
