# -*- coding: utf-8 -*-
"""한국어 무료 계산기 사이트(정적 HTML). 순수 계산만 하며 입력 값은 서버로 보내지 않는다."""
import html
import pathlib

OUT = pathlib.Path(__file__).parent / "docs"
OUT.mkdir(exist_ok=True)

CSS = """:root{--bg:#fff;--fg:#1c2230;--mut:#5b6475;--card:#f4f6fa;--ac:#1a56db;--bd:#d9dee8}
@media(prefers-color-scheme:dark){:root{--bg:#12151c;--fg:#e8ebf2;--mut:#a3adc2;--card:#1b2030;--ac:#7ba5ff;--bd:#2c3347}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.7 -apple-system,'Malgun Gothic',sans-serif}
main{max-width:720px;margin:0 auto;padding:20px 16px 60px}h1{font-size:1.5rem;margin:.4em 0}h2{font-size:1.15rem;margin-top:2em}
.card{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:16px;margin:14px 0}
label{display:block;margin:.6em 0 .2em;font-weight:600}input,select{width:100%;padding:10px;border:1px solid var(--bd);border-radius:8px;background:var(--bg);color:var(--fg);font-size:16px}
button{margin-top:14px;padding:12px 18px;border:0;border-radius:8px;background:var(--ac);color:#fff;font-size:16px;font-weight:700;cursor:pointer}
.res{font-size:1.1rem;margin-top:14px}.res b{color:var(--ac)}table{width:100%;border-collapse:collapse;font-size:.92rem}td,th{border-bottom:1px solid var(--bd);padding:6px;text-align:right}
a{color:var(--ac)}nav a{margin-right:14px}.note{color:var(--mut);font-size:.9rem}footer{margin-top:40px;color:var(--mut);font-size:.85rem}"""

NAV = '<nav><a href="index.html">계산기 목록</a><a href="loan.html">대출 이자</a><a href="savings.html">적금·복리</a><a href="severance.html">퇴직금</a><a href="hourly.html">시급 월급 환산</a><a href="lotto.html">로또 확률</a></nav>'
PAGES = {}
FMT = "const f=n=>Math.round(n).toLocaleString('ko-KR');"


def page(slug, title, desc, body, script, faq):
    faqs = "".join(f"<h2>{html.escape(q)}</h2><p>{html.escape(a)}</p>" for q, a in faq)
    doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><style>{CSS}</style></head><body><main>{NAV}
<h1>{html.escape(title)}</h1><p class="note">{html.escape(desc)}</p>{body}{faqs}
<footer>입력한 값은 이 기기 안에서만 계산되며 서버로 전송되지 않습니다. 결과는 참고용이며 법적·금융 효력이 없습니다.</footer></main><script>{script}</script></body></html>"""
    (OUT / f"{slug}.html").write_text(doc, encoding="utf-8")
    PAGES[slug] = (title, desc)


page("loan", "대출 이자 계산기 (원리금균등·원금균등)", "대출 금액, 연 이자율, 기간을 넣으면 월 상환액과 총 이자를 계산합니다.",
     """<div class="card"><label>대출 금액 (원)</label><input id="p" type="number" value="100000000"><label>연 이자율 (%)</label><input id="r" type="number" step="0.01" value="4.5">
