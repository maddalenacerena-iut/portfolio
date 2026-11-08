const menu=document.querySelector('.menu'),nav=document.querySelector('#navigation');
function closeMenu(){menu?.setAttribute('aria-expanded','false');nav?.classList.remove('open')}
menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open)});
nav?.querySelectorAll('a').forEach(link=>link.addEventListener('click',closeMenu));
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&menu?.getAttribute('aria-expanded')==='true'){closeMenu();menu.focus()}});
document.addEventListener('click',event=>{if(!event.target.closest('.header'))closeMenu()});
matchMedia('(min-width:851px)').addEventListener('change',closeMenu);
const dialog=document.querySelector('.lightbox'),stage=dialog?.querySelector('.zoom-stage');let opener;
document.querySelectorAll('[data-zoom]').forEach(link=>link.addEventListener('click',event=>{if(!dialog?.showModal||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;event.preventDefault();opener=link;const img=new Image();img.src=link.dataset.zoom;img.alt=link.querySelector('img').alt;stage.replaceChildren(img);dialog.querySelector('.zoom-caption').textContent=img.alt;dialog.showModal();document.body.classList.add('modal-open')}));
dialog?.querySelector('.close-lightbox').addEventListener('click',()=>dialog.close());
dialog?.addEventListener('click',event=>{if(event.target===dialog)dialog.close()});
dialog?.addEventListener('close',()=>{document.body.classList.remove('modal-open');stage.replaceChildren();opener?.focus()});
const timeline=document.querySelector('.timeline');
if(timeline){
 const svg=timeline.querySelector('.timeline-path'),path=svg.querySelector('path');
 const dots=[...svg.querySelectorAll('circle')],dates=[...timeline.querySelectorAll('.date')];
 function alignTimeline(){
  const box=svg.getBoundingClientRect(),width=box.width,height=box.height;
  if(!width||!height)return;
  const x=width/2,ys=dates.map(date=>{const rect=date.getBoundingClientRect();return rect.top-box.top+rect.height/2});
  svg.setAttribute('viewBox',`0 0 ${width} ${height}`);
  // Every dot is an endpoint of a cubic segment of this same SVG path.
  // Pixel coordinates preserve circular dots at every responsive width.
  let d=`M${x} ${ys[0]}`;
  for(let i=1;i<ys.length;i++){
   const delta=(ys[i]-ys[i-1])/3,side=i%2?-width/2:width*1.5;
   d+=` C${side} ${ys[i-1]+delta} ${side} ${ys[i]-delta} ${x} ${ys[i]}`;
  }
  path.setAttribute('d',d);
  dots.forEach((dot,i)=>{dot.setAttribute('cx',x);dot.setAttribute('cy',ys[i])});
 }
 alignTimeline();
 if('ResizeObserver'in window){const resize=new ResizeObserver(alignTimeline);resize.observe(timeline);dates.forEach(date=>resize.observe(date))}
 else window.addEventListener('resize',alignTimeline);
 document.fonts?.ready.then(alignTimeline);
 if('IntersectionObserver'in window&&!matchMedia('(prefers-reduced-motion:reduce)').matches){timeline.classList.add('animate-line');const observer=new IntersectionObserver(entries=>{if(entries.some(entry=>entry.isIntersecting)){timeline.classList.add('visible');observer.disconnect()}},{threshold:.2});observer.observe(timeline)}
}

const reduced=matchMedia('(prefers-reduced-motion:reduce)').matches;
if('IntersectionObserver' in window&&!reduced){
 const reveal=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');reveal.unobserve(entry.target)}}),{threshold:.08});
 document.querySelectorAll('.reveal').forEach(el=>{el.classList.add('reveal-pending');reveal.observe(el)});
}
const form=document.querySelector('#contact-form');
if(form){
 const message=form.querySelector('#message');
 const validateMessage=()=>message.setCustomValidity(message.value.trim()?'':'Indiquez votre message.');
 message.addEventListener('input',validateMessage);
 form.addEventListener('submit',event=>{
  const status=document.querySelector('#form-status');
  if(form.dataset.configured!=='true'){
   event.preventDefault();status.textContent='L’envoi est indisponible. Contactez-moi directement par email.';return;
  }
  validateMessage();
  if(!form.reportValidity()){event.preventDefault();return}
  // Keep native POST: the provider handles CAPTCHA, activation, errors and
  // confirmation. No local success is inferred from a redirect or HTTP 200.
 });
}
