// Contract tests in a simulated DOM. These do not validate browser layout or send email.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync('script.js', 'utf8');

class Element {
  constructor() {
    this.attrs = {};
    this.events = new Map();
    this.classes = new Set();
    this.dataset = {};
    this.textContent = '';
    this.children = [];
    this.classList = {
      add: name => this.classes.add(name),
      remove: name => this.classes.delete(name),
      toggle: (name, on) => on ? this.classes.add(name) : this.classes.delete(name),
    };
  }
  addEventListener(name, callback) {
    const list = this.events.get(name) || [];
    list.push(callback);
    this.events.set(name, list);
  }
  dispatch(name, props = {}) {
    const event = {target: this, defaultPrevented: false,
      preventDefault() { this.defaultPrevented = true; }, ...props};
    for (const callback of this.events.get(name) || []) callback(event);
    return event;
  }
  setAttribute(name, value) { this.attrs[name] = String(value); }
  getAttribute(name) { return this.attrs[name]; }
  querySelector(selector) { return this.nodes?.[selector] || null; }
  querySelectorAll(selector) { return this.lists?.[selector] || []; }
  replaceChildren(...children) { this.children = children; }
  focus() { this.focused = true; }
  closest() { return null; }
  getBoundingClientRect() { return this.rect; }
}

// Different row heights/positions model wrapped content; these are supplied rectangles,
// not a claim about the CSS layout produced by a browser at each viewport.
const sizes = {
  375: {width: 20, height: 540, offsets: [14, 207, 412], heights: [28, 28, 28]},
  430: {width: 20, height: 495, offsets: [10, 181, 376], heights: [28, 28, 28]},
  768: {width: 32, height: 390, offsets: [12, 145, 298], heights: [30, 30, 30]},
  1024: {width: 32, height: 345, offsets: [9, 128, 259], heights: [30, 30, 30]},
  1440: {width: 32, height: 330, offsets: [8, 124, 250], heights: [30, 30, 30]},
};

function fixture(viewport = 1440, {reduced = false, observers = true, fonts = true,
    modal = true, emptyPage = false} = {}) {
  const menu = new Element(), nav = new Element(), dialog = new Element();
  const stage = new Element(), close = new Element(), caption = new Element();
  const link = new Element(), form = new Element(), message = new Element();
  const status = new Element(), timeline = new Element(), reveal = new Element();
  const svg = new Element(), path = new Element();
  const dots = Array.from({length: 3}, () => new Element());
  const dates = Array.from({length: 3}, () => new Element());
  const document = new Element(), window = new Element();
  const resizeObservers = [], intersectionObservers = [], mediaEvents = new Map();
  let fetchCalls = 0, resetCalls = 0, validityReports = 0;
  let geometry = sizes[viewport];
  menu.setAttribute('aria-expanded', 'false');
  nav.lists = {'a': [new Element(), new Element()]};
  link.dataset.zoom = 'images/original-flyer.webp';
  link.nodes = {'img': {alt: 'myLEDmask — visuel original'}};
  dialog.nodes = {'.zoom-stage': stage, '.close-lightbox': close, '.zoom-caption': caption};
  if (modal) dialog.showModal = () => { dialog.open = true; };
  dialog.close = () => { dialog.open = false; dialog.dispatch('close'); };
  message.value = 'Bonjour, je souhaite vous contacter.';
  message.setCustomValidity = value => { message.customValidity = value; };
  form.nodes = {'#message': message};
  form.dataset.configured = 'true';
  form.dataset.nativeService = 'true';
  form.valid = true;
  form.reportValidity = () => { validityReports++; return form.valid && !message.customValidity; };
  form.reset = () => { resetCalls++; };
  status.textContent = 'Confirmation assurée par le prestataire après traitement.';
  timeline.nodes = {'.timeline-path': svg};
  timeline.lists = {'.date': dates};
  svg.nodes = {'path': path};
  svg.lists = {'circle': dots};
  dots.forEach(dot => dot.setAttribute('r', '4'));
  function applyGeometry(next) {
    geometry = next;
    const top = 127;
    svg.rect = {top, width: next.width, height: next.height};
    dates.forEach((date, i) => {
      date.rect = {top: top + next.offsets[i], height: next.heights[i]};
    });
  }
  applyGeometry(geometry);
  const nodes = emptyPage ? {} : {'.menu': menu, '#navigation': nav,
    '.lightbox': dialog, '.timeline': timeline, '#contact-form': form, '#form-status': status};
  document.querySelector = selector => nodes[selector] || null;
  document.querySelectorAll = selector => emptyPage ? [] :
    selector === '[data-zoom]' ? [link] : selector === '.reveal' ? [reveal] : [];
  document.body = new Element();
  if (fonts) document.fonts = {ready: Promise.resolve()};
  const context = {document, Image: class {},
    matchMedia: query => ({matches: query.includes('prefers-reduced-motion') && reduced,
      addEventListener: (name, callback) => mediaEvents.set(query + ':' + name, callback)}),
    addEventListener: window.addEventListener.bind(window),
    fetch: () => { fetchCalls++; throw new Error('Unexpected request during native POST'); },
  };
  if (observers) {
    context.ResizeObserver = class {
      constructor(callback) { this.callback = callback; this.targets = []; resizeObservers.push(this); }
      observe(target) { this.targets.push(target); }
    };
    context.IntersectionObserver = class {
      constructor(callback) { this.callback = callback; this.targets = []; intersectionObservers.push(this); }
      observe(target) { this.targets.push(target); }
      unobserve(target) { this.targets = this.targets.filter(item => item !== target); }
      disconnect() { this.targets = []; }
    };
  }
  context.window = context;
  vm.runInNewContext(source, context, {filename: 'script.js'});
  return {menu, nav, document, dialog, stage, close, caption, link, form, message,
    status, timeline, reveal, svg, path, dots, dates, resizeObservers,
    intersectionObservers, mediaEvents, window, applyGeometry,
    get geometry() { return geometry; },
    get fetchCalls() { return fetchCalls; }, get resetCalls() { return resetCalls; },
    get validityReports() { return validityReports; }};
}

