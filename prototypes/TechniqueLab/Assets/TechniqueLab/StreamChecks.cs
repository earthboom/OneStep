using System.Collections.Generic;
using UnityEngine;
namespace TechniqueLab
{
    public static class StreamChecks
    {
        public static List<CheckResult> Run()
        {
            var rows=new List<CheckResult>();
            void Add(string name,bool pass,string detail){rows.Add(new CheckResult{name=name,passed=pass,detail=detail});}
            Add("stream.swept-swap",StreamKernel.Gap(Vector2.zero,Vector2.right*1.5f,.6f,Vector2.right*1.5f,Vector2.zero,.35f)<0,"opposite edge traversal collides between endpoints");
            Add("stream.corner-large",StreamKernel.Gap(Vector2.zero,Vector2.right*1.5f,.6f,Vector2.right*1.5f,Vector2.one*1.5f,.6f)<0,"following around a corner can collide without vertex conflicts");
            Add("stream.corner-small",StreamKernel.Gap(Vector2.zero,Vector2.right*1.5f,.2f,Vector2.right*1.5f,Vector2.one*1.5f,.2f)>.04,"small following pair has adequate swept clearance");
            Add("stream.pending-age",StreamKernel.Overdue(501,0,480),"pending requests count toward response deadline even before spawn");
            Add("stream.deadline-boundary",!StreamKernel.Overdue(480,0,480),"deadline comparison does not invent an earlier miss");
            var map=new StreamMap(0);var planner=new StreamPlanner(map);
            Add("stream.static-map",map.blocked[10+12*32]&&!map.blocked[1+12*32],"baffles obstruct direct crossing without directional lane data");
            int[] path=planner.Plan(1+12*32,30+12*32,.6f);
            bool legal=path!=null&&path.Length>30;
            if(path!=null)for(int i=1;i<path.Length;i++)legal&=!map.blocked[path[i]]&&(Mathf.Abs(path[i]%32-path[i-1]%32)+Mathf.Abs(path[i]/32-path[i-1]/32)<=1);
            Add("stream.unlaned-search",legal,"search discovers a cardinal detour around baffles");
            Add("stream.unreachable",planner.Plan(1+12*32,10+12*32,.6f)==null,"blocked target produces explicit no route");
            var reservations=new StreamReservations(map);reservations.Add(new[]{5+5*32,6+5*32},0,.6f);
            Add("stream.edge-reservation",!reservations.Safe(0,6+5*32,5+5*32,.35f),"new route cannot swap with an existing edge");
            bool coverage=true;var random=new System.Random(914);reservations.Clear();
            for(int i=0;i<100;i++){int u=random.Next(1,31)+random.Next(1,23)*32,v=map.Neighbor(u,random.Next(4));reservations.Add(new[]{u,v},0,i%2==0?.6f:.2f);}
            for(int i=0;i<2000;i++){int u=random.Next(1,31)+random.Next(1,23)*32,v=map.Neighbor(u,random.Next(5));float radius=i%2==0?.6f:.35f;coverage&=reservations.Safe(0,u,v,radius)==reservations.Safe(0,u,v,radius,true);}
            Add("stream.index-exhaustive",coverage,"2000 deterministic candidate edges agree with exhaustive radius-aware reservation checks");
            var world=new StreamWorld(0,2,20);world.Begin();
            for(int t=0;t<400;t++){world.Finish();world.Begin();}
            Add("stream.fifo-drain",world.jobs.Count==40&&world.completed==40&&world.pending.Count==0&&world.active.Count==0,"all generated IDs finish after sustained FIFO inflow stops");
            bool fifo=true,bounded=true;int previous=-1;foreach(var j in world.jobs){fifo&=j.admitted>=previous;previous=j.admitted;bounded&=j.routeActions<=96&&j.routeActions>0;}
            Add("stream.fifo-no-bypass",fifo,"admitted epochs never decrease with immutable request IDs");
            Add("stream.complete-plan-bound",bounded,"every admitted body has a finite complete route within the horizon");
            var invalid=new StreamWorld(0,0,0);invalid.Request(1+12*32,10+12*32,.6f);invalid.Request(1+12*32,30+12*32,.35f);invalid.Begin();
            for(int t=0;t<150;t++){invalid.Finish();invalid.Begin();}
            Add("stream.reject-and-continue",invalid.rejected==1&&invalid.completed==1&&invalid.jobs[0].rejected==0,"unreachable request has an explicit disposition and does not silently block younger work");
            var terminal=new StreamAudit();terminal.Observe(map,new List<StreamSegment>{new StreamSegment{id=0,from=new Vector2(6,6),to=new Vector2(7.5f,6),radius=.6f,terminal=true},new StreamSegment{id=1,from=new Vector2(7.5f,6),to=new Vector2(6,6),radius=.35f}});
            Add("stream.independent-terminal",terminal.pairPenetrations>0,"independent auditor retains a body's final segment");
            var unequal=new StreamAudit();unequal.Observe(map,new List<StreamSegment>{new StreamSegment{id=0,from=new Vector2(6,6),to=new Vector2(6,6),radius=.6f},new StreamSegment{id=1,from=new Vector2(7,6),to=new Vector2(7,6),radius=.6f}});
            Add("stream.independent-radii",unequal.pairPenetrations>0,"independent auditor cannot substitute a fixed small diameter");
            var watch=new StreamAudit();var waiting=new StreamWorld(0,0,0);waiting.Request(33,34,.2f);waiting.epoch=481;watch.Watch(waiting);
            Add("stream.pending-watchdog",watch.deadlineViolations==1,"per-ID monitoring includes a never-spawned request");
            var stuck=new StreamAudit();var stationary=new List<StreamSegment>{new StreamSegment{id=0,from=new Vector2(6,6),to=new Vector2(6,6),radius=.2f}};
            for(int t=0;t<12;t++)stuck.Observe(map,stationary);
            Add("stream.global-watchdog",stuck.maximumGlobalStall==6,"stationary active-body control triggers the global no-motion signal");
            var auditedWorld=new StreamWorld(2,2,20,3);var audit=new StreamAudit();auditedWorld.Begin();
            for(int t=0;t<250;t++){auditedWorld.Finish();audit.Observe(auditedWorld.map,auditedWorld.last);audit.Watch(auditedWorld);auditedWorld.Begin();}
            Add("stream.continuous-geometry",audit.GeometrySafe&&auditedWorld.completed==40,"independent continuous-segment audit covers births, waits, crossings and arrivals");
            return rows;
        }
    }
}
