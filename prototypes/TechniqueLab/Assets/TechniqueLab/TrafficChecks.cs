using System.Collections.Generic;
using UnityEngine;
namespace TechniqueLab
{
    public static class TrafficChecks
    {
        public static List<CheckResult> Run()
        {
            var rows=new List<CheckResult>();
            void Add(string name,bool pass,string detail){rows.Add(new CheckResult{name=name,passed=pass,detail=detail});}
            Add("traffic.narrow-small",TrafficGeometry.FitsNarrow(.2f)&&TrafficGeometry.FitsNarrow(.35f),"small profiles fit one-unit opening with margin");
            Add("traffic.narrow-large",!TrafficGeometry.FitsNarrow(.6f),"large disc must choose wide corridor");
            Add("traffic.clearance-boundary",TrafficGeometry.FitsNarrow(.46f)&&!TrafficGeometry.FitsNarrow(.47f),"0.04 margin is part of feasibility");
            Add("traffic.audit-radius-sum",TrafficGeometry.PairGap(Vector2.zero,Vector2.zero,.6f,new Vector2(.7f,0),new Vector2(.7f,0),.35f)<0,"fixed .4 diameter must not miss unequal-radius overlap");
            Add("traffic.audit-swept-swap",TrafficGeometry.PairGap(Vector2.left,Vector2.right,.2f,Vector2.right,Vector2.left,.35f)<0,"separated endpoints do not excuse crossing trajectories");
            var gate=new TrafficGate(16);for(int i=0;i<16;i++)gate.Request(i,i<8?1:-1);gate.Resolve();
            bool mixed=false;int dir=0;for(int i=0;i<16;i++)if(gate.leased[i]){if(dir!=0&&dir!=gate.directions[i])mixed=true;dir=gate.directions[i];}
            Add("traffic.gate-exclusion",!mixed&&gate.active>0,"opposite leases must not coexist");
            Add("traffic.gate-batch",gate.active<=4,"opposite pending caps same-phase admissions at four");
            for(int i=0;i<8;i++)if(gate.leased[i])gate.Release(i);gate.Resolve();
            Add("traffic.gate-fair-turn",gate.leased[8]&&!gate.leased[4],"opposite oldest queue gets next turn");
            var paused=new TrafficGate(2);paused.Request(0,1);paused.paused=true;paused.Resolve();
            Add("traffic.gate-pause",paused.active==0,"admission pause does not grant a new lease");
            paused.paused=false;paused.Resolve();Add("traffic.gate-resume",paused.leased[0],"resume preserves pending ticket");
            var waiting=TrafficWorld.Pair(false);waiting.gate.paused=true;
            for(int t=0;t<60;t++)waiting.Step(1f/60);
            Add("traffic.wait-clock",Mathf.Abs(waiting.agents[0].waited-1)<.0001f,"one simulated second of pause is one second of waiting");
            bool partition=true;string partitionDetail="all slots initialized for smallest allowed population";
            try{TrafficWorld.Dense(8,true);}catch(System.Exception e){partition=false;partitionDetail=e.GetType().Name;}
            Add("traffic.population-partition",partition,partitionDetail);
            var reversed=TrafficWorld.Dense(16,true,true);reversed.Step(1f/60);
            Add("traffic.reverse-arrival",reversed.gate.phase==-1,"reversed eligible arrival order lets westbound ticket enter first");
            var redirected=TrafficWorld.Pair(false,largeProbe:true);
            Add("traffic.profile-redirect",redirected.redirected==1&&!redirected.agents[0].narrow,"radius-specific shared field rejects large requested narrow route");
            var safe=TrafficWorld.Pair(false);for(int t=0;t<7200&&safe.arrived<2;t++)safe.Step(1f/60);
            Add("traffic.headon-completes",safe.arrived==2&&safe.narrowOpposingTicks==0&&safe.maxStallSeconds<5,"both narrow directions finish without a wait cycle");
            var wide=TrafficWorld.Pair(true);for(int t=0;t<7200&&wide.arrived<2;t++)wide.Step(1f/60);
            Add("traffic.wide-simultaneous",wide.arrived==2&&wide.wideOpposingTicks>0,"opposite unequal discs actually pass simultaneously in the wide region");
            var deadlock=TrafficWorld.Pair(false,false,true);for(int t=0;t<1200&&deadlock.stallSeconds<5;t++)deadlock.Step(1f/60);
            Add("traffic.deadlock-control",deadlock.stallSeconds>=5&&deadlock.arrived<2,"pair safety alone must expose a head-on wait cycle without admission control");
            var hashed=TrafficWorld.Dense(64,true);var brute=TrafficWorld.Dense(64,true);brute.bruteNeighbors=true;
            for(int t=0;t<240;t++){hashed.Step(1f/60);brute.Step(1f/60);}
            bool same=true;for(int i=0;i<64;i++)same&=(hashed.agents[i].position-brute.agents[i].position).sqrMagnitude<.00000001;
            Add("traffic.hash-reference",same,"bounded neighbor search matches exhaustive pair checking over crossing/queue steps");
            var smallProfile=new TrafficProfile(.35f);var largeProfile=new TrafficProfile(.6f);
            Add("traffic.two-goal-profiles",smallProfile.SelectNarrow(1,true)&&smallProfile.SelectNarrow(-1,true)&&!largeProfile.SelectNarrow(1,true)&&!largeProfile.SelectNarrow(-1,true),"radius compatibility applies to both reverse fields, not one goal only");
            var overlap=TrafficWorld.Pair(true);overlap.agents[0].position=new Vector2(61,23);overlap.agents[1].position=new Vector2(61.7f,23);
            var unequalAudit=new TrafficAudit(overlap);unequalAudit.Observe(overlap,1f/60);
            Add("traffic.independent-audit-radii",unequalAudit.pairPenetrations>0,"independent auditor detects .6+.2 overlap that fixed .4 misses");
            var terminal=TrafficWorld.Pair(true);terminal.agents[0].position=new Vector2(61,23);terminal.agents[1].position=new Vector2(62.1f,23);
            var terminalAudit=new TrafficAudit(terminal);terminal.agents[0].position=new Vector2(61.4f,23);terminal.agents[0].arrived=true;terminalAudit.Observe(terminal,.2f);
            Add("traffic.independent-audit-terminal",terminalAudit.pairPenetrations>0,"terminal movement remains observed after arrival removal");
            return rows;
        }
    }
}