<label>기간 (개월)</label><input id="n" type="number" value="360"><label>상환 방식</label><select id="m"><option value="eq">원리금균등</option><option value="pr">원금균등</option></select>
<button onclick="go()">계산하기</button><div class="res" id="o"></div></div>""",
     FMT + """function go(){const P=+p.value,R=+r.value/1200,N=+n.value;let t=0,first,last;
if(m.value==='eq'){const pay=R?P*R*Math.pow(1+R,N)/(Math.pow(1+R,N)-1):P/N;t=pay*N;first=last=pay}
else{const pr=P/N;for(let i=0;i<N;i++){const pay=pr+(P-pr*i)*R;t+=pay;if(i==0)first=pay;last=pay}}
o.innerHTML='첫 달 상환액 <b>'+f(first)+'원</b>'+(m.value==='pr'?' → 마지막 달 <b>'+f(last)+'원</b>':'')+'<br>총 상환액 <b>'+f(t)+'원</b><br>총 이자 <b>'+f(t-P)+'원</b>'}go()""",
     [("원리금균등과 원금균등은 무엇이 다른가요?", "원리금균등은 매달 갚는 금액이 같고, 원금균등은 원금을 같은 금액씩 갚아 초기 부담이 크지만 총 이자가 적습니다."),
      ("중도상환수수료는 포함되나요?", "포함되지 않습니다. 은행 상품 약관을 따로 확인하세요.")])

page("savings", "적금·복리 계산기", "월 납입액과 연 이율, 기간으로 만기 금액과 이자를 계산합니다.",
     """<div class="card"><label>월 납입액 (원)</label><input id="a" type="number" value="500000"><label>연 이율 (%)</label><input id="r" type="number" step="0.01" value="3.5">
<label>기간 (개월)</label><input id="n" type="number" value="36"><label>이자 방식</label><select id="m"><option value="s">단리 (일반 적금)</option><option value="c">월복리</option></select>
<button onclick="go()">계산하기</button><div class="res" id="o"></div></div>""",
     FMT + """function go(){const A=+a.value,R=+r.value/100,N=+n.value;let fv,pr=A*N;
if(m.value==='s'){fv=pr+A*R/12*N*(N+1)/2}else{const i=R/12;fv=i?A*((Math.pow(1+i,N)-1)/i)*(1+i):pr}
o.innerHTML='원금 <b>'+f(pr)+'원</b><br>세전 이자 <b>'+f(fv-pr)+'원</b><br>세전 만기 금액 <b>'+f(fv)+'원</b><br><span class="note">일반 이자소득세 15.4%를 빼면 세후 이자는 약 '+f((fv-pr)*0.846)+'원입니다.</span>'}go()""",
     [("단리와 복리는 어떻게 다른가요?", "단리는 원금에만 이자가 붙고, 복리는 이자에도 이자가 붙습니다. 일반 적금은 단리가 많습니다."),
      ("세금은 얼마인가요?", "일반 과세 이자소득세는 15.4%(소득세 14% + 지방소득세 1.4%)입니다. 비과세·세금우대 상품은 다를 수 있습니다.")])

page("severance", "퇴직금 계산기", "입사일, 퇴사일, 최근 3개월 급여로 법정 퇴직금을 계산합니다.",
     """<div class="card"><label>입사일</label><input id="s" type="date" value="2021-03-01"><label>퇴사일</label><input id="e" type="date" value="2026-03-01">
<label>퇴직 전 3개월 급여 합계 (세전, 원)</label><input id="w" type="number" value="9000000"><label>연간 상여금 (원)</label><input id="b" type="number" value="0"><label>연차수당 (원, 지급액)</label><input id="v" type="number" value="0">
<button onclick="go()">계산하기</button><div class="res" id="o"></div></div>""",
     FMT + """function go(){const S=new Date(s.value),E=new Date(e.value);const days=Math.round((E-S)/864e5)+1;
const q=new Date(E);q.setMonth(q.getMonth()-3);const d3=Math.round((E-q)/864e5)+1;
const avg=(+w.value+ +b.value*3/12+ +v.value*3/12)/d3;const sev=avg*30*days/365;
o.innerHTML='재직일수 <b>'+days+'일</b> ('+(days/365).toFixed(2)+'년)<br>1일 평균임금 <b>'+f(avg)+'원</b><br>예상 퇴직금 <b>'+f(days>=365?sev:0)+'원</b>'+(days<365?'<br><span class="note">재직 1년 미만이면 법정 퇴직금 대상이 아닙니다.</span>':'')}go()""",
     [("퇴직금 계산식은 무엇인가요?", "1일 평균임금 × 30일 × (재직일수 ÷ 365)입니다. 평균임금은 퇴직 전 3개월 임금 총액을 그 기간의 일수로 나눈 값에 상여금·연차수당의 3/12을 더해 계산합니다."),
      ("정확한 금액은 어디서 확인하나요?", "회사의 급여 기준과 근로계약에 따라 달라질 수 있습니다. 정확한 금액은 고용노동부 퇴직금 계산기나 노무 상담으로 확인하세요.")])

page("hourly", "시급 월급 환산 계산기 (주휴수당 포함)", "시급과 주 근무시간을 넣으면 주휴수당을 포함한 월 환산 급여를 계산합니다.",
     """<div class="card"><label>시급 (원)</label><input id="h" type="number" value="10320"><label>주 근무시간 (시간)</label><input id="t" type="number" step="0.5" value="40">
