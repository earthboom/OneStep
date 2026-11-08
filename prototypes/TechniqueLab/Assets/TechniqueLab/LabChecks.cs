using System;
using System.Collections.Generic;
using UnityEngine;

namespace TechniqueLab
{
    [Serializable] public class CheckResult { public string name,detail; public bool passed; }
    public static class LabChecks
    {
        static List<CheckResult> results;
        static void Expect(string name,bool condition,string detail)
        { results.Add(new CheckResult{name=name,passed=condition,detail=detail}); }
        public static List<CheckResult> Run()
        {
            results=new List<CheckResult>();
            foreach(int fps in new[]{30,60,144})
            {
                float x=0;for(int i=0;i<fps*2;i++)x=CameraDamping.Step(x,10,4,1f/fps);
                float expected=10*(1-Mathf.Exp(-8));
                Expect("camera.stationary."+fps,Mathf.Abs(x-expected)<=0.0001f,"actual="+x+" expected="+expected);
            }
            float hitch=0;foreach(float dt in new[]{0.01f,0.07f,0.35f,0.02f,0.55f,1f})hitch=CameraDamping.Step(hitch,10,4,dt);
            Expect("camera.hitch",Mathf.Abs(hitch-10*(1-Mathf.Exp(-8)))<=0.0001f,"actual="+hitch);
            Expect("camera.zero-dt",CameraDamping.Step(3,10,4,0)==3,"zero dt must preserve current position");
            CheckShooting(); CheckPaths(); return results;
        }
        public static GameObject MakeBox(string name,Vector3 position,Vector3 size,int layer)
        {
            var go=GameObject.CreatePrimitive(PrimitiveType.Cube);go.name=name;go.layer=layer;
            go.transform.position=position;go.transform.localScale=size;return go;
        }
        static void CheckShooting()
        {
            var wall=MakeBox("CheckWall",new Vector3(1,1,-1),new Vector3(0.7f,2,0.4f),ShotResolver.WallLayer);
            var target=MakeBox("CheckTarget",new Vector3(0,1,8),Vector3.one,ShotResolver.TargetLayer);
            var camera=new Vector3(0,2,-6);var muzzle=new Vector3(1,1,-3);var root=new Vector3(0,1,-3);
            var direction=(target.transform.position-camera).normalized;
            Physics.SyncTransforms();
            var naive=ShotResolver.CameraOnly(camera,direction,50);var actual=ShotResolver.Resolve(camera,direction,root,muzzle,50);
            Expect("shot.control.camera-only-wall",naive.hitTarget,"sensitivity control: camera sees target beyond offset cover");
            Expect("shot.muzzle-wall",actual.blocked&&!actual.hitTarget,"camera intent must not bypass muzzle cover");
            wall.transform.position=new Vector3(5,1,-1);Physics.SyncTransforms();
            actual=ShotResolver.Resolve(camera,direction,root,muzzle,50);
            Expect("shot.open",actual.hitTarget&&!actual.blocked,"open muzzle path must hit target");
            wall.transform.position=muzzle;Physics.SyncTransforms();
            actual=ShotResolver.Resolve(camera,direction,root,muzzle,50);
            Expect("shot.origin-inside",actual.blocked&&!actual.hitTarget,"origin overlap must not exploit raycast inside behavior");
            wall.transform.position=new Vector3(0.5f,1,-3);wall.transform.localScale=new Vector3(0.2f,2,1);Physics.SyncTransforms();
            actual=ShotResolver.Resolve(camera,direction,root,muzzle,50);
            Expect("shot.root-to-muzzle",actual.blocked&&!actual.hitTarget,"animated muzzle beyond cover must not bypass root obstruction");
            wall.SetActive(false);target.GetComponent<Collider>().isTrigger=true;Physics.SyncTransforms();
            Expect("shot.ignore-triggers",!ShotResolver.Resolve(camera,direction,root,muzzle,50).hitTarget,"triggers excluded explicitly");
            target.GetComponent<Collider>().isTrigger=false;target.layer=0;Physics.SyncTransforms();
            Expect("shot.layer-mask",!ShotResolver.Resolve(camera,direction,root,muzzle,50).hitTarget,"unrelated layer excluded");
            wall.SetActive(false);target.SetActive(false);
            if(Application.isPlaying){UnityEngine.Object.Destroy(wall);UnityEngine.Object.Destroy(target);}
            else{UnityEngine.Object.DestroyImmediate(wall);UnityEngine.Object.DestroyImmediate(target);}
            Physics.SyncTransforms();
        }
        static void CheckPaths()
        {
            var g=new WeightedGraph(4);g.AddEdge(0,1,18);g.AddEdge(1,3,2);g.AddEdge(0,2,2);g.AddEdge(2,3,6);
            var f=new WeightedField(4);f.Compute(g,3);
            Expect("path.weighted",f.distance[0]==8&&f.Next(g,0)==2,"expected cost 8 via node 2; not min remaining cost alone");
            var z=new WeightedGraph(3);z.AddEdge(0,1,0);z.AddEdge(1,0,0);z.AddEdge(1,2,4);z.AddEdge(0,2,5);
            var field=new WeightedField(3);field.Compute(z,2);
            Expect("path.zero-cycle",field.distance[0]==4&&Reaches(z,field,0,2),"cost 4 with acyclic next hops");
            var d=new WeightedGraph(4);d.AddEdge(0,1,3);d.AddEdge(1,0,40);d.AddEdge(1,2,2);
            var df=new WeightedField(4);df.Compute(d,2);
            Expect("path.directed",df.distance[0]==5,"reverse search must keep original directed cost");
            Expect("path.unreachable",float.IsPositiveInfinity(df.distance[3])&&df.Next(d,3)==-1,"unreachable has no successor");
            d.SetBlocked(1,true);Expect("path.invalidated",!df.IsValidFor(d),"topology change invalidates cached field");
            bool rejected=false;try{df.Next(d,0);}catch(InvalidOperationException){rejected=true;}
            Expect("path.stale-rejected",rejected,"consumer rejects stale field");
            df.Compute(d,2);Expect("path.closed",float.IsPositiveInfinity(df.distance[0]),"closed route must be unreachable after rebuild");
            var random=new System.Random(1591);bool fields=true,astar=true;
            for(int run=0;run<16;run++)
            {
                var graph=new WeightedGraph(10);var costs=new float[10,10];
                for(int i=0;i<10;i++)for(int j=0;j<10;j++)costs[i,j]=i==j?0:float.PositiveInfinity;
                for(int i=0;i<10;i++)for(int j=0;j<10;j++)if(i!=j&&random.NextDouble()<0.25)
                {float w=random.Next(0,8);graph.AddEdge(i,j,w);costs[i,j]=w;}
                // Independent all-pairs dynamic programming oracle, not the implementation's heap.
                for(int k=0;k<10;k++)for(int i=0;i<10;i++)for(int j=0;j<10;j++)costs[i,j]=Math.Min(costs[i,j],costs[i,k]+costs[k,j]);
                var shared=new WeightedField(10);shared.Compute(graph,9);var workspace=new AStarWorkspace(10);
                for(int i=0;i<10;i++)
                {fields&=shared.distance[i]==costs[i,9]&&(float.IsPositiveInfinity(costs[i,9])||Reaches(graph,shared,i,9));astar&=workspace.Cost(graph,i,9)==costs[i,9];}
            }
            Expect("path.oracle-fields",fields,"160 directed/zero-cost source comparisons against Floyd-Warshall and termination");
            Expect("path.oracle-astar",astar,"160 independent search comparisons against Floyd-Warshall");
            var owner=new WeightedGraph(2);owner.AddEdge(0,1,1);
            var other=new WeightedGraph(2);other.AddEdge(0,1,9);
            var bound=new WeightedField(2);bound.Compute(owner,1);
            Expect("path.graph-identity",!bound.IsValidFor(other),"equal revision counters on distinct graphs must not validate a cached field");
        }
        static bool Reaches(WeightedGraph graph,WeightedField field,int start,int goal)
        {int n=start;for(int i=0;i<=graph.Count;i++){if(n==goal)return true;n=field.Next(graph,n);if(n<0)return false;}return false;}
    }
}
