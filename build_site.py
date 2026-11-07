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
a{color:var(--ac)}nav{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:.92rem}.note{color:var(--mut);font-size:.9rem}footer{margin-top:40px;color:var(--mut);font-size:.85rem}"""

BASE = "https://jamesdin94-sketch.github.io/calc/"
DOCS = {}
PAGES = {}
FMT = "const f=n=>Math.round(n).toLocaleString('ko-KR');"


def page(slug, title, desc, body, script, faq):
    faqs = "".join(f"<h2>{html.escape(q)}</h2><p>{html.escape(a)}</p>" for q, a in faq)
    doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{BASE}{slug}.html"><style>{CSS}</style></head><body><main>@@NAV@@
<h1>{html.escape(title)}</h1><p class="note">{html.escape(desc)}</p>{body}{faqs}
<footer>입력한 값은 이 기기 안에서만 계산되며 서버로 전송되지 않습니다. 결과는 참고용이며 법적·금융 효력이 없습니다.</footer></main><script>{script}</script></body></html>"""
    DOCS[slug] = doc
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

TODAY = "const td=new Date(),tds=td.getFullYear()+'-'+String(td.getMonth()+1).padStart(2,'0')+'-'+String(td.getDate()).padStart(2,'0');"

page("vat", "부가세 계산기 (공급가액·합계금액)", "공급가액에서 부가세 10%를 더하거나, 합계금액에서 공급가액과 부가세를 나눕니다.",
     """<div class="card"><label>금액 (원)</label><input id="a" type="number" value="110000"><label>입력한 금액은</label><select id="m"><option value="t">합계금액(부가세 포함)</option><option value="s">공급가액(부가세 별도)</option></select>
<button onclick="go()">계산하기</button><div class="res" id="o"></div></div>""",
     FMT + """function go(){const A=+a.value;let sup,vat,tot;if(m.value==='t'){tot=A;sup=Math.round(A/1.1);vat=tot-sup}else{sup=A;vat=Math.round(A*0.1);tot=sup+vat}
o.innerHTML='공급가액 <b>'+f(sup)+'원</b><br>부가세(10%) <b>'+f(vat)+'원</b><br>합계금액 <b>'+f(tot)+'원</b>'}go()""",
     [("부가세율은 얼마인가요?", "일반과세자의 부가가치세율은 10%입니다. 면세 품목이나 영세율 거래는 다릅니다."),
      ("간이과세자도 같은가요?", "간이과세자는 업종별 부가율을 적용해 납부세액이 달라집니다. 이 계산기는 거래 금액의 10% 기준입니다.")])

page("rent", "전월세 전환 계산기", "전세를 월세로, 월세를 전세로 바꿀 때 금액을 계산합니다. 전환율은 직접 입력합니다.",
     """<div class="card"><b>전세 → 월세</b><label>전세금 (원)</label><input id="j" type="number" value="300000000"><label>월세로 바꿀 때 남길 보증금 (원)</label><input id="d" type="number" value="50000000">
<label>전월세 전환율 (연 %)</label><input id="r" type="number" step="0.01" value="5"><button onclick="go1()">월세 계산</button><div class="res" id="o1"></div></div>
<div class="card"><b>월세 → 전세</b><label>보증금 (원)</label><input id="d2" type="number" value="50000000"><label>월세 (원)</label><input id="w2" type="number" value="1000000">
<label>전월세 전환율 (연 %)</label><input id="r2" type="number" step="0.01" value="5"><button onclick="go2()">전세 환산</button><div class="res" id="o2"></div></div>""",
     FMT + """function go1(){const m=(+j.value-+d.value)*(+r.value/100)/12;o1.innerHTML='월세 <b>'+f(m)+'원</b>'}
function go2(){const R=+r2.value/100;o2.innerHTML=R?'전세 환산액 <b>'+f(+d2.value+ +w2.value*12/R)+'원</b>':'전환율을 입력하세요'}go1();go2()""",
     [("전월세 전환율은 어떻게 정해지나요?", "주택임대차보호법 시행령은 한국은행 기준금리에 일정 비율을 더한 값을 상한으로 정합니다. 현재 적용되는 값은 법제처 국가법령정보센터에서 확인하세요."),
      ("계산식은 무엇인가요?", "월세 = (전세금 − 보증금) × 전환율 ÷ 12 입니다. 반대로 전세 환산액 = 보증금 + 월세 × 12 ÷ 전환율 입니다.")])