<button onclick="go()">계산하기</button><div class="res" id="o"></div></div>""",
     FMT + """function go(){const H=+h.value,T=+t.value;const hol=T>=15?Math.min(T,40)/40*8:0;const wk=(T+hol)*H;const mo=wk*365/7/12;
o.innerHTML='주휴수당 포함 주급 <b>'+f(wk)+'원</b><br>월 환산 급여 <b>'+f(mo)+'원</b> (월 환산 시간 '+((T+hol)*365/7/12).toFixed(1)+'시간)<br><span class="note">주 15시간 미만이면 주휴수당이 없습니다. 세전 금액입니다.</span>'}go()""",
     [("주휴수당 조건은 무엇인가요?", "주 15시간 이상 일하고 소정근로일을 개근하면 하루 치 임금을 더 받습니다. 이 계산기는 개근을 가정합니다."),
      ("시급은 어디에서 확인하나요?", "해당 연도 최저임금은 최저임금위원회에서 확인하세요. 입력란의 기본값은 예시입니다.")])

page("lotto", "로또 확률 계산기", "로또 6/45에서 몇 개를 맞힐 확률과 몇 장을 사면 어떻게 되는지 계산합니다.",
     """<div class="card"><label>구매 장수</label><input id="k" type="number" value="5"><button onclick="go()">계산하기</button><div class="res" id="o"></div></div>
<div class="card"><table><tr><th>등수</th><th>조건</th><th>한 장 확률</th></tr><tr><td>1등</td><td>6개 일치</td><td>1/8,145,060</td></tr><tr><td>2등</td><td>5개 + 보너스</td><td>1/1,357,510</td></tr><tr><td>3등</td><td>5개</td><td>1/35,724</td></tr><tr><td>4등</td><td>4개</td><td>1/733</td></tr><tr><td>5등</td><td>3개</td><td>1/45</td></tr></table></div>""",
     FMT + """function go(){const K=+k.value,p1=1/8145060;const any=1/45+1/733+1/35724+1/1357510+p1;
o.innerHTML=K+'장(<b>'+f(K*1000)+'원</b>)을 사면<br>1등 확률 <b>1/'+f(1/(K*p1))+'</b><br>5등 이상 한 번이라도 당첨될 확률 <b>'+((1-Math.pow(1-any,K))*100).toFixed(1)+'%</b><br><span class="note">로또는 기대 수익이 구매금보다 낮습니다. 오락으로만 즐기세요. 도박 상담 1336</span>'}go()""",
     [("번호를 고르는 방법으로 확률을 높일 수 있나요?", "모든 번호 조합의 1등 확률은 같습니다. 어떤 분석 방법도 확률을 높이지 못합니다."),
      ("몇 장을 사면 1등이 되나요?", "1등 확률은 장수에 비례해 늘어나지만 1천 장을 사도 약 0.012%입니다.")])

cards = "".join(f'<div class="card"><a href="{s}.html"><b>{html.escape(t)}</b></a><div class="note">{html.escape(d)}</div></div>' for s, (t, d) in PAGES.items())
(OUT / "index.html").write_text(f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>생활 계산기 모음</title>
<meta name="description" content="대출 이자, 적금, 퇴직금, 시급 월급 환산, 로또 확률을 계산하는 무료 계산기 모음"><style>{CSS}</style></head><body><main>{NAV}<h1>생활 계산기 모음</h1>
<p class="note">회원가입 없이 바로 쓰는 무료 계산기. 입력한 값은 기기 밖으로 나가지 않습니다.</p>{cards}</main></body></html>""", encoding="utf-8")
(OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
print("pages", len(PAGES))
