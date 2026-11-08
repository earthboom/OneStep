using System;
using System.Collections.Generic;
using UnityEngine;

namespace TechniqueLab
{
    public static class CrowdChecks
    {
        static CheckResult Check(string name,bool pass,string detail)
        {return new CheckResult{name=name,passed=pass,detail=detail};}
        public static List<CheckResult> Run()
        {
            var checks=new List<CheckResult>();
            var w=new CrowdWorld(24,16,1);w.Place(0,w.doorA-1);
            for(int t=0;t<4;t++)w.Step(1f/60);
            var before=w.agents[0].position;int id=w.agents[0].id;w.Close(w.doorA);
            checks.Add(Check("dynamic.close-preserves-pose",w.agents[0].id==id&&w.agents[0].position==before,"close must preserve continuous pose and ID"));
            checks.Add(Check("dynamic.close-occupied-deferred",w.Pending(w.doorA)&&!w.Solid(w.doorA),"reserved doorway waits for occupant, not an immediate solid"));
            checks.Add(Check("dynamic.close-invalidates-routes",w.RouteBlocked(w.doorA)&&w.Fresh,"new routes avoid pending close and field is fresh"));
            for(int t=0;t<180;t++)w.Step(1f/60);
            checks.Add(Check("dynamic.close-drains",w.Solid(w.doorA)&&!w.Pending(w.doorA),"existing traveler must leave and close must commit"));
            w.Open(w.doorA);checks.Add(Check("dynamic.reopen",!w.Solid(w.doorA)&&!w.RouteBlocked(w.doorA)&&w.Fresh,"reopen refreshes routing"));
            var dense=new CrowdWorld(24,16,2);dense.Place(0,4*24+10);dense.Place(1,4*24+11);
            float minimum=float.PositiveInfinity;
            for(int t=0;t<120;t++)
            {dense.Step(1f/60);if(!dense.agents[0].arrived&&!dense.agents[1].arrived)minimum=Mathf.Min(minimum,Vector2.Distance(dense.agents[0].position,dense.agents[1].position));}
            checks.Add(Check("dynamic.following-separation",minimum>=2*CrowdWorld.Radius-.0001f&&dense.agents[0].position.x>10,"following movers advance without overlap"));
            var blocked=new CrowdWorld(24,16,1);blocked.Place(0,4*24+10);blocked.Close(blocked.doorA);blocked.Close(blocked.doorB);
            var start=blocked.agents[0].position;for(int t=0;t<60;t++)blocked.Step(1f/60);
            checks.Add(Check("dynamic.unreachable-waits",blocked.agents[0].position==start,"no path waits safely without reset"));
            blocked.Open(blocked.doorA);for(int t=0;t<600;t++)blocked.Step(1f/60);
            checks.Add(Check("dynamic.reachable-resumes",blocked.arrived==1,"reopen resumes and completes the original agent"));
            foreach(int width in new[]{24,32})
            {
                var crateWorld=new CrowdWorld(width,16,1);crateWorld.Place(0,2*width+2);int crate=-1;bool valid=true;string detail="40 repeated relocations remain valid floor cells";
                try{for(int i=0;i<40;i++)crate=crateWorld.RelocateCrate(crate);}catch(Exception e){valid=false;detail=e.Message;}
                checks.Add(Check("dynamic.repeated-crate-"+width,valid,detail));
            }
            var terminal=new CrowdWorld(24,16,2);terminal.Place(0,terminal.goal-1);terminal.Place(1,terminal.goal);
            var terminalAudit=new CrowdAudit(terminal);terminal.agents[0].position=terminal.Center(terminal.goal);terminal.agents[0].arrived=true;
            terminalAudit.Observe(terminal,1f/3);
            checks.Add(Check("dynamic.audit-arrival-segment",terminalAudit.pairPenetrations>0,"controlled overlap on terminal segment must be observed even after arrival removal"));
            if(Application.isPlaying)
            {
                var root=new GameObject("Paused obstacle regression");var camera=new GameObject("Test camera").AddComponent<Camera>();camera.transform.SetParent(root.transform);camera.enabled=false;
                var runner=root.AddComponent<DynamicRunner>();runner.report=new DynamicReport();runner.view=root.AddComponent<DynamicView>();runner.view.cameraView=camera;
                var materials=new Material[6];for(int i=0;i<6;i++)materials[i]=new Material(Shader.Find("Unlit/Color"));runner.view.materials=materials;
                var pausedWorld=DynamicRunner.Spawn(24,16,1);runner.view.Configure(pausedWorld);runner.TogglePause();runner.SetObstacle(pausedWorld.doorA,true);
                var center=pausedWorld.Center(pausedWorld.doorA);
                bool synced=Physics.CheckSphere(new Vector3(center.x,.5f,center.y),.1f,1<<10,QueryTriggerInteraction.Ignore);
                checks.Add(Check("dynamic.paused-native-sync",synced,"paused public close control must immediately update visible obstacle/native collider"));
                root.SetActive(false);UnityEngine.Object.Destroy(root);foreach(var material in materials)UnityEngine.Object.Destroy(material);
            }
            return checks;
        }
    }
}
