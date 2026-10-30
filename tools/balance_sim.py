# 자동 플레이 밸런스 비교: python3 tools/balance_sim.py /abs/path/old.html /abs/path/index.html
# 스테이지별 4판 평균 (처치 수, 적이 죽는 평균 높이, 판 끝 레벨, 능력 수, 피격, 정예기/보스 처치 시간)
import sys
from playwright.sync_api import sync_playwright
SIM="""(n)=>{const PR=['lightning','blast','ricochet','spread','laser','focus','overcharge','rapid','wing','drone'];const R={k:0,y:0,ky:0,lv:0,h:0,el:0,ab:0};const runs=4;const ok=kill;window.__ys=[];kill=function(e){if(!e.dead&&!isBig(e)&&e.type!=='part')__ys.push(e.y);return ok.apply(this,arguments)};
 for(let r=0;r<runs;r++){__ys=[];progress.cleared=[];for(let k=1;k<n;k++)progress.cleared.push(k);hangar();start(n);let guard=0,bt=null;
 while(state!=='won'&&state!=='over'&&state!=='victory'&&guard<12000){guard++;if(state==='upgrade'){const c=[...offeredChoices].sort((a,b)=>(PR.indexOf(a)<0?99:PR.indexOf(a))-(PR.indexOf(b)<0?99:PR.indexOf(b)));chooseUpgrade(c[0]);continue}if(state==='playing'&&graze>=100)reverse();
  const big=enemies.find(e=>isBig(e)&&!e.dead),tgt=big||enemies.filter(e=>!e.dead&&e.y>0).sort((a,b)=>b.y-a.y)[0];if(tgt)player.x+=Math.max(-3,Math.min(3,tgt.x-player.x));
  update(1/30);if(player.hp<3){R.h+=3-player.hp;if(state==='over'){settled=false;state='playing'}player.hp=3}if(bt===null&&big)bt=t}
 R.k+=kills;R.ky+=__ys.length?__ys.reduce((a,b)=>a+b,0)/__ys.length:0;R.lv+=level;R.el+=t-(bt??t);R.ab+=Object.values(ranks).reduce((a,b)=>a+b,0)}
 kill=ok;const f=x=>(x/runs).toFixed(0);return `kills ${f(R.k)} killY ${f(R.ky)} lv ${f(R.lv)} abil ${f(R.ab)} hits ${f(R.h)} bigTTK ${f(R.el)}s`}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for f in sys.argv[1:]:
        pg=b.new_page(viewport={'width':390,'height':844});pg.goto('file://'+f);pg.evaluate("localStorage.clear()");pg.reload();pg.wait_for_timeout(300);pg.evaluate("()=>{state='hangar'}")
        for n in (3,8,13,18,23):print(f.split('/')[-1][:6],n,pg.evaluate(SIM,n))
    b.close()
