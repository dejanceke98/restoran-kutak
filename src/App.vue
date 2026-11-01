<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import menuData from '../menu.json'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'
const menu = ref([])
const apiOnline = ref(false)
const sending = ref(false)
const notice = ref('')
const noticeType = ref('success')
const today = new Date().toISOString().slice(0, 10)
const form = reactive({ name: '', phone: '', date: '', time: '19:00', guests: '2', note: '' })

const menuCategories = computed(() => {
  const grouped = new Map()
  for (const dish of menu.value) {
    if (!grouped.has(dish.category)) grouped.set(dish.category, [])
    grouped.get(dish.category).push(dish)
  }
  return Array.from(grouped, ([name, items]) => ({ name, items }))
})
const formattedDate = computed(() => form.date ? new Date(`${form.date}T12:00:00`).toLocaleDateString('sr-RS') : '')

onMounted(async () => {
  try {
    const [health, dishes] = await Promise.all([
      fetch(`${API_URL}/api/health`),
      fetch(`${API_URL}/api/menu`),
    ])
    if (!health.ok || !dishes.ok) throw new Error('API nije dostupan')
    menu.value = await dishes.json()
    apiOnline.value = true
  } catch {
    menu.value = menuData
  }
})

async function submitReservation() {
  notice.value = ''
  sending.value = true
  try {
    const response = await fetch(`${API_URL}/api/reservations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })
    const result = await response.json()
    if (!response.ok) throw new Error(result.error || 'Rezervacija nije poslata.')
    noticeType.value = 'success'
    notice.value = `${result.message} Hvala, ${form.name}! Sto za ${form.guests} ${Number(form.guests) === 1 ? 'osobu' : 'osobe'} tražen je za ${formattedDate.value} u ${form.time}.`
    Object.assign(form, { name: '', phone: '', date: '', time: '19:00', guests: '2', note: '' })
  } catch (error) {
    noticeType.value = 'danger'
    notice.value = error instanceof TypeError
      ? 'Ne možemo da se povežemo sa serverom. Proverite da li je Flask pokrenut.'
      : error.message
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light site-nav sticky-top">
      <div class="container">
        <a class="navbar-brand d-flex align-items-center gap-2" href="#pocetna" aria-label="Kutak, početna">
          <span class="brand-logo" role="img" aria-label="Kutak Gastro Bar logo"></span>
          <span class="brand-wordmark"><span class="brand-title"><span>K</span><span class="brand-coffee-u">U</span><span>T</span><span>A</span><span class="brand-reversed-k">K</span></span><span class="brand-subtitle"><i></i>GASTRO BAR<i></i></span></span>
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav" aria-controls="mainNav" aria-expanded="false" aria-label="Otvori navigaciju">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div id="mainNav" class="collapse navbar-collapse">
          <div class="navbar-nav ms-auto align-items-lg-center gap-lg-4">
            <a class="nav-link" href="#meni">Naš meni</a>
            <a class="nav-link" href="#prica">Naša priča</a>
            <a class="nav-link" href="#poseta">Pronađite nas</a>
            <a class="btn btn-brand nav-book" href="#rezervacija">Rezervišite sto <span aria-hidden="true">↗</span></a>
          </div>
        </div>
      </div>
    </nav>

    <main>
      <section id="pocetna" class="hero-section">
        <div class="hero-orb hero-orb-one"></div>
        <div class="hero-orb hero-orb-two"></div>
        <div class="container hero-content">
          <div class="row align-items-center gy-5">
            <div class="col-lg-6">
              <div class="eyebrow"><span class="eyebrow-line"></span> DOBRO DOŠLI U NAŠ KUTAK</div>
              <h1>Mesto gde<br />se <span>ostaje</span><br />još malo.</h1>
              <p class="hero-copy">Domaći ukusi, duga druženja i sto za kojim uvek ima mesta za još jednog.</p>
              <div class="d-flex flex-wrap gap-3 hero-actions">
                <a class="btn btn-brand btn-lg" href="#meni">Otkrijte naš meni <span aria-hidden="true">↗</span></a>
                <a class="btn btn-outline-light btn-lg" href="#prica">Upoznajte Kutak</a>
              </div>
              <div class="hero-note"><span class="note-stars">★★★★★</span><span>Mali restoran. Veliko zadovoljstvo.</span></div>
            </div>
            <div class="col-lg-6">
              <div class="hero-visual" role="img" aria-label="Ilustracija tanjira domaće hrane na stolu">
                <div class="visual-label"><span class="label-dot"></span> KUHANO S LJUBAVLJU</div>
                <div class="plate-shadow"></div>
                <div class="plate">
                  <div class="plate-inner">
                    <div class="food-bed"></div>
                    <div class="food-piece piece-one"></div><div class="food-piece piece-two"></div><div class="food-piece piece-three"></div>
                    <div class="herb herb-one">✦</div><div class="herb herb-two">✦</div><div class="herb herb-three">✦</div>
                    <div class="food-sauce"></div>
                  </div>
                </div>
                <div class="floating-card"><span class="floating-icon">✿</span><div><strong>Sveže svakog dana</strong><small>Od lokalnih sastojaka</small></div></div>
                <div class="visual-sun"></div>
                <div class="visual-stem stem-a"></div><div class="visual-stem stem-b"></div><div class="visual-stem stem-c"></div>
                <div class="visual-caption">Sezonsko. Domaće. Naše.</div>
              </div>
            </div>
          </div>
          <div class="hero-bottom"><span>01 — 03</span><span class="bottom-rule"></span><span>UKUS KOJI VRAĆA</span></div>
        </div>
      </section>

      <section class="promise-strip" aria-label="Naše vrednosti">
        <div class="container promise-grid">
          <div><span class="promise-icon">✳</span><span>Pažljivo birani sastojci</span></div>
          <div><span class="promise-icon">⌂</span><span>Ukus kao kod kuće</span></div>
          <div><span class="promise-icon">♡</span><span>Uvek topla dobrodošlica</span></div>
        </div>
      </section>

      <section id="meni" class="menu-section section-pad">
        <div class="container">
          <div class="section-heading text-center">
            <div class="eyebrow eyebrow-green"><span class="eyebrow-line"></span> KUTAK GASTRO BAR <span class="eyebrow-line"></span></div>
            <h2>Naš <em>jelovnik.</em></h2>
            <p>Doručak, omiljeni klasici i nešto slatko za kraj.</p>
          </div>
          <div class="menu-categories row g-5">
            <section v-for="category in menuCategories" :key="category.name" class="col-md-6 menu-category">
              <h3 class="menu-category-title">{{ category.name }}</h3>
              <article v-for="dish in category.items" :key="dish.id" class="menu-item">
                <div class="menu-item-heading">
                  <h4>{{ dish.name }}</h4>
                  <span class="menu-price">{{ dish.price.toLocaleString('sr-RS') }} <small>RSD</small></span>
                </div>
                <p v-if="dish.description" class="menu-description">{{ dish.description }}</p>
              </article>
            </section>
          </div>
          <div class="text-center menu-footnote">Sve cene su izražene u dinarima.</div>
        </div>
      </section>

      <section id="prica" class="story-section section-pad">
        <div class="container">
          <div class="row align-items-center gy-5">
            <div class="col-lg-6">
              <div class="story-art">
                <div class="story-frame"><div class="story-arch"><span class="arch-sun"></span><span class="arch-table"></span><span class="arch-vase">✿</span></div></div>
                <div class="story-stamp"><span>OD</span><strong>2026</strong><span>S LJUBAVLJU</span></div>
                <div class="story-scribble">mali<br />trenuci,<br /><em>veliki</em><br />ukusi.</div>
              </div>
            </div>
            <div class="col-lg-5 offset-lg-1">
              <div class="eyebrow eyebrow-green"><span class="eyebrow-line"></span> NAŠA PRIČA</div>
              <h2 class="story-title">Nismo samo<br />restoran. Mi smo<br /><em>vaš Kutak.</em></h2>
              <p class="story-copy">Kutak je nastao iz jednostavne želje — da napravimo mesto na koje ćete doći gladni, a otići siti, nasmejani i već razmišljati o sledećoj poseti.</p>
              <p class="story-copy">Kuvamo polako, biramo lokalno i verujemo da je najbolji sastojak svakog jela osećaj da ste dobrodošli.</p>
              <a class="text-link" href="#poseta">Čekamo vas za stolom <span aria-hidden="true">→</span></a>
              <div class="signature">Vaši domaćini <span>♡</span></div>
            </div>
          </div>
        </div>
      </section>

      <section class="quote-section">
        <div class="container text-center">
          <span class="quote-mark">“</span>
          <blockquote>Najlepši razgovori počinju<br />kad stigne <em>hrana na sto.</em></blockquote>
          <div class="quote-sign"><span></span> KUTAK FILOZOFIJA <span></span></div>
        </div>
      </section>

      <section id="rezervacija" class="reservation-section section-pad">
        <div class="container">
          <div class="row g-0 reservation-wrap">
            <div class="col-lg-5 reservation-aside">
              <div class="eyebrow"><span class="eyebrow-line"></span> VAŠ STO VAS ČEKA</div>
              <h2>Sačuvajte<br />mesto za<br /><em>lepe trenutke.</em></h2>
              <p>Recite nam kada dolazite. Mi ćemo se pobrinuti za ostalo.</p>
              <div class="aside-detail"><span>01</span><div><strong>Bez žurbe</strong><small>Vaš sto čuvamo 15 minuta.</small></div></div>
              <div class="aside-detail"><span>02</span><div><strong>Za posebne prilike</strong><small>Napišite nam želje u napomeni.</small></div></div>
              <div class="reservation-decoration">K.</div>
            </div>
            <div class="col-lg-7 reservation-form-wrap">
              <div class="form-heading"><span>REZERVACIJA</span><span class="api-status" :class="{ online: apiOnline }"><i></i>{{ apiOnline ? 'SISTEM DOSTUPAN' : 'DEMO PRIKAZ' }}</span></div>
              <div v-if="notice" class="alert" :class="`alert-${noticeType}`" role="status">{{ notice }}</div>
              <form class="row g-3" @submit.prevent="submitReservation">
                <div class="col-md-6"><label class="form-label" for="guest-name">Vaše ime</label><input id="guest-name" v-model.trim="form.name" class="form-control" name="name" autocomplete="name" placeholder="npr. Milica Petrović" required /></div>
                <div class="col-md-6"><label class="form-label" for="guest-phone">Broj telefona</label><input id="guest-phone" v-model.trim="form.phone" class="form-control" name="phone" type="tel" autocomplete="tel" placeholder="+381 60 123 4567" required /></div>
                <div class="col-md-6"><label class="form-label" for="reservation-date">Datum</label><input id="reservation-date" v-model="form.date" class="form-control" name="date" type="date" :min="today" required /></div>
                <div class="col-md-3"><label class="form-label" for="reservation-time">Vreme</label><select id="reservation-time" v-model="form.time" class="form-select" name="time"><option>12:00</option><option>13:00</option><option>14:00</option><option>18:00</option><option>19:00</option><option>20:00</option><option>21:00</option></select></div>
                <div class="col-md-3"><label class="form-label" for="guest-count">Osoba</label><select id="guest-count" v-model="form.guests" class="form-select" name="guests"><option v-for="number in 12" :key="number" :value="String(number)">{{ number }}</option></select></div>
                <div class="col-12"><label class="form-label" for="guest-note">Posebna napomena <span>(opciono)</span></label><textarea id="guest-note" v-model.trim="form.note" class="form-control" name="note" rows="3" placeholder="Proslava, dečja stolica, omiljeni kutak…"></textarea></div>
                <div class="col-12 d-flex flex-wrap justify-content-between align-items-center gap-3 form-submit-row"><small>Rezervacija je potvrđena nakon našeg poziva.</small><button class="btn btn-brand btn-lg" type="submit" :disabled="sending"><span v-if="sending" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>{{ sending ? 'Šaljemo…' : 'Pošalji rezervaciju' }} <span v-if="!sending" aria-hidden="true">↗</span></button></div>
              </form>
            </div>
          </div>
        </div>
      </section>

      <section id="poseta" class="visit-section section-pad">
        <div class="container">
          <div class="row gy-5">
            <div class="col-lg-5"><div class="eyebrow eyebrow-green"><span class="eyebrow-line"></span> GDE SE VIDIMO?</div><h2>Uvek ima<br />mesta u <em>Kutku.</em></h2><p>Navratite na ručak, ostanite na još jednoj priči.</p></div>
            <div class="col-lg-7"><div class="row g-4 visit-details">
              <div class="col-sm-6"><span class="detail-number">ADRESA</span><h3>Pronađite nas</h3><p>Bulevar Cara Lazara 19<br />Novi Sad, Srbija</p></div>
              <div class="col-sm-6"><span class="detail-number">RADNO VREME</span><h3>Otvorena vrata</h3><p>Pon–Pet &nbsp; 07:30 – 23:00<br />Sub &nbsp; 08:00 – 00:00<br />ned &nbsp; 08:00 – 23:00</p></div>
              <div class="col-sm-6"><span class="detail-number">POZOVITE</span><h3>Tu smo za vas</h3><a href="tel:+381112345678">+38166-5665-792</a></div>
              <div class="col-sm-6"><span class="detail-number">ZAPIŠITE</span><h3>Za vašu sledeću posetu</h3><p>Rezervacije primamo i putem forme iznad.</p></div>
            </div></div>
          </div>
          <div class="hours-banner"><span class="hours-star">✳</span><span>Dobro društvo, dobra hrana, bez gledanja na sat.</span><a href="#rezervacija">Pronađite svoj sto <span aria-hidden="true">↗</span></a></div>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <div class="container footer-main"><a class="footer-brand" href="#pocetna" aria-label="Kutak, početna"><span class="brand-logo" role="img" aria-label="Kutak Gastro Bar logo"></span><span class="brand-wordmark"><span class="brand-title"><span>K</span><span class="brand-coffee-u">U</span><span>T</span><span>A</span><span class="brand-reversed-k">K</span></span><span class="brand-subtitle"><i></i>GASTRO BAR<i></i></span></span></a><p>Mali restoran sa velikim srcem.<br />Svratite, osećajte se kao kod kuće.</p><a href="#pocetna" class="back-top">NA VRH ↑</a></div>
      <div class="container footer-bottom"><span>© 2026 Kutak. S ljubavlju, za vaš sto.</span><span>DOMAĆE JE UVEK NAJBOLJE <span class="footer-heart">♥</span></span></div>
    </footer>
  </div>
</template>