page("pyeong", "평수 ㎡ 변환 계산기", "평을 제곱미터(㎡)로, 제곱미터를 평으로 바꿉니다.",
     """<div class="card"><label>평</label><input id="py" type="number" step="0.01" value="25"><button onclick="a()">㎡로 변환</button><div class="res" id="o1"></div></div>
<div class="card"><label>제곱미터 (㎡)</label><input id="m2" type="number" step="0.01" value="84"><button onclick="b()">평으로 변환</button><div class="res" id="o2"></div></div>""",
     """const K=400/121;function a(){o1.innerHTML=(+py.value)+'평 = <b>'+(py.value*K).toFixed(2)+'㎡</b>'}function b(){o2.innerHTML=(+m2.value)+'㎡ = <b>'+(m2.value/K).toFixed(2)+'평</b>'}a();b()""",
     [("1평은 몇 ㎡인가요?", "1평은 약 3.3058㎡입니다(400/121㎡)."),
      ("아파트 84㎡는 몇 평인가요?", "약 25.4평입니다. 다만 분양 면적과 전용 면적은 다르므로 어느 면적인지 확인해야 합니다."),
      ("평을 광고에 써도 되나요?", "계량법상 거래 증명에는 ㎡ 사용이 원칙입니다. 평은 참고용으로만 쓰세요.")])

page("age", "만 나이 계산기", "생년월일로 만 나이, 연 나이, 세는나이와 태어난 지 며칠인지 계산합니다.",
     """<div class="card"><label>생년월일</label><input id="b" type="date" value="1990-01-01"><label>기준일</label><input id="r" type="date"><button onclick="go()">계산하기</button><div class="res" id="o"></div></div>""",
     TODAY + """r.value=tds;function go(){const B=b.value.split('-').map(Number),R=r.value.split('-').map(Number);let y=R[0]-B[0];if(R[1]<B[1]||(R[1]===B[1]&&R[2]<B[2]))y--;
const days=Math.round((Date.UTC(R[0],R[1]-1,R[2])-Date.UTC(B[0],B[1]-1,B[2]))/864e5);
o.innerHTML='만 나이 <b>'+y+'세</b><br>연 나이 '+(R[0]-B[0])+'세 · 세는나이 '+(R[0]-B[0]+1)+'세<br>태어난 지 <b>'+days.toLocaleString('ko-KR')+'일</b>'}go()""",
     [("만 나이는 어떻게 계산하나요?", "기준일의 연도에서 태어난 연도를 빼고, 올해 생일이 아직 지나지 않았으면 1을 뺍니다. 2023년 6월부터 법적·사회적 나이는 만 나이로 통일되었습니다."),
      ("연 나이는 무엇인가요?", "기준 연도에서 출생 연도를 뺀 나이입니다. 병역·청소년 보호 등 일부 법령에서 쓰입니다.")])