function assertGeometry(f) {
  const {width, height, offsets, heights} = f.geometry;
  assert.equal(f.svg.getAttribute('viewBox'), `0 0 ${width} ${height}`);
  const segments = [...f.path.getAttribute('d').matchAll(/([MC])([^MC]+)/g)];
  assert.equal(segments.length, 3, 'Three curve endpoints for three milestones');
  const endpoints = segments.map(([, , values]) => {
    const numbers = values.trim().split(/[ ,]+/).map(Number);
    return numbers.slice(-2);
  });
  f.dots.forEach((dot, i) => {
    const x = Number(dot.getAttribute('cx')), y = Number(dot.getAttribute('cy'));
    assert.equal(x, width / 2, 'Dot centered horizontally in its SVG');
    assert.equal(y, offsets[i] + heights[i] / 2, 'Dot aligned to actual date center');
    assert.deepEqual(endpoints[i], [x, y], 'Dot center is an exact curve endpoint');
    assert.equal(dot.getAttribute('r'), '4', 'Pixel viewBox keeps constant circular radius');
  });
}

async function run() {
  for (const width of [375, 430, 768, 1024, 1440]) {
    const f = fixture(width);
    await Promise.resolve();
    assertGeometry(f);
    assert.equal(f.resizeObservers.length, 1);
    assert.equal(f.resizeObservers[0].targets.length, 4, 'Observe timeline and each date');
    const observer = f.intersectionObservers.find(o => o.targets.includes(f.timeline));
    observer.callback([{target: f.timeline, isIntersecting: true}]);
    assert(f.timeline.classes.has('visible'));
    f.applyGeometry({width: 24, height: 620, offsets: [22, 242, 510], heights: [32, 32, 32]});
    f.resizeObservers[0].callback();
    assertGeometry(f);
    assert(f.timeline.classes.has('visible'), 'Resize does not restart reveal state');
  }
  const f = fixture();
  f.menu.dispatch('click');
  assert.equal(f.menu.getAttribute('aria-expanded'), 'true');
  assert(f.nav.classes.has('open'));
  f.document.dispatch('keydown', {key: 'Escape'});
  assert.equal(f.menu.getAttribute('aria-expanded'), 'false');
  assert(f.menu.focused, 'Escape restores focus to menu control');
  f.menu.dispatch('click');
  f.nav.lists.a[0].dispatch('click');
  assert.equal(f.menu.getAttribute('aria-expanded'), 'false');
  f.menu.dispatch('click');
  f.document.dispatch('click', {target: {closest: () => f.menu}});
  assert.equal(f.menu.getAttribute('aria-expanded'), 'true', 'Header click keeps menu open');
  f.document.dispatch('click', {target: {closest: () => null}});
  assert.equal(f.menu.getAttribute('aria-expanded'), 'false', 'Outside click closes menu');
  f.menu.dispatch('click');
  f.mediaEvents.get('(min-width:851px):change')();
  assert.equal(f.menu.getAttribute('aria-expanded'), 'false', 'Desktop breakpoint closes menu');

  assert(!f.link.dispatch('click', {ctrlKey: true}).defaultPrevented,
    'Modified link navigation preserves native opening');
  assert(!f.dialog.open);
  assert(f.link.dispatch('click').defaultPrevented);
  assert(f.dialog.open);
  assert(f.document.body.classes.has('modal-open'));
  assert.equal(f.stage.children[0].src, f.link.dataset.zoom);
  assert.equal(f.caption.textContent, 'myLEDmask — visuel original');
  f.close.dispatch('click');
  assert(!f.dialog.open);
  assert(!f.document.body.classes.has('modal-open'));
  assert.equal(f.stage.children.length, 0);
  assert(f.link.focused, 'Closing dialog restores opener focus');
  f.link.dispatch('click');
  f.dialog.dispatch('click');
  assert(!f.dialog.open, 'Backdrop click closes dialog');
  const fallback = fixture(375, {modal: false});
  assert(!fallback.link.dispatch('click').defaultPrevented,
    'Missing dialog API preserves original image link');

  const revealObserver = f.intersectionObservers.find(o => o.targets.includes(f.reveal));
  assert(f.reveal.classes.has('reveal-pending'));
  revealObserver.callback([{target: f.reveal, isIntersecting: true}]);
  assert(f.reveal.classes.has('visible'));
  const reduced = fixture(375, {reduced: true});
  assertGeometry(reduced);
  assert.equal(reduced.intersectionObservers.length, 0);
  assert(!reduced.timeline.classes.has('animate-line'));
  assert(!reduced.reveal.classes.has('reveal-pending'));
  const old = fixture(430, {observers: false, fonts: false});
  assertGeometry(old);
  old.applyGeometry(sizes[1024]);
  old.window.dispatch('resize');
  assertGeometry(old);
  assert(!old.reveal.classes.has('reveal-pending'), 'Content visible without IntersectionObserver');
  fixture(1440, {observers: false, fonts: false, emptyPage: true});

  const initialStatus = f.status.textContent;
  assert(!f.form.dispatch('submit').defaultPrevented, 'Configured valid form permits native POST');
  assert.equal(f.status.textContent, initialStatus, 'No invented local delivery confirmation');
  assert.equal(f.fetchCalls, 0, 'No AJAX request');
  assert.equal(f.resetCalls, 0, 'Message preserved before provider handoff');
  f.message.value = ' \n\t ';
  assert(f.form.dispatch('submit').defaultPrevented, 'Whitespace-only message blocked');
  assert(f.message.customValidity);
  f.message.value = 'Message complet.';
  f.message.dispatch('input');
  assert.equal(f.message.customValidity, '', 'Typing valid content clears validation error');
  f.form.valid = false;
  assert(f.form.dispatch('submit').defaultPrevented, 'Other native field errors block submission');
  f.form.valid = true;
  assert(!f.form.dispatch('submit').defaultPrevented);
  f.form.dataset.configured = 'false';
  assert(f.form.dispatch('submit').defaultPrevented, 'Unconfigured form cannot submit');
  assert(f.status.textContent.includes('indisponible'));
  assert.equal(f.fetchCalls, 0);
  assert.equal(f.resetCalls, 0);
  assert(f.validityReports >= 4);
  console.log('PASS: simulated DOM menu/keyboard, dialog/focus/fallback, SVG geometry at five supplied viewport scenarios and resize, reduced motion/missing observers, native form validation and truthful handoff. No browser layout or real email delivery tested.');
}
run().catch(error => { console.error(error); process.exitCode = 1; });