page("dday", "날짜 계산기 (D-day·며칠 후)", "두 날짜 사이의 일수를 구하거나, 어떤 날로부터 N일 뒤가 언제인지 계산합니다.",
     """<div class="card"><b>두 날짜 사이</b><label>시작일</label><input id="a" type="date"><label>종료일</label><input id="b" type="date"><button onclick="go1()">일수 계산</button><div class="res" id="o1"></div></div>
<div class="card"><b>N일 후·전 날짜</b><label>기준일</label><input id="c" type="date"><label>일수 (뒤는 +, 앞은 −)</label><input id="n" type="number" value="100"><button onclick="go2()">날짜 계산</button><div class="res" id="o2"></div></div>""",
     TODAY + """a.value=tds;c.value=tds;const t2=new Date(td.getTime()+100*864e5);b.value=t2.getFullYear()+'-'+String(t2.getMonth()+1).padStart(2,'0')+'-'+String(t2.getDate()).padStart(2,'0');
const U=v=>{const x=v.split('-').map(Number);return Date.UTC(x[0],x[1]-1,x[2])};const DN=['일','월','화','수','목','금','토'];
function go1(){const d=Math.round((U(b.value)-U(a.value))/864e5);o1.innerHTML='<b>'+Math.abs(d)+'일</b> ('+(d>=0?'종료일이 이후':'종료일이 이전')+') · 약 '+(Math.abs(d)/7).toFixed(1)+'주<br><span class="note">시작일 당일을 포함하면 '+(Math.abs(d)+1)+'일입니다.</span>'}
function go2(){const t=new Date(U(c.value)+ +n.value*864e5);o2.innerHTML='<b>'+t.getUTCFullYear()+'년 '+(t.getUTCMonth()+1)+'월 '+t.getUTCDate()+'일 ('+DN[t.getUTCDay()]+')</b>'}go1();go2()""",
     [("100일은 어떻게 세나요?", "관례적으로 기준일을 1일째로 세면 99일 후가 100일째입니다. 이 계산기는 기준일 다음 날을 1일로 셉니다. 기념일은 그에 맞춰 입력하세요."),
      ("기준일을 포함해서 세려면?", "일수 계산 결과에 1을 더하면 됩니다. 결과 아래에 포함한 일수도 함께 표시합니다.")])

page("bmi", "BMI 계산기 (체질량지수)", "키와 몸무게로 체질량지수(BMI)와 대한비만학회 기준 구간을 확인합니다.",
     """<div class="card"><label>키 (cm)</label><input id="h" type="number" step="0.1" value="170"><label>몸무게 (kg)</label><input id="w" type="number" step="0.1" value="65"><button onclick="go()">계산하기</button><div class="res" id="o"></div></div>""",
     """function go(){const H=+h.value/100,B=+w.value/(H*H);const g=B<18.5?'저체중':B<23?'정상':B<25?'비만 전단계(과체중)':B<30?'1단계 비만':B<35?'2단계 비만':'3단계 비만';
o.innerHTML='BMI <b>'+B.toFixed(1)+'</b> · '+g+'<br><span class="note">정상 체중 범위: '+(18.5*H*H).toFixed(1)+'~'+(22.9*H*H).toFixed(1)+'kg</span>'}go()""",
     [("BMI 기준은 무엇인가요?", "대한비만학회는 아시아 기준으로 18.5 미만 저체중, 18.5~22.9 정상, 23~24.9 비만 전단계, 25 이상 비만으로 봅니다."),
      ("BMI만으로 건강을 판단할 수 있나요?", "근육량·체지방·나이를 반영하지 못하는 단순 지표입니다. 건강 판단은 의료진 상담이 필요하며 이 결과는 의학적 조언이 아닙니다.")])

NAV = '<nav><a href="index.html">목록</a>' + "".join(f'<a href="{sl}.html">{html.escape(t.split(" (")[0])}</a>' for sl, (t, d) in PAGES.items()) + "</nav>"
for sl, doc in DOCS.items():
    (OUT / f"{sl}.html").write_text(doc.replace("@@NAV@@", NAV), encoding="utf-8")
cards = "".join(f'<div class="card"><a href="{s}.html"><b>{html.escape(t)}</b></a><div class="note">{html.escape(d)}</div></div>' for s, (t, d) in PAGES.items())
(OUT / "index.html").write_text(f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>생활 계산기 모음</title>
<meta name="description" content="대출 이자, 적금, 퇴직금, 시급, 부가세, 전월세 전환, 평수, 만 나이, 날짜, BMI 등 무료 계산기 모음"><link rel="canonical" href="{BASE}"><style>{CSS}</style></head><body><main>{NAV}<h1>생활 계산기 모음</h1>
<p class="note">회원가입 없이 바로 쓰는 무료 계산기. 입력한 값은 기기 밖으로 나가지 않습니다.</p>{cards}</main></body></html>""", encoding="utf-8")
urls = [BASE] + [f"{BASE}{sl}.html" for sl in PAGES]
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
print("pages", len(PAGES))
